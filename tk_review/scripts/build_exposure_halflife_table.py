#!/usr/bin/env python3
"""Build the headline table: PFAS name, serum concentration, exposure amount and
half-life, for human studies and animal experiments on the same sheet.

Human rows come from db/human_halflife_extended.csv, whose concentration fields
are free text ("49 median (range 0.5-1090)"), so a numeric column is parsed out
and the original string is kept beside it. Animal rows come from
db/master_exposure_halflife.csv, which is already numeric.

Output: db/exposure_vs_halflife.csv and a printed summary.
"""
import csv
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
DB = HERE.parent / "db"
OUT = DB / "exposure_vs_halflife.csv"

FIELDS = [
    "chemical", "evidence", "species", "sex", "study_or_source", "year",
    "pmid_or_doi", "n", "population_or_strain",
    "serum_ng_mL", "serum_as_reported",
    "exposure_amount", "exposure_units", "exposure_as_reported",
    "halflife_y", "halflife_ci_low", "halflife_ci_high",
    "vd_L_kg", "model", "estimation_basis", "verified_or_source",
]

# A leading number, tolerating "<", "~", thousands separators and a trailing unit.
LEADING_NUM = re.compile(r"^[<~>\s]*([0-9]+(?:[.,][0-9]+)?)(?:\s*[eE][-+]?\d+)?")


def parse_num(text):
    """Return the leading numeric value of a free-text field, else None."""
    if not text:
        return None
    t = text.strip()
    # Reject fields that open with a word ("lower than males", "see Table S1").
    if not re.match(r"^[<~>\s]*[0-9]", t):
        return None
    m = LEADING_NUM.match(t)
    if not m:
        return None
    try:
        return float(m.group(1).replace(",", ""))
    except ValueError:
        return None


def main() -> None:
    rows = []

    # ---- human studies -------------------------------------------------
    for r in csv.DictReader((DB / "human_halflife_extended.csv").open()):
        serum = parse_num(r["initial_serum_ng_mL"])
        water = parse_num(r["water_conc_ngL"])
        intake = parse_num(r["intake_ng_kg_day"])
        if intake is not None:
            amount, units, as_rep = intake, "ng/kg/day intake", r["intake_ng_kg_day"]
        elif water is not None:
            amount, units, as_rep = water, "ng/L drinking water", r["water_conc_ngL"]
        else:
            amount, units, as_rep = None, "", r["exposure_source"]
        rows.append({
            "chemical": r["chemical"], "evidence": "human study",
            "species": "human", "sex": r["sex"],
            "study_or_source": r["study"], "year": r["year"],
            "pmid_or_doi": r["pmid"] or r["doi"], "n": r["n"],
            "population_or_strain": r["population"],
            "serum_ng_mL": f"{serum:g}" if serum is not None else "",
            "serum_as_reported": r["initial_serum_ng_mL"],
            "exposure_amount": f"{amount:g}" if amount is not None else "",
            "exposure_units": units, "exposure_as_reported": as_rep,
            "halflife_y": r["halflife_y"], "halflife_ci_low": r["ci_low"],
            "halflife_ci_high": r["ci_high"], "vd_L_kg": r["vd_L_kg"],
            "model": r["model"],
            "estimation_basis": r["estimation_basis_serumdecay_or_massbalance"],
            "verified_or_source": r["verified"],
        })

    # ---- animal and primate experiments --------------------------------
    for r in csv.DictReader((DB / "master_exposure_halflife.csv").open()):
        if r["species"] == "human":
            continue   # Chiu's human row is already represented above
        if not r["halflife_y"]:
            continue
        rows.append({
            "chemical": r["chemical"], "evidence": "animal experiment",
            "species": r["species"], "sex": r["sex"],
            "study_or_source": "EPA CPHEA population PK fit", "year": "",
            "pmid_or_doi": "", "n": r["n_observations"],
            "population_or_strain": "",
            "serum_ng_mL": f"{float(r['serum_median_ng_mL']):g}"
                           if r["serum_median_ng_mL"] else "",
            "serum_as_reported": f"{r['serum_median_ng_mL']} (median of "
                                 f"{r['n_observations']} observations)",
            "exposure_amount": r["dose_median"], "exposure_units": r["dose_units"],
            "exposure_as_reported": f"{r['dose_min']}-{r['dose_max']} "
                                    f"{r['dose_units']}",
            "halflife_y": r["halflife_y"], "halflife_ci_low": "",
            "halflife_ci_high": "", "vd_L_kg": r["vd_L_kg"],
            "model": r["model"], "estimation_basis": "serum decay",
            "verified_or_source": "EPA CPHEA fits via ../species_dose",
        })

    rows.sort(key=lambda r: (r["chemical"], r["evidence"],
                             r["species"], r["sex"]))
    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

    n_h = sum(1 for r in rows if r["evidence"] == "human study")
    n_a = len(rows) - n_h
    n_serum = sum(1 for r in rows if r["serum_ng_mL"])
    n_exp = sum(1 for r in rows if r["exposure_amount"])
    print(f"wrote {OUT}")
    print(f"  {len(rows)} rows: {n_h} human, {n_a} animal")
    print(f"  {n_serum} carry a numeric serum concentration")
    print(f"  {n_exp} carry a numeric exposure amount")
    print(f"  {len(rows)-n_serum} human rows report serum only as text "
          "(kept in serum_as_reported)")

    print("\nHUMAN ROWS WITH BOTH A SERUM LEVEL AND A HALF-LIFE")
    print(f"  {'chemical':<8} {'serum':>9} {'t1/2 y':>7}  {'study':<28} basis")
    print("  " + "-" * 78)
    sel = [r for r in rows if r["evidence"] == "human study"
           and r["serum_ng_mL"] and r["halflife_y"]]
    sel.sort(key=lambda r: (r["chemical"], float(r["serum_ng_mL"])))
    for r in sel[:28]:
        print(f"  {r['chemical']:<8} {float(r['serum_ng_mL']):9.1f} "
              f"{r['halflife_y']:>7}  {r['study_or_source'][:28]:<28} "
              f"{r['estimation_basis'][:22]}")
    if len(sel) > 28:
        print(f"  ... and {len(sel)-28} more")


if __name__ == "__main__":
    main()
