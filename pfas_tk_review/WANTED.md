# Papers wanted, ranked by what each would change

Every item here was attempted and failed — publisher 403, paywall, not indexed,
or behind a proof-of-work wall. Retrieval logs are in `papers/SOURCES_*.md`.

Identifiers are copied from those logs, not written from memory. Where a log did
not capture an identifier, the entry says so rather than guessing one.

**Format preference:** PDF is fine; a plain-text or HTML full text is just as
good. For the tier-1 items, the *supplementary tables* matter as much as the
article. Drop files anywhere in the repo — `papers/` is the natural home.

---

## Tier 1 — would change or directly test a conclusion in the report

### 1. Argoul / Gayrard 2026 — the missing mouse limb
*Nonlinear mixed-effects modelling of IV and oral kinetics of 11 PFAS in female
mice.* Environ Res 2026. **PMID 42162713**, doi:10.1016/j.envres.2026.124802

11 PFAS × clearance, Vd, half-life and bioavailability, IV and oral, 119-day
sampling, NLME. **This is the single most valuable missing paper.**

*What it changes:* §3.2 records that the mouse side of the PFOA, PFHxS and PFNA
species ratios each rests on exactly **one** study (Lou 2009, Sundström 2012,
Tatum-Gibbs 2011) while the rat side is replicated four to six times. The
headline 31× mouse/rat PFOA ratio depends on a single mouse datum. This paper
would independently re-measure that limb across 11 compounds at once.

### 2. Thompson et al. 2010 — the most load-bearing citation nobody has read
*Environ Int 36:390.* **PMID 20236705**, doi:10.1016/j.envint.2010.02.008

*What it changes:* §5.4 and §5.5 show that **nine of 42** adopted regulatory
clearance factors are computed from this paper's Vd, and EPA's own Table B-26
(§5.1b) shows ten human studies *assigning* it rather than measuring anything.
It is the hinge of the entire regulatory layer, and this project has only ever
seen it second-hand.

Two specific things to settle:
- **Zhang 2013 and Andersson 2025 give transposed values for it** — 170/230 vs
  230/170 mL/kg for PFOA/PFOS. One of them is wrong and it has propagated.
- Confirm the derivation: the account on disk says Vd was *calibrated* as
  `Dose·t½/(Css·ln2)` from two US water communities using an **assumed** 2.3-year
  half-life. If so, every clearance derived from it is circular.

### 3. Kudo et al. 2002 — the mechanistic foundation of the female-rat story
*Sex hormone-regulated renal transport of perfluorooctanoic acid.* Chem Biol
Interact 139(3):301–316. **PMID 11879818**, doi:10.1016/s0009-2797(02)00006-6

*What it changes:* §3.4 rests the rat mechanism on this paper's castration and
testosterone-replacement experiments, which we have **only from the abstract**.
It is also needed to resolve a flat contradiction: EPA's PFHxA review states the
rat male/female Oatp1a1 mRNA ratio is **2.5-fold**, EPA's PFOA assessment says
**5–20-fold**, and neither traces to anything in the abstract. The report
currently refuses to quote any single fold-value because of this.

### 4. Buist & Klaassen 2004 — the only direct rat-vs-mouse transporter comparison
*Rat and mouse differences in gender-predominant expression of organic anion
transporter (Oat1-3; Slc22a6-8) mRNA.* Drug Metab Dispos 32(6):620–625.
**PMID 15155553**, doi:10.1124/dmd.32.6.620

*What it changes:* §3.4 concludes the mouse mechanism is **unestablished**,
partly on this paper's finding that the one clear rat/mouse species difference
is in **Oat2 — which does not transport PFOA**. That conclusion deserves to rest
on the full text rather than an abstract.

Companions, same request: **Buist 2002** (PMID 11907168), **Buist & Klaassen
2003** (PMID 12695343, doi:10.1124/dmd.31.5.559).

