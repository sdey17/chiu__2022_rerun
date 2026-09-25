"""
model_corrected.py
==================
One generic PyMC model for all four PFAS that follows Chiu et al.'s MCSim
input files (the `.in.R` files in data/) exactly. It also has switches
that bring back each deviation found in the original model_*.py scripts,
so you can measure how much each one moves the half-life.

    python model_corrected.py PFOA                 # faithful replication
    python model_corrected.py PFOA --shared-sc     # + deviation 1
    python model_corrected.py PFOA --drop-t0       # + deviation 2
    python model_corrected.py PFNA --old-priors    # + deviation 3 (PFNA only)
    python model_corrected.py PFOS --no-truncate   # + deviation 4
    python model_corrected.py all                  # faithful, all four

Deviations of the original scripts from Chiu's model (see ANALYSIS.md):
  1. --shared-sc   : one M_ln_Cbgd_sc / M_ln_C_0_sc shared by every study.
                     MCSim declares them in the "Studies" Level, which gives
                     ONE INSTANCE PER STUDY (the .out headers list
                     M_ln_Cbgd_sc(1.1) ... M_ln_Cbgd_sc(1.15)).
  2. --drop-t0     : use only the last Data() value of each individual.
                     Every individual time-course record has TWO data
                     points, at t=0 and at the follow-up, and both enter
                     the likelihood.
  3. --old-priors  : PFNA priors used by model_pfna.py
                     (M_ln_k mu=-1.60944, M_ln_Vd mu=-1.60944,
                     V_ln_k LN(0.12, 1.335)) instead of those in Chiu's PFNA file
                     (-1.80181, -1.77196, LN(0.20, 1.275)).
  4. --no-truncate : dosing segments that START AFTER the blood draw
                     (all 110 Arnsberg PFOA people, all 18 Decatur PFOS
                     people) are simulated anyway, followed by a
                     negative-duration "segment" back to the draw time.
"""

import argparse
import time

import numpy as np
import pymc as pm
import pytensor.tensor as pt
import arviz as az

from parse_chiu_data import build_dataframe

# Hyper-priors copied from the top Level{} of each Chiu .in.R file.
# (V_ln_k: ("invgamma", shape, scale) or ("lognormal", GM, GSD), MCSim convention.)
PRIORS = {
    "PFOA":  dict(M_ln_k=(-1.8971, 0.4055), M_ln_Vd=(-1.7720, 0.2624),
                  V_ln_k=("invgamma", 9, 0.75), SD_ln_Vd=0.2),
    "PFOS":  dict(M_ln_k=(-1.8971, 0.4055), M_ln_Vd=(-1.46968, 0.2624),
                  V_ln_k=("lognormal", 0.2024, 1.261), SD_ln_Vd=0.17),
    "PFNA":  dict(M_ln_k=(-1.80181, 0.4055), M_ln_Vd=(-1.77196, 0.2624),
                  V_ln_k=("lognormal", 0.2000, 1.275), SD_ln_Vd=0.17),
    "PFHxS": dict(M_ln_k=(-2.03422, 0.4055), M_ln_Vd=(-1.38629, 0.2624),
                  V_ln_k=("lognormal", 0.20, 1.275), SD_ln_Vd=0.17),
}
# What model_pfna.py used (deviation 3)
OLD_PFNA_PRIORS = dict(M_ln_k=(-1.60944, 0.4055), M_ln_Vd=(-1.60944, 0.2624),
                       V_ln_k=("lognormal", 0.12, 1.335), SD_ln_Vd=0.17)

# Chiu et al. 2022, EHP 130(12):127001, Table 3 -- population GM half-life (yr)
PAPER = {"PFOA": (3.14, 2.69, 3.73), "PFOS": (3.36, 2.52, 4.42),
         "PFNA": (2.35, 1.65, 3.16), "PFHxS": (8.30, 5.38, 13.5)}

# Fixed values, identical in all four .in.R files
M_ln_DWI = -4.3955
SD_ln_DWI = 0.888
SD_ln_Cbgd_sc = 1.0
SD_ln_C_0_sc = 1.0


