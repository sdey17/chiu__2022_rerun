"""
LESSON 3 -- The oldest method: fit a straight line to log C.

If C(t) = C0*exp(-k*t), then

        ln C(t) = ln C0 - k*t

so ordinary least squares on (t, ln C) gives you k from the slope and C0
from the intercept. No optimiser, no priors, no MCMC. You can do it in a
spreadsheet, and for a century everybody did.

This lesson does it, then shows you the three ways it misleads you.

Run:  python 03_loglinear.py
"""
import numpy as np

from tk import load, one_dataset, half_life, clearance

def loglinear(t, C):
    """Return k, C0, and the R^2 of the log-scale fit."""
    t, C = np.asarray(t, float), np.asarray(C, float)
    ok = C > 0
    t, y = t[ok], np.log(C[ok])
    slope, intercept = np.polyfit(t, y, 1)
    pred = intercept + slope * t
    r2 = 1 - np.sum((y - pred) ** 2) / np.sum((y - y.mean()) ** 2)
    return -slope, np.exp(intercept), r2


# ----------------------------------------------------------------------
# A. Fit the monkey data three ways
# ----------------------------------------------------------------------
mk = load("PFOA_Male_primate")
one = mk[mk.animal_id == 2054].sort_values("time_d")
dose = 10.0

print("A. Same animal, same data, three choices of which points to use\n")
print(f"   {'points used':28s} {'n':>3s} {'k (1/d)':>9s} {'t1/2 (d)':>9s} "
      f"{'C0 (mg/L)':>10s} {'Vd (L/kg)':>10s} {'R2':>6s}")

for label, sel in [
    ("everything",            one.time_d >= 0),
    ("after day 1",           one.time_d >= 1),
    ("after day 7 (terminal)", one.time_d >= 7),
    ("first 7 days only",     one.time_d <= 7),
]:
    d = one[sel]
    k, C0, r2 = loglinear(d.time_d, d.conc_mgL)
    print(f"   {label:28s} {len(d):3d} {k:9.4f} {half_life(k):9.2f} "
          f"{C0:10.2f} {dose/C0:10.3f} {r2:6.3f}")

print("""
   TRAP 1: the answer depends on where you start the line.

   Using everything gives a half-life pulled down by the fast early
   distribution phase. Using only the terminal points gives the true
   elimination half-life -- that is what "terminal half-life" means and
   why papers report it. And the Vd you back out of the intercept is
   nonsense for the terminal fit, because that intercept extrapolates the
   SLOW line back to t=0, where the fast phase actually was.

   Rule of thumb: start the terminal line after distribution is over,
   which you judge from the consecutive-slope table in lesson 02.
""")

# ----------------------------------------------------------------------
# B. Log-linear regression is not least squares on C
# ----------------------------------------------------------------------
print("B. What taking the log does to the errors\n")
d = one[one.time_d >= 7]
k, C0, _ = loglinear(d.time_d, d.conc_mgL)
print(f"   {'t':>6s} {'observed':>10s} {'predicted':>10s} "
      f"{'resid (mg/L)':>13s} {'resid (log)':>12s}")
for _, r in d.iterrows():
    pred = C0 * np.exp(-k * r.time_d)
    print(f"   {r.time_d:6.1f} {r.conc_mgL:10.3f} {pred:10.3f} "
          f"{r.conc_mgL - pred:13.3f} {np.log(r.conc_mgL / pred):12.3f}")

print("""
   On the mg/L scale the early residuals are huge and the late ones are
   tiny -- but on the log scale they are comparable. Fitting on the log
   scale therefore weights every point by its RELATIVE error, i.e. it
   assumes the noise is multiplicative (a constant coefficient of
   variation), which is what PK measurement error usually looks like.

   TRAP 2: this is a modelling assumption, not a mathematical trick.
   Least squares on C and least squares on ln C are different models and
   give different answers. Log-scale is almost always the right one here,
   but say so out loud.
""")

# ----------------------------------------------------------------------
# C. Every experiment in the male-rat file
# ----------------------------------------------------------------------
print("C. Terminal-slope half-life for each PFOA male-rat experiment\n")
rat = load("PFOA_Male_rat")
print(f"   {'dataset':28s} {'route':>7s} {'dose':>7s} {'n_term':>7s} "
      f"{'t1/2 (d)':>9s} {'R2':>6s}")
rows = []
for name, g in rat.groupby("dataset"):
    g = g.sort_values("time_d")
    cut = g.time_d.max() / 3          # crude: terminal = last two-thirds
    term = g[(g.time_d >= cut) & (g.conc_mgL > 0)]
    if len(term) < 4 or term.time_d.nunique() < 3:
        continue
    k, C0, r2 = loglinear(term.time_d, term.conc_mgL)
    if k <= 0:
        continue
    rows.append((name, g.route.iloc[0], g.dose_mgkg.iloc[0], half_life(k)))
    print(f"   {name:28s} {g.route.iloc[0]:>7s} {g.dose_mgkg.iloc[0]:7.2f} "
          f"{len(term):7d} {half_life(k):9.2f} {r2:6.3f}")

hl = np.array([r[3] for r in rows])
print(f"\n   {len(hl)} experiments, half-life {hl.min():.1f} to {hl.max():.1f} days, "
      f"median {np.median(hl):.1f}")
print("""
   TRAP 3: the spread is large, and "terminal" was defined here by a
   crude rule (last two-thirds of each curve). Different papers make
   this choice differently and never all the same way. A published
   half-life is a fitted number plus a judgement call about where the
   terminal phase begins.

   Compare: the careful Bayesian 2-compartment fit of these same data in
   ../pfas_dose gives 13.3 days.

QUESTIONS
  1. Why is the Vd you get from the terminal intercept too LARGE rather
     than too small? Sketch the two lines on a log axis.
  2. Section A shows R2 near 1 for several different answers. What does
     that tell you about R2 as a check on a PK fit?
  3. If a study sampled for only 7 days, would it report a half-life
     that is too short or too long? Which way would that bias a
     species comparison, given that human studies run for years?
  4. Log-linear regression silently drops any point with C <= 0 (below
     the detection limit). Those are always the LATE points. What does
     that do to the estimated half-life?

EXERCISES
  a. Rerun section C with cut = t_max/2 and cut = t_max/5. How much do
     the half-lives move? That movement is the judgement call, quantified.
  b. Compute the half-life for each of the three monkeys separately.
     How much do individuals differ? Compare that spread to the spread
     across rat experiments in section C.
""")
