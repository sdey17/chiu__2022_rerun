#!/usr/bin/env python3
"""Check this project's own CPHEA terminal-slope fits against published values.

`fit_cphea_halflives.py` refits 186 terminal slopes from the EPA CPHEA raw
curves. It selects, among windows of the last n post-peak points, the one with
the best adjusted R-squared. That rule has a failure mode: on a biphasic curve
the most log-linear segment is the shallow terminal tail, which is not the
dominant elimination phase a published half-life describes.

Kudo et al. 2002 Table 2 makes this checkable. The CPHEA study 2990271 is that
experiment -- Wistar rat, IV 48.63 umol/kg PFOA, both sexes, the dose matching
exactly -- so the published half-lives are a direct reference for two of our
fitted curves.

Run:  python3 scripts/validate_cphea_fits.py          # report
      python3 scripts/validate_cphea_fits.py --write  # add a flag column
"""
import csv
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FITS = os.path.join(HERE, "..", "db", "cphea_fitted_halflives.csv")
RAWDIR = os.path.join(HERE, "..", "..", "tk_learning", "data")

# Kudo 2002 Table 2, read from the full text in papers/.
PUBLISHED = {
    ("2990271", "Male"): ("Kudo 2002 Table 2", 5.68),
    ("2990271", "Female"): ("Kudo 2002 Table 2", 0.08),
}
INFLATION_FLAG = 3.0        # x, versus the dominant-phase estimate


def curves_by_key():
    """Raw CPHEA curves, keyed by (study, sex, dataset label).

    The dataset label carries the dose in mg/kg. The fitted table carries the
    dose in the source paper's own units, which for Kudo and Ohmori is
    umol/kg, so the two cannot be matched on the dose field. Part 2 therefore
    only uses study/sex combinations that have exactly one raw dataset, where
    the pairing is unambiguous without needing the dose at all.
    """
    out = {}
    for fn in sorted(os.listdir(RAWDIR)):
        if not fn.endswith(".csv"):
            continue
        sex = "Female" if "Female" in fn else "Male"
        with open(os.path.join(RAWDIR, fn)) as fh:
            for r in csv.DictReader(fh):
                try:
                    pt = (float(r["time_d"]), float(r["conc_mgL"]))
                except (ValueError, KeyError):
                    continue
                out.setdefault((r["study"], sex, r.get("dataset", "")), []).append(pt)
    return out


def dominant_halflife(pts):
    """Half-life from the peak to the first point at or below 10% of peak.

    A deliberately crude estimate of the phase that carries most of the dose,
    chosen because it cannot select a tail: it is anchored at the peak.
    """
    pts = sorted(pts)
    pi = max(range(len(pts)), key=lambda i: pts[i][1])
    t0, c0 = pts[pi]
    for t, c in pts[pi + 1:]:
        if c > 0 and c <= 0.10 * c0:
            return (t - t0) * math.log(2) / math.log(c0 / c)
    return None


