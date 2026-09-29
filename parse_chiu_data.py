"""
Read Chiu et al.'s MCSim input files (data/*.in.R) into a pandas table.

Each `Simulation { }` block is one person or one population summary. We keep
only blocks that sit inside a Level with a `Likelihood()` -- those are the
training data. Blocks without one are test data and do not affect the fit.

    python parse_chiu_data.py PFOA     # print the table


WHAT THESE FILES ARE
--------------------
Chiu fitted his model with MCSim, a simulation tool driven by plain-text
input files. Despite the `.in.R` extension they are NOT R code -- they are
MCSim's own format. A file looks like this, nested with curly braces:

    Level {                                  # population priors
      Distrib (M_ln_k, Normal, -1.8971, 0.4055);
      Level {                                # "Studies"
        Distrib (M_ln_Cbgd_sc, Normal, -0.22314, 0.4055);
        Level {   # Decatur Training - has individual data
          Likelihood (Cserum, LogNormal, Prediction(Cserum), GSD_Cserum);
          Simulation {                       # <- one person
            Cbgd_in_gm = 0.63;               # their background prior
            C_0_in_gm  = 1.9;                # their starting level
            DWC = PerDose(DWC_belowMRL,...); # their water exposure
            Print(Cserum, 0, 5.802);         # when blood was taken (years)
            Data (Cserum, 1.9, 1.1);         # what it measured (ug/L)
          }
          Simulation { ... }                 # <- next person
        }
        Level {   # Decatur TEST SET ... }   # no Likelihood -> not fitted
      }
    }

Two things have to be read from the STRUCTURE, not from any one line:

1. TRAINING vs TEST. A block counts toward the fit only if some enclosing
   Level declared a `Likelihood()`. Chiu held out half of each study to
   check predictions afterwards, and those held-out blocks look identical
   apart from the missing Likelihood. Comments are not a reliable guide --
   one training Level is labelled only "41 Males; 69 Females has individual
   data", with no mention of training or testing.

2. WHICH STUDY a person belongs to. In MCSim, a `Distrib` inside a Level
   is drawn once per CHILD of that Level, so the parameters declared in
   the "Studies" Level exist once per town. A person's study is therefore
   the Level at depth 2, and `model.py` gives each one its own background
   scale.

So `load()` walks the file tracking brace depth and a stack of open Levels,
rather than pattern-matching lines in isolation.
"""
import re
import sys
from pathlib import Path

import pandas as pd

DATA = Path(__file__).parent / "data"
# Filenames are not consistent across the four chemicals (note the lowercase
# .r on PFHxS), so they are listed rather than globbed.
FILES = {
    "PFOA": DATA / "PFOA_1cpt_v8.MCMC_TrainTest.in.R",
    "PFOS": DATA / "PFOS_1cpt_v8.PopMCMC_MeanIndivTrainTest.in.R",
    "PFNA": DATA / "PFNA_1cpt_v8.PopMCMC_MeanIndivTrainTest.in.R",
    "PFHxS": DATA / "PFHxS_1cpt_v8.PopMCMC_MeanIndivTrainTest.in.r",
}
# int, decimal or scientific notation, with optional sign
NUM = r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?"


def numbers(s):
    """Every number in a string, in order (MCSim lists them comma-separated)."""
    return [float(x) for x in re.findall(NUM, s)]


