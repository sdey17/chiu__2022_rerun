"""
Chiu et al. 2022 one-compartment PFAS model, rewritten in PyMC.

    python model.py PFNA        # one chemical (PFOA, PFOS, PFNA or PFHxS)
    python model.py all         # all four, then a summary table

The equations are copied from Chiu's MCSim model file; the data and priors
come from data/*.in.R. Units: time in years, concentrations in ug/L,
volume of distribution Vd in L/kg, elimination rate k per year.
"""
import sys

import numpy as np
import pymc as pm
import pytensor.tensor as pt

from parse_chiu_data import load

# Priors from the top of each .in.R file.
#   M_ln_k, M_ln_Vd: Normal(mean, sd) for the log of the population GM
#   V_ln_k: variance of ln(k) between people; SD_ln_Vd: SD of ln(Vd) between people
PRIORS = {
    "PFOA":  dict(M_ln_k=(-1.8971, 0.4055), M_ln_Vd=(-1.7720, 0.2624),
                  V_ln_k=("InverseGamma", 9, 0.75), SD_ln_Vd=0.20),
    "PFOS":  dict(M_ln_k=(-1.8971, 0.4055), M_ln_Vd=(-1.46968, 0.2624),
                  V_ln_k=("LogNormal", 0.2024, 1.261), SD_ln_Vd=0.17),
    "PFNA":  dict(M_ln_k=(-1.80181, 0.4055), M_ln_Vd=(-1.77196, 0.2624),
                  V_ln_k=("LogNormal", 0.20, 1.275), SD_ln_Vd=0.17),
    "PFHxS": dict(M_ln_k=(-2.03422, 0.4055), M_ln_Vd=(-1.38629, 0.2624),
                  V_ln_k=("LogNormal", 0.20, 1.275), SD_ln_Vd=0.17),
}

# Published population half-life, median (95% CI), from Table 3 of the paper
PAPER = {"PFOA": (3.14, 2.69, 3.73), "PFOS": (3.36, 2.52, 4.42),
         "PFNA": (2.35, 1.65, 3.16), "PFHxS": (8.30, 5.38, 13.5)}

# Drinking-water intake per kg body weight is FIXED in Chiu's model, not fitted
LN_DWI_MEAN, LN_DWI_SD = -4.3955, 0.888     # log(L/kg per day)
DAYS = 365.25                                # intake is per day, k is per year


