# Retrieval log — PFAS volume of distribution & dose-dependence

Scope: primary-literature Vd provenance and multi-dose (saturation) studies.
Retrieval window: 2026-10-01. All attempts logged, success and failure.

Column key: `status` = SUCCESS (file on disk), METADATA (abstract/metadata only,
no full text), SECONDARY (value obtained from an agency tabulation that cites the
primary paper — primary PDF not obtained), FAIL (could not retrieve).

## Files on disk in this directory

| File | Full citation | PMID / DOI | URL | Date | Status |
|---|---|---|---|---|---|
| `Huang 2019 PFBS PFHxS PFOS rat multidose toxicokinetics.txt` | Huang MC, Dzierlenga AL, Robinson VG, Waidyanatha S, DeVito MJ, Eifrid MA, Granville CA, Gibbs ST, Blystone CR. Toxicokinetics of perfluorobutane sulfonate (PFBS), perfluorohexane-1-sulphonic acid (PFHxS), and perfluorooctane sulfonic acid (PFOS) in male and female Hsd:Sprague Dawley SD rats after intravenous and gavage administration. Toxicol Rep. 2019;6:645–655. | PMID 31334035; PMC6624215; doi:10.1016/j.toxrep.2019.06.016 | https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6624215/fullTextXML | 2026-10-01 | SUCCESS (text + all 4 PK tables extracted from Europe PMC JATS XML). **PDF FAILED** — PMC `/pdf/main.pdf`, `europepmc.org/articles/...?pdf=render` and ScienceDirect `pdfft` all returned HTML, not PDF. |
| `Gasiorowski 2022 plasma blood donation PFAS firefighters RCT.txt` | Gasiorowski R, Forbes MK, Silver G, Krastev Y, Hamdorf B, Lewis B, Tisbury M, Cole-Sinclair M, Lanphear BP, Klein RA, Holmes N, Taylor MP. Effect of Plasma and Blood Donations on Levels of Perfluoroalkyl and Polyfluoroalkyl Substances in Firefighters in Australia: A Randomized Clinical Trial. JAMA Netw Open. 2022;5(4):e226257. | PMID 35394514; PMC8994130; doi:10.1001/jamanetworkopen.2022.6257 | https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8994130/fullTextXML | 2026-10-01 | SUCCESS (text + baseline table). **PDF FAILED** (JAMA CDN returned HTML). |
| `ATSDR 2021 Toxicological Profile Perfluoroalkyls.pdf` / `.txt` | ATSDR. Toxicological Profile for Perfluoroalkyls. US DHHS, May 2021. | — | https://www.atsdr.cdc.gov/toxprofiles/tp200.pdf | pre-existing in repo | SUCCESS (pre-existing). Tables 3-5, 3-6, A-3, A-4 and §3.1.5 PBPK summaries used heavily. |
| `EPA 2024 PFOA human health toxicity assessment.pdf` / `.txt` | US EPA. Final Human Health Toxicity Assessment for Perfluorooctanoic Acid (PFOA) and Related Salts. EPA-815-R-24-006, April 2024. | — | https://www.epa.gov/sdwa/ | pre-existing | SUCCESS. §3.3.1.2.5, §3.3.2.2–3.3.2.3, Table 4-3, Table 4-6 used. |
| `EPA 2024 PFOS human health toxicity assessment.pdf` / `.txt` | US EPA. Final Human Health Toxicity Assessment for PFOS. EPA-815-R-24-007, April 2024. | — | https://www.epa.gov/sdwa/ | pre-existing | SUCCESS (little Vd content; PFOS Vd handled in Appendix). |
| `EPA 2023 IRIS PFHxA toxicological review.pdf` / `.txt` | US EPA. IRIS Toxicological Review of Perfluorohexanoic Acid (PFHxA) and Related Salts. EPA/635/R-23/027Fa, 2023. | — | https://iris.epa.gov/ | pre-existing | SUCCESS. §5.2.1, Tables 5-3/5-4 — Vd for rat/mouse/monkey and the explicit no-dose-dependence finding. |
| `OEHHA 2024 PFOA PFOS PHG.pdf` / `.txt` | OEHHA. Public Health Goals for PFOA and PFOS in Drinking Water. California EPA, March 2024. | — | https://oehha.ca.gov/water/public-health-goal/final-public-health-goals-perfluorooctanoic-acid-and-perfluorooctane | pre-existing | SUCCESS. **§4.8 Table 4.8.1 is the single best published Vd-provenance table** (reference, data source, species, Vd, method). Table 4.8.2 = OEHHA re-derivation from Andersen 2006. |
| `OEHHA 2021 PFOA PFOS PHG first draft.pdf` / `.txt` | OEHHA. PHG for PFOA and PFOS, first public review draft, June 2021. | — | https://oehha.ca.gov/ | pre-existing | SUCCESS. |
| `OEHHA 2024 PFOA PFOS PHG responses to comments.pdf` / `.txt` | OEHHA. Responses to Public Comments, PFOA/PFOS PHG, 2024. | — | https://oehha.ca.gov/ | pre-existing | SUCCESS (contains the dispute over Vd selection). |
| `OEHHA 2024 PFHxA notification level.pdf` / `.txt` | OEHHA. Notification level for PFHxA, 2024. | — | https://oehha.ca.gov/ | pre-existing | SUCCESS. |

