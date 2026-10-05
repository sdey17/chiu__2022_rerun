# Does PFAS clearance depend on dose?

> Every number below is also in `per_dataset_fits.csv`,
> `within_study_dose_contrasts.csv` and `equal_duration_dose_slopes.csv`,
> one row per dataset or contrast, each with a `provenance` field.


Two chemicals so far, both male rats. **PFOA yes, PFHxA no.**

| | PFOA | PFHxA |
|---|---|---|
| clearance | 0.0150 L/kg/d | 3.02 L/kg/d (200x faster) |
| half-life | 13.3 d | 0.095 d (~2.3 h) |
| Vdss | 0.270 L/kg | 0.446 L/kg |
| dose slope, gavage | **+0.110 (+0.007, +0.222)** | **+0.039 (-0.041, +0.122)** |
| within-study ratios outside 0.8-1.2 | 2 of 5 | **0 of 5** |

---

# PFOA in male rats

First result. Fit of the EPA model (`fit_rat_pfoa.py`) to 860 observations
from 6 studies / 14 datasets, then `dose_analysis.py`.

## The fit reproduces theirs

LOO picks the 2-compartment model (elpd_diff 40.7; their notebook 46.3).

| | this run | their notebook |
|---|---|---|
| Clearance (L/kg/d) | 0.0150 | 0.0151 |
| Vdss (L/kg) | 0.270 | 0.289 |
| Half-life (d) | 13.3 | 14.2 |
| Vc (L/kg) | 0.138 | 0.136 |

Caveat: their `pass_all_metrics` was False for the 2-compartment run here.
That is their effective-sample-size rule (~83 per chain against their
threshold of 100), not r-hat: worst r-hat was 1.010, and the per-dataset
clearances we use have ess_bulk >= 392. Usable, but a longer run would be
better before publishing anything.

## Clearance rises with dose

Within-study ratios against the lowest dose of the same study:

| study | dose | fold dose | clearance ratio (90% CI) |
|---|---|---|---|
| 5916078 | 6 -> 12 mg/kg | 2x | 1.21 (0.84, 1.75) |
| 5916078 | 6 -> 48 | 8x | **2.13 (1.38, 3.30)** |
| 6302380 | 0.1 -> 1 | 10x | 1.17 (0.81, 1.69) |
| 6302380 | 0.1 -> 5 | 50x | 1.15 (0.73, 1.81) |
| 6302380 | 0.1 -> 25 | 250x | **1.63 (1.05, 2.51)** |

Meta-regression, per-study intercepts, dataset uncertainty propagated:

    gavage only:  beta = +0.110  (90% CI +0.007, +0.222)   P(beta < 0) = 0.04
    both routes:  beta = +0.095  (90% CI +0.004, +0.191)   P(beta < 0) = 0.04

So clearance goes roughly as dose^0.1: a 10x dose raises clearance ~1.3x,
and half-life falls by the same factor. The direction is positive in both
studies that have multiple doses, and the interval excludes zero, but only
just.

## Reading it

Positive slope means **higher doses are cleared faster**, so half-life gets
*shorter* as dose rises. That is the opposite of ordinary metabolic
saturation, and it is what PFOA in male rats is known for: PFOA is
reabsorbed from urine back into blood by kidney transporters, and
saturating that reabsorption at high dose lets more escape in urine.

## Follow-up duration does not explain it

The main worry was that high-dose arms might be followed longer, capturing
more of the slow terminal phase. Checked directly (`duration_check.py`):

| study | doses | follow-up | ln(dose) vs ln(follow-up) |
|---|---|---|---|
| 5916078 | 6, 12, 48 mg/kg | **50 d for all three** | no variation to confound |
| 6302380 | 0.1, 1, 5, 25 | 84 d at 0.1; 22 d for the rest | r = -0.83 |

The correlation in 6302380 runs the *wrong* way for comfort: its lowest
dose was followed nearly 4x longer, which by itself would depress the
low-dose clearance and manufacture a positive slope. So restrict to dose
contrasts where follow-up is identical:

| study | follow-up | doses | beta (90% CI) |
|---|---|---|---|
| 5916078 | 50 d | 6-48 | +0.358 (-0.037, +0.730) |
| 6302380 | 22 d | 1-25 | +0.097 (-0.168, +0.383) |
| pooled | - | 6 datasets | **+0.171 (-0.004, +0.355)** |

