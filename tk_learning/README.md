# Learning toxicokinetic modelling, from one compartment to PBPK

Seven runnable lessons on real PFAS animal data, building from
`C(t) = C0·exp(-k·t)` to the point where you can see for yourself why
physiologically based models exist.

Each lesson is a script you run. It prints tables, explains what to look
at, and ends with questions and exercises. Do the questions — they are
the point. The scripts are short enough to read in full, and you should.

```bash
pip install -r requirements.txt           # or: numpy scipy pandas pymc arviz

python 01_simulate.py          # no data yet: what the knobs do
python 02_explore.py           # look at the data before modelling it
python 03_loglinear.py         # the classic method, and its three traps
python 04_nls.py               # nonlinear least squares, residuals, AUC
python 05_oral.py              # gavage dosing and identifiability
python 06_bayes.py             # the same model in PyMC; hierarchy      (~1 min)
python 07_two_compartment.py   # where 1-compartment fails -> PBPK      (~3 min)
```

`tk.py` holds the model equations and the data loader. Read it first —
it is 150 lines and every one of them is something you should be able to
derive.

## The arc

| lesson | what you can do afterwards | the idea it lands |
|---|---|---|
| 01 | simulate any 1-compartment scenario | half-life is set by k alone; dose and Vd only slide the curve |
| 02 | read a PK dataset critically | a bending log-curve means one compartment is not enough |
| 03 | get a half-life from a spreadsheet | "terminal half-life" hides a judgement call about where to start the line |
| 04 | fit any model you can write down | residual patterns diagnose the model; AUC checks it without one |
| 05 | fit oral data, and know when not to | oral data alone confounds F with Vd, and k with ka |
| 06 | fit hierarchically with uncertainty | partial pooling; exact intervals on derived quantities |
| 07 | choose between structures by LOO | a fitted compartment is not an organ — which is what PBPK fixes |

## The data

`data/` holds five CSVs exported from the EPA's animal PFAS database
([USEPA/CPHEA-Animal-PFAS-PK](https://github.com/USEPA/CPHEA-Animal-PFAS-PK)),
so the lessons run with no database and no network.

| file | rows | experiments | note |
|---|---|---|---|
| `PFOA_Male_primate.csv` | 43 | 1 | 10 mg/kg IV, 3 monkeys, 123 days — the cleanest decay curve there is |
| `PFOS_Male_primate.csv` | 48 | 1 | 2 mg/kg IV, 161 days |
| `PFOA_Male_rat.csv` | 860 | 14 | 6 studies, 0.1–49 mg/kg, IV and gavage |
| `PFOA_Female_rat.csv` | 377 | 13 | females clear PFOA ~44× faster than males |
| `PFOS_Male_rat.csv` | 246 | 9 | 0.1–20 mg/kg |

Columns: `study, author, route, dose_mgkg, dose_mg, bw_kg, time_d,
conc_mgL, conc_sd, n_animals, animal_id, dataset`. One row per measured
serum concentration; `dataset` identifies one experiment (study + dose +
route), which is the unit you fit.

Units throughout: **days, mg/L, mg/kg, L/kg, L/kg/day, 1/day**.

## The equations, all of them

**One compartment, IV bolus**

```
dC/dt = -k·C,  C(0) = dose/Vd        C(t) = (dose/Vd)·exp(-k·t)
```

**One compartment, first-order oral absorption**

```
dA/dt = -ka·A,              A(0) = F·dose          (gut)
dC/dt = ka·A/Vd - k·C,      C(0) = 0               (blood)

C(t) = (F·dose/Vd)·ka/(ka-k)·(exp(-k·t) - exp(-ka·t))
```

**Two compartments, IV bolus**

```
dA1/dt = -(k10+k12)·A1 + k21·A2,   A1(0) = dose    (central)
dA2/dt =  k12·A1      - k21·A2,    A2(0) = 0       (peripheral)

C(t) = A·exp(-alpha·t) + B·exp(-beta·t),   alpha > beta
```

**Derived quantities**

| quantity | formula | what it means |
|---|---|---|
| half-life | `ln2 / k` | time to halve; independent of dose and Vd |
| clearance | `CL = k·Vd` | volume of blood fully cleared per unit time — the physiological quantity |
| steady state | `Css = dose_rate / CL` | Vd does not appear |
| AUC (IV) | `dose / CL` | exact for any linear model, no shape assumption |
| Vss (2-comp) | `V1·(1 + k12/k21)` | total distribution volume once tissue has filled |

## Eight things the lessons will make you believe

1. **Half-life is the robust number; clearance is the meaningful one.**
   k comes off the slope and needs neither dose nor volume. CL needs Vd,
   and Vd is the shakiest quantity in PK. This one fact explains a
   17-fold published disagreement about human PFOA — see
   `../literature/SYNTHESIS.md` §2.
2. **Fit on the log scale.** It is a statement about the error model
   (multiplicative noise), not a convenience.
3. **Read the residuals, not R².** Lesson 03 produces four different
   half-lives all with R² > 0.93.
4. **"Terminal half-life" contains a judgement call** about where the
   terminal phase begins. Different labs make it differently.
5. **Oral data alone cannot separate F from Vd, or k from ka.** An IV
   arm fixes both. Design beats statistics.
6. **Check against a model-free quantity.** `CL = dose/AUC` holds for
   any linear model; if your fit disagrees, your structure is wrong.
7. **Partial pooling is the default, not an advanced technique.** Three
   monkeys differ threefold; a pooled fit calls that "noise".
8. **A fitted compartment is not an organ.** Which is where PBPK starts.

## Then what

The parent repository is what these lessons are preparation for:

- `../model.py` — Chiu et al. 2022's human model: the same one-compartment
  equation, with drinking-water input, fitted hierarchically over
  population → study → person. You now have everything needed to read it.
- `../pfas_dose/` — the EPA animal pipeline: 1- vs 2-compartment chosen by
  LOO, per-dataset clearance, then a meta-regression asking whether
  clearance depends on dose.
- `../species_dose/` — using those fits to test whether the human/rodent
  half-life gap is really a dose gap. (It is not.)
- `../SUMMARY.md` — what the whole project found.

For PBPK itself, the natural next steps are the `httk` R package (which
has PFAS models), and Fischer et al. 2025's PBTK sensitivity analysis
(`../literature/fulltext/`), which asks which physiological parameters
actually control PFAS elimination — the question compartmental models
cannot pose.
