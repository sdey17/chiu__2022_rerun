# State and national regulatory documents: toxicokinetic extraction

Companion to `db/state_docs_extraction.csv`. Every row in that CSV records both the
primary study cited and the regulatory document it was read from, plus an explicit
DERIVED / COMPUTED / ADOPTED tag.

## 1. NY DOH 2022 (emerging contaminant notification levels + PFHxS/PFHpA/PFNA/PFDA MCLs)

Source: `papers/NY DOH 2022 emerging contaminant notification levels PFAS.txt` (15,967 lines;
most of the file is DWQC meeting transcript with no TK content. All TK is in lines ~6630-7520.)

**Structure of NY's use of toxicokinetics.** NY uses TK in two completely separate ways:

1. *As a hazard-prioritization criterion* (Tables 2 and 3). Human half-life is one of four
   criteria used to sort 19 emerging PFAS into a prioritized 30 ppt notification level and a
   second, higher category. No dose-response arithmetic; half-life is used purely
   qualitatively ("multiple years" = prioritized, "approaching one year" = not).
2. *As a dosimetric bridge* in the four chemical-specific MCL derivations (PFHxS, PFHpA,
   PFNA, PFDA), where a single chemical-specific human clearance factor converts an animal
   point-of-departure serum concentration into a human equivalent dose.

**The three clearance values, and who derived them:**

| Chemical | Clearance (mL/kg/day) | POD serum (ng/mL) | HED (ng/kg/day) | Critical study | Derived by |
|---|---|---|---|---|---|
| PFHxS | 0.086 | 13,900 | 1,200 | Chang et al. 2018 (mouse) | NH DES 2019 - NY ADOPTED |
| PFOA (applied to PFHpA) | 0.092 | 4,980 | 460 | **Macon et al. 2011 (mouse)** | **NYS DOH 2018 - NY's own** |
| PFNA (applied to PFDA) | 0.098 | 6,800 | 665 | Das et al. 2015 (mouse) | MI SAW 2019 - NY ADOPTED |

**The Macon et al. 2011 point of interest.** NY's PFOA reference dose (1.5 ng/kg/day, derived
by NYS DOH in 2018 and re-presented in 2022 as the basis for the PFHpA MCL) rests on a
**mouse** developmental study: increased relative liver weight in the offspring of mice dosed
on gestational days 1-17. The measured serum level at the LOEL (4,980 ng/mL) is converted with
a *human* clearance of 0.092 mL/kg/day, then divided by UF 300 (10 sensitive humans x 3
interspecies x 3 LOEL-to-NOEL x 3 database). This is unusual on two counts: (a) a mouse rather
than rat or human critical study for PFOA, and (b) serum-concentration equivalence is assumed
across species (mouse serum level = human serum level of concern) with the interspecies
uncertainty factor reduced to 3 on that basis.

**What the document does NOT say.** The NY document never states a volume of distribution,
never states which human half-life was used, and never cites a primary source for any of the
three clearance values. The three values (0.086, 0.092, 0.098 mL/kg/day) are suspiciously close
together, which is what one expects if each was computed as ln2 x Vd / t-half with a common
assumed Vd of roughly 0.2 L/kg and chemical-specific human half-lives - but that inference
cannot be checked from this document. Anyone needing the Vd must go to NH DES 2019, MI SAW 2019
and NYS DOH 2018 respectively.

**Internal inconsistency.** The PFNA RfD narrative uses the Michigan SAW HED of 665 ng/kg/day
(developmental delays, 6,800 ng/mL NOAEL). But Table 7 (margins of protection) uses an
NJ DEP 2015 HED of 431 ng/kg/day for maternal relative liver weight from the same Das et al.
2015 study. Two agencies' dosimetric conversions of one study sit in the same document.

**Rejections and conflicts.**
- GenX: short human half-life (81 h, US EPA 2021a using Clark 2021 data) was explicitly NOT
  treated as grounds for de-prioritization, because the liver effect level (0.5 mg/kg/day) and
  RfD (3 ng/kg/day) were low. GenX received its own 10 ppt level.
