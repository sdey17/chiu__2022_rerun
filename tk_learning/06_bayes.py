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
import matplotlib.pyplot as plt
import numpy as np
import pymc as pm
import arviz as az

import plotting as P
from tk import load, half_life, iv_1comp

P.setup()

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


def worst_rhat(idata):
    """Largest r-hat over every parameter, across ArviZ versions.

    az.rhat returns an xarray Dataset in ArviZ 0.x, but the 1.x
    refactor returns a DataTree, which has no .to_array(). Writing
    `az.rhat(idata).to_array().max()` therefore breaks with an
    AttributeError on newer installs. Handle both.
    """
    r = az.rhat(idata)
    if hasattr(r, "to_array"):                     # Dataset, ArviZ 0.x
        return float(r.to_array().max())
    vals = [float(v.max()) for node in r.subtree   # DataTree, ArviZ 1.x
            for v in node.dataset.data_vars.values()]
    return max(vals) if vals else float("nan")


def az_summary(idata, var_names, prob=0.95):
    """az.summary with a `prob` highest-density interval, on ArviZ 0.x or 1.x.

    ArviZ 1.x renamed the argument hdi_prob -> ci_prob, and made the
    interval EQUAL-TAILED by default rather than highest-density, so you
    have to ask for "hdi" back. The column names changed with it:

        0.x:  mean  sd  hdi_2.5%  hdi_97.5%  ...
        1.x:  mean  sd  hdi95_lb  hdi95_ub   ...

    Same numbers, different headings. Do not read a renamed column as a
    changed result.
    """
    try:
        return az.summary(idata, var_names=var_names, hdi_prob=prob)
    except TypeError:                                        # ArviZ >= 1.0
        return az.summary(idata, var_names=var_names,
                          ci_prob=prob, ci_kind="hdi")


def compare_loo(models):
    """az.compare on LOO, on ArviZ 0.x or 1.x.

    ArviZ 1.x dropped WAIC, so LOO is the only information criterion and
    the `ic=` argument is gone. Two other things moved:

      * the ELPD column is called `elpd`, not `elpd_loo`;
      * `elpd_diff` is now elpd_model - elpd_reference, so it is
        NEGATIVE for the losing models. In 0.x it was positive. Take
        abs() before comparing it with dse, or a decisive result will
        silently read as "not decisive".

    round_to="none" keeps raw numbers so the arithmetic below is exact.
    """
    try:
        return az.compare(models, ic="loo")
    except TypeError:                                        # ArviZ >= 1.0
        return az.compare(models, round_to="none")


def run(m, name):
    """Sample, and cache to disk so re-running is instant."""
    import os
    cache = f"trace_{name}.nc"
    if os.path.exists(cache):
        print(f"\n--- {name} (loaded from {cache}) ---")
        return az.from_netcdf(cache)
    with m:
        idata = pm.sample(1500, tune=1500, chains=4, random_seed=SEED,
                          target_accept=0.95, progressbar=False,
                          idata_kwargs={"log_likelihood": True})
    print(f"\n--- {name} ---")
    div = int(idata["sample_stats"]["diverging"].sum())
    rhat = worst_rhat(idata)
    print(f"divergences {div}   worst r-hat {rhat:.4f}"
          f"   {'OK' if div == 0 and rhat < 1.01 else 'CHECK THIS'}")
    idata.to_netcdf(cache)
    return idata


