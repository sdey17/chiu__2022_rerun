"""
Check data/*.csv against EPA's published extracted_data/, row by row.

This repository's CSVs are a re-export of EPA's digitised values. That
claim is only worth anything if you can check it, so:

    git clone --depth 1 https://github.com/USEPA/CPHEA-Animal-PFAS-PK /tmp/epa
    python data/verify_against_epa.py /tmp/epa/extracted_data

It matches on (study, animal_id or dose, time) and reports the largest
disagreement in concentration. Expected result: zero.

It also reports, per file, how many rows EPA transcribed from a table,
appendix or supplement versus digitised from a figure -- the `source`
column in their files records this per record, and it matters, because
a value read off a plot carries error that no later analysis recovers.
"""
import glob
import os
import re
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))


def load_epa(folder):
    out = {}
    for p in glob.glob(os.path.join(folder, "*.csv")):
        m = re.search(r"_(\d+)\.csv$", p)
        if m:
            out[int(m.group(1))] = pd.read_csv(p)
    if not out:
        sys.exit(f"no *_<heroid>.csv files found in {folder}")
    return out


# EPA stores every study in the units its paper used. Our export
# normalises to mg/L, so a faithful comparison has to undo that --
# including a molar-to-mass conversion for the two studies reporting
# nmol/ml. Molecular weights from the DSSTox records in
# auxiliary/pfas_master.csv.
MW = {                      # g/mol, keyed by DTXSID
    "DTXSID8031865": 414.07,    # PFOA
    "DTXSID3031864": 500.13,    # PFOS
    "DTXSID3031862": 314.05,    # PFHxA
    "DTXSID8031863": 464.08,    # PFNA
    "DTXSID3031860": 514.08,    # PFDA
    "DTXSID7040150": 400.11,    # PFHxS
    "DTXSID5030030": 300.10,    # PFBS
    "DTXSID4059916": 214.04,    # PFBA
}


def to_mgL(df):
    """Convert EPA's per-study concentration units to mg/L."""
    u = df.conc_units.astype(str).str.lower().str.strip()
    c = pd.to_numeric(df.conc_mean, errors="coerce")
    mw = df.dtxsid.map(MW)
    out = np.full(len(df), np.nan)
    out = np.where(u.isin(["ug/ml", "mg/l"]), c, out)
    out = np.where(u.isin(["ng/ml", "ug/l"]), c / 1000.0, out)
    # nmol/ml -> umol/L -> mg/L needs the molecular weight
    out = np.where(u == "nmol/ml", c * mw / 1000.0, out)
    return out


def to_days(df):
    """EPA records time in hours, days, minutes or weeks per study."""
    u = df.time_units.astype(str).str.lower()
    t = pd.to_numeric(df.time, errors="coerce")
    return np.select(
        [u.str.startswith("h"), u.str.startswith("mi"),
         u.str.startswith("w"), u.str.startswith("d")],
        [t / 24.0, t / 1440.0, t * 7.0, t],
        default=t)


def source_kind(s):
    return "figure" if str(s).lower().startswith("figure") else "table"


def main(folder):
    epa = load_epa(folder)
    print(f"EPA extracted_data: {len(epa)} study files\n")

    worst, checked, unmatched = 0.0, 0, 0
    for f in sorted(glob.glob(os.path.join(HERE, "*.csv"))):
        mine = pd.read_csv(f)
        name = os.path.basename(f)[:-4]
        kinds = {"table": 0, "figure": 0}
        file_worst, file_n = 0.0, 0

        for hero, g in mine.groupby("study"):
            e = epa.get(hero)
            if e is None:
                print(f"   {name}: HERO {hero} not in EPA folder")
                continue
            e = e.copy()
            # blood compartment only: these files also carry liver,
            # kidney, brain and other tissue measurements. EPA records
            # "serum" for the primate studies and "plasma" for most rat
            # ones; for our purposes they are the same compartment.
            if "matrix" in e.columns:
                e = e[e.matrix.astype(str).str.lower()
                      .isin(["serum", "plasma", "blood"])]
            e["t_d"] = to_days(e)
            e["c"] = to_mgL(e)
            e = e[np.isfinite(e.c)]
            if not len(e):
                continue
            # rows are counted by source kind below, as each is matched
            for _, row in g.iterrows():
                # Narrow on time AND dose together first. Filtering by
                # animal_id before dose can empty the candidate set and
                # report a spurious mismatch.
                cand = e[np.isclose(e.t_d, row.time_d, rtol=1e-6, atol=1e-9)
                         & np.isclose(e.dose, row.dose_mgkg, rtol=1e-3)]
                # animal_id is a string here and may be "-1" (a group
                # mean) or NaN; use it only to disambiguate, never to
                # exclude.
                aid = pd.to_numeric(getattr(row, "animal_id", None),
                                    errors="coerce")
                if pd.notna(aid) and aid > 0:
                    c2 = cand[pd.to_numeric(cand.animal_id,
                                            errors="coerce") == aid]
                    if len(c2):
                        cand = c2
                if not len(cand):
                    unmatched += 1
                    continue
                diff = float(np.min(np.abs(cand.c.values - row.conc_mgL)))
                file_worst = max(file_worst, diff)
                file_n += 1
                kinds[source_kind(cand.source.iloc[0])] += 1

        worst = max(worst, file_worst)
        checked += file_n
        tot = kinds["table"] + kinds["figure"]
        pct = 100 * kinds["figure"] / tot if tot else 0
        print(f"   {name:<20s} {file_n:4d}/{len(mine):4d} rows matched, "
              f"max diff {file_worst:.2e} mg/L")
        print(f"   {'':20s}      provenance: {kinds['table']} from tables, "
              f"{kinds['figure']} digitised from figures ({pct:.0f}%)")

    print(f"\n{checked} values compared, {unmatched} unmatched")
    print(f"largest disagreement anywhere: {worst:.3e} mg/L")
    if worst == 0.0 and unmatched == 0:
        print("\nEvery value is identical to EPA's. The export changed no data.")
    elif worst > 1e-9:
        print("\nVALUES DIFFER -- EPA's are authoritative, not ours.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1])
