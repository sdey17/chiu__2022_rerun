#!/usr/bin/env python3
"""Fit terminal elimination half-lives directly from the EPA CPHEA
observation-level PFAS concentration-time data.

Why bother, when fitted half-lives already exist. The review has been using the
EPA population-model composites (ln2 x Vd,ss / CL), and a sex ratio derived that
way for rat PFOA gives about 20x while the primary studies report 8.5-72x. A
composite can differ from a directly fitted terminal slope for real reasons - it
borrows strength across doses and routes, and it is a ratio of posterior means
rather than the mean of a ratio. Fitting the raw curves says which number the
underlying data actually support.

Method. Within each (study, chemical, species, strain, sex, dose, route, matrix)
group, replicate observations are averaged per time point to give one curve.
The terminal phase is then chosen the way non-compartmental analysis normally
does it: fit log(concentration) on time for the last n points, for every n from
3 up to the number of post-peak points, and keep the n with the best adjusted
R-squared among fits with a negative slope. Half-life is ln2 divided by the
magnitude of that slope.

Concentration units cancel in a slope, so the mixed units in the source are
harmless; time is normalised to hours.

Input:  papers/CPHEA-Animal-PFAS-PK extracted_data/*.csv  (7,962 rows, 20 studies)
Output: db/cphea_fitted_halflives.csv

NOTE: this window rule has a known failure mode -- on a biphasic curve the most
log-linear segment is the shallow terminal tail, not the dominant elimination
phase that a published half-life describes. See report section 8 item 9. After
re-running this script, re-run `validate_cphea_fits.py --write` to restore the
`tail_selection_flag` column, which this script does not emit.
"""
import csv
import glob
import math
import os
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RAW = ROOT / "papers" / "CPHEA-Animal-PFAS-PK extracted_data"
MASTER = ROOT / "papers" / "CPHEA-Animal-PFAS-PK pfas_master.csv"
OUT = ROOT / "db" / "cphea_fitted_halflives.csv"

TIME_TO_H = {"hour": 1.0, "day": 24.0, "minute": 1 / 60, "week": 168.0}
PLASMA = {"plasma", "serum"}
MIN_POINTS = 3

# EPA population-fit composites currently used in the review, days.
EPA_COMPOSITE = {
    ("PFOA", "rat"): (14.200, 0.690), ("PFOA", "mouse"): (25.630, 21.453),
    ("PFOS", "rat"): (57.075, 54.734), ("PFOS", "mouse"): (35.491, 32.810),
    ("PFHxS", "rat"): (29.713, 1.744), ("PFHxS", "mouse"): (27.397, 26.665),
    ("PFNA", "rat"): (53.722, 2.831), ("PFNA", "mouse"): (227.460, 59.439),
    ("PFBA", "rat"): (0.348, 0.098), ("PFBA", "mouse"): (0.724, 0.186),
    ("PFBS", "rat"): (0.120, 0.041), ("PFBS", "mouse"): (0.186, 0.125),
    ("PFHxA", "rat"): (0.095, 0.034), ("PFHxA", "mouse"): (0.215, 0.251),
}


def fnum(x):
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    return None if v <= -1 else v


