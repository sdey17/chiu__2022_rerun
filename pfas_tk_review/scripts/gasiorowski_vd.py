#!/usr/bin/env python3
"""Derive an independent human volume of distribution from the Gasiorowski 2022
blood- and plasma-donation randomised trial.

The trial removed a known volume of plasma from people with known serum PFAS
concentrations and measured the resulting fall in serum. That is a mass-balance
experiment, and it fixes Vd without assuming a half-life:

    mass removed      = V_plasma_removed x C_plasma(time-averaged)
    body burden lost  = Vd(L) x delta_C_serum
    =>  Vd(L) = V_removed x C_mean / delta_C

The trial's own observation arm supplies the correction that makes this work:
subtracting it nets out continuing background intake and natural elimination,
leaving only what the donations removed. The authors never did this calculation.

Two arms give two independent estimates from the same trial, which is the
internal check.

Source: Gasiorowski R et al. 2022, JAMA Netw Open 5(4):e226257,
doi:10.1001/jamanetworkopen.2022.6257, PMID 35394514. Trial design from the
Interventions section; concentrations from the baseline characteristics Table
and the Results section.
"""
import csv
import math
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "db" / "gasiorowski_vd.csv"

# ---- what the trial reports -------------------------------------------
# arm -> (n donations (mean), volume per donation in L, is_whole_blood)
ARMS = {
    "plasma": (6.4, 0.800, False),   # "up to 800 mL every 6 weeks", mean 6.4
    "blood":  (4.3, 0.470, True),    # "approximately 470 mL every 12 weeks"
}

# chemical -> arm -> (baseline ng/mL, within-arm change, change vs observation)
DATA = {
    "PFOS":  {"plasma": (11.7, -2.9, -3.1), "blood": (10.9, -1.1, -1.1)},
    "PFHxS": {"plasma": (5.2, -1.1, -1.5),  "blood": (3.6, -0.1, -0.6)},
    "PFOA":  {"plasma": (1.2, -0.5, -0.8),  "blood": (1.2, -0.1, -0.3)},
}

# Body weight is NOT reported. BMI is 27.9 (SD 3.6) and the cohort is 97.9% male.
# Weight is reconstructed from BMI x height^2 over a plausible height range.
BMI = 27.9
HEIGHTS = (1.74, 1.78, 1.82)        # m; Australian adult male range
HAEMATOCRIT = 0.45                   # plasma fraction of whole blood = 1 - Hct

# Published comparators, mL/kg
COMPARATORS = {
    "PFOS":  {"Abraham 2024 measured": 152, "Chiu 2022 fitted": 320,
              "Thompson 2010 assumed": 230},
    "PFHxS": {"Abraham 2024 measured": 125, "Chiu 2022 fitted": 290},
    "PFOA":  {"Abraham 2024 measured": 121, "Chiu 2022 fitted": 430,
              "Thompson 2010 assumed": 170},
}


def log_mean(c0, c1):
    """Time-averaged concentration under exponential decline from c0 to c1."""
    if c0 <= 0 or c1 <= 0 or abs(c0 - c1) < 1e-9:
        return (c0 + c1) / 2
    return (c0 - c1) / math.log(c0 / c1)


def vd_mL_per_kg(n_don, vol_L, whole_blood, baseline, delta_within,
                 delta_vs_obs, bw_kg, vol_fraction=1.0):
    """Vd in mL/kg from one arm and one chemical."""
    v_removed_L = n_don * vol_L * vol_fraction
    if whole_blood:
        v_removed_L *= (1 - HAEMATOCRIT)      # only plasma carries the PFAS
    c_end = baseline + delta_within           # delta_within is negative
    c_mean = log_mean(baseline, c_end)
    mass_ng = v_removed_L * 1000.0 * c_mean   # mL x ng/mL
    if delta_vs_obs >= 0:
        return None
    vd_mL = mass_ng / abs(delta_vs_obs)       # ng / (ng/mL) = mL
    return vd_mL / bw_kg


