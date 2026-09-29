"""
Is the dose->clearance trend an artefact of follow-up duration?

The worry: if high-dose arms were followed for longer, they would capture
more of the slow terminal phase. Missing that phase in a short study makes
elimination look faster... but missing it also makes the *fitted* clearance
look different, so a dose/duration correlation could manufacture the trend.

This script asks three things of the raw data, before any modelling:

  1. Within each study, does follow-up length track dose?
  2. Is follow-up long relative to the fitted half-life? (Rule of thumb: you
     want to observe at least ~1 half-life, ideally 2-3.)
  3. Does adding follow-up duration to the dose regression kill the dose
     slope?

Usage:  python duration_check.py PFOA Male rat PFOA_Male_rat_2cmpt.nc
"""
import os
import sys

import numpy as np
import pandas as pd

from dose_analysis import load_dataset_clearance


def observed_windows(chem, sex, species):
    """Follow-up window and sampling density for each (study, dose, route)."""
    epa = os.environ["EPA_REPO"]
    sys.path.insert(0, epa)
    cwd = os.getcwd()
    os.chdir(os.path.join(epa, "pfas_notebooks"))
    try:
        from pfas_prep import PFAS
        prep = PFAS("../PFAS.db", pfas_file="../auxiliary/pfas_master.csv")
        d = prep.get_processed_data(chemical=chem, sex=sex, species=species)
    finally:
        os.chdir(cwd)
    g = d.groupby("dataset_str").agg(
        t_last=("time_cor", "max"), t_first=("time_cor", "min"),
        n_points=("time_cor", "size"), n_times=("time_cor", "nunique"))
    return g.reset_index().rename(columns={"dataset_str": "dataset"})



def equal_duration_slopes(df, route="gavage"):
    """
    Slope of ln(clearance) on ln(dose) using only dose contrasts where
    follow-up is IDENTICAL, so duration cannot explain the trend.

    For each study we take the largest group of datasets sharing one
    follow-up length, and fit within it.
    """
    import pymc as pm
    out, keep = [], []
    for study, g in df[df.route == route].groupby("study"):
        # biggest set of doses sharing an identical follow-up length
        counts = g.groupby("t_last").dose.nunique()
        if counts.max() < 2:
            continue
        t_keep = counts.idxmax()
        gg = g[g.t_last == t_keep].sort_values("dose")
        x = np.log(gg.dose.values) - np.log(gg.dose.values).mean()
        with pm.Model():
            a = pm.Normal("a", np.log(gg.clc_median).mean(), 3)
            beta = pm.Normal("beta", 0, 1)
            tau = pm.HalfNormal("tau", 0.5)
            pm.Normal("obs", mu=a + beta * x,
                      sigma=pm.math.sqrt(gg.ln_clc_sd.values ** 2 + tau ** 2),
                      observed=gg.ln_clc_mean.values)
            idata = pm.sample(2000, tune=2000, chains=4, cores=4,
                              target_accept=0.99, random_seed=1, progressbar=False)
        b = idata.posterior["beta"].values.ravel()
        out.append(dict(study=study, follow_up_d=t_keep, n_doses=len(gg),
                        dose_range=f"{gg.dose.min():g}-{gg.dose.max():g}",
                        beta=np.median(b), lo=np.percentile(b, 5),
                        hi=np.percentile(b, 95), p_negative=(b < 0).mean()))
        keep.append(gg)
    return pd.DataFrame(out), (pd.concat(keep) if keep else None)


