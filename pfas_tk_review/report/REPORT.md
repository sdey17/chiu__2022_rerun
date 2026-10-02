# Why PFAS half-lives differ between humans, rats and mice

A literature review built around one question: **is the species difference in
PFAS elimination a difference in how much is given, how much is held, or how
much is let go?**

The answer is the third, and it is not close. Everything else in this report is
either the evidence for that, the assumptions that obscured it, or the places
where the evidence runs out.

---

## 0. How to read this

Section 1 builds the foundation — one equation that governs the whole subject.
Everything after is an application of it. Sections 2–4 answer the three
questions you asked, in order. Sections 5–7 are the supporting evidence
(assumptions, binding, transporters). Section 8 lists what this review corrects
in the existing repository, section 9 what nobody knows yet.

Code blocks are runnable from `pfas_tk_review/`. Every number traces to
`db/*.csv`, and every row there carries a PMID or DOI and the table it came
from.

There are questions at the end of several sections. They are there because the
reasoning is easy to follow and easy to half-follow, and the difference matters.

---

## 1. The foundation: one equation, three quantities, two of them free

Elimination kinetics rests on an identity:

```
t½ = ln2 · Vd / CL
```

- **Vd**, volume of distribution (L/kg) — the apparent volume the compound
  occupies. It is not an anatomical volume. It is the number that relates total
  body burden to plasma concentration.
- **CL**, clearance (L/kg/day) — the volume of plasma cleared of compound per
  unit time.
- **t½**, half-life — *not an independent quantity*. It is what the other two
  produce.

This matters more than it looks. **Any two of the three fix the third.** So a
paper reporting a half-life has either measured two things or measured one and
assumed another. Which it did decides how much to trust the number — and most
of the disagreement in this literature is an argument about an assumption, not
about data.

```bash
cd pfas_tk_review
python3 scripts/human_parameter_reconciliation.py
```

That script lays each major human source side by side and completes whichever
term it left implicit. The result is section 5.

### Two designs, two failure modes

| design | what it measures | what it must assume | fails when |
|---|---|---|---|
| **serum decay** — follow concentration after exposure stops | the elimination rate directly, from the slope of log C against t | that exposure actually stopped; that background is negligible or subtracted | exposure continues; levels approach background |
| **mass balance** — measure excretion and divide | clearance | a volume of distribution; *and* that you counted every excretion route | Vd is wrong; a route is missed |

**Serum-decay designs never need a Vd.** Mass-balance designs need both a Vd and
a complete excretion accounting, each uncertain by severalfold, and both
multiply straight into the answer. That single structural distinction sorts the
literature better than any judgement about authors or journals.

> **Check your understanding.** A paper reports a human PFOA half-life of 1.3 y
> from urinary clearance and an assumed Vd of 170 mL/kg. Someone objects that
> the true Vd is 430 mL/kg. Does the half-life go up or down, and by how much?
> *(Answer: up, by the Vd ratio — 2.5×, to 3.3 y. Half-life scales linearly with
> Vd. This is exactly what happened with Zhang 2013; see §8.)*

---

## 2. Your citation list: what it can and cannot support

The attached `PFAS_TK.xlsx` holds 81 citations. Each was resolved to a PMID
(title-matched against PubMed; the match check caught three wrong
identifications the automated search had made) and classified by evidence type.

```bash
python3 scripts/parse_xlsx_list.py && python3 scripts/resolve_pmids.py
python3 scripts/verify_pmids.py && python3 scripts/finalize_source_list.py
# -> db/source_catalogue.csv, 81 rows, 81 verified PMIDs
```

| category | n | can yield a TK parameter? |
|---|---|---|
| mechanistic / hazard only | 47 | no |
| in vivo toxicokinetics | 11 | yes |
| in vitro protein binding | 9 | yes |
| transporter or enzyme | 8 | yes |
| receptor binding | 3 | no |
| membrane biophysics | 3 | no |

**42 of 81 cannot contribute a half-life, Vd, clearance or binding constant.**
They are immunotoxicity, hepatic steatosis, oxidative-stress and
gene-expression studies — a hazard-characterisation corpus, which is a
different thing from a toxicokinetic one.

A further **21 are repeat-dose toxicity studies that measured serum or tissue
PFAS** without reporting kinetics. Those are flagged `supplies_internal_dose`,
because a measured internal concentration at a known administered dose is
exactly the dose↔serum pairing the exposure question needs, even with no
half-life attached.

The genuinely load-bearing entries are a small set: Kudo 2002 (sex-hormone
regulation of renal PFOA transport), Yang 2009 (Oatp1a1 reabsorption),
Nakagawa 2008 (OAT secretion), Han 2004 (α2u-globulin), Chang 2009 and
Chengelis 2009 and Lau 2020 and Das 2008 (rodent TK), and the albumin-binding
cluster (Luo 2012, Chen 2015, Wang 2016, Zhang 2009, Weiss-Errico 2018).

**So the review had to be built mostly from outside your list.** That is not a
criticism of the list; it is a statement about what it is for.

---

## 3. The species question: one axis, and the female rat falls off it

### 3.1 It is clearance, not distribution

Split the identity for every chemical × sex pair where both rodents were fitted:

```
ln(t_mouse/t_rat) = ln(Vd_mouse/Vd_rat) − ln(CL_mouse/CL_rat)
```

```bash
python3 scripts/rat_mouse_decomposition.py   # -> db/mouse_rat_decomposition.csv
```

| term | correlation with the half-life gap |
|---|---|
| volume of distribution | **r = +0.00** |
| clearance | **r = +0.87** |

Vd ratios stay inside ~4× for every chemical and sex. Clearance ratios reach
50×. Across all 46 species × sex × chemical groups in the database, **Vd spans
12.6× while clearance spans 7,384×**. Distribution is not where the action is.

### 3.2 The gap is specific to female rats — for long chains

| | female ÷ male clearance, **rat** | female ÷ male clearance, **mouse** |
|---|---|---|
| PFOA | **44×** | 1.8× |
| PFNA | **21×** | 1.1× |
| PFHxS | **20×** | 0.8× |
| PFOS | 0.8× | 1.0× |
| PFBA | 3.6× | **2.9×** |

Male mouse and male rat agree within ~4× for every chemical. The headline
15–31× "species" differences are **all in females, and all in long chains**.

The last row matters and I nearly missed it. **The mouse does show a PFBA sex
difference** — Chang 2008 measured 4.6–5.3×, as large as the rat's 5.2–6.2×. So
the mouse is perfectly capable of sex-dependent renal PFAS handling; what it
lacks is the sex dependence *for long-chain compounds*. Any explanation that
makes the mouse constitutionally sex-indifferent is wrong. And PFBA's sex
difference cannot be Oatp1a1-mediated, because C4 compounds do not interact with
Oatp1a1 at all (Yang 2009: no inhibition at 1 mM).

