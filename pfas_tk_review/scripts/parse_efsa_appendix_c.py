#!/usr/bin/env python3
"""Parse EFSA 2020 Appendix C Tables C.2 and C.3 into per-record rows.

EFSA's CONTAM opinion tabulates animal toxicokinetic parameters that are hard to
find elsewhere - in particular Table C.3 carries mouse clearance and volume of
distribution for PFUnDA, PFDoDA, PFTrDA and PFTeDA, long-chain carboxylates with
almost no other in vivo data.

The source is a markdown rendering of the web version, where each table row
packs several records into one cell with <br> separators: one chemical, then a
stack of species/sex entries with matching stacks of route, dose, half-life,
clearance, Vd and reference. This unpacks them by zipping the stacks, and
refuses to guess when the stacks are different lengths.

Source: EFSA CONTAM Panel 2020, EFSA Journal 18(9):6223,
doi:10.2903/j.efsa.2020.6223, Appendix C Tables C.2 and C.3.
"""
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "papers" / "EFSA 2020 CONTAM four PFAS opinion fulltext-from-web.txt"
OUT = ROOT / "db" / "efsa_appendix_c.csv"

TABLES = {"C.2": "Selected TK parameters for PFOS and PFOA in animals",
          "C.3": "Selected TK parameters for PFASs other than PFOS and PFOA"}
LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")        # markdown link -> its text
TAG = re.compile(r"<[^>]+>")


def clean(s):
    s = LINK.sub(r"\1", s)
    s = s.replace("\\", "").replace("_", "")
    s = TAG.sub("", s)
    return re.sub(r"\s+", " ", s).strip()


def split_stack(cell):
    """A cell holds several records separated by <br>."""
    parts = re.split(r"<br\s*/?>", cell)
    return [clean(p) for p in parts]


def find_table(lines, caption):
    """Return the pipe-delimited data rows of the table with this caption."""
    start = None
    for i, ln in enumerate(lines):
        if caption in ln:
            start = i
            break
    if start is None:
        return []
    rows, seen_header = [], False
    for ln in lines[start:start + 400]:
        # Every line in this rendering ends with a literal backslash; strip it
        # before anything else or the separator row never matches.
        ln = ln.rstrip().rstrip("\\").rstrip()
        if not ln.lstrip().startswith("|"):
            if rows:
                break
            continue
        cells = [c for c in ln.strip().strip("|").split("|")]
        if set("".join(cells).strip()) <= set("- :"):
            seen_header = True
            continue
        if not seen_header:
            continue
        rows.append(cells)
    return rows


def main() -> None:
    lines = SRC.read_text(errors="replace").splitlines()
    out, skipped = [], []

    for tbl, caption in TABLES.items():
        for cells in find_table(lines, caption):
            if len(cells) < 8:
                continue
            chem = clean(cells[0])
            stacks = [split_stack(c) for c in cells[1:8]]
            n = max(len(s) for s in stacks)
            # A single-entry column applies to every record in the row.
            norm = []
            for s in stacks:
                if len(s) == 1:
                    norm.append(s * n)
                elif len(s) == n:
                    norm.append(s)
                else:
                    norm.append(None)
            if any(s is None for s in norm):
                # The web-to-markdown rendering dropped some <br> separators:
                # in the PFOS row, one half-life cell merges three values and
                # another repeats one, and two species cells each hold two
                # animals. Aligning 18 half-lives to 20 doses would mean
                # guessing which value belongs to which dose, so these rows are
                # refused rather than reconstructed. PFOS, PFOA and PFBS are
                # covered from primary sources elsewhere in this collection
                # (db/animal_halflife_measured.csv and the CPHEA raw curves);
                # the unique contribution of Appendix C is the long-chain
                # carboxylates, which parse cleanly.
                skipped.append((tbl, chem, [len(s) for s in stacks]))
                continue
            for i in range(n):
                sp, route, dose, hl, cl, vd, ref = (s[i] for s in norm)
                if not (sp or hl or cl or vd):
                    continue
                m = re.match(r"(.+?)\s*\((F|M)\)", sp)
                species = clean(m.group(1)) if m else sp
                sex = {"F": "Female", "M": "Male"}.get(m.group(2)) if m else ""
                out.append({
                    "source_table": f"EFSA 2020 Appendix Table {tbl}",
                    "chemical": chem, "species": species.lower(), "sex": sex,
                    "route": route, "dose_umol_kg": dose,
                    "halflife": hl, "clearance_total_mL_kg_day": cl,
                    "vd_mL_kg": vd, "reference": ref,
                    "source": ("EFSA CONTAM Panel 2020, EFSA Journal 18(9):6223, "
                               "doi:10.2903/j.efsa.2020.6223"),
                })

    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)

    print(f"parsed {len(out)} records -> {OUT}")
    if skipped:
        print(f"\n{len(skipped)} rows REFUSED - the source rendering lost <br> "
              "separators so the\ncolumns cannot be aligned without guessing. "
              "These compounds are covered\nfrom primary sources elsewhere; see "
              "the comment in this script.")
        for t, c, lens in skipped:
            print(f"  {t}  {c[:40]:<40} stack lengths {lens}")

    from collections import Counter
    print("\nby chemical:")
    for c, n in Counter(r["chemical"] for r in out).most_common():
        print(f"  {c:<12} {n:>3}")
    print("\nby species:")
    for c, n in Counter(r["species"] for r in out).most_common():
        print(f"  {c:<12} {n:>3}")

    # The point of the exercise: records carrying a clearance or Vd for a
    # compound the rest of the collection barely covers.
    RARE = {"PFUnDA", "PFDoDA", "PFTrDA", "PFTeDA", "PFHpA", "PFBS", "PFHxS"}
    rare = [r for r in out if r["chemical"] in RARE
            and (r["clearance_total_mL_kg_day"] not in ("", "NR")
                 or r["vd_mL_kg"] not in ("", "NR"))]
    print(f"\nRARE-COMPOUND RECORDS WITH A CLEARANCE OR Vd  ({len(rare)})")
    print(f"  {'chemical':<9} {'species':<8} {'sex':<7} {'route':<6} "
          f"{'CL mL/kg/d':>14} {'Vd mL/kg':>12}")
    print("  " + "-" * 62)
    for r in rare:
        print(f"  {r['chemical']:<9} {r['species']:<8} {r['sex']:<7} "
              f"{r['route']:<6} {r['clearance_total_mL_kg_day'][:14]:>14} "
              f"{r['vd_mL_kg'][:12]:>12}")


if __name__ == "__main__":
    main()
