# Human PFAS half-lives: which estimates to trust, and why they disagree

Literature search run through PubMed on 2026-09-29. Nine open-access
full texts were then pulled from PMC (`fetch_pmc.py`, files in
`fulltext/`); the rest is from abstracts. The `verified` column in
`studies.csv` records which is which. Nothing here is quoted from
memory.

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

## A seventh, specific to this project: exposure level

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
- Worley 2017: one-compartment model, no background term
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

## The practical answer

For a **central estimate**, Chiu 2022 is the most defensible for this
project's purpose: it is the only one that pools multiple populations,
carries background explicitly, and reports genuine uncertainty rather
than a point estimate. Use 3.14 y for PFOA with the caveat that the
plausible range across methods is roughly 1.5-5 y.

For **sensitivity analysis**, carry the ARA 1.3 y as a low anchor. If a
conclusion flips between 1.3 y and 3.14 y, it is not robust to the
current state of the literature.

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
