"""
parse_chiu_data.py
===================

WHAT THIS FILE IS FOR
----------------------
Chiu et al. 2022 (the paper we are replicating) fit their toxicokinetic
models using a program called MCSim, not Python. MCSim is configured with
a domain-specific language written in plain text files ending in ".in.R"
(they look like R, but they are actually MCSim's own syntax, not real R
code). Those ".in.R" files are the ONLY place that specifies:

  - which human study each data point came from (e.g. "Decatur, WV" or
    "Arnsberg, Germany")
  - what was actually measured (a person's blood-serum concentration over
    time, or a population's mean steady-state concentration)
  - the drinking-water concentration (DWC) each person/population was
    exposed to, which is what drives the model's prediction
  - whether a given data point was actually used to fit the model
    ("training" data) or only used to generate a validation plot after
    fitting ("test" data, technically: not accompanied by a Likelihood())

This file reads one of those ".in.R" files and turns it into a normal
pandas DataFrame, one row per data point, with a validation step so we
are not trusting a regex parser blindly.

WHY THIS IS TRICKIER THAN IT SOUNDS
-------------------------------------
MCSim's file format nests curly-brace blocks: a top-level "Level { }"
represents one study/site, and inside it "Simulation { }" blocks each
describe one person or one population summary. A "Likelihood(var, ...)"
call declared inside a Level applies to every Simulation block inside
that Level (and any Levels nested inside it) -- so whether a data point
actually influenced the fitted parameters depends on which Level it sits
inside, not on anything printed on the Simulation block itself. Some
Levels are commented as "Test set" in English, but not all of them are
(one is only commented "41 Males; 69 Females has individual data" with
no obvious "test" or "train" keyword at all) -- so we track the REAL
brace-nesting and Likelihood() scope directly, instead of guessing from
comment text.

HOW TO USE THIS FILE
----------------------
You will not usually run this file directly. The four model_*.py scripts
each import `build_dataframe` from here and call it once at the top:

    from parse_chiu_data import build_dataframe
    df, raw_text = build_dataframe("PFOA")

But you CAN run it directly to see the parsed+validated table for
yourself, chemical by chemical:

    python parse_chiu_data.py PFOA
    python parse_chiu_data.py PFOS
    python parse_chiu_data.py PFNA
    python parse_chiu_data.py PFHxS
    python parse_chiu_data.py all      # parses + validates all four
"""

import re
import sys
from pathlib import Path
import pandas as pd

# The four ".in.R" files this script reads live in the data/ folder next
# to this script (they were copied straight out of Chiu et al.'s own
# public GitHub repository -- we did not modify their contents at all).
DATA_DIR = Path(__file__).parent / "data"

# The four chemical folders in Chiu's repo don't share one filename
# convention (capital vs lowercase ".r", different suffixes), so we look
# each one up explicitly instead of guessing a pattern.
IN_FILES = {
    "PFOA": DATA_DIR / "PFOA_1cpt_v8.MCMC_TrainTest.in.R",
    "PFOS": DATA_DIR / "PFOS_1cpt_v8.PopMCMC_MeanIndivTrainTest.in.R",
    "PFNA": DATA_DIR / "PFNA_1cpt_v8.PopMCMC_MeanIndivTrainTest.in.R",
    "PFHxS": DATA_DIR / "PFHxS_1cpt_v8.PopMCMC_MeanIndivTrainTest.in.r",
}