## Metadata-only retrievals (abstract + citation verified via PubMed MCP; full text not obtained)

| Citation | PMID / DOI | Status | Why sought |
|---|---|---|---|
| Thompson J, Lorber M, Toms LML, Kato K, Calafat AM, Mueller JF. Use of simple pharmacokinetic modeling to characterize exposure of Australians to perfluorooctanoic acid and perfluorooctane sulfonic acid. Environ Int. 2010;36(4):390–397. | PMID 20236705; doi:10.1016/j.envint.2010.02.008 | METADATA (abstract confirms the Vd derivation verbatim) | **The origin of the PFOA Vd = 170 mL/kg and PFOS Vd = 230 mL/kg.** Abstract: "A volume of distribution was calibrated for PFOA to a value of 170 ml/kg bw using data from two communities in the United States where the residents' serum concentrations could be assumed to result primarily from a known and characterized source, drinking water contaminated with PFOA by a single fluoropolymer manufacturing facility. For PFOS, a value of 230 ml/kg bw was used, based on adjustment of the PFOA value." Paywalled (Elsevier). |
| Harada K, Inoue K, Morikawa A, Yoshinaga T, Saito N, Koizumi A. Renal clearance of perfluorooctane sulfonate and perfluorooctanoate in humans and their species-specific excretion. Environ Res. 2005;99(2):253–261. | PMID 16194675; doi:10.1016/j.envres.2004.12.003 | METADATA | Source of the human PFOA/PFOS Vd = 0.3 L/kg used by ATSDR Table A-3. |
| Ohmori K, Kudo N, Katayama K, Kawashima Y. Comparison of the toxicokinetics between perfluorocarboxylic acids with different carbon chain length. Toxicology. 2003;184(2-3):135–140. | PMID 12499116; doi:10.1016/s0300-483x(02)00573-5 | METADATA | Rat Vss for PFHpA/PFOA/PFNA/PFDA, both sexes; abstract states Vss "not much different between PFCAs and between sexes"; CL and CLR per compound; plasma protein binding >98%. |
| Kudo N, Suzuki E, Katakura M, Ohmori K, Noshiro R, Kawashima Y. Comparison of the elimination between perfluorinated fatty acids with different carbon chain length in rats. Chem Biol Interact. 2001;134(2):203–216. | PMID 11311214; doi:10.1016/s0009-2797(01)00155-7 | METADATA | The "Kudo 2001" paper; its dose-dependence is of *testosterone*, not of PFOA dose (see notes). |
| Kudo N, Sakai A, Mitsumoto A, Hibino Y, Tsuda T, Kawashima Y. Tissue distribution and hepatic subcellular distribution of perfluorooctanoic acid at low dose are different from those at high dose in rats. Biol Pharm Bull. 2007;30(8):1535–1540. | PMID 17666816; doi:10.1248/bpb.30.1535 | METADATA | **Direct measured evidence that PFOA tissue distribution is dose-dependent** (0.041 vs 16.56 mg/kg IV). |
| Sundström M, Chang SC, Noker PE, Gorman GS, Hart JA, Ehresman DJ, Bergman Å, Butenhoff JL. Comparative pharmacokinetics of perfluorohexanesulfonate (PFHxS) in rats, mice, and monkeys. Reprod Toxicol. 2011;33(4):441–451. | PMID 21856411; doi:10.1016/j.reprotox.2011.07.004 | METADATA | Monkey PFHxS Vd (0.287 M / 0.213 F L/kg, via ATSDR); mouse 1 vs 20 mg/kg clearance. (Often cited as "Chang et al. 2012" or "Sundström et al. 2012" — same paper, 2011 e-pub / 2012 issue.) |
| Chang SC, Noker PE, Gorman GS, Gibson SJ, Hart JA, Ehresman DJ, Butenhoff JL. Comparative pharmacokinetics of perfluorooctanesulfonate (PFOS) in rats, mice, and monkeys. Reprod Toxicol. 2012;33(4):428–440. | PMID 21889587; doi:10.1016/j.reprotox.2011.07.002 | METADATA (values taken from ATSDR Table 3-6) | Rat 2 vs 15 mg/kg and mouse 1 vs 20 mg/kg PFOS clearance — a true multi-dose, same-sex comparison. |
| Dzierlenga AL, Robinson VG, Waidyanatha S, DeVito MJ, Eifrid MA, Gibbs ST, Granville CA, Blystone CR. Toxicokinetics of perfluorohexanoic acid (PFHxA), perfluorooctanoic acid (PFOA) and perfluorodecanoic acid (PFDA) in male and female Hsd:Sprague Dawley SD rats following intravenous or gavage administration. Xenobiotica. 2020;50(6):722–732. | PMID 31680603; doi:10.1080/00498254.2019.1683776 | METADATA; Vd values via OEHHA Table 4.8.1, clearances via EPA PFHxA IRIS §5.2.1 | The companion NTP carboxylate study; multi-dose PFOA/PFHxA/PFDA rat. Taylor & Francis paywall. |
| Huang MC et al. Corrigendum to Toxicol Rep 6:645–655. Toxicol Rep. 2021;8:365. | PMID 33665134; PMC7902757; doi:10.1016/j.toxrep.2021.02.001 | METADATA (Europe PMC record carries no body text; corrigendum content not retrieved) | **GAP** — the nature of the correction to the 2019 NTP rat PK tables could not be established. Values in `vd_clearance.csv` are from the 2019 tables and are flagged accordingly. |

