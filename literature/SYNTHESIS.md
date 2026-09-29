# PFAS half-lives: what 20 sources actually support

Synthesis across the full collection: two modelling papers re-run from
source (Chiu 2022 human, EPA 2025 animal), 13 human half-life studies,
one systematic review with meta-analysis, two expert-review documents,
two mechanism papers, and one excretion-route study. Full texts in
`fulltext/`, extraction in `studies.csv`, appraisal framework in
`APPRAISAL.md`.

---

## 1. A correction to an earlier claim in this project

In an earlier round I reported that Li et al. 2022 confirmed the dose
hypothesis at the individual level, quoting its text:

> "positive associations between higher initial PFAS levels and shorter
> half-lives ... especially in PFHxS and PFHpS"

**Its own supplementary Table S4 shows the opposite.** Figure 1's caption
defines the groups as "low-medium-high initial total PFAS levels", so
tertile 1 is the LOWEST initial level:

| PFAS | rate, low tertile | rate, high tertile | HL low | HL high | p |
|---|---|---|---|---|---|
| PFOA | -0.30 | -0.27 | 2.29 y | 2.58 y | 0.25 |
| PFHxS | -0.18 | -0.14 | 3.88 y | **4.83 y** | **0.02** |
| PFHpS | -0.18 | -0.14 | 3.94 y | **4.94 y** | **0.02** |
| L-PFOS | -0.28 | -0.25 | 2.49 y | 2.77 y | 0.13 |

Two columns say it independently: the low-exposure tertile declines more
steeply (larger |rate|) and has the shorter half-life. Higher initial
level goes with **slower** elimination - the opposite sign to saturable
reabsorption, and significant for the two chemicals the text singles out.

This is the same failure mode this project hit on day one, when the
original replication's README quoted stale narrative text instead of the
underlying MCMC output. **Read the table, not the sentence.**

---

## 2. The central controversy is an artefact of one assumption

Published human PFOA half-lives span 17-fold, 0.5 to 8.5 years. Reading
the primary methods resolves most of it.

Zhang 2013, the study the expert collaborations lean on for the short
end, estimates half-life by mass balance:

    T-half = 0.693 * V / CL_total
    CL_total := CL_renal            (urine only, + menstrual for young females)
    V        := ASSUMED 170 mL/kg   (PFOA, from Thompson et al.)

Half-life scales linearly with V, and published V for PFOA spans nearly
sixfold:

| Vd source | Vd (mL/kg) | implied PFOA half-life |
|---|---|---|
| Andersson 2025 (measured) | 74 | 0.57 y |
| Zhang's assumption | 170 | 1.30 y |
| Chiu 2022 (fitted) | 430 | **3.29 y** |

Substituting Chiu's fitted Vd into Zhang's own clearance data gives
3.29 y against Chiu's independent serum-decay estimate of 3.14 y. **The
two studies agree to within 5% once they share a Vd.** The famous
disagreement is a disagreement about an assumed constant.

Zhang's second assumption runs the other way. It equates total with
renal clearance, and Andersson 2025 measured PFOA at roughly 1.7:1
urinary, so true clearance is higher. Correcting both:

| | PFOA half-life |
|---|---|
| Zhang as published | 1.30 y |
| + Chiu's fitted Vd | 3.29 y |
| + non-renal elimination | **1.93 y** |
| *Rosato 2024 pooled, general populations* | *2.35 y* |

Zhang's paper states its estimates "should be considered as **upper
limit** estimates". Campbell 2022 adopted 1.3 y as a central tendency;
the authors offered it as a bound.

### The rule that follows

**Serum-decay designs never need Vd** - they read the rate off the slope
of log concentration against time. **Mass-balance designs need a Vd and
a complete excretion accounting**, each uncertain by 2-6x, multiplying
directly into the answer. That is a structural criterion for trust, not
a judgement about any author.

---

## 3. The excretion-route assumption is false, not merely unverified

Andersson 2025 measured matched serum, urine and faeces in 147 Ronneby
subjects:

| | urinary | faecal | dominant route |
|---|---|---|---|
| L-PFOS | 91 ng/day | **364 ng/day** | faeces, 4:1 |
| PFOA | **26 ng/day** | 15 ng/day | urine, ~1.7:1 |

Their framing: "most pharmacokinetic models assume that the urinary
route dominates". For PFOS that is wrong fourfold. Any renal-clearance
half-life therefore counts part of elimination, underestimates clearance
and overestimates half-life - which retrospectively justifies Rosato's
exclusion of that whole method class, and lands squarely on Zhang.

Li 2022 adds a mechanism for the faecal route: higher calprotectin (a
marker of intestinal inflammation) went with shorter half-lives, read as
inflammation reducing intestinal reabsorption.

---

## 4. Does exposure level change elimination? Five levels of evidence

This is the project's original question. The evidence splits cleanly by
what is being compared.

| level of comparison | source | direction | notes |
|---|---|---|---|
| **within a person over time** | Li 2022, Table 5 | **supports** | early samples clear faster than late; concentration falls over follow-up |
| **within a species across doses** | our rat fits | **supports** | PFOA +0.11 (90% CI +0.007, +0.222); PFHxA null |
| between people, one cohort | Li 2022, Table S4 | **contradicts** | higher initial -> longer half-life; PFHxS, PFHpS p=0.02 |
| between human cohorts | `human_dose_test.py` | mixed | PFHxS +0.27, PFOA +0.09, PFOS -0.12 |
| between water districts | Seals 2011 | supports, implausibly | +1.55, above the mechanistic ceiling of 1 |

### The pattern is not noise - it is the level of comparison