**How reliable are these ratios?** Less than their precision suggests, in three
specific ways:

- They are composites, `ln2·Vd,ss/CL`, not measured half-lives. For rat PFOA the
  measured male/female ratio is **8.5–72×** across five primary studies
  (Kudo 2002 72×; Ohmori 2003 70×; Kemper 2003 39–63×; Kim 2016 8.5–12×)
  against the composite's 20×. The EPA fit's female-rat Vd,ss of 0.649 L/kg is
  2–3× every other rat value in the same file, and measured female half-lives
  cluster at 1.9–4.6 h rather than the implied 16.6 h.
- **The mouse side of each ratio rests on exactly one study** — Lou 2009 (PFOA),
  Sundström 2012 (PFHxS), Tatum-Gibbs 2011 (PFNA) — while the rat side is
  replicated four to six times. The mouse PFNA male value of 227 d sits 3.3×
  above the measured ceiling of 34.3–68.9 d, with a tenfold-wide credible
  interval.
- A **route confound attacks the female rat specifically**: IV clearance
  significantly exceeded gavage clearance in female rats for six compounds
  (apparent bioavailability > 100%). EPA's PFHxS assessment responded by
  discarding all IV rat data; the fits producing these ratios pool IV and oral.

The direction and rough magnitude survive all three. The second decimal does not.

### 3.3 The axis that unifies all of it

OEHHA's PHG appendix (Table A6.4, pp. 327–328, adapted from Han et al. 2012)
tabulates GFR, measured renal clearance and net tubular reabsorption of PFOA
across seven species. Every group sits on one scale:

| | % of filtered PFOA reabsorbed |
|---|---|
| human | 99.8% |
| mouse male / female | 97.0% / 95.2% |
| **rat male** | **93.2%** |
| macaque male / female | 91.2% / 81.2% |
| dog male / female | 59% / 52% |
| **rat female** | **net secretion** |
| rabbit male / female | net secretion |

**The female rat does not reabsorb less — it secretes.** Its renal clearance
(666–1,009 mL/kg-day) exceeds its entire filtered load (288 mL/kg-day). The
mouse sits at 95–97% in *both* sexes. The 31× PFOA "species difference" is one
group crossing from net reabsorption into net secretion.

Because `t½ ∝ 1/(1−FR)`, small changes near FR = 1 produce enormous changes in
half-life. Going from 97% to 99.8% reabsorbed cuts the escaping fraction
fifteenfold.

```bash
python3 scripts/reabsorption_axis.py   # -> db/reabsorption_axis.csv
```

Using **only** measured renal clearance and fitted Vd — no free parameters —
the identity reproduces every rodent group to within **1.7×** across a 37×
half-life span:

| | Vd (L/kg) | CL_renal (L/kg/d) | predicted t½ | observed t½ | ratio |
|---|---|---|---|---|---|
| rat female | 0.649 | 0.838 | 0.5 d | 0.7 d | 0.78 |
| rat male | 0.289 | 0.0197 | 10.2 d | 14.2 d | 0.72 |
| mouse female | 0.299 | 0.0160 | 12.9 d | 21.5 d | 0.60 |
| mouse male | 0.252 | 0.0100 | 17.5 d | 25.6 d | 0.68 |

### 3.4 Two honest caveats

**The "99.8%" is softer than it looks.** It depends on an unbound fraction
OEHHA *assumed* to be 0.02 for every species. Fischer et al. 2024 measured human
serum PFOA f_unbound at **0.00061** by solid-phase microextraction — 33× lower.
Recomputed, the figure is 96.2%. The qualitative claim survives; the headline
number does not. The *prediction* above is unaffected, because `fu · GFR · (1−FR)`
is just `CL_renal` rearranged and f_unbound cancels.

**In the rat, the mechanism is established.** The sex difference is renal and
androgen-driven at the apical reabsorptive step, and the evidence is
interventional rather than correlational: castration raises male PFOA renal
clearance **14-fold** to the female level and testosterone reverses it
(Kudo 2002); oestradiol raises male 24-h urinary excretion from 9 ± 4% to
61 ± 19% of dose (Ylinen 1989); probenecid works only in castrated males
(Vanden Heuvel 1992). Rat renal Oatp1a1 is apical, male-dominant,
testosterone-induced (Lu 1996), and transports PFOA (Km 126–162 µM;
Weaver 2010, Yang 2009). Worley 2015's PBPK puts the whole difference in one
parameter, and Gotoh 2002 showed the mechanism can generate > 250× using a
non-PFAS Oatp1a1 substrate with GFR and protein binding held equal.

**Three competing hypotheses are dead** and should be stated as such:

- **α2u-globulin** — Han 2004 measured Kd ~10⁻³ M and concluded it "cannot
  adequately explain the sex-dependent elimination of PFOA in rats". The mouse's
  lack of α2u-globulin is a red herring.
- **L-FABP / I-FABP** — Modaresi 2025's double-knockout mouse showed no change
  in PFOS half-life, clearance or Vd.
- **Oat2** — the most sex-divergent rat renal transporter (male = 13% of female)
  does not transport PFOA at all (Nakagawa 2008).

**In the mouse, the mechanism is not established.** Mouse renal Oatp1a1 is
*also* androgen-dependent (Cheng 2005; Cheng 2006; Isern 2001 independently),
so its regulation is not rat-specific and cannot by itself generate the species
difference. The only clean measured rat-vs-mouse renal comparison (Buist &
Klaassen 2004) found the species difference in **Oat2 — the wrong transporter**.
**No mouse orthologue transport kinetics exist for any PFAS**, and no
sex-resolved mouse PFOA half-life pair has been measured anywhere — which is
precisely the number the 31× ratio depends on.

One plausible reconciliation, flagged as inference rather than finding: mouse
elimination is multi-route and compensating. Furukawa 2024's Abcb4-null mice
lose biliary PFOA but gain renal clearance via upregulated Abcb1, and
Abcb1a/b-null mice lose renal clearance. A redundant system is structurally
less sensitive to any single androgen-regulated step.

**So: the phenomenology is one axis and is quantitative. The mechanism is
established for the male rat and absent for the mouse.** That gap is itself a
result, and it is the highest-value experiment in §9.

### 3.5 PFOS is not exempt for the reason it looks

