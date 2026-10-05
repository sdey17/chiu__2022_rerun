#!/usr/bin/env python3
"""Build the master exposure-versus-kinetics table: one row per
PFAS x species x sex, carrying the administered dose, the serum concentration
actually measured, the half-life, Vd and clearance.

This is the table that lets dose, internal concentration and half-life be
compared on one line, which is what the exposure-versus-half-life question
needs. Animal and primate rows come from the EPA population PK fits; the human
rows come from Chiu 2022.
"""
import csv
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent.parent / "species_dose" / "species_exposure.csv"
OUT = HERE.parent / "db" / "master_exposure_halflife.csv"

# Chiu's human fits are reported per YEAR (half-life in years, clearance in
# L/kg/year); the EPA animal fits are per DAY. The source file mixes the two
# without a units column, so normalise here and keep the native values too.
HUMAN_TIME_UNIT_IS_YEARS = True
DAYS_PER_YEAR = 365.25

FIELDS = [
    "chemical", "species", "sex", "n_observations",
    "dose_median", "dose_min", "dose_max", "dose_units",
    "serum_median_ng_mL", "serum_min_ng_mL", "serum_max_ng_mL",
    "halflife_native", "halflife_ci_low_native", "halflife_ci_high_native",
    "native_time_unit",
    "halflife_d", "halflife_y",
    "vd_L_kg", "vd_ci_low", "vd_ci_high",
    "clearance_native", "clearance_ci_low_native", "clearance_ci_high_native",
    "clearance_units",
    "body_weight_kg", "model", "source",
]

SOURCE = ("EPA CPHEA animal PFAS PK population fits, re-harvested in "
          "../species_dose/harvest_pk.py; human rows from Chiu et al. 2022 "
          "(doi:10.1289/EHP10103)")


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def main() -> None:
    rows = []
    for r in csv.DictReader(SRC.open()):
        hl = f(r["halft_mean"])
        years = r["species"] == "human" and HUMAN_TIME_UNIT_IS_YEARS
        unit = "year" if years else "day"
        hl_d = (hl * DAYS_PER_YEAR if years else hl) if hl is not None else None
        rows.append({
            "chemical": r["PFAS"], "species": r["species"], "sex": r["sex"],
            "n_observations": r["n_obs"],
            "dose_median": r["dose_median"], "dose_min": r["dose_min"],
            "dose_max": r["dose_max"], "dose_units": r["dose_units"],
            "serum_median_ng_mL": r["serum_median"],
            "serum_min_ng_mL": r["serum_min"], "serum_max_ng_mL": r["serum_max"],
            "halflife_native": r["halft_mean"],
            "halflife_ci_low_native": r["halft_lower"],
            "halflife_ci_high_native": r["halft_upper"],
            "native_time_unit": unit,
            "halflife_d": f"{hl_d:.4f}" if hl_d is not None else "",
            "halflife_y": f"{hl_d/DAYS_PER_YEAR:.5f}" if hl_d is not None else "",
            "vd_L_kg": r["Vd_mean"], "vd_ci_low": r["Vd_lower"],
            "vd_ci_high": r["Vd_upper"],
            "clearance_native": r["CLC_mean"],
            "clearance_ci_low_native": r["CLC_lower"],
            "clearance_ci_high_native": r["CLC_upper"],
            "clearance_units": f"L/kg/{unit}",
            "body_weight_kg": r["BW"], "model": r["model"], "source": SOURCE,
        })

    rows.sort(key=lambda r: (r["chemical"],
                             {"human": 0, "primate": 1, "rat": 2, "mouse": 3}
                             .get(r["species"], 9), r["sex"]))
    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {OUT}  ({len(rows)} rows)\n")

    # Print the human-versus-animal contrast the review turns on.
    print("MASTER TABLE - dose, measured serum concentration and half-life on one line")
    print(f"{'chemical':8} {'species':8} {'sex':7} {'dose':>11} {'units':<14} "
          f"{'serum ng/mL':>12} {'t1/2 (d)':>11} {'t1/2 (y)':>9}")
    print("-" * 96)
    for r in rows:
        if not r["halflife_d"]:
            continue
        d = f(r["dose_median"])
        sc = f(r["serum_median_ng_mL"])
        ds = f"{d:11.3g}" if d is not None else "          -"
        ss = f"{sc:12.1f}" if sc is not None else "           -"
        print(f"{r['chemical']:8} {r['species']:8} {r['sex']:7} {ds} "
              f"{r['dose_units']:<14} {ss} "
              f"{f(r['halflife_d']):11.3f} {f(r['halflife_y']):9.4f}")

    # The human/rodent exposure gap, which is the confound the review must break.
    print()
    print("HUMAN vs RODENT, where both exist")
    print("(half-lives both in DAYS after normalising Chiu's human years)")
    print(f"{'chemical':8} {'human serum':>12} {'rat serum':>12} {'serum gap':>10} "
          f"{'human t1/2':>11} {'rat t1/2':>10} {'t1/2 gap':>9}")
    print("-" * 80)
    idx = {(r["chemical"], r["species"], r["sex"]): r for r in rows}
    for c in sorted({r["chemical"] for r in rows}):
        h = idx.get((c, "human", "Male"))
        rt = idx.get((c, "rat", "Male"))
        if not (h and rt and h["halflife_d"] and rt["halflife_d"]):
            continue
        hs, rs = f(h["serum_median_ng_mL"]), f(rt["serum_median_ng_mL"])
        ht, rtt = f(h["halflife_d"]), f(rt["halflife_d"])
        sg = rs / hs if hs else float("nan")
        tg = ht / rtt if rtt else float("nan")
        print(f"{c:8} {hs:12.1f} {rs:12.1f} {sg:9.0f}x {ht:11.0f} {rtt:10.1f} {tg:8.1f}x")


if __name__ == "__main__":
    main()