def find_simulation_blocks(text: str):
    """
    Walk the raw text of an ".in.R" file line by line, tracking brace
    depth, and maintain TWO parallel stacks as we go:

      - study_stack:       which named Level (= which human study/site)
                            the current position is nested inside
      - likelihood_stack:  which Likelihood(variable_name, ...) call is
                            currently "in force" at the current position

    Why the second stack matters: there are only 7 Likelihood() calls in
    the whole PFOA file (which is ~6300 lines long), one per Level that
    actually gets fit. A Level with no Likelihood() of its own (every
    "held-out" / validation block) still runs Print()/Data() to generate
    a predicted value for a plot, but that predicted value never
    influences the posterior distribution -- it is purely a "here's what
    the fitted model predicts for this person we didn't train on" check.

    Returns a list of tuples, one per Simulation{} block found:
        (study_name, sim_label, block_text, start_line, fit_likelihood_var)
    where `fit_likelihood_var` is the name of the variable this block's
    data is being fit against (e.g. "Cserum"), or None if this block sits
    outside any Likelihood()'s scope (i.e. it is held-out/validation-only).
    """
    lines = text.split("\n")
    depth = 0
    study_stack = []       # list of (depth_at_open, label)
    likelihood_stack = []  # list of (depth_at_open, likelihood_variable_name)
    i, n = 0, len(lines)
    results = []

    level_re = re.compile(r"^\s*Level\s*\{\s*(#\s*(.*))?")
    sim_re = re.compile(r"^\s*Simulation\s*\{\s*(#\s*(.*))?")
    likelihood_re = re.compile(r"^\s*Likelihood\s*\(\s*(\w+)")

    while i < n:
        line = lines[i]

        # Case 1: this line opens a Simulation{} block (one person or one
        # population-summary data point). Slurp the whole block (it may
        # span many lines) by counting braces until it balances back to 0.
        m_sim = sim_re.match(line)
        if m_sim:
            sim_label = (m_sim.group(2) or "").strip() or None
            block_depth = line.count("{") - line.count("}")
            block_lines = [line]
            j = i + 1
            while block_depth > 0 and j < n:
                block_lines.append(lines[j])
                block_depth += lines[j].count("{") - lines[j].count("}")
                j += 1
            block_text = "\n".join(block_lines)

            # Record which study and which Likelihood() (if any) currently
            # apply, based on the stacks as they stand right now.
            current_study = study_stack[-1][1] if study_stack else None
            fit_likelihood_var = likelihood_stack[-1][1] if likelihood_stack else None
            results.append((current_study, sim_label, block_text, i + 1, fit_likelihood_var))

            # Advance depth past this whole block, and pop any stack
            # entries that belonged to a scope we've now closed.
            depth += block_text.count("{") - block_text.count("}")
            while study_stack and study_stack[-1][0] > depth:
                study_stack.pop()
            while likelihood_stack and likelihood_stack[-1][0] > depth:
                likelihood_stack.pop()
            i = j
            continue

        # Case 2: this line opens a new Level{} (= a new study/site scope).
        m_level = level_re.match(line)
        if m_level:
            label = (m_level.group(2) or "").strip() or None
            depth += line.count("{") - line.count("}")
            study_stack.append((depth, label))
            i += 1
            continue

        # Case 3: this line declares a Likelihood(variable, ...) -- from
        # here until the CURRENT (already-open) Level closes, every
        # Simulation{} block we see is being fit against `variable`.
        m_lik = likelihood_re.match(line)
        if m_lik:
            likelihood_stack.append((depth, m_lik.group(1)))
            i += 1
            continue

        # Case 4: an ordinary line -- just track brace depth and pop any
        # scopes that have now closed.
        depth += line.count("{") - line.count("}")
        while study_stack and study_stack[-1][0] > depth:
            study_stack.pop()
        while likelihood_stack and likelihood_stack[-1][0] > depth:
            likelihood_stack.pop()
        i += 1

    return results


