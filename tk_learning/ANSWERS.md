# Answers

Worked answers to the 53 questions, and expected outcomes for the 38
exercises.

**Use these to check yourself, not to skip the work.** Most of these
questions have an answer you can reach by thinking for two minutes or
by running three lines of code, and the reasoning is the part that
transfers. Where a question has a defensible second answer, that is
noted rather than hidden.

Numbers quoted here are produced by `test_lessons.py`, so if a library
upgrade moves one, that test fails and this file is wrong.

---

## Lesson 01 — Forward simulation

**1. Half-life 5 days; what is left after 15 days?**
15 days is exactly 3 half-lives, so 0.5³ = **12.5%**.
`iv_1comp(15, 1, 1, np.log(2)/5)` → 0.125. The point of the question is
that you never need the dose or Vd to answer it: the *fraction*
remaining depends only on how many half-lives have elapsed.

**2. Same half-life, Vd = 0.1 vs 1.0 L/kg. Higher clearance? Higher
steady state?**
CL = k·Vd, and k is the same, so the **Vd = 1.0 chemical has 10× the
clearance**. Css = rate/CL, so it reaches the **lower** steady state —
ten-fold lower. This is the trap the whole course keeps returning to:
"stays in the body a long time" (half-life) and "accumulates to a high
level" (Css) are different properties, and Vd separates them.

**3. Double the daily intake — what happens to Css? Does it depend on k?**
Css = intake/CL is linear in intake, so Css **doubles**, and **no**, it
does not depend on k. k controls how long you take to get there (about
5 half-lives), not where you end up. Doubling intake doubles Css whether
the chemical clears in hours or years.

**4. PFOA: ~13 d in male rats, ~3 y in humans, same dose per kg. How
much higher is the human steady state?**
Css ratio = CL_rat/CL_human. Using this project's fitted values
(rat CL 0.0141, human CL 0.00026 L/kg/day) the answer is **about 54×**.

If you assumed the two species shared a Vd you would get the half-life
ratio instead, 1147/13.3 ≈ **86×**. Both readings are defensible from
the question as asked; noticing that they differ, and why, is the
answer. Vd is not equal (rat 0.27, human 0.43 L/kg), so 54× is the
better number.

**Exercise (a): PFHxA at half-life 0.095 d.** Five half-lives is under
12 hours, so a study sampling daily would see essentially nothing but
the first point. You need sampling on a scale of minutes to hours. This
is why the PFHxA analysis in `../pfas_dose` has such different-looking
data from PFOA.

**Exercise (b): dose weekly instead of daily, same average rate.** Css
(the *average*) is unchanged, because it depends only on rate/CL. The
peak-to-trough swing grows a lot. Which matters depends on the
mechanism: peak concentration matters for acute effects, average for
cumulative ones. For PFAS, with a half-life far longer than the dosing
interval, the swing is tiny either way.

**Exercise (c): redraw on a linear axis.** The parallel lines stop
looking parallel — on a linear axis, equal ratios are not equal
distances, so exponentials with the same rate but different amplitudes
look like completely different curves.

---

## Lesson 02 — Reading the data

**1. Why is the early slope steeper than the late one? Where has the
chemical gone?**
Into tissue. Early on, the blood is losing chemical to *two* processes
— elimination and distribution into a peripheral compartment that
started empty. Only elimination is permanent. Once tissue is loaded,
the net transfer stops and the fall reflects elimination alone, which
is slower. Nothing has left the body at that early rate; most of it has
just moved.

**2. 288 observations over 84 days vs 9 over 12 days — which is better
for the half-life?**
The 84-day study, but **not because of the point count**. What
determines a half-life estimate is how many *half-lives* of decay you
observed. With a ~13-day half-life, 84 days is 6.3 half-lives (a
100-fold fall) and 12 days is 0.9 (a halving). A hundred points
clustered in the first half-life still pin down the slope poorly,
because there is barely any slope to see. Duration in half-lives beats
sample count — the same idea lesson 10 section E uses.

**3. IV and gavage arms at the same dose — what does the comparison give?**
Bioavailability F, and with it a real Vd instead of Vd/F. The IV arm
has F = 1 by definition, so comparing AUCs gives
F = AUC_oral/AUC_IV. It also pins k independently of ka, which resolves
flip-flop ambiguity. This is lesson 05 section E.

