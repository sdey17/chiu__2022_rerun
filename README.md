# PFAS half-lives: Chiu et al. 2022 in Python

This repository re-fits the Bayesian toxicokinetic model of Chiu et al. 2022
(*Environ Health Perspect* 130(12):127001) for four PFAS: PFOA, PFOS, PFNA and
PFHxS. The original work used MCSim, a C-based simulation tool driven by
R-like input files ([original repository](https://github.com/wachiuphd/2022-Bayes-PFAS-PK)).
This version uses [PyMC](https://www.pymc.io/).

It reproduces the published half-lives:

| PFAS  | This code, median (95% CI) | Paper, Table 3 |
|-------|----------------------------|----------------|
| PFOA  | 3.16 (2.65–3.77)  | 3.14 (2.69–3.73) |
| PFOS  | 3.34 (2.45–4.45)  | 3.36 (2.52–4.42) |
| PFNA  | 2.28 (1.53–3.19)  | 2.35 (1.65–3.16) |
| PFHxS | 8.52 (5.66–13.01) | 8.30 (5.38–13.5) |

The half-life here is for the population geometric mean (GM), i.e. a
"typical" person. MCMC is random, so your numbers can differ from these in
the second decimal place.

## Quick start

```bash
pip install -r requirements.txt
python parse_chiu_data.py      # optional: see which data are used
python model.py PFNA           # about 1 minute
python model.py all            # all four; PFOA takes about 4 minutes
```

Each run prints the half-life next to the paper's value and saves the full
posterior to `results_<chem>.nc` (open it with `arviz.from_netcdf`).

## Files

```
model.py               the model (one file for all four chemicals)
parse_chiu_data.py     reads Chiu's input files into a table
data/                  Chiu's MCSim input files, unmodified (GPLv3, see LICENSE-chiu-GPLv3)
*.pdf                  the paper and its supplement
```

---

## 1. The model in plain words

Treat the body as one well-mixed bucket. PFAS comes in with drinking water
and leaves at a rate proportional to how much is there:

```
dC/dt = DWI · DWC / Vd  −  k · (C − Cbgd)
```

| symbol | meaning | units |
|---|---|---|
| C    | serum concentration | µg/L |
| DWC  | drinking-water concentration | µg/L |
| DWI  | water intake per kg body weight (fixed, not fitted) | L/kg/day |
| Vd   | volume of distribution | L/kg |
| k    | elimination rate — **what we want** | 1/year |
| Cbgd | background level from food, dust, etc. | µg/L |

Half-life = ln(2) / k. With constant water, the level moves exponentially
from its starting value C0 towards the steady state `Cbgd + DWI·DWC/(k·Vd)`.

**Try it:** how the serum level approaches steady state.

```python
import numpy as np
k, Vd, DWI, DWC, Cbgd, C0 = 0.3, 0.2, 0.0123 * 365.25, 0.05, 0.6, 5.0
Css = Cbgd + DWI * DWC / (k * Vd)
for t in [0, 1, 2, 5, 10, 20]:
    C = Css + (C0 - Css) * np.exp(-k * t)
    print(f"year {t:2d}: {C:5.2f} ug/L   (steady state {Css:.2f})")
```

## 2. The hierarchy: three levels of parameters

Nobody's k is known, and one person's data can't pin it down. The model
therefore assumes each person's value is drawn from a population
distribution and estimates that distribution from everyone at once.

```
Population   M_ln_k, V_ln_k, M_ln_Vd, SD_ln_Vd        one set, shared by everyone
   │
Study        M_ln_Cbgd_sc, M_ln_C_0_sc,               one set PER STUDY
   │         (DWC below MRL)                          (Decatur, Arnsberg, Minnesota, ...)
   │
Person       k, Vd, DWI, Cbgd, C0                     one set PER PERSON
```

Each person's value is written as *population value + person's z-score*:

```python
k = exp(M_ln_k + sqrt(V_ln_k) * z_k)      # z_k ~ Normal(0, 1), one per person
```

This is called a *non-centred* parameterisation, and it makes MCMC sample
much more smoothly.

In MCSim, a `Distrib()` placed inside a `Level { }` creates **one copy for
each child** of that Level. In PyMC you get the same thing by giving the
parameter a `shape`:

```python
M_ln_Cbgd_sc = pm.Normal("M_ln_Cbgd_sc", -0.22, 0.41, shape=n_studies)  # one per study
Cbgd = Cbgd_gm * exp(M_ln_Cbgd_sc[study_of_each_person] + ...)          # pick your study's value
```

## 3. Four kinds of data

| kind | what was measured | where | formula in `model.py` |
|---|---|---|---|
| `Cserum`     | two blood samples, constant water | PFNA, PFHxS Decatur | section 3(a) |
| `Cserum_t`   | two blood samples, water level changing over time | PFOA Decatur and Arnsberg, PFOS Decatur | section 3(b) |
| `Cbgd_Css`   | one blood sample at steady state | Minnesota (PFOA, PFOS) | section 3(c) |
| `M_...`      | community **average** only | Paulsboro, Horsham, Lubeck, Little Hocking | section 4 |

For community averages we need the *mean* over people, not the value for an
average person. For a lognormal variable, `E[X] = exp(mu + sigma²/2)`, which
is larger than `exp(mu)`.

Only records inside a `Level` that has a `Likelihood()` are used for fitting
(the "training" set). The rest are the paper's test set.

---

## 4. Why an earlier Python version disagreed with the paper

An earlier version of this repository (see git history) gave PFOA 4.30,
PFOS 3.10, PFNA 2.89 and PFHxS 6.59 years. Comparing it line by line with
Chiu's input files turned up four differences. All four are fixed in
`model.py`.

| # | difference | effect |
|---|---|---|
| 1 | Only the **last** blood sample of each person was used. The t = 0 sample was dropped. | Major, all four chemicals |
| 2 | **One** background scale (`M_ln_Cbgd_sc`, `M_ln_C_0_sc`) for all studies instead of one per study | Major for PFOA |
| 3 | PFNA priors did not match Chiu's PFNA file | Small |
| 4 | Water-level changes after the blood draw were simulated | Small (1–2%) |

Median half-life (years) when each difference is added back **on its own**
to the correct model:

| PFAS  | correct | + #1 | + #2 | + #3 | + #4 | all four |
|-------|--------:|-----:|-----:|-----:|-----:|---------:|
| PFOA  | 3.16 | 2.94 | 3.36 | –    | 3.18 | **4.30** |
| PFOS  | 3.36 | 3.22 | 3.32 | –    | 3.28 | 3.10 |
| PFNA  | 2.27 | **2.89** | 2.30 | 2.28 | – | 2.74 |
| PFHxS | 8.51 | **6.69** | 8.48 | – | – | 6.62 |

For PFOA, neither #1 nor #2 matters much alone, but together they move the
answer by more than a year. When errors interact like this, fixing one at a
time can make each look harmless. All of them have to be fixed together.

### Why dropping the t = 0 sample matters

Each person's file entry has two samples, for example
`Data(Cserum, 1.9, 1.1)` at t = 0 and t = 5.8 years. Only the *difference*
between them tells you k. Without the first sample, the starting level C0
is known only roughly (its prior allows about ±50%), and a lower start needs
less decay:

```python
import numpy as np
C_start, C_end, T, Cbgd = 1.9, 1.1, 5.802, 0.5    # one PFNA person
for fraction in [1.0, 0.8, 0.67]:
    C0 = C_start * fraction
    k = -np.log((C_end - Cbgd) / (C0 - Cbgd)) / T
    print(f"start = {fraction:.0%} of measured -> half-life {np.log(2)/k:.1f} yr")
# 100% -> 4.7 yr,  80% -> 7.6 yr,  67% -> 15.9 yr
```

In the full fit without the t = 0 samples, PFNA's starting-level scale
drifted to −0.40 (a start about 33% too low) and became correlated with k
(r = +0.49). With them it stays at 0.00 ± 0.10 and is uncorrelated.

### Why one shared background scale matters

In Chiu's fitted chains, the background scale is very different between
studies: Decatur **+0.57**, Arnsberg **−0.69**, Minnesota **−0.77**. A single
shared value can't fit all three. The model then compensates by distorting
k and its spread between people (GSD 1.36 instead of the paper's 1.57).

---

## 5. How to tell if a run worked

`pm.sample` prints warnings if something went wrong. Check two things:

- **r_hat** below about 1.01: the 4 chains agree. `arviz.summary(idata)` shows it.
- **divergences** of 0, or a handful: printed by `model.py`. Many divergences
  mean the sampler could not explore the posterior properly.

Expect a PyMC warning that some r_hat values are above 1.01. In our runs that
comes from nuisance parameters such as the Minnesota measurement error
(r_hat 1.02). The half-life, its spread between people and Vd all had
r_hat = 1.00. To remove the warning, run longer: `fit(chem, draws=2000)`.

```python
import arviz as az
idata = az.from_netcdf("results_PFNA.nc")
print(az.summary(idata, var_names=["halflife", "halflife_GSD", "Vd"]))
```

## 6. Conventions worth knowing

- MCSim writes `LogNormal(GM, GSD)`. In PyMC that is
  `pm.LogNormal(mu=log(GM), sigma=log(GSD))`.
- `LogUniform(1.1, 10)` becomes `Uniform` on `log(GSD)` between `log(1.1)` and `log(10)`.
- The paper reports **95%** intervals, so compare against 95% intervals.
- On some sandboxed machines PyMC's parallel chains hang. If that happens,
  change `cores=4` to `cores=1` in `fit()`.