## Secondary-sourced values (primary not retrieved; agency tabulation cited)

| Primary study | Value(s) taken | Secondary source used | Status |
|---|---|---|---|
| Butenhoff JL et al. 2004 (cynomolgus monkey PFOA, Toxicology 196:95–116) | Vd 181 mL/kg (M), 198 mL/kg (F); CL 12.4 (M), 5.3 (F) mL/d/kg | OEHHA 2024 PHG Table 4.8.1; ATSDR 2021 Tables 3-6, A-3 | SECONDARY |
| Kemper RA 2003 (unpublished DuPont rat PFOA study, Haskell) | Vd 211–264 mL/kg; CL by dose, both sexes; dose-dependent female t½ 3.2/3.5/4.6/16.2 h at 0.1/1/5/25 mg/kg | OEHHA 2024 PHG Table 4.8.1 (citing Vestergren & Cousins 2009); ATSDR 2021 Tables 3-5, 3-6 and §3.1.4 | SECONDARY — unpublished, never peer-reviewed, yet underpins Wambaugh 2013 and Worley & Fisher 2015 rat calibration |
| Andersen ME, Clewell HJ, Tan YM, Butenhoff JL, Olsen GW 2006 (Toxicology 227:156–164) | Vdc 140 (PFOA) / 220 (PFOS) mL/kg; k12 3.3 /h; k21 0.1 /h | OEHHA 2024 PHG Table 4.8.2 | SECONDARY. **PDF FAIL** — Oxford Academic / Elsevier page fetched for Toxicol Sci returned the wrong article; numeric Tm and KT not obtained from the primary. |
| Loccisano AE et al. 2011 (Regul Toxicol Pharmacol 59:157–175), 2012a/b (Reprod Toxicol), 2013 | Free fractions, Tm/KT ratios, partition coefficients, provenance of human Tm | ATSDR 2021 §3.1.5.1–3.1.5.2 | SECONDARY — numeric Tm and KT (µg/h/kg and µg/L) not obtained; only the ratios Tm/KT that ATSDR prints |
| Fàbrega F et al. 2014, 2016 | Human vs rat tissue:plasma partition coefficients for PFOA and PFOS | ATSDR 2021 §3.1.5.8 | SECONDARY |
| Kim SJ et al. 2018 (PFHxS rat+human PBPK, Arch Toxicol) | Partition coefficients, free fractions, Tm/KT ratios | ATSDR 2021 §3.1.5.9 | SECONDARY |
| Worley RR, Fisher J 2015a/b; Worley et al. 2017 | Model structure, saturable apical/basolateral transport, in vitro Km provenance | ATSDR 2021 §3.1.5.6–3.1.5.7 | SECONDARY — numeric Km/Vmax not obtained |
| Chang SC et al. 2008 (PFBA, Toxicology 251:60) | Rat/monkey PFBA CL; mouse dose-dependent CL at 10/30/100 mg/kg | ATSDR 2021 §3.1.4 and Table 3-6 | SECONDARY |
| Chengelis CP et al. 2009a (PFBS/PFHxA, Reprod Toxicol) | Rat/monkey PFBS and PFHxA CL and Vd | ATSDR 2021 Table 3-6; EPA 2023 PFHxA IRIS §5.2.1 | SECONDARY |
| Olsen GW et al. 2009 (PFBS, Chem Biol Interact 179:3) | Rat and monkey PFBS CL | ATSDR 2021 Table 3-6 | SECONDARY |
| Weaver YM et al. 2010 | Rat OAT1 Km for PFOA = 43.2 µM | OEHHA 2024 PHG (line 18191 of text extraction) | SECONDARY |
| Harris MW, Barton HA 2008 | Saturable albumin binding: Kd 1e-7 M, Bmax 4.1e-4 M | ATSDR 2021 §3.1.5.5 | SECONDARY |
| Daikin Industries 2010 (mouse PFHxA, 35/175/350 mg/kg) | Cmax/dose 2.76 / 1.88 / 1.30 kg/L; t½ 0.9–1.2 h, no dose trend | EPA 2023 PFHxA IRIS §3.1 | SECONDARY (unpublished company study) |
| Convertino M et al. 2018 | Plateau in plasma PFOA with increasing dose in cancer patients | ATSDR 2021 §3.1.4 | SECONDARY |
| Andersson E et al. 2025 | Measured human Vd: PFOA 0.074, PFOS 0.093 L/kg | `../literature/APPRAISAL.md` §8 (pre-existing in this repo) | SECONDARY — not re-verified in this pass |

