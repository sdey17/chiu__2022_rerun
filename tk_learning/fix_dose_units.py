#!/usr/bin/env python3
"""Repair the dose_mgkg column in data/*.csv.

The bug. These files were built from the EPA CPHEA-Animal-PFAS-PK database,
whose `dose` column carries whatever unit the source paper used. Two of the
studies - Kudo (HERO 2990271) and Ohmori (HERO 3858670), both PFOA in rats -
report dose in umol/kg rather than mg/kg. The build copied that raw number into
a column named `dose_mgkg` without converting it, so those rows read 48.63 when
the dose is 20.14 mg/kg: a factor of 1000/414.07 = 2.415, PFOA's molar mass.

Concentration and time WERE converted correctly, and the `dataset` label was
built from a correctly converted dose. That label is therefore an independent,
internally consistent record of the right value, and is used here as the
authority rather than re-deriving from a molar mass.

Why it matters. Lesson 10 computes clearance as dose/AUC, so the affected
datasets came out 2.415x too high - in the lesson about sex and species
differences, which is exactly where a spurious factor would mislead.

Not affected: ../pfas_dose, which reads EPA's own processed data through
get_processed_data(dose_label="dose_mg") rather than these CSVs, and whose
meta-regression uses within-study contrasts that are invariant to a constant
unit error anyway; and ../pfas_tk_review/scripts/fit_cphea_halflives.py, which
filters on dose_units == "mg/kg" explicitly.

Run:  python fix_dose_units.py          # report only
      python fix_dose_units.py --write  # apply
"""
import sys
import re
from pathlib import Path

import pandas as pd

DATA = Path(__file__).resolve().parent / "data"
LABEL = re.compile(r"-([\d.]+) mg/kg-")


def main() -> None:
    write = "--write" in sys.argv
    total = 0
    for f in sorted(DATA.glob("*.csv")):
        d = pd.read_csv(f)
        label_dose = d.dataset.str.extract(LABEL)[0].astype(float)
        if label_dose.isna().any():
            print(f"{f.name}: {label_dose.isna().sum()} rows have no parseable "
                  "dose in the dataset label; skipped")
        bad = (label_dose - d.dose_mgkg).abs() > 1e-6
        bad &= label_dose.notna()
        if not bad.any():
            print(f"{f.name}: ok")
            continue
        total += int(bad.sum())
        print(f"{f.name}: correcting {bad.sum()} of {len(d)} rows")
        for ds, g in d[bad].groupby("dataset"):
            was = g.dose_mgkg.iloc[0]
            now = label_dose[g.index].iloc[0]
            print(f"    {ds:<34} {was:g} -> {now:g} mg/kg "
                  f"(factor {was/now:.3f})  n={len(g)}")
        if write:
            d.loc[bad, "dose_mgkg"] = label_dose[bad]
            # dose_mg is the absolute dose; keep it consistent where present.
            if "dose_mg" in d.columns and "bw_kg" in d.columns:
                d.loc[bad, "dose_mg"] = d.loc[bad, "dose_mgkg"] * d.loc[bad, "bw_kg"]
            d.to_csv(f, index=False)

    print()
    if total == 0:
        print("nothing to correct")
    elif write:
        print(f"corrected {total} rows. Re-run test_lessons.py and lesson 10.")
    else:
        print(f"{total} rows need correction. Re-run with --write to apply.")


if __name__ == "__main__":
    main()