### 5. Cheng & Klaassen, mouse Oatp1a1 regulation — resolve a contradiction
- Cheng X, Maher J, Chen C, Klaassen CD 2005, Drug Metab Dispos 33(7):1062–1073.
  **PMID 15843488**, doi:10.1124/dmd.105.003640
- Cheng X, Klaassen CD 2009, Drug Metab Dispos 37(11):2178–2185.
  **PMID 19679677**, doi:10.1124/dmd.109.027177
- Cheng X, Maher J, Lu H, Klaassen CD 2006, Mol Pharmacol 70(4):1291–1297.
  **PMID 16807376**, doi:10.1124/mol.106.025122 — *the one whose abstract calls
  renal Oatp1a1 "female-predominant"*

*What it changes:* §3.4 states mouse renal Oatp1a1 is androgen-induced, which is
why Oatp1a1 cannot by itself explain the rat/mouse difference. But Cheng 2006's
abstract **contradicts Cheng 2005 and its own conclusion** on the direction. The
report flags this as unresolved.

### 6. Han et al. 2003 — a 100-fold conflict in free fraction
*Binding of PFOA to rat and human plasma proteins.* Chem Res Toxicol
16(6):775–781. **PMID 12807361**, doi:10.1021/tx034005w

*What it changes:* §6.2 records that this paper's ">90% bound" (f_unbound < 0.10)
conflicts **~100×** with Fischer 2024's measured f_unbound of 0.00061, and that
older PBPK models parameterised on Han therefore carry a free fraction two orders
of magnitude too high. Worth confirming against the primary methods.

Companion: **Han 2012**, Chem Res Toxicol 25(1):35–46, **PMID 21985250**,
doi:10.1021/tx200363w — the compilation OEHHA's Table A6.4 is adapted from, and
therefore the ultimate source of the reabsorption axis in §3.3.

### 7. Yang et al. 2009 and 2010 — the transporter Km values
- Yang CH, Glover KP, Han X 2009, Toxicol Lett 190(2):163–171. **PMID 19616083**,
  doi:10.1016/j.toxlet.2009.07.011
- Yang CH, Glover KP, Han X 2010, Toxicol Sci 117(2):294–302. **PMID 20639259**,
  doi:10.1093/toxsci/kfq219

*What it changes:* §4.3's margin calculation — that transporter Km values sit
2,200–82,000× above human serum concentrations — depends on these. Also,
**Louisse 2023 found URAT1 transported nothing, flatly contradicting Yang 2010.**

---

## Tier 2 — would corroborate a claim that currently rests on one study

| paper | identifier | why |
|---|---|---|
| **Lou et al. 2009**, *Modeling single and repeated dose pharmacokinetics of PFOA in mice.* Toxicol Sci 107(2):331–341 | **PMID 19005225**, doi:10.1093/toxsci/kfn234 | the 31× mouse/rat PFOA ratio rests on this alone; **no source consulted reports male and female mouse PFOA half-lives separately**, so EPA's re-analysis pair (M 25.6 d, F 21.5 d) has never been checked against a published measurement |
| **Sundström et al. 2012**, mouse PFHxS. Reprod Toxicol 33(4):441–451 | **PMID 21856411**, doi:10.1016/j.reprotox.2011.07.004 | sole mouse source for PFHxS; also the monkey Vd four states use. (Cited as both 2011 and 2012 — same paper, 2011 e-pub / 2012 issue) |
| **Tatum-Gibbs et al. 2011**, PFNA mouse/rat | doi:10.1016/j.tox.2011.01.003 | sole mouse PFNA source; our fitted 227 d sits 3.3× above its ceiling |
| **Kemper 2003**, DuPont Haskell unpublished | — | the PFOA rat dose series behind §4.2's female dose-dependence; unpublished report |
| **Huang et al. 2021 corrigendum** | **PMID 33665134**, **PMC7902757**, doi:10.1016/j.toxrep.2021.02.001 | **which NTP numbers were corrected is unknown**; all affected rows are flagged |
| **Kudo et al. 2001**, *Comparison of the elimination between perfluorinated fatty acids with different carbon chain length in rats.* Chem Biol Interact 134(2):203–216 | **PMID 11311214**, doi:10.1016/s0009-2797(01)00155-7 | the 120-h urinary percentages by chain length and sex, the <5% faecal figures and the biliary comparison behind §5.3. Note: its dose-dependence is of *testosterone*, not of PFOA dose |
| **Ohmori et al. 2003**, PFCA chain-length TK | **PMID 12499116** | one of two studies giving rat PFOA sex ratio ≈70× |

