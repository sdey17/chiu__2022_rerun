#!/usr/bin/env python3
"""Transcribe EPA 2024 Appendix Table B-26, the summary of human PFOA volume of
distribution values.

The table's own title is the finding: "Summary of PFOA Volume of Distribution
Values ASSIGNED in Human Studies". EPA reviewed the human PFOA literature and
tabulated, for each study, the Vd that study ASSIGNED - because none measured
one. Six of the ten entries assign 170 mL/kg, which is Thompson et al. 2010's
calibrated value.

This matters for the report's central open question. The human Vd literature
looks tightly agreed at 170-200 mL/kg, and that apparent agreement is an
artefact of everyone adopting the same assumed constant. The only direct
measurement, Abraham et al. 2024's 121 mL/kg from a labelled dose, falls outside
that whole range, and Chiu et al. 2022's fitted 430 sits far above it.

Source: US EPA 2024, Appendix to the Final Human Health Toxicity Assessment for
PFOA, EPA-815R24006, Table B-26, p. B-50. Read from
papers/"EPA 2024 PFOA toxicity assessment appendix volume.txt" at line 10979.
"""
import csv
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "db" / "epa_table_b26_human_vd.csv"
DOC = ("US EPA 2024, Appendix to the Final Human Health Toxicity Assessment "
       "for PFOA, EPA-815R24006, Table B-26 p. B-50")

ROWS = [
    ("Mondal et al.", "2014", "Adult, breastfeeding", "Females",
     "Maternal serum", 198,
     "GM breastfeeding 18.32 ng/mL (95% CI 16.36, 20.50); "
     "GM non-breastfeeding 19.26 (16.80, 22.08)", "NR"),
    ("Zhang et al.", "2015a", "Adult", "Males and females", "Whole blood", 170,
     "Mean 2.71; GM 2.47", "Steady state assumed"),
    ("Zhang et al.", "2015a", "Adult, pregnant", "Females", "Whole blood", 170,
     "Mean 3.36; GM 3.09",
     "Steady state NOT assumed due to variable PFAS levels during pregnancy"),
    ("Worley et al.", "2017", ">12 yr", "Males and females", "Blood (2016)", 170,
     "Mean 11.7 ug/L (95% CI 8.7-14.6)", "NR"),
    ("Worley et al.", "2017", ">12 yr", "Males and females", "Blood (2010)", 170,
     "Mean 16.3 (95% CI 13.2-19.6)", "NR"),
    ("Fu et al.", "2016", "Adult, occupational", "Males and females", "Serum",
     170, "Mean 1,052 ng/mL; median 427 ng/mL", "NR"),
    ("Zhang et al.", "2013c", "Adults", "Males and females",
     "Serum and whole blood", 170, "Mean 3.1 ng/mL", "NR"),
    ("Shin et al.", "2011", "Adult, nonoccupational", "Males", "Serum", 181,
     "Median predicted 13.7 ppb; observed 23.5 ppb (updated in Erratum, "
     "Shin et al. 2013)", "NR"),
    ("Shin et al.", "2011", "Adult, nonoccupational", "Females", "Serum", 198,
     "Median predicted 13.7 ppb; observed 23.5 ppb (updated in Erratum, "
     "Shin et al. 2013)", "NR"),
    ("Gomis et al.", "2017", "Human and animals", "Males and females", "Serum",
     200, "Reports an AVERAGE of human and animal Vd values",
     "Authors note that due to declining values in U.S. and Australian "
     "populations, steady state was not achieved in the past decade"),
]

# Published comparators, for the contrast the table is being read against.
COMPARATORS = [
    ("Abraham et al. 2024", 121, "MEASURED, labelled oral dose, Vd = D_abs/C0"),
    ("Gasiorowski 2022, derived in this project", None,
     "mass balance from a donation trial; PFOS 113-199, PFHxS 71-187 mL/kg"),
    ("Andersson et al. 2025", 74, "MEASURED by urinary/faecal mass balance"),
    ("Thompson et al. 2010", 170,
     "CALIBRATED against an assumed 2.3 y half-life, not measured"),
    ("Chiu et al. 2022", 430, "FITTED by a Bayesian hierarchical model"),
]


def main() -> None:
    fields = ["primary_study", "primary_year", "population", "sex",
              "compartment", "vd_mL_kg", "assigned_or_measured",
              "concentration_measured", "steady_state_considerations",
              "source_document"]
    out = []
    for study, yr, pop, sex, comp, vd, conc, ss in ROWS:
        out.append({
            "primary_study": study, "primary_year": yr, "population": pop,
            "sex": sex, "compartment": comp, "vd_mL_kg": vd,
            # The table's title states this for every row in it.
            "assigned_or_measured": "assigned",
            "concentration_measured": conc,
            "steady_state_considerations": ss, "source_document": DOC,
        })
    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(out)

    print("EPA 2024 TABLE B-26: human PFOA volume of distribution")
    print('Title, verbatim: "Summary of PFOA Volume of Distribution Values')
    print(' ASSIGNED in Human Studies"\n')
    print(f"  {'study':<22} {'population':<24} {'sex':<18} {'Vd mL/kg':>8}")
    print("  " + "-" * 76)
    for r in out:
        print(f"  {r['primary_study'] + ' ' + r['primary_year']:<22} "
              f"{r['population'][:24]:<24} {r['sex'][:18]:<18} "
              f"{r['vd_mL_kg']:>8}")

    vds = [r["vd_mL_kg"] for r in out]
    n170 = sum(1 for v in vds if v == 170)
    print()
    print(f"  {len(out)} entries, all ASSIGNED, none measured.")
    print(f"  {n170} of {len(out)} assign exactly 170 mL/kg - Thompson et al. "
          "2010's value.")
    print(f"  Full range {min(vds)}-{max(vds)} mL/kg, a spread of only "
          f"{max(vds)/min(vds):.2f}x.")
    print()
    print("  Shin et al. 2011 is the only entry with a sex-specific Vd "
          "(181 male, 198 female).")
    print("  Gomis et al. 2017's 200 mL/kg is an average of human AND ANIMAL "
          "values.")
    print()
    print("WHAT THE NARROWNESS ACTUALLY MEANS")
    print("  The human Vd literature looks tightly agreed because its members")
    print("  are not independent estimates. They are the same assumed constant,")
    print("  re-adopted. Set against the values that were measured or fitted:\n")
    for name, v, how in COMPARATORS:
        shown = f"{v:>4}" if v is not None else "   -"
        print(f"   {shown} mL/kg  {name:<42} {how[:46]}")
    print()
    print("  Every direct measurement falls BELOW the assigned range; the one")
    print("  population-model fit sits more than twice ABOVE it. The assigned")
    print("  consensus sits in neither place, and nothing in this table tests it.")
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
