# Why the Python replication disagreed with Chiu et al. 2022

**Short answer:** the Python scripts do not fit the same model as Chiu's MCSim
files. They differ in two important ways and two minor ways. With all four
fixed (`model_corrected.py`), PyMC reproduces the published half-lives for all
four PFAS, including PFOA, the gap the README lists as "genuinely open":

| PFAS  | Paper, Table 3 (95% CI) | Chiu's raw `.out` chains | Original scripts* | **Corrected PyMC** (95% CI) |
|-------|-------------------------|--------------------------|-------------------|------------------------------|
| PFOA  | 3.14 (2.69, 3.73)       | 3.14 (2.68, 3.73)        | 4.30 (3.39, 5.47) | **3.16 (2.65, 3.77)**        |
| PFOS  | 3.36 (2.52, 4.42)       | 3.38 (2.54, 4.49)        | 3.10 (2.17, 4.63) | **3.36 (2.46, 4.46)**        |
| PFNA  | 2.35 (1.65, 3.16)       | 2.32 (1.58, 3.23)        | 2.74 (1.70, 4.79) | **2.27 (1.53, 3.20)**        |
| PFHxS | 8.30 (5.38, 13.5)       | 8.38 (5.54, 13.45)       | 6.62 (4.25, 11.23)| **8.51 (5.46, 13.17)**       |

Population GSD of the half-life (variability between people), PFOA: paper 1.57
(1.42, 1.73); original scripts 1.36; corrected **1.57**.

\* "Original scripts" means `model_corrected.py` with every deviation below
switched back on (`--shared-sc --drop-t0 --old-priors --no-truncate`). It
reproduces the README's own numbers (PFOA 4.30, PFOS 3.10, PFHxS 6.59, PFNA
2.89). The PFNA gap from 2.89 to 2.74 comes from a different seed and draw
count. Every row above uses 4 chains × 1000 draws after 1000 tuning steps,
target_accept 0.95; max r̂ ≤ 1.05.

---

## The four deviations

### 1. Individual time-course data: the t = 0 observation was thrown away (major; all four PFAS)

Every individual in the training sets has **two** data points in Chiu's file:

```
Print(Cserum_t, 0, 5.802);
Data (Cserum_t, 41, 29.3);     # t = 0 and t = 5.8 yr
```

All four scripts do `obs = r["data_values"][-1]` and `t_query = r["print_times"][-1]`,
so only the follow-up value enters the likelihood. In Chiu's model both values do.
That is 128 missing likelihood terms for PFOA (18 Decatur + 110 Arnsberg),
18 for PFOS, 18 for PFNA and 18 for PFHxS.

**Why it matters.** The prediction at t = 0 is just `C_0`, and with
`GSD_Cserum ≈ 1.10` the t = 0 point pins each person's `C_0` to within about
±10%. Without it, `C_0` is held only by its prior, and the study-level scale
`M_ln_C_0_sc` (prior SD 0.41, so ×/÷ 2.3 at 2 SD) is free to trade off
against `k`. Starting lower means less decay is needed to reach the
follow-up value, so k comes out smaller and the half-life longer. Measured on PFNA:

| | `M_ln_C_0_sc` (Decatur) | corr(`M_ln_C_0_sc`, `M_ln_k`) | T½ |
|---|---|---|---|
| with t = 0 data (Chiu) | −0.01 (−0.10, +0.10) | +0.01 | 2.27 |
| without (scripts)      | −0.40 (−1.03, +0.23) | **+0.49** | 2.89 |

This one change accounts for almost all of the PFNA, PFHxS and PFOS gaps.

### 2. Background and initial-concentration scales were shared across studies (major for PFOA)

In the `.in.R` files:

```
Level {                     # population
  Distrib(M_ln_k, ...) ...
  Level {                   # "Studies"
    Distrib(M_ln_Cbgd_sc, Normal, -0.22314, 0.4055);
    Distrib(M_ln_C_0_sc,  Normal,  0,       0.4055);
    Level { # Decatur ... }
    Level { # Arnsberg ... }
    Level { # Minnesota ... }
    ...
```

In MCSim, a `Distrib` inside a `Level` is drawn **once for each child** of that Level.
So every study gets its own `M_ln_Cbgd_sc` and `M_ln_C_0_sc`. Chiu's own output
header confirms this. `PFOA_1cpt_v8.MCMC_TrainTest1.out` has columns
`M_ln_Cbgd_sc(1.1)`, `M_ln_Cbgd_sc(1.2)`, … `M_ln_Cbgd_sc(1.15)`. The scripts use a
single scalar for all studies.