## Failed retrieval attempts (explicit)

| Target | Method tried | Result |
|---|---|---|
| Huang 2019 Toxicol Rep PDF | `pmc.ncbi.nlm.nih.gov/articles/PMC6624215/pdf/main.pdf`; `pmc.../instance/6624215/pdf/main.pdf`; `europepmc.org/articles/PMC6624215?pdf=render`; `sciencedirect.com/.../pdfft` | All returned HTML, not PDF. Text + tables recovered from Europe PMC JATS XML instead. |
| Gasiorowski 2022 JAMA Netw Open PDF | `pmc.../instance/8994130/pdf/...` | HTML returned. Text recovered from Europe PMC XML. |
| Andersen ME et al. 2006 numeric Tm / KT | WebFetch of Oxford Academic Toxicol Sci article page | Wrong article served (Fasano 2006). Values not obtained from primary. |
| Thompson et al. 2010 full text | PubMed MCP full-text (not in PMC); no OA copy found | Abstract only. The abstract nevertheless states the derivation explicitly. |
| Loccisano et al. 2011/2012 numeric Tm, KT, partition coefficients | Web search | Only secondary descriptions and one third-party restatement (human PFOS PL 2.03, PK 1.26, PRest 0.2) found. Primary tables not obtained. |
| Dzierlenga 2020 Xenobiotica full tables | PubMed (not in PMC) | Paywalled. Vd values obtained via OEHHA Table 4.8.1; clearances via EPA PFHxA IRIS. |
| Numata J et al. 2014 (pig PK); Pizzurro DM et al. 2019 (RTP cross-species half-lives); Fenton SE et al. 2021 (ETC review); Chou WC & Lin Z 2019/2021; Cheng W & Ng CA; Gomis MI et al. 2017; Lin Z et al. 2023; Tan YM et al. 2008; Butenhoff 2012; Vanden Heuvel 1991; Olsen 2009 human PFBS half-life | Not attempted in this pass | **GAP — out of budget.** Flagged for a follow-up pass. Pizzurro 2019, Fenton 2021 and Lin 2023 are reviews and would mostly duplicate ATSDR/EPA/OEHHA tabulations already captured. |