- PFPeS: half-life 223-365 days, "approaching one year, rather than multiple years", was the
  stated reason for placing it in the higher (less stringent) category.
- PFDoA, 11Cl-PF3OUdS, 4:2 and 8:2 FTS: no TK data at all; assigned by structural read-across.

**Species comparison.** The only cross-species TK statement is in Table 3 footnote b: rat
half-lives of 2-13 hours for short-chain PFAS versus "weeks to months" for long-chain
(ATSDR 2021), used to place 6:2 FTS (rat 20-24 h, ECHA 2020) with the short-chain PFAS when
no human half-life existed. **There is no discussion anywhere in the NY document of
rat-versus-mouse differences, of sex differences, or of the female-rat phenomenon** - notable
given that every one of NY's four critical studies is a mouse study.

**Not captured in the CSV** (exposure factors, not TK): drinking water ingestion rates
0.035 L/kg/day (adults), 0.047 (lactating women), 0.143 (infants); relative source
contribution 0.5 (NY departs from the EPA default of 0.2, citing NJ DEP, NH DES and others).

> **Cross-document resolution of the NY clearance values (found while working WA DOH 2021).**
> WA DOH's Table 9 footnote d gives the NHDES PFHxS DAF as `8.61 x 10-2 mL/kg-day`, assuming a
> human serum half-life of 1,716 days for *women* (Li et al. 2018) and Vd = 0.213 L/kg. That is
> NY's 0.086 mL/kg/day. WA DOH's Table 8 footnote e gives the Michigan SAW PFNA DAF as
> `0.2 L/kg x ln2/1417 d = 0.978 x 10-4 L/kg-day`. That is NY's 0.098 mL/kg/day. So two of NY's
> three clearance values are fully reconstructible, but only from the WA document, not from NY's.
> NY's own PFOA value (0.092 mL/kg/day) remains unreconstructed; no document in this set gives
> the NYS DOH 2018 inputs.

## 2. WA DOH 2021 (state action levels for PFOA, PFOS, PFNA, PFHxS, PFBS)

Source: `papers/WA DOH 2021 PFAS state action levels approach methods.txt` (4,201 lines).
This is the richest TK document of the state set: it tabulates, side by side, every other US
agency's dosimetric constant for five PFAS *and states the Vd and half-life behind each one*.
It is effectively a concordance for the whole US state-level PFAS dosimetry literature.

### Two distinct dosimetric architectures

| | PFOA, PFOS, PFHxS, PFNA | PFBS |
|---|---|---|
| Form of the adjustment | `DAF = Vd x ln2 / t-half` (L/kg-day) | half-life ratio or clearance ratio (dimensionless) |
| What it converts | animal **serum** POD -> human dose | animal **administered dose** -> human dose |
| Depends on an assumed Vd | yes | no |

Nobody in the state set seems to remark on this, but it matters: the four long-chain PFAS
standards are all hostage to a volume of distribution that no agency re-derives, while the PFBS
standards are hostage to a mouse half-life that two agencies disagree about by a factor of two.

### WA's transgenerational model (adopted from MDH 2019)

Serum = dose / clearance rate, with clearance rate = Vd x ln2/t-half. WA retained MDH's
half-life, Vd, placental and breast-milk transfer ratios wholesale (PFNA inputs from Michigan
DHHS). The model inputs are in the CSV; the headline numbers:

| | PFOA | PFOS | PFHxS | PFNA |
|---|---|---|---|---|
| half-life (y) | 2.3 | 3.4 | 5.3 | 3.5 |
| Vd (L/kg) | 0.17 | 0.230 | 0.25 | 0.20 |
| placental transfer | 0.87 | 0.40 | 0.70 | 0.69 |
| breast-milk transfer | 0.052 | 0.017 | 0.014 | 0.032 |

Placental and breast-milk transfer rank differently: carboxylates (PFOA 0.052, PFNA 0.032)
reach milk far better than sulfonates (PFOS 0.017, PFHxS 0.014), while PFOA also has the
highest placental ratio and PFOS the lowest. Both sets of ratios trace only to MDH's 2019
compilation; no primary citations are given, so provenance stops there.

