# What this project has learned so far

Five phases, each building on the last. This file is the short version;
each phase has its own directory with the code, the data and a longer
write-up. Read this first, then follow the links.

| phase | question | directory | verdict |
|---|---|---|---|
| 1 | Why did our Python re-fit disagree with Chiu et al. 2022? | `./` (`model.py`) | four specific bugs, all found and fixed |
| 2 | How does the EPA's animal PK pipeline work? | `pfas_dose/` | 1- vs 2-compartment Bayesian fits, chosen by LOO |
| 3 | Does clearance depend on dose *within* a species? | `pfas_dose/` | yes for PFOA, but weakly (slope ≈ 0.11); no for PFHxA |
| 4 | Does dose explain the human/rodent half-life gap? | `species_dose/` | **no** — about 13% of it at best |
| 5 | What does the wider literature actually support? | `literature/` | the 17-fold PFOA controversy is one assumed constant |

---

## Phase 1 — replicating Chiu et al. 2022

**The model.** One compartment, three levels of hierarchy
(population → study → person):

```
dC/dt = DWI·DWC/Vd − k·(C − Cbgd)        half-life = ln(2)/k
```

Four PFAS, fitted in PyMC against Chiu's own MCSim input files. Final
agreement with the paper's Table 3:

| PFAS | this code | paper |
|---|---|---|
| PFOA | 3.16 (2.65–3.77) | 3.14 (2.69–3.73) |
| PFOS | 3.34 (2.45–4.45) | 3.36 (2.52–4.42) |
| PFNA | 2.28 (1.53–3.19) | 2.35 (1.65–3.16) |
| PFHxS | 8.52 (5.66–13.01) | 8.30 (5.38–13.5) |

**The four bugs.** An earlier version gave PFOA 4.30 y instead of 3.14 y.

1. Only the *last* blood sample per person entered the likelihood; the
   t = 0 sample was dropped. Only the *difference* between two samples
   identifies k, so without the first one the starting level floats and
   correlates with k.
2. One shared background-scale parameter instead of one per study. In
   Chiu's own chains those scales differ hugely (Decatur +0.57, Arnsberg
   −0.69, Minnesota −0.77); a single value cannot fit all three and the
   model distorts k to compensate.
3. PFNA priors did not match Chiu's PFNA input file.
4. Water-concentration changes after the blood draw were simulated.

**The transferable lesson.** For PFOA, neither #1 nor #2 mattered much on
its own (3.16 → 2.94 and → 3.36), but together they moved the answer by
more than a year. *Ablating one error at a time can make every error look
harmless.* Always check the joint effect.

**The second transferable lesson.** The original disagreement was
diagnosed by reading Chiu's raw `.out` MCMC chains, not his narrative
text. This turned out to be the recurring theme of the whole project —
see the Li 2022 correction in phase 5.

---

## Phase 2 — the EPA animal pipeline

