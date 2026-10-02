#!/usr/bin/env python3
"""Build the PFAS x species x parameter coverage matrix.

The question is not "what is the half-life of PFAS" but "for which compound, in
which species, has anyone actually measured anything". This script merges every
toxicokinetic extraction in db/ and answers that, including the negative half:
which combinations have no data at all.

Sources merged:
  animal_halflife_measured.csv  measured animal half-lives
  vd_clearance.csv              Vd and clearance, flagged measured/fitted/assumed
  human_halflife_extended.csv   human estimates
  compiled_tk_parameters.csv    EPA httk, Zurlinden 2025 CPHEA, Dourson 2025
  dose_dependence.csv           multi-dose studies
  master_exposure_halflife.csv  the EPA CPHEA population fits

Counting rule: a combination "has data" when at least one row carries a non-empty
value for that parameter. Studies are counted distinctly, because a single study
contributing twenty rows is still one study - and the review has already been
caught out once by a headline ratio resting on a single mouse study.
"""
import csv
import re
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
DB = HERE.parent / "db"

# ---- canonical chemical names ------------------------------------------
# Maps the spellings actually present across the source files onto one label.
CHEM_ALIAS = {
    "pfuda": "PFUnDA", "pfunda": "PFUnDA", "pfundoa": "PFUnDA",
    "pfdoa": "PFDoDA", "pfdoda": "PFDoDA",
    "hfpo-da (genx)": "HFPO-DA", "hfpo-da": "HFPO-DA", "genx": "HFPO-DA",
    "6:2 cl-pfesa (f-53b)": "6:2 Cl-PFESA", "f-53b": "6:2 Cl-PFESA",
    "dona": "ADONA", "adona": "ADONA",
    "pfoa (as 8:2-ftoh metabolite)": "PFOA",
    "cc6o4 (perfluoro-dioxolane pfoa replacement)": "cC6O4",
    "5:3 fluorotelomer acid": "5:3 FTCA",
}
# Rows naming several compounds at once cannot be attributed to one of them.
MULTI = re.compile(r"\band\b|,|multiple|^all$|short-chain|menstrual")

# ---- canonical species -------------------------------------------------
SPECIES_PATTERNS = [
    (r"human", "human"),
    (r"monkey|primate|macaque|cynomolgus|rhesus", "monkey"),
    (r"\brat\b", "rat"),
    (r"mouse|mice", "mouse"),
    (r"pig|swine|cow|cattle|sheep|dog|rabbit|chicken|fish|trout|zebrafish",
     "other"),
]

# ---- canonical parameters ---------------------------------------------
PARAM_PATTERNS = [
    (r"half[- ]?life|t1/?2|^hl$", "half-life"),
    (r"clearance|^cl\b|clint", "clearance"),
    (r"volume of distribution|^vd\b|vdss|vss", "Vd"),
    (r"elimination rate|rate constant|kelim|^k$|^ke\b", "k"),
]
PARAMS = ["half-life", "clearance", "Vd", "k"]


def norm_chem(s):
    if not s:
        return None
    t = s.strip()
    if MULTI.search(t.lower()):
        return None
    return CHEM_ALIAS.get(t.lower(), t)


def norm_species(s, default=None):
    t = (s or "").strip().lower()
    if not t:
        return default
    # A row covering several species cannot be attributed to one.
    if t.count(",") >= 1 or " and " in t:
        return None
    for pat, name in SPECIES_PATTERNS:
        if re.search(pat, t):
            return name
    return "other"


def norm_param(s):
    t = (s or "").strip().lower()
    for pat, name in PARAM_PATTERNS:
        if re.search(pat, t):
            return name
    return None


def norm_sex(s):
    t = (s or "").strip().lower()
    if t.startswith("m") and not t.startswith("mix"):
        return "M"
    if t.startswith("f"):
        return "F"
    return "U"


def read(name):
    p = DB / name
    return list(csv.DictReader(p.open())) if p.exists() else []


