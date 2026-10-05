# Does PFAS clearance depend on dose?

Work in progress, built on the EPA animal-PK model
([USEPA/CPHEA-Animal-PFAS-PK](https://github.com/USEPA/CPHEA-Animal-PFAS-PK),
accompanying [doi:10.1016/j.taap.2025.117336](https://doi.org/10.1016/j.taap.2025.117336)).
Separate from the Chiu human replication in the parent folder.

## The idea

That model's hierarchy has the **dataset** as its lowest level, where a
dataset is one (study, dose, route), and each dataset gets its own
clearance. So a single fit already yields a clearance estimate per dose
level, with uncertainty. If clearance trends with dose, the kinetics are
not linear and half-life depends on how much was given.

## Running it

These scripts import the EPA repository rather than vendoring it:

```bash
git clone https://github.com/USEPA/CPHEA-Animal-PFAS-PK   # anywhere
export EPA_REPO=/path/to/CPHEA-Animal-PFAS-PK
# build their SQLite database once (see their README: auxiliary_notebooks/create_db.ipynb)
python fit_rat_pfoa.py                      # ~45-60 min, both model structures
python dose_analysis.py PFOA_Male_rat_2cmpt.nc
python plot_dose.py     PFOA_Male_rat_2cmpt.nc
```

Two compatibility shims are needed against current libraries, neither
affecting the science:

- their data prep needs `pandas < 2.3` (newer pandas rejects an assignment
  in `pfas_prep.py`)
- `pm.Data(..., mutable=True)` was removed from PyMC; `fit_rat_pfoa.py`
  wraps `pm.Data` to drop the argument
- `PyPKMC.py` line ~1143 hardcodes the posterior-predictive dimension name
  `conc_indiv_dim_2`, which newer PyMC no longer produces. Replace the two
  hardcoded names with `post_pred.conc_indiv.dims[-1]` and
  `post_pred.conc_summary.dims[-1]`, or sampling results are discarded by
  their own post-processing

`fit_rat_pfoa.py` saves each trace to disk immediately after sampling,
before that post-processing runs, so a failure there cannot throw away an
hour of sampling.

## Method notes

**Comparisons are within study.** Dose is confounded with laboratory, so
the regression gives each study its own intercept and only within-study
dose contrasts identify the slope. The plot is small multiples, one panel
per study, for the same reason. The EPA code's own `ROPE_compare` filters
on `hero_id` for this.

**Uncertainty is propagated.** Each dataset's clearance is a posterior,
not a point. The meta-regression treats each log-scale SD as known
measurement error and adds a between-dataset scatter term.

**Reading the slope** of ln(clearance) on ln(dose):

| slope | meaning |
|---|---|
| 0 | linear kinetics; half-life independent of dose |
| < 0 | clearance falls as dose rises (saturation); half-life grows with dose |
| > 0 | clearance rises with dose (e.g. saturable reabsorption) |

## What the data can support

Oral dose levels available per chemical, species and sex (from
`inventory` over their database):

- **Rats** carry this question: PFHxA male 9 dose levels over 3000x,
  PFOA male 7 over 480x, PFOA female 7 over 3200x, PFBS male 7 over 75x.
- **Mice** have 2-3 levels, 10-60x.
- **Primates** cannot contribute: every primate study is a single IV dose.

So a species comparison is really rat vs mouse; the richer axis is across
chemicals within rats.

## Files

```
fit_animal.py       fit both model structures, compare by LOO, save traces
dose_analysis.py    per-dataset clearance, within-study ratios, dose slope
duration_check.py   is the slope a follow-up-duration artefact?
plot_dose.py        clearance vs dose, one panel per study
```

Results, as data rather than prose. Refitting needs `EPA_REPO` and about an
hour of PyMC, so the numbers these scripts printed are kept here:

| file | rows | what it holds |
|---|---|---|
| `per_dataset_fits.csv` | 25 | one row per (chemical, study, dose, route): half-life, follow-up, points, half-lives observed, clearance with 90% CI where available |
| `within_study_dose_contrasts.csv` | 5 | PFHxA clearance ratios against the lowest dose of the same study, with the practical-equivalence verdict |
| `equal_duration_dose_slopes.csv` | 6 | the dose slope beta restricted to equal-follow-up subsets, per study and pooled, for both chemicals |
| `PFOA_Male_rat_loo.csv`, `PFHxA_Male_rat_loo.csv` | 2 each | the 1- vs 2-compartment LOO comparison |

Each row carries a `provenance` field naming the script that produced it.
`RESULTS.md` is the write-up; these files are the numbers behind it.