For PFOA the per-study posteriors from Chiu's chains are far apart:
Decatur **+0.57**, Arnsberg **−0.69**, Minnesota **−0.77**. One shared value
cannot fit all three. The model compensates through `k` and `Vd`.

README item 3 ("not a site-grouping/hierarchy issue") was right that `k` and
`Vd` have no study level. It missed that the background scales do.

### 3. Wrong PFNA priors (minor effect on the median)

| | `model_pfna.py` | Chiu's `PFNA_…in.R` |
|---|---|---|
| `M_ln_k`  | N(**−1.60944**, 0.4055) | N(**−1.80181**, 0.4055) |
| `M_ln_Vd` | N(**−1.60944**, 0.2624) | N(**−1.77196**, 0.2624) |
| `V_ln_k`  | LN(**0.12**, **1.335**) | LN(**0.20**, **1.275**) |

These values match neither the PFNA file nor the paper (prior T½ of 4.3 yr, meaning
k = 0.165 = e^−1.80). On their own they move the median very little
(2.27 → 2.28), but they narrow the variability between people (GSD_k 1.53 → 1.39).

### 4. Dose segments after the blood draw were simulated (minor; PFOA Arnsberg and PFOS Decatur)

For all 110 Arnsberg (PFOA) and all 18 Decatur (PFOS) training individuals, the
`NDoses()` schedule runs past the final measurement. For example, Arnsberg
doses run to 1.109 yr but blood is drawn at 0.9829 yr, and PFOS Decatur doses
run to 6.171 yr with the draw at 5.802 yr. The scripts build boundaries as
`dose_times + [tq]`. The scan therefore integrates *forward past* the draw and then
takes a **negative-duration** step back to it. MCSim integrates only to the
`Print()` time. Checked against a brute-force ODE solve, the error is about
+0.28 µg/L (1–2%) per PFOS person and about 0.2% for PFOA. It barely changes T½
(PFOS 3.36 → 3.28, PFOA 3.16 → 3.18).

---

## Attribution (median T½, one deviation switched on at a time)

| PFAS  | faithful | + shared scales | + drop t=0 | + old priors | + no truncation | all on |
|-------|---------:|----------------:|-----------:|-------------:|----------------:|-------:|
| PFOA  | 3.16 | 3.36 | 2.94 (GSD_k 1.31) | – | 3.18 | **4.30** (GSD_k 1.36) |
| PFOS  | 3.36 | 3.32 | 3.22 | – | 3.28 | 3.10 |
| PFNA  | 2.27 | 2.30 | **2.89** | 2.28 | – | 2.74 |
| PFHxS | 8.51 | 8.48 | **6.69** | – | – | 6.62 |

For PFOA neither major deviation explains the gap alone. It is an
**interaction**:

- Dropping t = 0 frees `C_0`.
- Sharing the scales forces Decatur, Arnsberg and Minnesota backgrounds to one
  compromise value.

With both, the only way left to fit the individual trajectories is a slower,
less variable `k`: 4.30 yr with GSD 1.36. That is why the README found "less
V_ln_k than Chiu", and why the chains, when started at Chiu's values, moved
back to 4.3. Under the misspecified model, 4.3 really is the posterior mode.

## Smaller reporting issues

- The scripts print a **90%** CI and compare it with Chiu's **95%** CI. That
  makes the Python intervals look tighter than they are.
- The `data/` folder the scripts read from is not committed. Copy the four
  `.in.R` / `.in.r` files from the chemical folders of
  <https://github.com/wachiuphd/2022-Bayes-PFAS-PK> into `data/` before running.

## Reproduce

```bash
pip install -r requirements.txt
python model_corrected.py all                          # faithful: ~1 min each; PFOA ~4 min on 4 cores
python model_corrected.py PFOA --shared-sc --drop-t0   # brings the 4.3 yr back
python model_corrected.py PFNA --drop-t0               # 2.9 yr
```

`model_corrected.py` replaces the `pytensor.scan` with the exact closed-form
solution of the linear ODE, summed over the piecewise-constant dose segments.
It matches `scipy.integrate.solve_ivp` to 4 decimals and is much faster.
