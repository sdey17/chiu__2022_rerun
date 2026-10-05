# What this project has learned so far

Six phases, each building on the last. This file is the short version;
each phase has its own directory with the code, the data and a longer
write-up. Read this first, then follow the links.

| phase | question | directory | verdict |
|---|---|---|---|
| 1 | Why did our Python re-fit disagree with Chiu et al. 2022? | [`chiu_replication/`](chiu_replication/) | four specific bugs, all found and fixed |
| 2 | How does the EPA's animal PK pipeline work? | [`pfas_dose/`](pfas_dose/) | 1- vs 2-compartment Bayesian fits, chosen by LOO |
| 3 | Does clearance depend on dose *within* a species? | [`pfas_dose/`](pfas_dose/) | yes for PFOA, but weakly (slope ≈ 0.11); no for PFHxA |
| 4 | Does dose explain the human/rodent half-life gap? | [`species_dose/`](species_dose/) | **no** — about 13% of it at best |
| 5 | What does the wider literature actually support? | [`literature/`](literature/) | the 17-fold PFOA controversy is one assumed constant |
| 6 | So *why* do the species differ, and what did the field assume? | [`tk_review/`](tk_review/) | clearance, not distribution — and one mechanistic axis orders every species |

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

## Phase 6 — the species question, at the source

Phases 1–5 asked whether *dose* explained the species gap and found it did
not. Phase 6 asked what does, by reading 186 full texts and re-deriving the
numbers from the tables they came from. Full write-up in
[`tk_review/report/REPORT.md`](tk_review/report/REPORT.md);
the short version is
[`tk_review/EXECUTIVE_SUMMARY.md`](tk_review/EXECUTIVE_SUMMARY.md).

**It is clearance, not distribution.** Six datasets that measure both terms
in both sexes: Vd spans **1.33–2.18×** (male higher every time), clearance
spans **0.78–44.3×** and changes sign between species. Argoul 2026
reproduces this inside one experiment — clearance spans 5,254×, Vss 7.7×.

**One axis orders every species.** Fractional renal reabsorption,
`CL_renal = fu · GFR · (1 − FR)`:

| species | FR |
|---|---|
| human | 99.94% |
| mouse M / F | 97.0 / 95.2% |
| rat M | 93.7% |
| macaque M / F | 91.2 / 81.2% |
| dog M / F | 59 / 52% |
| rat F, rabbit | net secretion |

It predicts every rodent within **1.7×** over a 37× span with no fitted
parameter. Of the 333× male-mouse-to-human renal clearance gap, the escape
fraction carries 50× and the ~6× lower human GFR carries 6.5× (68%/32% on a
log scale).

**Humans run two near-complete reabsorption loops,** renal (99.94%) and
biliary (97%, Harada 2007). The second closes the 4.3× human residual and
reconciles Andersson (faeces dominant) with Abraham (faecal not detected):
at 97% resorption the gross biliary flux is large while net faecal
elimination is small.

**The human Vd that nine regulatory clearance factors inherit is a
calculation, not a measurement.** It is reproducible to three figures from
Thompson 2010's own Table S1 given an assumed `k = 0.0008/day` — and that
half-life came from Bartell 2010, measured in the *same two communities*.
The half-life cancels from any derived clearance; the Vd does not
(168 mL/kg at 2.3 y → 277 at 3.8 y).

**The binding conflict was a ratio artefact, not a contradiction.** Han's
">90% bound" is a floor computed from Kd and albumin, and Fischer's measured
`fu = 0.00061` satisfies it. Han titrated 50–60 µM albumin with 0.1–3 mM
PFOA (1.7:1 to 60:1); human serum sits at 10⁻⁵–10⁻³:1. The defect was
downstream: PBPK models read ">90%" as "≈90%", ~164× too high.

**18 corrections to the published record** are listed in §8 of the report,
including EPA's "2.5-fold" Oatp1a1 ratio (it is OAT-K's number; the real
value is 23×), two values altered in OEHHA's adaptation of Han Table 4, and
a transposition of Thompson's PFOA/PFOS volumes in Andersson 2025.

