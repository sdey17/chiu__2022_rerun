#!/usr/bin/env python3
"""Where does the sex difference live, and where does the species difference?

Report section 3.1 answers this from composite values -- Vd and clearance
assembled across studies and recombined as ln2*Vd/CL. Cross-study composites
carry every difference in strain, dose, route, assay and model along with the
biology.

Three primary sources now on disk measure both terms in both sexes directly:

  Kudo et al. 2002, Chem Biol Interact 139:301, Table 2
      Wistar rat, IV 48.63 umol/kg (= 20.14 mg/kg) PFOA, male and female
  Lou et al. 2009, Toxicol Sci 107:331, Table 2
      CD-1 mouse, oral 1 and 10 mg/kg PFOA, male and female
  Argoul et al. 2026, Environ Res 303:124802, Table 1
      female CD-1 mouse, IV + oral, 11 PFAS in one cocktail

That is enough to do the decomposition within single experiments, and to
replicate the mouse limb that section 3.2 flags as resting on one study.

Run:  python3 scripts/primary_sex_species_decomposition.py
"""
import csv
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PRIM = os.path.join(HERE, "..", "db", "primary_2026")
LN2 = math.log(2)


def load(name):
    with open(os.path.join(PRIM, name)) as fh:
        return list(csv.DictReader(fh))


def share_of_log(ratio_cl, ratio_vd):
    """Fraction of the log half-life ratio contributed by each term."""
    a, b = abs(math.log(ratio_cl)), abs(math.log(ratio_vd))
    return a / (a + b), b / (a + b)


