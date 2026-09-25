# PFAS toxicokinetics: a from-scratch Python replication

> **Update:** the gaps described below (including the "open" PFOA gap) are
> explained in [`ANALYSIS.md`](ANALYSIS.md). The `model_*.py` scripts drop
> the t = 0 serum observations and share one background/initial-concentration
> scale across all studies, where Chiu's model uses one per study. The PFNA
> priors are also wrong. `model_corrected.py` fixes these and reproduces the
> published half-lives for all four PFAS (PFOA 3.16, PFOS 3.36, PFNA 2.27,
> PFHxS 8.51 yr).

This folder replicates the population human elimination half-life
estimates from Chiu et al. 2022, a Bayesian toxicokinetic analysis of
four PFAS ("forever chemicals") — PFOA, PFOS, PFNA, and PFHxS — using
PyMC instead of Chiu's original tool (MCSim, a program driven by R-like
configuration scripts). Everything here was built and run directly
against Chiu's own published input data files; nothing is simulated or
invented.

If you are new to Bayesian modeling, MCMC, or toxicokinetics, **start
with `model_pfna.py`** — it has the longest, most complete explanation
of every concept used, and the other three scripts point back to it
instead of repeating themselves.

## Quick start

```bash
pip install -r requirements.txt
python model_pfna.py       # ~1-3 min, simplest model, start here
python model_pfhxs.py      # ~2-3 min
python model_pfos.py       # ~3-5 min
python model_pfoa.py       # ~8-12 min, largest/slowest model
```

or run all four back-to-back with `python run_all.py`.

Each script is fully self-contained once you've `pip install`ed the
requirements — it reads its chemical's data straight out of the
`data/` folder, builds the model, samples the posterior, prints a
results table to your terminal, and saves a `.nc` file (the full
posterior, reloadable with `arviz.from_netcdf`) and a `.png` diagnostic
plot.

## What's in this folder

```
README.md                  <- you are here
requirements.txt
parse_chiu_data.py          <- reads Chiu's raw data files into a table
model_pfna.py                <- START HERE. Simplest model.
model_pfhxs.py               <- same structure as PFNA, different numbers
model_pfos.py                <- adds pytensor.scan for time-varying exposure
model_pfoa.py                <- largest model, same ideas at bigger scale
run_all.py                   <- convenience: runs all four in sequence
data/
  PFOA_1cpt_v8.MCMC_TrainTest.in.R
  PFOS_1cpt_v8.PopMCMC_MeanIndivTrainTest.in.R
  PFNA_1cpt_v8.PopMCMC_MeanIndivTrainTest.in.R
  PFHxS_1cpt_v8.PopMCMC_MeanIndivTrainTest.in.r
```

The four files in `data/` are copied, unmodified, from Chiu et al.'s own
public GitHub repository (GPLv3-licensed). They are MCSim's own
configuration-script format (not real R code, despite the extension) —
`parse_chiu_data.py`'s module docstring explains the format in detail if
you're curious, but you don't need to read or understand these files
directly; the model scripts do that for you.

## The concept, in one paragraph

PFAS chemicals accumulate in the body and leave slowly. If you know how
much someone drinks and how contaminated their water is, and you measure
their blood level, you can work out how fast their body eliminates the
chemical — that elimination rate, converted to a half-life
(`ln(2) / rate`), is the number regulators use to set health guidance.
No single person's data is precise enough to pin this down alone, so
Chiu pooled many people from several contaminated communities into one
**hierarchical Bayesian model**: everyone's own personal elimination
rate is treated as a random draw from one shared population
distribution, and the data from ALL the people at once tells us what
that shared distribution must have been. This is the same idea as a
mixed-effects model in classical statistics — just solved by full
Bayesian sampling (MCMC) instead of maximum likelihood.

## Results you should expect

