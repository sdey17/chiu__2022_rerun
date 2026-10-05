#!/usr/bin/env python3
"""Is the human Vd that nine regulatory clearance factors inherit a measurement?

Thompson et al. 2010 (Environ Int 36:390, PMID 20236705) is the source of the
170 mL/kg PFOA volume of distribution that EPA's Table B-26 shows ten human
studies assigning. Section 5.4/5.5 of the report records that nine of 42 adopted
regulatory clearance factors are computed from it. Until the full text arrived
this project had only ever seen it second-hand.

The paper's own Table S1 lists the inputs. This script reproduces the Vd from
them and asks three questions:

  1. Was the Vd measured, or back-calculated from an assumed half-life?
  2. What half-life does the published value imply?
  3. What survives if a different half-life is assumed instead?

Run:  python3 scripts/thompson_vd_circularity.py
"""
import csv
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, "..", "db", "primary_2026", "thompson2010_vd_calibration.csv")

LN2 = math.log(2)

# Thompson 2010 Eq. 2c, quoted verbatim from p.392:  Vd = DP / (CP * kP)
# with DP the absorbed daily dose (ng/kg bw/day), CP the steady-state serum
# concentration (ng/mL) and kP the first-order elimination rate (1/day).
#
# The paper assigns kP for PFOA from Bartell et al. 2010, stated in the main
# text as a 2.3-year half-life and in the corrigendum as 2.5 years, both
# rounded to kP = 0.0008 /day.
K_ASSIGNED = 0.0008


def vd_from_inputs(dose_ng_kg_day, serum_ng_mL, k_per_day):
    """Eq. 2c. Serum in ng/mL is ng per mL, so the result is already mL/kg."""
    return dose_ng_kg_day / (serum_ng_mL * k_per_day)


def main():
    with open(DB) as fh:
        rows = list(csv.DictReader(fh))

    print(__doc__.split("Run:")[0].rstrip())
    print("=" * 72)
    print("\n1. REPRODUCING THE PUBLISHED Vd FROM THE PAPER'S OWN TABLE S1")
    print("-" * 72)
    print(f"{'community':16} {'dose':>10} {'serum':>8} {'Vd(k=.0008)':>13} "
          f"{'published':>10} {'match':>7}")
    print(f"{'':16} {'ng/kg/d':>10} {'ng/mL':>8} {'mL/kg':>13} {'mL/kg':>10}")
    for r in rows:
        dose = float(r["daily_dose_ng_kg_day"])
        serum = float(r["serum_pfoa_ng_mL"])
        pub = float(r["calculated_vd_mL_kg"])
        got = vd_from_inputs(dose, serum, K_ASSIGNED)
        print(f"{r['community']:16} {dose:10.0f} {serum:8.0f} {got:13.1f} "
              f"{pub:10.0f} {got / pub:6.3f}x")

    print("\n   The column in Table S1 is headed 'calculated Vd'. Eq. 2c with the")
    print("   assigned kP reproduces both published values to three figures, so the")
    print("   number is an algebraic consequence of the assumed elimination rate,")
    print("   not an independent measurement of distribution volume.")

    print("\n2. WHAT HALF-LIFE DOES THE PUBLISHED Vd IMPLY?")
    print("-" * 72)
    for r in rows:
        dose = float(r["daily_dose_ng_kg_day"])
        serum = float(r["serum_pfoa_ng_mL"])
        pub = float(r["calculated_vd_mL_kg"])
        # invert Eq. 2c:  k = DP / (CP * Vd),  t_half = ln2 / k
        k = dose / (serum * pub)
        print(f"{r['community']:16} implied k = {k:.6f} /day  ->  "
              f"t_half = {LN2 / k:7.1f} d = {LN2 / k / 365.25:.2f} y")
    print("\n   Both communities imply the same ~2.37-year half-life, confirming a")
    print("   single assumed value was used throughout. The main text cites Bartell")
    print("   2010 at 2.3 y; the corrigendum says 2.5 y. kP = 0.0008/day is 2.37 y.")
    print("   Bartell measured it in THE SAME two communities used for the")
    print("   calibration -- the paper says so explicitly as its reason for")
    print("   preferring that value.")

    print("\n3. THE CLEARANCE THAT FOLLOWS, AND WHY THE HALF-LIFE CANCELS")
    print("-" * 72)
    print("   Agencies combine the adopted Vd with a half-life to get clearance:")
    print("       CL = ln2 * Vd / t_half = k * Vd")
    print("   Substituting Eq. 2c for Vd:")
    print("       CL = k * DP / (CP * k) = DP / CP")
    print("   The assumed half-life cancels exactly. Thompson's data therefore")
    print("   support one clearance, the intake-to-serum ratio, and no other:\n")
    for r in rows:
        dose = float(r["daily_dose_ng_kg_day"])
        serum = float(r["serum_pfoa_ng_mL"])
        cl = dose / serum          # (ng/kg/d) / (ng/mL) = mL/kg/d
        print(f"{r['community']:16} CL = {dose:.0f}/{serum:.0f} = "
              f"{cl:.4f} mL/kg-day")
    print("\n   But Vd itself does NOT cancel -- it is proportional to the assumed")
    print("   half-life. Adopting '170 mL/kg' while assuming a different half-life")
    print("   silently changes the intake the calibration data imply:\n")
    print(f"   {'assumed t_half':>16} {'self-consistent Vd':>20} {'source of that t_half'}")
    for t_half_y, src in [(2.37, "Bartell 2010, as used"),
                          (2.3, "main text statement"),
                          (2.5, "corrigendum statement"),
                          (3.3, "Olsen 2007, used in the preprint"),
                          (3.8, "Olsen 2007 upper, kP=0.0005 as printed")]:
        k = LN2 / (t_half_y * 365.25)
        r = rows[0]
        vd = vd_from_inputs(float(r["daily_dose_ng_kg_day"]),
                            float(r["serum_pfoa_ng_mL"]), k)
        print(f"   {t_half_y:14.2f} y {vd:18.0f} mL/kg   {src}")

    print("\n   The corrigendum's own factor-of-0.6 correction is this effect: the")
    print("   authors switched kP from 0.0005 to 0.0008 /day (ratio 0.625) and")
    print("   applied the new Vd to one set of intake units but not the other.")

    print("\n4. THE TRANSPOSITION, SETTLED")
    print("-" * 72)
    print("   Thompson 2010 abstract, p.390, and Table 1:")
    print("       PFOA  Vd = 170 mL/kg bw  -- calibrated, as above")
    print("       PFOS  Vd = 230 mL/kg bw  -- 'based on adjustment of the PFOA value'")
    print("   So PFOA=170 / PFOS=230 is correct; any source giving PFOA=230 and")
    print("   PFOS=170 has them transposed. The PFOS value was never calibrated")
    print("   against serum or intake data at all: the paper scales the PFOA")
    print("   figure up by 20-50% on the basis of cited animal work, landing on")
    print(f"   230, a factor of {230 / 170:.2f}x.")


if __name__ == "__main__":
    main()
