#!/usr/bin/env python3
"""Is the 100-fold PFOA free-fraction conflict real, or an artefact of ratio?

Report section 6.2 recorded a ~100x conflict between two accounts of how
tightly PFOA binds human plasma protein:

    Han et al. 2003   ">90% bound"  (i.e. f_unbound < 0.10)
    Fischer et al. 2024  f_unbound = 0.00061, measured by SPME

Both full texts are now on disk, and the conflict resolves. The decisive fact
is the ligand-to-protein ratio each worked at.

Run:  python3 scripts/binding_conflict_han_vs_fischer.py
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PRIM = os.path.join(HERE, "..", "db", "primary_2026")

# Han 2003 Methods, p.777: "50 or 60 uM of protein was titrated with
# 0.1-3 mM PFOA in PBS".
HAN_PROTEIN_UM = (50.0, 60.0)
HAN_PFOA_UM = (100.0, 3000.0)

# Fischer 2024: solid-phase microextraction at PFAS:protein <= 0.004.
FISCHER_RATIO = 0.004
FISCHER_FU = 0.00061

# Physiological: human serum albumin ~40 g/L / 66.5 kDa.
ALBUMIN_UM = 600.0
MW_PFOA = 414.07
SERUM_NG_ML = [("general population", 4.0),
               ("Lubeck WV", 68.0),
               ("Little Hocking OH", 448.0),
               ("occupational", 1000.0)]


def main():
    print(__doc__.split("Run:")[0].rstrip())
    print("=" * 74)

    print("\n1. WHAT RATIO DID EACH STUDY WORK AT?")
    print("-" * 74)
    lo = HAN_PFOA_UM[0] / HAN_PROTEIN_UM[1]
    hi = HAN_PFOA_UM[1] / HAN_PROTEIN_UM[0]
    print(f"  Han 2003      {lo:8.1f} : 1  to {hi:8.1f} : 1   (0.1-3 mM PFOA vs 50-60 uM albumin)")
    print(f"  Fischer 2024  {FISCHER_RATIO:8.3f} : 1              (stated ceiling)")
    print(f"\n  Han sits {lo / FISCHER_RATIO:,.0f}x to {hi / FISCHER_RATIO:,.0f}x higher in ligand:protein ratio.")

    print("\n  And the physiological ratio, for scale:")
    for lab, ng in SERUM_NG_ML:
        um = ng / MW_PFOA
        print(f"     {lab:22} {um / ALBUMIN_UM:.2e} : 1   ({ng:g} ng/mL vs 600 uM albumin)")
    phys_hi = SERUM_NG_ML[-1][1] / MW_PFOA / ALBUMIN_UM
    print(f"\n  So Han's lowest ratio is {lo / phys_hi:,.0f}x above even an occupational serum,")
    print("  and Fischer's ceiling sits just above the top of the physiological range.")

    print("\n2. WHAT HAN'S OWN PARAMETERS PREDICT")
    print("-" * 74)
    print("  Han measured Kd = 0.3-0.4 mM with n = 6-9 sites per albumin. At low")
    print("  occupancy that gives  f_unbound = Kd / (Kd + n*[Alb]):\n")
    print(f"  {'Kd (mM)':>8} {'n':>4} {'n*[Alb] (mM)':>13} {'f_unbound':>11} {'% bound':>9}")
    preds = []
    for kd in (0.3, 0.4):
        for n in (6, 9):
            nalb = n * ALBUMIN_UM / 1000.0          # mM
            fu = kd / (kd + nalb)
            preds.append(fu)
            print(f"  {kd:8.1f} {n:4d} {nalb:13.1f} {fu:11.4f} {100 * (1 - fu):8.1f}%")
    print(f"\n  Range: f_unbound {min(preds):.3f} to {max(preds):.3f} — which is where")
    print('  the ">90% bound" statement comes from. It is a CALCULATION from Kd and')
    print("  albumin concentration, not a measured free fraction. Han's abstract says")
    print("  so: 'On the basis of these binding parameters and the estimated plasma")
    print("  concentration of serum albumin, greater than 90% of PFOA would be bound'.")

    print("\n3. THE RESOLUTION")
    print("-" * 74)
    print(f'  (a) ">90% bound" is a FLOOR, and Fischer\'s value satisfies it.')
    print(f"      f_unbound = {FISCHER_FU} is 99.94% bound, which is indeed > 90%.")
    print("      The two statements are not formally in conflict at all. The error")
    print("      entered downstream, when PBPK models read \">90%\" as \"~90%\" and")
    print(f"      used f_unbound ~ 0.1 — about {0.1 / FISCHER_FU:,.0f}x too high.")
    kd_needed = FISCHER_FU * (9 * ALBUMIN_UM / 1000.0) / (1 - FISCHER_FU)
    print(f"\n  (b) The real disagreement is in Kd. To reproduce Fischer's f_unbound")
    print(f"      with n = 9 sites you need Kd = {kd_needed * 1000:.1f} uM. Han measured")
    print(f"      300-400 uM — a factor of {300 / (kd_needed * 1000):.0f}-{400 / (kd_needed * 1000):.0f} apart.")
    print("\n  (c) That factor is what a ratio difference of ~10^3-10^4 produces. At")
    print("      1.7:1 to 60:1 the high-affinity site is saturated immediately and the")
    print("      fitted constant is dominated by the 6-9 low-affinity sites. At")
    print("      0.004:1 only the tightest site is occupied. The two studies measured")
    print("      different things, and only one of them measured the regime humans")
    print("      are actually in.")

    print("\n  (d) A third value agrees with neither extreme and sits between them:")
    print("      Ohmori 2003 reports plasma protein binding 'over 98% for all PFCAs")
    print("      tested' in rat (f_unbound < 0.02), by an in vitro method.")

    print("\n4. CONSEQUENCE FOR THE REVIEW")
    print("-" * 74)
    print("  Section 6.2 should no longer describe this as a contradiction between")
    print("  two measurements. It is a ratio-dependent artefact with a known")
    print("  direction: binding constants measured near saturation understate")
    print("  affinity, and every PBPK model parameterised on Han's figure carries a")
    print("  free fraction roughly two orders of magnitude too high.")
    print("\n  Han 2003 also records that ultrafiltration FAILED for this assay —")
    print("  'PFOA completely nonspecifically bound to the membrane' — which is why")
    print("  microdesalting columns were used, and is a standing warning about")
    print("  method choice in PFAS binding work.")


if __name__ == "__main__":
    main()
