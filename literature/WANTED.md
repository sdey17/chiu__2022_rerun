# Papers to add as PDFs

> **Status:** Rosato 2024 (item 1) has been added and extracted. Three
> further PDFs were added that were not on this list - Andersson 2025,
> Fischer 2024 and Fischer 2025 - and two of them changed the appraisal
> more than anything still outstanding. See `APPRAISAL.md`.
>
> Still wanted: Zhang 2013, Li 2022 (only its summary rows are in hand,
> via Rosato's table), and the two Regulatory Toxicology papers.

Not in PubMed Central, so unreachable even with PMC access open. Drop
the PDFs anywhere in the repo and they can be extracted the way the Chiu
paper and SI were.

Priority order: the value each adds to `studies.csv` and to the
appraisal.

## 1. ~~The 2023 systematic review and meta-analysis~~  [ADDED - Rosato 2024]

Cavalieri d'Oro et al. (exact authorship to confirm from the PDF), 2023.
"Estimation of per- and polyfluoroalkyl substances (PFAS) half-lives in
human studies: a systematic review and meta-analysis."
*Environmental Research*, 2023.
PMID 38008199 - doi:10.1016/j.envres.2023.117743

Covers 13 studies (5 general population, 8 occupational) with a
random-effects meta-analysis and OHAT risk-of-bias scoring. Its
extraction table would roughly triple `studies.csv` in one step, and its
risk-of-bias assessment is an independent check on the tiering in
`APPRAISAL.md`.

## 2. Zhang et al. 2013  [PIVOTAL, AND CONTESTED]

Zhang Y, Beesoon S, Zhu L, Martin JW. "Biomonitoring of perfluoroalkyl
acids in human urine and estimates of biological half-life."
*Environmental Science & Technology* 2013;47(18):10619-27.
PMID 23980546 - doi:10.1021/es401905e

The single study the ARA collaboration calls "the single best value" for
the short-half-life position (PFOA GM 1.3 y). Worth having because of a
direct conflict between two sources we already hold:

- The ARA (2022) treats it as the least confounded study available.
- The 2023 systematic review **excluded** studies estimating half-life
  "based solely on renal clearance", which is exactly this method.

Its own abstract also notes urinary excretion is the major route only
for short PFCAs (C <= 8), and that "other routes likely contribute" for
PFOS and PFHxS - so the method's validity differs by chemical. Estimates
in it span 0.5 y to 90 y across isomers, so which number gets quoted
matters enormously.

## 3. Li et al. 2022, Ronneby determinants  [BEST NEXT ANALYSIS]

Li Y, et al. "Determinants of serum half-lives for linear and branched
perfluoroalkyl substances after long-term high exposure - a study in
Ronneby, Sweden." *Environment International* 2022.
PMID 35447437 - doi:10.1016/j.envint.2022.107198

114 participants, up to ten blood samples over 2014-2018, linear mixed
models, linear and branched isomers reported separately. Two reasons to
want it:
- It is the cleanest test of whether INDIVIDUAL half-life tracks
  INDIVIDUAL starting concentration, with study, lab, background and
  cessation date all held constant. That is a far stronger version of
  the cross-cohort slope in `human_dose_test.py`.
- Separating isomers addresses bias (3) in `APPRAISAL.md`, which almost
  no other study does.

## 4 and 5. The two expert-review papers

Dourson ML, Gadagbui B. "The Dilemma of perfluorooctanoate (PFOA) human
half-life." *Regulatory Toxicology and Pharmacology* 2021;126:105025.
PMID 34400261 - doi:10.1016/j.yrtph.2021.105025

"The Conundrum of the PFOA human half-life, an international
collaboration." *Regulatory Toxicology and Pharmacology* 2022;132:105185.
PMID 35537634 - doi:10.1016/j.yrtph.2022.105185

These argue the consensus half-life is roughly 2-3x too long. We have
their abstracts and conclusions, but not their reasoning or the
adjustments they propose. Needed to judge the argument rather than just
record its conclusion.

## 6 and 7. Firefighter cohorts (lower priority)

Nilsson S, et al. "Serum concentration trends and apparent half-lives of
per- and polyfluoroalkyl substances (PFAS) in Australian firefighters."
*International Journal of Hygiene and Environmental Health* 2022.
PMID 36162311 - doi:10.1016/j.ijheh.2022.114040

"Apparent Half-Lives of Chlorinated-Perfluorooctane Sulfonate and
Perfluorooctane Sulfonate Isomers in Aviation Firefighters."
*Environmental Science & Technology* 2022.
PMID 36367310 - doi:10.1021/acs.est.2c04637

Both give occupational estimates at the long end (PFOA 5.0 y, PFHxS
7.8 y). Useful for the range, but occupational cohorts are Tier 3 here
because ongoing exposure is hard to exclude - so they add breadth rather
than resolving anything.

## Already retrieved (in `fulltext/`, no action needed)

Olsen 2007, Bartell 2010, Seals 2011, Li 2018, Worley 2017 (both the
biomonitoring paper and the PBPK one), Worley 2015 rat PBPK, the GenX
fluoroether study, and the Chinese fluorochemical worker cohort.