if __name__ == "__main__":
    chem, sex, species, trace = sys.argv[1:5]
    clc, _ = load_dataset_clearance(trace)
    win = observed_windows(chem, sex, species)
    df = clc.merge(win, on="dataset", how="left")
    # how much of the elimination curve each study actually watched
    df["halflives_observed"] = df.t_last / df.halflife_d
    pd.set_option("display.width", 220)

    print("Follow-up versus dose and versus the fitted half-life:\n")
    print(df[["study", "route", "dose", "t_last", "n_points",
              "halflife_d", "halflives_observed", "clc_median"]]
          .round(3).to_string(index=False))

    print("\n1. Within-study correlation between ln(dose) and ln(follow-up):")
    for (study, route), g in df.groupby(["study", "route"]):
        if g.dose.nunique() < 2:
            continue
        r = np.corrcoef(np.log(g.dose), np.log(g.t_last))[0, 1]
        span = g.t_last.max() / g.t_last.min()
        print(f"   study {study} {route}: r = {r:+.2f} over {len(g)} doses; "
              f"follow-up spans {span:.2f}x "
              f"({g.t_last.min():.1f} to {g.t_last.max():.1f} d)")

    print("\n2. Half-lives observed (want >= 1, ideally 2-3):")
    short = df[df.halflives_observed < 1]
    print(f"   {len(short)} of {len(df)} datasets observed less than one half-life")
    if len(short):
        print(short[["study", "route", "dose", "t_last", "halflife_d",
                     "halflives_observed"]].round(2).to_string(index=False))

    print("\n3. Dose slope with and without follow-up duration as a covariate:")
    from dose_analysis import dose_slope
    base, used = dose_slope(df, "gavage")
    if base is None:
        print("   not enough within-study dose contrasts")
        sys.exit()
    b = base.posterior["beta"].values.ravel()
    print(f"   dose only:            beta = {np.median(b):+.3f} "
          f"(90% CI {np.percentile(b, 5):+.3f}, {np.percentile(b, 95):+.3f})")

    # same model plus a ln(follow-up) term, so the dose slope is what remains
    # after duration is accounted for
    import pymc as pm
    d = used.copy()
    sidx, studies = pd.factorize(d.study)
    x = np.log(d.dose.values) - np.log(d.dose.values).mean()
    z = np.log(d.t_last.values) - np.log(d.t_last.values).mean()
    with pm.Model():
        alpha = pm.Normal("alpha", np.log(d.clc_median).mean(), 3, shape=len(studies))
        beta = pm.Normal("beta", 0, 1)
        gamma = pm.Normal("gamma", 0, 1)
        tau = pm.HalfNormal("tau", 0.5)
        pm.Normal("obs", mu=alpha[sidx] + beta * x + gamma * z,
                  sigma=pm.math.sqrt(d.ln_clc_sd.values ** 2 + tau ** 2),
                  observed=d.ln_clc_mean.values)
        adj = pm.sample(2000, tune=2000, chains=4, cores=4, target_accept=0.99,
                        random_seed=1, progressbar=False)
    b2 = adj.posterior["beta"].values.ravel()
    g2 = adj.posterior["gamma"].values.ravel()
    print(f"   + follow-up covariate: beta = {np.median(b2):+.3f} "
          f"(90% CI {np.percentile(b2, 5):+.3f}, {np.percentile(b2, 95):+.3f})")
    print(f"                          gamma (duration) = {np.median(g2):+.3f} "
          f"(90% CI {np.percentile(g2, 5):+.3f}, {np.percentile(g2, 95):+.3f})")

    print("\n4. Slope using only dose contrasts at IDENTICAL follow-up:")
    eq, eq_rows = equal_duration_slopes(df)
    print(eq.round(3).to_string(index=False) if len(eq) else "   none available")
    if eq_rows is not None and eq_rows.study.nunique() > 1:
        pooled, _ = dose_slope(eq_rows, "gavage")
        bp = pooled.posterior["beta"].values.ravel()
        print(f"\n   pooled over those equal-duration subsets "
              f"({eq_rows.study.nunique()} studies / {len(eq_rows)} datasets): "
              f"beta = {np.median(bp):+.3f} "
              f"(90% CI {np.percentile(bp, 5):+.3f}, {np.percentile(bp, 95):+.3f})"
              f"   P(beta < 0) = {(bp < 0).mean():.2f}")