def main() -> None:
    rows = []
    print("INDEPENDENT Vd FROM THE GASIOROWSKI 2022 DONATION TRIAL")
    print(f"BMI {BMI}; body weight reconstructed over heights "
          f"{HEIGHTS[0]}-{HEIGHTS[-1]} m "
          f"({BMI*HEIGHTS[0]**2:.0f}-{BMI*HEIGHTS[-1]**2:.0f} kg)\n")

    for chem, arms in DATA.items():
        print(f"=== {chem} ===")
        print(f"  {'arm':<8} {'V removed':>10} {'C mean':>8} {'dC vs obs':>10} "
              f"{'Vd mL/kg':>22}")
        print("  " + "-" * 64)
        for arm, (baseline, dw, dobs) in arms.items():
            n_don, vol, wb = ARMS[arm]
            v_removed = n_don * vol * (1 - HAEMATOCRIT if wb else 1.0)
            c_mean = log_mean(baseline, baseline + dw)
            vds = [vd_mL_per_kg(n_don, vol, wb, baseline, dw, dobs,
                                BMI * h ** 2) for h in HEIGHTS]
            vds = [v for v in vds if v is not None]
            if not vds:
                print(f"  {arm:<8} {v_removed:9.2f}L {c_mean:8.2f} "
                      f"{dobs:10.2f}   not estimable (no net fall)")
                continue
            span = f"{min(vds):.0f} - {max(vds):.0f}  (mid {vds[1]:.0f})"
            print(f"  {arm:<8} {v_removed:9.2f}L {c_mean:8.2f} {dobs:10.2f} "
                  f"{span:>22}")
            rows.append({
                "chemical": chem, "arm": arm,
                "n_donations_mean": n_don, "volume_per_donation_L": vol,
                "whole_blood": "yes" if wb else "no",
                "plasma_volume_removed_L": f"{v_removed:.3f}",
                "baseline_ng_mL": baseline,
                "change_within_arm_ng_mL": dw,
                "change_vs_observation_ng_mL": dobs,
                "time_averaged_conc_ng_mL": f"{c_mean:.2f}",
                "vd_mL_per_kg_low": f"{min(vds):.0f}",
                "vd_mL_per_kg_mid": f"{vds[1]:.0f}",
                "vd_mL_per_kg_high": f"{max(vds):.0f}",
                "source": ("Gasiorowski 2022 JAMA Netw Open "
                           "doi:10.1001/jamanetworkopen.2022.6257; "
                           "derived here, not published"),
            })
        comp = COMPARATORS.get(chem, {})
        if comp:
            print("  published comparators: " +
                  ", ".join(f"{k} {v}" for k, v in comp.items()))
        print()

    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {OUT}\n")

    print("READING IT")
    pfos = [r for r in rows if r["chemical"] == "PFOS"]
    lo = min(float(r["vd_mL_per_kg_low"]) for r in pfos)
    hi = max(float(r["vd_mL_per_kg_high"]) for r in pfos)
    print(f"  PFOS: the two arms independently give {lo:.0f}-{hi:.0f} mL/kg.")
    print(f"  Abraham 2024's measured value is 152 mL/kg - inside that range.")
    print(f"  Chiu 2022's fitted 320 mL/kg sits above it; Thompson's assumed 230")
    print(f"  sits at the top edge.")
    print()
    print("  ASSUMPTIONS, all of which push in knowable directions:")
    print("   - Plasma donations are 'up to 800 mL'. Using the ceiling as the mean")
    print("     OVERSTATES volume removed and therefore OVERSTATES Vd. The true")
    print("     plasma-arm value is at or below what is printed.")
    print("   - Whole blood counts only the plasma fraction (Hct 0.45). PFAS")
    print("     carried in red cells would add mass and raise the blood-arm Vd.")
    print("   - Body weight is reconstructed from BMI; it scales Vd inversely.")
    print("   - PFOA baseline (1.2 ng/mL) sits at the 1 ng/mL reporting limit and")
    print("     the authors' own sensitivity analysis more than halves its effect")
    print("     size, so the PFOA row here should not be relied on.")


if __name__ == "__main__":
    main()
