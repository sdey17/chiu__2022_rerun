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

### New Hampshire DES — URL identified and content-confirmed this run

https://www.des.nh.gov/sites/g/files/ehbemt341/files/documents/r-wd-19-29-final.pdf  (report R-WD-19-29, 57 pages)

`www.des.nh.gov` sits behind **Akamai** and returns a 403 "Access Denied" HTML body (reference `errors.edgesuite.net`) to `curl` for this path even with a complete browser header set including Referer and Sec-Fetch-*. Oddly, other PDFs in the same directory (e.g. `r-wd-19-25.pdf`) DO serve to curl, so the block is path- or rate-dependent rather than blanket. **Firecrawl scrape with `parsers: ["pdf"]` retrieves it successfully** and was used to confirm the first 3 pages match the on-disk `.txt`. The on-disk `.txt` (from the prior run, 162 KB) is a Firecrawl markdown conversion, which is why it contains `$$...$$` LaTeX blocks for the DAF equations; no PDF sibling exists.

Wrong guesses: `r-wd-19-25.pdf` (that is a Haunted Lake phosphorus TMDL), and the `.../documents/2020-01/` date-prefixed directory (404).

### Texas TCEQ — URL verified this run (md5 match)

https://www.tceq.texas.gov/downloads/toxicology/pfc/pfcs.pdf  (February 14, 2023)

Dead ends: `/downloads/toxicology/dsd/final/pfcs.pdf` and `/downloads/toxicology/dsd/short-summaries/pfas.pdf` both 404. The live directory is `/downloads/toxicology/pfc/`. Not bot-protected.

### New York State DOH — URL identified this run (md5 match vs on-disk 343-page PDF)

https://health.ny.gov/facilities/public_health_and_health_planning_council/meetings/2022-12-08/docs/full_council_agenda.pdf  (343 pp, md5 7dc6d2e5...)

**Caution for anyone re-running this:** the sibling `attachments.pdf` at the same path now serves a DIFFERENT, 55-page document that does NOT contain the PFAS Regulatory Impact Statement. `codes_committee_agenda.pdf` (147 pp) contains the same RIS text but is a different file. The PFAS clearance values are on RIS pages 50-53. health.ny.gov is not bot-protected.

### North Carolina SAB (GenX) — URL verified this run (md5 match)

https://files.nc.gov/ncdeq/GenX/SAB/SAB-GenX-Report-draft-08-29-2018.pdf  (27 pp, md5 b23e3cab...)

A 25-page variant is mirrored at https://www.nccoast.org/wp-content/uploads/2018/10/DEQ-and-DHHS-Science-Advisory-Board-Health-Goal-for-GenX.pdf (different md5, likely without the appendices). Guesses that 403'd: `ncdenr.s3.amazonaws.com/s3fs-public/GenX/SAB/...` and `files.nc.gov/ncdeq/GenX/SAB/SAB-GenX-Recommendations-FINAL-2018.pdf`. Related NC documents found but not retrieved: the final appendices (`deq.nc.gov/energy-mineral-and-land-resources/demlr/sab-genx-report-final-appendices-10-30-2018/download`) and the DHHS benchmark-dose modelling report (`deq.nc.gov/waste-management/dwm/sw/rules/toxics/risk/sab/nc-dhhs-bmd-report-26may2018/download`).

### Connecticut DPH — URL verified this run (md5 match)

https://www.newmoa.org/wp-content/uploads/2024/10/FieldsCheToxicologyApril2024.pdf  (30 slides, md5 37e5becc...)

The on-disk file is a CONFERENCE PRESENTATION (Northeast Conference on the Science of PFAS, 2 April 2024) by CT DPH toxicologists Cheryl Fields and Xun Che, hosted by NEWMOA, not a CT DPH web page. It documents the July 2023 Action Levels for GenX, PFHxA, PFBS, PFBA, 6:2 Cl-PFESA and 8:2 Cl-PFESA, with full DAF arithmetic on slides 22-27. The CT DPH circular letters (`portal.ct.gov/dph/-/media/.../ehdw_cl-2022-30_revision_of_drinking_water_al_for_pfas-pws.pdf` and `ehdw_cl_2024-17_epa_npdwr_for_pfas.pdf`) announce the levels but were not retrieved and do not carry the TK derivations.

