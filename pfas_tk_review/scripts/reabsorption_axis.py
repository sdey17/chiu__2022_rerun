#!/usr/bin/env python3
"""Place human, male rat, female rat and mouse on a single mechanistic axis:
renal handling of PFOA.

    CL_renal = fu x GFR x (1 - FR)          FR = fraction reabsorbed
    t_half   = ln2 x Vd / CL_total

Two things matter about the algebra. First, the PREDICTION needs only measured
renal clearance and Vd; fu cancels, because fu x GFR x (1 - FR) is just CL_renal
rearranged. Second, the FRAMING as a percentage does not: "99.8% reabsorbed"
depends entirely on the assumed fu, and OEHHA assumes 0.02 for every species
while Fischer et al. 2024 measured 0.00061 in whole human serum - 33x lower.
Both are reported here so the reader can see which conclusions survive.

Sources
  reabsorption / GFR / CL_renal : OEHHA (2024) PHG for PFOA and PFOS in Drinking
      Water, Table A6.4 pp. 327-328, adapted from Han et al. (2012)
  measured fu                   : Fischer et al. 2024, solid-phase microextraction
      in whole human serum (see ../db/protein_binding.csv)
  adopted human clearance       : OEHHA 2024 Sec 4.9 (2.8e-4 L/kg-day);
      US EPA 2024 Table 4-6 (0.120 mL/kg-day)
  urinary:faecal split          : Andersson et al. 2025, matched serum/urine/faeces
  Vd and observed half-life     : ../db/master_exposure_halflife.csv
"""
import csv
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
DB = HERE.parent / "db"

SOURCE = ("OEHHA 2024 PHG for PFOA and PFOS in Drinking Water, Table A6.4 "
          "pp. 327-328, adapted from Han et al. 2012")

# species, sex, GFR (mL/day-kg), measured renal clearance CL_R (mL/kg-day),
# % reabsorbed as OEHHA computes it at fu=0.02 (None = net secretion), reference
REABS = [
    ("rat",     "Female", 14400, 666.0,  None,  "Kemper 2003 (unpublished)"),
    ("rat",     "Female", 14400, 1009.0, None,  "Ohmori et al. 2003"),
    ("rat",     "Male",   14400, 18.2,   93.7,  "Kemper 2003 (unpublished)"),
    ("rat",     "Male",   14400, 21.2,   92.7,  "Ohmori et al. 2003"),
    ("rabbit",  "Female", 4000,  670.0,  None,  "Kudo and Kawashima 2003"),
    ("rabbit",  "Male",   4000,  640.0,  None,  "Kudo and Kawashima 2003"),
    ("dog",     "Female", 5300,  50.8,   52.0,  "Kudo and Kawashima 2003"),
    ("dog",     "Male",   5300,  43.0,   59.0,  "Kudo and Kawashima 2003"),
    ("macaque", "Female", 8500,  32.0,   81.2,  "Harada et al. 2005a"),
    ("macaque", "Male",   8500,  15.0,   91.2,  "Harada et al. 2005a"),
    ("mouse",   "Female", 16700, 16.0,   95.2,  "Kudo and Kawashima 2003"),
    ("mouse",   "Male",   16700, 10.0,   97.0,  "Kudo and Kawashima 2003"),
    ("human",   "Male",   2570,  0.06,   99.8,  "OEHHA 2024 Table 4.5.1"),
]
FU_OEHHA = 0.02       # OEHHA's assumption, applied to every species
FU_MEASURED = 0.00061  # Fischer et al. 2024, PFOA in whole human serum
URINE_SHARE_PFOA = 1.7 / 2.7   # Andersson 2025: PFOA roughly 1.7:1 urine:faeces

VD_OBS = {}


def load_master():
    for r in csv.DictReader((DB / "master_exposure_halflife.csv").open()):
        if r["chemical"] != "PFOA":
            continue
        try:
            VD_OBS[(r["species"], r["sex"])] = (float(r["vd_L_kg"]),
                                                float(r["halflife_d"]))
        except (ValueError, KeyError):
            pass


