"""
LESSON 7 -- Where one compartment fails, and why that leads to PBPK.

Lesson 02 showed the monkey curve bending on a log axis. Lesson 04
showed the residuals of a one-compartment fit marching in a systematic
pattern. Both say the same thing: the body is not one well-mixed bucket.

The minimal repair is a second compartment -- a tissue pool that the
chemical distributes into and comes back out of:

    central (blood)      <---k12/k21--->     peripheral (tissue)
         |
        k10 (elimination)

This lesson fits both models properly, compares them by LOO, and then
asks what the second compartment actually IS. That question is the one
PBPK exists to answer.

Run:  python 07_two_compartment.py     (about 2-3 minutes)
"""
import numpy as np
import pymc as pm
import pytensor.tensor as pt
import arviz as az

from tk import load

SEED = 20260929
mk = load("PFOA_Male_primate")
mk = mk[mk.conc_mgL > 0]
DOSE = 10.0
animals = np.sort(mk.animal_id.unique())
idx = np.searchsorted(animals, mk.animal_id.values)
t, y = mk.time_d.values, np.log(mk.conc_mgL.values)
na = len(animals)


def one_compartment():
    with pm.Model() as m:
        mu_V = pm.Normal("mu_ln_V", np.log(0.2), 0.5)
        mu_k = pm.Normal("mu_ln_k", np.log(0.06), 0.7)
        sd_V = pm.HalfNormal("sd_ln_V", 0.3)
        sd_k = pm.HalfNormal("sd_ln_k", 0.5)
        V = pm.math.exp(mu_V + sd_V * pm.Normal("zV", 0, 1, shape=na))[idx]
        k = pm.math.exp(mu_k + sd_k * pm.Normal("zk", 0, 1, shape=na))[idx]
        sigma = pm.HalfNormal("sigma", 0.5)
        pm.Normal("obs", pt.log(DOSE / V) - k * t, sigma, observed=y)
        pm.Deterministic("half_life_pop", np.log(2) / pm.math.exp(mu_k))
    return m


def two_compartment():
    """Same hierarchy, but the analytical two-compartment solution.

    Parameterised by (V1, k10, k12, k21) rather than the eigenvalues,
    because those are the physiological quantities: V1 is the volume the
    dose mixes into immediately, k10 is elimination, and k12/k21 are
    exchange with tissue.
    """
    with pm.Model() as m:
        mu = {n: pm.Normal(f"mu_ln_{n}", np.log(v), s)
              for n, v, s in [("V1", 0.15, 0.5), ("k10", 0.08, 0.7),
                              ("k12", 0.3, 1.0), ("k21", 0.3, 1.0)]}
        sd = {n: pm.HalfNormal(f"sd_ln_{n}", 0.4) for n in mu}
        p = {n: pm.math.exp(mu[n] + sd[n] * pm.Normal(f"z_{n}", 0, 1, shape=na))
             for n in mu}
        V1, k10, k12, k21 = (p["V1"][idx], p["k10"][idx],
                             p["k12"][idx], p["k21"][idx])

        s = k10 + k12 + k21
        disc = pt.sqrt(pt.maximum(s ** 2 - 4 * k10 * k21, 1e-12))
        alpha, beta = (s + disc) / 2, (s - disc) / 2     # fast, slow
        c0 = DOSE / V1
        A = c0 * (alpha - k21) / (alpha - beta)
        B = c0 * (k21 - beta) / (alpha - beta)
        conc = A * pt.exp(-alpha * t) + B * pt.exp(-beta * t)

        sigma = pm.HalfNormal("sigma", 0.5)
        pm.Normal("obs", pt.log(pt.maximum(conc, 1e-12)), sigma, observed=y)

        # The reported half-life of a two-compartment model is the SLOW
        # (terminal) one, beta -- that is what governs long-term burden.
        s_pop = pm.math.exp(mu["k10"]) + pm.math.exp(mu["k12"]) + pm.math.exp(mu["k21"])
        d_pop = pt.sqrt(pt.maximum(
            s_pop ** 2 - 4 * pm.math.exp(mu["k10"]) * pm.math.exp(mu["k21"]), 1e-12))
        pm.Deterministic("half_life_terminal", np.log(2) / ((s_pop - d_pop) / 2))
        pm.Deterministic("half_life_alpha", np.log(2) / ((s_pop + d_pop) / 2))
        # Vss = V1*(1 + k12/k21): total volume once tissue has filled
        pm.Deterministic("Vss", pm.math.exp(mu["V1"]) *
                         (1 + pm.math.exp(mu["k12"] - mu["k21"])))
        pm.Deterministic("CL", pm.math.exp(mu["V1"] + mu["k10"]))
    return m


def fit(m, name):
    """Sample, and cache the result so you can re-analyse without refitting."""
    import os
    cache = f"trace_{name}.nc"
    if os.path.exists(cache):
        print(f"{name:18s} loaded from {cache}")
        return az.from_netcdf(cache)
    with m:
        i = pm.sample(2000, tune=2000, chains=4, random_seed=SEED,
                      target_accept=0.95, progressbar=False,
                      idata_kwargs={"log_likelihood": True})
    div = int(i.sample_stats.diverging.sum())
    print(f"{name:18s} divergences {div:4d}   "
          f"worst r-hat {float(az.rhat(i).to_array().max()):.4f}")
    i.to_netcdf(cache)
    return i