**4. What if you pooled male and female rats?**
You would be fitting one exponential to a mixture of two that differ
~28-fold in rate. The fit would land somewhere in between, match
neither, and show exactly the kind of systematic residual sweep lesson
04 section B diagnoses. Worse, the fitted "population variance" would
absorb a real, explainable, categorical difference as if it were random
noise — which is the hierarchical-modelling failure lesson 06 warns
about.

**Exercise.** Datasets with dense early sampling (6302380) bend
visibly; short or sparse ones look log-linear mostly because there is
not enough resolution to see the bend. Absence of curvature is often
absence of data, not evidence of one compartment.

---

## Lesson 03 — Log-linear fitting

**1. Why is the terminal-intercept Vd too LARGE, not too small?**
Vd = dose/C₀, so overestimating Vd means underestimating C₀. The
terminal line is shallower than the true early curve and lies *below*
it; extrapolating that shallow line back to t = 0 lands below the real
starting concentration. Small intercept → large Vd. In lesson 09 this
is quantified: Vextrap = 2.12 L/kg against a true V1 of 0.126, a
17-fold overestimate.

**2. R² near 1 for several different answers — what does that say about R²?**
That R² is nearly useless here. It measures how much of the *variance*
in log C the line explains, and since log C drops by orders of
magnitude over the study, almost any downward line explains most of it.
R² answers "is there a trend", which was never in doubt. Use the
residual *pattern* (lesson 04 section B) instead — it answers "is this
the right shape", which is the actual question.

**3. A 7-day study: half-life too short or too long?**
Too **short**, because it catches the fast distribution phase and reads
its slope as elimination. Lesson 03 section A: the first-7-days fit
gives 4.4 days against 10.2 for the terminal.

The bias direction matters for species comparisons: animal studies are
short relative to their half-lives and human studies run for years, so
short animal studies are biased toward *shorter* half-lives while human
ones are not. That inflates the apparent human/animal gap — a bias
pointing the same way as the dose hypothesis, which is one more reason
`../species_dose` had to test it carefully rather than eyeball it.

**4. Dropping points below the detection limit.**
Those are always the late, low points — exactly the ones carrying the
terminal slope. Dropping them truncates the curve early and biases the
half-life **short**, the same direction as question 3. Proper handling
treats them as censored (known to be below a limit) rather than
missing; Chiu's model does this with the MRL fields that
`../chiu_replication/parse_chiu_data.py` extracts.

**Exercise (a): cut at t_max/2 and t_max/5.** The half-lives move by
tens of percent. That movement *is* the analyst's degree of freedom,
quantified — and it is why two labs analysing identical data publish
different numbers.

**Exercise (b): per-monkey half-lives.** Roughly 27, 9 and 11 days
(lesson 06 confirms this hierarchically). The 3-fold spread across
three animals of one species is comparable to the spread across the 13
rat experiments, which should make you cautious about any half-life
quoted without an interval.

---

## Lesson 04 — Nonlinear least squares

**1. What fraction of the AUC was extrapolated?**
1.2 out of 568.2, about **0.2%** — far below the 20% rule of thumb, so
this AUC is trustworthy. The study ran to 87 days on a ~10-day
half-life, which is why.

**2. Why does CL = dose/AUC hold for two compartments?**
Integrate the mass balance. For any linear model, elimination happens
only from the central compartment at rate CL·C, so
dA_total/dt = −CL·C(t). Integrating from 0 to ∞:
A(∞) − A(0) = −CL·∫C dt, and A(∞) = 0, A(0) = dose. So
dose = CL·AUC regardless of how many compartments the chemical
visited in between. The result needs only linearity and that all
elimination is from the sampled compartment — not any particular
structure.

**3. Which term must dominate for CL to beat both Vd and k?**
var(lnCL) = var(lnVd) + var(lnk) + 2cov. For CL to be tighter than
*both*, the covariance term must be negative enough to overcome the
*larger* of the two variances — you would need
2|cov| > var(lnVd) + var(lnk) − min(var), i.e. a correlation near −1.
Here r = −0.56, enough to beat Vd (×/1.35 vs ×/1.42) but not k
(×/1.16). CL beats both only when the two parameters are almost
perfectly anti-correlated.