The obvious reading of the PFOS row — sulfonate head group escapes a pathway
that acts on carboxylates — **is wrong, and measured data refute it.** Rat
Oatp1a1 transports PFOS with ~7× *higher* affinity than PFHxS (Km 37 vs 256 µM),
and Zhao 2017 concluded outright that "rOATP1A1 is not the major transporter for
the renal elimination of PFOS".

What PFOS and PFDA actually share is that **renal excretion has become
negligible** — Kudo 2001 recovered 0.2% of a PFDA dose in urine over 120 h — so
there is nothing left for a reabsorptive transporter to modulate. The sex
difference needs a *window*: substantial renal elimination **and** adequate
Oatp1a1 affinity. C8–C9 carboxylates and the C6 sulfonate sit inside it; C4–C5
are not Oatp1a1 ligands at all; C10 carboxylate and C8 sulfonate are renally
silent.

> **Check your understanding.** Male mouse PFOS half-life is 35.5 d, male rat
> 57.1 d — the mouse is *faster*. But for PFOA the mouse is *slower* (25.6 vs
> 14.2 d). Why does the direction flip between two compounds in the same pair of
> species? *(Because the rat's androgen-regulated renal pathway acts on PFOA and
> is irrelevant for PFOS — not because PFOS fails to bind the transporter, but
> because PFOS barely leaves by the kidney at all. Remove that pathway and the
> two species sit within ~2× of each other.)*

---

## 4. Does exposure relate to half-life or to volume of distribution?

**To neither, materially.** Six independent lines agree, and they fail in
different ways, which is what makes the convergence persuasive.

### 4.1 Vd does not track dose or concentration

```bash
python3 scripts/vd_vs_dose.py
```

Slope of ln(Vd) on ln(serum), within species × sex across chemicals:

| group | slope | r | concentration range |
|---|---|---|---|
| primate male / female | −0.21 / −0.15 | −0.76 / −0.89 | 280–380× |
| rat male / female | −0.13 / −0.02 | −0.45 / −0.06 | 21–46× |
| mouse male / female | −0.14 / +0.25 | −0.40 / +0.30 | 14–74× |

Inconsistent in sign, weak, and the same on dose rather than serum. The
albumin-saturation prediction (saturated plasma binding → more compound in
tissue → larger apparent Vd) **fails from both ends**: Kudo 2007 measured 52% of
a 0.041 mg/kg IV PFOA dose in rat liver versus 27% at 16.56 mg/kg, so hepatic
uptake saturates first and apparent Vd *decreases* with dose. And human serum
albumin is ~410 µM while human PFOS at 5 ng/mL occupies **0.0024% of binding
sites**.

### 4.2 Half-life is nearly dose-independent — except in one group

Over 8–25× dose in the NTP rat studies (Huang 2019), half-life moves 12–20% at
most — while *apparent* clearance moves 1.5–2.9×. In four of six series the
clearance change is matched within a few percent by the opposite change in
bioavailability (PFHxS male: CL +1.87×, F 98%→52% = −1.88×). **The apparent
dose-dependence of clearance in those studies is a bioavailability artefact.**
EPA's PFHxA IRIS review tested dose-dependence formally and rejected it; Lau
2020 states PFBS clearance "was linear with exposure doses".

**The exception is the female rat, and it is large.** Kemper 2003 dosed PFOA at
four levels over a 250× range in both sexes:

| dose (mg/kg) | male t½ (h) | female t½ (h) | ratio |
|---|---|---|---|
| 0.1 | 202 | 3.2 | 63× |
| 1 | 138 | 3.5 | 39× |
| 5 | 174 | 4.6 | 38× |
| 25 | 157 | **16.2** | **10×** |

Over that 250× dose rise the male half-life moves 0.78× (slope −0.05) while the
female moves **5.1× (slope +0.29)**. The sex ratio collapses from 63× to 10×.

This is the clearest dose-dependence anywhere in the dataset, and it is
sex-specific — which makes mechanistic sense once the directions are kept
straight:

| group | regime | what saturates | effect of raising dose |
|---|---|---|---|
| male rat | reabsorption-dominated | reabsorption | clearance **↑** (slope +0.11) |
| female rat | secretion-dominated | secretion | clearance **↓** (slope −0.29) |

Saturating *reabsorption* lets more escape, so clearance rises. Saturating
*secretion* lets less be pumped out, so clearance falls. Both are observed, in
the predicted directions, in the same species and compound.

**Two consequences.** First, pooling doses blurs the sex difference, which is
part of why the EPA composite gives 20× where matched-dose measurements give
~70×. Second — and this is the one that matters for extrapolation — dose
dependence is strong only where a high-capacity secretory pathway exists to
saturate. Male rats, mice, monkeys and humans are all
reabsorption-dominated, and there the effect is the +0.1 of §4.4.

### 4.3 Saturation is unreachable at human exposure

Measured transporter Km values sit **2,200× to 82,000×** above current human
serum concentrations (NHANES geometric means: PFOA 1.56 ng/mL = 3.8 nM; PFOS
4.72 ng/mL = 9.4 nM). The tightest margin anywhere — C8 Health Project Little
Hocking mean 227.6 ng/mL against human URAT1 Km 64.1 µM = 26,542 ng/mL — is
**~117×**, at which the Michaelis–Menten term is 99.1% linear. Tubular water
reabsorption concentrates luminal fluid ~100-fold, closing two of the four
orders; a 20–800× margin remains.

### 4.4 The four slopes that do exist all land in the same place

| contrast | slope d ln(CL)/d ln(C) |
|---|---|
| male rat PFOA, 250× dose range (this repo) | +0.11 |
| human cross-cohort PFOA (this repo) | +0.09 |
| Abraham tracer dose vs cohorts | +0.08 |
| three PFBS studies over 1,200× | +0.12 |

Against a mechanistic ceiling of 1. Applied to the 187× human/rat serum gap,
+0.1 predicts a 1.6× half-life difference; the observed gap is 81×. **Dose
explains ~13% on a log scale, and that is generous.**

### 4.5 The confounder that manufactures the opposite conclusion

This is the most useful methodological finding in the review. Unsubtracted
background inflates a fitted half-life, and the inflation scales with how close
the cohort sits to background:

| serum ÷ background | inflation | source |
|---|---|---|
| 1.7 | **+150%** (5.0 → 2.0 y) | Nilsson 2022a, PFOA |
| 5.5 | +57% | Lyu 2026 |
| 13 | +20% | Xu 2020 |
| 49 | +15% | Batzella 2024 |
| 260 | +0.7% | Li 2022, PFHxS |

**Any cross-cohort regression of half-life on exposure that pools corrected and
uncorrected studies produces a spurious negative slope that is
indistinguishable from saturable reabsorption.** Low-exposure cohorts get
inflated half-lives; high-exposure cohorts do not. That alone can generate the
"higher exposure → shorter half-life" pattern with no mechanism behind it.

