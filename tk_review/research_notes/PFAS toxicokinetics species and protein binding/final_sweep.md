# Final targeted sweep - PFAS toxicokinetics

Run 2026-10-02. Output: `db/final_sweep.csv` (108 data rows), `papers/SOURCES_final_sweep.md`,
`papers/Zurlinden 2025 SUPPLEMENTARY tables from EPA repo notebook.txt`.
No existing CSV in `db/` was edited.

## Bottom line by priority

| # | Target | Outcome |
|---|---|---|
| 1 | DOG (only empty species column) | **Broken open.** 6 rows, 5 with values. All from on-disk regulatory documents; no primary dog paper exists to retrieve. |
| 2 | Anything 2025-2026 | **8 studies with numeric values** (rat, mouse, bird, sheep, cattle), 4 more logged as gaps. |
| 3 | Systematic review after Rosato 2024 | **Confirmed none.** Previous search was right. |
| 4 | Compounds with exactly one study | **6:2 diPAP and 5:3 FTCA and PFHpS gained a second source.** Cl-PFESA and FOSA attempted, logged as gaps. cC6O4 already covered - skipped. |
| 5 | Dzierlenga/Zurlinden 2025 supplementary | **Obtained, 66 rows**, via the paper's own code repository after every PMC/Europe PMC route failed. |

## 1. DOG - what is actually there, and what is not

The dog column was empty because **there is essentially one primary dog PFAS study in existence**, it is a
1988 book chapter, and it is not indexed in PubMed.

- **Hanhijarvi H, Ylinen M, Haaranen T, Nevalainen T (1988).** "A proposed species difference in the renal
  excretion of perfluorooctanoic acid in the Beagle dog and rat." In: Beynen AC, Solleveld HA (Eds.),
  *New Developments in Biosciences: Their Implications for Laboratory Animal Science*, Martinus Nijhoff,
  Dordrecht, pp. 409-412. Full citation found verbatim in both `NJ DWQI 2017...txt` (line 10376) and
  `OEHHA 2024 PFOA PFOS PHG.txt` (line 14428).

**The two regulatory tabulations of this same study disagree, and that disagreement is now recorded:**

| Source | Dog PFOA half-life | Sex split |
|---|---|---|
| NJ DWQI 2017, Table 4, p.45 (adapted from Lau 2012) | 8-13 d female, 20-30 d male | yes - male longer |
| OEHHA 2024 PHG, Section 4.1 text, p.37 | 10.6-20.1 d | sexes combined |

Unresolvable without the 1988 chapter. Both rows are in the CSV, each flagged as secondary and
cross-referenced to the other. Note the dog's direction of sex difference (male slower) is the
**opposite** of the rat.

Also recovered: **OEHHA 2024 Table A6.4, p.327** gives dog PFOA **renal clearance** - 50.8 mL/kg-day
(F) and 43 mL/kg-day (M), attributed to Kudo and Kawashima (2003) - plus GFR 5300 mL/day-kg, net
tubular reabsorption 55/63 mL/kg-day, 52%/59% reabsorbed. The dog sex difference in CLR is small
(~1.2-fold) against roughly 37-fold in the rat in the same table.

### Dog leads that were run down and came up empty
- `ATSDR 2021 Toxicological Profile Perfluoroalkyls.txt` (2.9 MB): "dog", "dogs", "beagle" and
  "canine" occur **only inside the literature-search Boolean strings** (lines 38974, 39087, 39170).
  ATSDR 2021 tabulates no dog value.
- **Griffith & Long 1980** is cited ~10 times in ATSDR but exclusively for **rat and mouse** acute and
  28-day toxicity (LC50, LD50, mortality). It is not a dog study and not a TK study.
- EPA 2024 PFOA and PFOS assessments mention "dogs" once each - only as the source of an assumed 20%
  renal blood-flow fraction for the PBPK model.
- PubMed, perfluoro*/PFAS AND dog/dogs/beagle/canine AND PK terms: **16 hits, all irrelevant** -
  perfluorocarbon blood substitutes, perfluorooctyl bromide imaging agents, partial liquid
  ventilation, organ-preservation solutions. The only genuine hit is PMID 16720684 (FOSA
  N-glucuronidation by dog liver microsomes, 2006), which is in vitro and reports no kinetic
  constants in its abstract. Logged as a gap.

**Conclusion: the dog column is empty for a real reason, not for want of searching.** It can be
populated only from regulatory secondary tabulations, which is what was done, with every row labelled.

## 2. Priority 5 - how the supplementary tables were actually obtained