[USEPA/CPHEA-Animal-PFAS-PK](https://github.com/USEPA/CPHEA-Animal-PFAS-PK),
paper PMC12172007. What it does:

- A SQLite database of digitised serum time-courses across species, sexes,
  routes, doses.
- Both a **1-compartment** and a **2-compartment** model are fitted in
  PyMC to each chemical/sex/species group, with per-dataset clearance so
  each study gets its own value.
- **LOO cross-validation** (`az.compare`) picks between them. For PFOA in
  male rats the 2-compartment model wins by elpd_diff 40.7.

We reproduced their male-rat PFOA fit closely (CL 0.0150 vs 0.0151 L/kg/d,
Vdss 0.270 vs 0.289 L/kg, half-life 13.3 vs 14.2 d).

**Their headline conclusion:** volume of distribution scales with body
weight the way allometry predicts; **clearance does not**. Transporter
biology, not body size, sets PFAS elimination.

---

## Phase 3 — does dose change clearance?

Method: take the per-dataset clearances out of the posterior, then a
meta-regression `ln(CL) ~ β·ln(dose)` with **per-study intercepts**, so
the slope is measured *within* a study and not across studies that differ
in a hundred other ways.

| | PFOA (male rat) | PFHxA (male rat) |
|---|---|---|
| clearance | 0.0150 L/kg/d | 3.02 L/kg/d (200× faster) |
| half-life | 13.3 d | 0.095 d |
| dose slope β, gavage | **+0.110** (90% CI +0.007, +0.222) | +0.039 (−0.041, +0.122) |

So clearance goes roughly as dose^0.1: a 10× dose raises clearance ~1.3×.
Real, in the direction saturable reabsorption predicts, but small — and
the interval only just excludes zero.

**The mechanistic ceiling.** If elimination saturates,
`CL(C) = CLmax·C/(Km+C)`, so

```
d ln CL / d ln C = Km/(Km + C) ≤ 1
```

A log-log slope above 1 cannot come from saturation. Our 0.11 is far
below the ceiling; any published slope above 1 is telling you about bias,
not biology.

---

## Phase 4 — the cross-species hypothesis

**Hypothesis:** humans have multi-year half-lives because they are exposed
to far less; rodents are dosed high, so they clear fast. The species
difference is really a dose difference.

**The design problem:** species and dose are almost perfectly confounded.
Every human is low, every rodent is high. Both explanations predict the
same observation.

The exposure axis has to be **measured serum concentration**, not applied
dose — animals get a bolus in mg/kg, humans a daily intake in mg/kg/day,
and a saturable transporter responds to the concentration at the
transporter anyway.

Three tests break the confound. All three say no.

**1. The correlation reverses when you remove humans.**

| chemical | all species | animals only |
|---|---|---|
| PFOA | −0.64 | **+0.48** |
| PFOS | −0.85 | **+0.91** |
| PFNA | −0.46 | **+0.83** |
| PFHxS | −0.66 | **+0.65** |

The negative correlation is produced entirely by one point. Among animals,
whose serum spans 10–100×, the sign flips. There is no dose gradient
underneath — there is one outlying species.

**2. The slope is an order of magnitude too small.** Rat serum runs ~187×
human levels for PFOA; β = 0.11 predicts a 187^0.11 ≈ 1.8× half-life
ratio. Observed: **81×**. Dose explains ~13% on a log scale — and that is
generous, because a power law keeps accelerating while real saturation
*flattens* at low concentration.

**3. Species differ at matched exposure.** Across 24 species pairs within
2× on serum, half-lives still differ by a median of **2.6×** (up to 37×).

The clincher from the same database: **female rats clear PFOA 44× faster
than male rats at identical doses.** Sex, not dose.

---

## Phase 5 — the literature (20 sources)

**The 17-fold PFOA controversy is one assumed constant.** Published human
PFOA half-lives span 0.5–8.5 y. Zhang 2013 anchors the short end by mass
balance, `T½ = 0.693·V/CL`, with **V assumed at 170 mL/kg**:

| Vd source | Vd (mL/kg) | implied half-life |
|---|---|---|
| Andersson 2025 (measured) | 74 | 0.57 y |
| Zhang's assumption | 170 | 1.30 y |
| Chiu 2022 (fitted) | 430 | **3.29 y** |

Substituting Chiu's fitted Vd into Zhang's own clearance data gives 3.29 y
against Chiu's 3.14 y — **agreement within 5%**. Zhang's own paper calls
its numbers "upper limit estimates"; later reviews adopted 1.3 y as a
central tendency.

**The structural rule:** serum-decay designs read the rate off a slope and
never need Vd. Mass-balance designs need a Vd *and* a complete excretion
accounting, each uncertain 2–6×, multiplying straight into the answer.
That is a criterion for trust that does not depend on judging any author.

**An assumption that is simply false.** Andersson 2025 measured matched
serum/urine/faeces: L-PFOS excretion is **4:1 faecal**, PFOA ~1.7:1
urinary. Renal-clearance half-lives therefore miss most of PFOS
elimination.

**Dose evidence splits by level of comparison:**

| comparison | direction |
|---|---|
| within a person over time (Li 2022 Table 5) | supports |
| within a species across doses (our rat fits) | supports |
| between people in a cohort (Li 2022 Table S4) | **contradicts** |
| between cohorts | mixed |
| between water districts (Seals 2011, β=+1.55) | above the mechanistic ceiling → bias |

Within-unit comparisons support concentration dependence; between-unit
ones do not. That is the signature of a between-unit confounder, and
Li 2022 names it: **age**. Older people eliminate more slowly *and* have
higher accumulated burdens, so the between-person association is a
positive saturation effect minus a larger negative age effect.

**A correction we had to make.** We earlier reported Li 2022 as confirming
the hypothesis at the individual level, quoting its text. Its own
supplementary Table S4 shows the opposite: the *lowest*-exposure tertile
declines more steeply and has the shorter half-life (PFHxS 3.88 vs 4.83 y,
p = 0.02). Read the table, not the sentence — the same failure mode as
phase 1.

**What to use as a central estimate:** Rosato 2024's pooled
general-population values (PFOA 2.35 y, PFOS 4.77 y, PFHxS 5.35 y), which
apply an explicit cessation-of-exposure criterion and risk-of-bias
scoring. Note the I² split: community-water cohorts agree with each other
(43%), occupational ones do not (93%).

---

## Five things worth carrying forward

1. **Read the primary numbers.** Chains, not narrative. Supplementary
   tables, not abstracts. This project's two biggest corrections were both
   text-vs-table discrepancies.
2. **Check whether an effect is within-unit or between-unit** before you
   believe its sign. The same data can support and contradict the same
   hypothesis at different levels.
3. **Know the mechanistic ceiling** on any effect you are estimating.
   A saturation slope cannot exceed 1; measuring 1.55 tells you about the
   study design.
4. **Find the assumed constant.** In a mass-balance half-life it is Vd,
   and it multiplies straight through. Most "controversies" are one
   assumption in disguise.
5. **Ablate errors jointly.** Interacting bugs each look harmless alone.

## Still open

1. Re-run Li 2022's tertile analysis with age adjustment (needs
   individual-level data).
2. Resolve the Fischer 2025 tension: their PBTK puts short-chain PFAS in
   the transporter-controlled regime where saturation should be easiest,
   yet PFHxA (C5) showed no dose slope and PFOA (C7) did.
3. Female-rat PFOA dose slope — 7 dose levels over 3200× are available.
   If female clearance is 44× higher because reabsorption is weaker, the
   slope should be *flatter* than males'. Sharp and falsifiable.

## Where to go next

`tk_learning/` builds toxicokinetic modelling up from first principles on
the animal data used above, in nine runnable lessons with figures:
forward simulation, log-linear fitting, nonlinear least squares, oral
absorption, Bayesian hierarchical fitting, one-vs-two compartments by
LOO, numerical ODE solving (the bridge to PBPK), and volume of
distribution — where it shows that the 17-fold human PFOA controversy
in phase 5 above is, mechanically, a choice between four different
volumes that a two-compartment model defines.
