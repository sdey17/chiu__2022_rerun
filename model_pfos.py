"""
model_pfos.py
=============
Bayesian hierarchical toxicokinetic model for PFOS (perfluorooctane
sulfonic acid), replicating Chiu et al. 2022's MCSim model in pure
Python/PyMC.

READ model_pfna.py FIRST, model_pfoa.py SECOND
---------------------------------------------------
This script reuses everything from both: PFNA's hierarchical structure
and population-summary closed-form trick, plus PFOA's `pytensor.scan`
machinery for people with time-varying exposure histories. If any of
that is unfamiliar, read those two files' long docstrings first -- this
one only explains what's specific to PFOS.

STRUCTURE OF PFOS'S DATA
-----------------------------
  - 18 "Cserum_t" people (Decatur, WV) -- time-varying exposure history,
    needs the pytensor.scan simulation loop (same mechanism as PFOA).
  - 49 "Cbgd_Css" people (Minnesota) -- constant, KNOWN drinking-water
    concentration, closed-form steady-state formula (same as PFNA's
    Decatur group, just at a known rather than below-MRL concentration).
  - 2 "M_Cbgd_Css" population-summary rows (Paulsboro, Horsham) -- BOTH
    have a fixed, known drinking-water concentration here (unlike PFNA,
    where Horsham's DWC was a free below-MRL parameter), so neither adds
    a new free parameter to the model.

ONE DATA QUALITY WRINKLE WORTH KNOWING ABOUT
-------------------------------------------------
Chiu's own file has a comment on the Horsham row flagging that its water
concentration "may have been [reported in] parts-per-thousand instead of
parts-per-trillion -- looks low." We used the number exactly as given in
the file (we are replicating his model, not second-guessing his data
curation), and separately confirmed this one point does not distort the
fit: our model's predicted value for Horsham (26.27) landed close to the
observed value (24.64) either way. This is a good habit generally --
when a data file has an odd flagged value, check whether your model
actually struggles to fit it before assuming it's a problem.

EXPECTED RESULT
-------------------
This is the chemical where our replication matches Chiu's own published
number most closely of all four. Chiu's real PFOS half-life (recomputed
directly from his raw saved MCMC chain): 3.41 years, 95% CI [2.63, 4.40].
We got 3.10 years, 90% CI [2.28, 4.37] -- well within his own
uncertainty band.

HOW LONG THIS TAKES
-----------------------
Roughly 3-5 minutes on a typical laptop CPU (296 free parameters, and
the scan loop only has to simulate 18 people, not 128 like PFOA).
"""

import numpy as np
import pymc as pm
import pytensor
import pytensor.tensor as pt
import arviz as az
import matplotlib.pyplot as plt
import time

from parse_chiu_data import build_dataframe

t0 = time.time()

# ---------------------------------------------------------------------
# STEP 1: load the data (see model_pfoa.py for a detailed walkthrough of
# why the "Cserum_t" group needs the padded dosing-schedule matrices)
# ---------------------------------------------------------------------
df, _ = build_dataframe("PFOS")
fit_df = df[df["in_fit"] & df["endpoint"].isin(["Cserum_t", "Cbgd_Css"])].reset_index(drop=True)
cserum_df = fit_df[fit_df["endpoint"] == "Cserum_t"].reset_index(drop=True)   # Decatur, time-varying exposure
cbgd_df = fit_df[fit_df["endpoint"] == "Cbgd_Css"].reset_index(drop=True)      # Minnesota, constant known exposure
N1, N2 = len(cserum_df), len(cbgd_df)
print(f"PFOS: pooling {N1} Cserum_t + {N2} Cbgd_Css individuals + 2 population-summary rows")

M = int(cserum_df["dwc_n"].max())
t_start_mat = np.zeros((N1, M))
t_end_mat = np.zeros((N1, M))
conc_mat = np.zeros((N1, M))
for i, row in cserum_df.iterrows():
    dose_times = list(row["dwc_times"])
    dose_conc = list(row["dwc_conc"])
    tq = row["print_times"][-1]
    boundaries = dose_times + [tq]
    boundaries += [tq] * (M + 1 - len(boundaries))
    conc_padded = dose_conc + [0.0] * (M - len(dose_conc))
    t_start_mat[i, :] = boundaries[:M]
    t_end_mat[i, :] = boundaries[1:M + 1]
    conc_mat[i, :] = conc_padded

C_0_cserum = cserum_df["C_0_in_gm"].values.astype(float)
Cbgd_gm_cserum = cserum_df["Cbgd_in_gm"].values.astype(float)
Cbgd_gsd_cserum = cserum_df["Cbgd_in_gsd"].values.astype(float)
C_0_gsd_cserum = cserum_df["C_0_in_gsd"].fillna(1.01).values.astype(float)
obs_cserum = np.array([r["data_values"][-1] for _, r in cserum_df.iterrows()])