**Half-life is the wrong QSAR endpoint** (§11). Because `t½ = ln2·Vd/CL`, it
carries a body-size term. The replacement is the dimensionless renal
handling ratio `R = CL_renal/(fu·GFR)`, which divides out GFR and fu and
leaves the transport step. On the nine compounds where both terms were
measured in one experiment, R spans 875× — and chain length alone does not
order it.

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

## Closed since this file was first written

- **Li 2022's tertile analysis, age-adjusted.** Done in phase 6 from the
  paper's own supplementary variance decomposition rather than
  individual-level data: age carries 2–13× the partial R² of initial PFAS
  concentration, and the tertile effect is only 25–37% the size of the age
  effect. See `tk_review/db/li2022_age_adjustment.csv`.
- **Why the species differ.** Phase 6: clearance, not distribution, and one
  reabsorption axis orders every species.
- **The Han/Fischer binding conflict.** A ligand:protein ratio artefact, not
  a contradiction — §6.2 of the report.

## Still open

1. **A measured human K_T.** Six in vitro Km values span 47–310 µM against a
   PBPK-fitted 0.133 µM — a 354–2,336× contradiction, and no paper is known
   to supply the measurement.
2. **Unbound fraction by a single method across species.** Every value of
   the renal handling ratio is proportional to `fu`, and the mouse and human
   numbers currently come from different methods at different
   ligand:protein ratios. Measuring them one way decides whether the species
   difference is binding or transport — a ~33× swing. No animals required.
3. **Whether the biliary 0.97 replicates beyond n = 4.** It is now
   load-bearing for the human limb.
4. **The Fischer 2025 tension:** their PBTK puts short-chain PFAS in the
   transporter-controlled regime where saturation should be easiest, yet
   PFHxA (C5) showed no dose slope and PFOA (C7) did.
5. **Female-rat PFOA dose slope** — 7 dose levels over 3200× are available.
   If female clearance is 44× higher because reabsorption is weaker, the
   slope should be *flatter* than males'. Sharp and falsifiable.

The review keeps its own live list in
[`tk_review/WANTED.md`](tk_review/WANTED.md) (papers still wanted)
and §9 of the report (what nobody knows).

## Where to go next

**To learn the methods:** [`tk_learning/`](tk_learning/) builds
toxicokinetic modelling up from first principles on the animal data used
above, in twelve runnable lessons with figures, worked answers and a
regression test suite: forward simulation, log-linear fitting, nonlinear
least squares, oral absorption, Bayesian hierarchical fitting, one-vs-two
compartments by LOO, numerical ODE solving, volume of distribution, and a
working four-compartment PBPK model.

**To continue the science:** the next unblocked step needs no new data — a
two-loop PK model carrying renal `FR` and biliary 0.97 as explicit terms,
validated against the bile-acid-sequestrant data (Delaere 2025, Genuis
2010). After that, the single-method `fu` panel above, which serves both the
species question and the structure-activity work in §11.

Three of those lessons re-derive this project's own conclusions from
scratch, which is the best check on them there is:

- **Lesson 09** shows the 17-fold human PFOA controversy of phase 5 is,
  mechanically, a choice between four different volumes that any
  two-compartment model defines — `t½ = ln2·V/CL` gives 5.0, 6.5 or
  15.9 days on one dataset depending on which V you use.
- **Lesson 10** reaches phase 4's conclusion from data alone: across 7
  experiments matched on study, dose and route, female rats clear PFOA
  **28× faster** than males. Dose, at the measured slope of 0.11, would
  need a 10¹³-fold change to do that. Biology beats dose by two orders
  of magnitude.
- **Lesson 12** reaches phase 2's conclusion from mechanism: a PBPK
  model with correct organ volumes and blood flows, calibrated only on
  the rat, over-predicts the monkey half-life by 11× and the human by
  3×. Anatomy scales; renal transporters do not.
