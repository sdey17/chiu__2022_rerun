# SOURCES — US state agencies and non-US national agencies (PFAS toxicokinetics)

Retrieval log for PART 1 (US states) and PART 2 (non-US agencies).
Files live in `/home/user/chiu__2022_rerun/pfas_tk_review/papers/`.
Output CSV: `../db/state_international_regulatory.csv`.

## A. Already on disk from the prior (terminated) run — read from disk, not re-fetched

| Filename | Citation | Status |
|---|---|---|
| `MDH 2025 PFOA toxicological summary.pdf`/`.txt` | Minnesota Dept of Health, Toxicological Summary for PFOA | on disk |
| `MDH 2025 PFOS toxicological summary.pdf`/`.txt` | MDH, Toxicological Summary for PFOS | on disk |
| `MDH 2025 PFHxS MCL recommendation note.pdf`/`.txt` | MDH PFHxS MCL recommendation | on disk |
| `MDH 2023 PFHxS toxicological summary.pdf`/`.txt` | MDH, Toxicological Summary for PFHxS | on disk |
| `MDH 2023 PFHxA toxicological summary.pdf`/`.txt` | MDH, Toxicological Summary for PFHxA | on disk |
| `MDH 2023 PFBS toxicological summary.pdf`/`.txt` | MDH, Toxicological Summary for PFBS | on disk |
| `MDH 2018 PFBA toxicological summary.pdf`/`.txt` | MDH, Toxicological Summary for PFBA | on disk |
| `NJ DWQI 2017 PFOA health-based MCL support document.pdf`/`.txt` | NJ Drinking Water Quality Institute | on disk |
| `NJ DWQI 2018 PFOS health-based MCL support document.pdf`/`.txt` | NJ DWQI | on disk |
| `NJ DWQI 2015 PFNA health-based MCL support document.pdf`/`.txt` | NJ DWQI | on disk |
| `NJ DWQI 2023 review of interim EPA health advisories.pdf`/`.txt` | NJ DWQI | on disk |
| `Michigan SAW 2019 health-based drinking water values PFAS.pdf`/`.txt` | Michigan PFAS Science Advisory Workgroup | on disk |
| `NHDES 2019 PFAS MCL technical background report.txt` | New Hampshire DES | on disk (txt only) |
| `TCEQ 2023 PFAS toxicity factors 16 compounds.pdf`/`.txt` | Texas Commission on Environmental Quality | on disk |
| `WA DOH 2021 PFAS state action levels approach methods.pdf`/`.txt` | Washington State Dept of Health | on disk |
| `NY DOH 2022 emerging contaminant notification levels PFAS.pdf`/`.txt` | New York State DOH | on disk |
| `PA DPAG 2021 PFAS MCLG recommendations.pdf`/`.txt` + `PA DPAG 2021 PFAS MCLG workbook.pdf`/`.txt` | Pennsylvania Drinking Water PFAS Advisory Group / DEP contractor | on disk |
| `PA DEP 2022 PFAS MCL proposed rulemaking preamble.pdf`/`.txt` | Pennsylvania DEP | on disk |
| `NC SAB 2018 review GenX provisional health goal.pdf`/`.txt` | NC Secretaries' Science Advisory Board | on disk |
| `CT DPH 2024 drinking water action levels PFAS derivation.pdf`/`.txt` | Connecticut DPH | on disk |
| `RIVM 2018-0070 PFAS relative potency factor approach.pdf`/`.txt` | Netherlands RIVM | on disk |
| `UK DWI 2024 drinking water quality standards advisory group report.pdf`/`.txt` | UK Drinking Water Inspectorate / WQSAG | on disk |
| `NHMRC 2025 ADWG PFAS fact sheet.txt` | Australian NHMRC ADWG 2025 | on disk (txt only) |
| `FSANZ perfluorinated compounds page.txt` | FSANZ | on disk (txt only) |
| `WHO 2025 PFOS PFOA drinking water comments and responses to background document.pdf`/`.txt` | WHO | on disk |
| `ITRC 2020 basis of PFOA PFOS regulatory values tables.xlsx`/`.txt`, `ITRC 2025 PFAS environmental media values tables.xlsx` | ITRC | on disk |
| `OECD PFAS country information {Australia,Canada,Denmark,Germany,Japan,Korea,Netherlands,Norway,Sweden}.pdf`/`.txt` | OECD country information sheets | on disk |
| `Germany HBM-I derivation abstracts Holzer 2021.txt`, `Germany HBM-II derivation abstract Schumann 2021.txt` | German HBM Commission (abstracts only) | on disk (abstracts only) |
| `ECHA Annex XV PFAS restriction - industry commentary excerpt.pdf` | third-party commentary excerpt, NOT the ECHA annex | on disk; low value |

