# PFAS half-life literature: estimates and how much to trust them

Expands the two-paper comparison in `../species_dose` to the wider human
literature. Two files matter:

- **`APPRAISAL.md`** - why published human PFOA half-lives span 17-fold
  (0.5 to 8.5 years), the six assumptions that drive the spread and which
  direction each biases, and a tiering of studies by design rather than
  by reputation.
- **`studies.csv`** - the structured extraction: one row per
  chemical-per-study estimate, with the design fields that determine
  trustworthiness (statistic reported, follow-up length, whether exposure
  had ceased, whether background was modelled, whether isomers were
  separated) and a `verified` column recording where each number came
  from.

`screen_literature.py` reproduces the PubMed search and screening.

## Provenance

Searched via the PubMed MCP server on 2026-09-29; 199 hits on the
title-restricted query, 74 abstracts screened. Every number in
`studies.csv` was read from the paper's own abstract in that session
except where `verified` says otherwise (`secondary` = taken from another
paper's citation; `full text` = read from the PDF in this repository).

Journal websites and PMC are blocked by this environment's network
policy, so full text was only available for PMC-hosted open-access
papers. That is the main limit on this collection.