def dose_matrices(rows, truncate=True):
    """
    Pad each person's NDoses() schedule into (N, M) arrays of segment
    start, end and concentration, ending at the blood-draw time tq.

    truncate=True  : segments are clipped to [0, tq] (what MCSim does --
                     it only integrates the ODE up to the Print() time).
    truncate=False : reproduces the original scripts' boundaries
                     `dose_times + [tq]`, which can go past tq and back.
    """
    M = int(max(r["dwc_n"] for r in rows))
    s = np.zeros((len(rows), M))
    e = np.zeros((len(rows), M))
    c = np.zeros((len(rows), M))
    tq = np.zeros(len(rows))
    for i, r in enumerate(rows):
        times, conc, t_end = list(r["dwc_times"]), list(r["dwc_conc"]), r["print_times"][-1]
        tq[i] = t_end
        if truncate:
            bounds = [min(t, t_end) for t in times] + [t_end]
        else:
            bounds = times + [t_end]
        n = len(conc)
        s[i, :n] = bounds[:n]
        e[i, :n] = bounds[1:n + 1]
        c[i, :n] = conc
        s[i, n:] = e[i, n:] = t_end  # zero-length padding
    return s, e, c, tq


def build_model(chem, shared_sc=False, drop_t0=False, old_priors=False, truncate=True):
    df, _ = build_dataframe(chem)
    fit = df[df["in_fit"]].reset_index(drop=True)
    pri = OLD_PFNA_PRIORS if (old_priors and chem == "PFNA") else PRIORS[chem]

    studies = list(dict.fromkeys(fit["study"]))
    study_idx = {s: i for i, s in enumerate(studies)}
    n_sc = 1 if shared_sc else len(studies)
    sc = (lambda st: 0) if shared_sc else (lambda st: study_idx[st])

    with pm.Model() as model:
        # ---- population level (top Level{}) ----
        M_ln_k = pm.Normal("M_ln_k", *pri["M_ln_k"])
        M_ln_Vd = pm.Normal("M_ln_Vd", *pri["M_ln_Vd"])
        kind, a, b = pri["V_ln_k"]
        if kind == "invgamma":
            V_ln_k = pm.InverseGamma("V_ln_k", alpha=a, beta=b)
        else:  # MCSim LogNormal(GM, GSD)
            V_ln_k = pm.LogNormal("V_ln_k", mu=np.log(a), sigma=np.log(b))
        SD_ln_Vd = pm.HalfNormal("SD_ln_Vd", sigma=pri["SD_ln_Vd"])
        SD_ln_k = pt.sqrt(V_ln_k)
        pm.Deterministic("halflife_pop", np.log(2) / pt.exp(M_ln_k))
        pm.Deterministic("GSD_k", pt.exp(SD_ln_k))

        gsd = {}
        for ep in ["Cserum", "Cbgd_Css", "M_Cserum", "M_Cbgd_Css"]:
            ep_rows = fit["endpoint"].isin([ep, ep + "_t"] if ep == "Cserum" else [ep])
            if ep_rows.any():
                lg = pm.Uniform(f"log_GSD_{ep}", np.log(1.1), np.log(10.0))  # LogUniform(1.1, 10)
                gsd[ep] = pm.Deterministic(f"GSD_{ep}", pt.exp(lg))

        # ---- study level ("Studies" Level{}): one instance per study ----
        M_ln_Cbgd_sc = pm.Normal("M_ln_Cbgd_sc", -0.22314, 0.4055, shape=n_sc)
        M_ln_C_0_sc = pm.Normal("M_ln_C_0_sc", 0.0, 0.4055, shape=n_sc)

        # one DWC_belowMRL per study that has one
        dwc_mrl = {}
        for st in studies:
            g = fit[(fit["study"] == st) & (fit["dwc_type"] == "below_MRL")]
            if len(g):
                j = study_idx[st]
                dwc_mrl[st] = pm.Uniform(f"DWC_belowMRL_{j}", 0.0, float(g["dwc_mrl"].iloc[0]))

        def indiv(prefix, g):
            """Individual draws (non-centred), MCSim Initialize{} block."""
            n = len(g)
            sidx = np.array([sc(s) for s in g["study"]])
            z = {v: pm.Normal(f"{prefix}_z_{v}", 0, 1, shape=n) for v in ["k", "Vd", "DWI", "Cbgd", "C0"]}
            k = pt.exp(M_ln_k + SD_ln_k * z["k"])
            Vd = pt.exp(M_ln_Vd + SD_ln_Vd * z["Vd"])
            DWI = pt.exp(M_ln_DWI + SD_ln_DWI * z["DWI"])
            Cbgd = g["Cbgd_in_gm"].values * pt.exp(
                M_ln_Cbgd_sc[sidx] + SD_ln_Cbgd_sc * np.log(g["Cbgd_in_gsd"].values) * z["Cbgd"])
            C0 = g["C_0_in_gm"].values * pt.exp(
                M_ln_C_0_sc[sidx] + SD_ln_C_0_sc * np.log(g["C_0_in_gsd"].values) * z["C0"])
            return k, Vd, DWI, Cbgd, C0

        def add_obs(name, pred_matrix, g, sigma):
            """Likelihood for every Data() value (or only the last with drop_t0)."""
            obs, pred = [], []
            for i, (_, r) in enumerate(g.iterrows()):
                cols = [len(r["data_values"]) - 1] if drop_t0 else range(len(r["data_values"]))
                for j in cols:
                    obs.append(r["data_values"][j])
                    pred.append(pred_matrix(i, j))
            pm.LogNormal(name, mu=pt.log(pt.stack(pred)), sigma=pt.log(sigma), observed=np.array(obs))

        # ---- individual time-course, constant DWC (endpoint Cserum) ----
        g = fit[fit["endpoint"] == "Cserum"].reset_index(drop=True)
        if len(g):
            k, Vd, DWI, Cbgd, C0 = indiv("cs", g)
            DWC = pt.stack([dwc_mrl[s] if t == "below_MRL" else float(v)
                            for s, t, v in zip(g["study"], g["dwc_type"], g.get("dwc_value", [np.nan] * len(g)))])
            Css = DWI * 365.25 * DWC / (k * Vd)
            T = np.array([r["print_times"] for _, r in g.iterrows()])  # (n, n_times)
            ekt = pt.exp(-k[:, None] * T)
            C = Cbgd[:, None] + (C0 - Cbgd)[:, None] * ekt + Css[:, None] * (1 - ekt)
            add_obs("obs_Cserum", lambda i, j: C[i, j], g, gsd["Cserum"])

        # ---- individual time-course, time-varying DWC (endpoint Cserum_t) ----
        g = fit[fit["endpoint"] == "Cserum_t"].reset_index(drop=True)
        if len(g):
            k, Vd, DWI, Cbgd, C0 = indiv("ct", g)
            rows = [r for _, r in g.iterrows()]
            s, e, c, tq = dose_matrices(rows, truncate=truncate)
            # Linear ODE dC/dt = DWI*365.25*DWC(t)/Vd + k(Cbgd - C): closed-form
            # superposition over piecewise-constant dose segments (equivalent to
            # the scan in model_pfoa.py, but vectorised).
            kk = k[:, None]
            dose = pt.sum(c * (pt.exp(-kk * (tq[:, None] - e)) - pt.exp(-kk * (tq[:, None] - s))), axis=1)
            C_end = Cbgd + (C0 - Cbgd) * pt.exp(-k * tq) + DWI * 365.25 / (k * Vd) * dose
            # Data times are exactly (0, tq): prediction at t=0 is C0.
            assert all(r["print_times"][0] == 0 and len(r["print_times"]) == 2 for r in rows)
            add_obs("obs_Cserum_t", lambda i, j: C0[i] if j == 0 else C_end[i], g, gsd["Cserum"])

        # ---- individual single measurement (endpoint Cbgd_Css) ----
        g = fit[fit["endpoint"] == "Cbgd_Css"].reset_index(drop=True)
        if len(g):
            k, Vd, DWI, Cbgd, _ = indiv("ss", g)
            t = np.array([r["print_times"][0] for _, r in g.iterrows()])
            C = Cbgd + DWI * 365.25 * g["dwc_value"].values / (k * Vd) * pt.exp(-k * t)
            add_obs("obs_Cbgd_Css", lambda i, j: C[i], g, gsd["Cbgd_Css"])

        # ---- population summary rows (CalcOutputs{} closed forms) ----
        def pop_pred(r, t):
            j = sc(r["study"])
            DWC = dwc_mrl[r["study"]] if r["dwc_type"] == "below_MRL" else float(r["dwc_value"])
            gm, gs = r["Cbgd_in_gm"], np.log(r["Cbgd_in_gsd"])
            c0m, c0s = r["C_0_in_gm"], np.log(r["C_0_in_gsd"])
            M_Cbgd = gm * pt.exp(M_ln_Cbgd_sc[j] + (SD_ln_Cbgd_sc * gs) ** 2 / 2)
            mu_Css = M_ln_DWI + np.log(365.25) + pt.log(DWC) - M_ln_k - M_ln_Vd
            V_Css = SD_ln_DWI ** 2 + V_ln_k + SD_ln_Vd ** 2
            M_Css = pt.exp(mu_Css + V_Css / 2)
            M_kt = -t * pt.exp(M_ln_k + V_ln_k / 2)
            V_kt = (pt.exp(V_ln_k) - 1) * M_kt ** 2
            M_Cbgd_expkt = pt.exp(np.log(gm) + M_ln_Cbgd_sc[j] + M_kt + ((SD_ln_Cbgd_sc * gs) ** 2 + V_kt) / 2)
            M_C0_expkt = pt.exp(np.log(c0m) + M_ln_C_0_sc[j] + M_kt + ((SD_ln_C_0_sc * c0s) ** 2 + V_kt) / 2)
            M_Css_expkt = pt.exp(mu_Css + M_kt + (V_Css + V_kt) / 2)
            if r["endpoint"] == "M_Cbgd_Css":
                return M_Cbgd + M_Css_expkt
            return M_Cbgd + M_C0_expkt - M_Cbgd_expkt + M_Css - M_Css_expkt

        for ep in ["M_Cserum", "M_Cbgd_Css"]:
            g = fit[fit["endpoint"] == ep].reset_index(drop=True)
            if len(g):
                preds, obs = [], []
                for _, r in g.iterrows():
                    for t, y in zip(r["print_times"], r["data_values"]):
                        preds.append(pop_pred(r, t))
                        obs.append(y)
                pm.LogNormal(f"obs_{ep}", mu=pt.log(pt.stack(preds)), sigma=pt.log(gsd[ep]),
                             observed=np.array(obs))
    return model, studies