| Chemical | Our replication (median, 90% CI) | Chiu's actual published value (median, 95% CI)* | How close |
|---|---|---|---|
| PFNA  | 2.89 yr [1.92, 4.87] | 2.31 yr [1.62, 3.15] | Good — overlapping intervals |
| PFOS  | 3.10 yr [2.28, 4.37] | 3.41 yr [2.63, 4.40] | Best match of the four |
| PFHxS | 6.59 yr [4.58, 10.31] | 8.47 yr [5.69, 13.46] | Reasonable — overlapping, low side |
| PFOA  | 4.30 yr [3.52, 5.24] | 3.15 yr [2.62, 3.74] | Weakest — genuine open gap, see below |

\* "Chiu's actual published value" was computed directly from his own
raw saved MCMC chains (the `.out` files in his repository), not copied
from the narrative text in his write-up. That text turned out to be
stale, copy-pasted boilerplate identical across three different
chemicals' reports (all three claimed "3.06 [2.16-4.37]" verbatim) — a
real error we caught by cross-checking against the primary output
instead of trusting the prose summary. **Lesson: when validating a
model against a published paper, always go to the paper's raw output
data if it's available, not just its narrative sentences.**

Your own run will land close to these numbers but not identically —
MCMC sampling uses randomness, and even with a fixed random seed,
results can vary slightly by machine/library version. Small differences
(a few percent) are normal; large differences may mean something is
misconfigured. If you're not sure which is which, the `r_hat` and
"divergences" diagnostics each script prints are your first check (see
"How to tell if it worked" below).

## Should I run Chiu's original R/MCSim script too, to check agreement?

**No, you don't need to.** Every comparison number above already comes
from Chiu's own raw saved MCMC output, which is stronger ground truth
than re-running his script yourself would give you — it's his actual
published posterior, not a fresh re-derivation of it. The only reason to
learn MCSim/R at this point is if your day-to-day work will actually run
on that tool going forward, in which case it's worth knowing as a
separate skill — but it isn't needed to trust these results.

## Key concepts worth having solid

