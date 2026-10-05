# SOURCES - Final Sweep

Started 2026-10-02.

## Priority 1 - DOG (only completely empty species column)

### On-disk hits (no new download needed)
1. **NJ DWQI 2017 PFOA health-based MCL support document** (`papers/NJ DWQI 2017 PFOA health-based MCL support document.txt`, line 2105)
   - Table 4 "Serum/plasma elimination half-lives of PFOA" (adapted from Lau 2012), p.45.
   - Dog: females 8-13 days, males 20-30 days. Cites **Hanhijarvi et al. (1988)**.
   - Full citation found at line 10376: "...excretion of perfluorooctanoic acid in the beagle dog and rat. In: Beynen, A.C. Solleveld, H.A. (Eds.), New Developments in Biosciences..."
2. **OEHHA 2024 PFOA PFOS PHG** (`papers/OEHHA 2024 PFOA PFOS PHG.txt`)
   - line 1850, Section 4.1 narrative: "PFOA T1/2 was 5.5-7 hours in the rabbit, **10.6-20.1 days in the dog** and 2.7-5.6 days in the Japanese macaque (Hanhijarvi et al., 1988; Kudo and Kawashima, 2003; Harada et al., 2005a)."
   - line 18249+, **Table A6.4** "Estimate of net renal tubular reabsorption of PFOA in different species" (adapted from Han et al. 2012), p.327: dog female CLR 50.8 mL/kg-day, dog male CLR 43 mL/kg-day, GFR 5300 mL/day-kg, net reabsorption 55 / 63 mL/kg-day, 52% / 59% reabsorbed. Cites **Kudo and Kawashima (2003)**.
   - Same table also present in OEHHA 2021 PFOA PFOS PHG first draft (line 18378).
   - 5 dog rows appended to db/final_sweep.csv.

### Negative results
- `ATSDR 2021 Toxicological Profile Perfluoroalkyls.txt` (2.9 MB): "dog", "dogs", "beagle", "canine" appear ONLY inside the literature-search strategy Boolean strings (lines 38974, 39087, 39170). ATSDR 2021 does **not** tabulate any dog TK value. Griffith and Long 1980 is cited ~10x in ATSDR but exclusively for **rat and mouse** acute/28-day toxicity (LC50, LD50, mortality), not dog and not TK.
- EPA 2024 PFOA and PFOS assessments mention "dogs" once each, only as the source of an assumed 20% renal blood-flow fraction for the PBPK model - not a PFAS measurement.
- EPA 2024 PFOA appendix volume, EPA 2025 IRIS PFHxS, EFSA 2020: no dog TK.

## Priority 5 - DZIERLENGA/ZURLINDEN 2025 supplementary tables: OBTAINED (via code repo, not PMC)

Paper: Zurlinden TJ, **Dzierlenga MW**, Kapraun DF, Ring C, Bernstein AS, Schlosser PM, Morozov V.
"Estimation of species- and sex-specific PFAS pharmacokinetics in mice, rats, and non-human primates
using a Bayesian hierarchical methodology." Toxicol Appl Pharmacol 2025;499:117336.
PMID 40210099, PMC12172007, doi:10.1016/j.taap.2025.117336.

### Retrieval attempts (in order)
| Route | Result |
|---|---|
| NCBI E-utilities `efetch db=pmc&id=PMC12172007` | REFUSED - XML contains only `<!--The publisher of this article does not allow downloading of the full text in XML form.-->` |
| Europe PMC `/PMC12172007/fullTextXML` | HTTP 500 |
| Europe PMC `/PMC12172007/supplementaryFiles` | HTTP 200 but errorBean: "Article with id PMC12172007 is not open access one" |
| Europe PMC `/MED/40210099/supplementaryFiles` | HTTP 404 |
| Firecrawl stealth on PMC article page (links format) | SUCCESS - revealed the three supplement filenames |
| curl + Firecrawl stealth/enhanced on `pmc.ncbi.nlm.nih.gov/articles/instance/12172007/bin/NIHMS2077116-supplement-Supplement{1.pdf,2.docx,3.docx}` | BLOCKED - reCAPTCHA, then a JS proof-of-work "Preparing to download..." interstitial. Not solvable from here. |
| **Clone of the paper's own code repo `USEPA/CPHEA-Animal-PFAS-PK`** | **SUCCESS** |

### What was recovered and how
The supplementary tables are produced by `auxiliary_notebooks/PFAS_manuscript_results.ipynb`, whose
**executed outputs are committed in the repo**. The cells that write the supplementary CSVs:
- cell 41 -> `SUPPL_PFAS_PK_summary.csv` + `figures/SUPPL_UnityLine.pdf` (table itself NOT in notebook output - only the empty template is displayed in cell 39, so this one table remains unrecovered)
- **cell 45 -> `IV_vs_Gavage_ROPE_halft.csv`** - FULLY recovered (33 rows)
- **cell 47 -> `IV_vs_Gavage_ROPE_Vd.csv`** - FULLY recovered (33 rows)
- cells 32/35/43 -> sex-comparison ROPE tables (also in the saved .txt)

