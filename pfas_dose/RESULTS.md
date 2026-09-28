# PFOA in male rats: does clearance depend on dose?

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

## Next

1. ~~Check whether follow-up duration tracks dose.~~ Done, see above.
2. PFHxA male rat: 9 dose levels over 3000x, the strongest available test.
3. Then PFOS, PFNA, PFBS, PFDA in rats; compare slopes across chain length.
4. Mice where 2-3 dose levels exist. Primates cannot contribute (single IV
   dose only), so "across species" is really rat vs mouse.
