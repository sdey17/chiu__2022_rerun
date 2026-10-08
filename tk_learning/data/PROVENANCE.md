# Where these data came from

## How to cite it

**EPA compiled these data; they did not generate them.** Citing only
the EPA paper under-credits the nine laboratories that ran the
experiments. Cite the compilation, and cite the primary studies for any
specific result you lean on:

> Animal serum time-course data were obtained from the US EPA CPHEA
> PFAS pharmacokinetic compilation (Zurlinden et al. 2025,
> *Toxicol Appl Pharmacol* 499:117336;
> https://github.com/USEPA/CPHEA-Animal-PFAS-PK), which digitised and
> transcribed them from the primary studies listed below.

Nothing in `data/` is synthetic, and nothing in it originates with this
repository. Every row is a serum concentration measured in a published
animal study, digitised by the US EPA, and re-exported here in a flat
format so the lessons run without a database.

The chain is three links long, and you can verify each one independently:

```
published paper  ->  EPA digitisation (PFAS.db)  ->  data/*.csv
   (9 studies)        USEPA/CPHEA-Animal-PFAS-PK      (this repo)
```

## Link 1 — the original studies

The `study` column in every CSV is an **EPA HERO reference ID**. HERO
(Health and Environmental Research Online) is EPA's public literature
database, and any ID resolves at:

```
https://hero.epa.gov/hero/index.cfm/reference/details/reference_id/<ID>
```

All nine, verified against HERO:

| HERO ID | Citation |
|---|---|
| [3749227](https://hero.epa.gov/hero/index.cfm/reference/details/reference_id/3749227) | Butenhoff JL, Kennedy GL, Hinderliter PM, Lieder PH, Jung R, Hansen KJ, Gorman GS, Noker PE, Thomford PJ (2004). Pharmacokinetics of perfluorooctanoate in cynomolgus monkeys. *Toxicological Sciences* 82(2):394–406. |
| [1289832](https://hero.epa.gov/hero/index.cfm/reference/details/reference_id/1289832) | Chang SC, Noker PE, Gorman GS, Gibson SJ, Hart JA, Ehresman DJ, Butenhoff JL (2012). Comparative pharmacokinetics of perfluorooctanesulfonate (PFOS) in rats, mice, and monkeys. *Reproductive Toxicology* 33(4):428–440. |
| [6302380](https://hero.epa.gov/hero/index.cfm/reference/details/reference_id/6302380) | Kemper R (2003). Perfluorooctanoic acid: toxicokinetics in the rat. DuPont Haskell Laboratory, Report DuPont 7473; US EPA public docket AR-226-1499. *(a technical report, not a journal article)* |
| [5916078](https://hero.epa.gov/hero/index.cfm/reference/details/reference_id/5916078) | Dzierlenga AL, Robinson VG, Waidyanatha S, DeVito MJ, Eifrid MA, Gibbs ST, Granville CA, Blystone CR (2019). Toxicokinetics of PFHxA, PFOA and PFDA in male and female Hsd:Sprague Dawley SD rats following intravenous or gavage administration. *Xenobiotica* 50(6):722–732. |
| [3749289](https://hero.epa.gov/hero/index.cfm/reference/details/reference_id/3749289) | Kim SJ, Heo SH, Lee DS, Hwang IG, Lee YB, Cho HY (2016). Gender differences in pharmacokinetics and tissue distribution of 3 perfluoroalkyl and polyfluoroalkyl substances in rats. *Food and Chemical Toxicology* 97:243–255. |
| [2990271](https://hero.epa.gov/hero/index.cfm/reference/details/reference_id/2990271) | Kudo N, Katakura M, Sato Y, Kawashima Y (2002). Sex hormone-regulated renal transport of perfluorooctanoic acid. *Chemico-Biological Interactions* 139(3):301–316. |
| [3858670](https://hero.epa.gov/hero/index.cfm/reference/details/reference_id/3858670) | Ohmori K, Kudo N, Katayama K, Kawashima Y (2003). Comparison of the toxicokinetics between perfluorocarboxylic acids with different carbon chain length. *Toxicology* 184(2–3):135–140. |
| [3859701](https://hero.epa.gov/hero/index.cfm/reference/details/reference_id/3859701) | Iwabuchi K, Senzaki N, Mazawa D, Sato I, Hara M, Ueda F, Liu W, Tsuda S (2017). Tissue toxicokinetics of perfluoro compounds with single and chronic low doses in male rats. *Journal of Toxicological Sciences* 42(3):301–317. |
| [5387170](https://hero.epa.gov/hero/index.cfm/reference/details/reference_id/5387170) | Huang MC, Dzierlenga AL, Robinson VG, Waidyanatha S, DeVito MJ, Eifrid MA, Granville CA, Gibbs ST, Blystone CR (2019). Toxicokinetics of PFBS, PFHxS and PFOS in male and female Hsd:Sprague Dawley SD rats after intravenous and gavage administration. *Toxicology Reports* 6:645–655. |

Worth noticing: **Kudo 2002 is titled "Sex hormone-regulated renal
transport of perfluorooctanoic acid."** The mechanism lesson 10 appeals
to for the 28-fold sex difference is the subject of one of the papers
the data come from — the explanation and the observation are not
independent of each other, which is reassuring rather than circular,
but worth knowing.

## Link 2 — the EPA digitisation

**Repository:** https://github.com/USEPA/CPHEA-Animal-PFAS-PK
**Paper:** Zurlinden TJ, Dzierlenga MW, Kapraun DF, Ring C, Bernstein AS,
Schlosser PM, Morozov V (2025). Estimation of species- and sex-specific
PFAS pharmacokinetics in mice, rats, and non-human primates using a
Bayesian hierarchical methodology. *Toxicology and Applied Pharmacology*
499:117336. [doi:10.1016/j.taap.2025.117336](https://doi.org/10.1016/j.taap.2025.117336)
· open access at [PMC12172007](https://pmc.ncbi.nlm.nih.gov/articles/PMC12172007/)

Their own methods confirm the account below: "Graphical extraction of
concentration vs. time data was conducted using WebPlot Digitizer", and
their data availability statement points at the repository.
**Licence:** MIT, © U.S. Federal Government

**EPA ships the extracted data as plain CSVs**, one per study, in
[`extracted_data/`](https://github.com/USEPA/CPHEA-Animal-PFAS-PK/tree/main/extracted_data),
named `Author_HEROID.csv`. These are the direct upstream of everything
in this folder, and you do not need to build anything to read them:

| our file | upstream |
|---|---|
| `PFOA_Male_primate.csv` | [`Butenhoff_3749227.csv`](https://github.com/USEPA/CPHEA-Animal-PFAS-PK/blob/main/extracted_data/Butenhoff_3749227.csv) |
| `PFOS_Male_primate.csv` | [`Chang_1289832.csv`](https://github.com/USEPA/CPHEA-Animal-PFAS-PK/blob/main/extracted_data/Chang_1289832.csv) |
| `PFOA_Male_rat.csv` | `Kudo_2990271`, `Kim_3749289`, `Ohmori_3858670`, `Iwabuchi_3859701`, `Dzierlenga_5916078`, `Kemper_6302380` |
| `PFOA_Female_rat.csv` | `Kudo_2990271`, `Kim_3749289`, `Ohmori_3858670`, `Dzierlenga_5916078`, `Kemper_6302380` |
| `PFOS_Male_rat.csv` | `Chang_1289832`, `Kim_3749289`, `Iwabuchi_3859701`, `Huang_5387170` |

Column definitions are in
[`extracted_data/README.txt`](https://github.com/USEPA/CPHEA-Animal-PFAS-PK/blob/main/extracted_data/README.txt).
The SQLite database (`PFAS.db`) the analysis notebooks use is built
from these CSVs by `auxiliary_notebooks/create_db.ipynb`; it is not
itself checked in.

### Each record says where it came from

EPA's files carry a `source` column naming the table, appendix or
figure each value was taken from — so the digitisation question is
answerable per record rather than per study:

| our file | from tables/appendices | digitised from figures |
|---|---|---|
| `PFOA_Male_primate.csv` | **43 (100%)** — Butenhoff Table 5 | 0 |
| `PFOA_Male_rat.csv` | 808 (94%) | 52 (6%) |
| `PFOA_Female_rat.csv` | 348 (92%) | 29 (8%) |
| `PFOS_Male_rat.csv` | 108 (44%) | 138 (56%) |
| `PFOS_Male_primate.csv` | 0 | **48 (100%)** — Chang figures |

This matters more than it looks. The monkey PFOA curve that lessons 2,
3, 4, 6, 7, 8 and 9 are built on is **transcribed from Butenhoff's
Table 5**, not read off a plot — so the dataset carrying most of the
teaching is the most reliable one in the set. The PFOS primate data,
by contrast, is entirely digitised from figures.

Units differ per study in EPA's files (`ug/ml`, `ng/ml`, `ug/L`, and
`nmol/ml` for Kudo and Ohmori, which needs a molecular weight to
convert). Our export normalises everything to **mg/L**.

## Link 3 — this repository

`data/*.csv` was exported from `PFAS.db` by selecting five
chemical/sex/species slices and flattening to one row per measurement.
No values were altered, filtered or imputed. What changed:

- EPA's internal bookkeeping columns were dropped
- `dataset` was added, as `study + dose + route`, identifying one
  experiment — the unit the lessons fit
- units left as the database stores them: **days, mg/L, mg/kg**

| file | rows | HERO IDs behind it |
|---|---|---|
| `PFOA_Male_primate.csv` | 43 | 3749227 |
| `PFOS_Male_primate.csv` | 48 | 1289832 |
| `PFOA_Male_rat.csv` | 860 | 2990271, 3749289, 3858670, 3859701, 5916078, 6302380 |
| `PFOA_Female_rat.csv` | 377 | 2990271, 3749289, 3858670, 5916078, 6302380 |
| `PFOS_Male_rat.csv` | 246 | 1289832, 3749289, 3859701, 5387170 |
| `PFOA_Female_primate.csv` | 45 | 3749227 |

## What this export leaves out

EPA's `extracted_data/` holds **5247 serum/plasma rows**; these files
carry **1619**, about 31%. `export_from_epa.py` regenerates them and is
the definitive statement of the filter, but in words:

| left out | rows | why |
|---|---|---|
| six of eight chemicals (PFHxA, PFHxS, PFNA, PFDA, PFBA, PFBS) | ~2300 | scope: the lessons teach with PFOA and PFOS |
| all mouse data | ~800 | scope |
| PFOS female rats | 244 | scope |
| female primates for PFOS, PFHxS, PFBS, PFBA, PFHxA | ~180 | scope |
| all tissue matrices (liver, kidney, brain…) | 2715 | the lessons model serum only |
| `matrix == "blood"` in Iwabuchi 3859701 | 13 per chemical | whole blood is **not** serum — PFAS sit lower in red cells, so pooling them would put two different measurements on one curve |
| rows with `conc_mean == -1` | 169 | below the limit of detection, or not reported |

**That last row is the one with scientific consequences.** Censored
values are always the LATE, low points — exactly the ones carrying the
terminal slope. Dropping them truncates each curve early and biases
half-lives **short**. Proper handling treats them as censored rather
than missing; the lessons use ordinary least squares, which cannot
express "below 0.05", so they are dropped. Lesson 03 question 4 is
about this exact bias. Per-file counts are printed by the export
script.

Everything omitted is available in EPA's repository; nothing was
altered, and the 1619 rows kept match EPA's values exactly.

## Checking this yourself

**Verified: all 1574 values are identical to EPA's.** Reproduce it:

```bash
git clone --depth 1 https://github.com/USEPA/CPHEA-Animal-PFAS-PK /tmp/epa
python data/verify_against_epa.py /tmp/epa/extracted_data
```

```
1574 values compared, 0 unmatched
largest disagreement anywhere: 1.421e-14 mg/L
```

That residual is floating-point noise from the unit conversions, not a
data difference. The script also prints the table-versus-figure split
above, so it re-derives the provenance claims rather than trusting this
file.

Three further checks, independent of each other:

1. **Resolve a HERO ID** at the URL above and compare the author and
   year against the `author` column in the CSV.
2. **Compare against the paper itself.** Butenhoff 2004 is the easiest:
   three cynomolgus monkeys, 10 mg/kg IV, followed to day 123, reported
   in that paper's Table 5. Check it against `PFOA_Male_primate.csv`
   directly.
3. **Check a derived number.** `../test_lessons.py` re-derives every
   value quoted in the lessons straight from these CSVs.

## One caveat worth stating plainly

Link 3 is now verified exactly, so the uncertainty lives entirely in
link 2: reading values off a published figure introduces error that no
downstream analysis can recover.

The table above says where that applies. Most of the data is
transcribed rather than digitised, and the dataset the lessons lean on
hardest is 100% transcribed — but `PFOS_Male_primate.csv` is wholly
digitised, so treat its third decimal place as decorative.

If a conclusion in these lessons turned on a 5% difference you should
go to the original paper rather than trust the CSV. None of them do:
the effects they rest on are 2-fold, 11-fold and 28-fold.