Also worth having: an **age adjustment factor applied to Vd**, 2.4 in newborns falling to 1.0
after one year, justified by extracellular water as a fraction of body weight. This is a rarely
captured parameter and it is doing real work - it raises newborn clearance 2.4-fold.

### Disagreements between agencies, with WA's adjudication

- **PFOA half-life.** EPA used 2.3 y (Bartell 2010, n=200, mixed sex, drinking water); ATSDR
  used 3.8 y (Olsen 2007, n=24, mostly male retired workers) on the stated ground that longer
  follow-up better captures initial and terminal elimination. WA records the counter-argument
  in full but adopts the ATSDR MRL anyway - for its endpoint, not its TK. Resulting clearance
  factors: EPA 1.39e-4, ATSDR 0.99e-4, NHDES 1.49e-4 L/kg-day. A 1.5-fold spread.
- **PFOS half-life.** EPA/ATSDR used Olsen 2007 (5.4 y in EPA's hands); MDH/NHDES/WA used
  Li et al. 2018 (Ronneby, 1,241 d). WA's rationale for the switch is explicitly about
  *population structure*: Ronneby was a drinking-water exposure with all ages and 53 % women,
  "better suited to our transgenerational model". Clearance factors 8.1e-5 (EPA, NJ, CA) vs
  1.28e-4 (MDH, NHDES, WA) - a 1.6-fold divergence in the PFOS dosimetric constant alone.
- **Transcription error to be aware of:** Table 6 footnote e states the PFOS Vd as
  "0.023 L/kg (EPA, 2016)". The narrative for the same derivation says 0.23 L/kg, and only
  0.23 reproduces the stated DAF (0.23 x ln2/1241 = 1.284e-4). The footnote is a typo.
- **PFNA half-life - the sex-stratum dispute.** All of ATSDR, NHDES and Michigan SAW used the
  same study (Das et al. 2015), the same Vd (0.2 L/kg) and the same half-life paper
  (Zhang et al. 2013), yet produced DAFs spanning 1.74-fold, purely by choosing which *sex/age
  stratum's* half-life to use:
  - ATSDR: 900 d (women of reproductive age, 2.5 y) -> 1.54e-4. Rationale: the POD is
    developmental, so match the half-life to women at the time of pregnancy. Note this makes
    the MRL *less* protective.
  - NHDES: 1,570 d (men and women >50, 4.3 y) -> 0.883e-4. Rationale: the POD is a liver
    endpoint applying to the whole population.
  - Michigan SAW: 1,417 d, described as the arithmetic mean -> 0.978e-4. **This does not
    reproduce:** the mean of 913 and 1,570 d is 1,241 d (3.4 y), not 1,417 d (3.9 y).
  - WA then rejected all of them for **Yu et al. 2021** (1,285 d, NJ community, three annual
    serum measurements, 68 most exposed participants) and did its own arithmetic:
    `0.2 x ln2/1285 = 1.08e-4 L/kg-day`, giving 2.5 ng/kg-day. **Yu et al. 2021 found no
    statistically significant difference between younger women and older women/men**, which
    retrospectively dissolves the whole ATSDR-vs-NHDES stratum argument. This single change
    moved WA's PFNA action level from 14 to 9 ng/L.
- **PFHxS Vd and half-life.** ATSDR 8.5 y / 0.287 L/kg (implied DAF 6.4e-5); NHDES 4.7 y
  (female, Li 2018) / 0.213 (DAF 8.61e-5); MDH 5.3 y / 0.25 (DAF 9.0e-5). WA adopted MDH's.
- **PFBS mouse half-life.** Lau et al. 2020 says 4.5 h in female mice; Rumpler et al. 2016
  (plus *personal communication with C. Lau, 2017*) says 2.1 h. EPA used the former with Xu
  2020's human half-life (1,050 h) for DAF 233; MDH/Michigan used the latter with Olsen 2009's
  human half-life (665 h) for DAF 316.6; CA OEHHA used a clearance ratio instead,
  1344/3.90 mL/kg-day = 345. WA adopted EPA's. Note the entire California and Michigan PFBS
  human dosimetry rests on Olsen et al. 2009: **six workers, five men and one woman**,
  individual half-lives 13-46 days.

### Rat versus mouse, and the female-rat phenomenon

This document contains the single clearest statement of the female-rat phenomenon in the whole
state set (PFHxS Discussion of Uncertainties, citing Sundstrom et al. 2012):

> "Female rats have been shown to have a much shorter serum elimination half-life for PFHxS
> (~2 hours) compared to serum half-lives of one month in male rats and male and female mice."

That is roughly a 350-fold sex difference *within the rat*, with **no** corresponding sex
difference in the mouse. WA deploys it as a toxicokinetic defence of a mouse finding against
negative rat studies: Chang et al. 2018 found reduced litter size in mice, Butenhoff et al. 2009
and Ramhoj et al. 2018 found none in rats, and WA attributes the discrepancy to "lower serum
levels in the rat studies". WA nevertheless declines to use the mouse endpoint, asking for
replication, and adopts the male-rat thyroid POD instead. NTP 2019 independently confirms the
phenomenon - male rat serum PFHxS "much higher than in females reflecting the faster excretion
of PFHxS by female rats" - and the POD WA uses comes from the *male* rats, i.e. the accumulating
sex.

Counterexample worth keeping: for **PFBS** there is no rat-mouse difference at all. MDH's own
numbers give the female Sprague-Dawley rat 1.9 h and the female mouse 2.1 h. The female-rat
phenomenon is chemical-specific, not a general rodent property.

Other species findings:
- **PFOA, Loveless et al. 2006.** Male rats less sensitive than mice for relative liver weight
  (rat LOEL 1 mg/kg-day at serum 48-65 mg/L; mouse LOEL 0.3 mg/kg-day at serum 10-14 mg/L).
  Because rat serum at the rat LOEL was 4-5x *higher*, this is a genuine toxicodynamic
  difference, not a dosimetric artefact. The rat was also insensitive to PFOA immunotoxicity.
  In the rat, declining serum lipids were more sensitive than liver weight.
- **PFOS sex difference in humans:** men eliminate more slowly than women. WA uses this in the
  relative source contribution (20 % for all adults) rather than in the dosimetry.
- **Human vs mouse PPAR-alpha:** the stated reason EPA, ATSDR and (for PFNA) ATSDR all moved
  off mouse liver endpoints, applying the Hall et al. 2012 adversity criteria.

### Rejections

- **van Esterik et al. 2016** (PFOA, reduced female pup weight at 0.01 mg/kg-day) could not be
  used quantitatively by CA OEHHA **because serum was not measured** - internal dose could not
  be confirmed. It became a 3-fold database UF instead. A toxicology study rejected for a purely
  toxicokinetic reason.
- **Singh and Singh** PFNA male-reproductive studies in Parkes mice likewise unusable: "Without
  an indication of internal dose or more information about toxicokinetics of PFNA in this strain
  of mice, the study results are not suitable for dose-response modelling."
- **PFBS lactational modelling rejected outright.** WA could not run the MDH model for PFBS:
  PFBS was detected in fewer than half the breast-milk studies MDH found, and cord blood PFBS
  did not correlate with paired maternal serum (Wang et al. 2019). No placental or breast-milk
  transfer factor could be assigned, so WA fell back on a 95th-percentile infant water intake of
  0.174 L/kg-day and a default RSC of 0.2.
- **Mouse liver weight at low dose** rejected as a POD by EPA and ATSDR under the Hall criteria.

## 3. Health Canada 2016 PFOS drinking water consultation document - THE PRIMARY

Source: `papers/Health Canada 2016 PFOS drinking water consultation document.txt` (1,745 lines).
This project previously held Health Canada's PFOS clearance only second-hand through OEHHA.
**Settled: the Health Canada human PFOS clearance is 0.07 mL/day-kg (7e-5 L/kg-day).** Section
8.6.1 states the derivation in full:

```
CL_human = ln2 x Vd / t-half = ln2 x 200 mL/kg / 1971 days = 0.07 mL/day-kg
  Vd       = 200 mL/kg, ASSUMED, "to represent a chemical that is mostly
             distributed extracellularly" (supported by Thompson et al. 2010,
             that PFOS Vd is relatively consistent across species)
  t-half   = 1971 days (5.4 y), Olsen et al. 2007, 26 retired fluorochemical
             workers; 95 % CI 3.9-6.9 y; individual range 2.4-21.7 y
```

Two things make this the document to cite rather than any downstream source:

1. **It says the Vd is an assumption.** Health Canada writes plainly that clearance was not
   measured in humans and must be back-calculated, and that 0.2 L/kg was chosen on physiological
   reasoning about extracellular distribution. Every US state value of 0.2 L/kg rests on the same
   assumption, usually without saying so. (Historical note the document also preserves: Tan et al.
   2008 fitted a *time-dependent* Vd to high-dose monkey and rat data; Loccisano et al.
   subsequently **removed** the time dependency. The constant Vd is a modelling simplification.)
2. **It is almost identical to EPA 2016's 8.1e-5 L/kg-day** - because both use the same Olsen 2007
   half-life. The entire Canada/US difference in the PFOS dosimetric constant is Vd: 0.20 vs 0.23
   L/kg. Note too that Minnesota DOH's 2008 monkey-based HED implies 2500/35,000 = 0.0714
   mL/kg-day, i.e. the same number again.

### Health Canada does NOT use the clearance for its standard

This is the part that gets lost in second-hand citation. The clearance-ratio AKUFs were
**computed and then rejected**. Health Canada's chemical-specific interspecies toxicokinetic
factor (AKUF, replacing the IPCS 2005 default of 4.0 = 10^0.6, with 2.5 = 10^0.4 left for
toxicodynamics) was ultimately taken from **PBPK model ratios of steady-state plasma PFOS**.

| | monkey | mouse | male rat | female rat |
|---|---|---|---|---|
| Clearance (mL/day-kg), Chang et al. 2012 | 1.38 | 4.72 | 22.24 | 5.39 |
| **Clearance-ratio AKUF** (computed, then rejected) | 19 | 67 | **318** | 77 |
| PBPK AKUF at 0.001 / 0.01 / 0.1 / 1 mg/kg-day | 2/2/3/2 | NC/NC/21/3 | 16/14/10/1 | - |
| **AKUF actually applied** | **4** (IPCS default) | rat values | **14** (non-cancer), **10** (cancer) | - |

Why the clearance ratios were rejected: they rely on single values per species, cannot represent
non-linear kinetics, are dose- and regime-dependent (animals got single doses, humans were never
dosed), and are "ratios of low doses in humans to high doses in animals, and therefore exposures
between the species are not of the same magnitude". The PBPK approach compares matched doses and
yields a **dose-dependent** AKUF - the rat AKUF falls from 16 at 0.001 mg/kg-day to **1** at
1 mg/kg-day, i.e. at high dose rat and human reach the same steady-state plasma level. That dose
dependence *is* the saturable renal resorption, made visible.

Three overrides worth recording:
- Monkey PBPK AKUF (2-3) **not used**; the default of 4 was kept "due to insufficient confidence
  in the models to apply value lower than default". A rare case of an agency declining a
  chemical-specific factor because it would be *less* protective.
- Mouse PBPK AKUF **not used**; no PBPK model exists for the mouse (the rat model was merely
  scaled with mouse data), so "AKUF values for rats will be applied".
- "AKUF values for rats are also derived based on male rats only, despite sex differences in the
  species." The applied factor of 14 is a **male-rat** factor.

Health Canada also **rejected using the PBPK model to compute PODs directly**, which it calls the
most robust approach in principle, because the human model cannot be verified: there are no
controlled human dosing data, only biomonitoring at one or two timepoints. Confidence is medium
for human/monkey/rat and low for mouse.

Final arithmetic: non-cancer TDI 0.00006 mg/kg-day = (rat NOAEL 0.021, purity-adjusted, / AKUF 14)
/ UF 25, where UF 25 = 2.5 interspecies **toxicodynamic only** x 10 intraspecies. HBV 0.0006 mg/L.
Supported by a monkey thyroid TDI of 0.0001. Cancer TDI 0.0011 from male-rat BMDL10 0.276 / AKUF 10.

### Rat versus mouse, sex differences, the female-rat phenomenon

**The single most valuable sentence in the whole state/national set** (Section 8.6.1):

> "Clearance was much higher in male than female rats (**and differs from sex-related variability
> for PFOA, where females consistently have increased clearance and lower half-life than males**);
> therefore, clearance levels are presented separately for each sex."