def main():
    write = "--write" in sys.argv
    raw = curves_by_key()

    with open(FITS) as fh:
        rows = list(csv.DictReader(fh))
        fields = list(rows[0].keys())

    print("PART 1 -- AGAINST PUBLISHED VALUES FOR THE SAME EXPERIMENT")
    print("=" * 72)
    print(f"\n  {'study/sex':22} {'fitted':>8} {'published':>10} {'ratio':>7}  source")
    pub_rows = []
    for r in rows:
        study = r["study"].split("_")[-1]
        key = (study, r["sex"])
        if key not in PUBLISHED:
            continue
        src, pub = PUBLISHED[key]
        got = float(r["halflife_days"])
        pub_rows.append((key, got, pub))
        print(f"  {study + ' ' + r['sex']:22} {got:8.3f} {pub:10.2f} "
              f"{got / pub:6.1f}x  {src}")
    if len(pub_rows) == 2:
        fit_ratio = max(g for _, g, _ in pub_rows) / min(g for _, g, _ in pub_rows)
        pub_ratio = max(p for _, _, p in pub_rows) / min(p for _, _, p in pub_rows)
        print(f"\n  male/female ratio: fitted {fit_ratio:.1f}x, "
              f"published {pub_ratio:.0f}x")
        print(f"  The fit understates the sex ratio by {pub_ratio / fit_ratio:.0f}x.")
        print("  Both sexes are inflated, the fast-eliminating one far more, so the")
        print("  bias does not cancel in a ratio -- it compresses it toward 1.")

    print("\n\nPART 2 -- HOW WIDELY DOES THE TAIL GET SELECTED?")
    print("=" * 72)

    # Keep only study/sex pairs with exactly one raw dataset and one fitted row,
    # so a fit pairs with a curve unambiguously.
    by_ss = {}
    for k, pts in raw.items():
        by_ss.setdefault((k[0], k[1]), []).append((k[2], pts))
    fits_by_ss = {}
    for r in rows:
        fits_by_ss.setdefault((r["study"].split("_")[-1], r["sex"]), []).append(r)

    usable = [(ss, v[0][1], fits_by_ss[ss][0])
              for ss, v in sorted(by_ss.items())
              if len(v) == 1 and len(fits_by_ss.get(ss, [])) == 1]

    print(f"\n  Flagging any curve whose fitted half-life exceeds the")
    print(f"  dominant-phase estimate by more than {INFLATION_FLAG:.0f}x.")
    print(f"  Restricted to the {len(usable)} study/sex pairs where exactly one raw")
    print(f"  dataset and one fitted row exist, so the pairing is unambiguous.\n")
    print(f"  {'study':10} {'sex':7} {'n_fit/n':>9} {'fitted':>9} {'dominant':>9} {'ratio':>7}")
    flagged = set()
    for (study, sex), pts, r in usable:
        dom = dominant_halflife(pts)
        if dom is None or dom <= 0:
            continue
        got = float(r["halflife_days"])
        ratio = got / dom
        mark = "  <== flagged" if ratio > INFLATION_FLAG else ""
        if ratio > INFLATION_FLAG:
            flagged.add((r["study"], r["sex"], r["dose"]))
        print(f"  {study:10} {sex:7} "
              f"{r['n_timepoints_in_fit'] + '/' + r['n_timepoints_total']:>9} "
              f"{got:9.3f} {dom:9.3f} {ratio:7.1f}x{mark}")
    print(f"\n  {len(flagged)} of {len(usable)} unambiguously matched curves are flagged.")
    print("  Coverage note: only the PFOA/PFOS rat and primate datasets in")
    print("  tk_learning/data/ have raw curves on disk here, and the one-dataset")
    print("  restriction narrows that further. This is a spot check, not an audit")
    print("  of all 186 fits -- but the window rule that produced them is the same")
    print("  throughout, and Part 1 shows what it costs where it bites.")

    print("\n\nWHAT THIS MEANS FOR THE REPORT")
    print("=" * 72)
    print("  The direction of every conclusion in section 3 survives: the fits")
    print("  understate sex and species ratios, and those sections argue the")
    print("  ratios are large. But `cphea_fitted_halflives.csv` must not be read")
    print("  as a set of half-lives comparable to published ones. Where a")
    print("  published value exists, prefer it; the fitted column is useful for")
    print("  within-curve comparisons at matched sampling design, not as an")
    print("  absolute.")

    if write:
        for r in rows:
            k = (r["study"], r["sex"], r["dose"])
            r["tail_selection_flag"] = ("inflated_vs_dominant_phase" if k in flagged
                                        else "")
        if "tail_selection_flag" not in fields:
            fields.append("tail_selection_flag")
        with open(FITS, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)
        print(f"\n  --write: added tail_selection_flag to {FITS}")


if __name__ == "__main__":
    main()
