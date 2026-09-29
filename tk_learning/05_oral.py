"""
LESSON 5 -- Oral dosing, and the identifiability problem it creates.

Most animal PFAS studies use gavage, not IV. The chemical has to be
absorbed before it can be eliminated, so the model gains a compartment
(the gut) and a rate (ka):

    C(t) = (F*dose/Vd) * ka/(ka-k) * (exp(-k*t) - exp(-ka*t))

Three parameters now -- Vd, k, ka -- plus bioavailability F. This lesson
fits that to real rat data and then shows the two things that go wrong,
both of which are about IDENTIFIABILITY: whether the data can tell the
parameters apart at all.

Run:  python 05_oral.py
"""
import numpy as np
from scipy.optimize import curve_fit

from tk import load, oral_1comp, iv_1comp, half_life, clearance

# ----------------------------------------------------------------------
# A. What the curve looks like
# ----------------------------------------------------------------------
print("A. Absorption changes the shape, not the area\n")
dose, Vd, k = 1.0, 0.25, 0.05
print(f"   {'ka (1/d)':>9s} {'Cmax':>8s} {'tmax (d)':>9s} {'AUC':>8s}")
grid = np.linspace(0, 400, 40001)
for ka in [0.05001, 0.2, 1.0, 5.0, 50.0]:
    C = oral_1comp(grid, dose, Vd, k, ka)
    auc = np.trapezoid(C, grid) if hasattr(np, "trapezoid") else np.trapz(C, grid)
    print(f"   {ka:9.2f} {C.max():8.3f} {grid[C.argmax()]:9.2f} {auc:8.2f}")
print(f"   {'IV':>9s} {dose/Vd:8.3f} {0.0:9.2f} "
      f"{dose/clearance(k, Vd):8.2f}")

print("""
   Faster absorption gives a higher, earlier peak -- but the AUC is
   identical for every ka, and equal to the IV value when F = 1. That
   follows from CL = F*dose/AUC: total exposure depends on how much got
   in and how fast it leaves, never on how fast it entered.

   So AUC tells you about CL. The PEAK is what tells you about ka.
""")

# ----------------------------------------------------------------------
# B. Fit a real gavage experiment
# ----------------------------------------------------------------------
rat = load("PFOA_Male_rat")
g = rat[(rat.dataset == "5916078-6.0 mg/kg-gavage") & (rat.conc_mgL > 0)]
g = g.groupby("time_d", as_index=False).conc_mgL.mean()
t, C, DOSE = g.time_d.values, g.conc_mgL.values, 6.0

def oral_log(t, ln_Vd, ln_k, ln_ka):
    return np.log(oral_1comp(t, DOSE, np.exp(ln_Vd), np.exp(ln_k), np.exp(ln_ka)))

popt, pcov = curve_fit(oral_log, t, np.log(C),
                       p0=[np.log(0.25), np.log(0.05), np.log(2.0)], maxfev=20000)
Vd, k, ka = np.exp(popt)
se = np.sqrt(np.diag(pcov))

print("B. PFOA, male rats, 6 mg/kg by gavage (study 5916078)\n")
print(f"   n = {len(t)} time points, day {t.min():g} to {t.max():g}\n")
print(f"   Vd (=V/F)  = {Vd:8.4f} L/kg   (x/ {np.exp(1.96*se[0]):.2f})")
print(f"   k          = {k:8.4f} 1/day  (x/ {np.exp(1.96*se[1]):.2f})")
print(f"   ka         = {ka:8.4f} 1/day  (x/ {np.exp(1.96*se[2]):.2f})")
print(f"   half-life  = {half_life(k):8.2f} days")
print(f"   absorption half-time = {half_life(ka):.3f} days "
      f"({24*half_life(ka):.1f} hours)")

# ----------------------------------------------------------------------
# C. Problem 1: F and Vd are the same parameter
# ----------------------------------------------------------------------
print("\nC. You did not measure Vd. You measured Vd/F.\n")
print(f"   {'if F is':>9s} {'then true Vd':>14s} {'then true CL':>14s} {'t1/2':>8s}")
for F in [1.0, 0.8, 0.5, 0.2]:
    print(f"   {F:9.1f} {Vd*F:14.4f} {clearance(k, Vd*F):14.5f} {half_life(k):8.2f}")
print("""
   Every oral-only fit has this hole. The curve is identical for
   (F=1, Vd=0.25) and (F=0.5, Vd=0.125): only the ratio appears in the
   equation. Papers write "Vd/F" and "CL/F" to be honest about it.

   Note what is NOT affected: the half-life. k comes from the shape of
   the decay, and F just scales the curve. This is the same fact as
   lesson 01 section B, and it is why half-life is the most robustly
   estimated quantity in all of PK -- and why clearance, which everyone
   agrees is the more meaningful parameter, is the harder one.

   The fix is an IV arm at the same dose. Study 3749289 and 6302380 both
   have one; that is why those studies are valuable.
""")

