"""
Read Chiu et al.'s MCSim input files (data/*.in.R) into a pandas table.

Each `Simulation { }` block is one person or one population summary. We keep
only blocks that sit inside a Level with a `Likelihood()` -- those are the
training data. Blocks without one are test data and do not affect the fit.

    python parse_chiu_data.py PFOA     # print the table
"""
import re
import sys
from pathlib import Path

import pandas as pd

DATA = Path(__file__).parent / "data"
FILES = {
    "PFOA": DATA / "PFOA_1cpt_v8.MCMC_TrainTest.in.R",
    "PFOS": DATA / "PFOS_1cpt_v8.PopMCMC_MeanIndivTrainTest.in.R",
    "PFNA": DATA / "PFNA_1cpt_v8.PopMCMC_MeanIndivTrainTest.in.R",
    "PFHxS": DATA / "PFHxS_1cpt_v8.PopMCMC_MeanIndivTrainTest.in.r",
}
NUM = r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?"


def numbers(s):
    return [float(x) for x in re.findall(NUM, s)]


def parse_simulation(code):
    """Pull the fields we need out of one Simulation block (comments removed)."""
    row = {}
    for name in ["Cbgd_in_gm", "Cbgd_in_gsd", "C_0_in_gm", "C_0_in_gsd"]:
        row[name] = float(re.search(rf"{name}\s*=\s*({NUM})", code).group(1))

    doses = re.search(r"DWC_t\s*=\s*NDoses\((.*?)\)", code, re.S)
    const = re.search(rf"DWC\s*=\s*({NUM})\s*;", code)
    if doses:                                   # time-varying water concentration
        n, *rest = numbers(doses.group(1))
        row["dose_conc"], row["dose_times"] = rest[:int(n)], rest[int(n):]
    elif const:                                 # known constant water concentration
        row["dwc"] = float(const.group(1))
    # otherwise DWC = PerDose(DWC_belowMRL, ...): an unknown value below the MRL

    endpoint, data = re.search(r"Data\s*\(\s*(\w+)\s*,([^)]*)\)", code).groups()
    row["endpoint"] = endpoint
    row["values"] = numbers(data)
    row["times"] = numbers(re.search(r"Print\s*\(\s*\w+\s*,([^)]*)\)", code).group(1))
    return row


def load(chem):
    """Return one row per training Simulation block."""
    raw = FILES[chem].read_text().split("\n")
    lines = [l.split("#")[0] for l in raw]      # same lines, comments removed
    levels = []   # stack of open Levels: {"label", "depth", "fit", "mrl"}
    rows = []
    depth, i = 0, 0

    while i < len(lines):
        code = lines[i]
        if re.match(r"\s*Simulation\s*\{", code):
            block, d = [], 0
            while True:                         # collect lines until braces balance
                block.append(lines[i])
                d += lines[i].count("{") - lines[i].count("}")
                i += 1
                if d == 0:
                    break
            if any(lv["fit"] for lv in levels):
                row = parse_simulation("\n".join(block))
                # Levels: [0] population, [1] "Studies", [2] one study.
                # MCSim gives each child of "Studies" its own background scale,
                # so levels[2] is the study a row belongs to.
                row["study"] = levels[2]["label"]
                row["mrl"] = next((lv["mrl"] for lv in reversed(levels) if lv["mrl"]), None)
                rows.append(row)
            continue

        if re.match(r"\s*Level\s*\{", code):
            label = raw[i].split("#", 1)[1].strip()[:40] if "#" in raw[i] else ""
            levels.append({"label": label, "depth": depth + 1, "fit": False, "mrl": None})
        if re.search(r"Likelihood\s*\(", code):
            levels[-1]["fit"] = True
        m = re.search(rf"Distrib\s*\(\s*DWC_belowMRL\s*,\s*Uniform\s*,\s*{NUM}\s*,\s*({NUM})", code)
        if m:
            levels[-1]["mrl"] = float(m.group(1))

        depth += code.count("{") - code.count("}")
        levels = [lv for lv in levels if lv["depth"] <= depth]   # close finished Levels
        i += 1

    return pd.DataFrame(rows)


if __name__ == "__main__":
    for chem in sys.argv[1:] or FILES:
        df = load(chem)
        print(f"\n{chem}: {len(df)} training records")
        print(df.groupby(["study", "endpoint"], sort=False).size().to_string())
