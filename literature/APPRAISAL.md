# Human PFAS half-lives: which estimates to trust, and why they disagree

Literature search run through PubMed on 2026-09-29. Nine open-access
full texts were then pulled from PMC (`fetch_pmc.py`, files in
`fulltext/`); the rest is from abstracts. The `verified` column in
`studies.csv` records which is which. Nothing here is quoted from
memory.

> **Second update: Zhang 2013 and Li 2022 added.** The central
> controversy now has a quantitative resolution (see "Resolving the
> Zhang disagreement"), and Li 2022 supplies the individual-level test
> of the dose hypothesis.
>
> **Updated after four PDFs were added** (Rosato 2024, Andersson 2025,
> Fischer 2024, Fischer 2025). Three things changed: there are now
> pooled meta-analytic estimates to anchor on, the study at the centre
> of the short-half-life argument turns out to have been *excluded* from
> the systematic review, and two further assumptions had to be added to
> the list because a 2025 paper shows one of them is simply false.

## The disagreement is real and large

Published central estimates for the **human PFOA half-life**:

| source | estimate | basis |
|---|---|---|
| Dourson & Gadagbui 2021 | **0.5-1.5 y** | expert review incl. clinical data |
| ARA international collaboration 2022 | **1.3 y** ("likely < 2 y") | expert consensus, favouring Zhang 2013 |
| Bartell 2010 | **2.3 y** | community, after carbon filtration |
| Li 2018 (Ronneby) | **2.7 y** | community, after clean water supplied |
| Seals 2011 | **2.9 y** high-exposure district | former residents |
| Chiu 2022 | **3.14 y** | Bayesian hierarchical, many sites |
| Olsen 2007 | **3.8 y** (AM), 3.5 (GM) | retired workers |
| Worley 2017 | **3.9 y** | Decatur, one-compartment |
| Australian firefighters 2022 | **5.0 y** | after AFFF replacement |
| Seals 2011 | **8.5 y** low-exposure district | former residents |

That is a **17-fold spread**, and it matters: half-life feeds directly
into regulatory safe doses, so the ARA position would "likely raise many
existing regulatory safe levels".

The 2023 systematic review and meta-analysis (13 studies) puts the
between-study range at 1.48-5.1 y for PFOA, 3.4-5.7 y for PFOS and
2.84-8.5 y for PFHxS, and reports high heterogeneity.

## Six assumptions that drive the disagreement

The review names most of these explicitly; the direction of bias is what
matters when you read any single paper.

### 1. Ongoing, unmonitored exposure — inflates half-life
The big one. Every model assumes intake stopped (or is known). If people
keep getting PFAS from food, dust, consumer products or a second water
source, serum falls more slowly than true elimination, and the fitted
half-life is too long. The ARA collaboration treats this as the main
reason published values are too high. Worley's PBPK analysis
(PMID 28684146) supports it: historical **non-drinking-water** exposure
was needed to reproduce observed serum levels.

*Check:* did the study measure or model any non-water source? Most did
not.

### 2. Background exposure not subtracted — inflates half-life

**Now measured.** Li 2022 (Ronneby) reports its estimates both ways.
Subtracting background shortens the half-life by:

| | no subtraction | background subtracted | change |
|---|---|---|---|
| PFOA | 2.99 y | 2.47 y | **-17%** |
| L-PFOS | 2.87 y | 2.73 y | -5% |
| PFHxS | 4.55 y | 4.52 y | -1% |

So the bias is real, in the predicted direction, and modest - around 17%
at worst, in a cohort whose levels were far above background. It does
**not** account for the 17-fold spread on its own. Expect it to be much
larger in cohorts whose levels approach background, which is exactly
Seals' low-exposure district.

Related but distinct. Serum decays toward a non-zero background, not
zero. Fitting a pure exponential to a curve with a floor makes the decay
look slower, and the bias grows as levels approach background. Chiu 2022
handles this explicitly (NHANES-based background with a 20% drinking
water share); most single-cohort studies do not.

*Check:* is there a background term in the model? If not, the estimate is
biased long, more so the longer the follow-up.

### 3. Isomers pooled — deflates the linear-PFOA estimate
Branched isomers appear to clear faster than linear. Measuring "total
PFOA" mixes them, so the fitted half-life sits below the linear value.
This pushes in the *opposite* direction to (1) and (2), which is exactly
why the literature is confusing: two large biases of opposite sign.

*Check:* linear and branched reported separately? Only a few
(Li 2022; the aviation-firefighter Cl-PFOS study) do.

### 4. Which average is reported — arithmetic vs geometric
Olsen 2007 reports both: PFOS 5.4 y arithmetic, 4.8 y geometric; PFHxS
8.5 vs 7.3. That is a 10-15% difference from the summary statistic
alone. Half-lives are right-skewed across people, so the arithmetic mean
always exceeds the geometric mean.

*Check:* comparing an AM from one paper to a GM from another
manufactures a difference that isn't there.

### 5. Follow-up short relative to the half-life — unstable either way
Bartell 2010 observed ~1.2 years to estimate a 2.3-year half-life, i.e.
about half a half-life. Olsen 2007 had 5 years for a 3.8-year half-life.
Short windows make the estimate very sensitive to background and to
measurement error.

*Check:* how many half-lives were actually observed? Want >= 1, ideally
2-3.

### 6. Population — age and sex are real effect modifiers
Zhang 2013 (via ARA) separates young females (GM 1.7 y) from males and
older females (GM 1.2 y). Menstruation is a genuine elimination route.
Occupational cohorts are mostly male; community cohorts are mixed. Some
of the between-study spread is real biology, not method.

### 7. Which excretion routes are counted — invalidates urine-only methods

**This assumption turns out to be false, not merely unverified.**
Andersson et al. 2025 measured matched serum, urine and faeces in 147
Ronneby subjects:

| | urinary elimination | faecal elimination | dominant route |
|---|---|---|---|
| L-PFOS | 91 ng/day | **364 ng/day** | faeces, 4:1 |
| PFOA | **26 ng/day** | 15 ng/day | urine, ~1.7:1 |

Their opening line is that "most pharmacokinetic models assume that the
urinary route dominates". For PFOS that is wrong by a factor of four.

Any half-life estimated from renal clearance alone therefore counts only
part of total elimination, underestimates clearance and **overestimates
half-life** - badly for PFOS, moderately for PFOA. This retrospectively
justifies Rosato's decision to exclude renal-clearance-only studies, and
it is a specific, empirical strike against that whole method class.

### 8. The assumed volume of distribution — scales clearance-based estimates directly

Any mass-balance method computes t-half = ln2 x Vd / CL, so the assumed
Vd multiplies straight through. Andersson's measured values are far
below those in common use:

| source | PFOA Vd | PFOS Vd |
|---|---|---|
| Andersson 2025 (measured) | **0.074 L/kg** | 0.093 L/kg |
| Chiu 2022 (fitted) | 0.43 L/kg | 0.32 L/kg |
| Commonly assumed | 0.17-0.20 L/kg | - |

A 2-6x disagreement on Vd is a 2-6x disagreement on any half-life
derived this way. When comparing a clearance-based estimate against a
serum-decay estimate, this is often the real source of the difference,
and it is rarely stated prominently.

## A ninth, specific to this project: exposure level

Now resolved against full text, and the answer is more interesting than
the abstracts suggested.

### Seals 2011 read properly

The full text shows the study is **better controlled than its abstract
implies**. It did subtract background (5 ng/mL), did truncate at
15 ng/mL to keep subjects away from background, and did run sensitivity
analyses over both choices. Half-lives stayed apart under every setting:
Little Hocking 2.5-3.0 y, Lubeck 5.9-10.3 y.

Its strongest internal argument is one the abstract omits entirely:

> "the rate of decay (slope) of the second linear segment for Little
> Hocking is similar to the rate of decay for the first segment for
> Lubeck **at similar concentration levels**"

That is a matched-concentration comparison inside one study - the same
logic we used across species. The decay rate tracks **concentration**,
not district identity and not time since leaving. It is real evidence
for concentration-dependent clearance in humans.

### But the implied effect is mechanistically impossible

Little Hocking ran about 2x Lubeck's serum level. Turning the half-life
ratio into a slope of ln(clearance) on ln(concentration):

| Little Hocking | Lubeck | ratio | implied slope |
|---|---|---|---|
| 2.9 y | 8.5 y | 2.93 | **+1.55** (headline) |
| 3.0 y | 5.9 y | 1.97 | +0.98 (most conservative) |
| 2.5 y | 10.3 y | 4.12 | +2.04 (most extreme) |

For saturable renal reabsorption, CL(C) = CLmax x C/(Km + C), so
d ln CL / d ln C = Km/(Km+C), which is **at most 1** and falls toward 0
as concentration rises. A slope of 1.55 cannot be produced by this
mechanism; even the most conservative pairing sits at the ceiling.

So Seals' effect is real in direction but too large in magnitude to be
saturation alone. The residual is bias, and the paper names the likely
source: truncation at 15 ng/mL removed proportionally **more** Lubeck
subjects (they started lower), and "estimated half-lives were sensitive
to the truncation cut point". It is also cross-sectional - half-life
inferred from years-since-moving-away, not from following anyone.

### The cross-cohort test agrees with the rats

Li 2018's Table 1 tabulates initial serum level *and* half-life for
longitudinally followed cohorts. Pairing those (`human_dose_test.py`,
`human_initial_vs_halflife.csv`) gives a slope of ln(clearance) on
ln(initial level):

| chemical | n cohorts | slope | r |
|---|---|---|---|
| PFHxS | 3 | +0.27 | +0.94 |
| PFOA | 7 | +0.17 | +0.54 |
| PFOA excluding Seals | 5 | **+0.09** | +0.60 |
| PFOS | 3 | -0.12 | -0.79 |

**PFOA at +0.09 across human cohorts is almost exactly the +0.11 we
measured within male rats** over a 250x dose range - two completely
independent datasets, species and designs, landing on the same small
positive slope. PFHxS is steeper; PFOS runs the other way. Consistent
with a modest saturable component that varies by chemical, which is what
the animal work showed too (PFOA yes, PFHxA no).

Caveat: these are 3-7 cohorts each, confounded with study design, and
the "initial level" is a median or mean transcribed from a summary
table. It is a sanity check, not an estimate.

### What this does to the species hypothesis

It strengthens the mechanism and still refutes the explanation. A slope
of ~0.1 applied to the 187x human/rat serum gap predicts a half-life
ratio of 187^0.1 = 1.6x. The observed gap is 81x. Concentration
dependence is real, reproducible across species, and roughly an order of
magnitude too small to matter here.

Also note Olsen 2007's own closing line: species differences in
pharmacokinetics "may be due, in part, to a **saturable renal resorption
process**" - the same mechanism our rat dose analysis pointed at, and the
reason clearance does not scale with body weight.

## How to rank the studies

Tiers by how many of the six biases they control, not by journal or
citation count:

**Tier 1 - built to isolate elimination**
- A known, abrupt end to the dominant exposure (water filtered, AFFF
  replaced, worker retired)
- Repeated samples spanning >= 1 half-life
- Background accounted for, or exposure so high that background is
  negligible
- Examples: Li 2018 (Ronneby; abrupt cessation, repeated samples, very
  high starting levels), Olsen 2007 (5 y follow-up, very high starting
  levels so background is negligible - its weakness is n=26, 24 of whom
  are male)

  On Li 2018 specifically: its full text states background was *not*
  subtracted, and explains why - "the PFAS levels of the last sample for
  all the individuals were far above what is expected in the
  background", with median PFHxS 180x the neighbouring municipality.
  Not subtracting background is a weakness only when levels approach it.
  Here it is a justified design choice, and the paper says so.

**Tier 2 - good design, one uncontrolled bias**
- Bartell 2010: clean cessation, but only ~half a half-life observed
- ~~Worley 2017~~ - moved to Tier 3: Rosato excluded it because the main
  exposure was still present or its cessation was not clearly defined
- Chiu 2022: handles background and pools many sites, but assumes the
  same k applies across sites and relies on reconstructed exposure
  histories

**Tier 3 - informative but heavily confounded**
- Seals 2011: cross-sectional - half-life inferred from years since
  moving away rather than from following anyone; truncation at 15 ng/mL
  removed more low-exposure subjects; assumed uniform exposure within a
  water district. Better controlled than its abstract suggests, but the
  implied concentration effect exceeds what saturation can produce
- Firefighter cohorts: ongoing occupational exposure hard to exclude
- Any "temporal trend" study: excluded by the 2023 review for good reason

**Expert-judgement documents, not primary estimates**
- Dourson 2021 and ARA 2022 re-weight existing studies rather than adding
  data. Their conclusion (< 2 y) follows from taking bias (1) as dominant
  and Zhang 2013 as the cleanest study. That is a defensible reading, not
  a measurement. Note both appear in *Regulatory Toxicology and
  Pharmacology* and the shorter half-life would relax regulatory limits -
  worth knowing when weighing the argument, though it does not make the
  argument wrong.

## Resolving the Zhang disagreement

Zhang 2013's Methods, now read directly, explain the whole thing:

    T-half = 0.693 * V / CL_total          one-compartment mass balance
    CL_total := CL_renal                   urine only (+ menstrual, young females)
    V        := ASSUMED 170 mL/kg (PFOA), 230 (PFOS), from Thompson et al.

**Vd is an assumption, and half-life scales linearly with it.** Published
Vd values for PFOA span almost sixfold, so rescaling Zhang's own number:

| Vd source | Vd (mL/kg) | implied PFOA half-life |
|---|---|---|
| Andersson 2025 (measured) | 74 | 0.57 y |
| **Zhang's assumption** | **170** | **1.30 y** |
| Chiu 2022 (fitted) | 430 | **3.29 y** |

Substituting Chiu's fitted Vd into Zhang's own clearance data gives
3.29 y - against Chiu's independent serum-decay estimate of 3.14 y. The
two methods, held up as contradicting each other, **agree to within 5%
once they use the same Vd**. The disagreement was never about the data.

Zhang's second assumption pushes the other way. It sets total clearance
equal to renal clearance, and Andersson 2025 shows PFOA is only about
1.7:1 urinary, so true clearance is higher and the half-life lower.
Applying both corrections:

| | PFOA half-life |
|---|---|
| Zhang as published | 1.30 y |
| + Chiu's fitted Vd | 3.29 y |
| + non-renal elimination | **1.93 y** |
| *Rosato pooled, general populations* | *2.35 y* |

Zhang's own paper says as much: its estimates "should be considered as
**upper limit** estimates of the biological half-life" because non-renal
routes were not accounted for. The ARA collaboration adopted 1.3 y as a
central tendency; the authors offered it as a bound.

### The practical rule this yields

**Serum-decay designs never need Vd.** They read the elimination rate
straight off the slope of log concentration against time. Mass-balance
designs need both a Vd and a complete accounting of excretion routes,
and both are uncertain by factors of 2-6.

That is the clearest single criterion for which estimates to trust, and
it is structural rather than a judgement about any author.

## The dose hypothesis - CORRECTED

An earlier version of this file reported that Li 2022 confirmed the dose
hypothesis at the individual level, on the strength of its text. **Its
supplementary Table S4 shows the opposite**, and the table wins. Full
treatment in `SYNTHESIS.md` section 1; in brief, tertile 1 is the
LOWEST initial level (per Fig. 1's caption) and it has the SHORTER
half-life, so higher initial level goes with slower elimination -
significant for PFHxS and PFHpS.

The evidence now splits by the level of comparison, not by chemical:

| comparison | source | direction |
|---|---|---|
| within a person over time | Li 2022 Table 5 | **supports** saturation |
| within a species across doses | our rat fits | **supports** (PFOA +0.11) |
| between people, one cohort | Li 2022 Table S4 | **contradicts** (p=0.02) |
| between human cohorts | `human_dose_test.py` | mixed |
| between water districts | Seals 2011 | +1.55, above the ceiling |

Within-unit comparisons support it; between-unit comparisons do not.
Li 2022 supplies the likely confounder: age has a very strong effect
(preteens 45-60% shorter half-lives than over-50s) and also drives
accumulated burden, so between people, higher initial level partly means
older, and older means slower. Within-person and within-study contrasts
are immune to that.

Net: concentration dependence is real but small, of order 0.1 on a
log-log slope against a mechanistic ceiling of 1.

## Mechanism: why chain length decides everything

The two Fischer papers give the physical basis, and it reframes the
animal dose results.

**Fischer 2024** measured PFAS binding to the two dominant serum
proteins. There is a switch at seven perfluorinated carbons: PFAS with
npfc < 7 bind mostly to albumin, npfc >= 7 bind preferentially to
globulins. The unbound fraction varies up to 2.5-fold between
individuals in NHANES - which is a mechanism for interindividual
variability in half-life that no compartmental model represents.

**Fischer 2025** built a PBTK model and ran sensitivity analysis:
elimination of **short-chain** PFAA (npfc <= 6) is most sensitive to
**renal transporters and albumin binding**, while **long-chain** PFAA
(npfc >= 7) is governed by **membrane permeability and phospholipid
binding**.

### A tension worth chasing

That cuts against our animal result. PFOA (npfc = 7) showed a dose
dependence in male rats (clearance ~ dose^0.11) and PFHxA (npfc = 5)
showed none - yet Fischer puts the *short*-chain compound in the
transporter-controlled regime, where saturation should be easiest to
provoke.

Possible reconciliations, none tested here:
- PFHxA is cleared roughly 200x faster, so concentrations at the
  transporter may stay well below Km even at 300 mg/kg - transporter-
  controlled but never saturated.
- The relevant transporters differ in direction: saturating
  *reabsorption* raises clearance, saturating *secretion* lowers it, and
  the two could partly cancel.
- Fischer's sensitivity analysis is parameterised to mice; rat
  transporter expression differs sharply, which is the same
  sex-and-species story as the 44x male/female rat gap.

This is the most promising open thread in the whole project: a
mechanistic prediction that our own data appear to contradict.

## The practical answer

For a **central estimate**, prefer **Rosato 2024's pooled general-
population figure of 2.35 y (2.20-2.51) for PFOA**. It pools studies
selected on an explicit cessation-of-exposure criterion, it is the
subgroup where studies actually agree (I2 = 43%), and it comes with a
risk-of-bias assessment. Chiu 2022's 3.14 y remains the best single
*model-based* estimate and the right one when you need Vd and
population variability alongside the half-life, but note it sits above
the pooled value - consistent with its inclusion of cohorts with
ongoing exposure.

For PFOS use 4.77 y (3.26-6.29) and PFHxS 5.35 y (3.16-7.55), both with
the caveat that I2 exceeds 90%.

For **sensitivity analysis**, carry the ARA 1.3 y as a low anchor, but
weight it knowing the study behind it was excluded from the systematic
review. If a conclusion flips between 1.3 y and 3.14 y, it is not
robust to the current state of the literature.

For the **species/dose question**, none of this rescues the hypothesis.
The human-animal gap is ~80x; the entire human literature disagrees
within a 17x band, and the best-designed human studies cluster at 2.3-3.9
y rather than at the extremes. Even taking the ARA's 1.3 y, the gap to a
14-day rat half-life remains ~34x, far beyond what any measured dose
slope supports.

## Gaps in this collection

- 13 studies are in the 2023 meta-analysis; `studies.csv` has the main
  ones but not all. The review itself is paywalled (no PMC copy), so its
  extraction table was not available.
- Zhang 2013's numbers here come from the ARA paper, not the original.
  Worth verifying directly - it carries a lot of weight in the
  short-half-life argument.
- ~~Seals 2011 full text~~ - retrieved and analysed above.
- No search yet for non-English studies, or for PFNA/PFDA/PFBS in humans
  (thin literature).
- PMC access is now open, so all open-access full text is reachable;
  paywalled papers (the 2023 meta-analysis, Zhang 2013, the two
  Regulatory Toxicology papers) still need PDFs.
