"""
Build the QSAR-ready endpoint table, and argue for the right endpoint.

WHY THIS SCRIPT EXISTS
----------------------
A QSAR needs (a) structure descriptors and (b) ONE number per structure that
the descriptors are supposed to predict. The obvious choice -- half-life -- is
the wrong choice, and this script shows why by construction.

    t_half = ln2 * Vd / CL                 (the governing identity)

Half-life therefore confounds three things that structure affects separately:
binding (which sets both Vd and the filtered load), glomerular filtration
(which is body-size physiology, not chemistry), and tubular transport (which
is the part a QSAR could actually learn). Across species the GFR term alone
moves half-life ~6x between mouse and human with no change in chemistry at all.

The endpoint proposed here strips out the two non-chemical terms:

    R = CL_renal / (fu * GFR)              the dimensionless renal handling ratio

      R <  1  -> net tubular REABSORPTION  (less is cleared than was filtered)
      R == 1  -> pure filtration, no transport
      R >  1  -> net tubular SECRETION     (more is cleared than was filtered)

R divides out GFR (so species of different size are comparable) and divides out
fu (so the binding step is not double-counted). What is left is the transport
step. log10(R) is the natural scale: it is signed, continuous, and spans ~3
orders of magnitude across the compounds below.

Relation to the fractional-reabsorption axis already used in this review:
    FR = 1 - R, so FR = 0.999 is log10(R) = -3.
R is the same physiology, re-expressed so that it does not pile up against a
ceiling at FR -> 1 and does not go unboundedly negative under secretion.

Run:  python3 scripts/qsar_endpoint_table.py
"""

import csv
import math
import os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "db", "qsar", "qsar_endpoint_table.csv")

# ---------------------------------------------------------------------------
# 1. GFR constants -- stated, not hidden, because the endpoint is sensitive
#    to them and the two available sources disagree for the mouse.
# ---------------------------------------------------------------------------
# Argoul 2026 Table 4 reports a column "CL by GFR of free fraction". Dividing
# that column by its own fu column recovers the GFR the authors used:
#   PFBA  7700 / 0.77   = 10000
#   PFHxA 2500 / 0.25   = 10000
#   PFOA    87 / 0.0087 = 10000
# so Argoul's mouse GFR = 10.0 L/d/kg.
GFR_MOUSE_ARGOUL = 10_000.0   # mL/d/kg, back-calculated from Argoul 2026 Table 4
GFR_MOUSE_HAN    = 16_700.0   # mL/d/kg, Han 2012 Table 4 (1.67x higher)
GFR_HUMAN_HAN    =  2_570.0   # mL/d/kg, Han 2012 Table 4 (= 125 mL/min / 70 kg)

# ---------------------------------------------------------------------------
# 2. Structure descriptors.
#
#    n_fluorinated_c counts carbons that bear fluorine. This deliberately
#    EXCLUDES the carboxyl carbon of a PFCA (it bears none) and includes every
#    carbon of a PFSA (the head group is sulfur). The point of defining it this
#    way is that it makes PFOS and PFNA the same size on this axis -- a
#    prediction the data below can falsify.
# ---------------------------------------------------------------------------
DESCRIPTORS = {
    # chemical : (n_c_total, n_fluorinated_c, head_group, n_ether_o, n_branch, mw)
    "PFBA":   (4,  3, "carboxylate", 0, 0, 214.04),   # CF3CF2CF2-COOH
    "PFHxA":  (6,  5, "carboxylate", 0, 0, 314.05),
    "PFOA":   (8,  7, "carboxylate", 0, 0, 414.07),
    "PFNA":   (9,  8, "carboxylate", 0, 0, 464.08),
    "PFDA":   (10, 9, "carboxylate", 0, 0, 514.08),
    "PFBS":   (4,  4, "sulfonate",   0, 0, 300.10),   # CF3CF2CF2CF2-SO3H
    "PFHxS":  (6,  6, "sulfonate",   0, 0, 400.12),
    "PFOS":   (8,  8, "sulfonate",   0, 0, 500.13),
    "PFDS":   (10,10, "sulfonate",   0, 0, 600.15),
    # CF3CF2CF2-O-CF(CF3)-COOH : one ether O, one CF3 branch
    "GenX":   (6,  5, "ether-carboxylate", 1, 1, 330.05),
    # CF3CF2-O-CF2CF2-O-CF2-COOH : two ether O, linear
    "PFO2OA": (6,  5, "ether-carboxylate", 2, 0, 346.05),
}


def read_argoul():
    path = os.path.join(HERE, "db", "primary_2026", "argoul2026_mouse_tk.csv")
    rows = []
    with open(path, newline="") as fh:
        for row in csv.DictReader(fh):
            rows.append(row)
    return rows