**4. With only the first 7 days, which of Vd, k, CL is well estimated?**
**Vd**, and only Vd. It is fixed by the early concentrations, which is
exactly what you have. k needs the decay you have not observed, and
CL = k·Vd inherits k's problem. This is the mirror image of the
terminal-slope situation, where k is well determined and Vd is not.

**Exercise (b): refit with t ≥ 7.** The residual sweep improves and the
half-life lengthens from 8.59 to about 10.2 days — the same answer
lesson 03 reached by a different route, which is the point.

**Exercise (c): fit on the linear scale.** The early high-concentration
points dominate, because their absolute residuals are largest. The
half-life shortens, and the late points — the ones that actually carry
elimination information — become nearly irrelevant to the fit.

---

## Lesson 05 — Oral dosing

**1. Why is tmax later when ka is smaller?**
Set dC/dt = 0 in the two-exponential solution and solve:

```
t_max = ln(ka/k) / (ka − k)
```

Smaller ka means both a smaller numerator and a smaller denominator,
but the denominator shrinks faster, so t_max grows. Physically: the
peak is where input rate equals output rate, and slow input means the
blood level keeps climbing for longer before elimination catches up.

**2. CL/F = 0.02 reported with F = 1 assumed; the truth is F = 0.6.**
You measured CL/F. True CL = (CL/F)·F = 0.02 × 0.6 = **0.012**, so the
real clearance is **lower** than reported. The **half-life is
unaffected** — it comes from the shape of the decay, and F only scales
the curve vertically. Same lesson as 01 Q2 and 03 Q1: shape versus
scale.

**3. Why does the flip-flop swap need Vd rescaled by k/ka?**
Write the two cases out:

```
case 1 (k=lo, ka=hi):  (D/V )·hi/(hi−lo)·(e^−lo·t − e^−hi·t)
case 2 (k=hi, ka=lo):  (D/V')·lo/(lo−hi)·(e^−hi·t − e^−lo·t)
```

In case 2 both the prefactor and the bracket change sign, so the
product stays positive — that is why the apparent sign change cancels.
What is left is hi/V versus lo/V′, so the curves coincide when
V′ = V·lo/hi. The time dependence is *identical* in the two cases; only
the amplitude differs, and Vd absorbs it.

**4. PFOA is nearly completely absorbed in rats — does the problem go away?**
No. It makes the **assumption a good one**, which is not the same as
making the parameter **identifiable**. The data still contain only the
ratio Vd/F; you are supplying F from outside knowledge. The difference
matters because an unidentifiable parameter fixed by assumption
transmits the assumption's error into everything downstream, silently,
with no widening of the confidence interval to warn you — which is
precisely the Zhang 2013 Vd story in lesson 09.

**Exercise (b): run section E on study 3749289.** Both studies should
give F near 1 for PFOA in rats. Agreement across independent studies is
what turns "assumed" into "established".

---

## Lesson 06 — Bayesian fitting

**0. Which band answers which question?**
Use the **wide** band (parameters + σ) to ask "is the model adequate?",
because that is where new observations should fall — roughly 95% of
real points should sit inside it. Use the **narrow** band (parameters
only) to ask "how well do we know the typical monkey's curve?" Quoting
the narrow band as if data should lie in it is the most common error in
reporting a Bayesian fit; it makes every model look broken.

**1. Where does the pooled σ go in the hierarchical model?**
Into **between-animal variation**. σ drops 0.85 → 0.48 on the log
scale, and the freed variance reappears as sd_ln_k ≈ 0.48. Half of
what the pooled model called "measurement error" was one monkey
clearing PFOA three times more slowly than the other two — a real,
persistent, animal-level property, not noise.

**2. A very tight prior, Normal(log 0.06, 0.05).**
The posterior moves toward the prior and narrows. How far it moves
measures how much the data were actually saying: with 43 observations
the likelihood is strong for the population mean, so it resists — but
it will not resist completely. The general lesson: a prior that changes
your answer is either doing legitimate work (real external knowledge)
or smuggling in a conclusion, and only you can say which.

