#!/usr/bin/env python3
"""Decompose the rat-versus-mouse PFAS half-life difference into its two
mechanistic terms, and test whether exposure explains it.

Half-life is an identity, not an independent quantity:

    t_half = ln2 * Vd / CL

so for any two groups A and B,

    ln(t_A / t_B) = ln(Vd_A / Vd_B) - ln(CL_A / CL_B)

Every ratio therefore splits exactly into a distribution term and a clearance
term, and the split says which physiology to go looking at. Input is the EPA
animal PK fits already in ../../species_dose/species_exposure.csv.
"""
import csv
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent.parent / "species_dose" / "species_exposure.csv"
OUT = HERE.parent / "db"


def load():
    out = {}
    for r in csv.DictReader(SRC.open()):
        try:
            rec = {
                "halft": float(r["halft_mean"]),
                "vd": float(r["Vd_mean"]),
                "clc": float(r["CLC_mean"]),
                "serum": float(r["serum_median"]),
                "dose": float(r["dose_median"]),
                "dose_units": r["dose_units"],
                "bw": float(r["BW"]),
                "n_obs": int(r["n_obs"]),
                "model": r["model"],
            }
        except (ValueError, KeyError):
            continue
        out[(r["PFAS"], r["species"], r["sex"])] = rec
    return out


def ln(x):
    return math.log(x)