So for PFOS the rat sex difference is **inverted** relative to PFOA: male rats clear 4.1-fold
*faster* (22.24 vs 5.39 mL/day-kg). Set beside WA DOH's PFHxS finding (female rat ~2 h vs male rat
~1 month, i.e. female 350-fold faster) and MDH's PFBS finding (female rat 1.9 h ~ female mouse
2.1 h, no difference), the picture is that **the female-rat phenomenon is chemical-specific in both
magnitude and direction**, not a property of the rat:

| chemical | rat sex difference | direction |
|---|---|---|
| PFOA | female clears faster | classic female-rat phenomenon |
| PFHxS | female ~2 h vs male ~1 month | classic, extreme (~350x) |
| PFOS | **male clears 4.1x faster** | **inverted** |
| PFBS | none (F rat 1.9 h ~ F mouse 2.1 h) | absent |

And in the **mouse** there is essentially no PFOS sex difference at all (M/F half-life ratio
1.13-1.20), confirming the sex effect is a rat-specific transporter phenomenon.

**An internal tension Health Canada does not reconcile.** Table 1 reports, from the *same* Chang
et al. 2012 study, that with >=10-week follow-up the female rat PFOS half-life (62.3 d) is
1.6-fold **longer** than the male (38.3 d) - the same ranking as the clearance values. But at
24-hour follow-up the female half-life is *shorter* (1.94 vs 3.10 d). Half-life estimates from the
same animals span 1.94 to 62.3 days depending on follow-up duration: **a 32-fold protocol
artefact**. Any cross-study comparison of rodent PFAS half-lives has to control for follow-up
length first.

