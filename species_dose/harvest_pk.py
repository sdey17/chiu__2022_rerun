"""
Harvest the EPA paper's fitted PK parameters from their notebook outputs.

Their `PFAS_manuscript_results.ipynb` prints one dataframe row per
(PFAS, species, sex) as it loops, and those printed rows are saved in the
notebook. That saves refitting ~40 models: the traces themselves are not
in the repo (traces/ ships empty).
"""
import json
import os
import re
import sys

import pandas as pd

NB = os.path.join(os.environ["EPA_REPO"],
                  "auxiliary_notebooks", "PFAS_manuscript_results.ipynb")
PFAS = ["PFBA", "PFBS", "PFHxA", "PFHxS", "PFOA", "PFOS", "PFNA", "PFDA"]
# posterior arrays print truncated, e.g. "[0.294, 0.198, 0.34..." - collapse
# them to a single token so the row can be split on whitespace
LIST = re.compile(r"\[[^\]]*?\.\.\.")


def rows_from_text(text):
    out, header = [], None
    for line in text.split("\n"):
        clean = LIST.sub("LIST", line)
        cols = clean.split()
        if "PFAS" in cols and "species" in cols:
            header = cols                      # pandas omits the index name
            continue
        if header and cols and cols[0].isdigit() and cols[1] in PFAS:
            vals = cols[1:]                    # drop the row index
            if len(vals) == len(header):
                out.append(dict(zip(header, vals)))
    return out


def harvest():
    nb = json.load(open(NB))
    rows = []
    for cell in nb["cells"]:
        for o in cell.get("outputs", []):
            t = o.get("text") or (o.get("data", {}) or {}).get("text/plain")
            if t:
                rows += rows_from_text("".join(t))
    df = pd.DataFrame(rows)
    keep = ["PFAS", "sex", "species", "model", "CLC_mean", "CLC_lower", "CLC_upper",
            "halft_mean", "halft_lower", "halft_upper", "Vd_mean", "Vd_lower",
            "Vd_upper", "BW"]
    df = df[[c for c in keep if c in df]]
    for c in df.columns:
        if c not in ("PFAS", "sex", "species", "model"):
            df[c] = pd.to_numeric(df[c], errors="coerce")
    # the same row is printed more than once as the notebook loops
    df = df.drop_duplicates(subset=["PFAS", "sex", "species"]).reset_index(drop=True)
    return df.sort_values(["PFAS", "species", "sex"])


if __name__ == "__main__":
    df = harvest()
    df.to_csv("animal_pk.csv", index=False)
    pd.set_option("display.width", 200)
    print(df.to_string(index=False))
    print(f"\n{len(df)} of 48 PFAS x species x sex combinations recovered")