def fnum(s):
    """Parse a CSV cell to float, or None if the cell is blank."""
    s = (s or "").strip()
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def handling_ratio(cl_renal, fu_frac, gfr):
    """R = CL_renal / (fu * GFR). Returns (R, log10R) or (None, None)."""
    if cl_renal is None or fu_frac is None or not fu_frac:
        return None, None
    filtered = fu_frac * gfr
    if filtered <= 0:
        return None, None
    r = cl_renal / filtered
    return r, math.log10(r) if r > 0 else None


def main():
    rows = read_argoul()
    table = []

    for row in rows:
        chem = row["chemical"]
        d = DESCRIPTORS.get(chem)
        if d is None:
            continue
        n_c, n_cf, head, n_o, n_br, mw = d

        fu_pct = fnum(row["fu_pct"])
        fu = fu_pct / 100.0 if fu_pct is not None else None
        cl_renal = fnum(row["cl_renal_measured_mL_kg_day"])

        r_arg, log_arg = handling_ratio(cl_renal, fu, GFR_MOUSE_ARGOUL)
        r_han, log_han = handling_ratio(cl_renal, fu, GFR_MOUSE_HAN)

        table.append({
            "chemical": chem,
            "species": "mouse",
            "sex": "female",  # Argoul dosed FEMALE mice; section 4's table is a different animal
            "n_c_total": n_c,
            "n_fluorinated_c": n_cf,
            "head_group": head,
            "n_ether_o": n_o,
            "n_branch": n_br,
            "mw_g_mol": mw,
            "fu_pct": fu_pct,
            "cl_total_mL_kg_day": fnum(row["cl_mL_kg_day"]),
            "cl_renal_mL_kg_day": cl_renal,
            "vss_L_kg": fnum(row["vss_L_kg"]),
            "mrt_d": fnum(row["mrt_d"]),
            "R_gfr_argoul": None if r_arg is None else round(r_arg, 6),
            "log10R_gfr_argoul": None if log_arg is None else round(log_arg, 3),
            "R_gfr_han": None if r_han is None else round(r_han, 6),
            "log10R_gfr_han": None if log_han is None else round(log_han, 3),
            "fr_equiv_1_minus_R": None if r_arg is None else round(1 - r_arg, 4),
            "provenance": "Argoul 2026 Tables 1/2/4; descriptors assigned here; "
                          "R computed here",
        })

    # -- write ---------------------------------------------------------------
    cols = list(table[0].keys())
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(table)

    # -- report -------------------------------------------------------------
    print("=" * 78)
    print("PART 1.  The endpoint, one species, one laboratory, one experiment")
    print("=" * 78)
    print("""
  R = CL_renal / (fu * GFR).  R < 1 is net reabsorption, R > 1 is net
  secretion. Sorted by log10(R), strongest reabsorber first.
""")
    scored = [t for t in table if t["log10R_gfr_argoul"] is not None]
    scored.sort(key=lambda t: t["log10R_gfr_argoul"])
    print(f"  {'compound':8s} {'nCF':>4s} {'head':20s} {'etherO':>6s} "
          f"{'fu %':>7s} {'R':>9s} {'log10 R':>8s}  verdict")
    for t in scored:
        verdict = "reabsorbed" if t["R_gfr_argoul"] < 1 else "SECRETED"
        print(f"  {t['chemical']:8s} {t['n_fluorinated_c']:>4d} "
              f"{t['head_group']:20s} {t['n_ether_o']:>6d} "
              f"{t['fu_pct']:>7.2f} {t['R_gfr_argoul']:>9.4f} "
              f"{t['log10R_gfr_argoul']:>8.2f}  {verdict}")

    lo = scored[0]["log10R_gfr_argoul"]
    hi = scored[-1]["log10R_gfr_argoul"]
    print(f"\n  Span of the endpoint: {hi - lo:.2f} log units "
          f"({10 ** (hi - lo):,.0f}-fold) over {len(scored)} compounds.")

    # -- structure blocks ---------------------------------------------------
    print()
    print("=" * 78)
    print("PART 2.  Does structure order it? Split by head group.")
    print("=" * 78)
    for head in ("carboxylate", "sulfonate", "ether-carboxylate"):
        grp = [t for t in scored if t["head_group"] == head]
        grp.sort(key=lambda t: t["n_fluorinated_c"])
        if not grp:
            continue
        print(f"\n  {head} (by fluorinated carbon count):")
        for t in grp:
            print(f"     nCF {t['n_fluorinated_c']:>2d}  {t['chemical']:8s} "
                  f"log10 R = {t['log10R_gfr_argoul']:>6.2f}")
        vals = [t["log10R_gfr_argoul"] for t in grp]
        monotone = all(vals[i] <= vals[i + 1] for i in range(len(vals) - 1)) or \
                   all(vals[i] >= vals[i + 1] for i in range(len(vals) - 1))
        print(f"     monotonic in nCF? {'yes' if monotone else 'NO'}")

    # the falsifiable prediction the descriptor definition made
    pairs = {t["chemical"]: t["log10R_gfr_argoul"] for t in scored}
    if "PFOS" in pairs and "PFNA" in pairs:
        print(f"""
  The test the descriptor definition set up for itself:
  PFOS and PFNA both have 8 fluorinated carbons but different head groups.
     PFNA (carboxylate) log10 R = {pairs['PFNA']:.2f}
     PFOS (sulfonate)   log10 R = {pairs['PFOS']:.2f}
     difference         {abs(pairs['PFNA'] - pairs['PFOS']):.2f} log units """
              f"({10 ** abs(pairs['PFNA'] - pairs['PFOS']):.1f}-fold)")

    if "GenX" in pairs and "PFO2OA" in pairs and "PFHxA" in pairs:
        print(f"""
  And the ether test. Three compounds, all 5 fluorinated carbons, differing
  only in how many ether oxygens interrupt the chain:
     0 ether O  PFHxA   log10 R = {pairs['PFHxA']:>6.2f}   (secreted)
     1 ether O  GenX    log10 R = {pairs['GenX']:>6.2f}   (reabsorbed)
     2 ether O  PFO2OA  log10 R = {pairs['PFO2OA']:>6.2f}   (secreted)
  Chain length is held constant and the endpoint moves 1.4 log units, so
  chain length is not the controlling descriptor on its own.""")

    # -- GFR sensitivity ----------------------------------------------------
    print()
    print("=" * 78)
    print("PART 3.  How much of the endpoint is the assumed GFR?")
    print("=" * 78)
    print(f"""
  Argoul back-calculates to a mouse GFR of {GFR_MOUSE_ARGOUL/1000:.1f} L/d/kg;
  Han 2012 Table 4 uses {GFR_MOUSE_HAN/1000:.1f} L/d/kg. Ratio {GFR_MOUSE_HAN/GFR_MOUSE_ARGOUL:.2f}x.
  Because R is linear in 1/GFR, that is a flat offset of
  {math.log10(GFR_MOUSE_HAN/GFR_MOUSE_ARGOUL):.2f} log units on every compound:
""")
    print(f"  {'compound':8s} {'log10R (Argoul GFR)':>20s} {'log10R (Han GFR)':>18s}")
    for t in scored:
        print(f"  {t['chemical']:8s} {t['log10R_gfr_argoul']:>20.2f} "
              f"{t['log10R_gfr_han']:>18.2f}")
    print("""
  A flat offset does not change the RANKING, so the structure-activity
  question is unaffected. It does change every absolute cross-species
  comparison, which is Part 4.""")

    # -- the human comparison, and the fu leverage --------------------------
    print()
    print("=" * 78)
    print("PART 4.  The same endpoint for human PFOA -- and why fu decides it")
    print("=" * 78)
    cl_renal_human = 0.03   # mL/d/kg, Han 2012 Table 4
    fu_choices = [
        (0.10,     "PBPK models reading Han's '>90% bound' as '~90% bound'"),
        (0.02,     "Han 2012's own stated assumption"),
        (0.00061,  "Fischer et al., measured at physiological ligand:protein"),
    ]
    mouse_pfoa = pairs.get("PFOA")
    print(f"""
  Human renal clearance of PFOA is {cl_renal_human} mL/d/kg and human GFR is
  {GFR_HUMAN_HAN:,.0f} mL/d/kg; both are fixed. The unbound fraction is not
  fixed -- the literature carries three values spanning 164x, and R is
  linear in 1/fu, so the choice propagates straight through:
""")
    print(f"  {'fu':>9s} {'fu*GFR':>10s} {'R':>11s} {'log10 R':>9s} "
          f"{'vs mouse PFOA':>14s}   source")
    for fu, label in fu_choices:
        r, lg = handling_ratio(cl_renal_human, fu, GFR_HUMAN_HAN)
        gap = 10 ** (mouse_pfoa - lg) if (lg is not None and mouse_pfoa is not None) else None
        print(f"  {fu:>9.5f} {fu*GFR_HUMAN_HAN:>10.2f} {r:>11.6f} {lg:>9.2f} "
              f"{gap:>13.1f}x   {label}")
    print(f"""
  Mouse PFOA (Argoul 2026 is FEMALE mice), measured fu {0.87}%:
  log10 R = {mouse_pfoa:.2f}.

  Read the last column. Under Han's assumed fu the mouse-to-human gap in the
  TRANSPORT step is ~71x and the species difference looks like transport
  biology. Under the measured fu it is ~2x and the species difference is
  almost entirely binding. The two readings call for different experiments,
  different QSARs, and different risk-assessment defaults.

  CAVEAT, and it is the load-bearing one: Argoul's mouse fu and Fischer's
  human fu were measured by different methods at different ligand:protein
  ratios, which is the exact artefact section 6.2 of the report diagnoses.
  Comparing them across methods is not yet legitimate. That makes one cheap
  experiment decisive: measure fu for these compounds in mouse, rat and human
  plasma by a single method at physiological ligand:protein ratio. It needs no
  animals, and it decides whether the species problem is a binding problem.""")

    print()
    print(f"  wrote {os.path.relpath(OUT, HERE)}  ({len(table)} rows)")


if __name__ == "__main__":
    main()
