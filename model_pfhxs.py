"""
model_pfhxs.py
===============
Bayesian hierarchical toxicokinetic model for PFHxS (perfluorohexane
sulfonic acid), replicating Chiu et al. 2022's MCSim model in pure
Python/PyMC.

READ model_pfna.py FIRST
----------------------------
Structurally, PFHxS is IDENTICAL to PFNA -- same two pieces (18 Decatur
individuals under constant below-MRL exposure, closed-form; 2
population-summary rows, closed-form) and the same non-centered
hierarchical parameterization. If any of the general concepts here are
unfamiliar (hierarchical model, non-centered z-scores, the E[X] =
exp(mu+sigma^2/2) population-summary trick), read model_pfna.py's long
docstring first -- this file only calls out what's PFHxS-specific.

WHAT'S DIFFERENT ABOUT PFHxS
---------------------------------
Only the numbers: PFHxS-specific priors (below), a different MRL
(0.03 instead of PFNA's 0.02), and both population-summary rows here
have a FIXED, known drinking-water concentration (Paulsboro=0.0047,
Horsham=0.17) rather than one of them being a free below-MRL parameter
like PFNA's Horsham -- so this model needs no extra free DWC parameter
for the population-summary rows at all.

WHY THE HALF-LIFE IS SO MUCH LONGER THAN THE OTHER THREE
--------------------------------------------------------------
PFHxS's published half-life (8.47 years) is roughly 2-4x longer than
PFOA/PFOS/PFNA's. This is a genuine, well-established property of PFHxS
in humans (it's eliminated much more slowly), not an artifact of this
particular model -- you'll see it reflected directly in this script's
own prior: `M_ln_k`'s prior mean corresponds to a guessed half-life
around 5.3 years, already longer than the other three chemicals' priors,
before the data has even been seen.

EXPECTED RESULT
-------------------
Chiu's real PFHxS half-life (recomputed directly from his raw saved MCMC
chain): 8.47 years, 95% CI [5.69, 13.46]. We got 6.59 years, 90% CI
[4.58, 10.31] -- inside the right ballpark and overlapping his interval,
though on the low side of it; a reasonable, not perfect, match.

HOW LONG THIS TAKES
-----------------------
Roughly 2-3 minutes on a typical laptop CPU (98 free parameters -- the
smallest and fastest of the four scripts).
"""

import numpy as np
import pymc as pm
import pytensor.tensor as pt
import arviz as az
import matplotlib.pyplot as plt
import time

from parse_chiu_data import build_dataframe

t0 = time.time()

# ---------------------------------------------------------------------
# STEP 1: load the data
# ---------------------------------------------------------------------
df, _ = build_dataframe("PFHxS")
fit_df = df[df["in_fit"] & (df["endpoint"] == "Cserum")].reset_index(drop=True)
N = len(fit_df)
print(f"PFHxS: pooling {N} Decatur individuals + 2 population-summary rows")

MRL = 0.03  # mg/L -- PFHxS's own below-MRL bound (different from PFNA's 0.02)
Cbgd_gm = fit_df["Cbgd_in_gm"].values.astype(float)
Cbgd_gsd = fit_df["Cbgd_in_gsd"].values.astype(float)
C_0_gm = fit_df["C_0_in_gm"].values.astype(float)
C_0_gsd = fit_df["C_0_in_gsd"].fillna(1.01).values.astype(float)
t_query = np.array([r["print_times"][-1] for _, r in fit_df.iterrows()])
obs = np.array([r["data_values"][-1] for _, r in fit_df.iterrows()])

pop_df = df[df["in_fit"] & (df["endpoint"] == "M_Cbgd_Css")].reset_index(drop=True)
assert len(pop_df) == 2
paulsboro = pop_df[pop_df["study"].str.contains("Paulsboro")].iloc[0]
horsham = pop_df[pop_df["study"].str.contains("Horsham")].iloc[0]
print(f"Paulsboro: DWC={paulsboro['dwc_value']} t={paulsboro['print_times']} obs={paulsboro['data_values']}")
print(f"Horsham:   DWC={horsham['dwc_value']} t={horsham['print_times']} obs={horsham['data_values']}")

# ---------------------------------------------------------------------
# STEP 2: fixed constants (same values used for every PFAS chemical)
# ---------------------------------------------------------------------
M_ln_DWI_BW_d_fixed = -4.3955
SD_ln_DWI_BW_d_fixed = 0.888
SD_ln_Cbgd_sc_fixed = 1.0
SD_ln_C_0_sc_fixed = 1.0

print(f"\nSetup done at {time.time()-t0:.1f}s. Building PyMC model...")

