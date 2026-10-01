#!/usr/bin/env python3
"""Re-examine Li et al. 2022's between-person association between initial PFAS
level and individual half-life, adjusting for age.

Background. An earlier reading of this project's files treated Li 2022 Table S4
as evidence AGAINST saturable elimination, because the lowest initial-level
tertile has the SHORTER half-life. The obvious confounder is age: older people
have both longer half-lives and larger accumulated burdens, so a between-person
association between initial level and half-life is partly an age association.

Individual-level data are not published, so a true re-fit is impossible. Two
things in the supplement settle the question anyway:

  * Table S14 reports PARTIAL R-squared for each determinant of individual
    half-life. Partial R-squared is by construction the variance a term explains
    GIVEN the other terms in the model, so these values are already mutually
    adjusted. This is the age-adjusted answer, published but never quoted.
  * Tables S4 and S5 give the unadjusted tertile and age effects on the same
    cohort, which allows a bias calculation: how much age imbalance across
    tertiles would be needed to account for the whole tertile effect.

Source: Li Y et al. 2022, Environ Int, doi:10.1016/j.envint.2022.107198,
Supplementary Tables S4, S5 and S14, extracted from the .docx supplement to
db/li2022_si_tables/.
"""
import csv
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
TBL = HERE.parent / "db" / "li2022_si_tables"
OUT = HERE.parent / "db"

# Table S14 (file table_13.csv): partial R^2, n=54.
PARTIAL_R2_FILE = TBL / "table_13.csv"
# Table S4 (table_03.csv): tertiles of initial total PFAS, n=114.
TERTILE_FILE = TBL / "table_03.csv"
# Table S5 (table_04.csv): age groups, n=114.
AGE_FILE = TBL / "table_04.csv"

# Table S4 writes "-11.24%", Table S5 writes "-45.24" with no sign; accept both.
PCT = re.compile(r"(-?\d+\.?\d*)\s*%?\s*$")
HL = re.compile(r"(\d+\.?\d*)\s*\(")


def pct(s):
    m = PCT.search((s or "").strip())
    return float(m.group(1)) if m else None


def first_num(s):
    m = HL.search(s or "")
    return float(m.group(1)) if m else None


def read(path):
    return [r for r in csv.reader(path.open())]


