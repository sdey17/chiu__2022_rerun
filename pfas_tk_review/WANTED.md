# Papers wanted, ranked by what each would change

**Status, 2026-10-02: eleven received.** Argoul/Gayrard 2026, Thompson 2010 (with
all five supplementary files and the appended corrigendum), Kudo 2002,
Lou 2009, the Huang 2021 corrigendum, **Han 2012, Yang 2010, Kudo 2001,
Tatum-Gibbs 2011, Sundström 2012 and Cheng 2005** are now in `papers/` and
`papers/supplementary/`, extracted into `db/primary_2026/`, and folded into the
report (§3.2a, §3.3, §3.4, §3.6, §5.1c, §5.3, §6.2, §8). That includes all three
items the "if you can only get three" section named. What each one settled is
recorded under its entry below.

**Still wanted, and the list is now short.** Tier 1 item 6 (**Han 2003**, the
100× free-fraction conflict); tier 2 **Kemper 2003** (unpublished DuPont report,
EPA docket); and from tier 3 **Hanhijärvi 1988**, which is the entire dog column.
Everything else in tier 1 and the top of tier 2 has arrived or been downgraded.

**Two items closed without the paper.** Tier 1 item 5 (Cheng & Klaassen) is
**resolved**: Cheng 2005's full text is here, and the Cheng 2006 abstract —
recovered in full from the publisher's metadata — turns out to contradict
*itself*, so no full text is needed to settle the direction (see §3.4).
**Hanhijärvi 1988** was attempted again and is not online; HERO 5412773 confirms
the citation but it is a 1988 book chapter with no digital full text. Han 2012
Table 4 now supplies dog CLR (50.8 female, 43 male mL/d/kg) and reabsorbed
fractions (52%/59%) compiled from it, which is the best available substitute.

**What the four newest ones settled.** Han 2012 is the source OEHHA's Table A6.4
adapts: the adaptation altered two values (human 99.94→99.8, male rat
93.7→93.2), the fu = 0.02 assumption turns out to be Han's rather than OEHHA's,
and Han's own text makes a point this review had missed — humans reabsorb *less*
PFOA in absolute terms than rodents, so the axis is two factors (filtration and
escape fraction), splitting 32%/68%. Yang 2010 showed that **OATP1A2, the human
orthologue of rat Oatp1a1, does not transport PFOA at all** — human reabsorption
runs through OAT4 and URAT1 — and that its URAT1 Km required zero extracellular
chloride, which probably reconciles it with Louisse 2023 rather than
contradicting it. Its Km values, set against Han's Table 7 PBPK constants,
exposed a 483–2,336× disagreement that flips §4.3's saturation conclusion
depending on which family is used. Kudo 2001 gave the rat chain-length series
(92→55→2.0→0.2% urinary across C7–C10) and, with Argoul, makes the renal-to-
faecal hand-off a two-species replicated finding. Tatum-Gibbs 2011 replicated
the entire sex/species pattern in PFNA with strains matched.

Every item here was attempted and failed — publisher 403, paywall, not indexed,
or behind a proof-of-work wall. Retrieval logs are in `papers/SOURCES_*.md`.

Identifiers are copied from those logs, not written from memory. Where a log did
not capture an identifier, the entry says so rather than guessing one.

**Format preference:** PDF is fine; a plain-text or HTML full text is just as
good. For the tier-1 items, the *supplementary tables* matter as much as the
article. Drop files anywhere in the repo — `papers/` is the natural home.

---

## Tier 1 — would change or directly test a conclusion in the report

### 1. Argoul / Gayrard 2026 — the missing mouse limb — **RECEIVED**
*Nonlinear mixed-effects modelling of IV and oral kinetics of 11 PFAS in female
mice.* Environ Res 2026. **PMID 42162713**, doi:10.1016/j.envres.2026.124802