The limiting case is Gasiorowski 2022's randomised *control* arm: at serum PFOS
~11 ng/mL, 52 weeks produced −0.01 ng/mL (p = 0.96) — an effectively infinite
apparent half-life — with PFOA actually *rising* (p = 0.02).

And every between-person direct test gives the wrong sign for saturation:
Batzella 2024 (n = 5,860) finds PFOA half-life rising from 1.92 y in the lowest
baseline quartile to 2.85 y in the highest. The authors name the artefact
themselves — people with faster excretion have lower baseline concentrations
*because* they excreted more between exposure ending and first sampling, and
baseline was 41–75 months after cessation.

### 4.6 The between-person association does not survive adjustment

This project's longest-standing open question was whether Li 2022's
between-person result — higher initial level going with *longer* half-life,
the opposite sign to saturation — holds once age is controlled. Age is the
obvious confounder, because it drives both half-life and accumulated burden.

Individual data are not published, so no re-fit is possible. But the answer is
already in the supplement, in a table nobody quotes. **Table S14 reports partial
R² for each determinant of individual half-life — mutually adjusted by
construction**, since partial R² is the variance a term explains given the
others in the model.

```bash
python3 scripts/li2022_age_adjustment.py   # -> db/li2022_age_adjustment.csv
```

| determinant | PFOA | PFOS | PFHxS | range across 8 compounds |
|---|---|---|---|---|
| **Age** | 9.40% | 28.39% | 16.31% | **3.62 – 28.39%** |
| eGFR | 7.05% | 4.05% | 2.95% | 1.25 – 8.16% |
| Calprotectin | 6.78% | 5.43% | 7.71% | 0.24 – 7.71% |
| Gender | 0.87% | 3.02% | 5.39% | 0.87 – 6.16% |
| **initial PFAS tertile** | **0.70%** | **3.18%** | **2.32%** | **0.70 – 5.32%** |

**Initial PFAS level is the weakest determinant for 8 of 8 compounds**, beaten
by age by a median factor of 8.9× (range 2.0–37.4×). Adjusted, it explains under
1% of the variance in individual PFOA half-life.

A second, independent check points the same way. Comparing the two unadjusted
contrasts on the same cohort (n = 114), the tertile effect is only **6–37% the
magnitude of the age effect** for every compound — so a modest age imbalance
across tertiles accounts for all of it, and accumulated burden rising with age
makes that imbalance expected rather than hypothetical.

**Verdict: the between-person contradiction dissolves.** The within-person and
within-study evidence for mild concentration dependence stands alone and
unopposed, and the apparent between-person reversal was an age confound, exactly
as predicted. Note the sample for the adjusted table is n = 54, those with
complete data on all six determinants, against n = 114 for the unadjusted
tertile table.

> **Check your understanding.** Section 4.4 says higher dose → faster clearance
> (positive slope). Section 4.5 says the literature often shows higher exposure →
> *shorter* half-life, and calls that an artefact. Are those in conflict?
> *(No — they agree in sign. Faster clearance means shorter half-life. The point
> of 4.5 is that the observed between-cohort effect is far larger than +0.1 and
> is inflated by the background artefact, so it cannot be read as the mechanism.)*

---

## 5. Why published half-lives disagree: the assumption audit

`db/human_halflife_extended.csv` holds 142 rows from 39 studies, each carrying
the design fields that determine trustworthiness. `db/exposure_vs_halflife.csv`
(184 rows) pairs chemical, serum concentration, exposure amount and half-life
on one line, human and animal together.

### 5.1 The disagreement is about clearance, not Vd

```bash
python3 scripts/human_parameter_reconciliation.py
```

PFOA, each source's own triple with the missing term completed:

| source | Vd (mL/kg) | t½ (y) | CL (mL/kg/d) | derived |
|---|---|---|---|---|
| Abraham 2024 (measured, n=1) | **121** | 5.51 | 0.0417 | CL |
| Chiu 2022 (fitted) | 430 | 3.14 | 0.260 | CL |
| EPA 2024 (Vd assumed) | 170 | 2.70 | 0.120 | — |
| OEHHA 2024 (CL measured) | 398 | 2.70 | **0.280** | Vd |

Spread: Vd 3.6×, half-life 2.0×, **clearance 6.7×**.

Chiu's fitted parameters imply CL = 0.260 mL/kg-day against OEHHA's measured
0.280 — agreement to 7%. **So Chiu and OEHHA agree on clearance**, and the
~400 mL/kg Vd is what that shared clearance implies at a 2.7–3.1 y half-life.

Abraham et al. 2024 is the only **direct measurement** of human Vd: one
volunteer swallowed ~4 µg each of fifteen ¹³C-labelled PFAS and was followed
450 days in plasma, urine and faeces, giving `Vd = D_abs/C₀` with nothing
assumed. It gets 121 mL/kg and a 5.5 y PFOA half-life, hence a clearance **6.7×
below OEHHA's**. It needs no assumption about exposure cessation and no
background subtraction, because the label separates dose from background — it
is methodologically the strongest design in the human literature. It is also
n = 1, at tracer dose, with a half-life above every cohort estimate.

### 5.1a The donation trial adjudicates it — and sides with the measurement

Gasiorowski 2022 randomised 285 firefighters to donate plasma (up to 800 mL
every 6 weeks, mean 6.4 donations), donate whole blood (~470 mL every 12 weeks,
mean 4.3), or be observed. It removed a **known volume** of plasma from people
at **known serum concentrations** and measured the resulting fall. That is a
mass-balance experiment that fixes Vd without assuming a half-life:

```
Vd(L) = V_plasma removed × C_mean / ΔC_serum
```

The trial's own observation arm supplies the correction that makes it work —
subtracting it nets out continuing background intake and natural elimination.
**The authors never did this calculation.**

```bash
python3 scripts/gasiorowski_vd.py   # -> db/gasiorowski_vd.csv
```

| chemical | blood arm | plasma arm | Abraham 2024 | Chiu 2022 |
|---|---|---|---|---|
| PFOS | 113–124 | 182–199 | **152** | 320 |
| PFHxS | 71–78 | 171–187 | **125** | 290 |

Two arms of one trial, analysed independently, bracket Abraham's directly
measured values. **Chiu's fitted Vd sits above the entire range for both
compounds.**

