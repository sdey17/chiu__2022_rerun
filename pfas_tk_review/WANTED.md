# Papers still wanted

Everything previously on this list that has been supplied is **gone from it** —
11 full texts arrived between 2026-10-01 and 2026-10-02 and are now in `papers/`,
extracted into `db/primary_2026/`, and folded into the report. What each one
settled is recorded in `report/REPORT.md` §8 and in the git history, not here.

**Received and removed:** Argoul/Gayrard 2026 · Thompson 2010 (+ 5 supplementary
files + corrigendum) · Kudo 2002 · Kudo 2001 · Lou 2009 · Han 2012 · Yang 2010 ·
Tatum-Gibbs 2011 · Sundström 2012 · Cheng 2005 · Huang 2021 corrigendum.
Also removed: **Weaver 2010**, which was listed in error and had been on disk all
along, and **Cheng 2006**, which needed no full text — its own abstract
contradicts itself and Cheng 2005 settles the direction.

Identifiers below are copied from the retrieval logs in `papers/SOURCES_*.md`,
not written from memory. Every item here was attempted and failed.

**Format:** PDF, plain text or HTML are equally good; supplementary tables matter
as much as the article. Drop files anywhere in the repo — `papers/` is the
natural home.

---

## Blocks a conclusion

### 1. Han et al. 2003 — a 100-fold conflict in free fraction
*Binding of perfluorooctanoic acid to rat and human plasma proteins.*
Chem Res Toxicol 16(6):775–781. **PMID 12807361**, doi:10.1021/tx034005w

§6.2 records that this paper's ">90% bound" (f_unbound < 0.10) conflicts **~100×**
with Fischer 2024's measured 0.00061, and that older PBPK models parameterised on
it carry a free fraction two orders of magnitude too high. The mouse value now in
hand (0.0087, Argoul 2026) sits *between* the two, so it rescues neither — which
makes the primary methods the only way to adjudicate.

*Its companion Han 2012 has arrived and was the more important half.*

### 2. Yang et al. 2009 — the rat Oatp1a1 kinetics
*Toxicol Lett* 190(2):163–171. **PMID 19616083**,
doi:10.1016/j.toxlet.2009.07.011

The rat half of §4.3's saturation-margin calculation. Yang **2010** (the human
transporters) has arrived; this is its predecessor, and its Oatp1a1–PFOA
Km of 162.2 µM and the C6–C10 Ki values are currently held only second-hand,
quoted from Weaver 2010's Discussion.

### 3. A measured human KT — *no paper known to supply it*

Not a retrieval request but the single most valuable missing number, recorded
here so it is not lost. §4.3 now rests on a judgement between two parameter
families that disagree by **483–2,336×**: in vitro transporter Km values say
saturation is unreachable at human exposures, while the KT constants published
PBPK models run on imply three of four human populations sit at or above
half-saturation. Every KT in Han 2012 Table 7 is *fitted to plasma curves*, not
measured. If a study measuring human renal reabsorptive KT directly exists, it
settles the section outright.

---

## Would corroborate something resting on one source

| paper | identifier | why |
|---|---|---|
| **Kemper 2003**, *PFOA: toxicokinetics in the rat*, DuPont Haskell | unpublished; EPA docket | the rat PFOA dose series behind §4.2's female dose-dependence — the one place in the whole dataset where dose genuinely moves half-life (female t½ 3.2 → 16.2 h across 0.1 → 25 mg/kg). Grey literature, read only through ATSDR's tabulation, yet it underpins Wambaugh 2013 and Worley & Fisher 2015 |
| **Ohmori et al. 2003**, PFCA chain-length TK | **PMID 12499116** | one of two studies giving the rat PFOA sex ratio ≈70×; the other (Kudo 2002) is now in hand, so this would make it two independent primaries rather than one |
| **Buist & Klaassen 2004**, rat vs mouse Oat1-3 expression | **PMID 15155553**, doi:10.1124/dmd.32.6.620 | *downgraded.* Its load-bearing claim — that Oat2 does not transport PFOA — is now settled directly from Weaver 2010 Fig. 9A. The abstract suffices for the expression comparison. Useful, not decisive |
| **Cheng & Klaassen 2009**, mouse renal transporter regulation | **PMID 19679677**, doi:10.1124/dmd.109.027177 | *largely superseded.* Cheng 2005 answered the question this was wanted for. Would only add the ontogeny/hormone detail |