# ----------------------------------------------------------------------
# D. Problem 2: flip-flop kinetics
# ----------------------------------------------------------------------
print("D. Which exponential is which?\n")
lo, hi = sorted([k, ka])
fit_C = oral_1comp(t, DOSE, Vd, lo, hi)                 # k = lo, ka = hi
swap_C = oral_1comp(t, DOSE, Vd * lo / hi, hi, lo)      # k = hi, ka = lo
print(f"   fitted   k = {lo:.4f}, ka = {hi:.4f},  Vd = {Vd:.4f}")
print(f"   swapped  k = {hi:.4f}, ka = {lo:.4f},  Vd = {Vd*lo/hi:.6f}")
print(f"   max |ln| difference between the two curves: "
      f"{np.max(np.abs(np.log(fit_C / swap_C))):.2e}")
print("""
   The two curves are IDENTICAL to machine precision. Swapping k and ka
   and rescaling Vd by k/ka leaves the prediction untouched -- the
   formula is symmetric in the two rates up to that one factor. So oral
   data alone cannot tell you which rate is absorption and which is
   elimination. This is called
   "flip-flop kinetics", and it is not a curiosity: for slowly absorbed
   compounds the terminal slope is the ABSORPTION rate, and the
   half-life you report is wrong.

   Everyone resolves it by assumption -- ka > k, absorption is faster --
   which is usually true and occasionally not. The only real resolution
   is, again, an IV arm: IV has no ka, so it pins k directly.
""")

# ----------------------------------------------------------------------
# E. Do it properly: fit IV and gavage together
# ----------------------------------------------------------------------
print("E. Joint fit of the IV and gavage arms of one study\n")
both = rat[rat.study == 6302380]
both = both[(both.dose_mgkg == 1.0) & (both.conc_mgL > 0)]
iv = both[both.route == "iv"].groupby("time_d", as_index=False).conc_mgL.mean()
po = both[both.route == "gavage"].groupby("time_d", as_index=False).conc_mgL.mean()
D = 1.0

def joint(_, ln_Vd, ln_k, ln_ka, logit_F):
    F = 1 / (1 + np.exp(-logit_F))
    Vd_, k_, ka_ = np.exp([ln_Vd, ln_k, ln_ka])
    return np.concatenate([np.log(iv_1comp(iv.time_d.values, D, Vd_, k_)),
                           np.log(oral_1comp(po.time_d.values, D, Vd_, k_, ka_, F))])

y = np.concatenate([np.log(iv.conc_mgL.values), np.log(po.conc_mgL.values)])
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")      # see the note after the table
    p, pc = curve_fit(joint, np.zeros_like(y), y,
                      p0=[np.log(0.25), np.log(0.05), np.log(2.0), 2.0],
                      maxfev=40000)
Vd2, k2, ka2 = np.exp(p[:3]); F2 = 1 / (1 + np.exp(-p[3]))
print(f"   n = {len(iv)} IV + {len(po)} gavage time points, 1 mg/kg each\n")
print(f"   Vd        = {Vd2:8.4f} L/kg      (now a real Vd, not Vd/F)")
print(f"   k         = {k2:8.4f} 1/day")
print(f"   ka        = {ka2:8.4f} 1/day")
print(f"   F         = {F2:8.3f}           (bioavailability, now identified)")
print(f"   half-life = {half_life(k2):8.2f} days")
print(f"   CL        = {clearance(k2, Vd2):8.5f} L/kg/day")
print("""
   Adding the IV arm removed both problems at once: F is separated from
   Vd because the IV curve has F = 1 by definition, and k is pinned by
   the IV decay so ka has nowhere to hide.

   Two honest caveats on this particular fit. F came out at 1.000,
   pressed against its ceiling, so its standard error is undefined --
   curve_fit warns about the covariance and we suppressed the warning
   only to keep the output readable. That is the right answer
   biologically (PFOA is essentially completely absorbed in rats) but
   it means the data cannot distinguish F = 1.0 from F = 0.95. And the
   half-life here, 5.3 days, is well below the 11.6 days the 6 mg/kg
   gavage arm of a different study gave in section B. Different studies,
   but also a one-compartment model straining against a two-compartment
   curve -- lesson 06.

   Design beats statistics. No amount of cleverness in the fitting
   recovers information the experiment did not collect.

QUESTIONS
  1. In section A, why is tmax later when ka is smaller? Write down
     dC/dt = 0 and solve for t.
  2. Section C: if a paper reports "CL/F = 0.02 L/kg/day" and you assume
     F = 1 when the truth is F = 0.6, is the real clearance higher or
     lower than reported? What about the half-life?
  3. In section D the swap needed Vd rescaled by k/ka. Work through
     the algebra: why exactly that factor, and why does the apparent
     sign change in ka/(ka-k) cancel out?
  4. PFOA is almost completely absorbed in rats (F near 1). Does that
     make the section C problem go away, or just make the assumption a
     good one? What is the difference?

EXERCISES
  a. Refit section B forcing ka = 100 (essentially instant absorption).
     How much worse is the fit? How much does the half-life move?
  b. Run section E on study 3749289, which also has matched IV and
     gavage arms at 1 mg/kg. Do the two studies agree on F?
  c. The half-life from section B is a single number with a confidence
     interval that assumes the model is right. Compare it to the
     terminal-slope answer for the same dataset in lesson 03 section C.
""")