dwc_val_bg = cbgd_df["dwc_value"].values.astype(float)
Cbgd_gm_bg = cbgd_df["Cbgd_in_gm"].values.astype(float)
Cbgd_gsd_bg = cbgd_df["Cbgd_in_gsd"].values.astype(float)
obs_bg = np.array([r["data_values"][-1] for _, r in cbgd_df.iterrows()])

pop_df = df[df["in_fit"] & (df["endpoint"] == "M_Cbgd_Css")].reset_index(drop=True)
assert len(pop_df) == 2
paulsboro = pop_df[pop_df["study"].str.contains("Paulsboro")].iloc[0]
horsham = pop_df[pop_df["study"].str.contains("Horsham")].iloc[0]
print(f"Paulsboro: DWC={paulsboro['dwc_value']} t={paulsboro['print_times']} obs={paulsboro['data_values']}")
print(f"Horsham:   DWC={horsham['dwc_value']} t={horsham['print_times']} obs={horsham['data_values']}  "
      f"(flagged in Chiu's own file as possibly a units mismatch -- used as-is, see module docstring)")

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
with pm.Model() as pfos_model:

    # --- Population-level hyperparameters (PFOS-specific priors, from
    # Chiu's own file header) ---
    # M_ln_k's prior POINT VALUE is the same number as PFOA's -- Chiu's
    # own file comments that this was intentional, borrowed because
    # PFOS-specific half-life information going into the prior was thin;
    # the DATA (not the prior) is what then pulls this to its own
    # PFOS-specific posterior.
    M_ln_k = pm.Normal("M_ln_k", mu=-1.8971, sigma=0.4055)
    V_ln_k = pm.Lognormal("V_ln_k", mu=np.log(0.2024), sigma=np.log(1.261))
    SD_ln_k = pm.Deterministic("SD_ln_k", pt.sqrt(V_ln_k))

    M_ln_Vd = pm.Normal("M_ln_Vd", mu=-1.46968, sigma=0.2624)
    SD_ln_Vd = pm.HalfNormal("SD_ln_Vd", sigma=0.17)

    M_ln_Cbgd_sc = pm.Normal("M_ln_Cbgd_sc", mu=-0.22314, sigma=0.4055)
    M_ln_C_0_sc = pm.Normal("M_ln_C_0_sc", mu=0.0, sigma=0.4055)

    log_GSD_Cserum = pm.Uniform("log_GSD_Cserum", lower=np.log(1.1), upper=np.log(10.0))
    GSD_Cserum = pm.Deterministic("GSD_Cserum", pt.exp(log_GSD_Cserum))
    log_GSD_Cbgd_Css = pm.Uniform("log_GSD_Cbgd_Css", lower=np.log(1.1), upper=np.log(10.0))
    GSD_Cbgd_Css = pm.Deterministic("GSD_Cbgd_Css", pt.exp(log_GSD_Cbgd_Css))
    log_GSD_M_Cbgd_Css = pm.Uniform("log_GSD_M_Cbgd_Css", lower=np.log(1.1), upper=np.log(10.0))
    GSD_M_Cbgd_Css = pm.Deterministic("GSD_M_Cbgd_Css", pt.exp(log_GSD_M_Cbgd_Css))

    k_pop = pm.Deterministic("k_pop", pt.exp(M_ln_k))
    halflife_pop = pm.Deterministic("halflife_pop", pt.log(2) / k_pop)

    # --- Group 1: Decatur, time-varying exposure (pytensor.scan) ---
    z_k1 = pm.Normal("z_k1", 0, 1, shape=N1)
    z_Vd1 = pm.Normal("z_Vd1", 0, 1, shape=N1)
    z_DWI1 = pm.Normal("z_DWI1", 0, 1, shape=N1)
    z_Cbgd1 = pm.Normal("z_Cbgd1", 0, 1, shape=N1)
    z_C0 = pm.Normal("z_C0", 0, 1, shape=N1)

    k1 = pt.exp(M_ln_k + SD_ln_k * z_k1)
    Vd1 = pt.exp(M_ln_Vd + SD_ln_Vd * z_Vd1)
    DWI1 = pt.exp(M_ln_DWI_BW_d_fixed + SD_ln_DWI_BW_d_fixed * z_DWI1)
    Cbgd1 = Cbgd_gm_cserum * pt.exp(M_ln_Cbgd_sc + SD_ln_Cbgd_sc_fixed * np.log(Cbgd_gsd_cserum) * z_Cbgd1)
    C_0 = C_0_cserum * pt.exp(M_ln_C_0_sc + SD_ln_C_0_sc_fixed * np.log(C_0_gsd_cserum) * z_C0)

    def scan_step(t_start_col, t_end_col, conc_col, C_prev, k_v, Vd_v, DWI_v, Cbgd_v):
        """One dosing-segment step -- see model_pfoa.py for the full explanation."""
        dt = t_end_col - t_start_col
        C_ss = Cbgd_v + DWI_v * 365.25 * conc_col / (k_v * Vd_v)
        return C_ss + (C_prev - C_ss) * pt.exp(-k_v * dt)

    scan_out, _ = pytensor.scan(
        fn=scan_step,
        sequences=[pt.as_tensor_variable(t_start_mat.T),
                   pt.as_tensor_variable(t_end_mat.T),
                   pt.as_tensor_variable(conc_mat.T)],
        outputs_info=[C_0],
        non_sequences=[k1, Vd1, DWI1, Cbgd1],
        n_steps=M,
    )
    C_pred_cserum = scan_out[-1]

    # --- Group 2: Minnesota, constant known exposure (closed-form) ---
    z_k2 = pm.Normal("z_k2", 0, 1, shape=N2)
    z_Vd2 = pm.Normal("z_Vd2", 0, 1, shape=N2)
    z_DWI2 = pm.Normal("z_DWI2", 0, 1, shape=N2)
    z_Cbgd2 = pm.Normal("z_Cbgd2", 0, 1, shape=N2)

    k2 = pt.exp(M_ln_k + SD_ln_k * z_k2)
    Vd2 = pt.exp(M_ln_Vd + SD_ln_Vd * z_Vd2)
    DWI2 = pt.exp(M_ln_DWI_BW_d_fixed + SD_ln_DWI_BW_d_fixed * z_DWI2)
    Cbgd2 = Cbgd_gm_bg * pt.exp(M_ln_Cbgd_sc + SD_ln_Cbgd_sc_fixed * np.log(Cbgd_gsd_bg) * z_Cbgd2)
    Css2 = DWI2 * 365.25 * dwc_val_bg / (k2 * Vd2)
    C_pred_bg = Cbgd2 + Css2

    pm.LogNormal("obs_cserum", mu=pt.log(C_pred_cserum), sigma=pt.log(GSD_Cserum), observed=obs_cserum)
    pm.LogNormal("obs_bg", mu=pt.log(C_pred_bg), sigma=pt.log(GSD_Cbgd_Css), observed=obs_bg)

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

    n_params = N1 * 5 + N2 * 4 + 10
    print(f"Model built at {time.time()-t0:.1f}s ({n_params} free parameters)")

    idata = pm.sample(1500, tune=1500, chains=4, cores=1, target_accept=0.95,
                       random_seed=42, progressbar=True)