Human sex difference runs the *other* way from the rat: NHANES 1999-2008 shows serum PFOS
significantly higher in males at all ages, attributed to menstrual bleeding plus gestational and
lactational transfer (Harada 2004, Ingelido 2010) - elimination routes with no rodent analogue.
Rat Cmax sex difference is present at 2 mg/kg (female 2.5x male) but **absent at 15 mg/kg**: a
saturable, sex-dependent transport step.

Strain sensitivity: the immune endpoint was excluded from the quantitative assessment partly
because B6C3F1 mice had a LOAEL of 0.00166 mg/kg-day (Peden-Adams 2008) while C57Bl/6 mice had
0.0833 (Dong 2009/2011) and the lone rat study had 3.21 (Lefebvre 2008) - roughly 2,000-fold
mouse-to-rat.

### Other TK parameters captured

- **Oral absorption**: >95 % in rats (consistent across studies). No controlled human study exists.
- **Metabolism**: none. Clearance is entirely renal/biliary; enterohepatic recirculation likely.
- **Renal clearance in humans is substantially lower than in animals** (Harada 2005) - the
  mechanistic basis of the species difference, and the reason every PFOS PBPK model since Andersen
  et al. 2006 is built around saturable renal resorption.
- **Protein binding**: serum albumin principally; lesser binding to gamma-globulin,
  alpha-globulin, alpha-2-macroglobulin, transferrin, beta-lipoproteins. Lipoprotein-containing
  fractions <=9 % (human plasma in vitro, Butenhoff 2012a). Competitive binding to
  **transthyretin at less than one-tenth the affinity of T4** (Weiss 2009) - mechanistically tied
  to the thyroid endpoint used for the monkey TDI. The PBPK models assume **only the free fraction**
  is available for tissue uptake, excretion or resorption.