def main():
    kudo = {r["parameter"]: r for r in load("kudo2002_rat_tk.csv")}
    lou = {(r["matrix"], r["parameter"]): r for r in load("lou2009_mouse_tk.csv")}
    arg = {r["chemical"]: r for r in load("argoul2026_mouse_tk.csv")}

    print("PART 1 -- THE SEX DIFFERENCE, MEASURED WITHIN SINGLE EXPERIMENTS")
    print("=" * 74)

    # --- rat, Kudo 2002 Table 2 ---------------------------------------------
    cl_m = float(kudo["total_clearance_per_day"]["male"])
    cl_f = float(kudo["total_clearance_per_day"]["female"])
    vd_m = float(kudo["volume_of_distribution"]["male"])
    vd_f = float(kudo["volume_of_distribution"]["female"])
    t_m = float(kudo["halflife"]["male"])
    t_f = float(kudo["halflife"]["female"])

    print("\nRat (Kudo 2002 Table 2, Wistar, one IV dose, both sexes)")
    print(f"  clearance   M {cl_m:9.1f}   F {cl_f:9.1f} mL/kg-day   F/M = {cl_f / cl_m:7.1f}x")
    print(f"  Vd          M {vd_m:9.1f}   F {vd_f:9.1f} mL/kg       M/F = {vd_m / vd_f:7.2f}x")
    print(f"  half-life   M {t_m:9.2f}   F {t_f:9.2f} d           M/F = {t_m / t_f:7.1f}x")
    pred = LN2 * vd_m / cl_m, LN2 * vd_f / cl_f
    print(f"  identity check ln2*Vd/CL:  M {pred[0]:.2f} d (reported {t_m:.2f}), "
          f"F {pred[1]:.3f} d (reported {t_f:.2f})")
    s_cl, s_vd = share_of_log(cl_f / cl_m, vd_m / vd_f)
    print(f"  of the {t_m / t_f:.0f}x half-life ratio: "
          f"clearance carries {s_cl:.0%}, Vd carries {s_vd:.0%}")

    # --- mouse, Lou 2009 Table 2 --------------------------------------------
    m_vd_f = float(lou[("sera", "vd")]["female"])
    m_vd_m = float(lou[("sera", "vd")]["male"])
    m_cl_f = float(lou[("sera", "clearance_derived")]["female"])
    m_cl_m = float(lou[("sera", "clearance_derived")]["male"])
    m_t_f = float(lou[("sera", "halflife")]["female"])
    m_t_m = float(lou[("sera", "halflife")]["male"])

    print("\nMouse (Lou 2009 Table 2, CD-1, same model, both sexes)")
    print(f"  clearance   M {m_cl_m:9.2f}   F {m_cl_f:9.2f} mL/kg-day   F/M = {m_cl_f / m_cl_m:7.2f}x")
    print(f"  Vd          M {m_vd_m * 1000:9.1f}   F {m_vd_f * 1000:9.1f} mL/kg       M/F = {m_vd_m / m_vd_f:7.2f}x")
    print(f"  half-life   M {m_t_m:9.2f}   F {m_t_f:9.2f} d           M/F = {m_t_m / m_t_f:7.2f}x")
    s_cl2, s_vd2 = share_of_log(m_cl_f / m_cl_m, m_vd_m / m_vd_f)
    print(f"  of the {m_t_m / m_t_f:.2f}x half-life ratio: "
          f"clearance carries {s_cl2:.0%}, Vd carries {s_vd2:.0%}")

    print("\n  >>> The finding: the Vd sex ratio is essentially the SAME in both")
    print(f"      species -- rat {vd_m / vd_f:.2f}x, mouse {m_vd_m / m_vd_f:.2f}x -- while the")
    print(f"      clearance sex ratio differs by {(cl_f / cl_m) / (m_cl_f / m_cl_m):.0f}x")
    print(f"      (rat {cl_f / cl_m:.0f}x, mouse {m_cl_f / m_cl_m:.2f}x). Sex-dependent distribution")
    print("      is conserved and small; sex-dependent clearance is species-specific")
    print("      and enormous. Note the mouse clearance ratio is below 1: the female")
    print("      mouse clears PFOA slightly SLOWER than the male, the opposite sign")
    print("      to the rat.")

    print("\n\nPART 2 -- THE SPECIES DIFFERENCE IS A FEMALE DIFFERENCE")
    print("=" * 74)
    a_cl_f = float(arg["PFOA"]["cl_mL_kg_day"])
    print(f"\n  female mouse PFOA clearance, two independent studies:")
    print(f"      Lou 2009    {m_cl_f:8.2f} mL/kg-day   (ke x Vd, Table 2)")
    print(f"      Argoul 2026 {a_cl_f:8.2f} mL/kg-day   (NLME, Table 1)")
    print(f"      agreement:  {max(m_cl_f, a_cl_f) / min(m_cl_f, a_cl_f):.2f}x apart")
    print(f"  female mouse PFOA Vd / Vss:")
    print(f"      Lou 2009    {m_vd_f:8.3f} L/kg  (Vz, one-compartment)")
    print(f"      Argoul 2026 {float(arg['PFOA']['vss_L_kg']):8.3f} L/kg  (Vss, NLME)")
    print("\n  rat / mouse PFOA clearance ratio, from primary sources on both sides:")
    for label, mouse_cl in (("Lou 2009", m_cl_f), ("Argoul 2026", a_cl_f)):
        print(f"      FEMALE  rat {cl_f:8.1f} / mouse {mouse_cl:6.2f} = "
              f"{cl_f / mouse_cl:7.0f}x   (mouse from {label})")
    print(f"      MALE    rat {cl_m:8.1f} / mouse {m_cl_m:6.2f} = "
          f"{cl_m / m_cl_m:7.1f}x   (mouse from Lou 2009)")
    ratio_f = cl_f / m_cl_f
    ratio_m = cl_m / m_cl_m
    print(f"\n  >>> The species gap is {ratio_f / ratio_m:.0f}x larger in females than in males.")
    print("      This is section 3.2's conclusion, now with primary measurements")
    print("      on both limbs rather than one mouse study against a composite.")
    print("      Caveat on the dose mismatch: the rat was dosed at 20.14 mg/kg and")
    print("      the mice at 0.08-10 mg/kg. Female rat PFOA clearance FALLS as dose")
    print("      rises (saturable secretion, report section 4.2), so a dose-matched")
    print("      comparison would widen the female gap further, not narrow it.")

    print("\n\nPART 3 -- Vd VERSUS CLEARANCE ACROSS 11 PFAS IN ONE EXPERIMENT")
    print("=" * 74)
    print("\n  Argoul 2026 dosed 11 PFAS as a single cocktail to one sex of one")
    print("  strain in one laboratory, so strain, dose timing, assay and model are")
    print("  held constant. Section 3.1 made this comparison across studies.\n")
    cls, vss = [], []
    print(f"  {'chemical':9} {'CL mL/kg-d':>11} {'Vss L/kg':>9} {'MRT d':>7}")
    for chem, r in arg.items():
        if not r["cl_mL_kg_day"]:
            print(f"  {chem:9} {'nonlinear':>11} {r['vss_L_kg']:>9} {'<1 to 8':>7}")
            continue
        c, v = float(r["cl_mL_kg_day"]), float(r["vss_L_kg"])
        cls.append(c)
        vss.append(v)
        print(f"  {chem:9} {c:11.1f} {v:9.3f} {float(r['mrt_d']):7.2f}")
    print(f"\n  clearance spans {max(cls) / min(cls):8.0f}x")
    print(f"  Vss spans       {max(vss) / min(vss):8.1f}x  (all 10 compounds)")
    no_hxa = [float(r["vss_L_kg"]) for c, r in arg.items() if c != "PFHxA"]
    print(f"  Vss spans       {max(no_hxa) / min(no_hxa):8.1f}x  (excluding PFHxA, whose 4.0 L/kg")
    print("                            comes from a deep compartment; without it the")
    print("                            paper puts PFHxA's Vss at 0.12 L/kg)")
    print(f"\n  >>> Within one experiment, clearance varies over a range "
          f"{(max(cls) / min(cls)) / (max(vss) / min(vss)):.0f}x wider than Vss,")
    print(f"      or {(max(cls) / min(cls)) / (max(no_hxa) / min(no_hxa)):.0f}x wider once PFHxA's deep compartment is set aside.")
    print("      Distribution is not where the action is -- now without any")
    print("      cross-study confounding.")
    print("\n      The mouse sex comparison in Part 1 is the same point from the")
    print("      other side: when the clearance difference disappears (0.83x), the")
    print(f"      residual {m_t_m / m_t_f:.2f}x half-life difference is {s_vd2:.0%} Vd. Vd matters")
    print("      only where clearance does not.")


if __name__ == "__main__":
    main()