**3. sd_ln_k with a HalfNormal(2.0) prior, from three animals.**
The posterior for sd_ln_k widens a lot and drifts up, and the
population half-life interval widens with it. Three groups carry almost
no information about a group-level standard deviation, so the prior
does most of the work. This is the standard warning about hierarchical
models on few groups: the *group means* are fine, the *variance across
groups* is barely identified. Chiu's model has the same structure but
many more studies.

**4. Why is half_life a Deterministic?**
Because ln2/mean(k) ≠ mean(ln2/k) — the transform is nonlinear, so by
Jensen's inequality the two differ, and for a convex function like 1/k
the mean of the transform is the larger. Computing it inside the model
transforms every draw and gives the correct posterior for the half-life
itself, including its (asymmetric) interval. Transforming a summary
statistic afterwards throws that away.

**Exercise (b): the PFOS monkey.** PFOS should come out slower than
PFOA. Whether the intervals overlap is the interesting part — with one
experiment per chemical, they may, and that is a real limit on what two
studies can establish.

---

## Lesson 07 — One vs two compartments

**1. Why must Vss exceed V1, and what does the gap mean?**
Vss = V1·(1 + k12/k21), and k12, k21 > 0, so the factor exceeds 1.
Physically, Vss counts the chemical sitting in tissue as well as in
the central pool, while V1 counts only what the dose initially mixed
into. The gap *is* the tissue burden — see lesson 09 section D, where
the same quantity appears as the tissue/plasma split.

**2. Why does the one-compartment half-life sit between alpha and beta?**
Least squares (or the likelihood) must fit both phases with a single
rate, so it settles on a compromise weighted by where the data are.
With many early points it is pulled toward alpha; with many late ones,
toward beta. That is also why the answer depends on the sampling
schedule — an unattractive property for a number you want to compare
across studies.

**3. If the 2-compartment model had won by less than 2·dse?**
Conclude that the data **cannot distinguish** the two structures, not
that they are equivalent. Then prefer the simpler model for prediction,
but report both if the parameter you care about differs between them —
and note that the choice is undetermined rather than settled. Here the
margin is 5.5 standard errors, so this does not arise.

**4. What stops the 2-compartment model overfitting?**
Two things. **LOO** is out-of-sample by construction: a model that fits
noise predicts held-out points *worse*, so extra parameters that buy
nothing real lower the score rather than raising it. And the
**priors** shrink the extra parameters toward sensible values, so
unsupported flexibility costs prior probability. Extra parameters are
only free in an unregularised in-sample fit, which is neither of these.

**Exercise (b): drop everything after day 28.** LOO's preference
weakens or reverses, because the terminal phase — the evidence for a
second compartment — is what you just deleted. This is the "how long
must a study run" question, answerable quantitatively.

---

## Lesson 08 — Numerical integration

**1. Why does rtol = 1e-12 cost more evaluations?**
The integrator estimates local error at each step and shrinks the step
until the estimate is under tolerance. A tighter tolerance forces
smaller steps and more right-hand-side evaluations per unit time —
1472 versus 38 across four orders of magnitude of tolerance. It is
adapting the step size, not using a finer fixed grid.

**2. Amounts or concentrations, in a ten-organ model?**
**Amounts.** Mass balance becomes "what leaves A leaves A and arrives
in B", with no volumes in the transfer terms, so a sign error or a
missing term shows up immediately as non-conservation. In
concentrations, every transfer carries a volume ratio, and a wrong
volume looks like plausible kinetics rather than an obvious bug.
Convert to concentration only for output.

**3. A mechanism giving the falling sign.**
Saturable **reabsorption**, not saturable excretion. If a transporter
in the proximal tubule pulls PFOA back *into* the blood and that
transporter saturates at high dose, then at high dose a larger fraction
of filtered chemical escapes in urine — so clearance *rises* with dose
and half-life falls. That is the opposite topology to the
Michaelis–Menten elimination in section C, and it matches the +0.11
slope measured in `../pfas_dose`. The mechanism and the sign of the
effect are tightly linked; a saturable process can push either way
depending on which direction it moves the chemical.