Known directions of error: using the 800 mL ceiling as the plasma mean
*overstates* volume removed and so *overstates* the plasma-arm figure, which is
the higher of the two; counting only the plasma fraction of whole blood
*understates* the blood-arm figure. Body weight is reconstructed from the
reported BMI of 27.9 (weight is not reported) over a 84–92 kg range. The PFOA
row is not reliable — baseline was 1.2 ng/mL against a 1 ng/mL reporting limit,
and the authors' own sensitivity analysis more than halves the effect.

**So three independent human approaches — a labelled-dose study, a faecal/urinary
mass balance, and a randomised removal trial — all land at 74–199 mL/kg, while
the population-model fit gives 290–430.** The disagreement is real and it is now
three-to-one against the fitted value.

What it does *not* settle is clearance. For PFOS, Abraham's half-life (3.32 y)
and Chiu's (3.36 y) agree almost exactly while their Vd differ 2.1×, so the
clearance disagreement is entirely a Vd disagreement. For PFOA they differ on
both. **A population model that reproduces observed serum trajectories with a Vd
two to four times the measured one is fitting something, and what it is fitting
is the open question.**

### 5.1b EPA's own appendix says the human Vd literature never measured anything

The decisive confirmation is in a table nobody cites. EPA's 2024 appendix volume
tabulates the human PFOA Vd literature, and the table's **title** is the
finding:

> *Table B-26. Summary of PFOA Volume of Distribution Values **Assigned** in
> Human Studies*

```bash
python3 scripts/extract_epa_table_b26.py   # -> db/epa_table_b26_human_vd.csv
```

Ten entries. **All assigned, none measured.** Six assign exactly **170 mL/kg** —
Thompson 2010's calibrated value. The full range is 170–200 mL/kg, a spread of
1.18×.

| | Vd (mL/kg) | how obtained |
|---|---|---|
| Andersson 2025 | 74 | **measured**, urinary/faecal mass balance |
| Gasiorowski 2022 (derived, §5.1a) | 113–199 | **measured**, randomised removal |
| Abraham 2024 | 121 | **measured**, labelled oral dose |
| *EPA Table B-26, ten human studies* | *170–200* | ***assigned*** |
| Thompson 2010 | 170 | calibrated against an assumed half-life |
| Chiu 2022 | 430 | fitted by population model |

**The apparent tight agreement of the human Vd literature is an artefact of
everyone adopting the same assumed constant.** Every direct measurement falls
*below* the assigned range; the one population fit sits more than twice *above*
it. The assigned consensus sits in neither place, and nothing in that table
tests it.

Two details worth keeping: Shin 2011 is the only entry with a sex-specific Vd
(181 male, 198 female), and Gomis 2017's 200 mL/kg is explicitly an *average of
human and animal* values — a different circularity from Thompson's.

### 5.2 The assumptions that move the number, with directions

1. **Ongoing unmonitored exposure** → inflates half-life. The dominant bias.
2. **Background not subtracted** → inflates, scaling with proximity to
   background (quantified in §4.5).
3. **Isomers pooled** → not one-directional. Xu 2020 has every branched PFOS
   isomer faster than linear; Nilsson 2022b has branched slower; Rosato's pooled
   1m-PFOS is 5.86 y against L-PFOS 3.13 y.
4. **Which average** → AM vs GM is worth 10–15%; and Lyu 2026 shows
   `ln2/mean(k)` and `mean(ln2/k)` differ by 15–23% in the same data.
5. **Follow-up short relative to half-life** → unstable either way.
6. **Age and sex** → real modifiers. Lewis-Michl 2025 gives a clean 1.8-fold
   gradient within one cohort (1.96 y at 0–17 → 3.55 y at 60+). Paediatric
   estimates exist only from Batzella 2024 (1.64 y) and Lewis-Michl (1.96 y),
   both 30–45% below their adult strata, both cautioning that growth dilution is
   not separated from intrinsic elimination.
7. **Excretion routes counted** → renal-only underestimates clearance, hence
   overestimates half-life. Shi 2016 is the cleanest demonstration: F-53B total
   half-life 15.3 y against a renal-clearance-only 280 y **in the same paper**,
   an 18-fold gap.
8. **The assumed Vd** → scales mass-balance estimates linearly.

### 5.3 The faecal route is contested, not settled

| | Andersson 2025 (matched serum/urine/faeces, n=147) | Abraham 2024 (labelled bolus, n=1) |
|---|---|---|
| PFOS | faeces dominant, **4:1** | **faecal not detected** |
| PFOA | urine ~1.7:1 | faecal 17% of total |
| PFNA–PFDoDA | — | faecal 58–61% |

A candidate resolution neither paper tests: Andersson measured faecal PFOS in
people with ongoing dietary intake, so unabsorbed dietary PFOS passing through
would be scored as elimination — which a fully absorbed labelled bolus cannot
produce. If that is right, corrections to PFOS half-lives based on Andersson's
4:1 are not justified. Cholestyramine trials push the other way (Møller 2024,
n = 45: 63% PFOS lowering in 12 weeks vs 3% control).

**And two further routes appear in no agency's clearance accounting at all.**

*Breastfeeding.* Mondal 2014 (C8 Science Panel, n = 633) finds each month of
breastfeeding lowers maternal serum by **3% for PFOA, 3% PFOS, 2% PFNA, 1%
PFHxS** — and raises the infant's by 6% and 4%. For a woman breastfeeding a
year, that is a third of her PFOA burden leaving by a route no clearance factor
counts. The mother's excretion is the infant's dose.

*Menstrual blood loss.* Upson 2022 reviews the epidemiology: postmenopausal
women carry higher PFAS than premenopausal women, concentrations rise with years
since menopause and with hysterectomy, and a life-stage PBPK bias analysis
reproduces the apparent PFAS–menopause association purely from the loss of this
excretion route.

This matters for §3's framing. The rat sex difference is transporter-mediated
and androgen-driven; the **human** sex difference may be mostly mechanical —
blood leaving the body. Wallis 2023 states the position plainly: sex differences
from hormone-mediated transporters "have not been directly observed in humans."
Two species, two different reasons for the same-looking pattern.

### 5.4 Agencies disagree about clearance more than about half-life

```bash
python3 scripts/agency_clearance_comparison.py
```

| | adopted human clearance factor | spread |
|---|---|---|
| PFOA | 0.059 → 0.280 mL/kg-day | **4.7×** |
| PFOS | 0.016 → 0.390 mL/kg-day | **24×** |

EPA and OEHHA cite the **same** Li et al. half-life studies and land 2.3× apart,
because EPA computes `CL = Vd·ln2/t½` from Thompson's assumed 170 mL/kg while
OEHHA regresses intake against serum directly and states this "obviat[es] the
need for a T½ estimate".