def main() -> None:
    # (chemical, species, parameter) -> {"studies": set, "sexes": set, "rows": n}
    cov = defaultdict(lambda: {"studies": set(), "sexes": set(), "rows": 0,
                               "measured": 0, "modelled": 0})

    def add(chem, species, param, study, sex, measured=True):
        if not (chem and species and param):
            return
        e = cov[(chem, species, param)]
        e["rows"] += 1
        e["sexes"].add(norm_sex(sex))
        if study:
            e["studies"].add(study.strip())
        if measured:
            e["measured"] += 1
        else:
            e["modelled"] += 1

    # animal measured half-lives, plus their Vd and clearance columns
    for r in read("animal_halflife_measured.csv"):
        chem, sp = norm_chem(r["chemical"]), norm_species(r["species"])
        study = f"{r['study']} {r['year']}"
        # Rows the extractor marked as modelled are counted separately.
        is_meas = "modelled" not in (r.get("model", "") + r.get("source_table", "")).lower()
        for col, param in (("halflife", "half-life"), ("vd", "Vd"),
                           ("clearance", "clearance")):
            if r.get(col, "").strip():
                add(chem, sp, param, study, r.get("sex"), is_meas)

    # Vd / clearance / half-life extraction
    for r in read("vd_clearance.csv"):
        chem, sp = norm_chem(r["chemical"]), norm_species(r["species"])
        study = f"{r['study']} {r['year']}"
        meas = "assumed" not in r.get("vd_method_measured_fitted_assumed", "").lower()
        for col, param in (("vd", "Vd"), ("clearance", "clearance"),
                           ("halflife", "half-life")):
            if r.get(col, "").strip():
                add(chem, sp, param, study, r.get("sex"), meas)

    # human estimates
    for r in read("human_halflife_extended.csv"):
        chem = norm_chem(r["chemical"])
        study = f"{r['study']} {r['year']}"
        if r.get("halflife_y", "").strip():
            add(chem, "human", "half-life", study, r.get("sex"))
        if r.get("vd_L_kg", "").strip():
            meas = "assumed" not in r.get("vd_assumed_or_fitted", "").lower()
            add(chem, "human", "Vd", study, r.get("sex"), meas)

    # compiled datasets (httk, Zurlinden CPHEA, Dourson)
    for r in read("compiled_tk_parameters.csv"):
        chem = norm_chem(r["chemical"])
        sp = norm_species(r["species"])
        param = norm_param(r["parameter"])
        if r.get("value", "").strip():
            add(chem, sp, param, r["dataset_name"], r.get("sex"), measured=False)

    # multi-dose studies contribute half-life and clearance
    for r in read("dose_dependence.csv"):
        chem, sp = norm_chem(r["chemical"]), norm_species(r["species"])
        study = f"{r['study']} {r['year']}"
        if r.get("halflife_at_low_dose", "").strip():
            add(chem, sp, "half-life", study, r.get("sex"))
        if r.get("clearance_low", "").strip():
            add(chem, sp, "clearance", study, r.get("sex"))

    # the EPA population fits
    for r in read("master_exposure_halflife.csv"):
        chem, sp = norm_chem(r["chemical"]), norm_species(r["species"])
        study = "EPA CPHEA population fit"
        for col, param in (("halflife_d", "half-life"), ("vd_L_kg", "Vd"),
                           ("clearance_native", "clearance")):
            if r.get(col, "").strip():
                add(chem, sp, param, study, r.get("sex"), measured=False)

    chems = sorted({k[0] for k in cov})
    species = ["human", "monkey", "rat", "mouse", "other"]

    # ---- the matrix ----------------------------------------------------
    print("PFAS TOXICOKINETIC COVERAGE MATRIX")
    print("cell = number of distinct studies; '-' = no data found\n")
    for param in PARAMS:
        print(f"=== {param} ===")
        print(f"  {'chemical':<14}" + "".join(f"{s:>9}" for s in species))
        print("  " + "-" * (14 + 9 * len(species)))
        for c in chems:
            cells = []
            for s in species:
                e = cov.get((c, s, param))
                cells.append(f"{len(e['studies']):>9}" if e else f"{'-':>9}")
            if any(x.strip() != "-" for x in cells):
                print(f"  {c:<14}" + "".join(cells))
        print()

    # ---- long form + explicit gaps --------------------------------------
    rows, gaps = [], []
    for c in chems:
        for s in species:
            for param in PARAMS:
                e = cov.get((c, s, param))
                n = len(e["studies"]) if e else 0
                status = ("no_data" if n == 0 else
                          "single_study_only" if n == 1 else "has_data")
                rec = {
                    "chemical": c, "species": s, "parameter": param,
                    "status": status, "n_studies": n,
                    "n_rows": e["rows"] if e else 0,
                    "sexes_covered": "".join(sorted(e["sexes"])) if e else "",
                    "n_measured_rows": e["measured"] if e else 0,
                    "n_modelled_rows": e["modelled"] if e else 0,
                    "studies": "; ".join(sorted(e["studies"])[:6]) if e else "",
                }
                rows.append(rec)
                if status != "has_data" and s != "other":
                    gaps.append(rec)

    with (DB / "coverage_matrix.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print("SUMMARY")
    tot = len(chems) * 4 * 4           # chemicals x 4 core species x 4 params
    have = sum(1 for r in rows if r["status"] == "has_data"
               and r["species"] != "other")
    one = sum(1 for r in rows if r["status"] == "single_study_only"
              and r["species"] != "other")
    none = sum(1 for r in rows if r["status"] == "no_data"
               and r["species"] != "other")
    print(f"  {len(chems)} chemicals x 4 species x 4 parameters = {tot} cells")
    print(f"    {have:>4} have two or more studies   ({have/tot*100:.0f}%)")
    print(f"    {one:>4} rest on a SINGLE study     ({one/tot*100:.0f}%)")
    print(f"    {none:>4} have no data at all        ({none/tot*100:.0f}%)")

    print("\n  Best-covered chemicals (cells with any data, out of 16):")
    for c in chems:
        n = sum(1 for r in rows if r["chemical"] == c and r["species"] != "other"
                and r["status"] != "no_data")
        if n:
            print(f"    {c:<14} {n:>2}/16")

    print(f"\nwrote {DB/'coverage_matrix.csv'}  ({len(rows)} cells, "
          f"{len(gaps)} of them gaps)")


if __name__ == "__main__":
    main()
