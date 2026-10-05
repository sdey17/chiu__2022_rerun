#!/usr/bin/env python3
"""Reconcile the human PFAS kinetic parameters, which are over-determined.

Any two of (Vd, CL, t_half) fix the third through t_half = ln2 x Vd / CL. So a
disagreement about Vd is never only about Vd: it is a disagreement about which
two of the three you believe. This script lays each source's own triple side by
side and completes the missing term, so the real locus of disagreement is
visible.

Sources
  Abraham et al. 2024, Environ Int 193:109047 (PMID 39476597), Table 3 and
      Table 4. One volunteer, 15 13C-labelled PFAS, plasma followed 450 days.
      Vd = D_abs/C0, measured with nothing assumed. n = 1.
  Chiu et al. 2022, doi:10.1289/EHP10103. Bayesian hierarchical one-compartment
      model fitted to community drinking-water cohorts; Vd and half-life both
      estimated.
  US EPA 2024 PFOA/PFOS toxicity assessments, Table 4-6. Vd assumed from
      Thompson et al. 2010; half-life from Li et al.; clearance computed.
  OEHHA 2024 PHG Sec 4.9. Clearance regressed directly from intake against
      serum; half-life used "for Vd calculation only".
"""
import math

LN2 = math.log(2)
DPY = 365.25

# chemical -> source -> (Vd mL/kg, half-life years, CL mL/kg-day); None = not given
DATA = {
    "PFOA": {
        "Abraham 2024 (measured, n=1)": (121, 2011 / DPY, None),
        "Chiu 2022 (fitted)":           (430, 3.14,       None),
        "EPA 2024 (Vd assumed)":        (170, 2.7,        0.120),
        "OEHHA 2024 (CL measured)":     (None, 2.7,       0.280),
    },
    "PFOS": {
        "Abraham 2024 (measured, n=1)": (152, 1211 / DPY, None),
        "Chiu 2022 (fitted)":           (320, 3.36,       None),
        "EPA 2024 (Vd assumed)":        (230, 3.4,        0.128),
        "OEHHA 2024 (CL measured)":     (None, 3.4,       0.390),
    },
    "PFHxS": {
        "Abraham 2024 (measured, n=1)": (125, 1634 / DPY, None),
        "Chiu 2022 (fitted)":           (290, 2.35,       None),
        "EPA IRIS 2025 (adopted CL)":   (None, None,      0.041),  # CL only
    },
    "PFNA": {
        "Abraham 2024 (measured, n=1)": (124, 1305 / DPY, None),
        "Chiu 2022 (fitted)":           (190, 2.35,       None),
    },
}


def complete(vd, t_y, cl):
    """Fill in whichever of the three terms is missing."""
    if vd is not None and t_y is not None and cl is None:
        cl = LN2 * vd / (t_y * DPY)
    elif vd is not None and cl is not None and t_y is None:
        t_y = LN2 * vd / cl / DPY
    elif cl is not None and t_y is not None and vd is None:
        vd = cl * t_y * DPY / LN2
    return vd, t_y, cl


def main() -> None:
    for chem, sources in DATA.items():
        print(f"=== {chem} ===")
        print(f"  {'source':<32} {'Vd':>8} {'t1/2':>7} {'CL':>9}   derived")
        print(f"  {'':<32} {'mL/kg':>8} {'y':>7} {'mL/kg/d':>9}")
        print("  " + "-" * 70)
        rows = []
        for name, (vd, t_y, cl) in sources.items():
            given = {k for k, v in zip("VTC", (vd, t_y, cl)) if v is not None}
            vd2, t2, cl2 = complete(vd, t_y, cl)
            missing = {"V": "Vd", "T": "t1/2", "C": "CL"}
            derived = ", ".join(missing[k] for k in "VTC" if k not in given)
            if None in (vd2, t2, cl2):
                # Only one of the three was published; nothing to complete.
                f = lambda v, w, d: (f"{v:{w}.{d}f}" if v is not None
                                     else "-".rjust(w))
                print(f"  {name:<32} {f(vd2,8,0)} {f(t2,7,2)} {f(cl2,9,4)}"
                      f"   (only one term published)")
                continue
            print(f"  {name:<32} {vd2:8.0f} {t2:7.2f} {cl2:9.4f}   {derived}")
            rows.append((name, vd2, t2, cl2))

        for label, idx in (("Vd", 1), ("half-life", 2), ("clearance", 3)):
            vals = [r[idx] for r in rows]
            print(f"  spread in {label:<10} {max(vals)/min(vals):5.1f}x")
        print()

    print("WHERE THE DISAGREEMENT ACTUALLY LIVES\n")
    print("  For PFOA, Chiu's fitted parameters imply a clearance of")
    cl_chiu = LN2 * 430 / (3.14 * DPY)
    print(f"    CL = ln2 x 430 / (3.14 x 365.25) = {cl_chiu:.3f} mL/kg-day,")
    print(f"  against OEHHA's directly measured 0.280 - agreement to "
          f"{abs(cl_chiu-0.280)/0.280*100:.0f}%.")
    print("  So Chiu and OEHHA agree on CLEARANCE, and the Vd of ~400 mL/kg is")
    print("  what that shared clearance implies at a 2.7-3.1 y half-life. It is")
    print("  NOT an independent measurement of Vd, and an earlier framing of it")
    print("  as a convergence of two routes overstated the case.")
    print()
    cl_abr = LN2 * 121 / 2011
    print(f"  Abraham's measured triple gives CL = {cl_abr:.4f} mL/kg-day,")
    print(f"  which is {0.280/cl_abr:.1f}x BELOW OEHHA's and {0.120/cl_abr:.1f}x "
          "below EPA's.")
    print("  The disagreement is therefore about clearance, not about Vd. Vd")
    print("  simply follows from whichever clearance and half-life you accept.")
    print()
    print("  Abraham is the only direct measurement of human Vd (D_abs/C0, no")
    print("  assumed quantity), and it is also the only estimate from a single")
    print("  person at tracer dose, with a PFOA half-life of 5.5 y (4.0-8.8)")
    print("  that sits above every cohort estimate. Both facts matter: the")
    print("  method is the strongest available and the sample is n = 1.")


if __name__ == "__main__":
    main()