# ---------------------------------------------------------------------
# STEP 3: build the PyMC model
# ---------------------------------------------------------------------
with pm.Model() as pfhxs_model:

    # --- Population-level hyperparameters (PFHxS-specific priors) ---
    # mu=-2.03422 corresponds to exp(-2.03422) ~= 0.131/day, i.e. a
    # rough prior half-life guess around 5.3 years -- noticeably longer
    # than the ~4-5 yr rough guesses used for PFOA/PFOS/PFNA's priors,
    # reflecting PFHxS's known slower elimination even before the data
    # is seen. Chiu's file comments both V_ln_k and SD_ln_Vd's priors
    # here as "borrowed from the PFOA posterior" (PFHxS-specific
    # variability data was thinner).
    M_ln_k = pm.Normal("M_ln_k", mu=-2.03422, sigma=0.4055)
    V_ln_k = pm.Lognormal("V_ln_k", mu=np.log(0.20), sigma=np.log(1.275))
    SD_ln_k = pm.Deterministic("SD_ln_k", pt.sqrt(V_ln_k))

    M_ln_Vd = pm.Normal("M_ln_Vd", mu=-1.38629, sigma=0.2624)
    SD_ln_Vd = pm.HalfNormal("SD_ln_Vd", sigma=0.17)

    M_ln_Cbgd_sc = pm.Normal("M_ln_Cbgd_sc", mu=-0.22314, sigma=0.4055)
    M_ln_C_0_sc = pm.Normal("M_ln_C_0_sc", mu=0.0, sigma=0.4055)

    log_GSD_Cserum = pm.Uniform("log_GSD_Cserum", lower=np.log(1.1), upper=np.log(10.0))
    GSD_Cserum = pm.Deterministic("GSD_Cserum", pt.exp(log_GSD_Cserum))
    log_GSD_M_Cbgd_Css = pm.Uniform("log_GSD_M_Cbgd_Css", lower=np.log(1.1), upper=np.log(10.0))
    GSD_M_Cbgd_Css = pm.Deterministic("GSD_M_Cbgd_Css", pt.exp(log_GSD_M_Cbgd_Css))

    DWC_belowMRL = pm.Uniform("DWC_belowMRL", lower=0.0, upper=MRL)

    k_pop = pm.Deterministic("k_pop", pt.exp(M_ln_k))
    halflife_pop = pm.Deterministic("halflife_pop", pt.log(2) / k_pop)

    # --- Individual-level z-scores (non-centered parameterization,
    # explained in model_pfna.py) ---
    z_k = pm.Normal("z_k", 0, 1, shape=N)
    z_Vd = pm.Normal("z_Vd", 0, 1, shape=N)
    z_DWI = pm.Normal("z_DWI", 0, 1, shape=N)
    z_Cbgd = pm.Normal("z_Cbgd", 0, 1, shape=N)
    z_C0 = pm.Normal("z_C0", 0, 1, shape=N)

    k = pt.exp(M_ln_k + SD_ln_k * z_k)
    Vd = pt.exp(M_ln_Vd + SD_ln_Vd * z_Vd)
    DWI_BW_d = pt.exp(M_ln_DWI_BW_d_fixed + SD_ln_DWI_BW_d_fixed * z_DWI)
    Cbgd = Cbgd_gm * pt.exp(M_ln_Cbgd_sc + SD_ln_Cbgd_sc_fixed * np.log(Cbgd_gsd) * z_Cbgd)
    C_0 = C_0_gm * pt.exp(M_ln_C_0_sc + SD_ln_C_0_sc_fixed * np.log(C_0_gsd) * z_C0)

    # --- Individual prediction: exponential approach to steady state ---
    Css = DWI_BW_d * 365.25 * DWC_belowMRL / (k * Vd)
    C_pred = Cbgd + (C_0 - Cbgd) * pt.exp(-k * t_query) + Css * (1 - pt.exp(-k * t_query))
    pm.Deterministic("C_pred", C_pred)
    pm.LogNormal("obs", mu=pt.log(C_pred), sigma=pt.log(GSD_Cserum), observed=obs)

    # --- Population-summary rows: Paulsboro, Horsham (both fixed DWC) ---
    def M_Cbgd_Css_formula(DWC, t, Cbgd_gm_v, Cbgd_gsd_v):
        """See model_pfna.py for the full derivation of this closed-form
        'mean of a lognormal population at steady state' formula."""
        M_Cbgd = Cbgd_gm_v * pt.exp(M_ln_Cbgd_sc + (SD_ln_Cbgd_sc_fixed * np.log(Cbgd_gsd_v))**2 / 2)
        mu_Css = M_ln_DWI_BW_d_fixed + pt.log(365.25) + pt.log(DWC) - M_ln_k - M_ln_Vd
        V_Css = SD_ln_DWI_BW_d_fixed**2 + V_ln_k + SD_ln_Vd**2
        M_kt = -t * pt.exp(M_ln_k + V_ln_k / 2)
        V_kt = (pt.exp(V_ln_k) - 1) * M_kt**2
        M_Css_expkt = pt.exp(mu_Css + M_kt + (V_Css + V_kt) / 2)
        return M_Cbgd + M_Css_expkt

    pred_paulsboro = M_Cbgd_Css_formula(float(paulsboro["dwc_value"]), float(paulsboro["print_times"][0]),
                                         float(paulsboro["Cbgd_in_gm"]), float(paulsboro["Cbgd_in_gsd"]))
    pred_horsham = M_Cbgd_Css_formula(float(horsham["dwc_value"]), float(horsham["print_times"][0]),
                                       float(horsham["Cbgd_in_gm"]), float(horsham["Cbgd_in_gsd"]))
    pm.Deterministic("pred_paulsboro", pred_paulsboro)
    pm.Deterministic("pred_horsham", pred_horsham)
    pm.LogNormal("obs_paulsboro", mu=pt.log(pred_paulsboro), sigma=pt.log(GSD_M_Cbgd_Css),
                 observed=float(paulsboro["data_values"][0]))
    pm.LogNormal("obs_horsham", mu=pt.log(pred_horsham), sigma=pt.log(GSD_M_Cbgd_Css),
                 observed=float(horsham["data_values"][0]))

    n_params = N * 5 + 8
    print(f"Model built at {time.time()-t0:.1f}s ({n_params} free parameters)")

    idata = pm.sample(2000, tune=2000, chains=4, cores=1, target_accept=0.99,
                       random_seed=42, progressbar=True)

