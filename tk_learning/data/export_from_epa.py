"""
Regenerate the tutorial CSVs from EPA's extracted_data/.

The original export was done ad hoc and never written down, which made
"what exactly was dropped?" unanswerable. This script is the answer: it
is the whole pipeline, and running it reproduces data/*.csv exactly.

    git clone --depth 1 https://github.com/USEPA/CPHEA-Animal-PFAS-PK /tmp/epa
    python data/export_from_epa.py /tmp/epa

WHAT IT KEEPS AND WHAT IT DROPS

    keeps   serum and plasma only (EPA records "serum" for the primate
            studies and "plasma" for most rat ones; they are the same
            compartment for our purposes)
    drops   tissue matrices (liver, kidney, brain, ...)
    drops   matrix == "blood". Iwabuchi 3859701 reports whole blood AND
            serum for the same animals, as separate rows. They are not
            interchangeable -- PFAS bind plasma protein and sit at
            lower concentration in red cells, so whole-blood values run
            below serum ones. Pooling them would put two different
            measurements on one curve.
    drops   rows with conc_mean == -1, EPA's code for "missing or below
            the limit of detection"  <-- see the warning below
    keeps   everything else, values unaltered

THE BELOW-DETECTION-LIMIT WARNING

    Dropping censored values is NOT neutral. Below-LoD rows are always
    the LATE, low points -- exactly the ones carrying the terminal
    slope. Deleting them truncates each curve early and biases
    half-lives SHORT. Lesson 03 question 4 is about precisely this.

    Proper handling treats them as censored (known to be below a
    threshold) rather than missing. We drop them because the lessons
    use ordinary least squares, which has no way to express "this value
    is somewhere below 0.05". Know that the shortcut is there.

    Rows dropped this way, per file, are printed below.

UNITS

    EPA stores each study in the units its source paper used. This
    normalises everything to days and mg/L, which for the two studies
    reporting nmol/ml needs a molecular weight.
"""
import os
import re
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))

# (chemical DTXSID, species, sex) -> output filename stem
WANTED = {
    ("DTXSID8031865", "primate", "Male"): "PFOA_Male_primate",
    ("DTXSID8031865", "primate", "Female"): "PFOA_Female_primate",
    ("DTXSID3031864", "primate", "Male"): "PFOS_Male_primate",
    ("DTXSID8031865", "rat", "Male"): "PFOA_Male_rat",
    ("DTXSID8031865", "rat", "Female"): "PFOA_Female_rat",
    ("DTXSID3031864", "rat", "Male"): "PFOS_Male_rat",
}

MW = {"DTXSID8031865": 414.07, "DTXSID3031864": 500.13}   # g/mol


def body_weights(epa_root):
    """Parse register_pfas_data.py for the study-level body weights.

    EPA's extracted_data files carry BW = -1 for summary records; the
    real weights live in the registration script, which assigns
    hero_id on one line and calls register_study on later ones.
    """
    path = os.path.join(epa_root, "register_pfas_data.py")
    out, hero = {}, None
    for line in open(path):
        m = re.search(r"hero_id\s*=\s*(\d{6,})", line)
        if m and "register_study" not in line:
            hero = int(m.group(1))
        if "register_study(" in line and hero:
            sp = re.search(r"species='(\w+)'", line)
            sx = re.search(r"sex='(\w+)'", line)
            w = re.search(r"weight=([\d.]+)", line)
            u = re.search(r"weight_units='(\w+)'", line)
            if sp and sx and w:
                kg = float(w.group(1))
                if u and u.group(1).lower().startswith("gram"):
                    kg /= 1000.0
                out[(hero, sp.group(1), sx.group(1))] = kg
    return out


def to_days(df):
    u = df.time_units.astype(str).str.lower()
    t = pd.to_numeric(df.time, errors="coerce")
    return np.select([u.str.startswith("h"), u.str.startswith("mi"),
                      u.str.startswith("w"), u.str.startswith("d")],
                     [t / 24.0, t / 1440.0, t * 7.0, t], default=t)


def to_mgL(df):
    u = df.conc_units.astype(str).str.lower().str.strip()
    c = pd.to_numeric(df.conc_mean, errors="coerce")
    mw = df.dtxsid.map(MW)
    out = np.full(len(df), np.nan)
    out = np.where(u.isin(["ug/ml", "mg/l"]), c, out)
    out = np.where(u.isin(["ng/ml", "ug/l"]), c / 1000.0, out)
    out = np.where(u == "nmol/ml", c * mw / 1000.0, out)      # needs MW
    return out


def main(epa_root):
    folder = os.path.join(epa_root, "extracted_data")
    bw = body_weights(epa_root)
    print(f"body weights parsed for {len(bw)} study/species/sex groups\n")

    frames = {v: [] for v in WANTED.values()}
    dropped = {v: 0 for v in WANTED.values()}

    for p in sorted(os.listdir(folder)):
        m = re.match(r"([A-Za-z-]+)_(\d+)\.csv$", p)
        if not m:
            continue
        author, hero = m.group(1), int(m.group(2))
        d = pd.read_csv(os.path.join(folder, p))
        # serum/plasma only -- NOT "blood"; see the note at the top
        d = d[d.matrix.astype(str).str.lower().isin(["serum", "plasma"])]
        if not len(d):
            continue
        d = d.copy()
        d["t_d"], d["c"] = to_days(d), to_mgL(d)

        for (dtx, sp, sx), stem in WANTED.items():
            g = d[(d.dtxsid == dtx) & (d.species == sp) & (d.sex == sx)]
            if not len(g):
                continue
            raw = pd.to_numeric(g.conc_mean, errors="coerce")
            dropped[stem] += int((raw <= 0).sum() + raw.isna().sum())
            g = g[np.isfinite(g.c) & (g.c > 0)]
            if not len(g):
                continue
            w = bw.get((hero, sp, sx), np.nan)
            frames[stem].append(pd.DataFrame({
                "study": hero, "author": author, "route": g.route.values,
                "dose_mgkg": pd.to_numeric(g.dose).values,
                "dose_mg": pd.to_numeric(g.dose).values * w,
                "bw_kg": w, "time_d": g.t_d.values, "conc_mgL": g.c.values,
                "conc_sd": np.where(pd.to_numeric(g.conc_sd, errors="coerce") < 0,
                                    0.0, pd.to_numeric(g.conc_sd, errors="coerce")),
                "n_animals": pd.to_numeric(g.N_animals, errors="coerce").values,
                "animal_id": g.animal_id.values,
                "dataset": [f"{hero}-{dd} mg/kg-{rr}"
                            for dd, rr in zip(pd.to_numeric(g.dose), g.route)],
            }))

    print(f"{'file':24s} {'rows':>6s} {'studies':>8s} {'dropped <=0':>12s}")
    for stem, parts in frames.items():
        if not parts:
            print(f"{stem:24s} {'none':>6s}")
            continue
        out = pd.concat(parts, ignore_index=True)
        out = out.sort_values(["dataset", "time_d"]).reset_index(drop=True)
        dest = os.path.join(HERE, stem + ".csv")
        out.to_csv(dest, index=False)
        print(f"{stem:24s} {len(out):6d} {out.study.nunique():8d} "
              f"{dropped[stem]:12d}")

    print("\nDropped rows are EPA's conc_mean == -1: missing, or below the\n"
          "limit of detection. They are the LATE points, so dropping them\n"
          "biases half-lives short. See the note at the top of this file.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1])