**Bayesian inference, in one sentence.** You start with a *prior* belief
about each unknown quantity (a probability distribution reflecting
what's plausible before seeing data), combine it with a *likelihood*
(how probable the observed data would be under different parameter
values), and get out a *posterior* — an updated distribution reflecting
what you now believe, given both the prior and the data.

**MCMC / NUTS.** We can't write down the posterior distribution in
closed form for a model this complex, so we *sample* from it instead.
NUTS (the No-U-Turn Sampler, what PyMC uses by default) explores the
posterior by simulating physics — treating the negative log-posterior
as a landscape and "rolling a ball" across it using the gradient to know
which way is downhill — and is dramatically more efficient at this than
older methods like plain Metropolis-Hastings, especially in high
dimensions (our smallest model here has ~100 dimensions; PFOA has 840).

**Divergences.** A "divergence" is a specific NUTS warning: the
simulated trajectory's energy blew up locally, usually because the
posterior is "stiff" or funnel-shaped in some direction. A handful of
divergences isn't automatically fatal — you can check whether raising
`target_accept` (which makes NUTS take smaller, more careful steps)
makes them go away; if it does, it was mild stiffness, not a real
structural problem with the model.

**r_hat and convergence.** Each script runs 4 independent MCMC chains,
started from different random points. If they've all converged to the
same posterior, their between-chain and within-chain variance should
roughly agree — that's what `r_hat` measures. Values very close to 1.00
(the usual rule of thumb is `< 1.01`) mean the chains agree with each
other, which is strong (though not 100% ironclad) evidence of
convergence.

**Hierarchical / non-centered parameterization.** Rather than sampling
each person's own elimination rate directly, we sample a
standard-normal "z-score" per person (`z_k[i] ~ Normal(0,1)`) and build
their actual rate as `k[i] = exp(M_ln_k + SD_ln_k * z_k[i])`. This
"non-centered" trick is standard practice for hierarchical Bayesian
models — it makes the geometry NUTS has to explore much friendlier, and
is usually the first thing to try if a hierarchical model is sampling
badly.

**Log-space everywhere.** Concentrations, rates, and volumes are all
positive and tend to vary multiplicatively rather than additively, so
every quantity here is parameterized as the log of itself. When you see
`M_ln_k`, read it as "the log of the population's typical elimination
rate," not the rate itself.

**Population-summary rows and Jensen's inequality.** A few data points
in this dataset are not one person's blood level, but the *average*
blood level across an entire exposed population. You can't just plug
population-average parameters into the single-person formula and call
it the population average — because `E[exp(X)] != exp(E[X])` for a
random variable X (Jensen's inequality). Each model script includes a
closed-form correction for this (`E[Y] = exp(mu + sigma^2/2)` for a
lognormal Y), matching Chiu's own formula exactly. **This mattered a
lot in practice** — an earlier version of this replication that
accidentally skipped these rows for PFNA came out to 3.60 years instead
of the 2.89 years shown above; simply adding those 2 extra data points
closed most of the gap to the real 2.31-year answer.

## How to tell if it worked

Each script prints, near the bottom:

```
Worst r_hat: 1.0040 (want < 1.01) | divergences: 0
```

- `r_hat < 1.01` and `divergences: 0` (or a small handful, especially
  if you already used a high `target_accept`) → healthy run, trust the
  result.
- `r_hat` well above 1.01, or dozens+ of divergences → something is off;
  the posterior summary table's `ess_bulk`/`ess_tail` columns (effective
  sample size) are the next thing to check — very low values mean the
  chains aren't exploring efficiently.

## What's still open: PFOA's gap

PFOA is the one chemical where our replication doesn't close the gap to
Chiu's published number (4.30 vs. his 3.15 years). This was investigated
at length. What we found and ruled out:

1. **Not a missing-data issue** — adding PFOA's 4 population-summary
   rows (the same fix that worked well for PFNA) barely moved the
   estimate (4.23 → 4.30 years).
2. **Not a fixed-vs-free exposure-rate parameter issue** — checked
   Chiu's source directly; he fixes the same daily-water-intake
   parameters we do.
3. **Not a site-grouping/hierarchy issue** — checked Chiu's source
   directly; Decatur and Arnsberg (PFOA's two individual-level study
   sites) draw from the exact same flat population distribution, with
   no site-level hierarchy in his model either.
4. **Not an MCMC convergence problem on our side** — forcibly
   re-initializing our chains at Chiu's own real fitted parameter
   values, they migrated back to our answer rather than staying there,
   meaning our result is a genuine higher-posterior-density region under
   our model and data, not a sampler that got stuck in a worse local
   answer.
5. **Not a measurement-noise-budget difference** — Chiu's real fitted
   noise parameters (GSDs) are close to or tighter than ours, not
   looser, so "he just tolerates messier data" doesn't explain it.

What the gap actually traces to: our fit ends up with substantially LESS
individual-to-individual variability in elimination rate (the
`V_ln_k` parameter) than Chiu's own real posterior shows — our
population's range of per-person half-lives is much narrower than his.
We were not able to identify WHY our model and his diverge on this one
specific quantity, despite both starting from what appears to be the
same formula and the same data as parsed from his own input file. This
is left as a genuinely open question rather than papered over — further
progress would likely require either instrumenting MCSim itself to
compare its internal per-person calculations directly, or a much deeper
line-by-line audit of the ~6300-line PFOA input file.

## Gotchas if you extend this yourself

- **Trust raw MCMC output over narrative report text.** See "Results you
  should expect" above.
- **MCSim's `LogNormal`/`Distrib(..., LogNormal, p1, p2)` convention is
  (median, GSD), not (mean-of-log, sd-of-log).** Converting to PyMC:
  `sigma = log(GSD)`, and the `mu` you pass to `pm.LogNormal` is the log
  of the median directly.
- **`cores=1` is required** in a sandboxed/containerized environment —
  PyMC's multiprocessing can hang there. On your own machine, you can
  likely set `cores=4` to run the 4 chains in parallel and go faster.
- **The `k`-`Vd` identifiability ridge is real, not a bug.** For anyone
  with constant lifetime exposure, only the *product* `k * Vd` is
  constrained by their steady-state blood level — so the model's
  posterior naturally shows a negative correlation between the fitted
  `M_ln_k` and `M_ln_Vd` (around -0.55 in both our replication and in
  Chiu's own real posterior). This is an inherent feature of what the
  data can and can't tell you, not something to try to "fix."