- **Tissue partitioning, a real species difference**: human liver:serum only 1.3 (cadavers),
  "suggesting there is no extensive binding to liver protein in humans as measured in the rat";
  the rat sequesters PFOS in liver via **L-FABP** (Luebeker 2002), and the rat PBPK model
  accordingly includes *saturable liver protein binding* that the human model does not. Mouse
  liver:blood 2-6; monkey liver:serum 0.9-2.7 (4.4-8.7 % of dose in liver). Human lung:blood 1.5.
  CSF and thyroid are **not** relevant partitioning sites.
- **Placental**: rat fetal/pup serum *and brain* exceed maternal; human cord blood correlates with
  maternal serum; maternal serum falls through pregnancy. Health Canada adopts **no numerical
  placental transfer factor** - contrast WA DOH's 0.40.
- **Breast milk:maternal serum 0.01-0.03** (Liu 2011), which brackets the 0.017 that MDH/WA adopted.
  Milk PFOS falls with each additional infant breastfed. Children average 42 % higher than their
  mothers, persisting to age 19 (Mondal 2012).
- **Time to steady state**: Minnesota DOH estimated **27 years**, and used a time-weighted
  95th-percentile intake over the first 27 years of life (0.049 L/kg-day) as a result.

### Three agencies, three monkey-to-human TK factors for the same compound

