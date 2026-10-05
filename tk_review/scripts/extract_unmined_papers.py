#!/usr/bin/env python3
"""Extract toxicokinetic values from full texts that were retrieved earlier in
this project but never read into any database.

A check of which papers/*.txt files are cited by any db/ extraction found 37
that are not. Most are regulatory documents already represented in summary form,
but four carry toxicokinetic values that exist nowhere else in the collection.
Those are transcribed here, each against the sentence or table it came from.
"""
import csv
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "db" / "unmined_extraction.csv"

ROWS = [
    # --- Wallis et al. 2023: the only human half-lives for these fluoroethers.
    # "These are the first and possibly only estimates of human elimination
    # half-lives of these fluoroethers." GenX Exposure Study, 44 participants,
    # two serum measurements ~177 days apart, 5 and 11 months after discharges
    # into the drinking-water source were controlled.
    dict(study="Wallis 2023", year="2023", chemical="Nafion byproduct 2",
         species="human", sex="mixed (64% F)", n="44", parameter="half-life",
         value="296", units="days", ci_low="176", ci_high="924",
         source_table="Abstract and Table 3",
         note="GenX Exposure Study, North Carolina; serum decay after source control"),
    dict(study="Wallis 2023", year="2023", chemical="PFO4DA",
         species="human", sex="mixed (64% F)", n="44", parameter="half-life",
         value="127", units="days", ci_low="86", ci_high="243",
         source_table="Abstract and Table 3",
         note="The Results text repeats Nafion byproduct 2's CI (176-924) for "
              "this compound; the abstract's 86-243 is taken as correct"),
    dict(study="Wallis 2023", year="2023", chemical="PFO5DoA",
         species="human", sex="mixed (64% F)", n="44", parameter="half-life",
         value="379", units="days", ci_low="199", ci_high="3870",
         source_table="Abstract and Table 3", note=""),
    dict(study="Wallis 2023", year="2023", chemical="Nafion byproduct 2",
         species="human", sex="mixed (64% F)", n="44",
         parameter="elimination coefficient", value="-0.00234",
         units="ng/mL/day", ci_low="", ci_high="", source_table="Table 3",
         note=""),
    dict(study="Wallis 2023", year="2023", chemical="PFO4DA", species="human",
         sex="mixed (64% F)", n="44", parameter="elimination coefficient",
         value="-0.00546", units="ng/mL/day", ci_low="", ci_high="",
         source_table="Table 3", note=""),
    dict(study="Wallis 2023", year="2023", chemical="PFO5DoA", species="human",
         sex="mixed (64% F)", n="44", parameter="elimination coefficient",
         value="-0.00183", units="ng/mL/day", ci_low="", ci_high="",
         source_table="Table 3", note=""),
    dict(study="ECHA (as cited by Wallis 2023)", year="2023",
         chemical="HFPO-DA (GenX)", species="human", sex="", n="",
         parameter="half-life", value="81", units="hours", ci_low="",
         ci_high="", source_table="Wallis 2023 Results, citing ECHA",
         note="Workers. Second-hand via Wallis; close to Abraham 2024's "
              "measured 2.86 d (68.6 h) in a labelled-dose volunteer"),

    # --- Marine medaka depuration, filling the 6:2 Cl-PFESA fish cell.
    dict(study="Cl-PFESA medaka depuration (abstract set)", year="",
         chemical="6:2 Cl-PFESA (F-53B)", species="marine medaka",
         sex="", n="", parameter="half-life", value="18.50", units="days",
         ci_low="", ci_high="", source_table="abstract",
         note="SD 1.67; 28-day exposure then 14-day depuration, lower "
              "concentration group"),
    dict(study="Cl-PFESA medaka depuration (abstract set)", year="",
         chemical="6:2 Cl-PFESA (F-53B)", species="marine medaka",
         sex="", n="", parameter="half-life", value="21.38", units="days",
         ci_low="", ci_high="", source_table="abstract",
         note="SD 0.31; higher concentration group"),

    # --- Excretion routes that no regulatory clearance accounting includes.
    dict(study="Mondal 2014", year="2014", chemical="PFOA", species="human",
         sex="Female", n="633", parameter="serum change per month of breastfeeding",
         value="-3", units="% per month", ci_low="-5", ci_high="-2",
         source_table="Abstract, Results",
         note="C8 Science Panel; breastfeeding as a maternal excretion route"),
    dict(study="Mondal 2014", year="2014", chemical="PFOS", species="human",
         sex="Female", n="633", parameter="serum change per month of breastfeeding",
         value="-3", units="% per month", ci_low="-3", ci_high="-2",
         source_table="Abstract, Results", note=""),
    dict(study="Mondal 2014", year="2014", chemical="PFNA", species="human",
         sex="Female", n="633", parameter="serum change per month of breastfeeding",
         value="-2", units="% per month", ci_low="-2", ci_high="-1",
         source_table="Abstract, Results", note=""),
    dict(study="Mondal 2014", year="2014", chemical="PFHxS", species="human",
         sex="Female", n="633", parameter="serum change per month of breastfeeding",
         value="-1", units="% per month", ci_low="-2", ci_high="0",
         source_table="Abstract, Results", note=""),
    dict(study="Mondal 2014", year="2014", chemical="PFOA", species="human",
         sex="infant", n="49", parameter="infant serum change per month breastfed",
         value="+6", units="% per month", ci_low="1", ci_high="10",
         source_table="Abstract", note="The mother's excretion is the infant's dose"),
    dict(study="Mondal 2014", year="2014", chemical="PFOS", species="human",
         sex="infant", n="49", parameter="infant serum change per month breastfed",
         value="+4", units="% per month", ci_low="1", ci_high="7",
         source_table="Abstract", note=""),
]