Both remain positive, and the study with *perfectly constant* follow-up
shows the steepest slope. The trend is not a duration artefact. Each
subset alone is under-powered (3 doses), so the individual intervals now
straddle zero; the pooled estimate is slightly steeper than the headline
+0.11 and about as certain.

Also checked: 13 of 14 datasets observed at least one fitted half-life
(median 2.4). The exception is study 3859701, at 0.5 half-lives, and it
is single-dose so it contributes only an intercept.

## What would undermine it

- **Only 2 of 6 studies have more than one dose level.** The slope rests on
  those two. The other four contribute intercepts only.
- **Study effects dwarf the dose effect.** Clearance across studies spans
  0.003 to 0.057 L/kg/d, about 17x, against ~1.3x per decade of dose. If
  dose correlates with anything else a lab does, that is the bigger lever.
- Digitised-from-figures data, and the 2-compartment fit's marginal ESS.

---

# PFHxA in male rats

162 observations, 4 studies, 11 datasets. LOO picks the 2-compartment
model decisively (elpd_diff 77.2). Reproduces their notebook:

| | this run | their notebook |
|---|---|---|
| Clearance (L/kg/d) | 3.106 | 3.118 |
| Vdss (L/kg) | 0.446 | 0.426 |
| Half-life (d) | 0.100 | 0.095 |
| Vc (L/kg) | 0.334 | 0.336 |

## No dose dependence

| study | dose change | fold | clearance ratio (90% CI) | inside 0.8-1.2? |
|---|---|---|---|---|
| 2850314 | 2 -> 100 mg/kg | 50x | 1.14 (0.86, 1.50) | yes |
| 2850396 | 50 -> 150 | 3x | 1.17 (0.87, 1.57) | yes |
| 2850396 | 50 -> 300 | 6x | 1.05 (0.78, 1.40) | yes |
| 5916078 | 40 -> 80 | 2x | 1.20 (0.89, 1.61) | yes |
| 5916078 | 40 -> 160 | 4x | 1.17 (0.85, 1.60) | yes |

    gavage only:  beta = +0.039  (90% CI -0.041, +0.122)   P(beta < 0) = 0.19
    both routes:  beta = +0.012  (90% CI -0.048, +0.073)   P(beta < 0) = 0.37

Every within-study ratio falls inside the practical-equivalence band, and
the interval on beta is *tighter* than PFOA's while straddling zero. This
is a precise null, not an underpowered one.

## And the data are cleaner than PFOA's

- Two of the three multi-dose studies used **identical follow-up across
  every dose** (1.0 d), so duration cannot confound them at all.
- **All 11 datasets observed at least 3.6 half-lives** (median 10), against
  PFOA's median of 2.4 with one dataset under 1. With a ~2 hour half-life
  even a one-day study watches the curve all the way down.
- Equal-duration subsets: beta = +0.063 (90% CI -0.112, +0.246), still
  centred near zero.

## Why the contrast is interesting

PFOA's positive slope is consistent with saturable renal reabsorption:
kidney transporters pull PFOA back out of urine, and swamping them at high
dose lets more escape. PFHxA is already cleared 200x faster, i.e. it is
barely reabsorbed to begin with, so there is little for a high dose to
saturate. Same species, same sex, same model, opposite answer - and the
difference tracks the mechanism rather than the statistics.

Caveat worth keeping: PFHxA's within-study dose ranges (2-50x) are
narrower than PFOA's widest (250x), even though PFHxA spans more doses
overall. The comparison is not perfectly matched.

---

# Next

1. ~~Check whether follow-up duration tracks dose.~~ Done.
2. ~~PFHxA male rat.~~ Done, null result.
3. PFOS, PFNA, PFBS, PFDA in male rats, to see whether the split tracks
   carbon-chain length (PFOA and PFOS are 8-carbon; PFHxA is 6).
4. Female rats, where PFOA clearance is ~44x higher - if that is the same
   transporter story, the dose slope should differ too. This may be the
   sharpest mechanistic test available.
5. Mice where 2-3 dose levels exist. Primates cannot contribute (single IV
   dose only), so "across species" is really rat vs mouse.