if __name__ == "__main__":
    ip = run(pooled(), "pooled")
    print(az_summary(ip, ["Vd", "k", "half_life", "CL", "sigma"]).to_string())
    print("""
   Read the table: 'mean' is the posterior mean, hdi_2.5%/97.5%
   (hdi95_lb/hdi95_ub on ArviZ 1.x -- same numbers) the
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
    print(az_summary(ih, ["half_life_pop", "half_life_i",
                          "sd_ln_k", "sigma"]).to_string())
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


    # ------------------------------------------------------------------
    # C. Figures
    # ------------------------------------------------------------------
    print("C. Figures\n")

    # C1 -- posterior densities. A Bayesian answer is a SHAPE, not a
    # number with an error bar bolted on.
    fig, (a, b) = plt.subplots(1, 2, figsize=(8.6, 3.4), constrained_layout=True)
    hl_p = ip.posterior["half_life"].values.ravel()
    hl_h = ih.posterior["half_life_pop"].values.ravel()
    for ax, (vals, ttl, col) in zip(
            (a, b), [(hl_p, "pooled: one k for all three monkeys", P.BLUE),
                     (hl_h, "hierarchical: the POPULATION half-life", P.ORANGE)]):
        ax.hist(vals, bins=70, color=col, alpha=0.75, density=True)
        lo_, hi_ = np.percentile(vals, [2.5, 97.5])
        ax.axvline(np.median(vals), color=P.INK, lw=1.3)
        ax.axvspan(lo_, hi_, color=col, alpha=0.12)
        ax.set(xlabel="half-life (days)", ylabel="posterior density", xlim=(0, 40))
        ax.set_title(ttl)
    P.save(fig, "06_posteriors.png",
           "Shaded = 95% credible interval, line = median. The "
           "hierarchical population half-life is far more uncertain,\n"
           "and rightly so: three monkeys say little about monkeys in "
           "general. The pooled model's confidence was an artefact.")

    # C2 -- shrinkage. The single most useful picture in hierarchical
    # modelling: each animal's own estimate, pulled toward the group.
    fig, ax = plt.subplots(figsize=(6.4, 3.4), constrained_layout=True)
    for j, aid in enumerate(animals):
        d = mk[mk.animal_id == aid]
        kk, C0 = np.polyfit(d.time_d, np.log(d.conc_mgL), 1)[:2]
        alone = np.log(2) / -kk                       # that animal, fitted alone
        post = ih.posterior["half_life_i"].values[:, :, j].ravel()
        ax.plot([alone, np.median(post)], [j, j], "-", color=P.GREY, lw=1.2)
        ax.plot(alone, j, "o", color=P.BLUE, ms=7, mfc="none", mew=1.6,
                label="fitted alone" if j == 0 else None)
        ax.plot(np.median(post), j, "o", color=P.ORANGE, ms=7,
                label="hierarchical" if j == 0 else None)
        ax.hlines(j, *np.percentile(post, [2.5, 97.5]), color=P.ORANGE, lw=1.4,
                  alpha=0.5)
    ax.axvline(np.median(hl_h), color=P.INK, ls=":", lw=1.2,
               label="population median")
    ax.set_yticks(range(len(animals)), [f"monkey {a}" for a in animals])
    ax.set(xlabel="half-life (days)", ylim=(-0.6, len(animals) - 0.4))
    ax.set_title("partial pooling: each animal pulled toward the group")
    ax.legend(loc="center left", bbox_to_anchor=(1.01, 0.5))
    P.save(fig, "06_shrinkage.png",
           "Blue = that animal fitted on its own; orange = the same "
           "animal inside the hierarchy, with its 95% interval.\n"
           "The gaps are small here because each monkey has ~14 of its "
           "own points, so its own data dominate. With 3 points each "
           "the orange dots would sit much closer to the dotted line. "
           "That is the whole mechanism:\nshrinkage scales with how "
           "little that unit's own data say.")

    # C3 -- two DIFFERENT bands that beginners routinely conflate.
    fig, ax = plt.subplots(figsize=(6.6, 4.2), constrained_layout=True)
    grid = np.linspace(0.02, 95, 300)
    Vd_p = ip.posterior["Vd"].values.ravel()
    k_p = ip.posterior["k"].values.ravel()
    sig_p = ip.posterior["sigma"].values.ravel()
    curves = np.array([iv_1comp(grid, DOSE, v, kk)
                       for v, kk in zip(Vd_p[:1500], k_p[:1500])])

    # (i) uncertainty in the MEAN curve: only the parameters vary.
    lo_m, hi_m = np.percentile(curves, [2.5, 97.5], axis=0)
    ax.fill_between(grid, lo_m, hi_m, color=P.BLUE, alpha=0.35,
                    label="95% for the mean curve (parameters only)")

    # (ii) where a NEW observation should fall: parameters AND sigma.
    rng = np.random.default_rng(0)
    pred = curves * np.exp(rng.normal(0, sig_p[:1500][:, None]))
    lo_p, hi_p = np.percentile(pred, [2.5, 97.5], axis=0)
    ax.fill_between(grid, lo_p, hi_p, color=P.BLUE, alpha=0.12,
                    label="95% for a new observation (+ sigma)")

    for aid, col in zip(animals, P.CYCLE):
        d = mk[mk.animal_id == aid]
        P.data_points(ax, d.time_d, d.conc_mgL, label=f"monkey {aid}", color=col)
    ax.set(yscale="log", ylim=(0.005, 500), xlabel="days since dose",
           ylabel="serum conc (mg/L)")
    ax.set_title("two bands people confuse: mean curve vs new observation")
    ax.legend(loc="upper right", fontsize=7.5)
    P.save(fig, "06_posterior_predictive.png",
           "The dark band is narrow because 43 points pin the average "
           "curve well. It is NOT where data should fall, and almost\n"
           "every real point lies outside it -- that is correct, not a "
           "failure. The pale band, which includes sigma = 0.85, is the "
           "one to check a model against.\nIts width is the pooled "
           "model's admission that it cannot tell these three animals "
           "apart.")

    comp = compare_loo({"pooled": ip, "hierarchical": ih})
    print(comp.to_string())
    print("""
   LOO (leave-one-out cross-validation) estimates out-of-sample
   predictive accuracy. Higher elpd_loo is better (the column is just
   `elpd` on ArviZ 1.x); the ranking is what matters, and elpd_diff
   should be compared to its own standard error (dse) -- a difference
   smaller than about 2*dse is not decisive. Its SIGN is a version
   trap: positive for the losers in ArviZ 0.x, negative in 1.x.

   This is the same tool the EPA pipeline uses to choose between one and
   two compartments, and the same one lesson 07 will use.

QUESTIONS
  0. In 06_posterior_predictive.png, which band would you use to answer
     "is this model adequate?", and which to answer "how well do we know
     the typical monkey's curve?" Getting these two confused is the most
     common error in reporting a Bayesian fit.
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
