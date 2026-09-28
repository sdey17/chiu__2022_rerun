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

## What would undermine it

- **Only 2 of 6 studies have more than one dose level.** The slope rests on
  those two. The other four contribute intercepts only.
- **Study effects dwarf the dose effect.** Clearance across studies spans
  0.003 to 0.057 L/kg/d, about 17x, against ~1.3x per decade of dose. If
  dose correlates with anything else a lab does, that is the bigger lever.
- **Follow-up duration is not controlled for.** A study that stops earlier
  relative to the half-life may miss the terminal phase and understate
  clearance. Low-dose arms are the more likely to be cut short.
- Digitised-from-figures data, and the 2-compartment fit's marginal ESS.

## Next

1. Check whether follow-up duration tracks dose within these studies.
2. PFHxA male rat: 9 dose levels over 3000x, the strongest available test.
3. Then PFOS, PFNA, PFBS, PFDA in rats; compare slopes across chain length.
4. Mice where 2-3 dose levels exist. Primates cannot contribute (single IV
   dose only), so "across species" is really rat vs mouse.