---

## Addendum (same session): gap-closing sources already present in `papers/`, retrieved by parallel researchers

These were in the directory when I returned to it and they close three of my stated gaps.
I did not re-retrieve them; I mined the existing `.txt` extractions. Retrieval provenance for each
is logged in `SOURCES_human.md`, `SOURCES_transporters.md` and `SOURCES_regulatory.md` by whoever
fetched it. Listed here because the values I extracted from them now appear in `../db/*.csv`.

| File used | Citation | PMID / DOI | What it closed |
|---|---|---|---|
| `Abraham 2024 single oral dose 15 PFAS kinetics volunteer.txt` | Abraham K, Mertens H, Richter L, Mielke H, Schwerdtle T, Monien BH. Kinetics of 15 per- and polyfluoroalkyl substances (PFAS) after single oral application as a mixture – a pilot investigation in a male volunteer. Environ Int. 2024;193:109047. | PMID 39476597; doi:10.1016/j.envint.2024.109047 | **The "no measured human Vd" gap.** Tables 2, 3 and 4 give measured Vd, C0, kel, half-life, urinary/total/filtration/fecal clearance and fraction unbound in plasma for 15 PFAS in one subject. Open access. |
| `Worley 2015 PBPK kidney transporters PFOA rat.txt` | Worley RR, Fisher J. Application of Physiologically-Based Pharmacokinetic Modeling to Explore the Role of Kidney Transporters in Renal Reabsorption of Perfluorooctanoic Acid in the Rat. Toxicol Appl Pharmacol. 2015;289(3):428–441. | PMID 26522833; PMC4662604; doi:10.1016/j.taap.2015.10.017 | **The "numeric apical transporter Km" gap.** Table 3: Km_apical (Oatp1a1) = 52.3 µg/mL (Weaver et al. 2010); Km_baso (mean Oat1/Oat3) = 27.20 µg/mL (Nakagawa et al. 2007); Vmax_apicalC 0.947 and Vmax_basoC 0.04 mg/h/kg^0.75; free fraction 0.09 (fitted); RAFapi 35.0 (M) vs 0.001356 (F); RAFbaso 4.07 (M). |
| `Lau 2020 PFBS mouse PK.txt` | Lau C et al. (PFBS pharmacokinetics and hepatic transcriptional responses in CD-1 mice). Toxicology, 2020. | not captured in this pass | **Part of the "mouse partition coefficient" and the "PFBS dose-dependence" gaps.** Mouse PFBS Vd 0.32–0.40 L/kg (both sexes), t½ 5.8 h (M) / 4.5 h (F), liver:serum 0.2–0.3, kidney:serum 0.1–0.2, and the explicit statement that clearance was linear with dose across 30 and 300 mg/kg. |

### Gaps that remain after the addendum
- Mouse-versus-rat tissue:plasma partition coefficients for **PFOA and PFOS** side by side are still missing. The only mouse values recovered are for PFBS (Lau 2020), and they conflict with Bogdanska 2014 (liver:blood 1.4) and with Olsen 2009's rat value (liver 9.6×) by about an order of magnitude — plausibly a single-gavage versus 5-day-dietary difference, as Lau et al. themselves suggest.
- Andersen et al. 2006 numeric Tm / KT: still not obtained. The Worley & Fisher Km values now serve the same purpose better, because they are in µg/mL rather than model-internal units.
- Huang et al. 2021 corrigendum content: still not obtained.