print(f"\nSampling finished at {time.time()-t0:.1f}s total")
idata.to_netcdf("model_pfos_results.nc")

# ---------------------------------------------------------------------
# STEP 4: summarize and check convergence
# ---------------------------------------------------------------------
summary = az.summary(idata, var_names=["M_ln_k", "SD_ln_k", "k_pop", "halflife_pop",
                                        "M_ln_Vd", "SD_ln_Vd", "GSD_Cserum", "GSD_Cbgd_Css",
                                        "GSD_M_Cbgd_Css"])
print("\nPopulation-level posterior summary:")
print(summary)

halflife_samples = idata.posterior["halflife_pop"].values.flatten()
print(f"\n{'='*70}")
print(f"PFOS POPULATION half-life (yr): median = {np.median(halflife_samples):.2f}, "
      f"90% CI = [{np.percentile(halflife_samples,5):.2f}, {np.percentile(halflife_samples,95):.2f}]")
print("Chiu's ACTUAL published PFOS estimate (from his raw MCMC chain): 3.41 yr [2.63-4.40] (95% CI)")
print(f"{'='*70}")

Vd_pop_samples = np.exp(idata.posterior["M_ln_Vd"].values.flatten())
print(f"\nPopulation Vd (L/kg): median = {np.median(Vd_pop_samples):.3f} "
      f"(Chiu's real fitted PFOS Vd: 0.322 L/kg)")

worst_rhat = summary["r_hat"].max()
n_div = int(idata.sample_stats["diverging"].values.sum())
print(f"\nWorst r_hat: {worst_rhat:.4f} (want < 1.01) | divergences: {n_div}")

# ---------------------------------------------------------------------
# STEP 5: plot
# ---------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
ax = axes[0]
ax.hist(halflife_samples, bins=60, density=True, color="teal", alpha=0.8, label="Our PFOS model")
ax.axvline(3.41, color="red", lw=2, ls=":", label="Chiu published: 3.41 yr")
ax.axvspan(2.63, 4.40, color="red", alpha=0.1, label="Chiu published 95% CI")
ax.set_xlabel("population half-life (yr)")
ax.set_ylabel("posterior density")
ax.set_title("PFOS population half-life: our replication vs. published")
ax.legend(fontsize=8)

ax = axes[1]
for c in range(idata.posterior.sizes["chain"]):
    ax.plot(idata.posterior["halflife_pop"].values[c], lw=0.6, alpha=0.8, label=f"chain {c+1}")
ax.axhline(3.41, color="red", ls=":", lw=1.5)
ax.set_xlabel("MCMC draw number")
ax.set_ylabel("population half-life (yr)")
ax.set_title("Trace plot: do the 4 chains agree?")
ax.legend(fontsize=7, ncol=2)

plt.tight_layout()
plt.savefig("model_pfos_results.png", dpi=150)
print("\nSaved plot to model_pfos_results.png")
