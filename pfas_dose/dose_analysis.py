"""
Does clearance depend on dose?

The EPA model gives one clearance per "dataset", where a dataset is one
(study, dose, route). This script pulls those out and asks whether they
trend with dose.

Two ways of asking, both reported:

  1. Within-study dose ratios. For each study, compare clearance at each
     dose to the lowest dose in that SAME study. Comparing across studies
     would confound dose with laboratory. This is what their own
     ROPE_compare does.

  2. Meta-regression of ln(clearance) on ln(dose), with a separate
     intercept per study, so only within-study dose contrasts drive the
     slope. Each dataset's clearance carries its own uncertainty from the
     PK fit, which is propagated rather than ignored.

     slope = 0  -> linear kinetics, clearance independent of dose
     slope < 0  -> clearance falls as dose rises (saturation); half-life
                   grows with dose
     slope > 0  -> clearance rises with dose (e.g. saturable reabsorption)

Usage:  python dose_analysis.py PFOA_Male_rat_2cmpt.nc
"""
import re
import sys

import arviz as az
import numpy as np
import pandas as pd
import pymc as pm


def load_dataset_clearance(path):
    """One row per dataset: study, dose, route, and the posterior of ln(CLC)."""
    idata = az.from_netcdf(path)
    clc = idata.posterior["CLC [indiv]"]          # dims: chain, draw, dataset
    rows = []
    for name in clc.coords["dataset"].values:
        # dataset labels look like "6302380-1.0 mg/kg-gavage"
        study, dose, route = re.match(r"(\d+)-([\d.]+) mg/kg-(\w+)", name).groups()
        draws = np.log(clc.sel(dataset=name).values.ravel())
        rows.append(dict(dataset=name, study=study, dose=float(dose), route=route,
                         ln_clc_mean=draws.mean(), ln_clc_sd=draws.std(),
                         clc_median=np.exp(np.median(draws)),
                         clc_lo=np.exp(np.percentile(draws, 5)),
                         clc_hi=np.exp(np.percentile(draws, 95))))
    df = pd.DataFrame(rows).sort_values(["study", "route", "dose"]).reset_index(drop=True)
    df["halflife_d"] = np.log(2) / (df.clc_median / _vdss_median(idata))
    return df, idata


def _vdss_median(idata):
    """Population Vdss, used only to turn clearance into an approximate half-life."""
    return float(np.median(idata.posterior["Vdss [pop]"].values))


def within_study_ratios(df):
    """Clearance at each dose / clearance at the lowest dose of the same study."""
    out = []
    for (study, route), g in df.groupby(["study", "route"]):
        if len(g) < 2:
            continue
        ref = g.iloc[0]                       # lowest dose in this study+route
        for _, row in g.iloc[1:].iterrows():
            # ratio of two lognormals -> lognormal; combine the log-scale SDs
            ln_ratio = row.ln_clc_mean - ref.ln_clc_mean
            sd = np.hypot(row.ln_clc_sd, ref.ln_clc_sd)
            out.append(dict(study=study, route=route, dose_lo=ref.dose, dose_hi=row.dose,
                            fold_dose=row.dose / ref.dose, ratio=np.exp(ln_ratio),
                            ratio_lo=np.exp(ln_ratio - 1.645 * sd),
                            ratio_hi=np.exp(ln_ratio + 1.645 * sd),
                            # "practically equivalent" band used in their ROPE plots
                            within_0812=bool(0.8 < np.exp(ln_ratio) < 1.2)))
    return pd.DataFrame(out)


def dose_slope(df, route=None):
    """
    Meta-regression: ln(CLC_d) ~ study intercept + beta * ln(dose_d / geomean dose).

    Each dataset's ln(CLC) is an estimate with known uncertainty (ln_clc_sd from
    the PK fit), so the likelihood adds that to a between-dataset scatter term.
    Study intercepts mean beta is identified only by within-study dose contrasts.
    """
    d = df if route is None else df[df.route == route]
    d = d[d.study.map(d.groupby("study").dose.nunique()) > 1]   # studies with >1 dose
    if len(d) < 3:
        return None, d
    sidx, studies = pd.factorize(d.study)
    x = np.log(d.dose.values) - np.log(d.dose.values).mean()

    with pm.Model() as m:
        alpha = pm.Normal("alpha", np.log(d.clc_median).mean(), 3, shape=len(studies))
        beta = pm.Normal("beta", 0, 1)                     # the slope we care about
        tau = pm.HalfNormal("tau", 0.5)                    # extra dataset scatter
        mu = alpha[sidx] + beta * x
        # each dataset's own PK uncertainty, plus a shared between-dataset term
        sigma = pm.math.sqrt(d.ln_clc_sd.values ** 2 + tau ** 2)
        pm.Normal("obs", mu=mu, sigma=sigma, observed=d.ln_clc_mean.values)
        idata = pm.sample(2000, tune=2000, chains=4, cores=4,
                          target_accept=0.99, random_seed=1, progressbar=False)
    return idata, d


if __name__ == "__main__":
    path = sys.argv[1]
    df, _ = load_dataset_clearance(path)
    pd.set_option("display.width", 200)
    print("Per-dataset clearance (L/kg/day), sorted by study then dose:\n")
    print(df[["study", "route", "dose", "clc_median", "clc_lo", "clc_hi",
              "halflife_d"]].to_string(index=False))

    ratios = within_study_ratios(df)
    if len(ratios):
        print("\nWithin-study comparisons against the lowest dose of that study:\n")
        print(ratios.to_string(index=False))

    for route in ["gavage", None]:
        idata, used = dose_slope(df, route)
        label = route or "both routes"
        if idata is None:
            print(f"\n[{label}] not enough within-study dose contrasts")
            continue
        b = idata.posterior["beta"].values.ravel()
        print(f"\n[{label}] slope of ln(clearance) on ln(dose), "
              f"{used.study.nunique()} studies / {len(used)} datasets:")
        print(f"  beta = {np.median(b):+.3f}  (90% CI {np.percentile(b, 5):+.3f}, "
              f"{np.percentile(b, 95):+.3f})   P(beta < 0) = {(b < 0).mean():.2f}")
        print(f"  a 10x dose change multiplies clearance by "
              f"{10 ** np.median(b):.2f} (90% CI {10 ** np.percentile(b, 5):.2f}, "
              f"{10 ** np.percentile(b, 95):.2f})")