def main() -> None:
    load_master()

    print("1. THE RENAL AXIS FOR PFOA (OEHHA Table A6.4, fu assumed 0.02)\n")
    print(f"{'species':8} {'sex':7} {'GFR':>7} {'CL_renal':>9} {'fu*GFR':>8} "
          f"{'% reabs':>9}")
    print(f"{'':8} {'':7} {'mL/kg/d':>7} {'mL/kg/d':>9} {'mL/kg/d':>8}")
    print("-" * 54)
    for sp, sex, gfr, clr, pct, ref in REABS:
        filt = FU_OEHHA * gfr
        shown = "SECRETES" if pct is None else f"{pct:.1f}%"
        print(f"{sp:8} {sex:7} {gfr:7.0f} {clr:9.2f} {filt:8.1f} {shown:>9}")

    print()
    print("2. THAT PERCENTAGE IS AN ARTEFACT OF THE ASSUMED fu")
    gfr_h = 2570.0
    clr_h = 0.06
    for label, fu in (("OEHHA assumption", FU_OEHHA),
                      ("Fischer 2024, measured", FU_MEASURED)):
        filt = fu * gfr_h
        pct = (1 - clr_h / filt) * 100
        print(f"  human, fu = {fu:<8g} ({label:<22}) -> filtered load "
              f"{filt:8.2f} mL/kg/d, {pct:5.1f}% reabsorbed")
    print("  The qualitative claim (the human kidney reabsorbs most filtered PFOA)")
    print("  survives; the headline figure of 99.8% does not. It is 33x sensitive")
    print("  to an unbound fraction OEHHA assumed rather than measured.")

    print()
    print("3. THE PREDICTION DOES NOT DEPEND ON fu")
    print("   fu x GFR x (1-FR) is CL_renal rearranged, so predicting half-life")
    print("   needs only measured renal clearance and Vd.\n")
    print(f"{'species':8} {'sex':7} {'Vd':>6} {'CL_renal':>9} {'predicted':>10} "
          f"{'observed':>9} {'ratio':>8}")
    print(f"{'':8} {'':7} {'L/kg':>6} {'L/kg/d':>9} {'t1/2 (d)':>10} "
          f"{'t1/2 (d)':>9} {'pred/obs':>8}")
    print("-" * 62)
    agg = {}
    for sp, sex, gfr, clr, pct, ref in REABS:
        agg.setdefault((sp, sex), []).append((gfr, clr, pct, ref))

    out = []
    for (sp, sex), vals in agg.items():
        if (sp, sex) not in VD_OBS:
            continue
        vd, obs = VD_OBS[(sp, sex)]
        clr = sum(v[1] for v in vals) / len(vals) / 1000.0     # L/kg/d
        pred = math.log(2) * vd / clr
        secreting = all(v[2] is None for v in vals)
        print(f"{sp:8} {sex:7} {vd:6.3f} {clr:9.5f} {pred:10.1f} {obs:9.1f} "
              f"{pred/obs:8.2f}")
        out.append({
            "species": sp, "sex": sex, "chemical": "PFOA",
            "gfr_mL_kg_day": vals[0][0],
            "cl_renal_mL_kg_day": f"{clr*1000:.4f}",
            "pct_reabsorbed_at_fu_0.02": "" if secreting else
                f"{sum(v[2] for v in vals if v[2] is not None)/sum(1 for v in vals if v[2] is not None):.1f}",
            "net_secretion": "yes" if secreting else "no",
            "vd_L_kg": f"{vd:.4f}",
            "halflife_predicted_renal_only_d": f"{pred:.2f}",
            "halflife_observed_d": f"{obs:.2f}",
            "predicted_over_observed": f"{pred/obs:.3f}",
            "reabsorption_source": SOURCE,
            "original_reference": "; ".join(v[3] for v in vals),
        })

    rodents = [o for o in out if o["species"] != "human"]
    worst = max(abs(math.log(float(o["predicted_over_observed"]))) for o in rodents)
    print(f"\n   Rodents: every group predicted to within {math.exp(worst):.1f}x, "
          f"across a {max(float(o['halflife_observed_d']) for o in rodents)/min(float(o['halflife_observed_d']) for o in rodents):.0f}x "
          "span of half-life,\n   with no fitted parameter.")

    print()
    print("4. THE HUMAN POINT, AND WHY RENAL-ONLY CLEARANCE OVERSHOOTS")
    vd_h, obs_h = VD_OBS[("human", "Male")]
    ladder = [
        ("renal clearance only (OEHHA Table 4.5.1)", 0.06),
        ("renal + faecal, scaled by Andersson 2025 1.7:1",
         0.06 / URINE_SHARE_PFOA),
        ("US EPA 2024 adopted CL (Table 4-6)", 0.120),
        ("OEHHA 2024 adopted CL (intake-vs-serum regression)", 0.280),
    ]
    print(f"   Chiu et al. 2022 fitted Vd = {vd_h} L/kg, observed t1/2 = "
          f"{obs_h:.0f} d ({obs_h/365.25:.2f} y)\n")
    print(f"   {'basis for clearance':<52} {'CL':>7} {'t1/2':>8} {'ratio':>7}")
    print(f"   {'':<52} {'mL/kg/d':>7} {'(d)':>8} {'to obs':>7}")
    print("   " + "-" * 76)
    for label, cl in ladder:
        pred = math.log(2) * vd_h / (cl / 1000.0)
        print(f"   {label:<52} {cl:7.3f} {pred:8.0f} {pred/obs_h:7.2f}")
    print()
    print("   Renal-only clearance overestimates the human half-life 4.3-fold.")
    print("   OEHHA's directly measured total clearance reproduces Chiu's "
          "independently")
    print("   fitted half-life to within 7% - two unrelated methods agreeing.")

    with (DB / "reabsorption_axis.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)
    print(f"\nwrote {DB/'reabsorption_axis.csv'}")


if __name__ == "__main__":
    main()