Thompson et al. 2010 is worth knowing about: it is an Australian
exposure-reconstruction paper, and its Vd is *calibrated*, not measured —
`Vd = Dose·t½/(Css·ln2)` using Emmett 2006 serum, an **assumed** 2.3-y
half-life and fa = 0.91. And PFOS 230 mL/kg is literally 170 × 1.35, the 1.35
taken from Andersen 2006's monkey *central-compartment* volumes. EPA then uses
that Vd to compute clearance — circular. The measured value is 121.

Neither **OEHHA 2024 nor EPA 2024 cites Chiu 2022 at all** (verified by grep
over both complete documents, 38,696 and 13,747 lines).

### 5.5 The states agree with each other by repeating one derivation

Adding thirteen US state and further international bodies (261 rows,
`db/state_international_regulatory.csv`) widens the picture rather than
settling it.

```bash
python3 scripts/all_agency_clearance.py   # -> db/all_agency_clearance.csv
```

For **PFOA**, five jurisdictions — New Jersey DWQI, Michigan MPART,
Pennsylvania DEP, the Drexel advisory group that supports it, and New Hampshire
DES — all adopt **0.140 mL/kg-day**. That looks like consensus. It is one
derivation performed five times: every one computes `CL = Vd·ln2/t½` from
**Thompson 2010's Vd of 170 mL/kg** and **Bartell 2010's 2.3 y half-life**. The
same pattern repeats for PFOS at 0.128–0.130, where the Vd is Thompson's 230.

Across all 42 adopted values:

| how the number was produced | n |
|---|---|
| renal clearance only | 11 |
| **computed from Thompson 2010's assumed Vd** | **9** |
| animal-derived | 7 |
| adopted wholesale from another agency | 7 |
| measured: intake vs serum at steady state | 4 |
| other or unstated | 4 |

Recall from §5.4 what Thompson's Vd actually is: *calibrated* from two US water
communities using an **assumed** 2.3-year half-life, not measured. So the
apparent agreement among states is not independent confirmation — it is one
assumption propagating, and §5.1a shows the measured Vd is 121 mL/kg, not 170.

The jurisdictions that do **not** use it diverge sharply, and in both
directions: OEHHA's measured intake-vs-serum clearance is ~2× the
Thompson-derived cluster, while its renal-clearance-only figure is 2–8× below
it. **Minnesota MDH is the one state that broke ranks**, adopting OEHHA's
0.280/0.390 wholesale and landing twice as far from its neighbours as any
methodological disagreement between them.

Two further observations worth recording:

- **New York derived its PFOA clearance (0.092) from Macon et al. 2011, a mouse
  study.** Using animal data to set a human clearance factor is a different kind
  of assumption from the others here.
- **Four states set their human PFHxS clearance (0.086–0.090) from Sundström
  2012's cynomolgus monkey Vd.** The human PFHxS factor in Michigan, Minnesota,
  New Hampshire and New York rests on a monkey volume of distribution.
- The extraction also caught an apparent error: **ITRC's PFOS entry uses
  Bartell 2010's 840-day half-life, which is the PFOA value.** Recorded as
  found, not corrected.

---

## 6. In vitro binding to albumin and related proteins

`db/protein_binding.csv` — 273 rows, 54 studies, 30 protein targets, 272 with a
DOI, computational values flagged.

```bash
python3 scripts/build_binding_table.py
# -> db/binding_summary_ka.csv (association constants)
# -> db/binding_summary_logD.csv (protein/water distribution)
```

### 6.1 A single affinity number for a PFAS–protein pair does not exist

| chemical | protein | n | Ka range (M⁻¹) | spread |
|---|---|---|---|---|
| PFBS | HSA | 4 | 116 – 6.5 × 10⁶ | 55,800× |
| PFBA | HSA | 3 | 20.4 – 1 × 10⁶ | 49,100× |
| PFOA | HSA | 6 | 103 – 1.98 × 10⁶ | 19,200× |
| PFOA | BSA | 6 | 322 – 1 × 10⁶ | 3,110× |
| PFOS | BSA | 4 | 1.16 × 10³ – 2.44 × 10⁵ | 210× |

**The spread is not fluorescence-versus-dialysis.** Equilibrium dialysis alone
spans 3.2 × 10² to ~10⁶, and fluorescence quenching spans 10² to 2 × 10⁶ by
itself. The drivers are the **ligand:protein ratio regime** and the **fitting
model**: Alesio & Bothun 2022 obtained Ka from 0.07 to 6.16 × 10⁶ M⁻¹ from a
*single dataset* using three models. Differential scanning fluorimetry is
systematically low and its own authors say so, because Kd comes off a thermal
ramp rather than 37 °C.

Reported stoichiometry is a titration curve read at five points, not a
disagreement: n ≈ 1 (quenching), 1–3 (low-ratio dialysis), 6–9 (microdesalting),
8 (nanoESI-MS at 4:1), 45 (dialysis at 1.2 mM). **Physiological PFAS:albumin is
≤ 0.0005**; most in vitro work runs three to six orders of magnitude above it.

*Any table printing one number per pair is misleading. Use the range.*

### 6.2 The one dataset measured at a realistic ratio

Fischer et al. 2024 (solid-phase microextraction, PFAS:protein ≤ 0.004), log
D_protein/water in L_water/kg:

| chemical | HSA | γ-globulin |
|---|---|---|
| PFHxA | 3.20 | 1.73 |
| PFHpA | 4.10 | 1.81 |
| PFOA | 4.48 | 2.16 |
| PFNA | 4.49 | 2.81 |
| PFDA | 4.73 | 3.67 |
| PFHxS | 4.77 | 1.95 |
| PFOS | 4.62 | 3.33 |

Albumin dominates below ~7 perfluorinated carbons (D_glob/D_HSA < 0.1 for
MW < 500) and globulins catch up as the chain lengthens, reaching parity around
ηpfc 12–13.

Measured serum unbound fractions: **PFOA 0.061%, PFOS 0.042%, PFHxS 0.041%,
PFHpS 0.035%** — with interindividual variation of only 1.6–2.5×. These conflict
~100× with Han et al. 2003's ">90% bound" (f_unbound < 10%), so **older PBPK
models parameterised on Han carry an f_unbound roughly 100× too high.**

### 6.3 Binding does not explain the species difference

Two results settle this, and both are negative:

- **Starnes 2024** (Table 5): rat albumin binds PFOA ~2× *more* tightly than
  human albumin, while the rat half-life is ~1000× *shorter*. Wrong direction,
  wrong magnitude.
- **Han et al. 2004** explicitly reject α2u-globulin (Kd ~10⁻³ M) as the cause
  of male-rat PFOA retention — the authors of the α2u-globulin paper in your
  own citation list.