if __name__ == "__main__":
    print(f"PFOA, {na} monkeys, 10 mg/kg IV, {len(mk)} observations\n")
    i1 = fit(one_compartment(), "1compartment")
    i2 = fit(two_compartment(), "2compartment")

    print("\nA. Parameter estimates\n")
    print(az.summary(i1, var_names=["half_life_pop", "sigma"],
                     hdi_prob=0.95).to_string())
    print()
    print(az.summary(i2, var_names=["half_life_terminal", "half_life_alpha",
                                    "Vss", "CL", "sigma"],
                     hdi_prob=0.95).to_string())

    print("\n\nB. Which model predicts better? (LOO)\n")
    comp = az.compare({"1-compartment": i1, "2-compartment": i2}, ic="loo")
    print(comp.to_string())

    winner = comp.index[0]
    diff, dse = comp.elpd_diff.iloc[1], comp.dse.iloc[1]
    print(f"\n   {winner} wins by {diff:.1f} +/- {dse:.1f} elpd")
    print(f"   ratio {diff/max(dse,1e-9):.1f} standard errors "
          f"-- {'decisive' if diff > 4*dse else 'not decisive'}")

    print("""
   Note the 'warning' column: True for both models. ArviZ is telling you
   that some observations have a Pareto k above 0.7, meaning the LOO
   approximation is shaky for those points -- with 43 observations and
   3 animals, dropping a single point really can move the posterior.
   The ranking here is wide enough (5+ standard errors) to survive that,
   but never report a marginal LOO difference with this flag set; rerun
   the flagged points with az.reloo, or use k-fold.

C. What the second compartment bought you

   Look at sigma. In the one-compartment fit it has to absorb the
   systematic curvature; in the two-compartment fit that curvature is
   modelled, so sigma drops and the residuals stop marching. A drop in
   sigma with a better LOO is the signature of a genuinely better
   structural model, as opposed to one that is simply more flexible.

   Look at the two half-lives. The fast (alpha) phase is distribution
   into tissue; the slow (terminal) phase is what actually governs how
   long the chemical stays in the body, and it is the number that should
   be compared across species and across studies. A study that stopped
   sampling during the alpha phase reports the alpha half-life and calls
   it the half-life -- which is one concrete reason published PFAS
   half-lives disagree (lesson 03, trap 1).

D. And now the honest limitation

   The two-compartment model fits. But ask what the peripheral
   compartment IS, and there is no answer. It is a mathematical
   container with a volume and two rate constants, fitted to blood data.
   It cannot tell you:

     * how much PFOA is in the liver versus the kidney
     * what happens if you change the dose route
     * what happens in a pregnant animal, or a child
     * how to extrapolate from monkey to human other than by allometry,
       which the EPA paper showed fails for PFAS clearance
     * why male and female rats differ 44-fold

   Every one of those questions needs compartments that correspond to
   real organs, with real blood flows, real volumes, and elimination
   written as a transporter process rather than a rate constant. That is
   PBPK, and it is the next step.

   What carries over from these seven lessons:
     - mass balance, dC/dt = in - out, is the entire idea; PBPK just has
       one such equation per organ
     - first-order rates, half-life, clearance, AUC, steady state
     - identifiability: PBPK has dozens of parameters and blood data
       that can constrain only a handful, so most are FIXED from
       physiology rather than fitted. Knowing which is which is the
       whole skill.
     - the hierarchical Bayesian machinery, unchanged -- Chiu's human
       model and the EPA's animal models are both exactly this, and
       PBPK versions swap the ODE and keep the statistics

QUESTIONS
  1. Vss from the two-compartment fit should exceed V1. Why must that be
     true, and what does the gap mean physically?
  2. The one-compartment half-life sits between the alpha and terminal
     half-lives. Explain why, in terms of what least squares (or the
     likelihood) is trading off.
  3. LOO compares predictive accuracy, not truth. If the two-compartment
     model had won by less than 2*dse, what would you conclude, and what
     would you do?
  4. The 2-compartment model has 4 population parameters plus 4 spreads
     against the 1-compartment's 2 plus 2, fitted to 43 points from 3
     animals. What stops it from simply overfitting? (Two answers: one
     about LOO, one about priors.)

EXERCISES
  a. Refit both models on PFOS_Male_primate. Does the second
     compartment still win? PFOS distributes differently from PFOA.
  b. Drop every observation after day 28 and refit. Does LOO still pick
     two compartments? This is the "how long must a study run" question,
     and you can answer it quantitatively.
  c. Add a third compartment. At what point does LOO stop rewarding you?
     That boundary is where blood data alone runs out of information --
     and it is precisely why PBPK has to import structure from
     physiology instead of learning it from the data.
""")