---

## Tier 3 — would fill a hole in the coverage grid

| paper | identifier | fills |
|---|---|---|
| **Hanhijärvi et al. 1988**, beagle dog | book chapter, doi:10.1007/978-3-642-71248-7_96 | **the entire dog column** — essentially the only primary dog PFAS study; not in PubMed; two regulatory tabulations of it disagree |
| **Shi et al. 2016**, Cl-PFESA human kinetics | **PMID 26866980**, doi:10.1021/acs.est.5b05849 | longest human PFAS half-life on record (15.3 y); 6:2 Cl-PFESA has 2 of 44 cells |
| **Yi et al. 2022**, 6:2 Cl-PFESA rat TK | **PMID 33947185** | same compound, animal side |
| **Louisse et al. 2024**, human OAT1/2/3 Km table | doi:10.1016/j.tox.2024.153961 | largest remaining numeric transporter gap |
| **Kerstner-Wood 2003**, SRI contract report | no DOI/PMID | the main source for neat human plasma f_unbound of PFOS/PFOA/PFHxS |
| **Maso et al. 2021**, PFOA–HSA binding mode | **PMID 33550662**, doi:10.1002/pro.4036 | the crystallographic site assignment contested in §6.3 |
| **Jia et al. 2022**, PFAS liver/blood partition | **PMID 35436088**, doi:10.1021/acs.est.1c08493 | partition coefficients, ACS 403 |
| **Delaere et al. 2025**, firefighter PFAS reduction programme | Environ Int 2025;202:109609 | a second controlled-removal study to set against Gasiorowski (§5.1a) |
| **Dzierlenga et al. 2025**, `SUPPL_PFAS_PK_summary.csv` | doi:10.1016/j.taap.2025.117336 | the one supplementary table not recovered from the EPA repo |

---

## Not worth your time

- **Griffith & Long 1980** — on the original 81-paper list, and the obvious place
  to expect dog data. It is rat and mouse acute toxicity only, no TK. Checked.
- **ATSDR 2021 for dog values** — contains "dog"/"beagle"/"canine" only inside
  its literature-search Boolean strings.
- **cC6O4** — already captured via Fustinoni 2023.
- **Weaver et al. 2010**, rat renal OAT by chain length (PMID 19915082,
  doi:10.1093/toxsci/kfp275) — was listed in tier 2 in error. The full PMC text,
  including Tables 1–2 and the Yang 2009 Ki values quoted in its Discussion, is on
  disk at `papers/Weaver 2010 rat renal OAT PFCA chain length.txt`.
- Anything already in `papers/` — see that directory first; it holds ~75 full
  texts including Chiu 2022, Abraham 2024, Fischer 2024/2025, Andersson 2025,
  Rosato 2024, Li 2022, Zhang 2013, the EPA and OEHHA dossiers, and the EPA
  CPHEA raw animal PK data.

---

## If you can only get three

1. **Argoul/Gayrard 2026** — rebuilds the mouse limb the species comparison rests on
2. **Thompson et al. 2010** — the assumption nine regulatory clearance factors inherit
3. **Kudo et al. 2002** — the experiment the whole female-rat mechanism rests on