Also worth knowing: PFAS bind albumin at only **2–10% the affinity of
similar-chain fatty acids** (Hebert & MacManus-Spencer 2010), so nearly all in
vitro work uses fatty-acid-free albumin while in vivo binding competes against a
higher-affinity endogenous excess.

PFOA's albumin site is genuinely contested — crystallography puts the
high-affinity site in subdomain IIIA (Maso 2021) while warfarin displacement
puts it at Sudlow site I (Peng 2024, 96.1% reduction; Chen 2015). PFOS is
consistent across methods (FA3/4 + FA5, PDB 4E99).

---

## 7. Transporters: direction first, then kinetics

`db/transporter_kinetics.csv` — 217 rows, 27 studies, 48 transporter entities.

**Direction decides the sign of every inference:**

- **Reabsorptive (lengthen half-life):** rat Oatp1a1 (apical), human OAT4,
  human URAT1, ASBT; NTCP/OSTα-β on the enterohepatic loop. Weaver 2010:
  *"Oatp1a1 is the major player in the reabsorption of PFCAs."*
- **Secretory (shorten half-life):** OAT1, OAT3 (basolateral uptake into the
  tubule cell), and the apical pumps P-gp and BCRP.

Representative measured Km, from primary tables:

| transporter | species | PFAS | Km (µM) | source |
|---|---|---|---|---|
| Oatp1a1 | rat | PFOA / PFNA / PFDA | 126.4 / 20.5 / 28.5 | Weaver 2010 Tables 1–2 |
| Oatp1a1 | rat | PFOA | 162.2 | Yang 2009 |
| OAT1 / OAT3 | human | PFOA | 48.0 / 49.1 | Nakagawa 2008 |
| OAT1 / OAT3 | rat | PFOA | 51.0 / 80.2 | Nakagawa 2008 |
| OAT4 | human | PFOA | 172.3 (pH 6) / 310.3 (pH 7.4) | Yang 2010 |
| URAT1 | human | PFOA | 64.1 | Yang 2010 |
| OAT4 | human | 6 PFAS | 39–92 | Louisse 2023 Table 1 |

Three conflicts left open rather than silently resolved: Louisse 2023 found
**URAT1 transported nothing**, contradicting Yang 2010; Argoul 2026 reports
PFDA/PFOS as substrates of nothing, against both Louisse and Weaver; and
Cheng 2006's abstract calls renal Oatp1a1 "female-predominant", contradicting
Cheng 2005 and its own androgen conclusion.

**Two numbers that must not be cited as transporter measurements.** Worley &
Fisher's rat PBPK required a *fitted* male/female apical activity ratio of
~25,800×, and Loccisano (PFOA) and Kim (PFHxS) both report Tm/KT sex ratios of
exactly 91×. These are scalars absorbing an observed clearance difference, not
measurements of transporter expression. Relatedly, EPA's own two documents give
the rat male/female Oatp1a1 mRNA ratio as 2.5-fold and as 5–20-fold, and neither
traces to Kudo 2002's abstract — **no single fold-value should be quoted without
the primary full text.**

---

## 8. What this review corrects in the existing repository

1. **`SYNTHESIS.md`'s reconciliation of Zhang 2013 does not survive.** It
   rescales Zhang's clearance with Chiu's *fitted* Vd of 430 mL/kg, gets 3.29 y,
   and concludes Zhang and Chiu "agree to within 5%". Abraham's **measured**
   121 mL/kg gives ≈0.93 y instead. The reconciliation was an artefact of
   choosing the largest published Vd.
2. **Zhang 2013's headline PFOA numbers are 2.1 y (young females) and 2.6 y
   (males/older females), arithmetic means** — not the 1.3 y GM currently in
   `studies.csv`. Zhang's own Discussion says the value "is similar to the actual
   PFOA serum elimination half-lives reported for highly exposed populations
   (i.e., 2.3 or 2.9 years)". The short-half-life argument built on 1.3 y is
   weaker than the existing files imply.
3. **Zhang 2013 and Andersson 2025 give transposed values for Thompson 2010's
   Vd** (170/230 vs 230/170 for PFOA/PFOS). Thompson needs reading directly
   before any further rescaling.
4. **The `APPRAISAL.md` framing of Vd** treats Chiu's 0.43 L/kg as the
   comparator against "commonly assumed" 0.17–0.20. Abraham's measurement
   supports the assumed values, not the fitted one.
5. **An earlier claim in this session was overstated.** I reported that
   OEHHA's implied Vd (398 mL/kg) and Chiu's fitted Vd (430) were a convergence
   of two independent routes. They are not independent: Chiu's clearance and
   OEHHA's clearance agree, so at a common half-life they necessarily imply a
   common Vd. The real finding is agreement on *clearance*, and Abraham
   disagrees with both by 6.7×.
6. **`species_exposure.csv` mixes time units silently** — Chiu's human
   half-lives in years, EPA animal fits in days, no units column.
   `db/master_exposure_halflife.csv` carries an explicit `native_time_unit`.
7. **EPA's PFHxA human Vd is wrong by 6.1×** — it assumed human Vd = monkey Vd
   = 730 mL/kg; the measured human value is 119. EPA's *reasoning* (Vd roughly
   conserved across mammals) is vindicated; its number is not.

---

## 9. What nobody knows

### 9.0 The shape of the hole, measured

Before the specific gaps, the general one. Merging every extraction in `db/`
onto a single grid of chemical × species × parameter, and counting *distinct
studies* per cell:

```bash
python3 scripts/build_coverage_matrix.py   # -> db/coverage_matrix.csv
```

| | cells | share |
|---|---|---|
| two or more studies | 131 | 11% |
| **a single study only** | **101** | **8%** |
| **no data at all** | **1,000** | **81%** |

28 chemicals × 11 species × 4 parameters = 1,232 cells. **Four fifths are
empty.** Even PFOS, the best-covered compound in the world, fills 28 of its 44
cells; PFOA 25.

Coverage collapses away from four compounds and two species. PFOA, PFOS, PFHxS,
PFBS, PFBA and PFHxA account for most of what exists. The replacement
chemistries that are displacing them — HFPO-DA aside — are nearly empty:
6:2 Cl-PFESA has 2 of 44 cells, cC6O4 2, ADONA 3, and the diPAPs 1 each.

Two late additions moved cells without changing that picture. **EFSA 2020
Appendix C** (`scripts/parse_efsa_appendix_c.py`, 109 records) carries mouse
clearance and Vd for PFUnDA, PFDoDA, PFTrDA and PFTeDA from Fujii 2015 that
appear nowhere else, and deepened twelve cells from single-study to corroborated
— but opened none that were empty. Three of its rows were **refused** rather
than parsed: the web rendering lost `<br>` separators, so the PFOS row offers 18
half-lives against 20 doses, with one cell merging three values and another
repeating one. Aligning those would have meant guessing which half-life belongs
to which dose.