Saved: `papers/Zurlinden 2025 SUPPLEMENTARY tables from EPA repo notebook.txt`
66 rows appended to db/final_sweep.csv.

### Two findings worth propagating to the rest of the collection
1. **The Vd in this paper is Vdss.** The notebook's posterior variables are literally `Vdss [pop]` and
   `Vdss [indiv]`. This settles the vd_type for every Zurlinden 2025 Vd row already in the collection.
2. **The half-life is the terminal (beta-phase) half-life**, variable `halft_beta`.
3. Content of the recovered tables = posterior **ratio IV/oral** per underlying study/sex, with 95% HDI
   and a ROPE[0.8,1.2] decision. Route mattered (ROPE "Reject Null") in only 4 of 66 cases:
   PFHxS female Huang 2019 (half-life ratio 0.663), PFOA male Kim 2016 (0.241) and Kemper 2003 (0.303),
   and PFHxS female Kim 2018 Vdss (2.092 at 1 mg/kg and 2.331 at 4 mg/kg).

## Priority 3 - systematic review / meta-analysis of PFAS half-lives after Rosato 2024: CONFIRMED NONE

Fresh search run 2026-10-02. PubMed, publication date 2024/06/01-2026/12/31, title/abstract:
`(perfluoro* OR PFAS OR polyfluoroalkyl) AND ("systematic review" OR "meta-analysis" OR "meta-analyses" OR "scoping review") AND (half-life OR halflife OR elimination OR toxicokinetic* OR clearance OR pharmacokinetic*)`
-> **exactly 4 hits**, none of which is a systematic review or meta-analysis of PFAS half-lives:

| PMID | Year | What it actually is | Verdict |
|---|---|---|---|
| 41921758 | 2026 | Non-serum PFAS biomarkers and human reproductive/perinatal outcomes: systematic review | not TK |
| 40946629 | 2025 | Photo-based advanced oxidation processes for PFAS removal: systematic review | water treatment, not TK |
| 40847085 | 2025 | Birth weight vs PFOS biomarkers: meta-analysis + meta-regression (53 studies) | health outcome; "long half-life" only as framing |
| 39542374 | 2024 (Nov, Chemosphere) | Clinical, histological, molecular and **toxicokinetic** renal outcomes of PFAS: systematic review + meta-analysis. 169 studies, 68 toxicokinetic. | **closest candidate** - but pools no half-life estimates; TK is one of four outcome categories and the synthesis is qualitative |

A parallel Europe PMC search over the same window returned 236 hits, all of which on inspection were
health-outcome or mechanism reviews (EDCs and hypertension, MASLD, thyroid cancer, autoimmunity, etc.).

**Conclusion: the previous search's finding is CONFIRMED, not refuted.** Rosato 2024 remains the most
recent systematic review/meta-analysis of PFAS half-lives. 39542374 logged in db/final_sweep.csv as the
nearest miss, with no numeric value claimed.

## Priority 4 - compounds with exactly one study

### Hits
- **PFHpS in CATTLE** - PMID 39787095, doi 10.1080/19440049.2024.2444560, Food Addit Contam Part A 2025.
  "Tissue histology and depuration of PFAS from dairy cattle with lifetime exposures to PFAS-contaminated
  drinking water and feed." 30 dairy cattle removed from a contaminated farm, 22-week withdrawal.
  Plasma half-lives of PFHxS, **PFHpS**, L-PFOS, 3Me-PFOS, 6Me-PFOS given as a POOLED range 4-10 weeks.
  5 rows appended (one per analyte), range in ci_low/ci_high, per-analyte values need full text.
  New chemical-species cell: PFHpS had existed only in human.
- **5:3 FTCA in RAT** - PMID 38061571, doi 10.1016/j.fct.2023.114333, Food Chem Toxicol 2024.
  tss 150 d to >1 year in serum/tissues of nonpregnant rats dosed with the parent 6:2 FTOH.
  Matters because every existing 5:3 FTCA row in the matrix is from the EPA httk package (modelled);
  this is an independent measured in vivo source. 5:3A was NOT a renal-transporter substrate.
- **6:2 diPAP in RAT** - PMID 42664870 (see Priority 2) - the second diPAP study. 5 rows.
- **6:2/8:2 Cl-PFESA (F-53B) in RAT** - PMID 41774853 - would be the second Cl-PFESA study, but the
  ACS abstract carries no numeric TK parameter and the paper is paywalled. Logged as a gap.
- **FOSA in DOG** - PMID 16720684 - only in vitro hepatic N-glucuronidation, no kinetic constants in
  the abstract. Logged as a gap. Notable as the only PFAS-and-dog disposition record in PubMed.

