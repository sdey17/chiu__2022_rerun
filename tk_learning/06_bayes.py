"""
LESSON 6 -- The same model in PyMC, and what Bayes buys you.

Nothing about the kinetics changes. C(t) = (dose/Vd)*exp(-k*t) is still
the model. What changes is what we do with uncertainty:

    least squares   one best answer + a normal approximation to its
                    uncertainty, valid near the optimum, conditional on
                    the model being right

    Bayes           a full distribution over parameters, which you can
                    push through any function you like (half-life,
                    clearance, a prediction in 2035) and get the right
                    uncertainty for THAT quantity automatically

Three things you get that NLS cannot give you easily:
    * priors, so the fit cannot run off to biologically absurd values
    * hierarchy, so animals share strength without being forced equal
    * exact uncertainty on derived quantities, no delta method

Run:  python 06_bayes.py        (about 1-2 minutes)
"""
import numpy as np
import pymc as pm
import arviz as az

from tk import load, half_life

SEED = 20260929
mk = load("PFOA_Male_primate")
mk = mk[mk.conc_mgL > 0]
DOSE = 10.0

animals = np.sort(mk.animal_id.unique())
idx = np.searchsorted(animals, mk.animal_id.values)
t = mk.time_d.values
y = np.log(mk.conc_mgL.values)

print(f"Data: {len(mk)} observations, {len(animals)} monkeys, 10 mg/kg IV PFOA\n")


# ----------------------------------------------------------------------
# A. Pooled model: one Vd and one k for all three animals
# ----------------------------------------------------------------------
def pooled():
    with pm.Model() as m:
        # Priors on the LOG of each parameter -- guarantees positivity,
        # and a lognormal is the natural prior for a rate or a volume.
        #   ln Vd ~ N(ln 0.2, 0.5)  means: "most likely around 0.2 L/kg,
        #   and a factor of exp(2*0.5) = 2.7 either way is unremarkable"
        ln_Vd = pm.Normal("ln_Vd", np.log(0.2), 0.5)
        ln_k = pm.Normal("ln_k", np.log(0.06), 0.7)
        sigma = pm.HalfNormal("sigma", 0.5)      # residual SD on log scale

        mu = np.log(DOSE) - ln_Vd - pm.math.exp(ln_k) * t
        pm.Normal("obs", mu=mu, sigma=sigma, observed=y)

        # Deterministics are computed for every posterior draw, so their
        # uncertainty is exact -- no error propagation formula needed.
        pm.Deterministic("Vd", pm.math.exp(ln_Vd))
        pm.Deterministic("k", pm.math.exp(ln_k))
        pm.Deterministic("half_life", np.log(2) / pm.math.exp(ln_k))
        pm.Deterministic("CL", pm.math.exp(ln_k + ln_Vd))
    return m


# ----------------------------------------------------------------------
# B. Hierarchical model: each animal gets its own k and Vd
# ----------------------------------------------------------------------
def hierarchical():
    with pm.Model() as m:
        mu_ln_Vd = pm.Normal("mu_ln_Vd", np.log(0.2), 0.5)
        mu_ln_k = pm.Normal("mu_ln_k", np.log(0.06), 0.7)
        # Between-animal spread. HalfNormal(0.3) says "animals differ by
        # tens of percent, not orders of magnitude". Watch what happens:
        # the posterior for sd_ln_k comes back at about 0.48, well past
        # the prior's scale, because these three monkeys really do
        # differ by 3x. The data overruled the prior -- which is the
        # behaviour you want, and worth checking every time.
        sd_ln_Vd = pm.HalfNormal("sd_ln_Vd", 0.3)
        sd_ln_k = pm.HalfNormal("sd_ln_k", 0.3)

        # NON-CENTRED parameterisation: sample a standard normal z and
        # shift/scale it, rather than sampling the animal value directly.
        # Mathematically identical, far easier for the sampler when the
        # group-level SD is small. Chiu's model uses the same trick.
        z_Vd = pm.Normal("z_Vd", 0, 1, shape=len(animals))
        z_k = pm.Normal("z_k", 0, 1, shape=len(animals))
        ln_Vd_i = pm.Deterministic("ln_Vd_i", mu_ln_Vd + sd_ln_Vd * z_Vd)
        ln_k_i = pm.Deterministic("ln_k_i", mu_ln_k + sd_ln_k * z_k)

        sigma = pm.HalfNormal("sigma", 0.5)
        mu = np.log(DOSE) - ln_Vd_i[idx] - pm.math.exp(ln_k_i[idx]) * t
        pm.Normal("obs", mu=mu, sigma=sigma, observed=y)

        pm.Deterministic("half_life_pop", np.log(2) / pm.math.exp(mu_ln_k))
        pm.Deterministic("half_life_i", np.log(2) / pm.math.exp(ln_k_i))
    return m


