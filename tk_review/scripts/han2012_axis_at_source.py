#!/usr/bin/env python3
"""The reabsorption axis read at its origin, and what it decomposes into.

Report section 3.3 builds its mechanistic axis from OEHHA's PHG appendix
Table A6.4, which that appendix says is adapted from Han et al. 2012. The
review itself (Chem Res Toxicol 25:35-46) is now on disk, so three things can
be checked that could not be before:

  1. whether OEHHA's adaptation preserved the numbers;
  2. where the fu = 0.02 assumption actually originates;
  3. what the axis decomposes into, which Han states and this review missed.

Run:  python3 scripts/han2012_axis_at_source.py
"""
import csv
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PRIM = os.path.join(HERE, "..", "db", "primary_2026")
FU_ASSUMED = 0.02        # Han 2012 Table 4, footnotes c and d


def main():
    with open(os.path.join(PRIM, "han2012_table4_reabsorption_axis.csv")) as fh:
        rows = list(csv.DictReader(fh))

    print(__doc__.split("Run:")[0].rstrip())
    print("=" * 76)
    print("\n1. DID OEHHA'S ADAPTATION PRESERVE THE NUMBERS?")
    print("-" * 76)
    print(f"  {'species':18} {'sex':7} {'Han 2012':>9} {'OEHHA A6.4':>11}  verdict")
    for r in rows:
        han = r["pct_reabsorption"]
        oe = r["oehha_a6_4_value"]
        if not han:
            print(f"  {r['species']:18} {r['sex']:7} {'secretion':>9} {oe:>11}  agree")
            continue
        same = abs(float(han) - float(oe)) < 1e-9
        print(f"  {r['species']:18} {r['sex']:7} {float(han):8.2f}% {oe:>11}  "
              f"{'agree' if same else 'ALTERED'}")
    print("\n  Two values were altered in transmission: human 99.94 -> 99.8 and male")
    print("  rat 93.7 -> 93.2. Neither changes any conclusion, but the report should")
    print("  quote the primary figures, and does now.")

    print("\n2. WHOSE ASSUMPTION IS fu = 0.02?")
    print("-" * 76)
    print("  Report section 3.4 attributed it to OEHHA. It is Han 2012's, stated in")
    print("  the footnotes to its own Table 4: 'net tubular secretion = CLR - fu x")
    print("  GFR, where fu, the unbound fraction, is assumed to be 0.02'. OEHHA")
    print("  inherited it. Han also calls the table's values 'rough estimates' in")
    print("  the body text, which the chain of citation dropped.")
    print(f"\n  For scale, the measured human serum unbound fraction is 0.00061")
    print(f"  (Fischer 2024), which is {0.02 / 0.00061:.0f}x lower than assumed, and the")
    print("  measured mouse value is 0.0087 (Argoul 2026), "
          f"{0.02 / 0.0087:.1f}x lower.")

    print("\n3. WHAT THE AXIS DECOMPOSES INTO")
    print("-" * 76)
    print("  Han makes a point this review had missed. Humans have the LONGEST PFOA")
    print("  half-life but NOT the largest reabsorption in absolute terms:\n")
    print(f"  {'species':18} {'sex':7} {'reabsorbed':>11} {'of filtered':>12} {'% reabs':>9}")
    print(f"  {'':18} {'':7} {'mL/d/kg':>11} {'mL/d/kg':>12}")
    for r in rows:
        if not r["net_reabsorption_mL_d_kg"]:
            continue
        reab = float(r["net_reabsorption_mL_d_kg"])
        filt = FU_ASSUMED * float(r["gfr_L_d_kg"]) * 1000
        print(f"  {r['species']:18} {r['sex']:7} {reab:11.0f} {filt:12.0f} "
              f"{float(r['pct_reabsorption']):8.2f}%")
    print("\n  Humans reabsorb 51 mL/d/kg; male rats 270, mice 318-324, macaques")
    print("  138-155. In Han's words, the reason for the long human half-life is")
    print("  that humans have 'the highest percentage of renal tubular")
    print("  reabsorption', not the highest amount.")

    print("\n  That is because the axis has two factors, not one:")
    print("      CL_renal = [fu x GFR] x [1 - FR]")
    print("  a filtration term and an escape fraction. Both vary across species.\n")

    # Decompose the human-vs-male-mouse gap into its two factors.
    by = {(r["species"], r["sex"]): r for r in rows}
    hum, mou = by[("human", "both")], by[("mouse", "male")]
    filt_h = FU_ASSUMED * float(hum["gfr_L_d_kg"]) * 1000
    filt_m = FU_ASSUMED * float(mou["gfr_L_d_kg"]) * 1000
    esc_h = 1 - float(hum["pct_reabsorption"]) / 100
    esc_m = 1 - float(mou["pct_reabsorption"]) / 100
    gap = float(mou["clr_mL_d_kg"]) / float(hum["clr_mL_d_kg"])
    f_filt, f_esc = filt_m / filt_h, esc_m / esc_h
    print(f"  male mouse / human renal clearance   = {gap:8.0f}x")
    print(f"     of which the filtration term      = {f_filt:8.1f}x  "
          f"(GFR {mou['gfr_L_d_kg']} vs {hum['gfr_L_d_kg']} L/d/kg)")
    print(f"     of which the escape fraction       = {f_esc:8.1f}x  "
          f"({esc_m * 100:.1f}% vs {esc_h * 100:.2f}% escaping)")
    print(f"     product (check)                    = {f_filt * f_esc:8.0f}x")
    s_esc = math.log(f_esc) / (math.log(f_esc) + math.log(f_filt))
    print(f"\n  On a log scale the escape fraction carries {s_esc:.0%} of the gap and")
    print(f"  the lower human GFR carries {1 - s_esc:.0%}. So reabsorption is the larger")
    print("  term, which is why section 3.3's single-axis framing works -- but a")
    print("  third of the human/rodent difference is simply that humans filter")
    print("  blood ~6x more slowly per kg, which no transporter story explains and")
    print("  which allometry (section 3.6) would partly capture.")


if __name__ == "__main__":
    main()
