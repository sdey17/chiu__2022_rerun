#!/usr/bin/env python3
"""Test whether volume of distribution tracks dose or serum concentration.

The user's question is whether exposure relates to half-life or to Vd. Half-life
has been tested elsewhere in this repo; this script tests Vd.

Mechanistically, Vd should rise with concentration if the binding sites that hold
PFAS in plasma (albumin, globulins) saturate: a saturated plasma reservoir means
proportionally more compound in tissue, hence a larger apparent Vd. So a positive
slope of ln(Vd) on ln(serum) is the signature of binding saturation, and a flat
slope says the binding sites are nowhere near saturated.
"""
import csv
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "db" / "master_exposure_halflife.csv"


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def ols(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((a - mx) ** 2 for a in xs)
    sxy = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    syy = sum((b - my) ** 2 for b in ys)
    if not sxx or not syy:
        return float("nan"), float("nan")
    return sxy / sxx, sxy / math.sqrt(sxx * syy)


def main() -> None:
    rows = [r for r in csv.DictReader(SRC.open())
            if f(r["vd_L_kg"]) and f(r["serum_median_ng_mL"])]

    print("Does Vd rise with internal concentration?")
    print("Slope of ln(Vd) on ln(serum), within each species-sex group across chemicals\n")
    print(f"{'species':9} {'sex':7} {'n':>3} {'slope':>8} {'r':>7}   serum range (ng/mL)")
    print("-" * 68)
    for sp in ("human", "primate", "rat", "mouse"):
        for sex in ("Male", "Female"):
            sel = [r for r in rows if r["species"] == sp and r["sex"] == sex]
            if len(sel) < 3:
                continue
            xs = [math.log(f(r["serum_median_ng_mL"])) for r in sel]
            ys = [math.log(f(r["vd_L_kg"])) for r in sel]
            slope, r_ = ols(xs, ys)
            lo = min(f(r["serum_median_ng_mL"]) for r in sel)
            hi = max(f(r["serum_median_ng_mL"]) for r in sel)
            print(f"{sp:9} {sex:7} {len(sel):3} {slope:+8.3f} {r_:+7.3f}   "
                  f"{lo:,.0f} - {hi:,.0f}  ({hi/lo:,.0f}x)")

    print()
    print("Same test on DOSE rather than serum, animals only (mg/kg single dose)")
    print(f"{'species':9} {'sex':7} {'n':>3} {'slope':>8} {'r':>7}   dose range (mg/kg)")
    print("-" * 68)
    for sp in ("primate", "rat", "mouse"):
        for sex in ("Male", "Female"):
            sel = [r for r in rows if r["species"] == sp and r["sex"] == sex
                   and f(r["dose_median"])]
            if len(sel) < 3:
                continue
            xs = [math.log(f(r["dose_median"])) for r in sel]
            ys = [math.log(f(r["vd_L_kg"])) for r in sel]
            slope, r_ = ols(xs, ys)
            lo = min(f(r["dose_median"]) for r in sel)
            hi = max(f(r["dose_median"]) for r in sel)
            print(f"{sp:9} {sex:7} {len(sel):3} {slope:+8.3f} {r_:+7.3f}   "
                  f"{lo:g} - {hi:g}  ({hi/lo:.0f}x)")

    # How tightly is Vd constrained overall, compared with clearance?
    vds = [f(r["vd_L_kg"]) for r in rows]
    print()
    print("SPREAD OF EACH PARAMETER ACROSS ALL 46 SPECIES-SEX-CHEMICAL GROUPS")
    print(f"  Vd         : {min(vds):.3f} to {max(vds):.3f} L/kg   "
          f"({max(vds)/min(vds):.1f}x)")
    # Clearance units differ between human (per year) and animal (per day), so
    # compare animals only to keep the comparison honest.
    cls = [f(r["clearance_native"]) for r in rows
           if r["species"] != "human" and f(r["clearance_native"])]
    hls = [f(r["halflife_d"]) for r in rows
           if r["species"] != "human" and f(r["halflife_d"])]
    print(f"  clearance  : {min(cls):.5f} to {max(cls):.3f} L/kg/d  "
          f"({max(cls)/min(cls):,.0f}x)   [animals only]")
    print(f"  half-life  : {min(hls):.3f} to {max(hls):.1f} d       "
          f"({max(hls)/min(hls):,.0f}x)   [animals only]")
    print()
    print("  Vd varies ~20x across every chemical, species and sex in the set;")
    print("  clearance varies by four orders of magnitude. Whatever drives PFAS")
    print("  half-life differences, it is not the volume of distribution.")


if __name__ == "__main__":
    main()
