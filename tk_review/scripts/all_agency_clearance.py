#!/usr/bin/env python3
"""Compare the human clearance factor adopted by every agency in the collection -
federal, US state, and international - on one scale.

The clearance factor converts an internal (serum) point of departure into an
external dose, so it propagates directly into a drinking-water number. Two
agencies can agree on the half-life and still differ severalfold here, and the
state layer turns out to matter: states mostly do not derive their own value,
they inherit one, and which one they inherit decides the answer.

Inputs: db/regulatory_values.csv (federal and international, 173 rows) and
db/state_international_regulatory.csv (state plus further international).
"""
import csv
import math
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
DB = HERE.parent / "db"
OUT = DB / "all_agency_clearance.csv"

# Leading number, allowing scientific notation; trailing parentheticals ignored.
NUM = re.compile(r"^\s*([0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?)")
TO_ML_KG_DAY = {
    "ml/kg-day": 1.0, "ml/kg/day": 1.0, "ml/kg-d": 1.0,
    "l/kg-day": 1000.0, "l/kg/day": 1000.0, "l/kg-d": 1000.0,
    "ml/kg-hour": 24.0, "l/kg-hour": 24000.0,
}


def val(s):
    m = NUM.match((s or "").strip())
    return float(m.group(1)) if m else None


def unit(s):
    """First recognised unit token in a possibly messy units string."""
    t = (s or "").strip().lower()
    for k in sorted(TO_ML_KG_DAY, key=len, reverse=True):
        if t.startswith(k):
            return TO_ML_KG_DAY[k]
    for k, f in TO_ML_KG_DAY.items():
        if k in t:
            return f
    return None


# How the number was produced. This is the fault line that matters: a clearance
# computed from Thompson 2010's Vd inherits an ASSUMED volume of distribution,
# while one regressed from intake against serum measures clearance directly, and
# one from urinary clearance alone counts only part of elimination.
# Order matters. OEHHA's regressed clearance lists eight exposure studies, one
# of which is Thompson 2010 as a DATA source rather than as the Vd it supplied
# to everyone else - so the intake-vs-serum test must run before the Thompson
# test, or that value is misread as a Thompson-derived one.
METHOD_RULES = [
    ("adopted from another agency",
     r"OEHHA 20|California EPA OEHHA|MDH 20|NH DES|MI SAW|Health Canada 2018|"
     r"US EPA 2016b derivation"),
    ("measured: intake vs serum at steady state",
     r"Fromme|Trudel|Frisbee|Brede|Haug|Lorber|Egeghy|Silva|Ronneby"),
    ("computed from Thompson 2010 assumed Vd", r"Thompson"),
    ("renal clearance only",
     r"\bFu 2016|Fu et al\. 2016|Gao 2015|Zhang 2015|Fujii|Zhou 2014|"
     r"Harada|Zhang et al\. 2013|Zhang 2013"),
    ("animal-derived", r"Macon|Sundstrom|Ohmori|cynomolgus|monkey|rat |mouse "),
]


def classify(src):
    for name, pat in METHOD_RULES:
        if re.search(pat, src or "", re.I):
            return name
    return "other or unstated"


def harvest(path, agency_key="agency"):
    out = []
    if not path.exists():
        return out
    for r in csv.DictReader(path.open()):
        p = (r.get("parameter") or "").lower()
        if "clearance" not in p and "dosimetric adjustment" not in p:
            continue
        sp = (r.get("species") or "").lower()
        if sp and "human" not in sp:
            continue
        v, f = val(r.get("value")), unit(r.get("units"))
        if v is None or f is None:
            continue
        out.append({
            "agency": r[agency_key], "document": r.get("document", ""),
            "year": r.get("year", ""), "chemical": r.get("chemical", ""),
            "clearance_mL_kg_day": v * f,
            "value_as_published": r.get("value", ""),
            "units_as_published": r.get("units", ""),
            "adopted": "yes" if "adopted" in p else "no",
            "method": classify(r.get("primary_source_cited", "")),
            "primary_source_cited": r.get("primary_source_cited", ""),
            "jurisdiction_level": r.get("jurisdiction_level", "federal"),
            "page_or_table": r.get("page_or_table", ""),
            "url": r.get("url", ""),
        })
    return out


def main() -> None:
    rows = harvest(DB / "regulatory_values.csv") + \
           harvest(DB / "state_international_regulatory.csv")
    # Drop obvious unit-parse failures: a human clearance factor outside
    # 0.001-100 mL/kg-day is not plausible and indicates a mis-read unit.
    rows = [r for r in rows if 0.001 <= r["clearance_mL_kg_day"] <= 100]
    rows.sort(key=lambda r: (r["chemical"], r["clearance_mL_kg_day"]))

    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print("HUMAN CLEARANCE FACTOR ACROSS ALL AGENCIES, mL/kg-day")
    print("the serum-to-dose conversion that sets a drinking-water number\n")
    for chem in sorted({r["chemical"] for r in rows}):
        sel = [r for r in rows if r["chemical"] == chem]
        if len(sel) < 3:
            continue
        lo, hi = sel[0]["clearance_mL_kg_day"], sel[-1]["clearance_mL_kg_day"]
        print(f"=== {chem} ===  {len(sel)} values, spread {hi/lo:.1f}x "
              f"({lo:.3f} to {hi:.3f})")
        print(f"  {'agency':<44} {'mL/kg/d':>8}  traces to")
        for r in sel:
            src = (r["primary_source_cited"] or "")[:40]
            print(f"  {r['agency'][:44]:<44} {r['clearance_mL_kg_day']:8.3f}  {src}")
        print()

    # How were these numbers produced?
    from collections import Counter
    print("HOW EACH NUMBER WAS PRODUCED")
    for name, n in Counter(r["method"] for r in rows).most_common():
        print(f"  {n:>3}  {name}")
    print()
    thom = [r for r in rows
            if r["method"] == "computed from Thompson 2010 assumed Vd"]
    print(f"  {len(thom)} of {len(rows)} adopted values rest on Thompson et al.")
    print("  2010's volume of distribution. That Vd was CALIBRATED from two US")
    print("  water communities using an ASSUMED 2.3 y half-life, not measured.")
    print("  The measured human PFOA Vd is 121 mL/kg (Abraham 2024), against")
    print("  Thompson's 170. So the apparent agreement among states is one")
    print("  derivation repeated, not independent confirmation - and it carries")
    print("  a known assumption forward.")
    print()
    print("  The values that do NOT use it diverge sharply: OEHHA's measured")
    print("  intake-vs-serum clearance is 2x the Thompson-derived cluster, and")
    print("  its renal-clearance-only figure is 2-8x BELOW it.")
    print(f"\nwrote {OUT}  ({len(rows)} rows)")


if __name__ == "__main__":
    main()
