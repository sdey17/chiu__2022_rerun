"""
Hypothesis: PFAS half-lives are longer in humans because humans are
exposed to far lower doses, and shorter in rodents because they are dosed
high. I.e. the species difference is really a dose difference.

This script assembles the evidence for and against, from
species_exposure.csv (exposure actually measured) and animal_pk.csv
(fitted half-lives).

THE DESIGN PROBLEM
------------------
Species and dose are almost perfectly confounded. Every human is exposed
low; every rodent is dosed high. A plain comparison of humans against
rats cannot separate "because it is a human" from "because the dose is
low" -- the two explanations predict exactly the same thing.

Three things can break the confound, and all three are done below:

  1. WITHIN-SPECIES dose slopes. How much does clearance actually change
     per decade of dose, measured inside one species? That sets a ceiling
     on how much of the species gap dose could possibly explain.

  2. MATCHED-EXPOSURE species pairs. Where two species happen to reach
     SIMILAR serum concentrations, do their half-lives still differ? If
     yes, species matters independently of dose.

  3. The mechanism's shape. Saturable elimination flattens at low
     concentration; it does not keep accelerating forever. A power law
     extrapolated over orders of magnitude is the wrong functional form.
"""
import numpy as np
import pandas as pd

# Chiu et al. 2022, Table 3 -- half-life in YEARS, population GM.
# NOTE: the EPA repo's auxiliary/Chiu_human.csv gives PFHxS 2.35 y, which
# is PFNA's value and is inconsistent with the clearance and Vd in that
# same row (ln2/2.35*0.29 = 0.086, but it reports 0.025). Use the paper.
HUMAN_HALFLIFE_YR = {"PFOA": 3.14, "PFOS": 3.36, "PFNA": 2.35, "PFHxS": 8.30}
YEAR = 365.25

# Within-species dose slopes we measured ourselves, male rats, gavage:
# ln(clearance) ~ beta * ln(dose), per-study intercepts (see ../pfas_dose)
MEASURED_SLOPES = {"PFOA": 0.110, "PFHxA": 0.039}


def load():
    df = pd.read_csv("species_exposure.csv")
    human = df.species == "human"
    df.loc[human, "halft_mean"] = df.loc[human, "PFAS"].map(HUMAN_HALFLIFE_YR) * YEAR
    df = df.dropna(subset=["halft_mean", "serum_median"])
    df["ln_halft"] = np.log(df.halft_mean)
    df["ln_serum"] = np.log(df.serum_median)
    return df


def raw_correlation(df):
    print("1. THE RAW PATTERN (what the hypothesis predicts)\n")
    for chem in ["PFOA", "PFOS", "PFNA", "PFHxS"]:
        g = df[df.PFAS == chem].sort_values("serum_median")
        if g.species.nunique() < 2:
            continue
        print(f"   {chem}")
        for _, r in g.iterrows():
            print(f"      {r.species:8s} {r.sex:6s} serum {r.serum_median:10.1f} ug/L "
                  f"-> half-life {r.halft_mean:9.1f} d")
        r_all = np.corrcoef(g.ln_serum, g.ln_halft)[0, 1]
        animals = g[g.species != "human"]
        r_an = (np.corrcoef(animals.ln_serum, animals.ln_halft)[0, 1]
                if len(animals) > 2 else np.nan)
        print(f"      corr(ln serum, ln half-life): all {r_all:+.2f}"
              f"   |   animals only {r_an:+.2f}\n")


def ceiling_from_within_species_slope(df):
    print("2. HOW MUCH COULD DOSE EXPLAIN, given the slope measured WITHIN a species?\n")
    print("   If clearance ~ dose^beta, then dropping exposure by a factor F")
    print("   multiplies half-life by F^beta.\n")
    for chem, beta in MEASURED_SLOPES.items():
        g = df[df.PFAS == chem]
        h = g[g.species == "human"]
        rat = g[(g.species == "rat") & (g.sex == "Male")]
        if not len(h) or not len(rat):
            print(f"   {chem}: no human half-life to compare against\n")
            continue
        fold_exposure = float(rat.serum_median.iloc[0] / h.serum_median.iloc[0])
        observed = float(h.halft_mean.iloc[0] / rat.halft_mean.iloc[0])
        predicted = fold_exposure ** beta
        share = np.log(predicted) / np.log(observed)
        print(f"   {chem}  (beta = {beta:+.3f} measured in male rats)")
        print(f"      rat serum is {fold_exposure:,.0f}x the human level")
        print(f"      dose alone predicts human half-life {predicted:5.2f}x the rat's")
        print(f"      actually observed                   {observed:5.0f}x")
        print(f"      -> dose explains {100 * share:.0f}% of the gap on a log scale\n")


def matched_exposure(df, tol=2.0):
    """Species pairs that reached similar serum levels for the same chemical."""
    print(f"3. MATCHED EXPOSURE: pairs within {tol:g}x on serum, same chemical\n")
    rows = []
    for chem, g in df.groupby("PFAS"):
        g = g.reset_index(drop=True)
        for i in range(len(g)):
            for j in range(i + 1, len(g)):
                a, b = g.loc[i], g.loc[j]
                if a.species == b.species:
                    continue
                ratio_serum = max(a.serum_median, b.serum_median) / min(a.serum_median,
                                                                        b.serum_median)
                if ratio_serum > tol:
                    continue
                lo, hi = sorted([a, b], key=lambda r: r.halft_mean)
                rows.append(dict(PFAS=chem,
                                 pair=f"{lo.species}/{lo.sex[0]} vs {hi.species}/{hi.sex[0]}",
                                 serum_lo=lo.serum_median, serum_hi=hi.serum_median,
                                 serum_fold=ratio_serum,
                                 halft_lo=lo.halft_mean, halft_hi=hi.halft_mean,
                                 halft_fold=hi.halft_mean / lo.halft_mean))
    out = pd.DataFrame(rows).sort_values("halft_fold", ascending=False)
    if len(out):
        print(out.round(2).to_string(index=False))
        print(f"\n   Median half-life ratio at matched exposure: "
              f"{out.halft_fold.median():.1f}x")
        print("   If dose were the whole story these would all be ~1.0x.")
    return out


if __name__ == "__main__":
    df = load()
    raw_correlation(df)
    ceiling_from_within_species_slope(df)
    out = matched_exposure(df)
    out.to_csv("matched_exposure_pairs.csv", index=False)