US EPA 2009 used 13. Health Canada's clearance ratio gave 19. Health Canada applied 4.

## 4. PA DPAG 2021 (MCLG recommendations + agency comparison workbook)

Sources: `papers/PA DPAG 2021 PFAS MCLG recommendations.txt` (3,313 lines) and
`papers/PA DPAG 2021 PFAS MCLG workbook.txt` (3,344 lines). The workbook is a side-by-side
matrix of every agency's derivation; the recommendations document contains PA's own choices.

PA's Table 2 is the most fully *sourced* version of the Goeden-model parameter set:

| | PFOA | PFOS | PFHxS | PFNA |
|---|---|---|---|---|
| half-life (d) | 840 (Bartell 2010) | 1241 (Li 2018) | 1935 | 1417 (Zhang 2013) |
| Vd (L/kg) | 0.170 (Thompson 2010) | 0.230 (Thompson 2010) | 0.25 (Sundstrom 2012; Ali 2019) | 0.200 (MDH; ATSDR 2018) |
| placental | 0.87 | 0.40 (printed "40") | 0.70 | 0.69 |
| breast milk | 0.052 | 0.017 | 0.014 | 0.032 |

Transfer ratios are identical to WA's, confirming **MDH 2019/2020 as the single origin** of these
ratios for every Goeden-model state (MN, MI, NH, WA, PA). PA differs from WA on exposure, not TK:
**12 months exclusive breastfeeding** (WA: 6 months plus a 6-month phase-out) and 95th-percentile
water intake throughout (WA: 90th after age one), so PA's model delivers roughly twice WA's
lactational dose at the same water concentration.

### PA adjudicates the PFOA half-life the opposite way from ATSDR

> "DPAG selected the PFOA serum half-life of 840 days (2.3 years) (Bartell 2010). This was
> considered more relevant for exposure to the general population than occupational exposure
> studies used by ATSDR."

Then **accepted ATSDR's uncertainty factors (total 300)** while rejecting ATSDR's half-life. The
state documents routinely mix and match components across agencies like this.

PA is also the clearest source on where the PFOA Vd comes from: "the volume of distribution
(Vd = 0.17 L/kg) selected by MDHHS and MDH that was based on human data (Thompson 2010)". Note the
contrast with Health Canada, which cites the *same* Thompson paper only for the claim that Vd is
consistent across species, and then **assumes** 0.2 L/kg.

### Three provenance problems in PA's own Vd citations

1. **PFNA Vd 0.2 L/kg** is attributed in the derivation table to "ATSDR 2018; Ohmori 2003".
   **Ohmori et al. 2003 is a rat study** of perfluorocarboxylate chain-length pharmacokinetics.
   Table 2 of the same document instead credits MDH and ATSDR 2018. So the human PFNA Vd behind
   PA's, Michigan's and (via Michigan) New York's standards traces either to rat data or to an
   assumption, depending which page you read.