---

## Would fill a hole in the coverage grid

85% of the 1,716 chemical × species × parameter cells have no data. These are the
highest-yield fills.

| paper | identifier | fills |
|---|---|---|
| **Hanhijärvi et al. 1988**, beagle dog | book chapter, doi:10.1007/978-3-642-71248-7_96 | **the entire dog column** — dog has 2 of 44 cells. Essentially the only primary dog PFAS study; not in PubMed; two regulatory tabulations of it disagree. Re-attempted 2026-10-02 and confirmed not online: HERO 5412773 lists it, but it is a 1988 Springer chapter with no digital full text. **Likely needs a library scan.** Han 2012 Table 4's compiled values (CLR 50.8 F / 43 M mL/d/kg, 52%/59% reabsorbed) are the current substitute |
| **Kerstner-Wood 2003**, SRI contract report | no DOI/PMID | the main source for neat human plasma f_unbound of PFOS/PFOA/PFHxS — and therefore relevant to item 1 above |
| **Louisse et al. 2024**, human OAT1/2/3 Km table | doi:10.1016/j.tox.2024.153961 | the largest remaining numeric transporter gap. (Louisse **2023**, the OAT4 paper, is already on disk) |
| **Shi et al. 2016**, Cl-PFESA human kinetics | **PMID 26866980**, doi:10.1021/acs.est.5b05849 | the longest human PFAS half-life on record (15.3 y); 6:2 Cl-PFESA has 2 of 44 cells |
| **Yi et al. 2022**, 6:2 Cl-PFESA rat TK | **PMID 33947185** | the animal side of the same compound |
| **Maso et al. 2021**, PFOA–HSA binding mode | **PMID 33550662**, doi:10.1002/pro.4036 | the crystallographic site assignment contested in §6.3 |
| **Jia et al. 2022**, PFAS liver/blood partition | **PMID 35436088**, doi:10.1021/acs.est.1c08493 | tissue partition coefficients; ACS 403 |
| **Delaere et al. 2025**, firefighter PFAS reduction programme | Environ Int 2025;202:109609 | a second controlled-removal study to set against Gasiorowski (§5.1a) |
| **Dzierlenga et al. 2025**, `SUPPL_PFAS_PK_summary.csv` | doi:10.1016/j.taap.2025.117336 | the one supplementary table not recovered from the EPA repo |

---

## Not worth your time

- **Griffith & Long 1980** — the obvious place to expect dog data. Checked: rat
  and mouse acute toxicity only, no TK.
- **ATSDR 2021 for dog values** — contains "dog"/"beagle"/"canine" only inside
  its literature-search Boolean strings.
- **cC6O4** — already captured via Fustinoni 2023.
- **Katakura 2007** — the only study testing Npt2 and Mrp2 for PFOA. Not indexed
  in PubMed or Europe PMC; *J Health Sci* has no located DOI. Known second-hand
  through OEHHA Table A6.3 and Weaver 2010's Discussion.
- Anything already in `papers/` — 172 full-text extractions, including all 11
  received above.

---

## If you can only chase one

**Hanhijärvi 1988.** Everything else on this list changes a number or
corroborates a claim. That one is a whole species: the dog is the only mammal on
the reabsorption axis with just two data cells, it sits in the interesting middle
of the axis (52–59% reabsorbed, between the macaque and the female rat), and two
agencies tabulate it inconsistently with no way to adjudicate. It is also the
only item here that probably cannot be solved online — a university library's
interlibrary loan is the realistic route.
