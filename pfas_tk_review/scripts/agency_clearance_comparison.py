#!/usr/bin/env python3
"""Compare the human clearance factor each agency adopted, and show how much of
the disagreement comes from the half-life versus from the method.

The clearance factor is the number that converts an internal (serum) point of
departure into an external dose, so it propagates directly into a drinking-water
standard. Two agencies can agree on the half-life to the first decimal and still
differ severalfold here.
"""
import csv
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
DB = HERE.parent / "db"
SRC = DB / "regulatory_values.csv"
OUT = DB / "agency_clearance_comparison.csv"

# mL/kg-day is the common unit; L/kg-day values are multiplied by 1000.
TO_ML_KG_DAY = {"mL/kg-day": 1.0, "L/kg-day": 1000.0,
                "mL/kg/day": 1.0, "L/kg/day": 1000.0}


def num(s):
    try:
        return float(str(s).strip())
    except (TypeError, ValueError):
        return None


def main() -> None:
    rows = list(csv.DictReader(SRC.open()))
    recs = []
    for r in rows:
        if "clearance" not in r["parameter"].lower() or r["species"] != "human":
            continue
        v, f = num(r["value"]), TO_ML_KG_DAY.get(r["units"].strip())
        if v is None or f is None:
            continue
        recs.append({
            "chemical": r["chemical"], "agency": r["agency"],
            "document": r["document"], "year": r["year"],
            "parameter": r["parameter"],
            "clearance_mL_kg_day": v * f,
            "units_as_published": r["units"], "value_as_published": r["value"],
            "adopted": "yes" if "ADOPTED" in r["parameter"] else "no",
            "primary_source_cited": r["primary_source_cited"],
            "assumptions": r["assumptions"], "page_or_table": r["page_or_table"],
            "url": r["url"],
        })

    recs.sort(key=lambda x: (x["chemical"], x["clearance_mL_kg_day"]))
    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(recs[0].keys()))
        w.writeheader()
        w.writerows(recs)

    print("HUMAN CLEARANCE FACTOR, as adopted or reported by each agency")
    print("(this is the serum-to-dose conversion that sets the standard)\n")
    for chem in sorted({r["chemical"] for r in recs}):
        sel = [r for r in recs if r["chemical"] == chem]
        if len(sel) < 2:
            continue
        lo, hi = sel[0]["clearance_mL_kg_day"], sel[-1]["clearance_mL_kg_day"]
        print(f"=== {chem} === spread {hi/lo:.1f}x  ({lo:.3f} to {hi:.3f} mL/kg-day)")
        print(f"  {'agency':<34} {'mL/kg-day':>10} {'adopted':>8}  basis")
        for r in sel:
            basis = (r["primary_source_cited"] or r["assumptions"] or "")[:46]
            print(f"  {r['agency'][:34]:<34} {r['clearance_mL_kg_day']:10.3f} "
                  f"{r['adopted']:>8}  {basis}")
        print()

    print(f"wrote {OUT}  ({len(recs)} rows)")

    # The decomposition that matters: EPA computes CL from Vd and half-life,
    # OEHHA measures it directly. Show what each term contributes.
    print("\nWHY EPA AND OEHHA DIFFER, for PFOA")
    epa_vd, epa_t = 170.0, 2.7          # mL/kg, years  (EPA Table 4-6)
    epa_cl = epa_vd * math.log(2) / (epa_t * 365.25)
    oehha_cl = 0.28                      # mL/kg-day, regressed intake vs serum
    print(f"  EPA:   Vd {epa_vd:.0f} mL/kg, t1/2 {epa_t} y  ->  "
          f"CL = Vd*ln2/t1/2 = {epa_cl:.3f} mL/kg-day")
    print(f"  OEHHA: CL measured directly from intake-vs-serum regression "
          f"= {oehha_cl:.3f} mL/kg-day")
    print(f"  ratio OEHHA/EPA = {oehha_cl/epa_cl:.2f}x")
    implied_vd = oehha_cl * epa_t * 365.25 / math.log(2)
    print(f"  For EPA's formula to reproduce OEHHA's clearance at the SAME "
          f"2.7 y half-life,\n  Vd would have to be {implied_vd:.0f} mL/kg, "
          f"not {epa_vd:.0f} - a {implied_vd/epa_vd:.1f}x change in Vd alone.")
    print("  The two agencies cite the same half-life studies. The disagreement "
          "is entirely\n  in Vd and in whether clearance is computed or measured.")

    # Three independent routes to a human PFOA Vd, for comparison.
    print("\nWHAT Vd DOES THE EVIDENCE ACTUALLY SUPPORT? (human PFOA)")
    routes = [
        ("Thompson 2010, assumed - used by EPA 2024 and Zhang 2013", 170),
        ("implied by OEHHA's measured clearance at EPA's 2.7 y half-life",
         round(implied_vd)),
        ("Chiu 2022, fitted by Bayesian hierarchical model to serum decay", 430),
        ("Andersson 2025, measured by mass balance", 74),
    ]
    for label, v in routes:
        print(f"  {v:>4} mL/kg   {label}")
    print("  The two routes that ESTIMATE Vd from human data rather than assuming it")
    print(f"  ({round(implied_vd)} and 430 mL/kg) agree within "
          f"{abs(430-implied_vd)/implied_vd*100:.0f}%, and both sit ~2.4x above the "
          "assumed value.")


if __name__ == "__main__":
    main()