2. **PFHxS Vd 0.25 L/kg** gets *three* attributions inside one document: Table 2 says
   "Sundstrom 2012; Ali 2019"; the PFHxS derivation table says "USEPA 2016, Han 2012".
   **Sundstrom et al. 2012 is the comparative rodent PK study** that is the source of the
   female-rat 2-hour PFHxS half-life. A rodent PK paper cited for a human Vd again.
3. **PFHxS DAF**: PA writes the MDH formula (`0.25 x ln2/1935 = 9.0e-2 mL/kg/day`) and then
   substitutes the NHDES number (`8.61e-2`, which corresponds to Vd 0.213 and half-life 1716 d)
   in the arithmetic, landing on NH's RfD of 4.0 ng/kg/day.

### The 1417-day PFNA half-life is a propagated arithmetic error

PA states it explicitly: "The human serum half-lives were an arithmetic mean of 2.5 years
(913 days) for 50 year old or younger females and 4.3 years (1570 days) for females older than 50
years old and all males. An average of 3.9 years (1417 days) was calculated based on those
averages."

The mean of 913 and 1570 is **1241.5 days (3.4 years)**, not 1417 (3.9 y). The mean of the rate
constants would give 1155 days. Neither reproduces 1417. **This is now confirmed in two
independent documents** (PA DPAG 2021 and WA DOH 2021), both describing the same unreproducible
average, so the error originates upstream in MDHHS/Michigan SAW 2019 and has been copied forward
unchecked. The PFNA RfDs of Pennsylvania, Michigan and New York all rest on it. (WA escaped it by
switching to Yu et al. 2021.)

### PA supplies the Health Canada PFOA AKUF - the missing counterpart to the PFOS values

The workbook's Health Canada PFOA entry gives **AKUF = 96** for rats in the 0.01 mg/kg-day band
(PBPK steady-state plasma ratio, residual UFA 2.5). Compare the PFOS document's rat AKUF of 14 at
the same dose band: Health Canada's models imply the rat-human toxicokinetic disparity is nearly
**7-fold greater for PFOA than for PFOS**. Same architecture: dose-specific, male rats only,
interspecies UF reduced to the toxicodynamic component alone.

### Four incompatible kinds of interspecies adjustment now in evidence

| approach | example | magnitude (rodent to human) |
|---|---|---|
| Vd x ln2/t-half (serum POD -> dose) | PFOA clearance 1.4e-4 L/kg-day | n/a (dimensioned) |
| PBPK steady-state plasma ratio | Health Canada PFOA AKUF | 96 |
| half-life or clearance ratio | MDH PFBS DAF | 316 |
| BW^3/4 or BW^1/8 allometry | EPA PFBS DAF 0.149; OEHHA cancer BW^1/8 | ~6.7; ~1.9 |

For the *same* chemical and species these differ by 1-2 orders of magnitude.

**PA's PFBS de-allometrisation is the cleanest documented case of an agency choosing between
them.** PA took EPA's BMDL10 of 1.84 mg/kg/day, **divided by 0.149 to strip out EPA's allometric
DAF**, recovering an administered-dose POD of 12.35 mg/kg/day, then divided by MDH's
half-life-ratio DAF of 316 (human 665 h / female mouse 2.1 h) for an HED of 0.039 mg/kg/day. The
two adjustments differ about 47-fold, entirely from choosing TK data over body-weight scaling.
Caveat: that 2.1-hour female-mouse half-life rests partly on a **personal communication**
(Lau, 2017).

### GenX

The workbook's GenX entry shows the dosimetry falling back **entirely on allometry**: "DAF for the
allometric scaling of doses from mice to humans is 0.15", applied to a BMDL10 of 0.15 mg/kg/day
for single-cell liver necrosis (DuPont-18405-1037, 2010) to give a PODHED of 0.023 mg/kg/day. No
chemical-specific TK adjustment was possible. That factor carries no information about GenX at
all - which is the central reason GenX standards are not comparable with long-chain PFAS standards.
