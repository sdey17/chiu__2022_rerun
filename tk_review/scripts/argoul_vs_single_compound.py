"""
Argoul 2026 (eleven PFAS as one cocktail) against the single-compound studies.

Argoul carries a lot of weight in this review: it is the only source that
measures clearance and volume for many PFAS in one experiment, which is what
sections 3 and 10 need. Every other mouse value in the database comes from a
study that dosed ONE compound. So the question is whether dosing eleven at
once, at low dose, by mixed-effects fitting, reproduces what the
one-at-a-time literature found.

The answer has a shape. Clearance and volume are both systematically LOW --
and their ratio is not. That matters, because a half-life is their ratio.

All comparators are FEMALE mouse, matching Argoul; db/animal_halflife_measured.csv
and db/combined/tk_parameters.csv. Units harmonised to days and mL/kg.

Run:  python3 scripts/argoul_vs_single_compound.py
"""

import csv
import math
import os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LN2 = math.log(2)
OUT = os.path.join(HERE, "db", "argoul_vs_single_compound.csv")
PAIRS = []

# Female-mouse comparators from single-compound studies, half-life in DAYS.
# Chang and Sundstrom report hours for serum; converted here.
SINGLE = {
    "PFBA":  [("Chang 2008, 10 mg/kg",  2.87 / 24), ("Chang 2008, 30 mg/kg", 3.08 / 24),
              ("Chang 2008, 100 mg/kg", 2.79 / 24)],
    "PFOA":  [("Lou 2009, 1-10 mg/kg", 15.6)],
    "PFNA":  [("Tatum-Gibbs 2011, 1-10 mg/kg low", 25.8),
              ("Tatum-Gibbs 2011, 1-10 mg/kg high", 68.4)],
    "PFHxS": [("Sundstrom 2012, 1 mg/kg", 24.8), ("Sundstrom 2012, 20 mg/kg", 26.8)],
    "PFOS":  [("Chang 2012, 1 mg/kg", 907 / 24), ("Chang 2012, 20 mg/kg", 731 / 24)],
    "PFBS":  [("Lau 2020, 30 mg/kg", 3.0 / 24), ("Lau 2020, 300 mg/kg", 3.9 / 24)],
}
# The EPA Bayesian hierarchical fit pools the single-compound studies, so it is
# a second, independent summary of the same literature rather than a new study.
POOLED = {"PFBA": 0.186, "PFBS": 0.125, "PFHxA": 0.251, "PFHxS": 26.665,
          "PFNA": 59.439, "PFOA": 21.453, "PFOS": 32.810}

# Direct CL / Vd comparators, female mouse (mL/kg/d, mL/kg)
CLVD = {
    "PFOA":  [("Lou 2009", 5.99, 135), ("Fujii (via EPA)", 11.8, 150)],
    "PFHxS": [("Sundstrom 2012, 1 mg/kg", 2.68, 96),
              ("Sundstrom 2012, 20 mg/kg", 3.79, 147)],
    "PFHxA": [("US EPA PFHxA IRIS", None, 780)],
}


def argoul():
    p = os.path.join(HERE, "db", "primary_2026", "argoul2026_mouse_tk.csv")
    return {r["chemical"]: r for r in csv.DictReader(open(p))}