def run(chem, draws=1000, tune=1000, chains=4, cores=4, seed=1, **flags):
    t0 = time.time()
    model, studies = build_model(chem, **flags)
    with model:
        idata = pm.sample(draws, tune=tune, chains=chains, cores=cores, target_accept=0.95,
                          random_seed=seed, progressbar=False)
    hl = idata.posterior["halflife_pop"].values.ravel()
    q = np.percentile(hl, [50, 2.5, 97.5])
    summ = az.summary(idata, var_names=["halflife_pop", "GSD_k", "M_ln_Cbgd_sc", "~z_"], filter_vars="like")
    n_div = int(idata.sample_stats["diverging"].sum())
    tag = ",".join(("no_truncate" if k == "truncate" else k) for k, v in flags.items()
                   if (v if k != "truncate" else not v)) or "faithful"
    p = PAPER[chem]
    print(f"\n{chem} [{tag}]  T1/2 = {q[0]:.2f} (95% CI {q[1]:.2f}, {q[2]:.2f})   "
          f"paper: {p[0]} ({p[1]}, {p[2]})   GSD_k={np.median(idata.posterior['GSD_k']):.2f}  "
          f"max r_hat={summ['r_hat'].max():.3f}  divergences={n_div}  ({time.time()-t0:.0f}s)")
    print("  study index -> Level:", {i: s[:40] for i, s in enumerate(studies)})
    return idata, q


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("chem", choices=list(PRIORS) + ["all"])
    ap.add_argument("--shared-sc", action="store_true")
    ap.add_argument("--drop-t0", action="store_true")
    ap.add_argument("--old-priors", action="store_true")
    ap.add_argument("--no-truncate", action="store_true")
    ap.add_argument("--draws", type=int, default=1000)
    ap.add_argument("--cores", type=int, default=4)
    ap.add_argument("--save", action="store_true", help="write model_<chem>_corrected.nc")
    a = ap.parse_args()
    for chem in (list(PRIORS) if a.chem == "all" else [a.chem]):
        idata, _ = run(chem, draws=a.draws, tune=a.draws, cores=a.cores,
                       shared_sc=a.shared_sc, drop_t0=a.drop_t0,
                       old_priors=a.old_priors, truncate=not a.no_truncate)
        if a.save:
            idata.to_netcdf(f"model_{chem.lower()}_corrected.nc")
