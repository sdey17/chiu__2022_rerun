# PFAS volume of distribution across species, and whether PFAS elimination is dose- or concentration-dependent (saturable)

Companion data files written alongside these notes:
- `../../db/vd_clearance.csv` — 100+ rows of Vd / CL / half-life with method and provenance flags
- `../../db/dose_dependence.csv` — every multi-dose study found, with half-life and clearance at each dose
- `../../papers/SOURCES_vd_dose.md` — retrieval log, including every failure

Does not duplicate: `../../../species_dose/` (EPA-fitted animal PK, cross-species dose test),
`../../../pfas_dose/` (within-male-rat PFOA/PFHxA dose slope), `../../../literature/APPRAISAL.md` §8
(Zhang 2013 Vd issue). This extends those with primary-literature provenance and the multi-dose studies.

---

## Q1. Reported Vd values by chemical and species, with method

### Takeaway
Across every species for which a Vd has been measured — **including humans** — PFAS Vd is small:
roughly 0.11–0.7 L/kg, i.e. below total body water in the rat (0.668 L/kg), with one systematic
exception: Vd computed from *subchronic steady-state* data in monkeys comes out 7–25× larger
(1.3–6.3 L/kg). The split is not between species; it is between methods.

### Cited Findings
- **A measured human Vd exists and had been missing from the regulatory chain.** A single healthy
  male volunteer (age 67, ~82 kg) orally ingested a mixture of fifteen mostly ¹³C-labelled PFAS
  (3.7–19.6 µg each) and was followed for 450 days in plasma, urine and feces, with Vd computed as
  D_abs/C₀ from a two-compartment fit. Measured Vd (mL/kg bw, point estimate [95% CI]):
  **PFOA 121 [118–124]**, PFOS 152 [148–NA], PFHxS 125 [122–128], PFNA 124 [122–127],
  PFBA 132 [128–136], PFPeA 110 [107–115], PFHxA 119 [113–126], PFHpA 128 [125–131],
  PFDA 184 [180–188], PFUdA 241 [232–252], PFDoA 354 [342–368], PFBS 137 [134–140],
  HFPO-DA 177 [172–183], DONA 168 [140–212], 6:2 FTS 119 [115–122]. Gastrointestinal absorption was
  essentially complete (0.00–1.40% unabsorbed, measured in feces) — Abraham K, Mertens H, Richter L,
  Mielke H, Schwerdtle T, Monien BH, *Environ Int* 2024;193:109047, PMID 39476597,
  [doi:10.1016/j.envint.2024.109047](https://doi.org/10.1016/j.envint.2024.109047), Tables 2–3
  (local: `papers/Abraham 2024 single oral dose 15 PFAS kinetics volunteer.txt`).
- The Abraham dataset is internally consistent to a degree no other Vd source is: substituting each
  compound's Vd and total clearance into t½ = ln2·Vd/CL back-solves to an implied body weight of
  **81.4–83.1 kg for all fifteen compounds** (my calculation), confirming that Vd, kel, half-life and
  CL_tot in that paper are one coherent set rather than independently reported numbers.
- Mouse PFBS Vd 0.32–0.40 L/kg, "similar between the two sexes", with t½ 5.8 h (males) and 4.5 h
  (females) after 30 or 300 mg/kg oral gavage in CD-1 mice — Lau et al. 2020 abstract
  (`papers/Lau 2020 PFBS mouse PK.txt`).
- The single best published provenance table is OEHHA's Table 4.8.1, which lists reference, *data source*, species, Vd and *method* for 15 PFOA/PFOS Vd studies — [OEHHA 2024 PHG §4.8, pp. 53–55](https://oehha.ca.gov/water/public-health-goal/final-public-health-goals-perfluorooctanoic-acid-and-perfluorooctane) (local copy: `papers/OEHHA 2024 PFOA PFOS PHG.txt` lines 2705–2840).
- **Single-dose, non-compartmental or compartmental fits (the credible group):** PFOA monkey 181 mL/kg (M) / 198 (F), single IV 10 mg/kg, Vd = Dose·AUMC/AUC² (Butenhoff et al. 2004a); PFOA rat 196 (M) / 201 (F) mL/kg, single IV, 2-compartment (Ohmori et al. 2003, [doi:10.1016/s0300-483x(02)00573-5](https://doi.org/10.1016/s0300-483x(02)00573-5)); PFOA rat 211–264 mL/kg (Kemper 2003, unpublished); PFOA rat 112 (M) / 171 (F) mL/kg IV and 106/154 oral (Kim et al. 2016b); PFOA mouse 180 (M) / 150 (F) mL/kg, IV, 2-compartment, Vd = Dose/C(0) (Fujii et al. 2015); PFOS monkey 202 (M) / 274 (F) mL/kg (Chang et al. 2012); PFHxS monkey 287 (M) / 213 (F) mL/kg (Sundström et al. 2012) — all per [OEHHA 2024 PHG Table 4.8.1](https://oehha.ca.gov/water/public-health-goal/final-public-health-goals-perfluorooctanoic-acid-and-perfluorooctane) and [ATSDR 2021 Tables A-3, 3-6](https://www.atsdr.cdc.gov/toxprofiles/tp200.pdf).
- **NTP rat IV values (fully measured, both sexes, same strain and laboratory), summed over central and peripheral compartments:** PFOS 681 mL/kg (M, V1 417 + V2 264) and 421 (F, 297+124); PFHxS 224 (M, 88.4+136) and 144 (F, 66.3+77.6); PFBS 188 (M, 113+74.8) and 165 (F, 123+42) — [Huang et al. 2019, Toxicol Rep 6:645–655, Tables 2–4](https://doi.org/10.1016/j.toxrep.2019.06.016) (PMID 31334035), text extraction in `papers/Huang 2019 PFBS PFHxS PFOS rat multidose toxicokinetics.txt`.
- The NTP authors make the interpretive point explicitly: "the volume of distribution for all PFAS in this study was below the aqueous volume of total body water in rats (668 mL/kg)… these results support the previous literature indicating that PFAS remain in the plasma, likely due to their high binding affinity to serum albumin" — [Huang et al. 2019, Discussion](https://doi.org/10.1016/j.toxrep.2019.06.016).
- **Subchronic steady-state values (the discrepant group):** PFOA monkey 1,810–5,210 mL/kg (M) and 2,460–6,340 (F) from Washburn et al. 2005 using Noker (unpublished) data; 1,260–3,730 mL/kg from Butenhoff et al. 2002 data; 1,300–4,470 mL/kg from the 6-month arm of Butenhoff et al. 2004a re-analysed by Vestergren & Cousins 2009; 1,480–4,470 mL/kg in rhesus monkey from Griffith & Long 1980 — [OEHHA 2024 PHG Table 4.8.1](https://oehha.ca.gov/water/public-health-goal/final-public-health-goals-perfluorooctanoic-acid-and-perfluorooctane).
- **PFHxA is the outlier chemical.** EPA computed Vd,β = CL/β and got 1.36 L/kg averaged over rat experiments (male 1.37, female 1.35 — "virtually indistinguishable"), 0.75/0.78 L/kg in male/female mice, and 0.99 ± 0.58 / 0.47 ± 0.35 L/kg in male/female monkeys (Chengelis et al. 2009a, n = 3 per sex) — [EPA 2023 IRIS PFHxA Toxicological Review §5.2.1, pp. 5-12 to 5-13](https://iris.epa.gov/).
- Chiu et al. 2022's Bayesian human fits give larger values than any single-dose animal measurement: PFOA 0.43, PFOS 0.32, PFHxS 0.29, PFNA 0.19 L/kg — `../../../species_dose/animal_pk.csv` (from Chiu 2022 Table 3).

### Inferences
- The method, not the species, drives the spread. Within the single-dose literature, every mammal lands in 0.1–0.7 L/kg; every steady-state monkey calculation lands in 1.3–6.3 L/kg. The two groups do not overlap and the gap is ~10×.
- A Vd of 0.1–0.3 L/kg is approximately extracellular water, which is physically consistent with >98% plasma protein binding (Ohmori et al. 2003 abstract). A Vd of 4–6 L/kg would require most of the body burden to sit in tissue, which the measured tissue:plasma ratios below contradict. The single-dose group is therefore the mechanistically coherent one.

- With Abraham's measured human values in hand, the human/animal Vd comparison is now direct and
  close: human PFOA 121 mL/kg against rat 112–264, monkey 181–198, mouse 150–180; human PFOS
  152 mL/kg against rat 280–681, monkey 202–274; human PFHxS 125 mL/kg against monkey 213–287 and
  rat 144–224. Human Vd is at or slightly below the animal range for every chemical where both exist.
  This vindicates EPA's assumption (Q5) that Vd is conserved across mammals — **but it falsifies
  EPA's specific PFHxA number**, where the human Vd was assumed equal to the monkey's 730 mL/kg and
  the measured human value is 119 mL/kg, 6.1× lower.

### Gaps
- Numeric Vd for PFNA and PFDA in any species was not recovered from a primary source. Ohmori et al. 2003's abstract states only that "Distribution volumes in steady state (Vss) were not much different between PFCAs and between the sexes"; the per-compound table was not obtained (paywalled). ATSDR's assumption that human PFNA Vd = PFOA Vd = 0.2 L/kg rests entirely on that one qualitative sentence.
- No PFAS Vd was found for pig, hamster, rabbit or dog. Numata 2014 (pig) was not retrieved.

---

## Q2. Which Vd values are MEASURED and which are ASSUMED — the provenance chain

### Takeaway
The PFOA Vd of 170 mL/kg and PFOS Vd of 230 mL/kg in near-universal regulatory use are **not
measurements**. They come from Thompson et al. 2010, an Australian *exposure-reconstruction* paper
that back-calculated Vd from a US drinking-water cohort under a steady-state assumption and an
*assumed* half-life; the PFOS value is the PFOA value multiplied by 1.35, a factor lifted from a
monkey PBPK model's central-compartment volume. Every downstream citation inherits both the
assumption and the circularity.

### Cited Findings
- **Thompson et al. 2010 is the origin.** Its own abstract: "A volume of distribution was calibrated for PFOA to a value of 170 ml/kg bw using data from two communities in the United States where the residents' serum concentrations could be assumed to result primarily from a known and characterized source, drinking water contaminated with PFOA by a single fluoropolymer manufacturing facility. **For PFOS, a value of 230 ml/kg bw was used, based on adjustment of the PFOA value.**" — Thompson J, Lorber M, Toms LML, Kato K, Calafat AM, Mueller JF, *Environ Int* 2010;36(4):390–397, PMID 20236705, [doi:10.1016/j.envint.2010.02.008](https://doi.org/10.1016/j.envint.2010.02.008). (According to PubMed.)
- **The actual arithmetic**, reconstructed by OEHHA: Vd = Dose × T½ / (Css × ln2), with drinking water at 500 ng/L in Lubeck and 3,550 ng/L in Little Hocking, serum concentrations from **Emmett et al. 2006** (448 ng/mL for "Little Hocking system water only", n = 291; 68 ng/mL for non-occupationally exposed Lubeck residents, n = 12), 1.4 L/day water intake, absorption efficiency 0.91, and an **assumed** T½ of 2.3 years — [OEHHA 2024 PHG §4.8, p. 57](https://oehha.ca.gov/water/public-health-goal/final-public-health-goals-perfluorooctanoic-acid-and-perfluorooctane).
- **The PFOS 1.35 factor.** "Citing the lack of credible studies for a PFOS Vd, US EPA adopted the following strategy. Starting with the PFOA Vd of 170 ml/kg, a factor of 1.35 was applied based on the observation in the modeling paper of Andersen et al. (2006) that the optimized Vdc value for PFOS was 20–50% higher than the PFOA value. Thus, US EPA estimated a human PFOS Vd value of 230 ml/kg." OEHHA's objection: "Relying on a modeling study would not be optimal since compartment volumes are only some of the optimized parameters… Moreover… Vdc values determined in this study were not representative of the Vd, but rather of volume of the central compartment" — [OEHHA 2024 PHG §4.8, p. 56](https://oehha.ca.gov/water/public-health-goal/final-public-health-goals-perfluorooctanoic-acid-and-perfluorooctane).
- **EPA 2024 still carries 170 mL/kg forward unchanged**, citing Thompson et al. 2010a in Table 4-6, and derives clearance from it: "Volume of Distribution (mL/kg) … 170b … b Thompson et al. (2010a)"; "Cl = Vd × ln(2)/t½" — [EPA 2024 Final Human Health Toxicity Assessment for PFOA, Table 4-6](https://www.epa.gov/sdwa/) (`papers/EPA 2024 PFOA human health toxicity assessment.txt` line 18411). The same text states "In humans, the volume of distribution (Vd) for PFOA has been **assigned** values between 170 and 200 mL/kg" (§3.3.1.2.5).
- **OEHHA's re-run of Thompson's own method, with better serum data, gives 225 mL/kg.** Substituting C8 Science Panel serum (Frisbee et al. 2009: 227.58 ng/mL Little Hocking, 92.36 ng/mL Lubeck, 82–87% population coverage) for Emmett's volunteer-enriched sample yields 335 mL/kg (Little Hocking) and 116 mL/kg (Lubeck), average 225 mL/kg. OEHHA argues Emmett's "preliminary selection of households… may have introduced unaccounted for bias toward higher than average levels in plasma" — [OEHHA 2024 PHG §4.8, p. 57](https://oehha.ca.gov/water/public-health-goal/final-public-health-goals-perfluorooctanoic-acid-and-perfluorooctane).
- **Harada's 0.3 L/kg** (the value in ATSDR Table A-3) is from Harada K et al. 2005, *Environ Res* 99:253–261, PMID 16194675, [doi:10.1016/j.envres.2004.12.003](https://doi.org/10.1016/j.envres.2004.12.003). That paper measured *renal clearances* in 20 Kyoto subjects and found them "10⁻⁵-fold smaller than the glomerular filtration rate in humans, suggesting the absence of active excretion in human kidneys"; its 0.3 L/kg is a one-compartment model parameter applied to literature half-lives, not an independent Vd measurement. (According to PubMed.) A separate Harada et al. 2003 monkey PFOS value of 300 mL/kg is flagged by OEHHA as arithmetically wrong — re-running the authors' own inputs (Seacat et al. 2002: Css = 16 mg/L at 0.03 mg/kg/d and 80 mg/L at 0.15 mg/kg/d, T½ = 200 d) gives **541 mL/kg**, and correcting for non-attainment of steady state (exposure lasted only ~1 half-life) gives **1,080 mL/kg** — [OEHHA 2024 PHG Table 4.8.1 footnote a](https://oehha.ca.gov/water/public-health-goal/final-public-health-goals-perfluorooctanoic-acid-and-perfluorooctane).
- **ATSDR's human Vd values are all transferred from monkeys**, stated plainly: "Estimates of volume of distribution (Vd) are based on non-compartmental modeling of serum concentration kinetics in monkeys and are assumed to be applicable to humans at the above serum concentrations" — [ATSDR 2021, Appendix A, p. A-12](https://www.atsdr.cdc.gov/toxprofiles/tp200.pdf). Table A-4 footnotes: PFOA/PFOS/PFNA Vd = 0.2 L/kg "Estimates based on studies in nonhuman primates (Butenhoff et al. 2004c; Chang et al. 2012; Harada et al. 2005a)"; PFHxS 0.287 L/kg "based on studies in nonhuman **male** primates (Sundström et al. 2012)". PFNA is the weakest link: "Based on this, the estimated volume of distribution for PFNA in humans **will be assumed to be the same for PFOA**, 0.2 L/kg" (p. A-13).
- **Loccisano's human PBPK models do not measure Vd or transport, they impose a half-life.** "Values for the affinity constant (KT) and maximum (Tm) for tubular reabsorption were optimized to plasma concentration kinetics in monkeys. The value for KT in monkeys was used in the human model. **The value for Tm for PFOA in humans was set to yield a plasma elimination t½ of 2.3 or 3.8 years** … The value for Tm for PFOS in humans was set to yield a plasma elimination t½ of 5.4 years… **Tissue-plasma partition coefficients used in both models were derived from observations in rodents** and were the same in the monkey and human models." — [ATSDR 2021 §3.1.5.2, p. 611](https://www.atsdr.cdc.gov/toxprofiles/tp200.pdf).
- **Tan, Clewell & Andersen 2008 is a structural, not a parametric, contribution.** EPA describes it as "an earlier 'biologically motivated' model that served as a bridge between a one-compartment model and PBPK by implementing a tissue compartment…, an absorption compartment, and a renal filtrate compartment with saturable renal resorption (Tan et al., 2008). The work of Tan et al. (2008) was a development of the earlier work of Andersen et al. (2006)" — [EPA 2024 PFOA assessment §3.3.2.3](https://www.epa.gov/sdwa/).
- **Andersen et al. 2006's reported Vd is a central-compartment volume only**: Vdc = 140 mL/kg (PFOA) and 220 mL/kg (PFOS), with k12 = 3.3/h and k21 = 0.1/h. OEHHA computed the implied tissue volume as Vdt = k12·Vdc/k21 (the formula from Wambaugh et al. 2013), giving Vdt of 4,620 and 7,260 mL/kg and total Vd of 4,800 and 7,500 mL/kg; OEHHA then rejects these: "these Vd values are subject to many uncertainties, and are less reliable than Vd values directly estimated from experimental data" — [OEHHA 2024 PHG Table 4.8.2](https://oehha.ca.gov/water/public-health-goal/final-public-health-goals-perfluorooctanoic-acid-and-perfluorooctane).
- **Wambaugh et al. 2013 deliberately bounded Vd rather than estimating it freely**: "Wambaugh et al. (2013) **constrained the total Vd such that the amount in the tissue compartment was not greater than 100 times that in the serum**… the ratio of the two volumes (serum versus total) was estimated in place of establishing a rate of transfer from the tissue to serum" — [EPA 2024 PFOA assessment §3.3.2.2](https://www.epa.gov/sdwa/). Its fitted central-compartment volumes (Table 4-3) are 0.18 (CD1 mouse F), 0.17 (C57BL/6 mouse F), 0.14 (rat F), 0.15 (rat M), 0.40 L/kg (monkey), with volume ratios RV2:V21 of 1.07, 53, 9.2, 8.4 and 0.98.
- **Kemper 2003, which underpins the rat calibration of Wambaugh 2013 and Worley & Fisher 2015, is an unpublished DuPont/Haskell study.** EPA: "The PK data that supported the Wambaugh et al. (2013) analysis were derived from two in vivo PFOA PK studies. The monkey PK data were derived from Butenhoff et al. (2004b), and the data for the rats (M/F) were from Kemper et al. (2003)" — [EPA 2024 PFOA assessment §3.3.2.2](https://www.epa.gov/sdwa/).

### Inferences
- The provenance chain for the 170 mL/kg figure is: *assumed half-life (2.3 y) + steady-state assumption + a volunteer-enriched serum sample (Emmett 2006) + an assumed 0.91 absorption fraction* → Vd. Any downstream use of that Vd to compute a clearance and then a half-life (EPA 2024 Table 4-6 does exactly this: "Cl = Vd × ln(2)/t½") is circular with respect to the half-life, and the assumed absorption fraction and steady state remain unvalidated.
- The 1.35 PFOS-to-PFOA scaling is doubly indirect: it transfers a *ratio of fitted central-compartment volumes in monkeys* onto a *steady-state total Vd derived in humans*. These are not the same quantity, which is OEHHA's objection.
- Loccisano's human model cannot be used as independent evidence about human Vd or human half-life, because the human transport maximum was set to reproduce the half-life, and the partition coefficients came from rodents. Any paper that cites Loccisano for a "PBPK-derived" human Vd is citing an assumption.

### Gaps
- Thompson et al. 2010 full text was not obtained (Elsevier paywall; not in PMC). The reconstruction above rests on the abstract plus OEHHA's account. OEHHA's reconstruction uses Emmett's 448 ng/mL for Little Hocking, but it is not certain from the abstract alone which of Emmett's three reported means (448, 478, 321 ng/mL) Thompson used, nor exactly which body weight.
- Numeric Tm and KT from Andersen et al. 2006 were not retrieved (see `papers/SOURCES_vd_dose.md`); only OEHHA's restatement of Vdc, k12 and k21.
- Numeric Loccisano Tm, KT and partition coefficients were not retrieved from the primary papers.

---

## Q3. Why do published human PFOA Vd values span ~sixfold (74 to 430 mL/kg), and which are credible?

### Takeaway
Because each estimate is a ratio of two quantities, and almost every one of them assumes at least
one of the two. The spread is a spread of *assumptions about half-life, steady state, absorption
fraction and which serum sample to believe* — not a disagreement about measurement.

### Cited Findings
| Value (mL/kg) | Source | What was actually assumed |
|---|---|---|
| 74 (PFOA), 93 (PFOS) | Andersson et al. 2025, measured | per `../../../literature/APPRAISAL.md` §8; not re-verified in this pass |
| 170 | Thompson et al. 2010, [PMID 20236705](https://doi.org/10.1016/j.envint.2010.02.008) | T½ = 2.3 y assumed; steady state assumed; fa = 0.91; Emmett 2006 serum |
| 200 | ATSDR 2021 Table A-4 | transferred from monkey single-dose Vd |
| 225 | OEHHA 2024 | Thompson's method with Frisbee 2009 serum instead of Emmett 2006 |
| 300 | Harada et al. 2005 / Niisoe et al. 2010 | 1-compartment model parameter; Niisoe assumed 0.88 biliary reabsorption and T½ = 3.5 y |
| 430 | Chiu et al. 2022 Bayesian fit | fitted jointly with half-life from 13 serum-decay studies |
| 464–780 | Vestergren & Cousins 2009 | 95% CI of an intake–serum regression under steady state |
| **121 [118–124]** | **Abraham et al. 2024, [PMID 39476597](https://doi.org/10.1016/j.envint.2024.109047)** | **nothing assumed: measured dose, measured fecal non-absorption, measured plasma decay over 450 d; n = 1** |

- The unique strength of the Chiu 2022 value is that Vd and half-life were fitted *jointly* to serum decay, so neither is assumed — but it is correspondingly sensitive to the background-exposure and cohort problems documented in `../../../literature/APPRAISAL.md` §§1–7.
- The Vestergren & Cousins 464–780 mL/kg range and the Washburn/Butenhoff monkey 1,300–6,340 mL/kg values share one feature: all are steady-state calculations in which the measured steady-state serum came out *lower than expected for the dose*. Butenhoff et al. 2004a's own explanation was not a large Vd: "the plasma levels at steady state were lower than expected, which would drive the corresponding Vd values higher. The authors suggested that this could be due to incomplete absorption (due to the fact that fecal PFOA dropped dramatically when the dietary exposure stopped), and secondly, due to the possibility that some PFOA retained in the body could be trapped in the enterohepatic loop and therefore be absent from the plasma pool" — [OEHHA 2024 PHG §4.8, p. 57](https://oehha.ca.gov/water/public-health-goal/final-public-health-goals-perfluorooctanoic-acid-and-perfluorooctane).
- OEHHA's own verdict on the monkey steady-state approach: "none of the available subchronic monkey studies included controls to account for less than complete absorption and enterohepatic circulation. The uncertainty in the outcome of this approach also sheds light on the limitations of the steady state assumption" — same source.
- **An independent, non-PK handle exists: the Gasiorowski 2022 randomised trial.** 285 Australian firefighters; plasma arm donated "up to 800 mL every 6 weeks for a total of up to 9 plasma donations", blood arm "approximately 470 mL of blood every 12 weeks for a total of up to 5 donations". Mean serum PFOS fell 2.9 ng/mL (95% CI −3.6 to −2.3) in the plasma arm and 1.1 ng/mL (−1.5 to −0.7) in the blood arm, from baselines of 11.7 and 10.9 ng/mL; the observation arm was "unchanged" — [Gasiorowski et al. 2022, JAMA Netw Open 5(4):e226257](https://doi.org/10.1001/jamanetworkopen.2022.6257), PMID 35394514. (According to PubMed.)

### Inferences
- **My own mass-balance derivation from Gasiorowski 2022** (this is an inference, not a published number; row flagged as such in `vd_clearance.csv`):
  - Plasma arm: 9 × 0.8 L = 7.2 L plasma removed; mean serum over the year ≈ (11.7 + 8.8)/2 ≈ 10.2 ng/mL → ≈ 73.4 µg PFOS removed. Observed ΔC_serum = 2.9 ng/mL → Vd = 73.4 µg / 2.9 ng/mL ≈ 25.3 L; at BW ≈ 88 kg (BMI 27.9) → **≈ 288 mL/kg**.
  - Blood arm: 5 × 0.47 L = 2.35 L whole blood; whole-blood PFOS ≈ serum/2 (the authors state "serum PFAS levels are approximately 2 times higher" than whole blood) → ≈ 12.2 µg removed. ΔC = 1.1 ng/mL → Vd ≈ 11.0 L → **≈ 126 mL/kg**.
  - The two arms disagree by 2.3×, which bounds the method's precision. But both land inside 0.13–0.29 L/kg, i.e. **the trial independently supports the small-Vd (single-dose, extracellular-water) group and not the 0.46–6.3 L/kg steady-state group.** Since this estimate uses no assumed half-life and no assumed absorption fraction, it is methodologically the cleanest human constraint found.
- Credibility ranking that follows: **(1) Abraham et al. 2024's directly measured 121 mL/kg** — the only human value with no assumed parameter, and corroborated by (2) the human removal mass balance (Gasiorowski-derived, 0.13–0.29 L/kg) and single-dose IV measurements in animals (0.1–0.7 L/kg); (3) Thompson/EPA 0.17 and ATSDR 0.20, credible in magnitude but assumption-laden; (4) Chiu 2022's jointly fitted 0.43 L/kg, 3.6× the measured value; (5) steady-state monkey and intake–serum-regression values (0.46–6.3 L/kg), which OEHHA, the original authors and the mass-balance evidence all argue against.
- The sixfold spread is therefore better read as a ~2–3× real uncertainty (0.12–0.43 L/kg) plus one systematically biased method — and the measured anchor sits near the bottom of that range, so the commonly used 170 mL/kg is closer to right than the 430 mL/kg Bayesian fit. Note the tension this creates with `../../../literature/APPRAISAL.md` §8, which treats Chiu's 0.43 L/kg as the comparator; Abraham's measurement supports Andersson's low value (0.074 L/kg) in direction, though it is 1.6× higher.
- Abraham's single-subject design is simultaneously its strength and its weakness: n = 1 gives no between-person variance, so the narrow 95% CIs (±3%) are within-fit precision only and say nothing about population spread. But because the compound was ¹³C-labelled, the measurement is immune to the background-exposure confounding that afflicts every cohort-based estimate (`../../../literature/APPRAISAL.md` §§1–2).

### Gaps
- No haemodialysis PFAS-removal study was retrieved. Such a study would give a second, independent mass-balance handle.
- The body weight in my Gasiorowski derivation is assumed (the paper reports BMI 27.9 but not weight), and the number of donations actually completed per participant is reported only as "up to". Both push the derived Vd in the same direction (fewer donations or lower weight → lower Vd), so 288 mL/kg should be read as an upper bound for that arm.

---

## Q4. Does Vd vary with dose or serum concentration? (The binding-saturation prediction)

### Takeaway
The binding-saturation argument predicts apparent Vd should **rise** with dose as albumin sites fill
and free fraction increases. **The measured direction is the opposite.** In rats, apparent Vd and
tissue partitioning both *fall* with increasing dose for PFOA and PFOS, because the high-affinity
*hepatic* uptake/binding saturates first, pushing the chemical back into plasma.

### Cited Findings
- **Direct measurement, PFOA, rat, 400× dose range.** At 2 h after IV dosing, 52% of the dose was in liver at 0.041 mg/kg versus only 27% at 16.56 mg/kg; "larger proportion of PFOA dosed was distributed to serum, other tissues and carcass at the high dose compared with the low dose." Within the liver, the cytosolic (105,000 g supernatant) share rose from 3% to 43% of hepatic PFOA. Authors: "PFOA is preferentially taken-up by the liver, and distributed to membrane fractions… and hardly excreted into bile when exposed at very low dose" — Kudo N, Sakai A, Mitsumoto A, Hibino Y, Tsuda T, Kawashima Y, *Biol Pharm Bull* 2007;30(8):1535–1540, PMID 17666816, [doi:10.1248/bpb.30.1535](https://doi.org/10.1248/bpb.30.1535). (According to PubMed.)
- **PFOS, rat, NTP, same strain and sex.** Apparent V1 fell from 280 mL/kg at 2 mg/kg to 34.6 mL/kg at 20 mg/kg in males (417 → 34.6 including the IV point), and 222 → 27.9 mL/kg in females; V1+V2 fell 524 → 78.5 (M) and 315 → 55.1 (F) — [Huang et al. 2019 Table 4](https://doi.org/10.1016/j.toxrep.2019.06.016).
- **PFBS and PFHxS, rat, NTP: the opposite sign.** Apparent V1 *rose* with dose — PFBS male 164 → 311 mL/kg over 4 → 100 mg/kg; PFHxS male 123 → 192 mL/kg over 4 → 32 mg/kg; PFHxS female 155 → 264 mL/kg — [Huang et al. 2019 Tables 2–3](https://doi.org/10.1016/j.toxrep.2019.06.016).
- **PFOA rat, NTP (Dzierlenga 2020):** oral Vd 154–202 mL/kg in males (1-compartment) and **79.2–342 mL/kg in females** (2-compartment, sum of central and peripheral) across the dose range; EPA's own summary notes "Peripheral Vd values were dramatically lower than central Vd values at all doses after oral administration and, interestingly, also after IV administration" — [OEHHA 2024 PHG Table 4.8.1](https://oehha.ca.gov/water/public-health-goal/final-public-health-goals-perfluorooctanoic-acid-and-perfluorooctane); [EPA 2024 PFOA assessment §3.3.1.2.5](https://www.epa.gov/sdwa/).
- **The albumin binding sites are not remotely full at any of these doses.** Harris & Barton (2008) modelled PFOS–albumin binding as saturable with Kd = 10⁻⁷ M and maximum capacity 4.1 × 10⁻⁴ M (= 410 µM) — [ATSDR 2021 §3.1.5.5, p. 620](https://www.atsdr.cdc.gov/toxprofiles/tp200.pdf). The highest rat Cmax in the NTP PFOS study was 0.21 mM = 210 µM, i.e. ~half of Bmax; at the 2 mg/kg dose it was 10 µM, ~2.4% of Bmax.
- **Free fraction is treated as a fitted constant, not a concentration-dependent quantity, in every model found.** Loccisano's rat PFOA free fraction is "assigned a constant of 4.5% in females and 0.6% in males… optimized to fit observed kinetics"; for PFOS the model needed a *time*-dependent (not concentration-dependent) free fraction falling from 2.2% to 0.1% with a 14 h half-time, and ATSDR notes "the physiological mechanism for a dependence of plasma binding on the time following dosing (i.e., not on concentration of PFOS in plasma or some other dose surrogate) has not been established" — [ATSDR 2021 §3.1.5.1, pp. 608–609](https://www.atsdr.cdc.gov/toxprofiles/tp200.pdf).
- **The decisive low-dose test: free fraction is NOT elevated at trace human concentrations.** Abraham et al. 2024 measured the fraction unbound in plasma (fup) in their volunteer at plasma concentrations of 0.19–2.27 ng/mL — four to five orders of magnitude below any animal study: PFOA 0.001, PFOS 0.0045, PFHxS 0.0009, PFNA 0.0016, PFHpA 0.0004, PFDA 0.0027, PFUdA 0.0148, PFBS 0.0046, PFHxA 0.0068, PFPeA 0.044, PFBA 0.093, 6:2 FTS 0.0143 — [Abraham et al. 2024 Table 4](https://doi.org/10.1016/j.envint.2024.109047). These are the *same order* as, or lower than, the free fractions fitted at high animal doses (Loccisano rat PFOA 0.6–4.5%; Worley & Fisher rat PFOA 0.09; Wambaugh monkey 0.01, rat 0.08, mouse 0.011–0.034). If binding saturation were shaping PFAS kinetics, free fraction would have to be *lower* at the low human concentration and *higher* at animal doses; it is not.
- **And measured human Vd is not elevated at trace dose either**: 121 mL/kg for PFOA at a Cmax of 0.659 ng/mL, at the low end of every published human value — [Abraham et al. 2024 Table 3](https://doi.org/10.1016/j.envint.2024.109047).
- ATSDR identifies the absence of a concentration-dependent free fraction as a known modelling limitation: "without basing distribution kinetics on the free concentration, it is not possible for concentration-dependent free fraction to be modeled" (criticising Harris & Barton) — [ATSDR 2021 §3.1.5.5, p. 622](https://www.atsdr.cdc.gov/toxprofiles/tp200.pdf).

### Inferences
- Two saturable processes compete, and they move apparent Vd in opposite directions: **plasma protein binding** saturating raises free fraction and should raise Vd; **hepatic uptake/binding** (L-FABP, membrane fractions) saturating lowers tissue:plasma and should lower Vd. Kudo 2007's measurements say the hepatic process saturates at a far lower concentration — the shift is already obvious between 0.041 and 16.56 mg/kg, whereas 210 µM plasma PFOS is still only half of albumin Bmax. So for PFOA and PFOS the hepatic term wins and Vd falls with dose.
- The PFBS/PFHxS rise in apparent V1 with dose is probably not a distribution effect at all. For an oral two-compartment fit, V1 is `Dose/(A+B)` and is really V1/F; in those two chemicals bioavailability F fell from 133%→46% (PFBS) and 98%→52% (PFHxS) across the dose range, which alone accounts for the apparent V1 rise of 1.9× and 1.6×. **Apparent Vd from oral data is uninterpretable as a distribution volume when F is dose-dependent.** The same caveat voids the PFOS 8× V1 fall as a literal statement about distribution, which is why Kudo 2007's tissue measurement, not the V1 column, is the load-bearing evidence here.
- Practical conclusion for the user's question: there is **no evidence that apparent Vd increases with dose or serum concentration in the way the albumin-saturation story requires**, and the one direct tissue-distribution measurement across a 400× dose range runs the other way. At human environmental concentrations the predicted change is in any case negligible (see Q8).

- Taken together with Abraham's fup and Vd measurements, the binding-saturation explanation fails from both ends: at animal doses the apparent Vd goes *down*, not up (Kudo 2007), and at human trace doses the free fraction and the Vd are *not* different from the animal values at all. There is no concentration range in the available data over which protein-binding saturation visibly changes PFAS distribution.

### Gaps
- No *single* study was found that measures PFAS free fraction at two or more concentrations within one assay and one species. Abraham's human fup values and the animal model fup values are comparable only across papers and across methods (ultrafiltration versus model fitting), so the comparison above is suggestive rather than a measured dose–response. The free-fraction-versus-concentration curve from one laboratory still appears not to exist. (`Ryu 2024 unbound fractions PFAS rodent tissues.txt` and the albumin-binding files in `papers/` may bear on this; they are another researcher's scope and were not mined here.)
- Kudo 2007's full tables (tissue concentrations, not just percentages of dose) were not retrieved, so an apparent Vd at each dose cannot be computed from that paper.

---

## Q5. Does Vd or clearance explain the species differences? (half-life = ln2 · Vd / CL decomposition)

### Takeaway
Clearance, overwhelmingly. Vd varies by only 2–4× across mouse, rat, monkey and human for a given
PFAS and does not even order with half-life; clearance varies by 20–2,500×. In every pairwise
decomposition the Vd factor contributes less than a factor of 2.6 and the CL factor contributes
6–2,564×.

### Cited Findings
- Using the EPA/Chiu fitted values in `../../../species_dose/animal_pk.csv` (Chiu et al. 2022 Table 3 for humans; EPA animal PK model for animals, [doi:10.1016/j.taap.2025.117336](https://doi.org/10.1016/j.taap.2025.117336)), the identity t½ = ln2·Vd/CL closes to within 1–3% for every animal row, confirming the three quantities are internally consistent and can be decomposed:

| chemical | comparison | Vd(human)/Vd(animal) | CL(animal)/CL(human) | product | observed t½ ratio |
|---|---|---|---|---|---|
| PFOA | human vs male rat | 1.49× | 58× | 86× | 81× |
| PFOA | human vs female rat | 0.66× | 2,564× | 1,699× | 1,662× |
| PFOA | human vs male monkey | 2.40× | 42× | 100× | 100× |
| PFOA | human vs male mouse | 1.71× | 27× | 46× | 45× |
| PFOS | human vs male rat | 0.72× | 30× | 22× | 22× |
| PFOS | human vs male monkey | 1.51× | 6× | 9× | 9× |
| PFOS | human vs male mouse | 1.12× | 31× | 35× | 35× |
| PFHxS | human vs male rat | 1.44× | 72× | 104× | 102× |
| PFHxS | human vs male monkey | 1.07× | 18× | 19× | 17× |
| PFNA | human vs male rat | 0.79× | 22× | 17× | 16× |

  Implied human clearances (from Vd and half-life): PFOA 0.260, PFOS 0.181, PFHxS 0.066, PFNA 0.153 mL/kg/d.
- Within animals alone, the fitted Vd range for a given PFAS is 2.1× (PFOS), 2.4× (PFHxS), 3.2× (PFNA), 3.8× (PFOA); the fitted CL range is 60×, 84×, 21× and 143× respectively — computed from `../../../species_dose/animal_pk.csv`.
- **EPA reaches the same conclusion independently and uses it to set a regulatory value.** Comparing options for extrapolating PFHxA to humans, EPA weighed "whether it is more reasonable to expect CL or Vd to be similar in humans as in experimental animals", did a read-across using PFHxS, PFNA and PFOA human clearances from Zhang et al. 2013b (median urinary CL 0.015, 0.094 and 0.19 mL/kg/d respectively, in men and women over 50) against rat values (PFHxS total CL 7–9 mL/kg/d; PFOA 9–16 mL/kg/d; PFNA 2–66 mL/kg/d male rat), and concluded: "The alternative, option (2) above, requires one to accept that the **Vd in humans is roughly two orders of magnitude higher than in rats and monkeys**, although the biochemical factors that determine serum-tissue partitioning are expected to be conserved across mammalian species… Hence, option (2) seems highly unlikely… **the reasonable expectation, based on data from multiple chemicals, is the volume of distribution in humans does not substantially differ from that in experimental animals**" — [EPA 2023 IRIS PFHxA Toxicological Review §5.2.1, pp. 5-15 to 5-16](https://iris.epa.gov/).
- Human renal clearance is ~10⁵-fold below GFR: "The renal clearances were 10⁻⁵-fold smaller than the glomerular filtration rate in humans, suggesting the absence of active excretion in human kidneys. The renal clearances of PFOA and PFOS were approximately one-fifth of the total clearance based on their serum half-lives" — Harada et al. 2005, [doi:10.1016/j.envres.2004.12.003](https://doi.org/10.1016/j.envres.2004.12.003). (According to PubMed.)
- The mechanism for the clearance differences is transporter-level, not size-related: OAT1/OAT3 (basolateral, secretion) and OATP1a1 (rat) / OAT4 and URAT1 (human) (apical, reabsorption); "Affinity of rat OATP1a1 is strongly correlated with total clearance in rats (r² = 0.98; Yang et al. 2009)" — [ATSDR 2021 §3.1.4, pp. 602–603](https://www.atsdr.cdc.gov/toxprofiles/tp200.pdf).
- The 44× male/female rat PFOA clearance difference occurs at identical dose and identical Vd (Ohmori 2003: 196 vs 201 mL/kg, CL 135 vs 2,233 mL/d/kg) — proving clearance can move two orders of magnitude with Vd held fixed.

### Inferences
- The decomposition is unambiguous: the human/animal half-life gap is a clearance gap. The Vd term never exceeds 2.6× and in four of ten comparisons points the *wrong* way (human Vd smaller than the animal's).
- This also means a mis-specified Vd propagates straight into any clearance-based half-life estimate (`../../../literature/APPRAISAL.md` §8 makes the same point), but it cannot generate the species difference — the Vd values are simply not far enough apart.
- Because Vd is essentially species-invariant while clearance is not, EPA's choice to scale PFHxA by clearance rather than Vd is the defensible one, and the same logic should apply to any PFAS.

- **The decomposition redone with Abraham's measured human values** (Vd in mL/kg, CL in mL/kg/d, both measured in the same subject) tightens the conclusion considerably:

| chemical | human Vd (measured) | human CL (measured) | Vd(human)/Vd(male rat) | CL(male rat)/CL(human) | observed t½ ratio |
|---|---|---|---|---|---|
| PFOA | 121 mL/kg | 0.0417 mL/kg/d | 0.42× (vs rat 289) | 361× (vs rat 15.07) | 142× (2011 d vs 14.2 d) |
| PFOS | 152 mL/kg | 0.0870 mL/kg/d | 0.34× (vs rat 442) | 63× (vs rat 5.51) | 21× (1211 d vs 57.1 d) |
| PFHxS | 125 mL/kg | 0.0530 mL/kg/d | 0.62× (vs rat 202) | 90× (vs rat 4.79) | 55× (1634 d vs 29.7 d) |
| PFNA | 124 mL/kg | 0.0659 mL/kg/d | 0.52× (vs rat 240) | 50× (vs rat 3.31) | 24× (1305 d vs 53.7 d) |

  Human Vd (Abraham) and rat Vd (Chiu/EPA fits); human CL from Abraham Table 4; rat CL and t½ from `../../../species_dose/animal_pk.csv`.
  **With measured rather than fitted human Vd, the Vd term now works *against* the long human half-life in every case** (human Vd is 0.34–0.62× the rat's), so clearance has to carry more than the whole gap — 50–361× — not less.
- A second, within-subject version of the same point: across Abraham's PFCA homologue series, Vd rises monotonically (PFOA 121 → PFDA 184 → PFUdA 241 → PFDoA 354 mL/kg, a 2.9× span) while half-life *falls* (2011 → 862 → 584 → 295 d) because clearance rises 20× (0.0417 → 0.832 mL/kg/d). Within one human, one assay and one day of dosing, Vd and half-life move in **opposite** directions. Clearance decides.

### Gaps
- The animal Vd values in both decomposition tables are *fitted* (Chiu/EPA animal PK model), not measured, so the Vd ratios mix a measured human value against fitted animal values. Substituting the measured single-dose animal Vd values from Q1 instead (rat PFOA 112–264, PFOS 280–681 mL/kg) changes the Vd ratios by up to ~2× but never changes their sign or the conclusion.
- There is no measured human clearance for PFBA, PFPeA, PFDoA or the alternative PFAS in any species other than Abraham's single subject, so the decomposition cannot be extended to the short-chain and replacement compounds.
- Nothing found explains *why* human clearance is 50–360× below the rat's at concentrations where no transporter is saturated. The transporter-abundance and transporter-affinity explanations in the literature are supported only by fitted relative activity factors (Q8), which restate rather than explain the observation.

---

## Q6. Tissue:serum partition coefficients, and rat vs mouse

### Takeaway
All measured tissue:plasma ratios for PFAS are ≤ ~4, with liver highest, kidney ~0.3–1.5 and brain
0.01–0.13 — far too low to support a large Vd. Liver partitioning rises with chain length and is
consistently higher in male than female rats. Rat-versus-mouse partition coefficients were not
found side by side; the available side-by-side comparison is rat versus human.

### Cited Findings
- **NTP rat, measured tissue:plasma ratios in the same strain and laboratory** — [Huang et al. 2019](https://doi.org/10.1016/j.toxrep.2019.06.016):
  | PFAS | sex | liver:plasma | kidney:plasma | brain:plasma |
  |---|---|---|---|---|
  | PFBS (20 mg/kg) | M | >1, falling below 1.0 by 12 h | 0.29–0.38 | 0.01–0.02 |
  | PFBS | F | lower than male | higher than male | 0.02 (0.5 h) |
  | PFHxS (16 mg/kg) | M | 0.50–0.82, rising over time | 0.23–0.31 | 0.01–0.02 |
  | PFHxS | F | 0.29–0.55 | 0.26–0.44 | 0.01–0.02 |
  | PFOS (2 mg/kg) | M | >1 at all times, rising | ~1 | 0.06–0.12 (20 mg/kg) |
  | PFOS (2 mg/kg) | F | 3–4, steady | 1–2 | 0.04–0.10 (20 mg/kg) |
  Authors: "With the exception of PFOS in the liver, the tissue:plasma ratios of the PFAS were around one or less."
- **PFOS liver:plasma is itself dose-dependent** in the rat: in males the ratio "increased over time for all doses, most dramatically in the 2 mg/kg dose group"; in females the 20 mg/kg and repeat-dose groups started at 1–2.5 and converged on the 2 mg/kg group's 3–4 by the last time point — [Huang et al. 2019 Results §3.3](https://doi.org/10.1016/j.toxrep.2019.06.016). This is the partition-coefficient-level signature of the same hepatic saturation Kudo 2007 measured directly.
- **Rat vs human (Fàbrega et al. 2014, 2016, re-estimating Loccisano et al. 2011 from human cadaver data of Maestri et al. 2006):** for PFOA, liver 1.03 (human) vs 2.20 (rat); fat 0.47 (human) vs 0.04 (rat); plus new brain 0.17 and lung 1.27. For PFOS, liver 2.67 (human) vs 3.72 (rat); fat 0.33 (human) vs 0.14 (rat) — [ATSDR 2021 §3.1.5.8, p. 624](https://www.atsdr.cdc.gov/toxprofiles/tp200.pdf). Fàbrega found "Better agreement with observations was achieved with partition coefficients based on cadaver data."
- A third-party restatement of Loccisano et al. 2011's human PFOS baseline values: liver (PL) 2.03, kidney (PK) 1.26, rest of body (PRest) 0.2 — found via web search only; not verified against the primary paper.
- **PFHxS rat partition coefficients (Kim et al. 2018), measured from tissue:plasma ratios 14 days after 0.5–10 mg/kg IV:** "Values for each sex were significantly different for brain, lung, liver, spleen, gastrointestinal tract, adipose, and skeletal muscle; in each case, male > female. The highest partition coefficient was in male liver (approximately 0.13), with the value for female being approximately half of the male value" — [ATSDR 2021 §3.1.5.9, p. 627](https://www.atsdr.cdc.gov/toxprofiles/tp200.pdf). Free fraction in plasma, measured by ultrafiltration: 0.069% (female rat), 0.076% (male rat), 0.023% (human female), 0.025% (human male).
- Chain-length ordering of liver accumulation in rat: "Liver:plasma ratios of PFOS were the highest followed by PFHxS and PFBS, while brain:plasma ratios were low in all three sulfonates"; and across the carboxylates, "PFDA had the highest levels in the liver of the PFAS evaluated" — [Huang et al. 2019 abstract](https://doi.org/10.1016/j.toxrep.2019.06.016); [Dzierlenga et al. 2020 abstract, Xenobiotica 50:722](https://doi.org/10.1080/00498254.2019.1683776). (According to PubMed.)

### Inferences
- A set of partition coefficients all ≤ 4 with most ≤ 1, plus a plasma free fraction of 0.02–0.08%, is arithmetically compatible with Vd ≈ 0.1–0.7 L/kg and incompatible with Vd ≈ 4–7 L/kg. The partition-coefficient evidence therefore independently rejects the Andersen-derived total Vd values (Q1) and the steady-state monkey values (Q3).
- Kim 2018's PFHxS liver partition coefficient (~0.13) is an order of magnitude below the NTP's measured PFHxS liver:plasma ratio (0.50–0.82 in male rats). The likely reconciliation is that Kim's coefficients are defined against the *free* plasma pool while the NTP ratios are against *total* plasma — with a free fraction of 0.076%, those two conventions differ by >1,000×, so neither number can be used without checking the convention. Flagging this as a trap for anyone compiling partition coefficients across papers.
- Rat and human differ most in **fat** (human 3–12× higher for PFOA and 2.4× for PFOS) and least in liver. Because adipose is a large tissue fraction, the human-vs-rat fat difference is the single largest contributor to any species difference in Vd — and it still only moves Vd by tens of percent, consistent with the 2–4× species range in Q5.

### Partial rat-versus-mouse comparison (PFBS only)
- **Mouse, CD-1, single 30 or 300 mg/kg oral gavage:** "PFBS was detected in liver or kidney, although tissue levels of the chemical were only a fraction of those in serum" — liver:serum ~0.2–0.3, kidney:serum 0.1–0.2 at 24 h. Lau et al. compare this against two discordant literature values and offer the explanation: "this finding differs from those reported by Bogdanska et al. (2014) where the mouse hepatic levels of PFBS were described to be 1.4-fold higher than the level in blood, although this ratio is substantially lower than those reported by Olsen et al. (2009) with rats (9.6-fold)… The higher estimates of tissue:serum ratios from the Bogdanska 5-day dietary study compared to those from the current single gavage study may reflect a different manner of oral exposure" — `papers/Lau 2020 PFBS mouse PK.txt`.
- Against the NTP rat PFBS values (liver:plasma >1 falling below 1.0 by 12 h; kidney:plasma 0.29–0.38), the mouse single-gavage values are ~3–5× lower in liver and ~2–3× lower in kidney. But the three PFBS liver ratios in the literature — mouse 0.2–0.3 (single gavage), mouse 1.4 (5-day diet), rat 9.6 (Olsen) — span 30–50×, so **a rat-versus-mouse partition difference cannot be separated from a dosing-regimen difference** with the data found.

### Gaps
- **Side-by-side rat-vs-mouse partition coefficients for PFOA and PFOS were not found.** The NTP programme measured liver, kidney and brain in rats only; Fàbrega and Loccisano compare rat with human; the only mouse values recovered are for PFBS (above) and they are confounded with dosing regimen. Mouse tissue:plasma ratios for PFOA/PFOS exist in the primary literature (e.g. Lou et al. 2009, Fujii et al. 2015, Bogdanska et al.) but were not retrieved in this pass. `papers/Zhu 2023 route-specific PFAS mouse PK.txt` contains a mouse PBTK model with fitted liver and lung partition coefficients for PFOA/PFOS/PFHxS and would close this gap; it is in another researcher's scope and its numeric table was not extracted here.
- No adipose, lung or brain partition coefficient was found for PFHxA, PFBA, PFBS or PFNA in any species.

---

## Q7. Multi-dose studies: the cleanest test of saturable elimination

### Takeaway
Thirteen same-species, same-sex, multi-dose datasets were found. **Half-life is remarkably
dose-insensitive** — typically changing 12–20% over an 8–25× dose — while *apparent clearance*
changes 2–4× in **both directions** depending on the chemical. Where the data allow the check, the
apparent clearance change is matched almost exactly by a dose-dependent change in bioavailability,
not by a change in elimination.

### Cited Findings (full table in `../../db/dose_dependence.csv`)

**The NTP rat series (Huang et al. 2019) — same strain, sex, laboratory, analytical method:**

| PFAS | sex | dose range | k10 or β half-life, low → high | CL low → high (mL/h/kg) | F low → high |
|---|---|---|---|---|---|
| PFBS | M | 4 → 100 mg/kg (25×) | 4.37 → 2.86 h (k10); β 4.89 → 5.25 h | 26.0 → 75.5 (+2.9×) | 133% → 46% (−2.9×) |
| PFBS | F | 4 → 100 (25×) | 1.50 → 1.11 h | 152 → 259 (+1.7×) | 166% → 97% (−1.7×) |
| PFHxS | M | 4 → 32 (8×) | 17.6 → 14.8 d (−16%) | 0.201 → 0.376 (+1.87×) | 98% → 52% (−1.88×) |
| PFHxS | F | 4 → 32 (8×) | 2.33 → 1.98 d (−15%) | 1.92 → 3.84 (+2.0×) | 142% → 71% (−2.0×) |
| PFOS | M | 2 → 20 (10×) | 40.5 → 35.8 d (β, −12%) | 0.406 → 0.267 (**−1.5×**) | 135% → 205% (+1.5×) |
| PFOS | F | 2 → 20 (10×) | 40.7 → 36.0 d (β, −12%) | 0.226 → 0.186 (**−1.2×**) | 165% → 200% (+1.2×) |

Source: [Huang et al. 2019 Tables 2–4](https://doi.org/10.1016/j.toxrep.2019.06.016); extraction in `papers/Huang 2019 PFBS PFHxS PFOS rat multidose toxicokinetics.txt`.
The authors' own reading: "There was some evidence of saturation or induction of elimination… saturation of binding proteins/transporters may explain the changes in dose-adjusted AUC… High-affinity resorption processes in the kidney… are saturable such that at higher doses the dose-adjusted systemic exposure decreases. … The high bioavailability (>100%) observed at some doses may also be due to enterohepatic circulation."

**Other multi-dose datasets:**
- **PFOA, female rat, Kemper 2003 (4 doses, 250× range):** terminal half-life 3.2, 3.5, 4.6, 16.2 h at 0.1, 1, 5, 25 mg/kg — a 5× increase — and "plasma elimination kinetics in female rats converts from monophasic to biphasic" with increasing dose. **Male rats over the same range: "no apparent dose dependence"**, with clearances of 23.1, 20.9, 20.4 and 27.1 mL/d/kg (a 1.17× spread over 250× dose) — [ATSDR 2021 §3.1.4 p. 601 and Table 3-6](https://www.atsdr.cdc.gov/toxprofiles/tp200.pdf). Note the direction: in female rats the half-life gets *longer* at high dose, so if anything this is saturation of *secretion*, not of reabsorption.
- **PFOS, rat, Chang et al. 2012, 2 vs 15 mg/kg oral:** CL 11.3 → 4.9 mL/d/kg (M) and 22.2 → 5.4 (F) — clearance **falls** 2.3× and 4.1× as dose rises 7.5× — [ATSDR 2021 Table 3-6](https://www.atsdr.cdc.gov/toxprofiles/tp200.pdf).
- **PFOS, mouse, Chang et al. 2012, 1 vs 20 mg/kg oral:** CL 4.7 → 4.7 mL/d/kg (M) and 5.0 → 6.0 (F). **The cleanest null in the dataset: no change at all over a 20× dose** — same source.
- **PFHxS, mouse, Sundström et al. 2012, 1 vs 20 mg/kg oral:** CL 2.9 → 4.8 (M) and 2.7 → 3.8 (F), i.e. CL ∝ dose^0.17 and dose^0.11 — same source.
- **PFBA, mouse, Chang et al. 2008, 10/30/100 mg/kg:** "Systemic clearance following a single oral dose of 100 mg PFBA/kg was approximately 2 times higher than the systemic clearance following a dose of 10 or 30 mg PFBA/kg. Possible explanations… are dose-dependent bioavailability or that the one-compartment model used… did not adequately fit the serum kinetics observed at the higher dose. The latter could occur if renal tubular reabsorption of PFBA or plasma protein binding of PFBA is saturable in mice" — [ATSDR 2021 §3.1.4 p. 601](https://www.atsdr.cdc.gov/toxprofiles/tp200.pdf).
- **PFHxA, mouse, Daikin 2010, 35/175/350 mg/kg:** half-life 0.9–1.2 h with no dose-dependent pattern; AUC₀–∞/dose not dose-dependent (5.1–6.5 kg·h/L); but Cmax/dose fell 2.76 → 1.88 → 1.30 kg/L, "indicating saturation of absorption with higher doses… indicating that clearance was not dose-dependent" — [EPA 2023 PFHxA IRIS §3.1 p. 3-12](https://iris.epa.gov/).
- **PFOA, monkey, Butenhoff et al. 2004a, 3/10/20 mg/kg/d for 6 months:** steady-state serum 81 ± 40, 99 ± 50, 156 ± 103 µg/mL. A 6.7× dose produced only a 1.9× serum rise, implying apparent clearance rose ~3.5×. The authors attributed the shortfall to incomplete absorption and enterohepatic trapping, not to saturable elimination — [OEHHA 2024 PHG §4.8 p. 57](https://oehha.ca.gov/water/public-health-goal/final-public-health-goals-perfluorooctanoic-acid-and-perfluorooctane).
- **PFOS, rat, repeat vs single dosing at similar total dose (NTP):** apparent CL 0.068 (2 mg/kg/d × 5) vs 0.267 mL/h/kg (single 20 mg/kg) — a 4× difference — while β half-life was 33.4 vs 35.8 d, i.e. unchanged — [Huang et al. 2019 Table 4](https://doi.org/10.1016/j.toxrep.2019.06.016).
- **This repository's own Bayesian refit** of the EPA animal PK model gives, for male rats: PFOA CL ∝ dose^+0.110 (90% CI +0.007, +0.222) over 0.1–48 mg/kg; PFHxA CL ∝ dose^+0.039 (90% CI −0.041, +0.122), a null — `../../../pfas_dose/RESULTS.md`.

### Inferences
- **The half-life column is the signal; the clearance column is mostly an artefact.** Across six NTP dose series the half-life moved 12–20%, never more, over 8–25× dose. In four of those six the apparent clearance change (1.7–2.9×) is matched to within a few percent by the opposite change in bioavailability F — which is what you expect if the quantity being fitted from oral data is CL/F and F is dose-dependent. Non-compartmental clearance from oral dosing is not a measure of elimination capacity when absorption is dose-dependent.
- **The sign of the apparent dose effect is chemical-specific and inconsistent with a single saturable-reabsorption story.** PFBS/PFHxS/PFBA/PFOA-male-rat/this-repo's-PFOA → clearance rises with dose (consistent with saturating reabsorption). PFOS rat and PFOS monkey → clearance *falls* with dose. PFOA female rat → half-life *lengthens* 5× with dose. PFOS mouse and PFHxA → nothing. A mechanism that explains all of these at once has not been proposed in any source read here.
- The genuinely dose-dependent cases cluster where a *second* saturable process is present: absorption (PFBS, PFHxS, PFHxA Cmax/dose), enterohepatic recycling (PFOS F > 100% and rising with dose), or hepatic sequestration (PFOA, Kudo 2007). Elimination itself is the most dose-stable term.
- The practical consequence for the user's question: the cleanest same-species-same-sex tests say **half-life is close to dose-independent**, which argues *against* explaining the human/animal half-life gap by the dose difference. This agrees with, and strengthens, the conclusion already reached in `../../../species_dose/README.md` by a different route.

### Gaps
- Dzierlenga et al. 2020 (Xenobiotica, PFHxA/PFOA/PFDA rat, multi-dose) full tables were not obtained; only the Vd ranges via OEHHA and clearances "9–16 mL/kg/d, depending on the dose and route" via EPA. A per-dose half-life table for that study is missing.
- The Huang et al. 2021 corrigendum to the NTP paper was not retrievable (Europe PMC has the record but no body text). **Which numbers were corrected is unknown.** All NTP values here are from the 2019 tables and should be re-checked against the corrigendum.
- No multi-dose primate data exist: "every primate study is a single IV dose" (`../../../pfas_dose/README.md`), confirmed by ATSDR Table 3-6, where every non-human-primate row is a single 10 mg/kg or 2 mg/kg IV dose.
- No multi-dose human data of any kind exist, other than the Convertino 2018 oncology series (see Q8).

---

## Q8. Saturable renal reabsorption: implied Km, and the margin to human exposures

### Takeaway
Every saturable-reabsorption parameter in the literature is either a model-fitted quantity calibrated
to one unpublished rat study, or an in vitro transporter Km in the tens of micromolar. Human
environmental serum concentrations are 0.002–0.46 µM. **The margin is 50× at the very most extreme
comparison and 180–41,000× for every realistic one.** No transporter or binding protein is plausibly
saturated at human environmental exposures.

### Cited Findings — the parameters
- **The apical (reabsorptive) transporter Km, in units directly comparable to a human serum concentration.** Worley & Fisher's rat PFOA PBPK model takes its transporter affinities straight from in vitro studies without adjustment: **Km_apical (Oatp1a1) = 52.3 µg/mL** (from Weaver et al. 2010) and **Km_baso (mean of Oat1 and Oat3) = 27.20 µg/mL** (from Nakagawa et al. 2007), with Vmax_apicalC 0.947 and Vmax_basoC 0.04 mg/h/kg^0.75, free fraction in plasma 0.09 (fitted), and relative activity factors **RAFapi = 35.0 (male) versus 0.001356 (female)** and RAFbaso 4.07 (male) — Worley RR, Fisher J, *Toxicol Appl Pharmacol* 2015;289(3):428–441, PMID 26522833, [doi:10.1016/j.taap.2015.10.017](https://doi.org/10.1016/j.taap.2015.10.017), Table 3 (local: `papers/Worley 2015 PBPK kidney transporters PFOA rat.txt`). In ng/mL: **Km_apical = 52,300 ng/mL (126.3 µM)**, Km_baso = 27,200 ng/mL (65.7 µM).
- Worley & Fisher's model was evaluated against Kudo's two IV experiments at **0.041 and 16.56 mg/kg** (Table 1), i.e. the same 400× dose range as Kudo 2007 — so a model whose only saturable terms have Km ≈ 27–52 µg/mL was found adequate over that whole range.
- **In vitro transporter affinity, basolateral:** rat OAT1 Km for PFOA = **43.2 µM**; "No transport by rat OAT2, URAT1" — [OEHHA 2024 PHG, PFAS transporter table](https://oehha.ca.gov/water/public-health-goal/final-public-health-goals-perfluorooctanoic-acid-and-perfluorooctane) (citing Weaver et al. 2010). Consistent with Worley's 65.7 µM Oat1/Oat3 average.
- **A measured human net reabsorbed fraction, for the first time at environmental concentrations.** Abraham et al. 2024 report both total clearance and filtration clearance (CL_Filt = fup × GFR) for each compound. The implied net tubular reabsorption, 1 − CL_tot/CL_Filt (my calculation from their Table 4), is: **PFOA 97.8%, PFOS 99.0%, PFUdA 99.0%, PFNA 97.9%, PFDA 97.3%, PFHxS 97.0%, PFBA 88.3%, PFBS 79.4%, 6:2 FTS 30.7%, PFHpA 26.7%** — while **PFPeA and PFHxA show net *secretion*** (CL_tot exceeds CL_Filt by 1.7× and 4.2×) — [Abraham et al. 2024 Table 4](https://doi.org/10.1016/j.envint.2024.109047).
- **Albumin binding capacity:** Kd = 10⁻⁷ M (0.1 µM), Bmax = 4.1 × 10⁻⁴ M (**410 µM**) for PFOS — Harris & Barton 2008 via [ATSDR 2021 §3.1.5.5](https://www.atsdr.cdc.gov/toxprofiles/tp200.pdf).
- **Model-fitted reabsorption parameters, rat (Loccisano 2012a):** KT is "the concentration in the glomerular filtrate at which reabsorptive transport rate is half of maximum", in µg/L. ATSDR reports only the ratios: Tm/KT = 4.1 (male rat PFOA) vs 0.045 (female rat PFOA) — a 91× sex difference — and 7.2 for PFOS in both sexes — [ATSDR 2021 §3.1.5.1 p. 609](https://www.atsdr.cdc.gov/toxprofiles/tp200.pdf). For PFHxS (Kim et al. 2018): Tm/KT = 5.2 (male rat) vs 0.057 (female rat), again 91× — [ATSDR 2021 §3.1.5.9](https://www.atsdr.cdc.gov/toxprofiles/tp200.pdf).
- **Model-fitted reabsorption parameters, Wambaugh et al. 2013** (renal resorption affinity KT as a filtrate *amount*, µmol; maximum resorption rate Tmaxc, µmol/h): CD1 mouse F KT 0.037 (95% CrI 0.0057–0.17), Tmaxc 4.91; C57BL/6 mouse F KT 0.12, Tmaxc 2.7; rat F KT 1.1 (0.27–4.5), Tmaxc 1.1; rat M KT 0.092 (3.4e-4–1.6), Tmaxc 190 (5.5–50,000); monkey KT 0.043 (4.3e-5–0.29), Tmaxc 3.9 (0.65–9,700). Free fractions 0.011, 0.034, 0.086, 0.08, 0.01 — [EPA 2024 PFOA assessment Table 4-3](https://www.epa.gov/sdwa/). EPA's own caveat on the same table: "For some parameters, the distributions are quite wide, indicating uncertainty in that parameter (i.e., the predictions match the data equally well for a wide range of values)."
- **Human reabsorption parameters are not estimated at all** — Tm is set to reproduce an assumed half-life and KT is borrowed from monkey (Loccisano) or from rat (Kim 2018, who "assumed [Tm and Kt] to be the same in rats and humans") — [ATSDR 2021 §§3.1.5.2, 3.1.5.9](https://www.atsdr.cdc.gov/toxprofiles/tp200.pdf).
- **The concentrations at which saturation is actually observed in animals** (converted to ng/mL using MW 300.1 PFBS, 400.1 PFHxS, 500.1 PFOS, 414.1 PFOA):
  | observation | concentration |
  |---|---|
  | PFOS rat, lowest dose showing any CL change (2 mg/kg), Cmax 0.01 mM | 10 µM = **5,000 ng/mL** |
  | PFOS rat, high dose (20 mg/kg), Cmax 0.21 mM | 210 µM = **105,000 ng/mL** |
  | PFHxS rat, lowest dose (4 mg/kg), Cmax 0.08 mM | 80 µM = **32,000 ng/mL** |
  | PFBS rat, lowest dose (4 mg/kg), Cmax 0.053 mM | 53 µM = **15,900 ng/mL** |
  | PFOA monkey, lowest dose with a Css/dose shortfall (3 mg/kg/d), Css 81 µg/mL | 196 µM = **81,000 ng/mL** |
  | rat OAT1 Km for PFOA (Weaver 2010) | 43.2 µM = **17,900 ng/mL** |
  | albumin Bmax for PFOS (Harris & Barton 2008) | 410 µM = **205,000 ng/mL** |
  Cmax values from [Huang et al. 2019 Tables 2–4](https://doi.org/10.1016/j.toxrep.2019.06.016); monkey Css from [OEHHA 2024 PHG p. 57](https://oehha.ca.gov/water/public-health-goal/final-public-health-goals-perfluorooctanoic-acid-and-perfluorooctane).
- **Human serum concentrations, same units.** The Gasiorowski trial cohort — firefighters, i.e. a high-exposure group — had PFOS baseline mean 11.1 ng/mL (SD 12.9), range 2–190 ng/mL, and PFHxS 4.2 ng/mL (SD 9.7), range 0–140 ng/mL — [Gasiorowski et al. 2022, baseline table](https://doi.org/10.1001/jamanetworkopen.2022.6257). The NTP authors state for the general population: "Human plasma concentrations of PFHxS and PFOS have been found in the range of 0.1 to 70.7 ng/ml. PFBS in plasma was below detection limit in multiple studies; when detectable, concentrations of PFBS tend to be very low (e.g. 0.06 and 0.46 ng/ml)" — [Huang et al. 2019 Discussion](https://doi.org/10.1016/j.toxrep.2019.06.016). The highest community PFOA serum mean in the C8 region was 227.58 ng/mL (Little Hocking, Frisbee et al. 2009) — [OEHHA 2024 PHG p. 57](https://oehha.ca.gov/water/public-health-goal/final-public-health-goals-perfluorooctanoic-acid-and-perfluorooctane).

### The margin, stated explicitly in matched units

**The cleanest version, against the transporter Km that the saturable-reabsorption hypothesis is
actually about** (Km_apical = 52,300 ng/mL for rat Oatp1a1; Km_baso = 27,200 ng/mL for Oat1/Oat3,
both from Worley & Fisher 2015 Table 3):

| human PFOA serum | source of that number | margin to Km_apical (52,300 ng/mL) | margin to Km_baso (27,200 ng/mL) |
|---|---|---|---|
| 0.659 ng/mL | Cmax in the Abraham volunteer after a 4 µg tracer dose | **79,000×** | **41,000×** |
| 1.5 ng/mL | US general-population median, approx. | **35,000×** | **18,000×** |
| 100 ng/mL | high occupational | **523×** | **272×** |
| 227.6 ng/mL | C8 Little Hocking community mean (Frisbee 2009) | **230×** | **120×** |

At a serum concentration 230× below Km, the Michaelis–Menten term is 99.6% linear; at 35,000× below,
it is 99.997% linear. **For PFOA there is no realistic human exposure at which renal reabsorption is
measurably saturated.**

**The same margin against the *human* apical reabsorptive transporters** — which is the directly
relevant comparison and which I had flagged as a gap. Yang CH, Glover KP, Han X 2010, *Toxicol Sci*
117:294–302, PMID 20639259, [doi:10.1093/toxsci/kfq219](https://doi.org/10.1093/toxsci/kfq219),
report Km for human OAT4-mediated PFOA uptake of **172.3 ± 45.9 µM at pH 6.0** and
**310.3 ± 30.2 µM at pH 7.4**, and for human URAT1 **64.1 ± 30.5 µM**; human OATP1A2 showed no
saturable PFOA uptake above mock, so it is an inhibitor rather than a substrate (values as tabulated
in `../../db/transporter_kinetics.csv`, compiled by a parallel researcher from the primary paper):

| human PFOA serum | URAT1 (26,542 ng/mL) | OAT4 pH 6.0 (71,344 ng/mL) | OAT4 pH 7.4 (128,486 ng/mL) |
|---|---|---|---|
| 0.659 ng/mL (Abraham tracer Cmax) | 40,000× | 108,000× | 195,000× |
| 1.5 ng/mL (US median, approx.) | 17,700× | 47,600× | 85,700× |
| 100 ng/mL (high occupational) | 265× | 713× | 1,285× |
| 227.6 ng/mL (C8 Little Hocking mean) | **117×** | 313× | 565× |

The tightest margin anywhere in the human data is therefore **~117×**, against human URAT1 and using
the highest community serum mean on record. The human transporters are, if anything, lower-affinity
than the rat ones (64–310 µM versus 126 µM for rat Oatp1a1), so transferring rat Km values to humans
is conservative in the direction that matters.

**The same exercise against every other threshold found:**

| human concentration | animal/in vitro saturation threshold | margin |
|---|---|---|
| PFOS 5 ng/mL (0.0100 µM), US median-ish | rat Cmax at the lowest dose showing any CL change, 5,001 ng/mL | **1,000×** |
| PFOS 100 ng/mL (0.200 µM), high occupational | same, 5,001 ng/mL | **50×** |
| PFOS 190 ng/mL (0.380 µM), highest in the firefighter trial | rat Cmax at 20 mg/kg, 105,027 ng/mL | **553×** |
| PFOS 100 ng/mL (0.200 µM) | albumin Bmax, 205,053 ng/mL (410 µM) | **2,051×** |
| PFOS 5 ng/mL (0.0100 µM) | albumin Bmax, 205,053 ng/mL | **41,011×** |
| PFOA 1.5 ng/mL (0.0036 µM), US median-ish | rat OAT1 Km, 17,888 ng/mL (43.2 µM) | **11,925×** |
| PFOA 100 ng/mL (0.242 µM) | rat OAT1 Km, 17,888 ng/mL | **179×** |
| PFOA 227.6 ng/mL (0.550 µM), C8 Little Hocking mean | monkey Css at 3 mg/kg/d, 81,000 ng/mL | **356×** |
| PFHxS 120 ng/mL (0.300 µM), near trial max | rat Cmax at 4 mg/kg, 32,009 ng/mL | **267×** |

### Cited Findings — the one human observation of saturation
- "saturation of this transporter could result in an increase in urinary elimination of perfluoroalkyls due to decreased tubular reabsorption. This is consistent with the apparent plateau in plasma concentration with increasing dose observed in cancer patients treated with PFOA (Convertino et al. 2018)" — [ATSDR 2021 §3.1.4 p. 602](https://www.atsdr.cdc.gov/toxprofiles/tp200.pdf). Those were pharmacologic infusion doses, orders of magnitude above environmental exposure.
- EPA's own statement of the open question: PBPK refinement is needed "to address non-linearities in PK that may occur due to the saturation of PFAS-protein interactions… [and] are more representative of the general population due to saturation of renal resorption and…" — [EPA 2024 PFOA assessment, research-needs section](https://www.epa.gov/sdwa/) (`papers/EPA 2024 PFOA human health toxicity assessment.txt` lines 21219–21221). EPA treats this as an acknowledged uncertainty rather than a demonstrated effect at environmental levels.

### Inferences
- The *smallest* defensible margin is ~50×, and it requires pairing the top of the human occupational range (100 ng/mL PFOS) against the rat Cmax at the lowest dose in a study where the half-life changed by only 12%. For the general population the margin is 10³–10⁴×. At those margins a Michaelis–Menten reabsorption term is operating in its linear regime, where clearance is constant and independent of concentration.
- This also kills the mechanism as an explanation of the species gap *from the correct direction*: saturation makes clearance *faster* at high concentration, so de-saturating by lowering the dose makes clearance *slower* — but only up to the linear asymptote, which humans are already far inside. There is no further slowing available. (`../../../species_dose/README.md` makes the same argument from the dose-slope magnitude; the margin calculation here is the independent mechanistic version of it.)
- Albumin is the strongest case of all: with Bmax at 410 µM and typical human PFOS at 0.01 µM, **0.0024% of binding sites are occupied**. Protein-binding saturation cannot be happening at human exposures, and so cannot be raising the human free fraction or human apparent Vd.
- The 91× Tm/KT sex ratios in both the Loccisano PFOA rat model and the Kim PFHxS rat model are suspiciously identical. Since both are fitted to reproduce an observed sex difference in clearance, the ratio is probably a restatement of the observation rather than an independent finding about transport.

- The RAFapi male:female ratio of 35.0 : 0.001356 — **25,800×** — is a fitted scalar, not a measurement; Worley & Fisher state plainly that "Relative activity factor information for the basolateral membrane transporters was not available in the literature, so this parameter (RAFbaso) was fit to experimental data" and likewise for RAFapi. A 25,800-fold difference in transporter activity between male and female rats is not biologically credible as stated; it is the model's way of absorbing a 44× clearance difference through a parameter that enters nonlinearly. Anyone citing RAFapi as evidence about transporter expression is citing a curve-fitting artefact. (The same caution applies to the suspiciously identical 91× Tm/KT sex ratios noted below.)
- Abraham's measured 97–99% net reabsorption for the long-chain PFAS, at human environmental concentrations, is exactly what an *unsaturated* high-affinity reabsorption system should do. The point is often stated the other way round — that high reabsorption implies saturability matters — but a near-complete reabsorption measured at 0.5 ng/mL, against a Km of 52,000 ng/mL, is the signature of a transporter operating in its linear regime at maximal fractional efficiency. Saturation would *reduce* the reabsorbed fraction, and that is only visible in the animal studies.
- The chain-length switch from net reabsorption (C7 and longer) to net secretion (PFPeA C5, PFHxA C6) in Abraham's human data matches the rat transporter-affinity ordering reported by ATSDR (apical reabsorptive transporters have "highest [affinity] for C7–C10 perfluoroalkyl carboxylates"), so the human and rat mechanisms appear qualitatively the same — which strengthens the read-across EPA relies on while leaving the quantitative clearance gap unexplained.

### Gaps
- Numeric KT values in µg/L for the *Loccisano and Andersen* models were not obtained. ATSDR prints only Tm/KT ratios; Wambaugh's KT is an amount in µmol, not a concentration, and converting it requires the filtrate volume, whose 95% credible interval spans 8 orders of magnitude (EPA Table 4-3). **I did not attempt that conversion** because the uncertainty makes it meaningless. Worley & Fisher's Km values (above) serve the purpose better and are measured rather than fitted.
- Human apical transporter Km values are now in hand (above) but were taken from `../../db/transporter_kinetics.csv`, a parallel researcher's compilation of the Yang et al. 2010 abstract, **not** from the primary tables. Both the OAT4 and URAT1 Km values carry large standard deviations (±45.9 on 172.3; ±30.5 on 64.1), so the ~117× tightest margin is uncertain by roughly a factor of 2 — which does not change the conclusion. Further human and rat transporter kinetics are in `../../db/transporter_kinetics.csv` and in `papers/Louisse 2023 OAT4 PFAS substrates.txt`, `papers/Niu 2026 three renal transporters PFAS.txt`, `papers/Ryu 2024 14 PFAS OAT interactions.txt`; those belong to another researcher's scope and were not independently mined here.
- No Km at all was found for the human *basolateral* secretory transporters (OAT1, OAT3) for PFOA, so the secretion side of the human balance is unquantified. Abraham's finding that long-chain PFAS show 97–99% net reabsorption while PFPeA and PFHxA show net secretion implies the secretory arm is substantial for short chains and would be worth a Km.

---

## Q9. Is there an exposure-level dependence of human half-life, and is it confounded?

### Takeaway
No multi-dose human study exists, but there is now a *low-dose anchor*: a controlled tracer dose
~10⁴–10⁵× below any animal study gave a PFOA half-life of **5.5 years — longer than the 2.3–3.8 years
estimated from high-exposure cohorts**. If exposure level mattered through de-saturation, the
low-dose half-life should have been shorter. It is longer, and the most likely reason is that it is
the only human estimate free of background-exposure confounding, not that dose matters.

### Cited Findings
- **The low-dose anchor.** A ¹³C-labelled tracer dose (3.96 µg PFOA in an ~82 kg man, plasma Cmax 0.659 ng/mL) followed for 450 days gave a terminal half-life of **2011 days = 5.5 y (95% CI 1466–3206 d)**; PFHxS 1634 d = 4.5 y (1166–2733); PFOS 1211 d = 3.3 y (927–NA); PFNA 1305 d = 3.6 y (1054–1716) — [Abraham et al. 2024 Table 3](https://doi.org/10.1016/j.envint.2024.109047), PMID 39476597. Compare the cohort-based values EPA and ATSDR use: PFOA 2.3 y (Bartell 2010, drinking water), 2.7 y (Li 2017), 3.8 y (Olsen 2007a, retired workers); PFOS 5.4 y (Olsen 2007a).
- Abraham also found PFBS human half-life of **50.6 days (95% CI 47.7–53.8)**, roughly double the ~26 days usually quoted, and half-lives of 152 d for PFHpA, 295 d for PFDoA, 584 d for PFUdA and 862 d for PFDA — the first human half-lives for several of these.
- The same study found half-life *decreasing* with chain length beyond C9: PFOA 2011 > PFNA 1305 > PFDA 862 > PFUdA 584 > PFDoA 295 d — [Abraham et al. 2024 Table 3](https://doi.org/10.1016/j.envint.2024.109047).
- "The mean level of PFOS at 12 months was significantly reduced by plasma donation (−2.9 ng/mL; 95% CI, −3.6 to −2.3) and blood donation (−1.1 ng/mL; −1.5 to −0.7) **but was unchanged in the observation group**" (n = 95, baseline mean 10.7 ng/mL) — [Gasiorowski et al. 2022](https://doi.org/10.1001/jamanetworkopen.2022.6257). The paper quotes a PFOS half-life of 4.8 years in its introduction.
- Age and sex are established modifiers that confound any such comparison. "human monitoring studies have not consistently detected sex differences in elimination t½ of perfluoroalkyls; this may reflect limitations in the studies, including numbers and age of subjects (Bartell et al. 2010; Seals et al. 2011; Wong et al. 2014, 2015; Zhang et al. 2013)"; and "The effect of menstruation or other variables related to menstruation appear to contribute to faster elimination in younger (≤50 years) women compared to men and older women (Zhang et al. 2013)" — [ATSDR 2021 §3.1.4 p. 603](https://www.atsdr.cdc.gov/toxprofiles/tp200.pdf).
- ATSDR explicitly bounds the applicability of every human half-life to the serum range in which it was measured: for PFHxS, "The range of initial serum concentrations was 16–1,295 ng/mL (mean of 290 ng/mL), and the final concentrations ranged from 10 to 791 ng/mL (mean of 182 ng/mL). Estimates of the t½ for PFHxS are most applicable to serum concentrations within the above ranges and **would be less certain if applied to serum concentrations substantially below or above these ranges**" — [ATSDR 2021 p. A-12](https://www.atsdr.cdc.gov/toxprofiles/tp200.pdf).
- Isomer composition is a further confounder that mimics a dose effect: "The half-lives of the branched-chain PFOA isomers are shorter than those for the linear molecule, indicating that renal resorption is less prevalent for the branched-chain isomers (Fu et al., 2016; Zhang et al., 2015)" — [EPA 2024 PFOA assessment §3.3.1.4.1](https://www.epa.gov/sdwa/). High-exposure cohorts (occupational, C8) differ in isomer profile from the general population.

### Inferences
- A 52-week observation with a 4.8-year half-life predicts a 13% fall (10.7 → 9.3 ng/mL, i.e. −1.4 ng/mL); with the ATSDR 2,000-day half-life, −1.3 ng/mL. The observed "unchanged" is consistent only with ongoing intake replacing losses at essentially 100%, or with an effective half-life much longer than 4.8 years at ~10 ng/mL. Both readings cut against the dose hypothesis: the first says human serum is at steady state with ongoing intake (so "half-life" estimates from such cohorts are confounded exactly as `../../../literature/APPRAISAL.md` §1 says), and the second says the half-life is *longer*, not shorter, at low concentration — the opposite of what de-saturation predicts.
- Because every *cohort* half-life estimate comes from a different concentration *and* a different age/sex mix *and* a different isomer profile, an apparent concentration–half-life relationship across cohorts is not identifiable. The cross-cohort test already run in `../../../literature/APPRAISAL.md` is the right framing.
- **Abraham 2024 is the one unconfounded human data point, and it points the wrong way for the dose hypothesis.** Its internal dose is ~350× below the Little Hocking community mean and ~10⁵× below any animal study, yet PFOA's half-life came out 1.4–2.4× *longer* than the cohort estimates, not shorter. Two readings, and both hurt the dose hypothesis: (a) the difference is a de-confounding effect — the labelled tracer cannot be topped up by background intake, so the cohort estimates were biased short by ongoing exposure and the true half-life is ~5.5 y at all human exposures; or (b) the difference is real and half-life genuinely *lengthens* as concentration falls, which is the opposite of what relieving saturation predicts. Reading (a) is far more likely given `../../../literature/APPRAISAL.md` §1, and it implies no exposure-level dependence at all.
- One important caveat in the other direction: Abraham's design confounds dose with *isomer purity and labelling*. The tracer was linear ¹³C-PFOA, while cohort serum contains a branched/linear mixture whose branched component has a shorter half-life ([EPA 2024 §3.3.1.4.1](https://www.epa.gov/sdwa/)). Some of the 1.4–2.4× difference is therefore an isomer effect, not a dose or confounding effect, and the three explanations cannot be separated with n = 1.

### Gaps
- Olsen et al. 2009's human PFBS half-life (reportedly ~26 days, the shortest human PFAS half-life) was not retrieved, so the chemical with the most extreme human/animal clearance contrast is missing from this pass.
- Seals et al. 2011 was not re-examined (covered in `../../../literature/APPRAISAL.md` §"Seals 2011 read properly").

---

## Q10. Conversely: evidence that half-life is INDEPENDENT of dose over wide ranges

### Takeaway
This is the better-supported side of the question, and it comes from the regulators' own analyses as
well as from the primary data.

### Cited Findings
- **EPA tested dose-dependence formally for PFHxA and rejected it.** "Parameter estimation… was performed both including and excluding the highest dose data. Had the resulting estimate of β been significantly different when the high-dose data were included, this would have indicated a dose dependence. The results of the alternative analyses did not indicate such a difference, however, **leading to the conclusion that PFHxA PK is not dose dependent** and that the assumption of nonvarying parameters in the PK model equation is appropriate." Further: "A systematic deviation from the assumption of equal or more rapid clearance at higher doses has not been observed in the other relevant data (Iwabuchi et al., 2017; Gannon et al., 2011; Chengelis et al., 2009a). Further, because PFHxA is not metabolized, nonlinearity in its internal dose is not expected due to that mechanism." — [EPA 2023 IRIS PFHxA Toxicological Review §5.2.1, pp. 5-10 to 5-11](https://iris.epa.gov/).
- **The one PFHxA deviation runs the wrong way for the saturation story.** "Although PK data at lower doses do not show any trend consistent with dose-dependence, data for the highest dose indicate that elimination can be **reduced** (Dzierlenga et al., 2019); **the opposite of what is predicted based on the hypothesis of saturable resorption**. While saturation of reabsorption transporters would lead to a decreased half-life at higher doses, there are also transporters responsible for elimination of PFAS to urine, such as Oat1 and Oat3, and saturation of these transporters could lead to an increase in observed half-life." — same source.
- **PFOS in mice: a true null over 20× dose.** CL 4.7 vs 4.7 mL/d/kg (males) and 5.0 vs 6.0 (females) at 1 and 20 mg/kg — [ATSDR 2021 Table 3-6](https://www.atsdr.cdc.gov/toxprofiles/tp200.pdf) (Chang et al. 2012).
- **PFOA in male rats: a null over 250× dose.** Clearances 23.1, 20.9, 20.4, 27.1 mL/d/kg at 0.1, 1, 5, 25 mg/kg; ATSDR: "no apparent dose dependence was observed in male rats over the same dose range (Kemper 2003)" — [ATSDR 2021 §3.1.4 p. 601 and Table 3-6](https://www.atsdr.cdc.gov/toxprofiles/tp200.pdf).
- **PFHxA in mice: half-life flat over 10× dose** (0.9–1.2 h at 35, 175, 350 mg/kg, "lacked a dose-dependent pattern"), with AUC/dose also flat — [EPA 2023 PFHxA IRIS §3.1 p. 3-12](https://iris.epa.gov/) (Daikin 2010).
- **The NTP half-life columns are the strongest single body of evidence**: over 8–25× dose, β or k10 half-life changed by 12–20% at most for PFBS, PFHxS and PFOS in both sexes of the same rat strain ([Huang et al. 2019 Tables 2–4](https://doi.org/10.1016/j.toxrep.2019.06.016)) — while apparent clearance in the same tables changed 1.5–2.9×. When half-life and clearance disagree, half-life is the better-identified quantity because it does not depend on bioavailability.
- **PFBS in mice: an explicit author statement of linearity over 10× dose.** "The half-life of PFBS was estimated as 5.8 h in the males and 4.5 h in the females… Volume of distribution was similar between the two sexes (0.32–0.40 L/kg). **The rate of PFBS clearance was linear with exposure doses**" (30 and 300 mg/kg oral gavage, CD-1 mice) — `papers/Lau 2020 PFBS mouse PK.txt`. This is the same chemical in which the NTP rat study showed an apparent 2.9× clearance rise over 25× dose — reinforcing that the rat signal is a bioavailability artefact rather than saturable elimination.
- **This repository's own PFHxA result agrees:** dose slope +0.039 (90% CI −0.041, +0.122), 0 of 5 within-study clearance ratios outside 0.8–1.2 — `../../../pfas_dose/RESULTS.md`.
- **Worley & Fisher's rat PFOA model, whose only saturable terms have Km of 27–52 µg/mL, adequately described data spanning a 400× dose range** (Kudo's 0.041 and 16.56 mg/kg IV experiments, plus Kemper's 1–25 mg/kg oral) — [Worley & Fisher 2015, Table 1](https://doi.org/10.1016/j.taap.2015.10.017). A saturable model that fits across 400× dose without needing to be in its saturated regime is itself evidence that the nonlinearity is mild at those doses, let alone at human ones.

### Inferences
- The honest summary is that PFAS elimination is **weakly** dose-dependent, with a chemical- and sex-specific sign, over dose ranges of 8–250× at concentrations 50–40,000× above human exposure; and **essentially dose-independent** in half-life terms. The strongest nulls (PFOS mouse, PFOA male rat, PFHxA) and the strongest positives (PFOA male rat per this repo's refit, PFBS, PFBA) cannot both be right about the same mechanism, and the reconciliation is that most of the apparent positives are absorption or enterohepatic-recycling effects, not elimination effects.
- Combined with the margins in Q8, the dose hypothesis for the human/animal half-life gap fails on **five** independent grounds: (i) the measured dose slope is ~dose^0.1, an order of magnitude too small (`../../../species_dose/README.md`); (ii) half-life itself barely moves with dose (12–20% over 8–25×) even where apparent clearance moves 2–3×; (iii) human serum sits 230–79,000× below the measured Km of the reabsorptive transporter, deep in the linear regime, so there is no saturation left to relieve; (iv) the one controlled human low-dose measurement gives a *longer*, not shorter, half-life than the high-exposure cohorts (Q9); (v) the measured human free fraction at trace concentration is no higher than the free fractions fitted at animal doses (Q4).
- And the Vd route is closed too — more firmly now that a measured human Vd exists. Vd varies only 2–4× across species, and with Abraham's measured human values the Vd term points *against* the long human half-life (human Vd 0.34–0.62× the male rat's, Q5); Vd does not rise with dose in the way protein saturation would require, and in the one direct tissue measurement it falls (Q4). **Neither term of t½ = ln2·Vd/CL supports a dose explanation: the entire 20–360× human/rat half-life gap, and then some, has to be carried by clearance.**
- The remaining honest uncertainty is not about dose but about *why* human clearance is 50–360× below the rat's at concentrations where no transporter is saturated. Nothing read in this pass answers that. The candidates on offer — differing transporter abundance and differing apical/basolateral affinity, neither scaling with body size ([ATSDR 2021 §3.1.4](https://www.atsdr.cdc.gov/toxprofiles/tp200.pdf)) — are plausible but are supported in the models only by fitted relative activity factors, which is a restatement of the observation rather than an explanation of it.

### Gaps
- No study was found that dosed the **same species, same sex, same laboratory** at multiple levels and reported **half-life** (rather than non-compartmental clearance) with its confidence interval at each dose. The NTP tables report half-life point estimates with SEMs, which is the closest available, but no formal test of a dose trend in half-life has been published for any PFAS in any species. This is the single most useful missing experiment for the question, and it is cheap: the NTP already has the plasma curves.
- Butenhoff et al. 2012 (rat PFOS/PFOA chronic study), Pizzurro et al. 2019 (cross-species half-life review), Fenton et al. 2021 (ETC review), Numata et al. 2014 (pig), Chou & Lin 2019/2021 and Lin et al. 2023 (cross-species PBPK) were not retrieved in this pass (see `../../papers/SOURCES_vd_dose.md`). The three reviews would likely only re-tabulate values already captured from ATSDR/EPA/OEHHA, but the Chou & Lin Bayesian cross-species PBPK work is the one source that might report a *posterior* on a dose-dependence parameter, and it was not checked.
- Olsen et al. 2009's human PFBS half-life was not retrieved, so the discrepancy between the ~26 days usually quoted and Abraham's measured 50.6 days is unresolved.
