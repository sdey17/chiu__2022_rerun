# Does dose explain why PFAS half-lives are longer in humans?

**Hypothesis.** Humans are exposed to far lower PFAS doses than laboratory
animals, and low dose is why human half-lives are years while rodent
half-lives are days. The species difference is really a dose difference.

**Verdict: not supported.** Dose does have a real effect in the expected
direction, but it is roughly an order of magnitude too small. Species
differences persist at matched internal exposure.

```bash
export EPA_REPO=/path/to/CPHEA-Animal-PFAS-PK   # their DB must be built
python harvest_pk.py        # fitted half-lives, 42 animal + 7 human rows
python collect_exposure.py  # exposure actually measured, per species
python test_hypothesis.py   # the three tests below
python plot_species.py
```

## Why the obvious comparison cannot work

Species and dose are almost perfectly confounded: every human is exposed
low, every rodent is dosed high. "Because it is a human" and "because the
dose is low" predict exactly the same observation, so comparing humans
against rats cannot distinguish them.

Three things break the confound.

Also note the two literatures do not share a dose unit - animals get a
single bolus in mg/kg, humans a daily intake in mg/kg/day. The comparable
quantity, and the one a saturable transporter actually responds to, is
the **serum concentration measured**, so that is the exposure axis used
throughout.

## Test 1: the correlation reverses when humans are removed

| chemical | corr(ln serum, ln half-life), all species | animals only |
|---|---|---|
| PFOA | **-0.64** | **+0.48** |
| PFOS | **-0.85** | **+0.91** |
| PFNA | **-0.46** | **+0.83** |
| PFHxS | **-0.66** | **+0.65** |

Across all species the correlation is negative, exactly as the hypothesis
predicts. But it is produced entirely by the single human point. Among
animals alone - where serum concentrations still span 10-100x - the
correlation flips **positive** in all four chemicals. There is no dose
gradient underneath; there is one outlying species.

## Test 2: the within-species slope is far too small

We measured the dose response inside one species (male rats, PFOA):
clearance goes as dose^0.11 (90% CI +0.007 to +0.222; see `../pfas_dose`).
Applying that slope to the human/rat exposure gap:

    rat serum is 187x the human level
    dose alone predicts a human half-life  1.8x the rat's
    observed                                81x
    -> dose explains about 13% of the gap on a log scale

And 13% is an overestimate, because it extrapolates a slope measured over
250x across a 187x gap using a power law that keeps accelerating forever.
The mechanism it stands for - saturable renal reabsorption - does the
opposite: saturation flattens out at low concentration. At human
exposures the transporters are nowhere near saturated, so lowering the
dose further should change clearance hardly at all. PFHxA, where we
measured essentially no dose slope (+0.039), makes the same point.

## Test 3: species differ at matched exposure

Pairs of species that reached serum concentrations within 2x of each
other, same chemical (full list in `matched_exposure_pairs.csv`):

| chemical | pair | serum fold | half-life fold |
|---|---|---|---|
| PFOA | rat F vs mouse M | 1.8x | **37x** |
| PFHxS | rat F vs mouse M | 1.3x | **16x** |
| PFBS | rat F vs primate M | 1.1x | **14x** |
| PFHxS | rat M vs primate M | 1.3x | **6.0x** |
| PFNA | rat M vs mouse M | 1.8x | **4.2x** |
| PFOS | mouse F vs rat M | 1.0x | **1.7x** |

Median across all 24 matched pairs: **2.6x**. If dose were the whole
story these would all be about 1.0x.

## What is actually going on

Clearance differs between species because kidney transporters differ -
in abundance and in binding affinity - and those differences do not scale
with body size. That is the EPA paper's own headline conclusion: volume
of distribution scales with body weight as expected, clearance does not.
The 44x male/female rat difference in PFOA clearance is the same story
within one species, and no dose difference is involved there at all.

## A data error found along the way

`auxiliary/Chiu_human.csv` in the EPA repository gives PFHxS a human
half-life of 2.35 y. That is PFNA's value; Chiu's Table 3 reports 8.30 y.
It is also internally inconsistent with the clearance and Vd in the same
row (ln2/2.35 x 0.29 = 0.086, but the row reports 0.025; with 8.30 it
gives 0.024). `test_hypothesis.py` uses the published values.

## Files

```
harvest_pk.py       fitted PK values, recovered from their notebook outputs
collect_exposure.py serum concentrations and doses actually used, per species
test_hypothesis.py  the three tests above
plot_species.py     half-life vs measured serum concentration, per chemical
animal_pk.csv, species_exposure.csv, matched_exposure_pairs.csv
```

`harvest_pk.py` exists because the repository ships `traces/` empty, so
the fitted values are not directly available - but their results notebook
printed one dataframe row per PFAS/species/sex as it ran, and those
outputs are saved in the .ipynb. That recovers 42 of 48 animal
combinations without refitting (the missing 6 had no data). Spot-checked
against our own refits: PFOA male rat 14.20 d, PFHxA male rat 0.095 d,
PFOA male primate 11.45 d, all matching.
