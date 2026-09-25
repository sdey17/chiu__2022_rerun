"""
model_pfoa.py
=============
Bayesian hierarchical toxicokinetic model for PFOA (perfluorooctanoic
acid), replicating Chiu et al. 2022's MCSim model in pure Python/PyMC.

READ model_pfna.py FIRST
----------------------------
This script builds on every idea in model_pfna.py (hierarchical
structure, non-centered z-score parameterization, log-space priors, the
E[X]=exp(mu+sigma^2/2) population-summary trick). If any of that is
unfamiliar, start there -- it's the simplest of the four and has the
long-form explanations. This file only re-explains what is NEW for PFOA.

WHAT'S DIFFERENT ABOUT PFOA
--------------------------------
PFOA is by far the biggest dataset of the four chemicals (175 individual
people instead of ~18-20), and it is the ONLY one of the four where
people have TIME-VARYING exposure histories -- someone's drinking-water
concentration may have changed several times over their life (a new well
tested, a filtration system installed, a contamination event ended,
etc.), and we have to simulate their blood level marching forward through
each of those exposure segments, not just solve one algebra equation.

That means PFOA needs TWO different structural groups of people that get
combined into one model:

  1. "Cserum_t" people (128 of them): time-varying exposure, fit with a
     numerical simulation across each person's own dosing segments
     (implemented with `pytensor.scan`, explained below).
  2. "Cbgd_Css" people (47 of them): constant lifetime exposure at a
     KNOWN (not free-parameter) drinking-water concentration, so their
     predicted blood level is just the closed-form steady-state formula
     from model_pfna.py, no simulation loop needed.

On top of those 175 individuals, this script ALSO includes 4
population-summary rows (2 sites reporting a decaying MEAN serum
trajectory over time -- "M_Cserum" -- and 2 sites reporting a single
mean steady-state level -- "M_Cbgd_Css", same idea as PFNA's Paulsboro/
Horsham rows). Skipping these 4 rows is a real mistake to be aware of --
see "AN HONEST NEGATIVE RESULT" below.

WHY `pytensor.scan`?
------------------------
For the 128 time-varying people, each one's dosing history has to be
walked forward segment-by-segment: "you were exposed to X1 mg/L from day
0 to day T1, so your level moved from wherever it started toward
Css(X1); then exposure changed to X2 from day T1 to T2, so your level
moved from THAT toward Css(X2); ..." and so on until we reach the day
their blood was actually measured. In plain Python you'd write this as
a for-loop, but PyTensor (the array/graph engine underneath PyMC)
compiles the ENTIRE model into a single computational graph before
sampling even starts -- and a Python for-loop across ~13 dosing segments
for 128 people, unrolled explicitly, produces an enormous graph that
takes minutes just to COMPILE (we measured 148+ seconds on an early
attempt). `pytensor.scan` is PyTensor's native "loop" operator: it
represents "repeat this same step 13 times, once per exposure segment,
carrying the running blood-concentration forward" as ONE graph node, not
13 unrolled copies, which compiles in a few seconds instead.

AN HONEST NEGATIVE RESULT
-----------------------------
Unlike PFNA, adding the 4 population-summary rows to PFOA barely moved
the estimate: 4.23 -> 4.30 years, essentially unchanged, still well
above Chiu's real published 3.15 years. This is included here NOT
because it fixed anything, but because it is the right thing to try
(the same fix worked well for 2 of the other 3 chemicals) and a null
result is still useful evidence. If you dig into WHY PFOA specifically
still misses (we spent a long time on this), what we found is that our
fit ends up with much LESS individual-to-individual variability in
elimination rate (the V_ln_k parameter) than Chiu's own real posterior
does -- roughly 1/3 as much. We were not able to pin down WHY our model
and his produce different amounts of that variability from what appears
to be the same data and the same formula; see README.md's "What's still
open" section for the full list of things we ruled out.

We're telling you this up front so you don't spend an hour assuming
you've made a mistake if your PFOA run also lands around 4.2-4.3 years
instead of 3.15 -- that is the CORRECT, reproducible behavior of this
model as currently specified, not a bug in your setup.

HOW LONG THIS TAKES
-----------------------
This is the slowest of the four scripts: expect roughly 8-12 minutes on
a typical laptop CPU (840 free parameters, and the scan-based simulation
for 128 people is real computational work per NUTS step).
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
# STEP 1: load the 175 individual-level people, split into the two
# structural groups described above
# ---------------------------------------------------------------------
df, _ = build_dataframe("PFOA")
fit_df = df[df["in_fit"] & df["endpoint"].isin(["Cserum_t", "Cbgd_Css"])].reset_index(drop=True)
cserum_df = fit_df[fit_df["endpoint"] == "Cserum_t"].reset_index(drop=True)   # time-varying exposure, needs simulation
cbgd_df = fit_df[fit_df["endpoint"] == "Cbgd_Css"].reset_index(drop=True)      # constant known exposure, closed-form
N1, N2 = len(cserum_df), len(cbgd_df)
print(f"Pooling {N1} Cserum_t (time-varying) + {N2} Cbgd_Css (constant) individuals + 4 population-summary rows")

# --- Build the "dosing schedule" matrices for the time-varying group ---
# For each of the N1 people, they have a list of exposure segments:
# (start_time, end_time, concentration_during_that_segment). Different
# people have different numbers of segments, so we PAD every person's
# schedule out to the same length M (the max anyone needs) with
# zero-concentration filler segments of zero duration -- padding a
# segment with duration 0 and concentration 0 is a no-op in the physics
# (nothing changes over zero time), so it's safe to pad this way.
M = int(cserum_df["dwc_n"].max())
t_start_mat = np.zeros((N1, M))
t_end_mat = np.zeros((N1, M))
conc_mat = np.zeros((N1, M))
for i, row in cserum_df.iterrows():
    dose_times = list(row["dwc_times"])
    dose_conc = list(row["dwc_conc"])
    tq = row["print_times"][-1]                    # the day this person's blood was actually measured
    boundaries = dose_times + [tq]                  # segment boundaries: [t0, t1, ..., t_measurement]
    boundaries += [tq] * (M + 1 - len(boundaries))  # pad remaining slots with the final (no-op) boundary
    conc_padded = dose_conc + [0.0] * (M - len(dose_conc))
    t_start_mat[i, :] = boundaries[:M]
    t_end_mat[i, :] = boundaries[1:M + 1]
    conc_mat[i, :] = conc_padded

C_0_cserum = cserum_df["C_0_in_gm"].values.astype(float)
Cbgd_gm_cserum = cserum_df["Cbgd_in_gm"].values.astype(float)
Cbgd_gsd_cserum = cserum_df["Cbgd_in_gsd"].values.astype(float)
C_0_gsd_cserum = cserum_df["C_0_in_gsd"].fillna(1.01).values.astype(float)
obs_cserum = np.array([r["data_values"][-1] for _, r in cserum_df.iterrows()])

# --- The constant-exposure group (same closed-form idea as PFNA) ---
dwc_val_bg = cbgd_df["dwc_value"].values.astype(float)
Cbgd_gm_bg = cbgd_df["Cbgd_in_gm"].values.astype(float)
Cbgd_gsd_bg = cbgd_df["Cbgd_in_gsd"].values.astype(float)
obs_bg = np.array([r["data_values"][-1] for _, r in cbgd_df.iterrows()])

# ---------------------------------------------------------------------
# STEP 2: the 4 population-summary rows
# ---------------------------------------------------------------------
pop_df = df[df["in_fit"] & df["endpoint"].isin(["M_Cserum", "M_Cbgd_Css"])].reset_index(drop=True)
assert len(pop_df) == 4, f"expected 4 population-summary rows, got {len(pop_df)}"
lubeck = pop_df[pop_df["study"].str.contains("Lubeck")].iloc[0]      # M_Cserum: decaying mean trajectory over time
hocking = pop_df[pop_df["study"].str.contains("Hocking")].iloc[0]    # M_Cserum: same
paulsboro = pop_df[pop_df["study"].str.contains("Paulsboro")].iloc[0]  # M_Cbgd_Css: single mean steady-state level
horsham = pop_df[pop_df["study"].str.contains("Horsham")].iloc[0]      # M_Cbgd_Css: same

for label, r in [("Lubeck", lubeck), ("Little Hocking", hocking),
                  ("Paulsboro", paulsboro), ("Horsham", horsham)]:
    print(f"{label}: endpoint={r['endpoint']} dwc_type={r['dwc_type']} dwc_value={r['dwc_value']} "
          f"dwc_mrl={r['dwc_mrl']} t={r['print_times']} obs={r['data_values']}")

MRL_pfoa = 0.016  # mg/L -- shared "below reporting limit" bound for Lubeck & Little Hocking

# ---------------------------------------------------------------------
# STEP 3: fixed constants (same values Chiu uses for every PFAS chemical)
# ---------------------------------------------------------------------
M_ln_DWI_BW_d_fixed = -4.3955
SD_ln_DWI_BW_d_fixed = 0.8880025
SD_ln_Cbgd_sc_fixed = 1.0
SD_ln_C_0_sc_fixed = 1.0

print(f"\nSetup done at {time.time()-t0:.1f}s. Building PyMC model...")

# ---------------------------------------------------------------------
# STEP 4: build the PyMC model
# ---------------------------------------------------------------------
with pm.Model() as pooled_model:

    # --- Population-level hyperparameters (Chiu's own priors) ---
    M_ln_k = pm.Normal("M_ln_k", mu=-1.8971, sigma=0.4055)
    # PFOA is the one chemical where Chiu puts an InverseGamma prior on the
    # elimination-rate VARIANCE instead of the Lognormal used for the other
    # three -- we keep that distinction faithfully rather than unifying it,
    # since it is what his own file specifies.
    V_ln_k = pm.InverseGamma("V_ln_k", alpha=9, beta=0.75)
    SD_ln_k = pm.Deterministic("SD_ln_k", pt.sqrt(V_ln_k))

    M_ln_Vd = pm.Normal("M_ln_Vd", mu=-1.7720, sigma=0.2624)
    SD_ln_Vd = pm.HalfNormal("SD_ln_Vd", sigma=0.2)

    M_ln_Cbgd_sc = pm.Normal("M_ln_Cbgd_sc", mu=-0.22314, sigma=0.4055)
    M_ln_C_0_sc = pm.Normal("M_ln_C_0_sc", mu=0.0, sigma=0.4055)

    # Each of the 4 distinct endpoints (individual Cserum, individual
    # Cbgd_Css, population M_Cserum, population M_Cbgd_Css) gets its OWN
    # measurement-noise GSD -- they are fit separately in Chiu's file, not
    # shared, because e.g. a population-mean estimate averaged across many
    # people is inherently less noisy than any one person's measurement.
    log_GSD_Cserum = pm.Uniform("log_GSD_Cserum", lower=np.log(1.1), upper=np.log(10.0))
    GSD_Cserum = pm.Deterministic("GSD_Cserum", pt.exp(log_GSD_Cserum))
    log_GSD_Cbgd_Css = pm.Uniform("log_GSD_Cbgd_Css", lower=np.log(1.1), upper=np.log(10.0))
    GSD_Cbgd_Css = pm.Deterministic("GSD_Cbgd_Css", pt.exp(log_GSD_Cbgd_Css))
    log_GSD_M_Cserum = pm.Uniform("log_GSD_M_Cserum", lower=np.log(1.1), upper=np.log(10.0))
    GSD_M_Cserum = pm.Deterministic("GSD_M_Cserum", pt.exp(log_GSD_M_Cserum))
    log_GSD_M_Cbgd_Css = pm.Uniform("log_GSD_M_Cbgd_Css", lower=np.log(1.1), upper=np.log(10.0))
    GSD_M_Cbgd_Css = pm.Deterministic("GSD_M_Cbgd_Css", pt.exp(log_GSD_M_Cbgd_Css))

    # Lubeck and Little Hocking each get their own below-MRL free parameter
    # (confirmed: these are genuinely separate free parameters, not shared
    # with each other or with any individual-level DWC).
    DWC_Lubeck = pm.Uniform("DWC_Lubeck", lower=0.0, upper=MRL_pfoa)
    DWC_Hocking = pm.Uniform("DWC_Hocking", lower=0.0, upper=MRL_pfoa)

    k_pop = pm.Deterministic("k_pop", pt.exp(M_ln_k))
    halflife_pop = pm.Deterministic("halflife_pop", pt.log(2) / k_pop)

    # -------------------------------------------------------------
    # Group 1: the 128 "Cserum_t" (time-varying exposure) individuals
    # -------------------------------------------------------------
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
        """
        One "step" of the loop: given where a person's blood level was
        at the START of this dosing segment (C_prev), and this segment's
        drinking-water concentration (conc_col) and duration (dt), work
        out where their level ends up by the END of the segment. This
        is the same exponential-approach-to-steady-state math as the
        single-equation PFNA formula, just applied once per segment and
        chained together (this segment's ending level becomes next
        segment's starting level).
        `t_start_col`/`t_end_col`/`conc_col` are the M columns of the
        padded matrices, `k_v`/`Vd_v`/`DWI_v`/`Cbgd_v` are the same for
        every step of one person's loop (their own fixed personal traits),
        so `pytensor.scan` passes them in as `non_sequences`.
        """
        dt = t_end_col - t_start_col
        C_ss = Cbgd_v + DWI_v * 365.25 * conc_col / (k_v * Vd_v)
        return C_ss + (C_prev - C_ss) * pt.exp(-k_v * dt)

    # `sequences` are transposed to shape (M, N1) because scan iterates
    # over the FIRST axis, one "M-th segment, all N1 people at once" step
    # at a time -- this vectorizes all 128 people's simulations together
    # instead of looping over people individually, which is what keeps
    # this fast.
    scan_out, _ = pytensor.scan(
        fn=scan_step,
        sequences=[pt.as_tensor_variable(t_start_mat.T),
                   pt.as_tensor_variable(t_end_mat.T),
                   pt.as_tensor_variable(conc_mat.T)],
        outputs_info=[C_0],                       # everyone starts their loop at their own C_0
        non_sequences=[k1, Vd1, DWI1, Cbgd1],
        n_steps=M,
    )
    C_pred_cserum = scan_out[-1]   # we only need the FINAL step's output (the level at measurement time)

    # -------------------------------------------------------------
    # Group 2: the 47 "Cbgd_Css" (constant known exposure) individuals
    # -------------------------------------------------------------
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

    # -------------------------------------------------------------
    # Population-summary rows: M_Cbgd_Css (Paulsboro, Horsham)
    # -------------------------------------------------------------
    # Identical closed-form "mean of a lognormal" formula as model_pfna.py
    # -- see that file's long comment for the full derivation.
    def M_Cbgd_Css_formula(DWC, t, Cbgd_gm_v, Cbgd_gsd_v):
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

    # -------------------------------------------------------------
    # Population-summary rows: M_Cserum (Lubeck, Little Hocking)
    # -------------------------------------------------------------
    # These two report a MEAN blood level at SEVERAL time points (a
    # decaying trajectory, not one snapshot), so the closed-form formula
    # needs an extra term tracking the population-mean starting point
    # (C_0) and background (Cbgd) decaying away over time too -- this
    # exactly matches Chiu's own MCSim CalcOutputs{} block for M_Cserum.
    # Read it as: "final level = background + (starting-level term that
    # has decayed away) - (background term that has decayed away) +
    # (steady-state term) - (steady-state term that hasn't fully arrived
    # yet)" -- the same physics as the single-person formula, just each
    # term separately averaged across the population using the E[X] =
    # exp(mu + sigma^2/2) identity.
    def M_Cserum_formula(DWC, t_vec, Cbgd_gm_v, Cbgd_gsd_v, C0_gm_v, C0_gsd_v):
        M_Cbgd = Cbgd_gm_v * pt.exp(M_ln_Cbgd_sc + (SD_ln_Cbgd_sc_fixed * np.log(Cbgd_gsd_v))**2 / 2)
        mu_Css = M_ln_DWI_BW_d_fixed + pt.log(365.25) + pt.log(DWC) - M_ln_k - M_ln_Vd
        V_Css = SD_ln_DWI_BW_d_fixed**2 + V_ln_k + SD_ln_Vd**2
        M_Css = pt.exp(mu_Css + V_Css / 2)
        M_kt = -t_vec * pt.exp(M_ln_k + V_ln_k / 2)                 # vector: one value per query time
        V_kt = (pt.exp(V_ln_k) - 1) * M_kt**2
        mu_Cbgd_expkt = pt.log(Cbgd_gm_v) + M_ln_Cbgd_sc + M_kt
        V_Cbgd_expkt = (SD_ln_Cbgd_sc_fixed * np.log(Cbgd_gsd_v))**2 + V_kt
        M_Cbgd_expkt = pt.exp(mu_Cbgd_expkt + V_Cbgd_expkt / 2)
        mu_C0_expkt = pt.log(C0_gm_v) + M_ln_C_0_sc + M_kt
        V_C0_expkt = (SD_ln_C_0_sc_fixed * np.log(C0_gsd_v))**2 + V_kt
        M_C0_expkt = pt.exp(mu_C0_expkt + V_C0_expkt / 2)
        mu_Css_expkt = M_ln_DWI_BW_d_fixed + pt.log(365.25 * DWC) - M_ln_k - M_ln_Vd + M_kt
        V_Css_expkt = SD_ln_DWI_BW_d_fixed**2 + V_ln_k + SD_ln_Vd**2 + V_kt
        M_Css_expkt = pt.exp(mu_Css_expkt + V_Css_expkt / 2)
        return M_Cbgd + M_C0_expkt - M_Cbgd_expkt + M_Css - M_Css_expkt

    t_lubeck = np.array(lubeck["print_times"], dtype=float)
    obs_lubeck = np.array(lubeck["data_values"], dtype=float)
    t_hocking = np.array(hocking["print_times"], dtype=float)
    obs_hocking = np.array(hocking["data_values"], dtype=float)

    pred_lubeck = M_Cserum_formula(DWC_Lubeck, t_lubeck, float(lubeck["Cbgd_in_gm"]), float(lubeck["Cbgd_in_gsd"]),
                                    float(lubeck["C_0_in_gm"]), float(lubeck["C_0_in_gsd"]))
    pred_hocking = M_Cserum_formula(DWC_Hocking, t_hocking, float(hocking["Cbgd_in_gm"]), float(hocking["Cbgd_in_gsd"]),
                                     float(hocking["C_0_in_gm"]), float(hocking["C_0_in_gsd"]))
    pm.Deterministic("pred_lubeck", pred_lubeck)
    pm.Deterministic("pred_hocking", pred_hocking)
    pm.LogNormal("obs_lubeck", mu=pt.log(pred_lubeck), sigma=pt.log(GSD_M_Cserum), observed=obs_lubeck)
    pm.LogNormal("obs_hocking", mu=pt.log(pred_hocking), sigma=pt.log(GSD_M_Cserum), observed=obs_hocking)

    n_params = N1 * 5 + N2 * 4 + 12
    print(f"Model built at {time.time()-t0:.1f}s ({n_params} free parameters)")

    # target_accept=0.95 here (vs 0.99 for the smaller chemicals) -- PFOA's
    # posterior isn't as stiff, and with 840 free parameters, a slightly
    # lower target_accept keeps runtime reasonable without inflating
    # divergences meaningfully. cores=1 is required in this sandboxed
    # environment; use more cores on your own machine to parallelize the
    # 4 chains and speed this up.
    idata = pm.sample(1500, tune=1500, chains=4, cores=1, target_accept=0.95,
                       random_seed=42, progressbar=True)

print(f"\nSampling finished at {time.time()-t0:.1f}s total")
idata.to_netcdf("model_pfoa_results.nc")

# ---------------------------------------------------------------------
# STEP 5: summarize and check convergence
# ---------------------------------------------------------------------
summary = az.summary(idata, var_names=["M_ln_k", "SD_ln_k", "k_pop", "halflife_pop",
                                        "M_ln_Vd", "SD_ln_Vd", "GSD_Cserum", "GSD_Cbgd_Css",
                                        "GSD_M_Cserum", "GSD_M_Cbgd_Css"])
print("\nPopulation-level posterior summary:")
print(summary)

halflife_samples = idata.posterior["halflife_pop"].values.flatten()
print(f"\n{'='*70}")
print(f"PFOA POPULATION half-life (yr): median = {np.median(halflife_samples):.2f}, "
      f"90% CI = [{np.percentile(halflife_samples,5):.2f}, {np.percentile(halflife_samples,95):.2f}]")
print("Chiu's ACTUAL published PFOA estimate (from his raw MCMC chain): 3.15 yr [2.62-3.74] (95% CI)")
print("(Our replication typically lands around 4.2-4.3 yr -- see this script's module docstring, ")
print(" 'AN HONEST NEGATIVE RESULT', for why that is a known, unresolved gap, not a bug.)")
print(f"{'='*70}")

Vd_pop_samples = np.exp(idata.posterior["M_ln_Vd"].values.flatten())
print(f"\nPopulation Vd (L/kg): median = {np.median(Vd_pop_samples):.3f} "
      f"(Chiu's real fitted PFOA Vd: 0.432 L/kg -- this part usually matches well)")

worst_rhat = summary["r_hat"].max()
n_div = int(idata.sample_stats["diverging"].values.sum())
print(f"\nWorst r_hat: {worst_rhat:.4f} (want < 1.01) | divergences: {n_div}")

# ---------------------------------------------------------------------
# STEP 6: plot
# ---------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
ax = axes[0]
ax.hist(halflife_samples, bins=60, density=True, color="mediumpurple", alpha=0.8, label="Our PFOA model")
ax.axvline(3.15, color="red", lw=2, ls=":", label="Chiu published: 3.15 yr")
ax.axvspan(2.62, 3.74, color="red", alpha=0.1, label="Chiu published 95% CI")
ax.set_xlabel("population half-life (yr)")
ax.set_ylabel("posterior density")
ax.set_title("PFOA population half-life: our replication vs. published")
ax.legend(fontsize=7.5)
ax.set_xlim(0, 10)

ax = axes[1]
for c in range(idata.posterior.sizes["chain"]):
    ax.plot(idata.posterior["halflife_pop"].values[c], lw=0.6, alpha=0.8, label=f"chain {c+1}")
ax.axhline(3.15, color="red", ls=":", lw=1.5)
ax.set_xlabel("MCMC draw number")
ax.set_ylabel("population half-life (yr)")
ax.set_title("Trace plot: do the 4 chains agree?")
ax.legend(fontsize=7, ncol=2)

plt.tight_layout()
plt.savefig("model_pfoa_results.png", dpi=150)
print("\nSaved plot to model_pfoa_results.png")
