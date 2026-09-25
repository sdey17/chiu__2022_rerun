"""
model_pfna.py
=============
Bayesian hierarchical toxicokinetic model for PFNA (perfluorononanoic
acid), replicating Chiu et al. 2022's MCSim model in pure Python/PyMC.

START HERE IF YOU ARE NEW TO THIS
------------------------------------
This is the SIMPLEST of the four chemical scripts in this folder, so
read this one first even if PFNA isn't the chemical you care about --
the other three (model_pfoa.py, model_pfos.py, model_pfhxs.py) reuse
every idea introduced here and just add complexity on top.

THE SCIENTIFIC QUESTION
--------------------------
PFNA is a "forever chemical" that the body eliminates slowly. If you
measure someone's blood concentration once, you can't tell their
elimination half-life from that alone -- you need to know (a) how much
of it they're drinking (exposure) and (b) either how their level changes
over time, or how their level compares to a population at steady state.
Chiu et al. pooled data from several U.S. contamination sites and fit
ONE population-level elimination rate that explains all of it at once.
We want their same population-level half-life estimate.

THE MODEL, IN PLAIN WORDS
-----------------------------
Assume everyone's body behaves like a single, well-mixed compartment.
Water goes in at some daily rate, the chemical builds up, and it leaves
at a rate proportional to how much is currently in the body (first-order
elimination) -- for people with a lifetime of *constant* drinking-water
exposure, this reaches a steady-state blood concentration:

    Css = (dose rate) / (elimination rate x volume of distribution)
        = (DWI_BW_d * DWC) / (k * Vd)

  where:
    DWI_BW_d = daily water intake per body weight (L/kg-day)
    DWC      = drinking water concentration (mg/L or similar)
    k        = elimination rate constant (1/day) -- what we actually want
    Vd       = volume of distribution (L/kg) -- how "diluted" the
               chemical is across body tissue relative to blood

Half-life = ln(2) / k. That's the number this whole exercise is chasing.

We don't get to observe k or Vd directly for any one person -- we only
observe their blood concentration. So we build a HIERARCHICAL model:
each person's own k and Vd are draws from a shared population
distribution, and we let the data (everyone's measured blood levels
at once) tell us what that population distribution must have been for
the observations to make sense. This is exactly the same idea as a
mixed-effects / random-effects model in classical statistics, just
solved by full Bayesian sampling (MCMC) instead of maximum likelihood.

WHY LOG-SPACE EVERYWHERE?
----------------------------
Concentrations, rates, and volumes are all strictly positive and tend to
be lognormally distributed (multiplicative variation, not additive) --
this is standard practice in pharmacokinetics. So every population
parameter here is actually the MEAN OF THE LOG of the underlying
quantity (we prefix these "M_ln_..."), and every individual deviation
is a z-score (standard normal) scaled by a population standard
deviation in log-space ("SD_ln_..." or its square, "V_ln_..."):

    ln(k_person_i) = M_ln_k + SD_ln_k * z_k[i]
    k_person_i     = exp(M_ln_k + SD_ln_k * z_k[i])

If z_k[i] = 0 (perfectly average person), k_person_i = exp(M_ln_k), i.e.
M_ln_k is the log of the POPULATION MEDIAN elimination rate. This
"non-centered parameterization" (sampling the z-scores instead of the
individual k's directly) is a well-known trick that makes MCMC sample
far more efficiently for hierarchical models -- if you ever see NUTS
struggling with a hierarchical model, this is usually the first fix to
reach for.

TWO KINDS OF DATA POINTS IN THIS MODEL
------------------------------------------
1. INDIVIDUAL blood measurements ("Cserum_t" endpoint): 18 people from
   Decatur, WV with constant below-the-detection-limit exposure. Each
   person contributes one observed blood concentration.
2. POPULATION-SUMMARY measurements ("M_Cbgd_Css" endpoint): 2 rows
   (Paulsboro NJ and Horsham PA) where Chiu's data is not individual
   blood draws but the reported ARITHMETIC MEAN blood concentration
   across an entire exposed population. This needs its own closed-form
   formula (see M_Cbgd_Css_formula below) because "the mean of a
   lognormal population" is not the same number as "the lognormal
   value at the mean parameters" -- see the E[X] = exp(mu + sigma^2/2)
   comment inline.

   THIS MATTERS A LOT: an earlier version of this replication (without
   the population-summary rows) got PFNA's half-life to 3.60 years
   against Chiu's real published 2.31 years -- a large miss. Adding
   just these 2 extra data rows pulled it to 2.89 years, closing most
   of the gap, because the drinking-water-concentration free parameters
   these people have DWC constraints that meaningfully sharpen the
   fit for the whole population. Don't skip this half of the data.

EXPECTED RESULT
-------------------
Chiu's own published PFNA half-life (recomputed directly from his raw
saved MCMC chains, not from his write-up text -- see README for why we
don't trust the write-up text) is 2.31 years, 95% CI [1.62, 3.15]. This
script should land close to that (we got 2.89 years, 90% CI [1.92, 4.87]
in our own run -- a good, though not perfect, match; see README's "how
close is close enough" section).

HOW LONG THIS TAKES
-----------------------
On a typical laptop CPU, expect roughly 1-3 minutes for the full
sample() call below.
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
# STEP 1: load and filter the data
# ---------------------------------------------------------------------
# build_dataframe() gives us EVERY Simulation{} block in Chiu's PFNA
# input file, including held-out/validation-only rows. We only want the
# ones that actually feed the likelihood (in_fit == True) -- see
# parse_chiu_data.py's docstring for why that flag, not any comment
# text, is the reliable way to tell "training" from "test" data.
df, _ = build_dataframe("PFNA")
fit_df = df[df["in_fit"] & (df["endpoint"] == "Cserum")].reset_index(drop=True)
N = len(fit_df)
print(f"PFNA: pooling {N} Decatur individuals + 2 population-summary rows")

# All 18 Decatur individuals share the same "below the method reporting
# limit" (MRL) exposure situation: we don't know each person's exact
# drinking-water concentration, only that it was somewhere between 0 and
# the MRL. So instead of 18 separate unknown DWC values, the model
# has just ONE shared free parameter (DWC_belowMRL) for the whole group
# -- this mirrors exactly how Chiu's own MCSim file declares it.
MRL = 0.02  # mg/L, from Chiu's file (the Uniform(0, MRL) prior bound)
Cbgd_gm = fit_df["Cbgd_in_gm"].values.astype(float)     # background-concentration prior, geometric mean
Cbgd_gsd = fit_df["Cbgd_in_gsd"].values.astype(float)   # ...and geometric standard deviation
C_0_gm = fit_df["C_0_in_gm"].values.astype(float)       # starting-concentration prior, geometric mean
C_0_gsd = fit_df["C_0_in_gsd"].fillna(1.01).values.astype(float)  # (near-1 GSD = "essentially fixed" for people with no real prior spread)
t_query = np.array([r["print_times"][-1] for _, r in fit_df.iterrows()])  # time (days) each person's blood was drawn
obs = np.array([r["data_values"][-1] for _, r in fit_df.iterrows()])      # the actually-observed blood concentration

# The 2 population-summary rows (Paulsboro, Horsham). Each has its own
# reported drinking-water concentration as a genuinely separate free
# parameter (confirmed directly against Chiu's file: each site declares
# its own independent Distrib(DWC_belowMRL, ...), they are NOT the same
# free parameter as Decatur's DWC_belowMRL above, despite the shared name).
pop_df = df[df["in_fit"] & (df["endpoint"] == "M_Cbgd_Css")].reset_index(drop=True)
assert len(pop_df) == 2
paulsboro = pop_df[pop_df["study"].str.contains("Paulsboro")].iloc[0]
horsham = pop_df[pop_df["study"].str.contains("Horsham")].iloc[0]
print(f"Paulsboro: DWC={paulsboro['dwc_value']} t={paulsboro['print_times']} obs={paulsboro['data_values']}")
print(f"Horsham:   DWC={horsham['dwc_value']} t={horsham['print_times']} obs={horsham['data_values']}")

# ---------------------------------------------------------------------
# STEP 2: constants Chiu's model treats as FIXED, not fitted
# ---------------------------------------------------------------------
# Daily water intake per body weight is not estimated from this data at
# all -- Chiu fixes it (as literal constants, not a Distrib()) to values
# from a separate exposure-factors reference. We checked his source file
# directly before deciding to keep these fixed, rather than assuming.
M_ln_DWI_BW_d_fixed = -4.3955   # log of the population median (L/kg-day)
SD_ln_DWI_BW_d_fixed = 0.888    # log-space population SD

# The lognormal "spread" used to convert someone's background/C0 prior's
# GSD into a log-space standard deviation is likewise a fixed constant
# in Chiu's model, not something the data updates.
SD_ln_Cbgd_sc_fixed = 1.0
SD_ln_C_0_sc_fixed = 1.0

print(f"\nSetup done at {time.time()-t0:.1f}s. Building PyMC model...")

# ---------------------------------------------------------------------
# STEP 3: build the PyMC model
# ---------------------------------------------------------------------
with pm.Model() as pfna_model:

    # --- Population-level hyperparameters ---
    # These priors are Chiu's OWN priors (copied from his MCSim file),
    # not something we chose -- we want to reproduce his fit, not invent
    # a different one. Normal(mu, sigma) here means "our prior belief
    # about the log of the population value", centered at his rough
    # guess with room to move.
    M_ln_k = pm.Normal("M_ln_k", mu=-1.60944, sigma=0.4055)   # elimination rate, log-space population mean
    V_ln_k = pm.Lognormal("V_ln_k", mu=np.log(0.12), sigma=np.log(1.335))  # elimination rate, log-space population VARIANCE (not SD)
    SD_ln_k = pm.Deterministic("SD_ln_k", pt.sqrt(V_ln_k))     # convert variance -> SD for use below

    M_ln_Vd = pm.Normal("M_ln_Vd", mu=-1.60944, sigma=0.2624)  # volume of distribution, log-space population mean
    SD_ln_Vd = pm.HalfNormal("SD_ln_Vd", sigma=0.17)           # volume of distribution, log-space population SD

    M_ln_Cbgd_sc = pm.Normal("M_ln_Cbgd_sc", mu=-0.22314, sigma=0.4055)  # background-concentration "scale correction"
    M_ln_C_0_sc = pm.Normal("M_ln_C_0_sc", mu=0.0, sigma=0.4055)          # starting-concentration "scale correction"

    # Measurement-noise parameters (how much scatter is allowed between
    # a person's PREDICTED blood level and their ACTUALLY OBSERVED one,
    # beyond what the individual-level z-scores already explain).
    # Chiu declares these on a log-uniform prior between GSD 1.1 and 10 --
    # we implement "log-uniform" as literally Uniform() on log(GSD).
    log_GSD_Cserum = pm.Uniform("log_GSD_Cserum", lower=np.log(1.1), upper=np.log(10.0))
    GSD_Cserum = pm.Deterministic("GSD_Cserum", pt.exp(log_GSD_Cserum))
    log_GSD_M_Cbgd_Css = pm.Uniform("log_GSD_M_Cbgd_Css", lower=np.log(1.1), upper=np.log(10.0))
    GSD_M_Cbgd_Css = pm.Deterministic("GSD_M_Cbgd_Css", pt.exp(log_GSD_M_Cbgd_Css))

    # The single shared "below MRL" drinking-water-concentration free
    # parameter for the 18 Decatur individuals.
    DWC_belowMRL = pm.Uniform("DWC_belowMRL", lower=0.0, upper=MRL)

    # Convenience outputs: the population MEDIAN elimination rate and
    # half-life. This is the number we actually care about at the end.
    k_pop = pm.Deterministic("k_pop", pt.exp(M_ln_k))
    halflife_pop = pm.Deterministic("halflife_pop", pt.log(2) / k_pop)

    # --- Individual-level z-scores (non-centered parameterization) ---
    # One z-score per person per quantity that varies person-to-person.
    # These are what actually make this a HIERARCHICAL model: 18 people
    # each get their own implied k, Vd, exposure, background, and
    # starting concentration, all built from the SAME shared population
    # hyperparameters above plus their own personal random deviation.
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

    # --- The actual one-compartment TK prediction, per person ---
    # Css: the steady-state concentration this person's exposure would
    # eventually reach (see the module docstring's formula).
    # C_pred: blend from their (background) starting point toward Css,
    # at the exponential rate k, evaluated at their own query time.
    Css = DWI_BW_d * 365.25 * DWC_belowMRL / (k * Vd)
    C_pred = Cbgd + (C_0 - Cbgd) * pt.exp(-k * t_query) + Css * (1 - pt.exp(-k * t_query))
    pm.Deterministic("C_pred", C_pred)

    # The likelihood: we observe each person's blood level as a lognormal
    # draw around our model's prediction, with noise GSD_Cserum.
    pm.LogNormal("obs", mu=pt.log(C_pred), sigma=pt.log(GSD_Cserum), observed=obs)

    # -------------------------------------------------------------
    # Population-summary rows (Paulsboro, Horsham): closed-form formula
    # -------------------------------------------------------------
    # These 2 data points are each "the arithmetic mean blood level
    # across an entire exposed population at steady state", not any one
    # person's level. We cannot just plug population-average parameters
    # into the single-person formula above and call it done -- because
    # of Jensen's inequality, E[exp(X)] != exp(E[X]) for a random
    # variable X. We need the TRUE expectation of a lognormally
    # distributed quantity, which has a closed form:
    #     if ln(Y) ~ Normal(mu, sigma^2), then E[Y] = exp(mu + sigma^2/2)
    # This formula (matching Chiu's own MCSim CalcOutputs{} block exactly)
    # works out the mean and variance of ln(Css) across the WHOLE
    # population (folding in exposure variability, k variability, and Vd
    # variability all at once) and then applies that E[Y] identity.
    def M_Cbgd_Css_formula(DWC, t):
        M_Cbgd = Cbgd_gm_pop * pt.exp(M_ln_Cbgd_sc + (SD_ln_Cbgd_sc_fixed * np.log(Cbgd_gsd_pop))**2 / 2)
        mu_Css = M_ln_DWI_BW_d_fixed + pt.log(365.25) + pt.log(DWC) - M_ln_k - M_ln_Vd
        V_Css = SD_ln_DWI_BW_d_fixed**2 + V_ln_k + SD_ln_Vd**2
        M_kt = -t * pt.exp(M_ln_k + V_ln_k / 2)
        V_kt = (pt.exp(V_ln_k) - 1) * M_kt**2
        M_Css_expkt = pt.exp(mu_Css + M_kt + (V_Css + V_kt) / 2)
        return M_Cbgd + M_Css_expkt

    Cbgd_gm_pop = float(paulsboro["Cbgd_in_gm"])   # both rows share the same background prior in Chiu's file
    Cbgd_gsd_pop = float(paulsboro["Cbgd_in_gsd"])
    DWC_Horsham = pm.Uniform("DWC_Horsham", lower=0.0, upper=0.02)  # Horsham's own separate below-MRL free parameter

    pred_paulsboro = M_Cbgd_Css_formula(0.072, float(paulsboro["print_times"][0]))   # Paulsboro's DWC is a known fixed literal
    pred_horsham = M_Cbgd_Css_formula(DWC_Horsham, float(horsham["print_times"][0]))
    pm.Deterministic("pred_paulsboro", pred_paulsboro)
    pm.Deterministic("pred_horsham", pred_horsham)
    pm.LogNormal("obs_paulsboro", mu=pt.log(pred_paulsboro), sigma=pt.log(GSD_M_Cbgd_Css),
                 observed=float(paulsboro["data_values"][0]))
    pm.LogNormal("obs_horsham", mu=pt.log(pred_horsham), sigma=pt.log(GSD_M_Cbgd_Css),
                 observed=float(horsham["data_values"][0]))

    n_params = N * 5 + 9
    print(f"Model built at {time.time()-t0:.1f}s ({n_params} free parameters)")

    # -------------------------------------------------------------
    # STEP 4: run MCMC (NUTS -- the No-U-Turn Sampler)
    # -------------------------------------------------------------
    # NUTS explores the posterior by simulating physics: it treats the
    # negative log-posterior as a landscape and "rolls a ball" across it,
    # using the gradient to know which way is downhill. tune=2000 draws
    # are spent letting it learn a good step size (and thrown away, not
    # part of your results); draws=2000 are the actual samples you keep.
    # chains=4 independent chains, started from different random points,
    # let us check that they all converged to the SAME answer (that
    # check is the "r_hat" statistic printed below -- values very close
    # to 1.00 mean the chains agree with each other).
    #
    # target_accept=0.99 is set HIGH (default is usually 0.8) because
    # this model has a mildly "stiff" region of the posterior (see
    # README's "divergences" section) -- a higher target_accept makes
    # NUTS take smaller, more careful steps, at the cost of being a bit
    # slower, in exchange for avoiding spurious divergence warnings here.
    #
    # cores=1 is REQUIRED in this particular sandboxed environment
    # (PyMC's multiprocessing hangs here) -- on your own machine you can
    # likely set cores=4 to run the 4 chains in parallel and go faster.
    idata = pm.sample(2000, tune=2000, chains=4, cores=1, target_accept=0.99,
                       random_seed=42, progressbar=True)

print(f"\nSampling finished at {time.time()-t0:.1f}s total")
idata.to_netcdf("model_pfna_results.nc")   # save the full posterior for later reloading/plotting

# ---------------------------------------------------------------------
# STEP 5: summarize and check convergence
# ---------------------------------------------------------------------
summary = az.summary(idata, var_names=["M_ln_k", "SD_ln_k", "k_pop", "halflife_pop",
                                        "M_ln_Vd", "SD_ln_Vd", "GSD_Cserum", "GSD_M_Cbgd_Css",
                                        "DWC_belowMRL"])
print("\nPopulation-level posterior summary:")
print(summary)

halflife_samples = idata.posterior["halflife_pop"].values.flatten()
print(f"\n{'='*70}")
print(f"PFNA POPULATION half-life (yr): median = {np.median(halflife_samples):.2f}, "
      f"90% CI = [{np.percentile(halflife_samples,5):.2f}, {np.percentile(halflife_samples,95):.2f}]")
print("Chiu's ACTUAL published PFNA estimate (from his raw MCMC chain): 2.31 yr [1.62-3.15] (95% CI)")
print(f"{'='*70}")

Vd_pop_samples = np.exp(idata.posterior["M_ln_Vd"].values.flatten())
print(f"\nPopulation Vd (L/kg): median = {np.median(Vd_pop_samples):.3f} "
      f"(Chiu's real fitted PFNA Vd: 0.187 L/kg)")

# r_hat close to 1.00 (< 1.01 is the usual rule of thumb) means the 4
# independent chains agree -- strong evidence of convergence.
# "divergences" are a NUTS-specific warning: the simulated trajectory's
# energy blew up locally, usually a sign of a stiff/funnel-shaped region.
# A handful is not automatically fatal (see README) but zero is best.
worst_rhat = summary["r_hat"].max()
n_div = int(idata.sample_stats["diverging"].values.sum())
print(f"\nWorst r_hat: {worst_rhat:.4f} (want < 1.01) | divergences: {n_div} (want 0, a few is usually tolerable)")

# ---------------------------------------------------------------------
# STEP 6: plot
# ---------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

ax = axes[0]
ax.hist(halflife_samples, bins=60, density=True, color="steelblue", alpha=0.8, label="Our PFNA model")
ax.axvline(2.31, color="red", lw=2, ls=":", label="Chiu published: 2.31 yr")
ax.axvspan(1.62, 3.15, color="red", alpha=0.1, label="Chiu published 95% CI")
ax.set_xlabel("population half-life (yr)")
ax.set_ylabel("posterior density")
ax.set_title("PFNA population half-life: our replication vs. published")
ax.legend(fontsize=8)

ax = axes[1]
for c in range(idata.posterior.sizes["chain"]):
    ax.plot(idata.posterior["halflife_pop"].values[c], lw=0.6, alpha=0.8, label=f"chain {c+1}")
ax.axhline(2.31, color="red", ls=":", lw=1.5)
ax.set_xlabel("MCMC draw number")
ax.set_ylabel("population half-life (yr)")
ax.set_title("Trace plot: do the 4 chains agree? (a good trace looks like 'fuzzy caterpillars' overlapping)")
ax.legend(fontsize=7, ncol=2)

plt.tight_layout()
plt.savefig("model_pfna_results.png", dpi=150)
print("\nSaved plot to model_pfna_results.png")