print(f"\nSampling finished at {time.time()-t0:.1f}s total")
idata.to_netcdf("model_pfhxs_results.nc")

# ---------------------------------------------------------------------
# STEP 4: summarize and check convergence
# ---------------------------------------------------------------------
summary = az.summary(idata, var_names=["M_ln_k", "SD_ln_k", "k_pop", "halflife_pop",
                                        "M_ln_Vd", "SD_ln_Vd", "GSD_Cserum", "GSD_M_Cbgd_Css",
                                        "DWC_belowMRL"])
print("\nPopulation-level posterior summary:")
print(summary)

halflife_samples = idata.posterior["halflife_pop"].values.flatten()
print(f"\n{'='*70}")
print(f"PFHxS POPULATION half-life (yr): median = {np.median(halflife_samples):.2f}, "
      f"90% CI = [{np.percentile(halflife_samples,5):.2f}, {np.percentile(halflife_samples,95):.2f}]")
print("Chiu's ACTUAL published PFHxS estimate (from his raw MCMC chain): 8.47 yr [5.69-13.46] (95% CI)")
print(f"{'='*70}")

Vd_pop_samples = np.exp(idata.posterior["M_ln_Vd"].values.flatten())
print(f"\nPopulation Vd (L/kg): median = {np.median(Vd_pop_samples):.3f} "
      f"(Chiu's real fitted PFHxS Vd: 0.283 L/kg)")

worst_rhat = summary["r_hat"].max()
n_div = int(idata.sample_stats["diverging"].values.sum())
print(f"\nWorst r_hat: {worst_rhat:.4f} (want < 1.01) | divergences: {n_div}")

# ---------------------------------------------------------------------
# STEP 5: plot
# ---------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
ax = axes[0]
ax.hist(halflife_samples, bins=60, density=True, color="darkgoldenrod", alpha=0.8, label="Our PFHxS model")
ax.axvline(8.47, color="red", lw=2, ls=":", label="Chiu published: 8.47 yr")
ax.axvspan(5.69, 13.46, color="red", alpha=0.1, label="Chiu published 95% CI")
ax.set_xlabel("population half-life (yr)")
ax.set_ylabel("posterior density")
ax.set_title("PFHxS population half-life: our replication vs. published")
ax.legend(fontsize=8)

ax = axes[1]
for c in range(idata.posterior.sizes["chain"]):
    ax.plot(idata.posterior["halflife_pop"].values[c], lw=0.6, alpha=0.8, label=f"chain {c+1}")
ax.axhline(8.47, color="red", ls=":", lw=1.5)
ax.set_xlabel("MCMC draw number")
ax.set_ylabel("population half-life (yr)")
ax.set_title("Trace plot: do the 4 chains agree?")
ax.legend(fontsize=7, ncol=2)

plt.tight_layout()
plt.savefig("model_pfhxs_results.png", dpi=150)
print("\nSaved plot to model_pfhxs_results.png")