def main() -> None:
    d = load()
    chems = sorted({k[0] for k in d})
    OUT.mkdir(parents=True, exist_ok=True)

    # ---- 1. mouse / rat, decomposed -------------------------------------
    print("=" * 94)
    print("1. MOUSE vs RAT half-life ratio, split into distribution and clearance terms")
    print("   ln(t_mouse/t_rat) = ln(Vd_mouse/Vd_rat) - ln(CL_mouse/CL_rat)")
    print("=" * 94)
    print(f"{'PFAS':7} {'sex':7} {'t_mouse':>8} {'t_rat':>8} {'t ratio':>8} "
          f"{'Vd ratio':>9} {'CL ratio':>9} {'% from Vd':>10} {'% from CL':>10}")
    print("-" * 94)
    rows = []
    for c in chems:
        for s in ("Male", "Female"):
            m, r = d.get((c, "mouse", s)), d.get((c, "rat", s))
            if not (m and r):
                continue
            t_ratio = m["halft"] / r["halft"]
            vd_ratio = m["vd"] / r["vd"]
            cl_ratio = m["clc"] / r["clc"]
            lt, lv, lc = ln(t_ratio), ln(vd_ratio), -ln(cl_ratio)
            denom = abs(lv) + abs(lc)
            pv = 100 * abs(lv) / denom if denom else float("nan")
            pc = 100 * abs(lc) / denom if denom else float("nan")
            print(f"{c:7} {s:7} {m['halft']:8.3f} {r['halft']:8.3f} {t_ratio:8.2f} "
                  f"{vd_ratio:9.2f} {cl_ratio:9.2f} {pv:9.0f}% {pc:9.0f}%")
            rows.append({
                "PFAS": c, "sex": s,
                "halflife_mouse_d": f"{m['halft']:.4f}", "halflife_rat_d": f"{r['halft']:.4f}",
                "halflife_ratio_mouse_over_rat": f"{t_ratio:.3f}",
                "vd_ratio": f"{vd_ratio:.3f}", "clearance_ratio": f"{cl_ratio:.3f}",
                "ln_halflife_ratio": f"{lt:.4f}",
                "ln_vd_contribution": f"{lv:.4f}", "ln_clearance_contribution": f"{lc:.4f}",
                "pct_attributable_to_vd": f"{pv:.1f}", "pct_attributable_to_clearance": f"{pc:.1f}",
                "serum_median_mouse_ngml": f"{m['serum']:.1f}", "serum_median_rat_ngml": f"{r['serum']:.1f}",
                "dose_median_mouse": f"{m['dose']:.3f}", "dose_median_rat": f"{r['dose']:.3f}",
                "dose_units": m["dose_units"],
            })
    with (OUT / "mouse_rat_decomposition.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    # ---- 2. the same split applied to the sex difference ------------------
    print()
    print("=" * 94)
    print("2. FEMALE vs MALE within each species, same decomposition")
    print("=" * 94)
    print(f"{'PFAS':7} {'species':8} {'t_F':>9} {'t_M':>9} {'t_F/t_M':>8} "
          f"{'Vd ratio':>9} {'CL ratio':>9} {'% from CL':>10}")
    print("-" * 94)
    srows = []
    for c in chems:
        for sp in ("rat", "mouse", "primate"):
            f_, m_ = d.get((c, sp, "Female")), d.get((c, sp, "Male"))
            if not (f_ and m_):
                continue
            t_ratio = f_["halft"] / m_["halft"]
            vd_ratio = f_["vd"] / m_["vd"]
            cl_ratio = f_["clc"] / m_["clc"]
            lv, lc = ln(vd_ratio), -ln(cl_ratio)
            denom = abs(lv) + abs(lc)
            pc = 100 * abs(lc) / denom if denom else float("nan")
            print(f"{c:7} {sp:8} {f_['halft']:9.3f} {m_['halft']:9.3f} {t_ratio:8.3f} "
                  f"{vd_ratio:9.2f} {cl_ratio:9.2f} {pc:9.0f}%")
            srows.append({
                "PFAS": c, "species": sp,
                "halflife_female_d": f"{f_['halft']:.4f}", "halflife_male_d": f"{m_['halft']:.4f}",
                "halflife_ratio_F_over_M": f"{t_ratio:.4f}",
                "vd_ratio_F_over_M": f"{vd_ratio:.3f}",
                "clearance_ratio_F_over_M": f"{cl_ratio:.3f}",
                "pct_attributable_to_clearance": f"{pc:.1f}",
                "serum_median_female_ngml": f"{f_['serum']:.1f}",
                "serum_median_male_ngml": f"{m_['serum']:.1f}",
                "dose_median_female": f"{f_['dose']:.3f}", "dose_median_male": f"{m_['dose']:.3f}",
                "dose_units": f_["dose_units"],
            })
    with (OUT / "sex_decomposition.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(srows[0].keys()))
        w.writeheader()
        w.writerows(srows)

    # ---- 3. does the gap track exposure? ---------------------------------
    # If exposure level drove half-life, groups at matched serum concentration
    # would have matched half-lives. Test that directly on the mouse/rat pairs.
    print()
    print("=" * 94)
    print("3. IS THE MOUSE/RAT GAP AN EXPOSURE ARTEFACT?")
    print("   For each pair: how different is serum concentration, and how different is half-life?")
    print("=" * 94)
    print(f"{'PFAS':7} {'sex':7} {'serum ratio':>12} {'t ratio':>9} {'dose ratio':>11}  verdict")
    print("-" * 94)
    for r in rows:
        sm, sr = float(r["serum_median_mouse_ngml"]), float(r["serum_median_rat_ngml"])
        dm, dr = float(r["dose_median_mouse"]), float(r["dose_median_rat"])
        s_ratio = sm / sr if sr else float("nan")
        t_ratio = float(r["halflife_ratio_mouse_over_rat"])
        d_ratio = dm / dr if dr else float("nan")
        # Saturable elimination predicts higher exposure -> longer half-life,
        # i.e. serum ratio and half-life ratio should move together.
        if math.isnan(s_ratio):
            verdict = "-"
        elif (s_ratio > 1) == (t_ratio > 1):
            verdict = "consistent with exposure"
        else:
            verdict = "OPPOSITE to exposure"
        print(f"{r['PFAS']:7} {r['sex']:7} {s_ratio:12.2f} {t_ratio:9.2f} {d_ratio:11.2f}  {verdict}")

    # ---- 4. within-species correlation of half-life with exposure ---------
    print()
    print("=" * 94)
    print("4. WITHIN each species-sex group, does half-life track serum concentration")
    print("   across the seven chemicals? (Pearson r on logs)")
    print("=" * 94)
    for sp in ("rat", "mouse", "primate"):
        for s in ("Male", "Female"):
            pts = [(ln(v["serum"]), ln(v["halft"]))
                   for k, v in d.items() if k[1] == sp and k[2] == s and v["serum"] > 0]
            if len(pts) < 3:
                continue
            n = len(pts)
            mx = sum(p[0] for p in pts) / n
            my = sum(p[1] for p in pts) / n
            sxy = sum((p[0] - mx) * (p[1] - my) for p in pts)
            sxx = sum((p[0] - mx) ** 2 for p in pts)
            syy = sum((p[1] - my) ** 2 for p in pts)
            r_ = sxy / math.sqrt(sxx * syy) if sxx and syy else float("nan")
            slope = sxy / sxx if sxx else float("nan")
            print(f"  {sp:8} {s:7} n={n:2}  r={r_:+.3f}  slope d(ln t)/d(ln serum)={slope:+.3f}")

    print()
    print(f"wrote {OUT/'mouse_rat_decomposition.csv'}")
    print(f"wrote {OUT/'sex_decomposition.csv'}")


if __name__ == "__main__":
    main()
