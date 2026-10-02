# State and national regulatory documents: toxicokinetic extraction

Companion to `db/state_docs_extraction.csv`. Every row in that CSV records both the
primary study cited and the regulatory document it was read from, plus an explicit
DERIVED / COMPUTED / ADOPTED tag.

## 1. NY DOH 2022 (emerging contaminant notification levels + PFHxS/PFHpA/PFNA/PFDA MCLs)

Source: `papers/NY DOH 2022 emerging contaminant notification levels PFAS.txt` (15,967 lines;
most of the file is DWQC meeting transcript with no TK content. All TK is in lines ~6630-7520.)

**Structure of NY's use of toxicokinetics.** NY uses TK in two completely separate ways:

1. *As a hazard-prioritization criterion* (Tables 2 and 3). Human half-life is one of four
   criteria used to sort 19 emerging PFAS into a prioritized 30 ppt notification level and a
   second, higher category. No dose-response arithmetic; half-life is used purely
   qualitatively ("multiple years" = prioritized, "approaching one year" = not).
2. *As a dosimetric bridge* in the four chemical-specific MCL derivations (PFHxS, PFHpA,
   PFNA, PFDA), where a single chemical-specific human clearance factor converts an animal
   point-of-departure serum concentration into a human equivalent dose.

**The three clearance values, and who derived them:**

| Chemical | Clearance (mL/kg/day) | POD serum (ng/mL) | HED (ng/kg/day) | Critical study | Derived by |
|---|---|---|---|---|---|
| PFHxS | 0.086 | 13,900 | 1,200 | Chang et al. 2018 (mouse) | NH DES 2019 - NY ADOPTED |
| PFOA (applied to PFHpA) | 0.092 | 4,980 | 460 | **Macon et al. 2011 (mouse)** | **NYS DOH 2018 - NY's own** |
| PFNA (applied to PFDA) | 0.098 | 6,800 | 665 | Das et al. 2015 (mouse) | MI SAW 2019 - NY ADOPTED |

**The Macon et al. 2011 point of interest.** NY's PFOA reference dose (1.5 ng/kg/day, derived
by NYS DOH in 2018 and re-presented in 2022 as the basis for the PFHpA MCL) rests on a
**mouse** developmental study: increased relative liver weight in the offspring of mice dosed
on gestational days 1-17. The measured serum level at the LOEL (4,980 ng/mL) is converted with
a *human* clearance of 0.092 mL/kg/day, then divided by UF 300 (10 sensitive humans x 3
interspecies x 3 LOEL-to-NOEL x 3 database). This is unusual on two counts: (a) a mouse rather
than rat or human critical study for PFOA, and (b) serum-concentration equivalence is assumed
across species (mouse serum level = human serum level of concern) with the interspecies
uncertainty factor reduced to 3 on that basis.

**What the document does NOT say.** The NY document never states a volume of distribution,
never states which human half-life was used, and never cites a primary source for any of the
three clearance values. The three values (0.086, 0.092, 0.098 mL/kg/day) are suspiciously close
together, which is what one expects if each was computed as ln2 x Vd / t-half with a common
assumed Vd of roughly 0.2 L/kg and chemical-specific human half-lives - but that inference
cannot be checked from this document. Anyone needing the Vd must go to NH DES 2019, MI SAW 2019
and NYS DOH 2018 respectively.

**Internal inconsistency.** The PFNA RfD narrative uses the Michigan SAW HED of 665 ng/kg/day
(developmental delays, 6,800 ng/mL NOAEL). But Table 7 (margins of protection) uses an
NJ DEP 2015 HED of 431 ng/kg/day for maternal relative liver weight from the same Das et al.
2015 study. Two agencies' dosimetric conversions of one study sit in the same document.

**Rejections and conflicts.**
- GenX: short human half-life (81 h, US EPA 2021a using Clark 2021 data) was explicitly NOT
  treated as grounds for de-prioritization, because the liver effect level (0.5 mg/kg/day) and
  RfD (3 ng/kg/day) were low. GenX received its own 10 ppt level.
- PFPeS: half-life 223-365 days, "approaching one year, rather than multiple years", was the
  stated reason for placing it in the higher (less stringent) category.
- PFDoA, 11Cl-PF3OUdS, 4:2 and 8:2 FTS: no TK data at all; assigned by structural read-across.

**Species comparison.** The only cross-species TK statement is in Table 3 footnote b: rat
half-lives of 2-13 hours for short-chain PFAS versus "weeks to months" for long-chain
(ATSDR 2021), used to place 6:2 FTS (rat 20-24 h, ECHA 2020) with the short-chain PFAS when
no human half-life existed. **There is no discussion anywhere in the NY document of
rat-versus-mouse differences, of sex differences, or of the female-rat phenomenon** - notable
given that every one of NY's four critical studies is a mouse study.

**Not captured in the CSV** (exposure factors, not TK): drinking water ingestion rates
0.035 L/kg/day (adults), 0.047 (lactating women), 0.143 (infants); relative source
contribution 0.5 (NY departs from the EPA default of 0.2, citing NJ DEP, NH DES and others).