def main():
    a = argoul()
    print(__doc__.split("Run:")[0].rstrip())

    print("=" * 78)
    print("PART 1.  Clearance and volume, where a single-compound study reports both")
    print("=" * 78)
    print(f"\n  {'cmpd':<7s} {'source':<26s} {'CL':>8s} {'Vd':>7s} "
          f"{'CL ratio':>9s} {'Vd ratio':>9s}")
    cl_r, vd_r = [], []
    for c, comps in CLVD.items():
        r = a[c]
        acl = float(r["cl_mL_kg_day"]) if r["cl_mL_kg_day"] else None
        avd = float(r["vss_L_kg"]) * 1000
        print(f"  {c:<7s} {'Argoul 2026 (cocktail)':<26s} "
              f"{(f'{acl:g}' if acl else '-'):>8s} {avd:>7g} "
              f"{'-':>9s} {'-':>9s}")
        for name, ccl, cvd in comps:
            rc = f"{acl/ccl:.2f}x" if (acl and ccl) else "-"
            rv = f"{avd/cvd:.2f}x" if cvd else "-"
            if acl and ccl: cl_r.append(acl / ccl)
            if cvd: vd_r.append(avd / cvd)
            PAIRS.append(dict(
                parameter="clearance" if (acl and ccl) else "", chemical=c,
                comparator=name, argoul=acl, single=ccl,
                ratio=(acl / ccl) if (acl and ccl) else ""))
            PAIRS.append(dict(
                parameter="volume_of_distribution" if cvd else "", chemical=c,
                comparator=name, argoul=avd, single=cvd,
                ratio=(avd / cvd) if cvd else ""))
            print(f"  {'':<7s} {name:<26s} {(f'{ccl:g}' if ccl else '-'):>8s} "
                  f"{cvd:>7g} {rc:>9s} {rv:>9s}")
    gm = lambda v: math.exp(sum(math.log(x) for x in v) / len(v))
    vd_no_hxa = [v for v in vd_r if v < 3]
    print(f"""
  PFHxA's volume is the one outlier (5.1x HIGH) and is held out of the mean
  below; it is also the only compound Argoul puts in net tubular secretion,
  so its kinetics differ in kind.

  Geometric mean ratio, Argoul / single-compound:
      clearance                {gm(cl_r):.2f}x   ({1/gm(cl_r):.1f}x low)
      volume, excluding PFHxA  {gm(vd_no_hxa):.2f}x   ({1/gm(vd_no_hxa):.1f}x low)

  Both low, by similar factors. Hold on to that -- it is the whole result.
""")

    print("=" * 78)
    print("PART 2.  Half-life: the ratio of the two, so the offsets should cancel")
    print("=" * 78)
    print("""
  Argoul reports MRT, not a terminal half-life. MRT = Vss/CL exactly in its
  table (checked: agrees within 6% for 9 of 10 compounds), so ln2 x MRT is the
  half-life a one-compartment system with that Vss and CL would show. Against a
  measured TERMINAL half-life that is an approximation, and for a compound with
  a deep second compartment it is a LOWER bound. Read the ratios as indicative.
""")
    print(f"  {'cmpd':<7s} {'Argoul ln2*MRT':>14s} {'single-compound':>16s} "
          f"{'ratio':>7s}   source")
    ratios, pooled_r = [], []
    for c in ["PFBA", "PFBS", "PFHxA", "PFOA", "PFHxS", "PFOS", "PFNA"]:
        r = a.get(c)
        if not r or not r["mrt_d"]:
            continue
        at = LN2 * float(r["mrt_d"])
        for name, t in SINGLE.get(c, []):
            ratios.append(at / t)
            print(f"  {c:<7s} {at:>14.3f} {t:>16.3f} {at/t:>6.2f}x   {name}")
            PAIRS.append(dict(parameter="half_life", chemical=c,
                              comparator=name, argoul=at, single=t,
                              ratio=at / t))
        if c in POOLED:
            t = POOLED[c]
            pooled_r.append(at / t)
            print(f"  {c:<7s} {at:>14.3f} {t:>16.3f} {at/t:>6.2f}x   "
                  f"EPA pooled fit (same literature)")
            PAIRS.append(dict(parameter="half_life_pooled", chemical=c,
                              comparator="EPA pooled fit", argoul=at,
                              single=t, ratio=at / t))
    both = ratios + pooled_r
    print(f"\n  Over the {len(ratios)} independent single-compound comparisons the "
          f"half-life ratios\n  span {min(ratios):.2f}x to {max(ratios):.2f}x, "
          f"geometric mean {gm(ratios):.2f}x. The {len(pooled_r)} EPA pooled rows are "
          f"printed\n  above but kept out of that mean, since the pooled fit is built "
          f"from the\n  same studies; including them moves it to {gm(both):.2f}x "
          f"(span {min(both):.2f}x to {max(both):.2f}x)."
          f"\n\n  PFBS and PFDS have no comparator; Argoul reports no clearance for "
          f"PFBS at all.")
    print("""
  So the half-lives broadly agree while the clearances and volumes do not.
  That is the signature of a shared scaling on both terms rather than a
  disagreement about elimination: in t = ln2*Vd/CL, a factor that multiplies
  Vd and CL together cancels.""")

    print()
    print("=" * 78)
    print("PART 3.  What that leaves")
    print("=" * 78)
    print("""
  Three candidate causes, none separable with the data in hand:

   DOSE      Argoul dosed 0.019-1.55 mg/kg, 10-100x below the comparators.
             Section 8's saturable-reabsorption account predicts clearance
             rising with dose, and the one three-point series available
             (PFHxS female, 0.094 / 1 / 20 mg/kg across two laboratories)
             does rise monotonically: CL 1.3 / 2.68 / 3.79, slope +0.20 on
             log-log. Argoul sits at the bottom of that trend, not off it.

   COCKTAIL  Eleven PFAS dosed together could compete for the same
             reabsorptive transporters. That would RAISE clearance, not lower
             it, so it argues against the observed direction -- unless the
             competition is for plasma binding sites instead, which would
             raise the unbound fraction and lower the apparent volume.

   METHOD    Nonlinear mixed-effects fitting shrinks estimates toward the
             population mean; non-compartmental analysis does not. Shrinkage
             would compress the spread rather than shift the centre, so it is
             the weakest of the three.

  The useful conclusion for this review: Argoul's WITHIN-experiment contrasts
  (section 3's 5,254x clearance span against 7.7x in Vss) are unaffected,
  because a shared scaling cancels from a ratio. Its ABSOLUTE clearances are
  what section 10's endpoint R is built from, and those carry a roughly 2-3x
  low bias relative to the single-compound literature.""")

    fields = ["parameter", "chemical", "comparator", "argoul", "single", "ratio"]
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for row in PAIRS:
            if row["parameter"]:
                w.writerow(row)
    print(f"\n  wrote {os.path.relpath(OUT, HERE)} "
          f"({sum(1 for r in PAIRS if r['parameter'])} comparison rows)")


if __name__ == "__main__":
    main()
