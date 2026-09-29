"""
Does human PFAS half-life depend on exposure level?

Table 1 of Li et al. 2018 (PMC5749314) tabulates, for longitudinally
followed human cohorts, BOTH the initial serum level and the estimated
half-life. That pairing is the human analogue of the animal dose
analysis in ../pfas_dose: if elimination saturates, cohorts starting
higher should clear faster, i.e. show shorter half-lives.

Values below are transcribed from that table plus the two papers' own
abstracts (Seals 2011, Chiu 2022). Initial level is the central value
the source reports (median or mean as noted).
"""
import numpy as np
import pandas as pd

# chemical, cohort, initial serum ng/mL, half-life y, note
ROWS = [
    ("PFOA", "Olsen 2007 retired workers", 408, 3.5, "median initial, GM half-life"),
    ("PFOA", "Gomis ski waxers", 500, 2.4, "range 250-1050, median half-life"),
    ("PFOA", "Bartell 2010 Mid-Ohio", 180, 2.3, "mean initial"),
    ("PFOA", "Seals 2011 Little Hocking", 55, 2.9, "cross-sectional, 1st spline segment"),
    ("PFOA", "Seals 2011 Lubeck", 27, 8.5, "cross-sectional, ~half of Little Hocking"),
    ("PFOA", "Brede 2010 Arnsberg", 24, 3.26, "median initial, GM half-life"),
    ("PFOA", "Worley 2017 Decatur", 16.3, 3.9, "GM initial"),
    ("PFHxS", "Olsen 2007 retired workers", 193, 7.3, "median initial, GM half-life"),
    ("PFHxS", "Li 2018 Ronneby", 152, 5.3, "median initial"),
    ("PFHxS", "Worley 2017 Decatur", 6.4, 15.5, "GM initial"),
    ("PFOS", "Olsen 2007 retired workers", 626, 4.8, "median initial, GM half-life"),
    ("PFOS", "Worley 2017 Decatur", 39.8, 3.3, "GM initial"),
    ("PFOS", "Li 2018 Ronneby", 260, 3.4, "median initial"),
]


def slope(df):
    """ln(clearance) on ln(initial concentration). CL ~ 1/half-life."""
    x = np.log(df.initial_ngml.values)
    y = -np.log(df.halflife_y.values)          # ln CL, up to a constant
    if len(df) < 3:
        return np.nan, np.nan
    b, a = np.polyfit(x, y, 1)
    r = np.corrcoef(x, y)[0, 1]
    return b, r


if __name__ == "__main__":
    df = pd.DataFrame(ROWS, columns=["chemical", "cohort", "initial_ngml",
                                     "halflife_y", "note"])
    df.to_csv("human_initial_vs_halflife.csv", index=False)
    pd.set_option("display.width", 200)
    print(df.to_string(index=False), "\n")

    print("Slope of ln(clearance) on ln(initial serum level):")
    print("  positive = higher exposure clears faster = the saturation hypothesis\n")
    for chem, g in df.groupby("chemical"):
        b, r = slope(g)
        print(f"  {chem:6s} n={len(g)}  slope {b:+.2f}  r={r:+.2f}")
        g2 = g[~g.cohort.str.startswith("Seals")]
        if len(g2) < len(g) and len(g2) >= 3:
            b2, r2 = slope(g2)
            print(f"  {'':6s}       excluding Seals (cross-sectional): "
                  f"slope {b2:+.2f}  r={r2:+.2f}")

    print("""
Mechanistic ceiling. For saturable renal reabsorption,
    CL(C) = CLmax * C / (Km + C)   ->   d ln CL / d ln C = Km/(Km+C) <= 1
so any slope above 1 cannot come from this mechanism.

For comparison, measured within male rats over a 250x dose range: +0.11
""")