And **Wallis 2023** supplies what are, in its own words, "the first and possibly
only estimates of human elimination half-lives" for three fluoroethers, from the
GenX Exposure Study after Cape Fear discharges were controlled:

| compound | human half-life | 95% CI |
|---|---|---|
| PFO4DA | 127 d | 86–243 |
| Nafion byproduct 2 | 296 d | 176–924 |
| PFO5DoA | 379 d | 199–3,870 |

These sit between the short-chain carboxylates (PFHxA ~32 d, PFHpA ~62 d) and
the long-chain PFAAs (800–1,200 d) — consistent with ether oxygens shortening
half-life, which is the design rationale for the replacement chemistries. They
are the only human numbers testing it, from 44 people and two blood draws, and
the widest interval spans twentyfold. (Note a transcription error in the paper
itself: its Results text repeats Nafion byproduct 2's confidence interval for
PFO4DA; the abstract's 86–243 is the consistent one.)

This is the context for every ratio in this report. **When a cell holds one
study, a headline number is that study**, which is how the 31× mouse/rat PFOA
ratio came to rest on Lou 2009 alone (§3.2).

### 9.1 Specific gaps

Ranked by how much a single experiment would settle.

1. **No sex-resolved mouse PFOA half-life pair has ever been measured.** The
   31× mouse/rat ratio that frames this whole question depends on it. This is
   the single cheapest decisive experiment in the review.
2. **No study has measured renal Oatp1a1 protein in rat and mouse side by
   side**, and no Slco1a1-null animal has been dosed with PFAS. Without these
   the rat-vs-mouse mechanism cannot be closed. **No mouse transporter kinetics
   exist for any PFAS**, with any transporter.
3. **Abraham 2024 at a second dose level in the same volunteer** would settle
   human PFOA concentration-dependence outright, and would resolve whether the
   6.7× clearance disagreement is a dose effect or an individual.
4. ~~No controlled-removal study reports a Vd~~ — **done, §5.1a.** The
   Gasiorowski 2022 reanalysis gives PFOS 113–199 and PFHxS 71–187 mL/kg,
   bracketing Abraham's measured values and excluding Chiu's fitted ones. What
   remains open is *why* a population model needs a Vd two to four times the
   measured one to reproduce observed serum trajectories.
5. ~~Li 2022's tertile analysis re-run with age adjustment~~ — **done, §4.6.**
   The adjusted answer was already published as partial R² in Table S14:
   initial level is the weakest of six determinants for all eight compounds.
6. **Rat-vs-mouse tissue partition coefficients for PFOA/PFOS** are missing, as
   is any rat-vs-mouse biliary comparison under a common protocol. MRP4 appears
   never to have been tested for PFAS.
7. **Huang 2021's corrigendum content is unobtainable**, so which NTP numbers
   were corrected is unknown; affected rows are flagged.

### Three standing caveats on the animal data

- **"Mouse" means CD-1.** Every mouse PK dataset retrieved is CD-1, and Buist
  2004 found the *direction* of renal Oat3 sex bias differs between 129J and
  C57BL/6. Mouse renal transporter sex bias is not a species constant.
- **Transporter abundance is not a fixed parameter in these studies.** PFAS
  downregulate their own transporters: PFOA cuts hepatic Oatp1a1/1a4/1b2 and
  PFDA cuts all four while raising serum bile acids 300%, PPARα-dependently
  (Cheng & Klaassen 2008).
- **Non-linearity is not confined to the female rat.** Mouse PFOA is non-linear
  above ~40 mg/kg single or 5 mg/kg/d; mouse PFNA is non-linear while rat PFNA
  is linear. Fits dominated by high-dose data "would overestimate PFAS clearance
  at environmentally relevant doses" — the EPA animal PK authors' own warning
  about the dataset this review leans on.

---

## 10. The practical summary

**For a central human estimate**, Rosato 2024's pooled general-population PFOA
figure of 2.35 y (2.20–2.51) remains the best anchor — explicit cessation
criterion, risk-of-bias scoring, and the subgroup where studies actually agree
(I² = 43%). Batzella 2024 (n = 5,860, 2.36 y, 2.33–2.40) now corroborates it
from a cohort 29× larger than anything prior.

**For dosimetry**, the clearance factor matters more than the half-life, and it
is the least settled quantity in the field: 4.7× spread for PFOA, 24× for PFOS
across agencies. State which you used and why.

**For the species question**, the answer is renal handling, and dose is not a
competing explanation at any exposure humans experience.

**For in vitro binding**, report ranges and the ligand:protein ratio, never a
single Ka.

---

## Appendix: the databases

| file | rows | what it answers |
|---|---|---|
| `source_catalogue.csv` | 81 | your citation list, PMID-verified and classified |
| `exposure_vs_halflife.csv` | 184 | chemical, serum, exposure, half-life on one line |
| `master_exposure_halflife.csv` | 46 | dose/serum/half-life/Vd/CL per species × sex |
| `human_halflife_extended.csv` | 142 | human estimates with design and modelling assumptions |
| `regulatory_values.csv` | 173 | what each agency adopted, from which study, under which assumptions |
| `agency_clearance_comparison.csv` | 16 | clearance factors normalised to mL/kg-day |
| `protein_binding.csv` | 273 | in vitro binding, with method and ratio regime |
| `binding_summary_ka.csv` | 71 | association constants, as ranges |
| `binding_summary_logD.csv` | 111 | protein/water distribution at realistic ratio |
| `transporter_kinetics.csv` | 217 | Km/Vmax/IC50 with reabsorption-or-secretion direction |
| `transporter_mechanism.csv` | 83 | expression, hormonal regulation, species comparison |
| `animal_halflife_measured.csv` | 217 | measured animal half-lives by strain, sex, dose, route (187 measured, 30 flagged modelled) |
| `vd_clearance.csv` | 143 | Vd by species, flagged measured/fitted/assumed, with provenance |
| `dose_dependence.csv` | 32 | multi-dose studies, half-life at each level |
| `mouse_rat_decomposition.csv` | 14 | the species gap split into Vd and CL terms |
| `sex_decomposition.csv` | 21 | the same split for the sex difference |
| `reabsorption_axis.csv` | 5 | renal reabsorption and the half-life it predicts |

Figures in `figures/`; retrieval logs in `papers/SOURCES_*.md`; per-subtopic
research notes in `research_notes/`.
