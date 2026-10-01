#!/usr/bin/env python3
"""Patch in the six PMIDs resolved by hand, then apply the category corrections
that keyword matching cannot make, and emit the final source catalogue.

Two corrections matter for a toxicokinetics review:
  * a paper whose only pharmacokinetics is of a NON-PFAS comparator is not a
    PFAS TK study (row 74 measures [14C]clofibrate PK, not PFOA PK);
  * a repeat-dose toxicity study that measured serum or liver PFAS concentration
    supplies an internal dose at a known external dose, which is exactly the
    exposure-versus-half-life pairing this review needs, even when the paper
    reports no half-life. These are flagged with supplies_internal_dose.
"""
import csv
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "db"
SRC = DB / "xlsx_source_list_resolved.csv"
OUT = DB / "source_catalogue.csv"

# row -> (pmid, doi), each title-verified against PubMed esummary.
MANUAL_PMID = {
    "55": ("19239717", "10.1186/1471-2199-10-16"),
    "59": ("18511431", "10.1093/toxsci/kfn099"),
    "22": ("29705512", "10.1016/j.ecoenv.2018.04.032"),
    "12": ("31809754", "10.1016/j.tox.2019.152339"),
    "81": ("6773404", "10.1080/15298668091425301"),
    "6":  ("32743632", "10.1039/d0ay01052a"),
}

# row -> (new_category, reason)
RECLASSIFY = {
    "74": ("mechanistic_hazard",
           "the pharmacokinetics reported are of [14C]clofibrate, not of PFOA"),
    "25": ("in_vitro_protein_binding",
           "measures cellular accumulation and lipid binding, a distribution parameter"),
    "46": ("in_vivo_tk",
           "dermal flux and permeability coefficient are absorption parameters"),
}

# Repeat-dose studies that measured internal PFAS concentration at a known
# administered dose. These supply the dose-to-serum pairing even with no half-life.
SUPPLIES_INTERNAL_DOSE = {
    "4", "7", "14", "19", "22", "26", "28", "37", "45", "50", "51",
    "53", "56", "57", "59", "61", "66", "67", "79", "80", "81",
}


def main() -> None:
    rows = list(csv.DictReader(SRC.open()))
    fields = list(rows[0].keys())
    for f in ("supplies_internal_dose", "reclassified_reason"):
        if f not in fields:
            fields.insert(fields.index("raw_citation"), f)

    n_patched = n_recat = 0
    for r in rows:
        row = r["row"]
        if row in MANUAL_PMID and not r["pmid"]:
            r["pmid"], r["doi"] = MANUAL_PMID[row]
            r["resolved_how"] = "manual_verified"
            r["title_match_ratio"] = "1.000"
            n_patched += 1
        r["reclassified_reason"] = ""
        if row in RECLASSIFY:
            new, why = RECLASSIFY[row]
            if r["category"] != new:
                r["category"], r["reclassified_reason"] = new, why
                n_recat += 1
        r["supplies_internal_dose"] = "yes" if row in SUPPLIES_INTERNAL_DOSE else "no"
        r["tk_parameter_possible"] = "yes" if (
            r["category"] in {"in_vivo_tk", "in_vitro_protein_binding",
                              "transporter_or_enzyme"}
            or r["supplies_internal_dose"] == "yes"
        ) else "no"

    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    ok = sum(1 for r in rows if r["pmid"])
    print(f"patched {n_patched} PMIDs, reclassified {n_recat} entries")
    print(f"{ok}/{len(rows)} carry a verified PMID -> {OUT}\n")

    cats, usable = {}, 0
    for r in rows:
        cats[r["category"]] = cats.get(r["category"], 0) + 1
        usable += r["tk_parameter_possible"] == "yes"
    print("final categories")
    for k, v in sorted(cats.items(), key=lambda kv: -kv[1]):
        print(f"  {k:28} {v:3}")
    print(f"\ncan contribute a TK parameter or an internal dose: {usable}/{len(rows)}")
    print(f"hazard/mechanism only, no TK parameter:            {len(rows) - usable}/{len(rows)}")


if __name__ == "__main__":
    main()