**4. 10 ms × 500 evaluations — how long, and what follows?**
5 seconds for the least-squares fit. At 8000 MCMC draws with several
integrations per draw, the same model takes hours to days. This is why
PBPK models are usually fitted with optimisation rather than full
Bayesian inference, why the PBPK literature leans on sensitivity
analysis instead of posteriors, and why people invest in fast ODE
solvers and surrogate models. The statistics are not the bottleneck;
the right-hand side is.

**Exercise (b): continuous input.** You will have built Chiu's human
model — which is lesson 11.

**Exercise (d): saturable model with continuous input.** If the input
rate exceeds Vmax there is **no steady state**: the concentration rises
without bound, because elimination has a ceiling and input does not.
The model is telling you something true (accumulation outruns
clearance) in an unphysical way (real animals die, or induce other
pathways). Knowing when a model's answer is a real prediction and when
it is the model leaving its domain is the skill.

---

## Lesson 09 — Volume of distribution

**1. Vd = 40 L/kg — where is the chemical?**
Almost entirely out of the blood, bound to tissue. **Yes, Vd can exceed
the animal's volume**, and routinely does, because it is not a volume
at all — it is the proportionality constant between body burden and
*plasma* concentration. A Vd of 40 L/kg means plasma concentration is
tiny relative to how much is in the body: the chemical is sequestered
somewhere that is not plasma. PFAS are at the opposite extreme
(0.1–0.5 L/kg) because they bind albumin and stay largely in plasma.

**2. Why Vss ≥ V1, and Vz ≥ Vss?**
Vss = V1·(1 + k12/k21) with both rates positive, so Vss ≥ V1.
Vz = V1·(1 + k12/(k21 − β)), and since β > 0, the denominator
k21 − β is smaller than k21, so the factor is larger: Vz ≥ Vss. The
two volumes are the same formula evaluated at two different
tissue/plasma ratios — the steady-state ratio and the terminal-phase
ratio — and the terminal phase always has proportionally more in
tissue, because the central compartment is being drained by
elimination while tissue can only return chemical through k21.

**3. Sampling to 14 days instead of 87 — which volume suffers most?**
**Vz**, because Vz = CL/β needs the terminal slope β, and truncating
the study is precisely what destroys your estimate of β. Vss needs
AUMC, which weights late points by t and so is also badly hurt — more
than CL, which needs only AUC. Ranking of damage: Vz ≈ Vss ≫ CL ≫ V1.

**4. Chiu's 430 mL/kg vs Andersson's 74 mL/kg.**
Check **which volume each estimated** before concluding either is
wrong. A serum-decay fit and a mass-balance calculation do not target
the same quantity: one may be reporting something near Vz, the other
something near V1 or Vss, and those differ threefold within a single
dataset (0.126 vs 0.405 here). Also check whether either is a
Vd/F-style composite, and what steady-state assumption each made.
Only after they are shown to target the same quantity is a
disagreement a disagreement.

**5. Vd scales with body weight, clearance does not — which is anatomy?**
**Vss = V1 + V2 is anatomy**: organ volumes and blood volume scale with
body size in a regular way, and partition coefficients are physical
chemistry that does not vary much between mammals. **CL = V1·k10 is
biochemistry**: k10 depends on transporter abundance and affinity in
the kidney, which is under genetic and hormonal control and has no
reason to track body weight. Lesson 12 section D shows exactly this —
scaling the anatomy correctly still gets clearance wrong by 3–11×.

**Exercise (c): Vss vs Vz credible intervals.** **Vz is wider**, because
it depends on β, the terminal rate, which is the least well determined
quantity in the fit. Vss depends on k12/k21, which the early data
constrain better.

**Exercise (d): set k12 = k21 = 0.** All four volumes collapse to V1,
confirming the one-compartment model is the two-compartment model with
no peripheral exchange.

---

## Lesson 10 — Sex and species

**1. What does section B still not hold fixed?**
Section E lists four (one primate experiment, the terminal-slope rule,
group means rather than individuals, body-weight differences at matched
mg/kg). Ones it misses: **age** of the animals, which affects
transporter expression; **strain**, if a study used different strains
by sex; **assay** differences if sexes were measured in separate
batches; and **publication bias** in which sex-dose combinations got
reported at all. None plausibly generates a 28× effect in a consistent
direction across 7 independent pairs, which is the actual defence — not
that nothing else varies, but that nothing else varies *enough* and
*consistently enough*.