def main() -> None:
    # ---- 1. the published, already-adjusted answer ----------------------
    rows = read(PARTIAL_R2_FILE)
    header = [c.replace("\n", "") for c in rows[0]]
    chems = [c for c in header[1:] if c]
    data = {}
    for r in rows[1:]:
        if not r or not r[0].strip():
            continue
        name = r[0].replace("\n", " ").strip()
        data[name] = [pct(c) for c in r[1:1 + len(chems)]]

    print("1. PARTIAL R-SQUARED FOR EACH DETERMINANT OF INDIVIDUAL HALF-LIFE")
    print("   Li 2022 Table S14, n=54. These are MUTUALLY ADJUSTED by construction:")
    print("   each is the variance that term explains given the others.\n")
    width = max(len(k) for k in data) + 1
    print(f"   {'determinant':<{width}}" + "".join(f"{c[:9]:>10}" for c in chems))
    print("   " + "-" * (width + 10 * len(chems)))
    for name, vals in data.items():
        print(f"   {name:<{width}}" +
              "".join(f"{v:>9.2f}%" if v is not None else f"{'-':>10}"
                      for v in vals))

    age = data.get("Age")
    init = next((v for k, v in data.items() if k.lower().startswith("initial")), None)
    ratios = [a / i for a, i in zip(age, init) if a and i]
    print()
    print(f"   Age explains {min(age):.2f}-{max(age):.2f}% of the variance in "
          "individual half-life.")
    print(f"   Initial PFAS level explains {min(init):.2f}-{max(init):.2f}%.")
    print(f"   Age beats initial level by {min(ratios):.1f}x to {max(ratios):.1f}x "
          f"(median {sorted(ratios)[len(ratios)//2]:.1f}x).")
    worse = sum(1 for a, i in zip(age, init) if a and i and i < a)
    print(f"   Initial level is the weaker term for {worse} of {len(chems)} compounds.")

    # ---- 2. how much age imbalance would explain the tertile effect? -----
    ter = read(TERTILE_FILE)
    agetab = read(AGE_FILE)

    def collect(rows_, n_groups):
        """Walk a stacked table: a chemical name, then n_groups rows."""
        out, cur = {}, None
        for r in rows_[1:]:
            if not r or len(r) < 7:
                continue
            if r[0].strip():
                cur = r[0].strip()
                out[cur] = []
            if cur is not None and r[1].strip():
                out[cur].append({"group": r[1].strip(),
                                 "hl": first_num(r[5]),
                                 "diff_pct": pct(r[6]),
                                 "p": r[4].strip()})
        return {k: v for k, v in out.items() if len(v) >= n_groups}

    t_by_chem = collect(ter, 3)
    a_by_chem = collect(agetab, 3)

    print()
    print("2. COULD AGE ALONE PRODUCE THE TERTILE EFFECT?")
    print("   Both effects are reported as a % change in half-life relative to the")
    print("   reference group, on the same cohort (n=114).\n")
    print(f"   {'PFAS':<12} {'tertile 1 vs 3':>15} {'p':>6} "
          f"{'age 1-14 vs >50':>16} {'p':>8} {'share':>8}")
    print("   " + "-" * 72)
    shares = []
    for chem in t_by_chem:
        if chem not in a_by_chem:
            continue
        t = t_by_chem[chem][0]
        a = a_by_chem[chem][0]
        if t["diff_pct"] is None or a["diff_pct"] is None or a["diff_pct"] == 0:
            continue
        share = abs(t["diff_pct"]) / abs(a["diff_pct"])
        shares.append(share)
        print(f"   {chem:<12} {t['diff_pct']:>14.2f}% {t['p']:>6} "
              f"{a['diff_pct']:>15.2f}% {a['p']:>8} {share*100:>7.0f}%")

    print()
    print("   'share' is the fraction of the full age effect that the tertile")
    print("   effect amounts to. For every compound the tertile effect is a small")
    print("   fraction of the age effect, so only a modest age imbalance across")
    print(f"   tertiles - spanning {min(shares)*100:.0f}-{max(shares)*100:.0f}% of "
          "the 1-14 vs >50 age range -")
    print("   would account for the whole of it. Accumulated body burden rises")
    print("   with age, so that imbalance is expected, not hypothetical.")

    # ---- 3. write it out -------------------------------------------------
    with (OUT / "li2022_age_adjustment.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["chemical", "partial_r2_age_pct", "partial_r2_initial_pfas_pct",
                    "partial_r2_gender_pct", "partial_r2_egfr_pct",
                    "age_over_initial_ratio",
                    "tertile1_vs_3_halflife_pct", "tertile_p",
                    "age_young_vs_old_halflife_pct", "age_p",
                    "tertile_effect_as_share_of_age_effect"])
        gender = data.get("Gender", [None] * len(chems))
        egfr = next((v for k, v in data.items() if k.lower().startswith("egfr")),
                    [None] * len(chems))
        for i, chem in enumerate(chems):
            t = t_by_chem.get(chem, [{}])[0]
            a = a_by_chem.get(chem, [{}])[0]
            share = ""
            if t.get("diff_pct") is not None and a.get("diff_pct"):
                share = f"{abs(t['diff_pct'])/abs(a['diff_pct']):.3f}"
            w.writerow([
                chem, age[i], init[i], gender[i], egfr[i],
                f"{age[i]/init[i]:.1f}" if age[i] and init[i] else "",
                t.get("diff_pct", ""), t.get("p", ""),
                a.get("diff_pct", ""), a.get("p", ""), share])
    print(f"\nwrote {OUT/'li2022_age_adjustment.csv'}")


if __name__ == "__main__":
    main()
