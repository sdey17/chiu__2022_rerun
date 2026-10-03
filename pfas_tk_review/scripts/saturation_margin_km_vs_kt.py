#!/usr/bin/env python3
"""Is reabsorptive transport saturable at real human exposures?

Report section 4.3 answers no, on the grounds that transporter Km values sit
2,200-82,000x above human serum concentrations. That rests on in vitro Km
values read second-hand. Two of the papers behind it are now on disk:

  Yang et al. 2010, Toxicol Sci 117:294 -- human apical transporter Km values
  Louisse et al. 2024, Toxicology 509:153961 -- human OAT1/OAT2/OAT3 Km values
  Han et al. 2012, Chem Res Toxicol 25:35 -- Table 7, the Tm and KT values that
      PBPK models of PFOA elimination actually run on

These are two estimates of the same conceptual quantity: the concentration at
which reabsorptive transport half-saturates. They disagree by three orders of
magnitude, and the answer to the saturation question flips depending on which
one is used.

Run:  python3 scripts/saturation_margin_km_vs_kt.py
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PRIM = os.path.join(HERE, "..", "db", "primary_2026")
MW_PFOA = 414.07         # g/mol

# Human serum PFOA concentrations, for the margin calculation.
SERUM = [
    ("US general population, NHANES era", 4.0, "Calafat 2007, via Lou 2009"),
    ("Lubeck WV, contaminated water", 68.0, "Thompson 2010 Table S1"),
    ("Little Hocking OH, contaminated water", 448.0, "Thompson 2010 Table S1"),
    ("occupational, fluorochemical workers", 1000.0, "order of magnitude, Olsen 2007"),
]


def main():
    with open(os.path.join(PRIM, "yang2010_human_apical_transporters.csv")) as fh:
        yang = [r for r in csv.DictReader(fh) if r["km_uM"]]
    with open(os.path.join(PRIM, "louisse2024_human_oat_km.csv")) as fh:
        louisse = [r for r in csv.DictReader(fh)
                   if r["chemical"] == "PFOA" and r["km_uM"]]
    with open(os.path.join(PRIM, "han2012_table7_pbpk_tm_kt.csv")) as fh:
        han = list(csv.DictReader(fh))

    print(__doc__.split("Run:")[0].rstrip())
    print("=" * 78)

    print("\n1. THE TWO FAMILIES OF ESTIMATE, IN THE SAME UNITS")
    print("-" * 78)
    print("  In vitro Km for PFOA, human transporters -- six independent values:")
    for r in yang:
        km_uM = float(r["km_uM"])
        print(f"     {r['transporter']:7} {km_uM:7.1f} uM = "
              f"{km_uM * MW_PFOA / 1000:8.2f} mg/L  Yang 2010 ({r['condition']})")
    for r in louisse:
        km_uM = float(r["km_uM"])
        print(f"     {r['transporter']:7} {km_uM:7.1f} uM = "
              f"{km_uM * MW_PFOA / 1000:8.2f} mg/L  Louisse 2024 "
              f"(SE {r['km_se']})")
    print("\n  PBPK-fitted KT, same process, from models agencies use (Han 2012 Table 7):")
    for r in han:
        if not r["kt_mg_L"]:
            continue
        kt = float(r["kt_mg_L"])
        print(f"     {r['species']:11} {kt:9.4f} mg/L = "
              f"{kt / MW_PFOA * 1000:8.3f} uM   {r['kt_note'] or ''}")

    hum_kt = float([r for r in han if r["species"] == "human"][0]["kt_mg_L"])
    kms = sorted([float(r["km_uM"]) for r in yang]
                 + [float(r["km_uM"]) for r in louisse])
    hum_kt_uM = hum_kt / MW_PFOA * 1000
    print(f"\n  The human PBPK KT is {hum_kt_uM:.3f} uM. The six measured human Km")
    print(f"  values span {kms[0]:.0f}-{kms[-1]:.0f} uM, so the fitted value is "
          f"{kms[0] / hum_kt_uM:.0f}-{kms[-1] / hum_kt_uM:.0f}x LOWER")
    print("  than anything ever measured in a cell. With six independent")
    print("  measurements from two laboratories now agreeing within a factor of 7,")
    print("  and the KT values fitted rather than measured, the weight of evidence")
    print("  has moved decisively onto the in vitro side.")

    print("\n2. THE SATURATION QUESTION, ANSWERED BOTH WAYS")
    print("-" * 78)
    print(f"  {'human serum PFOA':40} {'vs KT':>10} {'vs lowest Km':>14}")
    print(f"  {'':40} {'(0.133 uM)':>10} {'(64.1 uM)':>14}")
    for label, ng_mL, _src in SERUM:
        c_uM = ng_mL / MW_PFOA          # ng/mL / (g/mol) = umol/L
        print(f"  {label[:40]:40} {c_uM / hum_kt_uM:9.1f}x {c_uM / kms[0]:13.3f}x")
    lo_km = min(ng / MW_PFOA / kms[0] for _l, ng, _s in SERUM)
    hi_km = max(ng / MW_PFOA / kms[0] for _l, ng, _s in SERUM)
    print(f"\n  Read down the KT column: the two contaminated communities and the")
    print(f"  occupational cohort sit AT or ABOVE the half-saturation constant human")
    print(f"  PBPK models use (1.2x, 8.1x, 18.2x); only the general population is")
    print(f"  below it. Read down the Km column: every one of them sits far BELOW the")
    print(f"  lowest measured in vitro Km, by {1 / hi_km:.0f}x to {1 / lo_km:.0f}x.")
    print("\n  So section 4.3's conclusion holds on in vitro data and fails on the")
    print("  PBPK parameters. The models agencies rely on imply that reabsorption")
    print("  is already saturated in exposed communities -- which, if true, means")
    print("  clearance there is dose-dependent and a single clearance factor does")
    print("  not transfer between exposure settings.")

    print("\n3. WHICH SHOULD BE BELIEVED?")
    print("-" * 78)
    print("  The evidence in hand favours the in vitro values, for three reasons.")
    print("\n  (a) The KT values are not independent measurements. Han's footnote says")
    print("      'Tmc and KT are obtained by fitting PFOA plasma elimination curves'.")
    print("      Two rows carry KT = 67 mg/L marked 'derived from an in vitro")
    print("      measurement' -- and those are ~500x HIGHER than the fitted 0.055,")
    print("      i.e. close to the in vitro Km range, inside the same table.")
    print("  (b) The fitted values are poorly identified. The mouse row is Lou 2009")
    print("      Table 4, whose Tm = 860.9 +/- 1298.3 and KT = 0.0015 +/- 0.0022 both")
    print("      have standard errors exceeding the estimate. Its Tmc/KT of 1.4e7")
    print("      L/d/kg is four orders off every other species in the table.")
    print("  (c) Independent dose-response evidence agrees with the in vitro side.")
    print("      Report section 4.2 finds human half-life essentially")
    print("      dose-independent, and section 4.6 finds the between-person")
    print("      association does not survive age adjustment. If reabsorption were")
    print("      saturated at 68-448 ng/mL, half-life would rise with exposure")
    print("      across exactly that range, and it does not.")
    print("\n  Conclusion: keep section 4.3's answer, but state the basis. Saturation")
    print("  is unreachable at human exposures according to every direct measurement")
    print("  of the transporters; the contrary implication of the PBPK KT values is")
    print("  an artefact of fitting a saturable model to data that do not constrain")
    print("  its parameters. That is a weaker and more honest claim than the one the")
    print("  section made, and it identifies what would settle it: a measured human")
    print("  KT, which nobody has.")


if __name__ == "__main__":
    main()