def parse_numbers(s: str):
    """Pull every number (int, float, or scientific notation) out of a string, in order."""
    s = s.replace("\n", " ")
    return [float(x) for x in re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", s)]


def find_mrl_declarations(text: str):
    """
    Some people's exposure was "below the method reporting limit" (MRL) --
    i.e. all we know is their drinking-water concentration (DWC) was
    somewhere between 0 and some small known MRL value. MCSim represents
    this as a free parameter with a uniform prior:

        Distrib(DWC_belowMRL, Uniform, 0, <MRL value>)

    NOTE: this is NOT the same as the nearby `PerDose(DWC_belowMRL, ...)`
    call -- PerDose's arguments are (magnitude_variable, dosing_period,
    exposure_duration, start_time), and none of those numbers is the MRL.
    The actual MRL bound only appears in this separate Distrib() line,
    declared once per study earlier in the same Level{} block, so we have
    to look it up by proximity rather than reading it off PerDose().
    """
    decls = []
    for m in re.finditer(r"Distrib\s*\(\s*DWC_belowMRL\s*,\s*Uniform\s*,\s*[-+0-9.eE]+\s*,\s*([-+0-9.eE]+)\s*\)",
                          text):
        line_no = text[: m.start()].count("\n") + 1
        decls.append((line_no, float(m.group(1))))
    return decls


def lookup_mrl(mrl_decls, start_line):
    """The nearest PRECEDING Distrib(DWC_belowMRL,...) declaration, by line number."""
    candidates = [v for ln, v in mrl_decls if ln <= start_line]
    return candidates[-1] if candidates else None


def parse_block(study, sim_label, block, start_line, mrl_decls, fit_likelihood_var):
    """Turn one Simulation{} block's raw text into a dict of structured fields."""
    row = {
        "study": study,
        "sim_label": sim_label,
        "start_line": start_line,
        # THE single most important flag in this whole file: does this
        # row sit inside a Level that declared a Likelihood(), i.e. does
        # it actually influence the posterior at all? If False, it is a
        # held-out data point used only to make a validation plot.
        "fit_likelihood_var": fit_likelihood_var,
        "in_fit": fit_likelihood_var is not None,
        # A rough human-readable label ONLY -- never used for any modeling
        # decision, because it is unreliable (see the module docstring).
        "label_says": "test" if study and re.search(r"\bTEST\b", study, re.I) else
                       ("train" if study and re.search(r"\bTRAIN(ing)?\b", study, re.I) else "unlabeled"),
    }

    # Background (Cbgd) and starting-concentration (C_0) priors for this
    # person: geometric mean (gm) and geometric standard deviation (gsd)
    # of a lognormal distribution.
    for field in ["Cbgd_in_gm", "Cbgd_in_gsd", "C_0_in_gm", "C_0_in_gsd"]:
        m = re.search(rf"{field}\s*=\s*([-+0-9.eE]+)\s*;", block)
        row[field] = float(m.group(1)) if m else None

    # Drinking-water concentration (DWC) can be specified three different
    # ways depending on the person/study -- figure out which one applies:
    m_dwc = re.search(r"DWC\s*=\s*PerDose\(([^)]*)\)", block)         # below-MRL (free param)
    m_dwc_const = re.search(r"DWC\s*=\s*([-+0-9.eE]+)\s*;", block)     # fixed known value
    m_dwc_t = re.search(r"DWC_t\s*=\s*NDoses\((.*?)\)\s*;", block, re.DOTALL)  # time-varying history

    if m_dwc_t:
        nums = parse_numbers(m_dwc_t.group(1))
        n_doses = int(nums[0])
        row["dwc_type"] = "time_varying"
        row["dwc_n"] = n_doses
        row["dwc_conc"] = nums[1: 1 + n_doses]
        row["dwc_times"] = nums[1 + n_doses: 1 + 2 * n_doses]
    elif m_dwc:
        row["dwc_type"] = "below_MRL"
        row["dwc_mrl"] = lookup_mrl(mrl_decls, start_line)
    elif m_dwc_const:
        row["dwc_type"] = "constant"
        row["dwc_value"] = float(m_dwc_const.group(1))
    else:
        row["dwc_type"] = "MISSING"   # flagged explicitly rather than silently left blank

    # Data(variable, values...) is the actual OBSERVED measurement(s).
    # Print(variable, times...) is the list of times those measurements
    # were taken at (or, for a population summary, just one "time" that
    # is really a study-duration marker).
    m_data = re.search(r"Data\s*\(\s*(\w+)\s*,\s*([^)]*)\)", block)
    m_print = re.search(r"Print\s*\(\s*(\w+)\s*,\s*([^)]*)\)", block)
    row["endpoint"] = m_data.group(1) if m_data else "MISSING"
    row["data_values"] = parse_numbers(m_data.group(2)) if m_data else []
    row["print_times"] = parse_numbers(m_print.group(2)) if m_print else []
    row["print_endpoint"] = m_print.group(1) if m_print else "MISSING"

    return row


def build_dataframe(chem: str):
    """
    Parse one chemical's ".in.R" file into a pandas DataFrame, one row
    per Simulation{} block (= one person, or one population-summary data
    point). Returns (dataframe, raw_file_text) -- the raw text is handed
    back too so validate() can double-check the parse against it.
    """
    in_file = IN_FILES[chem]
    text = in_file.read_text()
    blocks = find_simulation_blocks(text)
    mrl_decls = find_mrl_declarations(text)
    rows = [parse_block(study, label, block, line, mrl_decls, fit_var)
            for study, label, block, line, fit_var in blocks]
    df = pd.DataFrame(rows)
    df.insert(0, "chemical", chem)
    return df, text


def validate(chem: str, df, raw_text: str):
    """
    Sanity-check the parsed table against the raw text and against
    itself. Returns a list of problem strings -- an empty list means
    every check passed. Read this function if you want to know exactly
    what "trustworthy" means here; nothing is asserted blindly.
    """
    problems = []

    # 1. Did we find every Simulation{} block that the raw text actually has?
    raw_count = len(re.findall(r"Simulation\s*\{", raw_text))
    if raw_count != len(df):
        problems.append(f"Block count mismatch: found {len(df)} parsed rows but "
                         f"{raw_count} 'Simulation {{' occurrences in raw text")

    # 2. The variable named in Data(...) should match the variable named
    #    in Print(...) for the same block (they describe the same quantity).
    mismatch = df[(df["endpoint"] != df["print_endpoint"]) & (df["print_endpoint"] != "MISSING")]
    if len(mismatch):
        problems.append(f"{len(mismatch)} rows where Data() and Print() reference different variables")

    # 3. No block should be missing an endpoint or an exposure specification.
    missing_endpoint = df[df["endpoint"] == "MISSING"]
    if len(missing_endpoint):
        problems.append(f"{len(missing_endpoint)} rows with no Data(...) call found at all")

    missing_dwc = df[df["dwc_type"] == "MISSING"]
    if len(missing_dwc):
        problems.append(f"{len(missing_dwc)} rows with no DWC/DWC_t exposure found at all")

    # 4. For every row we're claiming IS in the fit, the Likelihood()
    #    variable it inherited should match its own Data() variable. If it
    #    doesn't, the brace/scope tracker latched onto the wrong Likelihood().
    in_fit = df[df["in_fit"]]
    lik_mismatch = in_fit[in_fit["fit_likelihood_var"] != in_fit["endpoint"]]
    if len(lik_mismatch):
        problems.append(f"{len(lik_mismatch)} in_fit rows where inherited Likelihood() variable "
                         f"doesn't match this row's own Data() variable -- scope tracking may be wrong")

    # 5. Every below_MRL row must have resolved to some MRL value, and a
    #    single chemical file should never mix more than one MRL value
    #    (if it does, our line-proximity lookup is probably wrong).
    below_mrl = df[df["dwc_type"] == "below_MRL"]
    if len(below_mrl):
        unresolved_mrl = below_mrl[below_mrl["dwc_mrl"].isna()]
        if len(unresolved_mrl):
            problems.append(f"{len(unresolved_mrl)} below_MRL rows with NO preceding "
                             f"Distrib(DWC_belowMRL,...) declaration found -- MRL unresolved")
        distinct_mrls = below_mrl["dwc_mrl"].dropna().unique()
        if len(distinct_mrls) > 1:
            problems.append(f"below_MRL rows resolve to {len(distinct_mrls)} different MRL values "
                             f"{sorted(distinct_mrls)} -- verify line-proximity lookup matches true Level scope")

    # 6. Time-varying dose histories: concentration list, time list, and
    #    declared count should all agree in length.
    tv = df[df["dwc_type"] == "time_varying"]
    bad_tv = tv[tv.apply(lambda r: not (len(r["dwc_conc"]) == len(r["dwc_times"]) == r["dwc_n"]), axis=1)]
    if len(bad_tv):
        problems.append(f"{len(bad_tv)} time-varying rows where dose/time list lengths don't match declared dwc_n")

    # 7. Observed values and query times should line up one-to-one.
    has_both = df[(df["data_values"].apply(len) > 0) & (df["print_times"].apply(len) > 0)]
    bad_len = has_both[has_both.apply(lambda r: len(r["data_values"]) != len(r["print_times"]), axis=1)]
    if len(bad_len):
        problems.append(f"{len(bad_len)} rows where len(data_values) != len(print_times)")

    return problems


if __name__ == "__main__":
    chems = list(IN_FILES) if (len(sys.argv) < 2 or sys.argv[1] == "all") else [sys.argv[1]]

    all_dfs = []
    for chem in chems:
        print(f"\n{'='*70}\n{chem}  ({IN_FILES[chem].name})\n{'='*70}")
        df, raw_text = build_dataframe(chem)
        problems = validate(chem, df, raw_text)

        print(f"Parsed {len(df)} Simulation blocks")
        print("Endpoint counts, split by whether they actually feed the likelihood (in_fit):")
        print(df.groupby(["endpoint", "in_fit"]).size().to_string())
        print("Exposure type counts:")
        print(df["dwc_type"].value_counts().to_string())
        print(f"Total rows contributing to the posterior (in_fit=True): {df['in_fit'].sum()} / {len(df)}")

        if problems:
            print("\n*** VALIDATION PROBLEMS ***")
            for p in problems:
                print(f"  - {p}")
        else:
            print("\nValidation: CLEAN (all checks passed)")

        all_dfs.append(df)

    combined = pd.concat(all_dfs, ignore_index=True)
    out_csv = Path(__file__).parent / "data" / "chiu_all_chemicals_parsed.csv"
    df_out = combined.copy()
    # (some single-chemical runs never have a time-varying dose history,
    # so "dwc_conc"/"dwc_times" may not exist as columns at all -- only
    # stringify list-valued columns that are actually present)
    for col in ["dwc_conc", "dwc_times", "data_values", "print_times"]:
        if col in df_out.columns:
            df_out[col] = df_out[col].apply(lambda v: str(v) if isinstance(v, list) else v)
    df_out.to_csv(out_csv, index=False)
    print(f"\n\nSaved combined table ({len(combined)} rows, all chemicals) to {out_csv}")