**2. CL ratio 28×, half-life ratio 13× — what must differ?**
Vd. Since CL = k·Vd and half-life ∝ 1/k:

```
CL_F/CL_M = (k_F/k_M)·(Vd_F/Vd_M)
28.3      =  12.7    ·(Vd_F/Vd_M)
Vd_F/Vd_M ≈ 2.2
```

So female rats have roughly **twice the volume of distribution** as
well as faster elimination. That is a second, independent biological
difference hiding inside the headline number — and a reminder that a
clearance ratio and a half-life ratio are not interchangeable.

**3. Why is 10¹³ a reductio?**
Because the power law is an empirical fit over a 250-fold dose range,
and extrapolating it 10¹³-fold is meaningless. Several things break
first: the animal dies; solubility is exceeded; the transporter
saturates completely, at which point the log-log slope must fall to 0
rather than staying at 0.11 (the mechanistic ceiling argument in
`../literature/SYNTHESIS.md`). The number is not a prediction — it is a
demonstration that no physically attainable dose change could produce
the observed effect.

**4. What does section A leave open that section B closes?**
That the sexes were studied at different doses (they were — females go
to 320 mg/kg, males stop at 48.6), in different studies, with different
routes, and by different laboratories. Any of those could produce a
spurious difference between two *groups* of experiments. Matching on
study, dose and route removes all four at once, at the cost of dropping
to 7 pairs.

**5. Rats show 28×, humans do not. What follows?**
That a mechanism can be real, large, and *species-specific*. The
androgen-regulated rat transporter (Oatp/Oat family) simply is not
regulated the same way in humans. So a rat sex difference is not
evidence about human sex differences, and — more importantly — a rat
*dose* response is not automatically evidence about a human dose
response either. It is a direct caution against the extrapolation this
whole project has been testing, and it argues for the mechanistic
framing (lesson 12) over the empirical one.

**Exercise (d): dose slope by sex.** The prediction is that females
show a *flatter* slope than males. If reabsorption is weaker in
females, there is less reabsorption available to saturate, so dose
should matter less. A clean falsifiable test, and still open.

---

## Lesson 11 — Continuous dosing

**1. Css has no Vd, but the curve does. Where does Vd enter?**
Through the **rate of approach**, k = CL/Vd. Doubling Vd halves k,
which doubles the half-life and so doubles the time to reach steady
state — but leaves the final level untouched. On the figure, the curve
would rise more slowly to the same plateau. Vd sets the *timescale*,
CL sets the *destination*.

**2. "Blood should be normal within a year or two."**
Not for PFOA. Decay after cleanup follows the same half-life as
accumulation: one half-life (3.14 y) to fall by half, about 5
half-lives — **15 years** — to approach background. After 1 year the
level is still ~80% of peak. What you need to know first: the
**half-life of the specific chemical** (PFHxS at 8.3 y takes 40+
years), whether the exposure really stopped completely, and what the
remaining background exposure from food and dust is, since the level
decays toward Cbgd rather than zero.

**3. Regressing serum on current water across towns.**
You would **under-estimate** the relationship in towns where
contamination is **falling** (serum still reflects high past exposure
while water is already low — the residuals go the wrong way), and
**over-estimate** it where contamination is **rising** (serum has not
caught up, so today's high water looks like it produces little serum —
actually this also biases the slope downward). In both directions the
mismatch attenuates and scatters the relationship, because today's
water is a noisy proxy for the integrated exposure that actually
determined today's serum. Yes, it depends on the direction — and since
different towns are at different points in their histories, the
resulting bias is not even consistent across the sample.

**4. Show Css ∝ half-life at fixed Vd.**
Css = DWI·DWC/(k·Vd) and k = ln2/t½, so

```
Css = DWI·DWC·t½ / (ln2 · Vd)
```

Css is directly proportional to t½. Doubling the assumed half-life
doubles the predicted steady-state serum level from the same water — a
1:1 propagation of the half-life controversy straight into risk
assessment.

**5. Why must DWI be fixed?**
Because only the **ratio DWI/Vd** appears in the equation, so serum
data alone cannot separate them — exactly the F-versus-Vd problem from
**lesson 05**. Fixing DWI from external water-consumption data breaks
the tie and lets Vd be estimated. The cost is the same as in lesson 05
question 4: any error in the assumed DWI transmits directly into Vd
without widening its interval.