Every documented route failed:
- E-utilities `efetch db=pmc` returns only `<!--The publisher of this article does not allow
  downloading of the full text in XML form.-->`
- Europe PMC `fullTextXML` -> HTTP 500; `supplementaryFiles` -> "not open access"
- Firecrawl stealth on the PMC article page **did** reveal the three filenames
  (`NIHMS2077116-supplement-Supplement1.pdf`, `Supplement2.docx`, `Supplement3.docx`), but the
  `/articles/instance/12172007/bin/...` download path is behind reCAPTCHA and then a
  **JavaScript proof-of-work** interstitial. Not solvable here.

**The route that worked:** the paper cites its own code repository, `USEPA/CPHEA-Animal-PFAS-PK`.
Cloning it gives `auxiliary_notebooks/PFAS_manuscript_results.ipynb` with **executed outputs
committed**. The cells that write the supplementary CSVs are cells 41, 45 and 47.

Two definitional findings that apply to **every Zurlinden 2025 row already in the collection**:
1. **The Vd is Vdss** - the posterior variables are literally `Vdss [pop]` and `Vdss [indiv]`.
   This settles the `vd_type` question for the whole dataset.
2. **The half-life is the terminal (beta-phase) half-life** - variable `halft_beta`.

The 66 recovered rows are posterior **IV/oral ratios** per underlying study and sex, with 95% HDI and
a ROPE[0.8, 1.2] decision. Route changed the estimate (ROPE "Reject Null") in only **4 of 66** cases:
PFHxS female Huang 2019 half-life ratio 0.663; PFOA male Kim 2016 (0.241) and Kemper 2003 (0.303);
PFHxS female Kim 2018 Vdss 2.092 (1 mg/kg) and 2.331 (4 mg/kg). Otherwise route was not resolvable
at this sample size - which is itself the useful result.

One supplementary table remains unrecovered: `SUPPL_PFAS_PK_summary.csv` (cell 41). The notebook
writes it to disk but only the empty template is displayed, so its contents are not in the committed
outputs. It would need the PMC supplement PDF or a re-run of the notebook against the MCMC traces
(`traces/` is empty in the repo).

## 3. New species-column coverage gained

- **sheep/goat**: 9 PFAS in male lambs with apparent plasma half-lives 0.3-57 d (Asshoff 2026);
  plus PFOS Fa 0.974, ka 0.098 1/h, CLrenal 0.108 L/h/kg (Inauen 2026).
- **bird**: house sparrow half-lives 29-91 d, the first wild-passerine values (Gillings 2026);
  plus chicken PFOS Fa 0.990, ka 0.005 1/h, absorption t1/2 139 h, CLrenal 0.15 L/h/kg.
- **cattle**: PFHpS added (new chemical for this species); PFOS Fa 0.954, CLrenal 0.13 L/h/kg.
- **dog**: 0 -> 6 rows.

## 4. Conventions used in db/final_sweep.csv

- **Ranges**: where a source reports only a range (dog half-lives, cattle 4-10 wk, sheep 0.3-57 d,
  bird 29-91 d, 5:3 FTCA tss, mouse MRT), `value` is left **deliberately blank** and the range sits in
  `ci_low`/`ci_high`, with `notes` saying so. `ci_low`/`ci_high` therefore means "reported range" on
  those rows and "95% CI/HDI" on the Zurlinden rows - `notes` always disambiguates.
- **Pooled ranges**: the cattle 4-10 wk range is given by the source for five analytes *together*. It
  is written to all five rows with an explicit POOLED RANGE warning, not split per analyte.
- **Gaps are rows, not silences**: 6 rows carry `parameter = "none extractable from abstract"` with the
  reason. Nothing was ever stated from memory.
- **Secondary sources are labelled** in both `study` and `peer_reviewed`.
- **Parameter names are explicit** about what they are: absorption vs elimination half-life, renal vs
  hepatic vs intrinsic vs total clearance, central vs steady-state Vd, MRT, tss, IV/oral ratio.

### One correction made during the run
Two dog clearance rows initially carried PMID 12820535 for Kudo and Kawashima 2003. On verification
that PMID is "Management of treatment-resistant epilepsy". The correct record is **PMID 12820537**,
*J Toxicol Sci* 2003;28(2):49-57, doi 10.2131/jts.28.49 - verified by PubMed author/journal search and
corrected in place, with the correction noted in the row. Likewise the Inauen 2026 DOI was verified as
`10.1007/s00204-026-04421-z`. All 17 distinct PMID/DOI pairs in the file came from a live
efetch/esummary retrieval, and all first-author names were verified against PubMed.
