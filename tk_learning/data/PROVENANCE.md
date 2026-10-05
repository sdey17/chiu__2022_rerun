# Where these data came from

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
**Paper:** "Estimation of species- and sex-specific PFAS pharmacokinetics
in mice, rats, and non-human primates using a Bayesian hierarchical
methodology", EPA ORD/CPHEA — [PMC12172007](https://pmc.ncbi.nlm.nih.gov/articles/PMC12172007/)
**Licence:** MIT, © U.S. Federal Government

EPA extracted the time-course values from the published figures and
tables into a SQLite database (`PFAS.db`), with chemical identity keyed
to DSSTox substance IDs (`auxiliary/pfas_master.csv`). Several of these
studies report data only as figures, so the EPA values are
**digitised from plots**, not transcribed from a table. That is normal
practice in this field and is the main reason to treat the third
decimal place as decorative.

To rebuild `PFAS.db` from their repository, follow their README; the
database is constructed by their build scripts rather than shipped.

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

## Checking this yourself

Any of these, independently of the others:

1. **Resolve a HERO ID** at the URL above and compare the author and
   year against the `author` column in the CSV.
2. **Compare against the paper.** Butenhoff 2004 is the easiest: three
   cynomolgus monkeys, 10 mg/kg IV, serum followed to day 123. Open the
   paper's figure and check it against `PFOA_Male_primate.csv`.
3. **Rebuild from EPA.** Clone their repository, build `PFAS.db`, and
   re-run the export. If a row disagrees with ours, theirs is right.
4. **Check a derived number.** `../test_lessons.py` re-derives every
   value quoted in the lessons straight from these CSVs.

## One caveat worth stating plainly

Two links in this chain were done by other people and one by this
repository, and the digitisation step is the one carrying the most
uncertainty — reading points off a published figure introduces error
that no downstream analysis can recover. If a conclusion in these
lessons turned on a 5% difference, you should go to the original paper
rather than trust the CSV. None of them do: the effects the lessons
rest on are 2-fold, 28-fold and 11-fold.