**Exercise (a): add a background term.** Css rises by Cbgd, and the
post-cleanup decline *appears* to slow and then stop, because the level
is approaching Cbgd rather than zero. Fitting such data with a model
that lacks the background term biases the half-life long — which is one
of the four bugs in the original replication (`../README.md` section 4).

---

## Lesson 12 — PBPK

**1. What does Q·(C_arterial − C_organ/P) = 0 mean?**
The organ is at **equilibrium with blood**: the concentration leaving
equals the concentration arriving, so there is no net transfer. The
organ's concentration is momentarily stationary — it is neither loading
nor unloading — and sits at exactly P times the blood concentration.
For non-eliminating organs this is the steady state; for the kidney it
never quite holds, because elimination keeps draining it.

**2. Why is elimination CLint·C_kidney/P rather than CLint·C_blood?**
Because it makes the kidney's *own* concentration the driver, so
elimination is limited by what blood actually delivers. That lets the
model express **flow-limited** clearance: as CLint grows, CL saturates
at Q rather than growing without bound
(CL_organ = Q·CLint/(Q + CLint/P)). Writing it against C_blood makes
elimination unbounded in CLint, which is physically wrong — you cannot
clear more chemical than the blood brings.

Section B's degenerate test (CLint = 0.02) shows the two forms differ
by 2.8%. At the calibrated PFOA value (CLint = 0.0039, only 0.56% of
renal blood flow) it is 0.56% — negligible, because PFOA is deeply
capacity-limited. For a compound cleared near the flow limit the two
forms diverge completely, and only the first one stays physical.

**3. Which parameters dropped out when every P was set to 1?**
The **blood flows** did — but only in the infinite-flow limit, which is
why the test has to push them up to recover k = CLint/Vtot exactly. At
real flows they emphatically do *not* drop out (the 3% gap). That is
what makes it a real test rather than a tautology: the degenerate case
is reached by a specific, checkable limit, and the *failure* to reach
it at finite flow is itself informative physiology rather than a bug.

**4. Derive Vss = Σ V_i·P_i.**
At steady state every organ satisfies question 1, so
C_i = P_i·C_blood. Total body burden is
A = Σ V_i·C_i = C_blood·Σ V_i·P_i. Volume of distribution is body
burden divided by plasma concentration:

```
Vss = A / C_blood = Σ V_i · P_i
```

For the rat model that is 0.3005 L/kg. Note it needed the
steady-state condition — which is exactly why this is Vss and not Vz.

**5. One fitted parameter per species — which, and what can you no
longer claim?**
**CLint**, because it is the parameter with no physiological table
behind it and the one the mechanism says should differ. Having fitted
it per species, you can no longer claim the model **predicts**
cross-species differences in clearance — you have calibrated the very
thing that differs. What you *can* still claim is that the model
predicts everything else (tissue distribution, dose dependence, route
differences, the shape of the curve) from physiology, with the species
difference isolated in one interpretable number you could go and
measure in vitro. That is a much weaker claim than "PBPK extrapolates
across species", and it is the honest one.

**Exercise (d): reproduce the 28× sex difference with CLint alone.**
Since PFOA is capacity-limited (CLint ≪ Q), CL is nearly proportional
to CLint, so a ~28× multiplier is needed. Whether that is plausible is
a real question — transporter expression differences of 10–30× between
sexes are reported in rat kidney, so it is at the top of the plausible
range but not absurd.

**Exercise (e): human physiology, CLint unchanged.** About 3400 days,
against an observed 1147 — the model over-predicts by ~3×, as section D
reports.

---

## If your answer disagreed

Check in this order:

1. **Run the code.** Most of these are checkable in three lines, and a
   number beats an argument.
2. **Check you answered the question asked** — several distinguish
   half-life from clearance, or scale from shape, and it is easy to
   answer the adjacent question correctly.
3. **Consider that this file might be wrong.** Two errors in the
   lessons were found by exactly this route during their construction
   (a wrong claim about CL's confidence interval in lesson 04, and a
   wrong plateau formula in lesson 09). If the code disagrees with the
   prose, the code is the evidence.