def build_model(chem):
    df = load(chem)
    if "dwc" not in df:
        df["dwc"] = np.nan
    studies = list(dict.fromkeys(df["study"]))
    df["s"] = df["study"].map(studies.index)          # study number, 0, 1, 2, ...
    p = PRIORS[chem]

    with pm.Model() as model:
        # ---------- 1. Population level: shared by everyone ----------
        M_ln_k = pm.Normal("M_ln_k", *p["M_ln_k"])
        M_ln_Vd = pm.Normal("M_ln_Vd", *p["M_ln_Vd"])
        dist, gm, gsd = p["V_ln_k"]
        if dist == "InverseGamma":
            V_ln_k = pm.InverseGamma("V_ln_k", alpha=gm, beta=gsd)
        else:                    # MCSim writes LogNormal as (GM, GSD)
            V_ln_k = pm.LogNormal("V_ln_k", mu=np.log(gm), sigma=np.log(gsd))
        SD_ln_Vd = pm.HalfNormal("SD_ln_Vd", p["SD_ln_Vd"])

        pm.Deterministic("halflife", np.log(2) / pt.exp(M_ln_k))   # the answer we want
        pm.Deterministic("halflife_GSD", pt.exp(pt.sqrt(V_ln_k)))  # spread between people
        pm.Deterministic("Vd", pt.exp(M_ln_Vd))

        # Measurement error, one per data type. LogUniform(1.1, 10) prior.
        def error_gsd(name):
            return pt.exp(pm.Uniform(f"log_GSD_{name}", np.log(1.1), np.log(10)))

        # ---------- 2. Study level: one value PER STUDY ----------
        # Background serum level scale and initial level scale.
        n = len(studies)
        M_ln_Cbgd_sc = pm.Normal("M_ln_Cbgd_sc", -0.22314, 0.4055, shape=n)
        M_ln_C_0_sc = pm.Normal("M_ln_C_0_sc", 0.0, 0.4055, shape=n)

        # Water concentration of each record: a known number, or, when it was
        # only reported as "below the MRL", a free parameter per study.
        dwc_free = {s: pm.Uniform(f"DWC_below_MRL_{s}", 0, mrl)
                    for s, mrl in df.groupby("s")["mrl"].first().dropna().items()}

        def water_conc(rows):
            return [dwc_free[r.s] if np.isnan(r.dwc) else r.dwc for r in rows.itertuples()]

        # ---------- 3. Individual level: one value PER PERSON ----------
        def person_params(rows, name):
            """Each person's k, Vd, intake, background and starting level."""
            z = {v: pm.Normal(f"z_{v}_{name}", 0, 1, shape=len(rows))
                 for v in ["k", "Vd", "DWI", "Cbgd", "C0"]}
            s = rows["s"].values
            k = pt.exp(M_ln_k + pt.sqrt(V_ln_k) * z["k"])
            Vd = pt.exp(M_ln_Vd + SD_ln_Vd * z["Vd"])
            DWI = pt.exp(LN_DWI_MEAN + LN_DWI_SD * z["DWI"])
            Cbgd = rows["Cbgd_in_gm"].values * pt.exp(
                M_ln_Cbgd_sc[s] + np.log(rows["Cbgd_in_gsd"].values) * z["Cbgd"])
            C0 = rows["C_0_in_gm"].values * pt.exp(
                M_ln_C_0_sc[s] + np.log(rows["C_0_in_gsd"].values) * z["C0"])
            return k, Vd, DWI, Cbgd, C0

        # (a) Two blood samples, t = 0 and t = T, constant water (PFNA, PFHxS)
        rows = df[df.endpoint == "Cserum"]
        if len(rows):
            k, Vd, DWI, Cbgd, C0 = person_params(rows, "Cserum")
            T = np.array([r[-1] for r in rows["times"]])
            Css = DWI * DAYS * pt.stack(water_conc(rows)) / (k * Vd)      # steady state from water
            C_T = Cbgd + (C0 - Cbgd) * pt.exp(-k * T) + Css * (1 - pt.exp(-k * T))
            observe("Cserum", C0, C_T, rows, error_gsd("Cserum"))

        # (b) Two blood samples, water level changed over time (PFOA, PFOS)
        rows = df[df.endpoint == "Cserum_t"]
        if len(rows):
            k, Vd, DWI, Cbgd, C0 = person_params(rows, "Cserum_t")
            T, start, end, conc = dose_table(rows)
            # dC/dt = DWI*DWC(t)/Vd - k*(C - Cbgd), solved exactly for a water
            # level that is constant within each segment [start, end]:
            kc = k[:, None]
            washin = pt.sum(conc * (pt.exp(-kc * (T[:, None] - end)) -
                                    pt.exp(-kc * (T[:, None] - start))), axis=1)
            C_T = Cbgd + (C0 - Cbgd) * pt.exp(-k * T) + DWI * DAYS / (k * Vd) * washin
            observe("Cserum_t", C0, C_T, rows, error_gsd("Cserum"))

        # (c) One blood sample at steady state (t ~ 0), known water level (Minnesota)
        rows = df[df.endpoint == "Cbgd_Css"]
        if len(rows):
            k, Vd, DWI, Cbgd, _ = person_params(rows, "Cbgd_Css")
            C = Cbgd + DWI * DAYS * rows["dwc"].values / (k * Vd)
            pm.LogNormal("obs_Cbgd_Css", mu=pt.log(C), sigma=pt.log(error_gsd("Cbgd_Css")),
                         observed=np.array([v[0] for v in rows["values"]]))

        # ---------- 4. Population averages (whole-community means) ----------
        # E[X] of a lognormal X is exp(mu + var/2). Formulas from Chiu's
        # CalcOutputs{} block; t is time since the water was cleaned up.
        def lognormal_mean(mu, var):
            return pt.exp(mu + var / 2)

        for endpoint in ["M_Cserum", "M_Cbgd_Css"]:
            rows = df[df.endpoint == endpoint]
            if not len(rows):
                continue
            preds, obs = [], []
            for r, dwc in zip(rows.itertuples(), water_conc(rows)):
                sd_bg, sd_c0 = np.log(r.Cbgd_in_gsd), np.log(r.C_0_in_gsd)
                mu_bg = np.log(r.Cbgd_in_gm) + M_ln_Cbgd_sc[r.s]
                mu_c0 = np.log(r.C_0_in_gm) + M_ln_C_0_sc[r.s]
                mu_ss = LN_DWI_MEAN + pt.log(DAYS * dwc) - M_ln_k - M_ln_Vd
                var_ss = LN_DWI_SD**2 + V_ln_k + SD_ln_Vd**2
                for t, y in zip(r.times, r.values):
                    # -k*t treated as normal with matching mean and variance
                    mu_kt = -t * pt.exp(M_ln_k + V_ln_k / 2)
                    var_kt = (pt.exp(V_ln_k) - 1) * mu_kt**2
                    bg = lognormal_mean(mu_bg, sd_bg**2)
                    ss_decayed = lognormal_mean(mu_ss + mu_kt, var_ss + var_kt)
                    if endpoint == "M_Cbgd_Css":
                        preds.append(bg + ss_decayed)
                    else:
                        preds.append(bg
                                     + lognormal_mean(mu_c0 + mu_kt, sd_c0**2 + var_kt)
                                     - lognormal_mean(mu_bg + mu_kt, sd_bg**2 + var_kt)
                                     + lognormal_mean(mu_ss, var_ss)
                                     - ss_decayed)
                    obs.append(y)
            pm.LogNormal(f"obs_{endpoint}", mu=pt.log(pt.stack(preds)),
                         sigma=pt.log(error_gsd(endpoint)), observed=np.array(obs))
    return model