def run(m, name):
    with m:
        idata = pm.sample(1500, tune=1500, chains=4, random_seed=SEED,
                          target_accept=0.95, progressbar=False,
                          idata_kwargs={"log_likelihood": True})
    print(f"\n--- {name} ---")
    div = int(idata.sample_stats.diverging.sum())
    rhat = float(az.rhat(idata).to_array().max())
    print(f"divergences {div}   worst r-hat {rhat:.4f}"
          f"   {'OK' if div == 0 and rhat < 1.01 else 'CHECK THIS'}")
    return idata


if __name__ == "__main__":
    ip = run(pooled(), "pooled")
    print(az.summary(ip, var_names=["Vd", "k", "half_life", "CL", "sigma"],
                     hdi_prob=0.95).to_string())
    print("""
   Read the table: 'mean' is the posterior mean, hdi_2.5%/97.5% the
   credible interval -- the range containing 95% of the posterior
   probability, which is what most people wrongly think a confidence
   interval is. ess_bulk should be in the thousands, r_hat below 1.01.

   Check it against least squares on the SAME data (all three animals,
   `curve_fit` as in lesson 04): Vd 0.174 L/kg, half-life 11.29 days.
   The posterior means are 0.180 and 11.46 -- agreement to a couple of
   percent, which is what you should expect with weak priors and 43
   observations. If they had disagreed, the prior would be doing work
   you did not intend.

   (Lesson 04's 8.59 days is not the comparison: that fit used monkey
   2054 alone, and 2054 is the fastest of the three.)
""")

    ih = run(hierarchical(), "hierarchical")
    print(az.summary(ih, var_names=["half_life_pop", "half_life_i",
                                    "sd_ln_k", "sigma"],
                     hdi_prob=0.95).to_string())
    print("""
   Now each monkey has its own half-life, and the population value has
   its own uncertainty on top. Look at sigma: it should have dropped
   sharply from the pooled model, because variation that the pooled fit
   had to call 'noise' is now explained by animals genuinely differing:
   0.85 pooled against 0.48 hierarchical, on the log scale. Half the
   apparent "measurement error" was in fact one monkey clearing PFOA
   three times more slowly than the other two (27 days against 9).

   That is PARTIAL POOLING. Each animal's estimate is pulled towards
   the population mean by an amount that depends on how much data that
   animal has -- automatically, with no tuning. It is the single most
   useful idea in applied Bayesian modelling, and it is exactly what
   Chiu's three-level human model (../model.py) is doing at scale.
""")

    comp = az.compare({"pooled": ip, "hierarchical": ih}, ic="loo")
    print(comp.to_string())
    print("""
   LOO (leave-one-out cross-validation) estimates out-of-sample
   predictive accuracy. Higher elpd_loo is better; the ranking is what
   matters, and elpd_diff should be compared to its own standard error
   (dse) -- a difference smaller than about 2*dse is not decisive.

   This is the same tool the EPA pipeline uses to choose between one and
   two compartments, and the same one lesson 07 will use.

QUESTIONS
  1. The pooled model's sigma mixes measurement error with
     between-animal differences. Which one does the hierarchical model
     move it into? Check the numbers.
  2. Change the prior on ln_k to Normal(log(0.06), 0.05) -- very tight.
     Does the posterior move? What does that tell you about how much the
     data are actually saying?
  3. sd_ln_k is estimated from three animals. Set its prior to
     HalfNormal(2.0) and rerun. What happens, and why is that a warning
     about hierarchical models on small groups?
  4. Why is 'half_life' a Deterministic rather than something you
     compute afterwards from the posterior mean of k? (Hint: is
     ln2/mean(k) the same as mean(ln2/k)?)

EXERCISES
  a. Add a Deterministic for the predicted concentration at day 200 and
     report its credible interval. Notice how wide it is -- that is
     honest extrapolation uncertainty, and NLS will not hand it to you.
  b. Fit the PFOS monkey data (PFOS_Male_primate, 2 mg/kg IV) the same
     way. PFOS should come out slower. By how much, and do the
     intervals overlap?
  c. Run az.plot_trace and az.plot_pair on the pooled fit. The Vd-k
     correlation from lesson 04 section C should be visible directly.
""")