CITE = {
    "Wallis 2023": ("Wallis DJ et al. 2023, Environ Sci Technol; GenX Exposure "
                    "Study; papers/'Wallis 2023 half-lives fluoroethers Nafion "
                    "byproduct exposed community.txt'"),
    "ECHA (as cited by Wallis 2023)": "second-hand via Wallis 2023",
    "Cl-PFESA medaka depuration (abstract set)":
        "papers/'Cl-PFESA PFECHS OBS toxicokinetics rat zebrafish medaka "
        "minnow ABSTRACTS.txt' (abstracts only, primary not retrieved)",
    "Mondal 2014": ("Mondal D et al. 2014, Environ Health Perspect 122:187-192, "
                    "doi:10.1289/ehp.1306613"),
}


def main() -> None:
    fields = ["study", "year", "chemical", "species", "sex", "n", "parameter",
              "value", "units", "ci_low", "ci_high", "source_table",
              "citation", "note"]
    for r in ROWS:
        r["citation"] = CITE.get(r["study"], "")
    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(ROWS)
    print(f"wrote {OUT}  ({len(ROWS)} rows)\n")
    print("THE FIND THAT MATTERS")
    print("  Wallis 2023 reports the first and possibly only human elimination")
    print("  half-lives for three fluoroethers:")
    for r in ROWS[:3]:
        print(f"    {r['chemical']:<20} {r['value']:>4} d "
              f"({r['ci_low']}-{r['ci_high']})")
    print()
    print("  These sit between the short-chain carboxylates (PFHxA ~32 d,")
    print("  PFHpA ~62 d) and the long-chain PFAAs (PFOA and PFOS 800-1200 d).")
    print("  Ether oxygens shorten PFAS half-lives, which is the design")
    print("  rationale for the replacement chemistries - and these are the only")
    print("  human numbers testing it.")
    print()
    print("TWO EXCRETION ROUTES NO CLEARANCE ACCOUNTING INCLUDES")
    print("  Mondal 2014: each month of breastfeeding lowers maternal serum by")
    print("  3% (PFOA), 3% (PFOS), 2% (PFNA), 1% (PFHxS), and raises the")
    print("  infant's by 6% and 4%. Upson 2022 reviews menstrual blood loss as")
    print("  a second route, and notes it may explain the human sex difference")
    print("  that transporter biology does not.")


if __name__ == "__main__":
    main()