## B. Broken/failed captures from the prior run — need re-retrieval

| Filename | Problem |
|---|---|
| `Health Canada 2024 PFAS drinking water objective.pdf` | Not a PDF — a 19 KB French-language canada.ca HTML shell. Re-retrieval needed. |
| `NJDEP 2022 comments on WHO PFAS draft guidelines.pdf` | 212-byte Imperva/Incapsula block page. Re-retrieval needed. |

## C. This run's retrievals

### MDH (Minnesota) — URLs verified this run by md5-matching the live file against the on-disk PDF

| Chemical | URL | md5 match |
|---|---|---|
| PFOA | https://www.health.state.mn.us/communities/environment/risk/docs/guidance/gw/pfoa.pdf | yes |
| PFOS | https://www.health.state.mn.us/communities/environment/risk/docs/guidance/gw/pfos.pdf | yes |
| PFHxS | https://www.health.state.mn.us/communities/environment/risk/docs/guidance/gw/pfhxs.pdf | yes |
| PFHxA | https://www.health.state.mn.us/communities/environment/risk/docs/guidance/gw/pfhxa.pdf | yes |
| PFBA | https://www.health.state.mn.us/communities/environment/risk/docs/guidance/gw/pfba2summ.pdf | yes |
| PFBS | https://www.health.state.mn.us/communities/environment/risk/docs/guidance/gw/pfbssummary.pdf | yes |

Index page that lists all of them (not bot-protected): https://www.health.state.mn.us/communities/environment/risk/guidance/gw/table.html
Companion "info" sheets also exist (`pfoainfo.pdf`, `pfosinfo.pdf`, `pfhxsinfo.pdf`, `pfbainfo.pdf`, `pfbsinfo.pdf`) and `pfhxsnote.pdf` (= the on-disk `MDH 2025 PFHxS MCL recommendation note.pdf`).

### NJ DWQI — URLs verified this run by md5-matching live file vs on-disk PDF

| Chemical | URL | md5 match |
|---|---|---|
| PFOA (2017) | https://www.nj.gov/dep/watersupply/pdf/pfoa-appendixa.pdf | yes |
| PFOS (2018) | https://www.nj.gov/dep/watersupply/pdf/pfos-recommendation-appendix-a.pdf | yes |
| PFNA (2015) | https://www.nj.gov/dep/watersupply/pdf/pfna-health-effects.pdf | yes |

Dead ends tried for PFNA before finding the right path: `pfna-appendixa.pdf`, `pfnaappendixa.pdf`, `pfna_recommendation.pdf` (= the DWQI recommendation letter, not the support document), `pfna.pdf`, under both `www.nj.gov/dep/watersupply/pdf/` and `dep.nj.gov/wp-content/uploads/watersupply/`. NJ serves BOTH hosts; `dep.nj.gov/wp-content/uploads/...` returns an HTML 404 page with a `.pdf` extension, so always check `file`.

### Re-retrieved this run (fixing broken prior captures)

| Filename | URL | Status |
|---|---|---|
| `NJDEP 2022 comments on WHO PFAS draft guidelines.pdf`/`.txt` | https://dep.nj.gov/wp-content/uploads/dsr/njdep-comments-who-pfas-guidelines.pdf | SUCCESS (445 KB, 2257 lines) — replaces the 212-byte Incapsula block page |

### Michigan MPART Science Advisory Workgroup — URL verified this run (md5 match vs on-disk PDF)

https://www.michigan.gov/-/media/Project/Websites/PFAS-Response/Reports/2019-Health-Based-Drinking-Water-Value-Recommendations-PFAS-MI.pdf

Dead ends: `.../Reports/Health-Based-Drinking-Water-Value-Recommendations-for-PFAS-in-Michigan.pdf` under both `www.michigan.gov/pfasresponse/-/media/...` and `www.michigan.gov/-/media/...` return HTML 404 bodies. The live path needs the `2019-` prefix and the abbreviated `PFAS-MI` suffix. michigan.gov is NOT bot-protected; a plain UA suffices, and the `?rev=`/`?hash=` query strings are optional.

