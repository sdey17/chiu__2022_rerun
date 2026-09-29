"""
LESSON 1 -- Forward simulation. No data, no fitting, no statistics.

The point of this lesson is that a toxicokinetic model is just a curve
with a few knobs. Before you try to learn the knobs from data, you should
know by feel what each one does to the curve.

    dC/dt = -k*C,  C(0) = dose/Vd     =>     C(t) = (dose/Vd)*exp(-k*t)

Three knobs:
    dose  how much went in        -> scales the whole curve up and down
    Vd    how far it spreads      -> scales the whole curve up and down
    k     how fast it comes out   -> changes the SHAPE

Run:  python 01_simulate.py
"""
import numpy as np

from tk import iv_1comp, half_life, clearance, steady_state

# ----------------------------------------------------------------------
# A. One curve, printed as a table. Read it before looking at any plot.
# ----------------------------------------------------------------------
print("A. A single IV bolus in a monkey: 10 mg/kg of PFOA\n")
dose, Vd, k = 10.0, 0.18, 0.06        # L/kg, 1/day -- roughly real values

print(f"   C(0)       = dose/Vd = {dose}/{Vd} = {dose/Vd:.1f} mg/L")
print(f"   half-life  = ln2/k   = {half_life(k):.1f} days")
print(f"   clearance  = k*Vd    = {clearance(k, Vd):.4f} L/kg/day\n")

print("   day     C (mg/L)    fraction of C(0)   half-lives elapsed")
for t in [0, 11.55, 23.1, 34.7, 46.2, 100]:
    C = iv_1comp(t, dose, Vd, k)
    print(f"   {t:6.1f}  {C:9.2f}   {C/(dose/Vd):14.3f}   {t*k/np.log(2):14.2f}")

print("""
   Every half-life the concentration halves, whatever it started at.
   That is the defining property of FIRST-ORDER elimination: the rate of
   removal is proportional to how much is there, so the FRACTION removed
   per unit time is constant.
""")

# ----------------------------------------------------------------------
# B. Which knob changes the shape?
# ----------------------------------------------------------------------
print("B. Change one knob at a time, look at day 0 and day 30\n")
print(f"   {'case':28s} {'C(0)':>8s} {'C(30)':>8s} {'ratio':>8s} {'t1/2':>7s}")
for label, d, v, kk in [
    ("baseline",                 10.0, 0.18, 0.06),
    ("dose x2",                  20.0, 0.18, 0.06),
    ("Vd x2",                    10.0, 0.36, 0.06),
    ("k x2  (faster clearing)",  10.0, 0.18, 0.12),
]:
    c0, c30 = iv_1comp(0, d, v, kk), iv_1comp(30, d, v, kk)
    print(f"   {label:28s} {c0:8.1f} {c30:8.2f} {c30/c0:8.3f} {half_life(kk):7.1f}")

print("""
   dose and Vd move C(0) but leave the RATIO C(30)/C(0) untouched --
   they slide the curve vertically. Only k changes the ratio.

   This is why a half-life can be measured from a decay curve without
   ever knowing the dose or the volume: the slope of log C against time
   is -k, and nothing else enters it. It is also why Vd is the weak link
   in any method that computes half-life from a measured clearance
   instead (see ../literature/SYNTHESIS.md section 2).
""")

# ----------------------------------------------------------------------
# C. Repeated dosing: accumulation and steady state
# ----------------------------------------------------------------------
print("C. Daily dosing instead of one bolus\n")
dose_rate = 0.1            # mg/kg/day, every day
CL = clearance(k, Vd)
Css = steady_state(dose_rate, CL)
print(f"   dose rate {dose_rate} mg/kg/day, CL {CL:.4f} L/kg/day")
print(f"   steady state Css = rate/CL = {Css:.2f} mg/L   (Vd does not appear)\n")

C = 0.0
print("   day    C (mg/L)   % of steady state")
for day in range(1, 121):
    C = C * np.exp(-k) + dose_rate / Vd          # dose, then decay 1 day
    if day in (1, 5, 12, 23, 35, 46, 60, 90, 120):
        print(f"   {day:4d}  {C:9.2f}   {100*C/Css:14.0f}%")

print("""
   The printed value is the PEAK just after each day's dose, so it
   settles a few percent above Css; the trough sits the same amount
   below, and the average is Css exactly. The continuous-infusion
   formula describes the average, not the peak.

   Accumulation stops when input equals output. It takes about 4-5
   half-lives to get within a few percent of Css, whatever the dose.
   For PFOA in humans (half-life ~3 years) that is 12-15 years -- which
   is why human blood levels respond so slowly to changes in exposure.
""")

# ----------------------------------------------------------------------
# QUESTIONS -- answer these before moving on
# ----------------------------------------------------------------------
print("""
QUESTIONS
  1. A chemical has a half-life of 5 days. What fraction is left after
     15 days? Check with iv_1comp.
  2. Two chemicals have the same half-life, but one has Vd = 0.1 L/kg
     and the other Vd = 1.0 L/kg. Which has the higher clearance? Which
     reaches a higher steady state on the same daily dose?
  3. You double someone's daily intake. By what factor does their
     eventual steady-state level change? Does the answer depend on k?
  4. PFOA in male rats has a half-life of ~13 days; in humans ~3 years.
     Same dose rate per kg. How much higher is the human steady state?

EXERCISES
  a. Modify section A to use PFHxA in male rats: half-life 0.095 days.
     How many days of sampling would you need to see the decay?
  b. In section C, change the dose to every 7 days instead of daily,
     keeping the same average rate. Does Css change? Does the
     peak-to-trough swing change? Which one matters for toxicity?
""")