**Within-unit comparisons support concentration dependence; between-unit
comparisons do not.** That is what you expect when a between-unit
confounder is present, and Li 2022 names it: age has a very strong
effect on half-life (preteens 45-60% shorter than over-50s). Age also
drives accumulated body burden, so within any cohort, higher initial
level partly means *older*, and older means slower elimination. The
between-person association is the sum of a positive saturation effect
and a larger negative age effect.

The within-person contrast is immune to this: each person is their own
control. So is our within-study rat dose contrast. Both are positive.

Seals 2011's district comparison is between-unit and gives +1.55, which
exceeds what the mechanism allows. For saturable reabsorption,
CL(C) = CLmax * C/(Km + C), so d ln CL/d ln C = Km/(Km+C) <= 1. A slope
above 1 cannot come from saturation, so part of that effect is bias -
the paper flags its own truncation at 15 ng/mL, which removed
proportionally more low-exposure subjects.

### Verdict

Concentration-dependent elimination is **real but small**: of order 0.1
on a log-log slope where the mechanistic ceiling is 1. It is visible in
the two clean within-unit designs and drowned by age in between-person
ones.

---

## 5. It does not explain the species difference

The original hypothesis: humans have long half-lives because they are
exposed to less.

- Rat serum runs ~187x human levels for PFOA.
- A slope of 0.1 predicts a half-life ratio of 187^0.1 = **1.6x**.
- Observed human/rat ratio: **81x**.

Dose accounts for roughly 13% of the gap on a log scale, and that is
generous, because saturation *flattens* at low concentration rather than
continuing to accelerate. At human exposures the transporters are
nowhere near saturated.

Two independent lines close the case:

1. **Matched exposure.** Where two species reach serum concentrations
   within 2x of each other, half-lives still differ by a median of 2.6x
   and up to 37x (`../species_dose/matched_exposure_pairs.csv`).
2. **Correlation reversal.** Across all species, log serum against log
   half-life correlates -0.46 to -0.85, as the hypothesis predicts. Drop
   the single human point and it flips **positive** (+0.48 to +0.91) in
   all four chemicals. There is no dose gradient underneath; there is one
   outlying species.

The real driver is transporter biology that does not scale with body
size - the EPA paper's own conclusion, and the same reason female rats
clear PFOA 44x faster than males with no dose difference at all.

---

## 6. Mechanism, and an unresolved tension

Fischer 2024 measured PFAS binding to serum proteins: a switch at seven
perfluorinated carbons, with npfc < 7 binding mostly albumin and
npfc >= 7 preferring globulins. Unbound fraction varies up to 2.5x
between individuals in NHANES - a source of interindividual variability
no compartmental model represents.

Fischer 2025's PBTK sensitivity analysis: elimination of **short-chain**
PFAA (npfc <= 6) is most sensitive to **renal transporters and albumin
binding**; **long-chain** (npfc >= 7) is governed by **membrane
permeability and phospholipid binding**.

**This contradicts our animal result.** PFOA (npfc = 7) showed dose
dependence in male rats; PFHxA (npfc = 5) showed none - yet Fischer puts
the short-chain compound in the transporter-controlled regime where
saturation should be easiest to provoke.

Candidate resolutions, none tested:
- PFHxA clears ~200x faster, so concentrations at the transporter may
  never approach Km even at 300 mg/kg: transporter-controlled but never
  saturated.
- Reabsorption and secretion transporters saturate in opposite
  directions and may partly cancel.
- Fischer's model is parameterised to mice; rat transporter expression
  differs sharply, which is the same species-and-sex story as the 44x
  male/female gap.

This is the most promising open thread in the project: a mechanistic
prediction our own data appear to contradict.

---

## 7. What to use

**Central estimates.** Rosato 2024's pooled general-population figures,
because they select on an explicit cessation-of-exposure criterion, come
with risk-of-bias scoring, and sit in the subgroup where studies agree:

| | pooled half-life (95% CI) | I2 |
|---|---|---|
| PFOA, general populations | **2.35 y (2.20-2.51)** | 43% |
| PFOA, workers | 2.92 y (1.66-4.19) | 93% |
| PFOS (total) | 4.77 y (3.26-6.29) | 97% |
| PFHxS | 5.35 y (3.16-7.55) | 93% |

The I2 split is itself a finding: **community-water cohorts agree with
each other; occupational cohorts do not.** Weight the former.

**When you need Vd and population variability too**, Chiu 2022 remains
the best model-based source, but note its 3.14 y sits above the pooled
value, consistent with including cohorts that had ongoing exposure.

**Sensitivity range.** Carry 1.3 y as a low anchor, knowing the study
behind it was excluded from the systematic review and that its authors
called it an upper limit. If a conclusion flips between 1.3 and 3.14 y,
it is not robust to the current literature.

**Isomers.** Branched is not uniformly faster: pooled L-PFOS 3.13 y,
2/6m-PFOS 2.55 y, 3/4/5m-PFOS 3.94 y, **1m-PFOS 5.86 y**. The isomer
correction is real but not one-directional, which weakens one plank of
the Campbell 2022 argument.

---

## 8. Open questions worth pursuing

1. **Re-run Li 2022's tertile analysis with age adjustment.** If the
   negative between-person association survives, saturation is in real
   trouble at the individual level. If it vanishes, the age confound is
   confirmed and the within-person evidence stands alone. This needs
   individual-level data, not the published tables.
2. **Resolve the Fischer tension** by testing PFHxA at doses high enough
   to approach transporter saturation, or by checking whether rat and
   mouse transporter expression explain the reversal.
3. **Female rats for PFOA** (7 dose levels over 3200x available). If
   clearance is 44x higher because reabsorption is weaker, the dose slope
   should be *flatter* than males' - a sharp, falsifiable prediction from
   the mechanism.
4. **Ask Li et al. about the Table S4 direction**, which appears to
   contradict their own text. Worth confirming before building on either.