11 PFAS × clearance, Vd, half-life and bioavailability, IV and oral, 119-day
sampling, NLME. **It was the single most valuable missing paper and it earned
that.** What it gave: a single-experiment test of §3.1 (clearance spans 5,254×,
Vss 7.7×); an independent recomputation of the §3.3 reabsorption axis putting
mouse PFOA at 95.9% against OEHHA's 95.2–97%; the first quantitative route split
for ten compounds (§5.3); mouse unbound fractions (§6.2); and the allometry test
in the new §3.6, where four of eight compounds scale within 1.25× but PFOA
misses by 3.4×. With Lou 2009 it retires the "one mouse study" caveat for PFOA.

*What it changes:* §3.2 records that the mouse side of the PFOA, PFHxS and PFNA
species ratios each rests on exactly **one** study (Lou 2009, Sundström 2012,
Tatum-Gibbs 2011) while the rat side is replicated four to six times. The
headline 31× mouse/rat PFOA ratio depends on a single mouse datum. This paper
would independently re-measure that limb across 11 compounds at once.

### 2. Thompson et al. 2010 — the most load-bearing citation nobody has read — **RECEIVED**
*Environ Int 36:390.* **PMID 20236705**, doi:10.1016/j.envint.2010.02.008

*What it changes:* §5.4 and §5.5 show that **nine of 42** adopted regulatory
clearance factors are computed from this paper's Vd, and EPA's own Table B-26
(§5.1b) shows ten human studies *assigning* it rather than measuring anything.
It is the hinge of the entire regulatory layer, and this project has only ever
seen it second-hand.

Both questions settled in §5.1c, with `scripts/thompson_vd_circularity.py`:
- **The transposition was Andersson 2025's alone.** Thompson gives PFOA = 170,
  PFOS = 230. Zhang 2013 has it right. This file was wrong to name Zhang.
- **The derivation is confirmed.** Supplementary Table S1 is headed "Input data
  for the calibration of the Vd parameter" with a column headed "calculated Vd",
  and Eq. 2c reproduces both published values to three figures from an assumed
  kP of 0.0008/day (2.37 y), taken from Bartell 2010 — measured in the same two
  communities. The half-life cancels exactly out of any clearance derived this
  way, but Vd stays proportional to it (168 mL/kg at 2.3 y, 277 at 3.8 y). The
  appended corrigendum is that error made and corrected by a factor of 0.6.
- **Bonus:** PFOS's 230 was never calibrated against data at all — it is
  170 × 1.35, scaled on a cited monkey model.

### 3. Kudo et al. 2002 — the mechanistic foundation of the female-rat story — **RECEIVED**
*Sex hormone-regulated renal transport of perfluorooctanoic acid.* Chem Biol
Interact 139(3):301–316. **PMID 11879818**, doi:10.1016/s0009-2797(02)00006-6

*What it gave:* the contradiction is resolved and EPA is wrong both times. The
primary text gives **oatp1 (Oatp1a1) 23×**, **OAT-K 2.5×** and **OAT2 0.13×** —
so EPA's "2.5-fold" is the OAT-K ratio misattributed, and 5–20-fold understates
it. Beyond that: Table 2 measures Vd in *both* sexes in one experiment (345.6 vs
211.2 mL/kg) against a 44.3× clearance difference, giving the clean 89%/11%
clearance/Vd split in §3.2a; Table 3's probenecid arm collapses male, castrated
male and female renal clearance onto a common value; and the paper's own
conclusion — OAT2/OAT3 secretion, with explicit agnosticism about oatp1 — turns
out to have been refuted by the later direct transport assays, which is now
recorded in §3.4 as a piece of intellectual history worth knowing.

### 4. Buist & Klaassen 2004 — **DOWNGRADED, no longer tier 1**
*Rat and mouse differences in gender-predominant expression of organic anion
transporter (Oat1-3; Slc22a6-8) mRNA.* Drug Metab Dispos 32(6):620–625.
**PMID 15155553**, doi:10.1124/dmd.32.6.620

