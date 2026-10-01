# Human PFAS half-life estimates since 2022, and an assumption audit of every human estimate

Extraction: `/home/user/chiu__2022_rerun/pfas_tk_review/db/human_halflife_extended.csv`
(142 rows, 39 studies, 28 chemical labels; 112 rows carry a half-life, 100 carry an initial
serum concentration, 42 carry a volume of distribution, 31 carry a drinking-water
concentration). Columns are a strict superset of `literature/studies.csv`, so the two
concatenate. Retrieval log: `pfas_tk_review/papers/SOURCES_human.md`.

## What human PFAS half-life estimates published 2022-2026 are NOT in the existing extraction?

### Takeaway
Five genuinely new primary human studies appeared, and two of them change the picture: a
Veneto cohort of 5,860 people that is 29x larger than anything before it, and a
single-volunteer controlled-dose study that is the first human PFAS kinetics experiment
with a known administered dose, a background-free label, and simultaneous urinary and
faecal measurement. No systematic review or meta-analysis of human half-lives has been
published since Rosato 2024.

### Cited findings
- **Batzella 2024, Veneto, Italy (n=5,860)** - PFOA mean half-life **2.36 y (95% CI 2.33-2.40)**, females 2.04 (2.00-2.08), males 2.83 (2.78-2.89), children <14 y **1.64 (1.58-1.70)**; apparent PFOS 7.45 (7.24-7.69) and apparent PFHxS 5.39 (5.28-5.51). Baseline medians PFOA 49 ng/mL (range 0.5-1,090), PFOS 4.3, PFHxS 4.3. Background PFOA 1.64 ng/mL subtracted (males 2.04, females 1.27). Two samples, ~4 y apart, first 41-75 months after exposure ended. — [Environ Health Perspect 132(2):27002, PMID 38306197](https://doi.org/10.1289/EHP13152)
- **Lewis-Michl 2025, Hoosick Falls and Petersburgh, New York** - PFOA GM half-life **3.15 y (2.97-3.34)**, AM 3.65 (3.34-3.95); **age-standardised GM 2.86 y, AM 3.26 y**; females 2.90, males 3.46; ages 0-17 **1.96 y (1.69-2.27)** rising to 3.55 (3.27-3.87) at 60+. Water PFOA averaged **533.6 ng/L** (range 422-983) at Hoosick Falls and 92.5 ng/L at Petersburgh. Baseline serum GM 70.7 ng/mL in the 307 repeat-testers (42.1 in the full baseline group of 1,573), falling to 37.3 over 2.5 y. Serum/water ratio 89.0-101.6. — [J Expo Sci Environ Epidemiol, PMID 40247098](https://doi.org/10.1038/s41370-025-00769-z)
- **Lyu 2026, Tama region, western Tokyo (n=17, all female, 53-83 y)** - linear PFOS **3.9 y (3.4-4.6)** unadjusted / **2.7 (2.3-3.4)** background-subtracted; linear PFHxS **5.7 (4.6-7.5) / 5.6 (4.5-7.4)**; linear PFOA **8.0 (6.0-10.0) / 5.1 (4.1-6.8)**. Serum GMs in 2020: PFOS 13.9, PFHxS 21.0, PFOA 5.5 ng/mL, falling to 8.1 / 14.6 / 4.2 by 2023. — [Environ Health Prev Med 31:003, PMID 41548900](https://doi.org/10.1265/ehpm.25-00330)
- **Abraham 2024, single volunteer, known oral dose of 15 PFAS** - half-lives span **0.52 d (PFPeA) to 2,011 d / 5.51 y (PFOA)**: PFBA 4.18 d, PFHxA 1.45 d, **HFPO-DA (GenX) 2.86 d**, 6:2 FTS 4.14 d, DONA 34.7 d, PFBS 50.6 d, PFHpA 152 d, PFDoDA 295 d, PFUnDA 584 d, PFDA 862 d, PFOS 1,211 d (3.32 y), PFNA 1,305 d (3.57 y), PFHxS 1,634 d (4.47 y). Doses ~4 ug each (PFBS 18.42, HFPO-DA 19.58 ug) in an 82 kg 67-year-old male; plasma C0 0.13-1.64 ug/L; 450 days of plasma, urine and faecal sampling; two-compartment model. — [Environ Int 193:109047, PMID 39476597](https://doi.org/10.1016/j.envint.2024.109047)
- **Fustinoni & Consonni 2023, Solvay Spinetta Marengo, Italy (n=93, 568 samples)** - PFOA **GM 3.16 y (2.98-3.37)** from 2013 (PFOA phase-out) to 2021, median C0 **750 ng/mL**; no significant influence of sex or age. — [Ann Work Expo Health 67(4):470-483, PMID 36715212](https://doi.org/10.1093/annweh/wxac095)
- **Fustinoni 2023, cC6O4 (a PFOA replacement), n=18 male workers** - half-life **184 h (162-213) = 7.7 d (6.7-8.9)**, median C0 2.34 ng/mL, 5 days off work, 114 h of sampling. — [Toxics 11(3):284, PMID 36977049](https://doi.org/10.3390/toxics11030284)
- **Delaere 2025, South Australian firefighters** - treatment group (plasma donation and/or cholestyramine, n=19): PFOS apparent half-life **1.2 y** (41%/y decrease, max decrease 162 ng/mL), PFHxS **2.5 y** (32%/y, max 37 ng/mL). Untreated observation group (n=9): PFOS **7.3 y** (12%/y), PFHxS **9.4 y** (10%/y). — [Environ Int 202:109609, PMID 40540942](https://doi.org/10.1016/j.envint.2025.109609)
- **No newer review.** Two independent searches (PubMed 2024+ and Europe PMC 2025-2026) returned Rosato 2024 as the only systematic review and meta-analysis of human PFAS half-lives. — [Rosato 2024, PMID 38008199](https://doi.org/10.1016/j.envres.2023.117743)
- Studies also added to the database that pre-date 2022 but were absent from the existing extraction: **Xu 2020 Arvidsjaur airport** (11 compounds, both with and without background subtraction), **Yu 2021 New Jersey PFNA** (3.52 y, n=68), **Shi 2016 6:2 Cl-PFESA/F-53B**, **Costa 2009**, **Olsen 2009 PFBS**, **Russell 2013 PFHxA/PFHpA**, **Gomis 2016**, **Chang 2008 PFBA**, **Genuis 2014 phlebotomy**.

### New chemicals now covered
- **PFNA**: Yu 2021 3.52 y (n=68 New Jersey residents) — [PMID 33962122](https://doi.org/10.1016/j.ijheh.2021.113757); Abraham 2024 3.57 y at ~1,000x lower concentration; Chiu 2022 pooled 2.35 y.
- **PFDA / PFUnDA / PFDoDA**: only Abraham 2024 — 2.36 y, 1.60 y, 0.81 y. Half-life *decreases* with chain length above C9, reversing the usual pattern.
- **PFBS**: Olsen 2009 GM 25.8 d (range 13.1-45.7) at mean serum 397 ng/mL; Xu 2020 43.8 d (0.12 y, 95% CI 0.10-0.15) at median 0.33 ng/mL; Abraham 2024 50.6 d at plasma C0 1.64 ng/mL.
- **PFHpA**: Russell 2013 70 d (whole blood); Xu 2020 0.17 y (62 d); Abraham 2024 152 d; Zhang 2013 0.82-1.0 y from renal clearance alone.
- **PFHxA**: Russell 2013 32 d (range 14-49) in **whole blood**; Abraham 2024 1.45 d. Xu 2020 could not estimate it at all in serum (53% of individuals showed no decline) and states why: "PFHxA is more bound to blood cells and whole blood would therefore be a more suitable blood matrix" — so any serum-based PFHxA half-life should be discarded. — [Xu 2020, PMID 32648786](https://doi.org/10.1289/EHP6785)
- **PFPeA**: only Abraham 2024 — 0.52 d, the shortest human PFAS half-life on record.
- **GenX / HFPO-DA**: Abraham 2024 2.86 d (68.6 h) from a known dose; 81 +/- 55 h in 18 Chemours Dordrecht workers over a 3-4 day off-work weekend (grey literature: Clark DS letter to US EPA 2021, EPA 822R-21-010, reported in Fustinoni 2023 Table 5). The two independent human estimates agree to within 18%.
- **F-53B / 6:2 Cl-PFESA**: Shi 2016 — renal-clearance half-life median **280 y (range 7.1-4,230)** but total-elimination half-life median **15.3 y (10.1-56.4)**, "the most biopersistent PFAS in humans reported to date". Serum range <0.019-5,040 ng/mL; median 93.7 in high fish consumers, 51.5 in metal platers, 4.78 in controls. — [Environ Sci Technol 50(5):2396-404, PMID 26866980](https://doi.org/10.1021/acs.est.5b05849)
- **Other alternatives**: DONA 34.7 d, 6:2 FTS 4.14 d, PFBA 4.18 d (Abraham 2024); PFBA 72 h (43-101) in 9 workers (Chang 2008); cC6O4 7.7 d (Fustinoni 2023); PFPeS 0.63 y and PFHpS 1.46 y (Xu 2020).

### Inferences
- The 1,800-fold gap *inside Shi 2016* between its renal-clearance half-life (280 y) and its total-elimination half-life (15.3 y) is the single cleanest demonstration in the human literature that renal clearance is not total clearance. It is a within-paper control for the assumption that Zhang 2013 and four other excluded studies rest on.
- Coverage of short-chain and replacement PFAS roughly tripled between 2020 and 2024, but it rests on one cohort of 17 people (Xu 2020) and one person (Abraham 2024). Rosato's three-study minimum for meta-analysis is still unmet for every compound other than PFOA, PFOS and PFHxS.

### Gaps
- No study has been *designed* around a paediatric or pregnancy cohort. Every paediatric number is an age stratum inside an adult cohort (Batzella 2024 <14 y; Lewis-Michl 2025 0-17 y; Li 2022 preteens), and the only pregnancy evidence is Batzella's childbirth stratification (1.78 vs 2.54 y). There is no measured infant half-life at all.
- No haemodialysis study yields a half-life. Huang 2023 (n=301 dialysis, 20 CKD, 55 controls) shows seven PFAS significantly lower in dialysis patients but is cross-sectional, with no serial sampling. — [Sci Total Environ 896:165184, PMID 37391133](https://doi.org/10.1016/j.scitotenv.2023.165184)
- Lorber 2015 (effect of ongoing blood loss on serum PFAA, Chemosphere, PMID 25180653) could not be retrieved and is not represented.
- No human PBPK model has estimated a half-life from primary human data. The F-53B PBPK model (Zhang 2024, PMID 39394996) extrapolates from pregnant mice.

## For each estimate, what are the design assumptions?

### Takeaway
Every one of the 13 studies in Rosato 2024 used a one-compartment first-order model, so
model structure explains none of the heterogeneity; it is driven by (a) whether background
was subtracted, which matters by 1% to 150% depending purely on how far serum sits above
background, (b) how many half-lives were actually observed, which ranges from 0.15 to 7,
(c) whether the summary statistic is an AM or a GM, worth 10-16%, and (d) age and sex,
worth up to 1.8-fold within a single cohort.

### Cited findings
**(a) Was exposure demonstrably ceased, and how.** Rosato 2024 made "defined cessation of main exposure" an explicit inclusion criterion and excluded 7 studies where "the main exposure was still present at the time of blood sampling, or cessation of exposure was not clearly defined or explicitly stated (Ding 2020; Fu 2016; Gribble 2015; Harada 2005, 2007; Worley 2017; Zhang 2013a, 2013b)" plus 10 temporal-trend studies. Cessation mechanisms in the included set: GAC filtration (Bartell 2010, Brede 2010, Li 2018/2022, Yu 2021, Xu 2020, Batzella 2024, Lewis-Michl 2025), retirement or transfer (Olsen 2007, Olsen 2009, Costa 2009, Fustinoni & Consonni 2023), end of ski season (Russell 2013, Gomis 2016), and AFFF replacement (Nilsson 2022a/b) — but for the firefighters, Rosato notes "'apparent' half-lives were estimated, as firefighters continued to work in PFAS contaminated sites". — [Rosato 2024](https://doi.org/10.1016/j.envres.2023.117743)
- The tightest cessation is **Xu 2020**: first blood sample 11-14 days after clean water was supplied, with every participant's home water supply individually verified PFAS-free. The loosest are the cross-sectional and single-timepoint designs (Seals 2011, Zhang 2013, Shi 2016), where nothing stopped.
- **Abraham 2024 needs no cessation assumption at all** - a single known bolus of 13C-labelled compound means intake is exactly zero after t=0 and the label separates the dose from background entirely. It is the only human study with this property.

**(b) Was background subtracted or modelled.** Rosato: "In most of the included studies (76.9%), with few exceptions (Li et al., 2022; Nilsson et al., 2022a; Xu et al., 2020), information regarding background exposures was not provided, and the presence of ongoing exposures was not taken into account." Studies that report both ways, with the size of the correction:

| study | chemical | initial serum (ng/mL) | uncorrected | corrected | inflation |
|---|---|---|---|---|---|
| Nilsson 2022a | PFOA | 1.7 | 5.0 | 2.0 | **+150%** |
| Lyu 2026 | L-PFOA | 5.5 | 8.0 | 5.1 | +57% |
| Xu 2020 | L-PFOS | 11 | 2.91 | 1.69 | +72% |
| Xu 2020 | PFOA | 13 | 1.77 | 1.48 | +20% |
| Lyu 2026 | L-PFOS | 13.9 | 3.9 | 2.7 | +44% |
| Nilsson 2022a | PFHxS | 14 | 7.8 | 6.0 | +30% |
| Li 2022 | PFOA | 16 | 2.99 | 2.47 | +21% |
| Lyu 2026 | L-PFHxS | 21.0 | 5.7 | 5.6 | +2% |
| Batzella 2024 | PFOA | 49 | 2.71 (derived) | 2.36 | +15% |
| Nilsson 2022b | total PFOS | 60 | 6.5 | 5.7 | +12% |
| Xu 2020 | PFHxS | 133 | 2.86 | 2.84 | +0.7% |
| Li 2022 | L-PFOS | 150 | 2.87 | 2.73 | +5% |
| Li 2022 | PFHxS | 260 | 4.55 | 4.52 | +0.7% |

Sources: [Rosato 2024 Tables 2-3](https://doi.org/10.1016/j.envres.2023.117743); [Xu 2020 Table 5](https://doi.org/10.1289/EHP6785); [Lyu 2026 Tables 3 and 5](https://doi.org/10.1265/ehpm.25-00330); [Batzella 2024 Discussion](https://doi.org/10.1289/EHP13152).
- Methods used: Xu 2020 subtracts the median of an age-matched unexposed Swedish reference population (Karlshamn, n=58) and replaces sub-threshold values with half the background. Batzella 2024 subtracts 1.64 ng/mL (sex-specific) from a separate Veneto background-area survey and excludes 90 subjects who fall below it. Lyu 2026 subtracts the Japanese national biomonitoring means (PFOS 2.5, PFOA 1.5, PFHxS 0.4 ng/mL). Lewis-Michl 2025 does not subtract at all - it *excludes* the 2.8% of participants below the NHANES 95th percentile (4.17 ng/mL).
- **Li 2018 justifies not subtracting**, and the justification is sound at its concentrations: "the PFAS levels of the last sample for all the individuals were far above what is expected in the background", with median PFHxS 180x the neighbouring municipality.

**(c) How long was follow-up relative to the half-life.** Observed half-lives per study (derived by us from the reported follow-up and half-life):
- 7.0 half-lives: Olsen 2009 PFBS (180 d / 25.8 d)
- 2.9: Xu 2020 PFHpA; 3.5: Xu 2020 PFBS
- 2.5: Fustinoni & Consonni 2023 PFOA (8 y / 3.16 y)
- 1.3: Olsen 2007 PFOA; 1.4: Costa 2009; 1.8: Li 2022 PFOA
- 1.0: Olsen 2007 PFOS; 0.8: Lewis-Michl 2025 (2.5 y / 3.15 y); 0.8: Lyu 2026 PFOS
- 0.6: Olsen 2007 PFHxS; 0.6: Fustinoni 2023 cC6O4; 0.5: Bartell 2010
- **0.15-0.18: Xu 2020 PFHxS and L-PFOS** (5 months for a ~2.9 y half-life)
- **0.23: Abraham 2024 PFOA** (450 d for a 2,011 d half-life) - the long-chain values are extrapolations of the early terminal slope, with a 95% CI of 1,466-3,206 d (4.0-8.8 y)
- Xu 2020's own synthesis of this: "there is some evidence of a possible nonlinear clearance process of PFAS from the literature, mainly about PFOA, showing that the estimated half-life appeared to decrease with increased follow-up time. For instance ... Olsen 3.8 y on 5 y, Brede 3.3 y on 2 y, Bartell 2.3 y with 1 y. Our PFOA half-life of 1.77 y is consistent with this pattern that elimination is faster in the early time window after exposure stopped and becomes slower after 1 or 2 y."

**(d) Which statistic is reported.** AM/GM gaps within single studies: Olsen 2007 PFOS 5.4 AM vs 4.8 GM (+13%), PFHxS 8.5 vs 7.3 (+16%), PFOA 3.8 vs 3.5 (+9%); Lewis-Michl 2025 PFOA 3.65 AM vs 3.15 GM (+16%); Costa 2009 5.1 AM vs 4.8 GM (+6%). Batzella 2024 reports the reverse ordering because its distribution is left-skewed in half-life space: "the median value was a little higher than the corresponding mean. This reflects the fact that the distribution of half-lives estimates was left skewed." Lyu 2026 reports both a "point-estimated" half-life from the mean rate constant and a "mean individual" half-life from individual rates, and the latter is systematically longer (PFOA 8.0 vs 9.8; PFOS 3.9 vs 4.6; PFHxS 5.7 vs 6.5) - **ln2/mean(k) and mean(ln2/k) are not the same number, and the gap is 15-23%.**

**(e) Were isomers separated.** Yes in Li 2022, Xu 2020, Nilsson 2022b, Zhang 2013 and Lyu 2026 (linear only); no elsewhere. The direction is not consistent: in **Xu 2020** every branched PFOS isomer cleared faster than linear (L-PFOS 2.91 y vs 1m 1.27, 3/4/5m 1.09, 2/6m 1.04); in **Nilsson 2022b** branched was *slower* (sum-branched 5.5 y vs linear 4.0 y); Rosato's pooled values split both ways (L-PFOS 3.13, 2/6m 2.55, 3/4/5m 3.94, **1m-PFOS 5.86**). Zhang 2013 found the same anomaly in renal clearance: "the renal clearance efficiency of 1m-PFOS was lower than n-PFOS, and was the lowest among all PFOS isomers ... its urinary elimination was even lower (p<0.001) than PFHxS and was the most persistent of all PFAA compounds examined."

**(f) Which excretion routes were counted.** None, in every serum-decay study - the slope is agnostic to route. Routes are counted only in the mass-balance studies, and that is where the assumption bites: Zhang 2013 and Shi 2016 count urine only (plus menstruation for Zhang's young females); Fustinoni 2023 counts urine only for cC6O4; **Andersson 2025 and Abraham 2024 are the only human studies that measured urine and faeces simultaneously.**
- **They disagree about PFOS.** Andersson 2025: L-PFOS 91 ng/day urinary vs **364 ng/day faecal** (4:1 faecal); PFOA 26 vs 15 ng/day (1.7:1 urinary). Abraham 2024 Table 4: faecal clearance of labelled PFOS was **not detected**, while faecal clearance was 17% of total for PFOA, **58% for PFNA, 61% for PFDA, 60% for PFUnDA and 60% for PFDoDA**, and not detected for PFHxS or any short-chain compound. The two agree that faeces dominate for long-chain PFCAs and contradict each other on PFOS.
- Independent support for a faecal route: three cholestyramine intervention studies (Genuis 2010 case report, Genuis 2013 case series n=8, **Moller 2024 cross-over n=45 with 63% lowering of serum PFOS in 12 weeks vs 3% without**), and Li 2022's finding that higher faecal calprotectin went with shorter half-lives. — [Andersson 2025 Introduction](https://doi.org/10.1016/j.envint.2024.108497)

**(g) Was a Vd assumed, and what value.** See the dedicated section below. Serum-decay designs never need one; mass-balance designs need one and it multiplies straight through.

**(h) One- or two-compartment or PBPK.** Rosato 2024: "In all the included studies, PFAS half-life was estimated using one-compartment models with first-order elimination." The only exceptions in the whole human literature are Chiu 2022 (Bayesian hierarchical, still one-compartment first-order) and **Abraham 2024 (two-compartment, with one-compartment used for PFBA and 6:2 FTS)**. No human PBPK half-life estimate exists.

**(i) Serum decay or mass balance.** Serum decay: Olsen 2007/2009, Bartell 2010, Brede 2010, Costa 2009, Russell 2013, Gomis 2016, Li 2018/2022, Xu 2020, Yu 2021, Nilsson 2022a/b, Fustinoni & Consonni 2023, Batzella 2024, Lewis-Michl 2025, Lyu 2026, Delaere 2025, Chang 2008, GenX workers. Mass balance / renal clearance: Zhang 2013, Shi 2016, Fustinoni 2023 (cC6O4 Vd), Zhou 2014, Zhang 2015, Gao 2015, Fujii 2015 (the last four known only as Rosato exclusions). Both: Abraham 2024, Andersson 2025.

### Inferences
- Because all 13 studies in the meta-analysis share the one-compartment first-order assumption, **no between-study comparison in that review can detect a bias arising from it**. Xu 2020's observation that apparent half-life lengthens with follow-up duration is the only evidence bearing on it, and it points the same way a two-compartment system would: an early fast phase followed by a slow terminal phase.
- The AM-vs-GM and ln2/mean(k)-vs-mean(ln2/k) choices together account for 10-25%, which is of the same order as the entire background correction at high exposure. Cross-study comparisons that ignore both are comparing noise.

### Gaps
- Daily intake in ng/kg/day is reported by essentially nobody. Three values in the database are derived by us from water concentration x 2 L/day / 70 kg (Hoosick Falls 15, Petersburgh 2.6, Arvidsjaur airport 8.6 for PFHxS) and all three are upper bounds.
- Olsen 2009, Russell 2013, Gomis 2016 and Girardi 2018 could only be extracted secondarily; their methods cannot be audited from the sources in hand. Girardi 2018's initial concentration is ambiguous by a factor of 1,000 (reported as "1.489" in a table headed ug/L).

## Serum concentrations and exposure levels per cohort

### Takeaway
Initial serum concentrations in the database span **0.13 ng/mL (Abraham's labelled
microdose) to 5,040 ng/mL (Shi's Cl-PFESA)**, a 39,000-fold range, and drinking-water
concentrations span 92.5 to 710 ng/L. Across that range the PFOA half-life moves only
between about 1.6 and 8 y, and the ordering is not monotone - which already rules out a
strong concentration dependence.

### Cited findings - initial serum concentrations (ng/mL)
- Shi 2016 Cl-PFESA: whole-sample range **<0.019-5,040**; median 93.7 (high fish consumers), 51.5 (metal platers), 4.78 (controls).
- Girardi 2018 Miteni retirees, PFOA: GM reported as "1.489" - almost certainly **1,489** (Italian thousands separator) but unverified.
- Olsen 2007: PFOA median **408** (72-5,100) falling to 148 (17-2,435); PFOS 626 (145-3,490) to 295 (37-1,740); PFHxS mean 290 (16-1,295) to 182 (10-791). — [ATSDR 2021 Appendix A Table A-2](https://www.atsdr.cdc.gov/toxprofiles/tp200.pdf)
- Fustinoni & Consonni 2023 Solvay: PFOA median C0 **750**.
- Gomis 2016 ski waxers: **250-1,050** (attributed to PFOS by Rosato Table 3 and to PFOA by the project's existing `human_initial_vs_halflife.csv` - unresolved conflict, flagged in the CSV).
- Olsen 2009 PFBS workers: mean **397**, median 363.
- Li 2018 Ronneby: PFOS mean **387**, PFHxS **353**, PFOA 21.2. Li 2022 Ronneby: GM PFHxS **260**, PFOS 150, PFOA 16.
- Bartell 2010 Mid-Ohio Valley: PFOA mean **180**.
- Xu 2020 Arvidsjaur, first serum from all 26 employees (median, range): PFHxS **76 (17-402)**, PFOA 9.1 (2.9-31), L-PFOS 9.5 (5.4-28), B-PFOS 6.4 (2.2-28), PFPeS 6.9 (1.4-17), PFHpS 1.3 (0.28-6.2), PFHpA 0.46 (0.07-2.2), PFHxA 0.38 (0.16-1.1), PFBS 0.33 (<LOD-1.3). In the 17 followed: PFHxS 133, PFOA 13, L-PFOS 11.
- Lewis-Michl 2025 Hoosick Falls: PFOA GM **70.7** in the half-life subgroup, 42.1 in the full baseline cohort; Petersburgh GM 9.57, median 11.3.
- Nilsson 2022b aviation firefighters: mean L-PFOS 26, median 21, mean total PFOS 60.
- Batzella 2024 Veneto: PFOA median **49** (0.5-1,090), PFOS 4.3 (0.5-142), PFHxS 4.3 (0.5-109.2).
- Brede 2010 Arnsberg: median PFOA 24, PFOS 9, PFHxS 2.
- Lyu 2026 Tokyo: PFHxS GM 21.0, PFOS 13.9, PFOA 5.5.
- Costa 2009: PFOA median 11.92, mean 18.8.
- Gasiorowski 2022 firefighters: PFOS mean 10.7 (SD 5.9) at baseline, PFHxS 4.2 (9.7, range 0-140), **PFOA 1.2 (SD 1.1)** - at the 1 ng/mL limit of detection.
- Nilsson 2022a: linear PFOA **1.7**, linear PFHxS 14, total PFOS 27, PFHpS 1.7 (Rosato labels these "initial" but the Nilsson abstract reports the same values as 2018-19 arithmetic means, so the assignment is uncertain - flagged).
- Yu 2021 New Jersey PFNA: **2.88 ng/mL** (Rosato Table 2 prints "2,882" under a ng/mL heading; it must be ng/L, since the abstract says participants exceeded the NHANES 95th percentile for PFNA which is of order 2-3 ng/mL - **unit discrepancy flagged, do not use 2,882 ng/mL**).
- Fustinoni 2023 cC6O4: median C0 2.34.
- Chang 2008 PFBA workers: C0 range 2-71.
- Abraham 2024: plasma C0 **0.129-1.641** across the 15 compounds (PFOA 0.529, PFOS 0.303, PFHxS 0.367, PFBS 1.641, HFPO-DA 1.341).
- Russell 2013 ski wax technicians: serum PFHxA mean 1.9, median 0.68 (half-life measured in whole blood).
- Genuis 2014 family, before -> after ~4 y of phlebotomy: PFHxS 125 -> 23.3 average (individual range 29.3-293 before); PFOS 43.4 -> 6.7; PFOA 5.7 -> 1.4.

### Cited findings - drinking-water concentrations and intake
- Hoosick Falls, NY: PFOA average **533.6 ng/L** over 25 samples (range 422-983); Petersburgh 92.5 ng/L. Serum/water ratios 89.0-101.6 and 103.4-122.2 respectively, "similar to ratios estimated for Little Hocking public water users and C-8 private well users". Private wells: median 25 ng/L in the Hoosick area, 49 ng/L in Petersburgh.
- Arvidsjaur airport water (Xu 2020 Table 3, in ng/mL, i.e. x1000 for ng/L): PFHxS 0.71 (**710 ng/L**), PFHxA 0.33, PFOA 0.30, PFBS 0.20, PFPeS 0.18, PFHpA 0.097, L-PFOS 0.062, B-PFOS 0.064, PFHpS 0.016. Serum/water ratios rise monotonically with chain length: PFHxA 1.15, PFBS 1.65, PFHpA 4.74, PFOA 30.3, PFPeS 38.3, PFHpS 81.3, B-PFOS 100, PFHxS 107, **L-PFOS 153**. Xu's PFOA serum/water ratio of 30.3 is far below the 100-231 of other studies, and the explanation is exposure duration, not kinetics: "in our study the individuals were only exposed at work and had a PFAS-free water supply at home".
- Tama region, Tokyo: pre-2019 groundwater exceeded Japan's 50 ng/L provisional target for PFOS+PFOA combined; the cohort's own tap-water concentration was never measured.
- Abraham 2024 is the only study with an exactly known dose: 3.71-4.02 ug of each labelled compound (PFBS 18.42, HFPO-DA 19.58 ug) in an 82 kg man, i.e. **45-49 ng/kg as a single bolus** (PFBS 225, HFPO-DA 239 ng/kg).

### Inferences
- Comparing the two ends of the PFOA series directly: Abraham 2024 measured **5.51 y (4.01-8.78) at a plasma C0 of 0.53 ng/mL**, while Fustinoni & Consonni measured **3.16 y at 750 ng/mL** and Batzella measured **2.36 y at 49 ng/mL**. Over a 1,400-fold concentration range the half-life changes by 2.3-fold, which on a log-log scale is a slope of ln(5.51/3.16)/ln(750/0.53) = **-0.077**, i.e. d ln(clearance)/d ln(concentration) ~= **+0.08**. That is within rounding of the +0.09 cross-cohort slope and the +0.11 male-rat slope already in this project, and of the +0.12 derived here from the three PFBS points.
- But the ordering inside the high-exposure range is wrong for saturation: Fustinoni's 750 ng/mL cohort has a *longer* half-life (3.16 y) than Batzella's 49 ng/mL cohort (2.36 y). Design (occupational, still on site, no background subtraction vs community, background-subtracted) explains that better than concentration does.

### Gaps
- No cohort reports measured daily intake. Every intake figure in the database is derived from water concentration with assumed consumption.
- Initial serum was not recoverable for Delaere 2025 (only the maximum decrease: 162 ng/mL PFOS, 37 ng/mL PFHxS), for the Chemours GenX workers, or by age stratum for Lewis-Michl's half-life subgroup.

## Do any human studies directly test whether half-life depends on serum concentration or exposure level?

### Takeaway
Five studies now test this directly, three of them new since 2022. **Every
between-person test gives a positive sign (higher baseline, longer half-life), the
opposite of saturable reabsorption; the one study that tests it across a known-dose
range gives a negative sign.** The between-person result is explained by two artefacts
the authors themselves identify, so the direct evidence is currently uninformative rather
than contradictory.

### Cited findings
| level of comparison | source | n | result | sign vs saturation |
|---|---|---|---|---|
| between persons, baseline quartiles | **Batzella 2024 Table S3** | 5,860 | PFOA **Q1 1.92 (1.86-1.98) -> Q4 2.85 (2.79-2.92)**; +34.1% in males, +26.4% in females | **contradicts** |
| between persons, baseline tertiles | Li 2022 Table S4 | 114 | PFHxS 3.88 -> 4.83 y, PFHpS 3.94 -> 4.94 y, both **p=0.02**; PFOA 2.29 -> 2.58 (p=0.25); L-PFOS 2.49 -> 2.77 (p=0.13) | **contradicts** |
| between persons, Pearson r | **Lyu 2026 Fig. 2** | 17 | PFOS r=**+0.214** (p=0.410), PFHxS r=**+0.168** (p=0.520), PFOA r=**-0.231** (p=0.371) - none significant | mixed, all null |
| between persons, exposure strata | **Lyu 2026 Table 4** | 17 | PFOA **2.0 y shorter** in the high-exposure group (8.7 -> 6.7; individual means 10.6 -> 8.0, p=0.351); PFOS 3.8 vs 4.0 (p=0.854); PFHxS 5.4 vs 6.1 (p=0.970) | supports for PFOA only, NS |
| between persons, Spearman rate vs level | **Xu 2020 Results** | 17 | "For most of the PFAS, the individual elimination rates were not correlated with their initial serum levels. Only PFHpA showed a significant positive correlation" - 1 of 11 compounds | supports for PFHpA only |
| between water districts | Seals 2011 (existing) | 1,573 | 2.9 y (Little Hocking) vs 8.5 y (Lubeck) at ~2x serum difference; implied log-log slope +1.55 | supports, but **above the mechanistic ceiling of 1** |
| across a known-dose range, same person | **Abraham 2024 vs cohorts** | 1 | PFOA 5.51 y at 0.53 ng/mL vs 2.36-3.16 y at 49-750 ng/mL; slope ~ **+0.08** | supports |
| across studies, no background | **DERIVED: PFBS** | 3 studies | 25.8 d at 397 ng/mL, 43.8 d at 0.33, 50.6 d at 1.64; slope ~ **+0.12** | supports |

- **Batzella 2024 names the confound and rules out resolving it**: "Of course, there will be a tendency for people with more rapid excretion having lower baseline concentrations due to relatively more excretion between the end of exposure and the first sample. Whether there is an effect of concentration in addition on excretion rate cannot be distinguished in this study." Sampling began 41-75 months (mean 53) after exposure ended, so fast eliminators had already been depleted for 3.4-6.3 years before baseline. — [Batzella 2024 Discussion](https://doi.org/10.1289/EHP13152)
- **Lyu 2026 names the second confound**, the background floor: "Because measured PFOA concentrations in our study were close to background levels, even small unaccounted exposures may have disproportionately influenced the rate constant estimates, biasing the elimination half-life upward. This interpretation is supported by the exposure-stratified analysis, in which participants with higher baseline PFOA levels showed shorter half-life estimates."
- **The background floor produces a spurious saturation signal of exactly the right sign and a plausible magnitude.** From the table in the assumptions section, the inflation from unsubtracted background falls monotonically from +150% at a serum/background ratio of ~1 to +0.7% at a ratio of 180. A cross-cohort regression that pools corrected and uncorrected estimates will therefore show lower-exposure cohorts eliminating more slowly - indistinguishable from saturation.
- **Gasiorowski 2022 supplies the limiting case in a randomised control arm**: at a baseline serum PFOS of 10.7-11.7 ng/mL, the observation group's mean change over 52 weeks was **-0.01 ng/mL (95% CI -0.5 to 0.5, p=0.96)**, i.e. no detectable decline and an effectively infinite apparent half-life. PFHxS *rose* by 0.4 ng/mL (p=0.06) and PFOA *rose* significantly by 0.2 ng/mL (p=0.02). The authors: "we would have expected PFAS levels to decrease by approximately 10% ... In our cohort, the baseline levels were substantially lower than those in the previous study, which may explain the lower-than-expected changes." — [JAMA Netw Open 5(4):e226257, PMID 35394514](https://doi.org/10.1001/jamanetworkopen.2022.6257)
- **ATSDR already concedes concentration-range dependence as a regulatory caveat**: its half-life estimates "are most applicable to serum concentrations within the above ranges and would be less certain if applied to serum concentrations substantially below or above these ranges", with the ranges being PFOA 72-5,100, PFOS 145-3,490 and PFHxS 16-1,295 ng/mL.

### Inferences
- The within/between split reported in the project's existing SYNTHESIS.md survives and strengthens. What is new is that **both of the leading between-person confounders are now quantified**: the survivorship/regression artefact (Batzella's 41-75 month delay before baseline) and the background floor (the inflation table). Both push the between-person association positive, which is why every between-person test gives the wrong sign.
- Two independent concentration contrasts that avoid *both* confounders - Abraham's known-dose PFOA and the three-study PFBS series, where background is undetectable - both give a log-log slope of +0.08 to +0.12. Four independent estimates now cluster there: +0.08 (Abraham vs cohorts, PFOA), +0.09 (existing cross-human-cohort, PFOA), +0.11 (project's male-rat fits, PFOA), +0.12 (PFBS, derived here). For a slope whose mechanistic ceiling is 1, this is a consistent and small effect.
- Applied to the project's species question nothing changes: a slope of 0.1 across the 187-fold rat/human serum gap predicts a 1.6-fold half-life ratio against an observed 81-fold.

### Gaps
- No human study has deliberately varied dose within individuals. Abraham 2024 is one dose in one person; a second dose level in the same volunteer would settle the question for PFOA directly and is the obvious experiment.
- Li 2022's tertile analysis has never been re-run with age adjustment, and age is the dominant between-person confounder (Lewis-Michl's 1.8-fold gradient, Batzella's age-by-sex interaction, Li 2022's 45-60% preteen/over-50 gap). This still needs individual-level data.

## Blood-donation, plasma-donation and other controlled-removal studies

### Takeaway
Four controlled-removal studies now exist (one randomised), and they establish that
removal works and roughly how fast, but **none of them reports a volume of distribution or
a clearance, which is the quantity they are uniquely placed to measure**. The randomised
trial sampled serum only at weeks 0, 52 and 64, so no kinetics can be fitted from it.

### Cited findings
- **Gasiorowski 2022, randomised clinical trial, Fire Rescue Victoria, n=285 (95 per arm), ANZCTR-registered.** Plasma donation (up to 800 mL every 6 weeks, mean 6.4 of 9 donations) reduced mean serum PFOS by **-2.9 ng/mL (95% CI -3.6 to -2.3, p<0.001)** over 52 weeks from a baseline of 10.7; whole-blood donation (~470 mL every 12 weeks, mean 4.3 of 5) by -1.1 (-1.5 to -0.7); observation by -0.01 (-0.5 to 0.5, p=0.96). PFHxS: plasma -1.1 (-1.6 to -0.7), blood -0.1 (p=0.54), observation +0.4 (p=0.06). PFOA: plasma -0.5 (p=0.001), blood -0.1 (p=0.63), observation **+0.2 (p=0.02)**. Treatment differences persisted from week 52 to week 64 with no donations. Haemoglobin fell 0.51 g/dL more in the blood arm; no change in lipids, thyroid, liver or kidney tests. Post hoc, treatment effects were largest in the top baseline quartile, with no such pattern in the observation arm. Limitation stated by the authors: "Serum PFAS levels were measured at screening, baseline, week 52, and week 64 but were not assessed during the intervention ... so we are not able to comment further on the kinetics of PFAS clearance." — [PMID 35394514](https://doi.org/10.1001/jamanetworkopen.2022.6257)
- **Delaere 2025, South Australian Metropolitan Fire Service voluntary treatment programme.** Treatment (n=19: 2 plasma donation, 12 cholestyramine, 5 both) gave PFOS apparent half-life **1.2 y** (41% annual decrease) and PFHxS **2.5 y** (32%); the untreated observation group (n=9) gave PFOS **7.3 y** (12%) and PFHxS **9.4 y** (10%). "The calculations only included data from participants whose serum PFOS and PFHxS concentrations decreased. The study did not conduct statistical comparisons; conclusions were drawn based on visual observations." — [PMID 40540942](https://doi.org/10.1016/j.envint.2025.109609)
- **Moller 2024, cholestyramine cross-over trial, n=45, Denmark.** 63% lowering of serum PFOS in a 12-week cholestyramine period vs 3% in a 12-week period without; PFOA, PFNA, PFDA and PFHxS also lowered "but to lesser degrees". Derived by us: the treatment period corresponds to a PFOS half-life of **0.16 y** and the control period to **5.25 y**. — [Environ Int 185:108497, quoted in Andersson 2025](https://doi.org/10.1016/j.envint.2024.108497)
- **Genuis 2014, phlebotomy case series, one family of 6 over ~4 years.** PFHxS fell from an average of 125 to 23.3 ng/mL, PFOS 43.4 to 6.7, PFOA 5.7 to 1.4. Apparent half-lives were significantly shorter than the Olsen 2007 geometric means in every member except the mother, whose venesection was often unsuccessful. The individual values appear only in Fig. 4 and are not given numerically. Key quantitative observation: the mother's achieved blood-removal rate of **0.028 mL blood/day/kg is almost exactly the average menstrual blood loss of 0.029 mL/day/kg**, and even that was not enough to produce a significant acceleration for PFHxS. — [PLoS One 9(12):e114295, PMID 25504057](https://doi.org/10.1371/journal.pone.0114295)
- Zhang 2013 independently puts menstrual serum clearance at **0.029 mL/day/kg**, comparable with the *renal* clearance of PFHxS (0.033), PFOS (0.044), PFDA (0.047) and PFUnA (0.045) - so menstruation is a material route only for the compounds that are hardest to excrete renally, which is precisely the set with the longest half-lives and the largest sex differences.
- Haemodialysis: Huang 2023 found total and linear PFOS, PFDA, PFNA, PFHxS, PFOA and PFUnDA significantly lower in 301 maintenance dialysis patients than in 20 CKD-5 and 55 controls, but the design is cross-sectional with no serial sampling, so no half-life or clearance follows. A 2024 in-vitro haemoadsorption kinetic model exists (PMID 38493768) but is not a human study. — [PMID 37391133](https://doi.org/10.1016/j.scitotenv.2023.165184)

### Inferences
- A controlled-removal design is the most direct available route to a human Vd: removing a known plasma volume of known concentration removes a known mass, and the resulting serum drop gives Vd = mass removed / concentration drop. **Gasiorowski 2022 has every input needed** (800 mL per donation, 6.4 donations, measured baseline and week-52 concentrations) and did not compute it. A rough calculation from the published means - 6.4 x 0.8 L x ~10 ng/mL removed, against a 2.9 ng/mL fall - implies a Vd of order 18 L, i.e. ~0.2 L/kg at 90 kg, but this ignores concurrent physiological elimination and intake and should not be quoted as a result.
- Delaere's untreated comparator (PFOS 7.3 y, PFHxS 9.4 y) and Batzella's apparent values (PFOS 7.45 y, PFHxS 5.39 y) converge on the same conclusion from opposite directions: in cohorts without demonstrated cessation and without background correction, PFOS apparent half-life lands near 7.5 y, roughly 1.6x the pooled literature value.

### Gaps
- No controlled-removal study reports Vd or clearance. This is the clearest actionable gap in the whole area and could be closed by reanalysing Gasiorowski 2022's existing data.
- The Gasiorowski trial's week-52-to-week-64 washout, with 12 weeks of no donation, is in principle a clean elimination window at a known starting concentration, and it is reported only as a group mean change.

## New evidence on faecal versus urinary elimination beyond Andersson 2025

### Takeaway
Abraham 2024 is the one genuinely new measurement, and it both corroborates and
contradicts Andersson 2025: faecal clearance accounts for 58-61% of total clearance for
PFNA, PFDA, PFUnDA and PFDoDA and 17% for PFOA, but **faecal clearance of labelled PFOS
was not detected at all**, against Andersson's 4:1 faecal dominance for PFOS.

### Cited findings
- **Abraham 2024 Table 4** (CLfec as a fraction of CLtot, derived by us from the printed clearances): PFOA 0.0004/0.0024 = **17%**; PFNA 0.0022/0.0038 = **58%**; PFDA 0.0051/0.0084 = **61%**; PFUnDA 0.0098/0.0163 = **60%**; PFDoDA 0.0286/0.0474 = **60%**. Faecal clearance **not detected** for PFOS, PFHxS, PFBS, PFBA, PFPeA, PFHxA, PFHpA, 6:2 FTS, HFPO-DA or DONA. Urinary clearance was measurable only for the short-chain and alternative compounds (PFPeA 8.89, PFHxA 2.68, HFPO-DA 1.43, PFBA 1.00, 6:2 FTS 0.97, DONA 0.178, PFBS 0.067, PFHpA 0.023 mL/min) and was below quantification for every long-chain compound. The paper's own summary: "Elimination from the body was completely explained by the urinary losses in case of the short-chain and 'alternative' PFAS, and in part by the fecal losses in case of the long-chain PFCA." — [PMID 39476597](https://doi.org/10.1016/j.envint.2024.109047)
- Abraham also reports the fraction unbound in plasma (fup, from Smeltz 2023) and the resulting glomerular filtration clearance, and the comparison is informative: for PFOA, CLfilt is **0.11 mL/min against a CLtot of 0.0024**, i.e. filtration alone would give a half-life of 42 days at the measured Vd of 121 mL/kg, against the observed 2,011 days. Net tubular reabsorption therefore accounts for a ~48-fold reduction in clearance.
- **Andersson 2025** (already on disk): L-PFOS 91 ng/day urinary vs **364 ng/day faecal**; PFOA 26 vs 15 ng/day. The paper's framing is that "most pharmacokinetic models assume that the urinary route dominates". Its Vd for PFHxS "indicated an under-estimated fecal concentration, which could not be explained by" the method - so the authors already flag that their faecal estimates are not uniformly reliable.
- **Moller 2024** (n=45 cross-over): 63% lowering of serum PFOS with 12 weeks of cholestyramine vs 3% without - strong independent support for an enterohepatic route for PFOS specifically, which is the compound Abraham could not detect in faeces.
- **Li 2022**: higher faecal calprotectin, a marker of intestinal inflammation, went with shorter half-lives, read as inflammation reducing intestinal reabsorption.
- **Niu 2026** characterised transport of PFAS by three renal transporters and notes that "the long biological half-lives of PFAS in humans have been linked to interactions with renal transport proteins and polypeptides. However, only a limited number of kidney transporters have been studied." — [Environ Health (Wash) PMID 42775203](https://doi.org/10.1021/envhealth.6c00088)

### Inferences
- The PFOS conflict has a candidate resolution that neither paper tests: Andersson measured faecal PFOS in people with ongoing dietary intake, so unabsorbed dietary PFOS passing straight through would be counted as elimination, whereas a labelled bolus that is "absorbed quickly and almost completely" cannot generate that signal. If so, Andersson's 4:1 faecal ratio for PFOS is partly a measurement of intake, not of elimination, and the correction it implies for Zhang 2013's PFOS half-life (dividing ~18 y by ~5) is not justified. **This directly affects the existing SYNTHESIS.md, which uses Andersson's route split to correct Zhang.**
- The cholestyramine results push the other way and favour a real enterohepatic route for PFOS. The two cannot both be fully right; a labelled-dose study with a cholestyramine arm would settle it.

### Gaps
- No study has measured faecal elimination of a labelled PFOS dose with and without a bile-sequestrant. Nothing resolves the conflict from existing data.
- Biliary secretion has never been measured directly in humans; it is inferred from faecal output in both studies.

## New human volume-of-distribution estimates

### Takeaway
Abraham 2024 provides the first human Vd values derived from a known administered dose,
for 15 compounds at once, and they are remarkably uniform: **110-177 mL/kg for twelve of
the fifteen**, rising only for PFDA (184), PFUnDA (241) and PFDoDA (354). These land close
to the long-assumed 170-200 mL/kg and far below Chiu 2022's fitted 430 mL/kg, which
matters because the project's reconciliation of Zhang 2013 rests on Chiu's value.

### Cited findings - all human PFOA and PFOS Vd values located
| source | PFOA Vd (L/kg) | PFOS Vd (L/kg) | basis |
|---|---|---|---|
| **Abraham 2024** | **0.121** (0.118-0.124) | **0.152** (0.148-NA) | **MEASURED**: absorbed dose / back-extrapolated plasma C0, n=1, 82 kg male |
| Andersson 2025 | 0.074 | 0.093 | measured via urinary+faecal mass balance and a mixed-model k, n=40 |
| Butenhoff 2004c (via ATSDR) | 0.18 male, 0.20 female | - | non-compartmental, **monkey**, assumed applicable to humans |
| Chang 2012 (via ATSDR) | - | 0.20 male, 0.27 female | non-compartmental, **monkey** |
| Harada 2005a (via ATSDR) | 0.3 | 0.3 | - |
| Thompson 2010 (as used by Zhang 2013) | **0.17** | **0.23** | PK modelling with assumed water intake |
| Thompson 2010 (as reported by Andersson 2025) | **0.23** | **0.17** | same source, **values transposed** |
| Buser 2021 | 0.20 | 0.20 | extrapolated from monkeys |
| **Chiu 2022** | **0.43** | **0.336** | **FITTED** jointly with the half-life in a Bayesian hierarchical model from paired water and serum data |
| Han et al. (via Zhang 2013) | 0.191 +/- 0.067 (mean across mammals) | - | cross-species summary |

- **Abraham 2024's full Vd set (mL/kg bw, point estimate and range)**: PFPeA 110 (107-115), PFHxA 119 (113-126), 6:2 FTS 119 (115-122), PFOA 121 (118-124), PFNA 124 (122-127), PFHxS 125 (122-128), PFHpA 128 (125-131), PFBA 132 (128-136), PFBS 137 (134-140), PFOS 152 (148-NA), DONA 168 (140-212), HFPO-DA 177 (172-183), PFDA 184 (180-188), PFUnDA 241 (232-252), PFDoDA 354 (342-368). "The volumes of distribution predominantly were within a narrow range <= 177 mL/kg bw."
- **Fustinoni 2023** gives a third directly estimated human value, for cC6O4: mean **0.084 L/kg** (median 0.081, SD 0.042, range 0.023-0.204; absolute Vd mean 6.6 L), from renal clearance and the fitted elimination constant in 18 workers.
- **PFHxS and PFNA**: ATSDR uses 0.287 (male) and 0.213 (female) L/kg for PFHxS from cynomolgus monkeys (Sundstrom 2012), and states that "the estimated volume of distribution for PFNA in humans will be assumed to be the same for PFOA" - a pure assumption of equality. Abraham 2024 now supplies measured human values of 0.125 (PFHxS) and 0.124 (PFNA) L/kg.
- **A citation conflict that must be resolved.** Zhang 2013's Methods state: "Thompson et al. reported that V was 170 and 230 mL/kg for PFOA and PFOS in humans ... Thus, to simplify the estimation, the V values of 170 and 230 mL/kg were used to estimate the half-lives for all PFCAs and PFSAs, respectively." Andersson 2025's Introduction states the reverse: "Thompson et al. used pharmacokinetic modelling with assumptions regarding daily intake of contaminated drinking water, yielding 230 mL/kg body weight for PFOA and 170 mL/kg for PFOS." One of the two has transposed the values.

### Inferences
- **This is a direct challenge to the project's existing reconciliation of Zhang 2013.** `SYNTHESIS.md` rescales Zhang's PFOA clearance with Chiu's fitted Vd of 430 mL/kg, gets 3.29 y, and concludes that Zhang and Chiu "agree to within 5% once they use the same Vd". Abraham's measured 121 mL/kg is 3.6x lower than Chiu's fitted value and is the more direct measurement - a known dose in a known body weight, with no exposure reconstruction. Substituting 121 mL/kg into Zhang's clearance gives roughly 0.93 y rather than 3.29 y, which breaks the reconciliation. The honest reading is that **the Vd disagreement is not settled, and which value is "right" decides whether Zhang's short half-life is an artefact or not.**
- Chiu's Vd is fitted jointly with the half-life from reconstructed intake, so it is not independent of either. A plausible reading is that the Bayesian fit absorbed under-estimated intake into an inflated Vd. That is a hypothesis, not a finding.
- Across Abraham's 15 compounds, Vd is nearly constant up to C9 and then rises 3-fold by C12, while half-life *falls* from 2,011 d (PFOA, C8) to 295 d (PFDoDA, C12). Since t1/2 = ln2 x Vd / CL, the falling half-life at rising Vd means clearance rises ~20-fold across that range - consistent with Fischer 2025's prediction that long-chain elimination is governed by membrane permeability and phospholipid binding rather than renal transporters.

### Gaps
- There is no human Vd for PFHxS, PFNA or any short-chain compound from more than one individual. Abraham 2024 is n=1 for all fifteen.
- Thompson et al. 2010 was not retrieved, so the transposition conflict cannot be resolved here. It should be checked directly before any further rescaling of Zhang 2013.
- No controlled-removal study (Gasiorowski 2022, Genuis 2014, Delaere 2025, Moller 2024) reports a Vd, despite having the data to compute one.