def ols(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((a - mx) ** 2 for a in xs)
    if sxx == 0:
        return None, None
    slope = sum((a - mx) * (b - my) for a, b in zip(xs, ys)) / sxx
    inter = my - slope * mx
    ss_res = sum((b - (inter + slope * a)) ** 2 for a, b in zip(xs, ys))
    ss_tot = sum((b - my) ** 2 for b in ys)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return slope, r2


def terminal_fit(curve):
    """curve: sorted [(t_hours, conc)]. Returns (halflife_h, n_used, r2, adj_r2)."""
    pts = [(t, c) for t, c in curve if c and c > 0]
    if len(pts) < MIN_POINTS:
        return None
    peak = max(range(len(pts)), key=lambda i: pts[i][1])
    post = pts[peak:]
    if len(post) < MIN_POINTS:
        post = pts[-MIN_POINTS:] if len(pts) >= MIN_POINTS else pts
    best = None
    for n in range(MIN_POINTS, len(post) + 1):
        seg = post[-n:]
        xs = [t for t, _ in seg]
        ys = [math.log(c) for _, c in seg]
        slope, r2 = ols(xs, ys)
        if slope is None or slope >= 0:
            continue
        adj = 1 - (1 - r2) * (n - 1) / (n - 2) if n > 2 else r2
        if best is None or adj > best[3]:
            best = (math.log(2) / abs(slope), n, r2, adj)
    return best


def main() -> None:
    chem_of = {}
    if MASTER.exists():
        for r in csv.DictReader(MASTER.open()):
            chem_of[r["dtxsid"]] = r["pfas_abbrev"]

    groups = defaultdict(lambda: defaultdict(list))
    meta = {}
    for f in sorted(glob.glob(str(RAW / "*.csv"))):
        study = os.path.basename(f).replace(".csv", "")
        for r in csv.DictReader(open(f)):
            if r["matrix"] not in PLASMA:
                continue
            if r["conc_units"] == "perc_dose":
                continue
            t, c = fnum(r["time"]), fnum(r["conc_mean"])
            scale = TIME_TO_H.get(r["time_units"])
            if t is None or c is None or c <= 0 or scale is None:
                continue
            chem = chem_of.get(r["dtxsid"], r["dtxsid"])
            key = (study, chem, r["species"], r["strain"], r["sex"],
                   r["dose"], r["dose_units"], r["route"].lower(), r["matrix"])
            groups[key][t * scale].append(c)
            meta[key] = r["conc_units"]

    rows = []
    for key, by_time in groups.items():
        curve = sorted((t, sum(v) / len(v)) for t, v in by_time.items())
        fit = terminal_fit(curve)
        if not fit:
            continue
        hl_h, n_used, r2, adj = fit
        study, chem, sp, strain, sex, dose, dunits, route, matrix = key
        rows.append({
            "study": study, "chemical": chem, "species": sp, "strain": strain,
            "sex": sex, "dose": dose, "dose_units": dunits, "route": route,
            "matrix": matrix, "conc_units": meta[key],
            "n_timepoints_total": len(curve), "n_timepoints_in_fit": n_used,
            "halflife_hours": f"{hl_h:.4f}", "halflife_days": f"{hl_h/24:.5f}",
            "r2": f"{r2:.4f}", "adj_r2": f"{adj:.4f}",
            "source": ("EPA CPHEA Animal PFAS PK extracted_data, "
                       "terminal log-linear fit computed here"),
        })

    rows.sort(key=lambda r: (r["chemical"], r["species"], r["sex"],
                             float(r["dose"] or 0)))
    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"fitted {len(rows)} curves from {len(groups)} groups -> {OUT}\n")

    # ---- sex ratios from the raw fits, against the EPA composite ----------
    print("FITTED SEX RATIOS vs THE EPA COMPOSITE (male half-life / female)")
    print("geometric mean over all doses and studies, plasma/serum only\n")
    print(f"{'PFAS':7} {'species':8} {'n(M)':>5} {'n(F)':>5} {'t_M (d)':>9} "
          f"{'t_F (d)':>9} {'fitted M/F':>11} {'EPA M/F':>9}")
    print("-" * 74)
    by = defaultdict(list)
    for r in rows:
        by[(r["chemical"], r["species"], r["sex"])].append(
            float(r["halflife_days"]))

    def gmean(v):
        return math.exp(sum(math.log(x) for x in v) / len(v)) if v else None

    for (chem, sp) in sorted({(k[0], k[1]) for k in by}):
        m = by.get((chem, sp, "Male"), [])
        f = by.get((chem, sp, "Female"), [])
        if not (m and f):
            continue
        gm, gf = gmean(m), gmean(f)
        epa = EPA_COMPOSITE.get((chem, sp))
        epa_s = f"{epa[0]/epa[1]:9.1f}" if epa else f"{'-':>9}"
        print(f"{chem:7} {sp:8} {len(m):5} {len(f):5} {gm:9.3f} {gf:9.3f} "
              f"{gm/gf:10.1f}x {epa_s}")

    print()
    print("NOTE ON COMPARABILITY")
    print("  These are terminal slopes from individual curves, pooled as a")
    print("  geometric mean over dose and study. The EPA composite is")
    print("  ln2 x Vd,ss / CL from a hierarchical fit that borrows strength")
    print("  across doses and routes. They answer slightly different questions,")
    print("  and where they disagree the raw fit is the more direct statement")
    print("  about what was observed.")


if __name__ == "__main__":
    main()