*Why downgraded:* the load-bearing half of this was "Oat2 does not transport
PFOA", and that is now settled directly from **Weaver 2010 Fig. 9A**, whose full
PMC text has been on disk all along — no significant net Oat2-mediated uptake of
C7, C8, C9 or C10 in Oat2-expressing CHO cells. The abstract is enough for the
rat-versus-mouse expression claim itself. Still useful, no longer decisive.

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
| **Lou et al. 2009** — **RECEIVED** | **PMID 19005225**, doi:10.1093/toxsci/kfn234 | **It does report the sexes separately** — Table 2: female t½ 15.6 d, male 21.7 d, with Vd 0.135 vs 0.226 L/kg. The "15.6–21.7 d range" EPA quotes is the two sexes, not a dose range. With Kudo 2002 this gives §3.2a's headline: the Vd sex ratio is 1.67× in mouse and 1.64× in rat while the clearance sex ratio is 0.83× and 44.3× |
| **Sundström et al. 2012** — **RECEIVED** | **PMID 21856411**, doi:10.1016/j.reprotox.2011.07.004 | Still the sole mouse PFHxS source, but now read directly. Confirms the monkey Vdss four states use (287 male / 213 female mL/kg) at source, and adds three more datasets to §3.2a's decomposition, taking it from two to six. Also exposes a data-quality problem regulatory tabulations inherit silently: its Table 1 male rat IV parameters come from **a single animal** and the female β-phase in Table 2 was not estimable |
| **Tatum-Gibbs et al. 2011**, PFNA mouse/rat | doi:10.1016/j.tox.2011.01.003 | sole mouse PFNA source; our fitted 227 d sits 3.3× above its ceiling |
| **Kemper 2003**, DuPont Haskell unpublished | — | the PFOA rat dose series behind §4.2's female dose-dependence; unpublished report |
| **Huang et al. 2021 corrigendum** — **RECEIVED** | **PMID 33665134**, **PMC7902757**, doi:10.1016/j.toxrep.2021.02.001 | It is a units-label fix only: AUC and AUC/Dose in Tables 2–4 should read mM·hr, not μM·hr. Verified arithmetically (CL = 4.0 μmol/kg ÷ 7320 μmol/L·hr = 0.546 mL/hr/kg, matching the printed CL). No half-life, clearance or Vd changed, and we store no AUC, so every flagged row was always correct |
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

## If you can only get three — all three received, 2026-10-02

1. ~~**Argoul/Gayrard 2026**~~ — rebuilt the mouse limb, and gave the
   single-experiment version of §3.1 as well
2. ~~**Thompson et al. 2010**~~ — the assumption turned out to be a calculation,
   and its supplementary Table S1 is the proof
3. ~~**Kudo et al. 2002**~~ — settled the fold-value, and moved the mechanism
   argument from assertion to elimination

## What to get next, in order

1. **Kudo et al. 2001** (PMID 11311214) — tier 2. Now the most useful remaining
   item: Kudo 2002 covers PFOA only, and this is the chain-length series from the
   same laboratory, which would let §3.3's axis be tested against rat data the
   way Argoul let it be tested against mouse data.
2. **Yang 2009 / Yang 2010** — tier 1 item 7, unchanged. §4.3's saturation margin
   still depends on Km values read second-hand, and Louisse 2023 contradicts
   Yang 2010 on URAT1.
3. **Han 2012** (PMID 21985250) — tier 1 item 6's companion, and now the more
   important half of it: it is the compilation OEHHA's Table A6.4 is adapted
   from, so it is the primary source of the reabsorption axis itself. Argoul 2026
   corroborates the axis for the mouse, which makes the rat and human rows the
   remaining unverified ones.
4. **Sundström 2012** (PMID 21856411) and **Tatum-Gibbs 2011** — tier 2. PFHxS
   and PFNA are now the only compounds where the mouse limb still rests on one
   study each.
5. **Hanhijärvi 1988** — tier 3, but it is the entire dog column and two
   regulatory tabulations of it disagree.