def parse_simulation(code):
    """Pull the fields we need out of one Simulation block (comments removed).

    Produces one dict: the person's background and starting-level priors,
    their water exposure, and the measurements themselves.
    """
    row = {}
    # Priors specific to this person: geometric mean and geometric SD of
    # their background level (Cbgd, from NHANES for the relevant year) and
    # of their starting serum level (C_0, their own first measurement).
    for name in ["Cbgd_in_gm", "Cbgd_in_gsd", "C_0_in_gm", "C_0_in_gsd"]:
        row[name] = float(re.search(rf"{name}\s*=\s*({NUM})", code).group(1))

    # Water exposure comes in three flavours, and which one decides how
    # model.py predicts this person's blood level.
    doses = re.search(r"DWC_t\s*=\s*NDoses\((.*?)\)", code, re.S)
    const = re.search(rf"DWC\s*=\s*({NUM})\s*;", code)
    if doses:                                   # time-varying water concentration
        # NDoses(n, c1..cn, t1..tn): a count, then n concentrations, then
        # the n times they started. A step function over the person's life.
        n, *rest = numbers(doses.group(1))
        row["dose_conc"], row["dose_times"] = rest[:int(n)], rest[int(n):]
    elif const:                                 # known constant water concentration
        row["dwc"] = float(const.group(1))
    # otherwise DWC = PerDose(DWC_belowMRL, ...): an unknown value below the MRL
    # (the water test could not resolve it). Left absent here; model.py then
    # fits it as a free parameter bounded by that study's MRL.

    # Data() holds the measured concentrations, Print() the times they were
    # taken. For a single steady-state record the "time" is a placeholder
    # (1e-6, since MCSim needs t > 0) or the years since the water was cleaned up.
    endpoint, data = re.search(r"Data\s*\(\s*(\w+)\s*,([^)]*)\)", code).groups()
    row["endpoint"] = endpoint      # Cserum, Cserum_t, Cbgd_Css, M_Cserum, M_Cbgd_Css
    row["values"] = numbers(data)
    row["times"] = numbers(re.search(r"Print\s*\(\s*\w+\s*,([^)]*)\)", code).group(1))
    return row


def load(chem):
    """Return one row per training Simulation block.

    Walks the file line by line keeping two things in step:
      depth   - current brace nesting depth
      levels  - the stack of Levels currently open, each remembering its
                label, the depth it opened at, whether a Likelihood() has
                been seen inside it, and any MRL it declared
    """
    raw = FILES[chem].read_text().split("\n")
    lines = [l.split("#")[0] for l in raw]      # same lines, comments removed
    levels = []   # stack of open Levels: {"label", "depth", "fit", "mrl"}
    rows = []
    depth, i = 0, 0

    while i < len(lines):
        code = lines[i]
        if re.match(r"\s*Simulation\s*\{", code):
            # Slurp the whole block. A Simulation can span many lines, so
            # read until the braces balance rather than assuming a shape.
            block, d = [], 0
            while True:                         # collect lines until braces balance
                block.append(lines[i])
                d += lines[i].count("{") - lines[i].count("}")
                i += 1
                if d == 0:
                    break
            # Keep it only if some enclosing Level declared a Likelihood,
            # i.e. this record is training data. Everything else is Chiu's
            # held-out test set and must not enter the fit.
            if any(lv["fit"] for lv in levels):
                row = parse_simulation("\n".join(block))
                # Levels: [0] population, [1] "Studies", [2] one study.
                # MCSim gives each child of "Studies" its own background scale,
                # so levels[2] is the study a row belongs to.
                row["study"] = levels[2]["label"]
                # The MRL is declared on a Level and applies to everything
                # inside it, so take the innermost one that has one.
                row["mrl"] = next((lv["mrl"] for lv in reversed(levels) if lv["mrl"]), None)
                rows.append(row)
            continue        # `i` already advanced past the block

        if re.match(r"\s*Level\s*\{", code):
            # The label is the trailing comment, which is how the towns are
            # named. Read it from `raw` (comments intact), not `code`.
            label = raw[i].split("#", 1)[1].strip()[:40] if "#" in raw[i] else ""
            levels.append({"label": label, "depth": depth + 1, "fit": False, "mrl": None})
        if re.search(r"Likelihood\s*\(", code):
            # Marks the innermost open Level as fitted. Every
            # Simulation inside it, however deeply nested, is training data.
            levels[-1]["fit"] = True
        m = re.search(rf"Distrib\s*\(\s*DWC_belowMRL\s*,\s*Uniform\s*,\s*{NUM}\s*,\s*({NUM})", code)
        if m:
            # Uniform(0, MRL) prior on an unmeasurable water concentration;
            # keep the upper bound so model.py can rebuild that prior.
            levels[-1]["mrl"] = float(m.group(1))

        depth += code.count("{") - code.count("}")
        levels = [lv for lv in levels if lv["depth"] <= depth]   # close finished Levels
        i += 1

    return pd.DataFrame(rows)


if __name__ == "__main__":
    # Run directly to see what was picked up: training records per study and
    # endpoint. Handy for checking the parse before trusting a fit.
    for chem in sys.argv[1:] or FILES:
        df = load(chem)
        print(f"\n{chem}: {len(df)} training records")
        print(df.groupby(["study", "endpoint"], sort=False).size().to_string())