def observe(name, C0, C_T, rows, gsd):
    """Likelihood for BOTH blood samples of each person (t = 0 and t = T)."""
    first = np.array([v[0] for v in rows["values"]])
    last = np.array([v[-1] for v in rows["values"]])
    pm.LogNormal(f"obs_{name}_t0", mu=pt.log(C0), sigma=pt.log(gsd), observed=first)
    pm.LogNormal(f"obs_{name}_T", mu=pt.log(C_T), sigma=pt.log(gsd), observed=last)


def dose_table(rows):
    """Water-level segments per person, clipped at the blood-draw time T."""
    T = np.array([r[-1] for r in rows["times"]])
    width = max(len(c) for c in rows["dose_conc"])
    start, end, conc = (np.zeros((len(rows), width)) for _ in range(3))
    for i, (times, c) in enumerate(zip(rows["dose_times"], rows["dose_conc"])):
        edges = np.minimum(list(times) + [T[i]], T[i])   # nothing after the draw
        start[i, :len(c)], end[i, :len(c)], conc[i, :len(c)] = edges[:-1], edges[1:], c
    return T, start, end, conc


def fit(chem, draws=1000, cores=4):
    with build_model(chem):
        idata = pm.sample(draws, tune=draws, chains=4, cores=cores,
                          target_accept=0.95, random_seed=1)
    post = idata.posterior
    hl = np.percentile(post["halflife"], [50, 2.5, 97.5])
    gsd = np.median(post["halflife_GSD"])
    div = int(idata.sample_stats["diverging"].sum())
    print(f"\n{chem}: half-life {hl[0]:.2f} yr (95% CI {hl[1]:.2f}-{hl[2]:.2f}), "
          f"paper {PAPER[chem][0]} ({PAPER[chem][1]}-{PAPER[chem][2]}); "
          f"GSD between people {gsd:.2f}; divergences {div}")
    idata.to_netcdf(f"results_{chem}.nc")
    return hl, gsd


if __name__ == "__main__":
    chems = list(PRIORS) if sys.argv[1:] in ([], ["all"]) else sys.argv[1:]
    results = {c: fit(c) for c in chems}
    print("\nChemical  Python median (95% CI)    Paper median (95% CI)")
    for c, (hl, _) in results.items():
        p = PAPER[c]
        print(f"{c:8s}  {hl[0]:5.2f} ({hl[1]:.2f}-{hl[2]:.2f})        {p[0]:5.2f} ({p[1]}-{p[2]})")