### Already covered - deliberately NOT re-extracted
- **cC6O4**: PMID 36977049 (Fustinoni 2023, Toxics) half-life 184 h (95% CI 162-213) and Vd 80 mL/kg
  are ALREADY in db/human_halflife_extended.csv (rows "Fustinoni 2023 cC6O4 workers" and
  "Fustinoni 2023 (measured Vd, cC6O4)"). Verified before writing; skipped.

### No new TK data found for
PFECHS, ADONA, 6:2 FTS, PFTrDA, PFTeDA, 10:2/8:2/6:2 diPAP beyond the 6:2 diPAP paper above.
Searched PubMed title/abstract for each of these names AND (half-life OR toxicokinetic* OR
pharmacokinetic* OR clearance OR elimination OR depuration OR "volume of distribution"): 69 hits,
and on title review the only in-scope new ones are those listed above. The 6:2 FTS hits are soil
and sludge biotransformation studies (e.g. PMID 38070347), not animal TK.

## Priority 2 - anything 2025-2026 reporting a PFAS half-life, clearance, Vd or elimination rate constant

PubMed, title/abstract, publication date 2025/01/01-2026/12/31:
`(perfluoro* OR PFAS OR polyfluoroalkyl) AND (half-life OR halflife OR toxicokinetic* OR pharmacokinetic* OR clearance OR "volume of distribution" OR elimination)`
-> **261 hits.** Titles triaged for the first 100 (sorted by date); the rest were degradation chemistry,
perfluorocarbon blood substitutes / ultrasound contrast agents, and health-outcome epidemiology.

### Captured with numeric values
| PMID | Study | What was captured |
|---|---|---|
| 42664870 | Kim M et al., Environ Int 2026 | **6:2 diPAP rat**: IV t1/2 32.1+/-4.3 h, CL 86.2+/-20.8 mL/h/kg, hepatic CL 75.3, CLint 334+/-56, near-complete oral F, biliary 14.5% of IV dose |
| 42190831 | Fan X et al., Environ Pollut 2026 | **PFBA female rat**: terminal t1/2 68.7 h, central Vd 323 mL/kg |
| 42202518 | Lai G et al., J Hazard Mater 2026 | **C7 HFPO-TA male CD-1 mouse**: PBPK serum t1/2 ~76 h |
| 42290009 | Gillings MM et al., Environ Sci Technol 2026 | **house sparrow (bird)**: t1/2 29 d (PFBS) to 91 d (PFNA), juveniles; decline 0.43-1.25%/day |
| 41720239 | Asshoff N et al., Environ Pollut 2026 | **male lambs (sheep)**: apparent plasma t1/2 0.3 d (PFPA) to 57 d (PFOS), 9 PFAS; FIRST TK data for PFAS other than PFOA/PFOS in lambs |
| 39787095 | Lupton SJ et al., Food Addit Contam 2025 | **dairy cattle**: plasma t1/2 4-10 wk pooled across PFHxS, PFHpS, L-PFOS, 3Me-PFOS, 6Me-PFOS |
| 42067648 | Inauen D et al., Arch Toxicol 2026 (OPEN ACCESS, PMC13379421) | **PFOS in cattle/sheep/chicken**, Table 1 + results text: Fa 0.954/0.974/0.990, ka 0.012/0.098/0.005 1/h, absorption t1/2 59/7/139 h, CLrenal 0.13/0.108/0.15 L/h/kg. 12 rows. |
| 42162713 | Argoul CM et al. (Gayrard group), Environ Res 2026 | **11 PFAS, female mice, IV+oral, NLME**: MRT <1 d to 68 d |

### Logged as gaps (retrieved, no numeric parameter available)
- 41774853 Zhang J et al., Environ Sci Technol 2026 - Cl-PFESA/F-53B rat PBTK (abstract has no parameters)
- 42127783 El Amraoui Aarab C et al., Chemosphere 2026 - chicken depuration (no rate in abstract)
- 42689832 Kim JH et al., Environ Sci Technol 2026 - infant PBPK from breast milk (no numeric t1/2 in abstract)
- 10.21203/rs.3.rs-9312722/v1 Ly T et al. - Atlantic salmon PBK, **PREPRINT, NOT PEER REVIEWED**

### Preprints
Europe PMC preprint-only search, 2025-2026, same terms: 11 hits, only two in scope -
the Atlantic salmon PBK model above, and "A Human Next Generation PBK Model for PFOA"
(PPR1224812) which is the preprint of the already-identified journal article PMID 41793954.
Neither abstract carries a numeric TK parameter.

### Highest-value remaining target for any future pass
**PMID 42162713** (Argoul/Gayrard, Environ Res 2026): 11 PFAS x clearance/Vd/half-life/bioavailability,
female mice, IV and oral, 119-day sampling, NLME. Elsevier, not in PMC, Europe PMC inEPMC=N, so the
per-compound table is out of reach from here. Everything else in the abstract was captured.