### Washington State DOH — URL verified this run (md5 match)

https://doh.wa.gov/sites/default/files/2022-02/331-673.pdf  (DOH 331-673, revised 1 Nov 2021, md5 fb008ccb...)

NOTE: a DIFFERENT, larger file (2.2 MB vs 1.57 MB, md5 1e29beca...) is served at `https://doh.wa.gov/sites/default/files/legacy/Documents/Pubs/331-673.pdf` - presumably an earlier revision. Use the `2022-02` path for the November 2021 revision that matches the on-disk copy. doh.wa.gov is not bot-protected.

### Pennsylvania — URLs

- Drexel PFAS Advisory Group report (Jan 2021), **verified this run by md5 match**:
  https://files.dep.state.pa.us/PublicParticipation/Public%20Participation%20Center/PubPartCenterPortalFiles/Environmental%20Quality%20Board/2021/June%2015/03_PFAS%20Petition/01a_App%201%20Drexel%20PFAS%20Report%20January%202021.pdf
- PA DEP / EQB proposed rulemaking preamble (25 Pa. Code Ch. 109, Safe Drinking Water PFAS MCL Rule): the on-disk `.pdf` was not md5-matched to a live URL this run. The rule text is published at
  https://www.pacodeandbulletin.gov/Display/pabull?file=/secure/pabulletin/data/vol53/53-2/46.html — recorded in the CSV as the citation URL and flagged here as NOT md5-verified.
- Also found but not retrieved: PA DEP Bureau of Safe Drinking Water comment-and-response document
  `files.dep.state.pa.us/PublicParticipation/.../04a_7-569_PFAS_Final_CRD.pdf` (76 pp) and the PFAS MCL Rule FAQ
  `files.dep.state.pa.us/Water/BSDW/DrinkingWaterManagement/Regulations/PFAS%20MCL%20Rule%20FAQs_June2024.pdf`.
- `PA DPAG 2021 PFAS MCLG workbook.pdf` on disk (md5 d8996798...) was not matched to a URL.

### ITRC census tables (on disk from the prior run, read this run)

- `ITRC 2020 basis of PFOA PFOS regulatory values tables.xlsx` — "ITRC PFAS Basis for PFOA and PFOS values in water", March 2020. Sheets: ReadMe, Water PFOA, Water PFOS. Column group "Kinetics" gives, for every jurisdiction, the method used to convert administered dose to internal serum level AND the method used to derive the human equivalent dose — the single most efficient census of agency TK methods found. Covers Alaska, California OEHHA, Maine, Massachusetts, Michigan, Minnesota, New Jersey, North Carolina, Texas, US EPA OW, Vermont and Canada.
- `ITRC 2025 PFAS environmental media values tables.xlsx` — "ITRC PFAS Regulations, Guidance, and Advisory Values", December 2025 (Version 2 corrections). Sheets: Water/Soil/Air Table, References, Pending Criteria, Updates. This 2025 workbook carries the VALUES but, per its own ReadMe, "does not include the bas[is]" — so it is a value census only, with no TK columns.
- Landing page for both: https://pfas-1.itrcweb.org/external-data-tables/  (guidance document at https://pfas-1.itrcweb.org)

All rows extracted from these workbooks are labelled "SECOND-HAND (ITRC-reported)" in the CSV. Two internal inconsistencies in the 2020 workbook are recorded rather than silently corrected: the Michigan DHHS PFOA clearance of 9.9e-5 L/kg-day (inconsistent with Vd 0.17 x ln2/840 d = 1.4e-4), and the Michigan DHHS PFOS clearance of 6.99e-5 L/kg-day attributed to "t1/2 of 840 days (2.3 yrs) from Bartell et al. (2010)", which is the PFOA half-life.

### RIVM (Netherlands) — URL verified this run (md5 match)

https://www.rivm.nl/bibliotheek/rapporten/2018-0070.pdf  (RIVM Report 2018-0070, 72 pp, md5 a5829357...)

Annex II Table A2 (pp. 43-44) is a five-species (rat / mouse / PIG / monkey / human) terminal half-life compilation for 12 PFAS, with male and female values separately — the most complete cross-species, sex-resolved half-life table found in any agency document in this survey. `rvs.rivm.nl/sites/default/files/2018-11/` 404s.

