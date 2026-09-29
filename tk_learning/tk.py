"""
Shared helpers for the lessons. Deliberately small -- everything here is
something you could rewrite from scratch in ten minutes, and you should
read it before using it.

Two things live here:
  1. the analytical solutions to the compartment models (one line each)
  2. a loader for the CSVs in data/

UNITS USED EVERYWHERE
---------------------
    time            days
    concentration   mg/L   (= ug/mL; the EPA database's native unit)
    dose            mg/kg body weight
    Vd              L/kg
    CL              L/kg/day
    k               1/day

Keeping dose in mg/kg and Vd in L/kg means dose/Vd comes out in mg/L
directly, with no body weight needed. That is why PK is usually done
per kg.
"""
import os

import numpy as np
import pandas as pd

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


# ----------------------------------------------------------------------
# 1. Models
# ----------------------------------------------------------------------
def iv_1comp(t, dose, Vd, k):
    """One compartment, instantaneous IV dose.

        dC/dt = -k*C,   C(0) = dose/Vd
        =>  C(t) = (dose/Vd) * exp(-k*t)

    The whole dose appears in the blood at t=0 and decays exponentially.
    On a log-concentration axis this is a straight line of slope -k.
    """
    return (dose / Vd) * np.exp(-k * t)


def oral_1comp(t, dose, Vd, k, ka, F=1.0):
    """One compartment, first-order absorption from the gut ("gavage").

        gut:   dA/dt = -ka*A,          A(0) = F*dose
        blood: dC/dt = ka*A/Vd - k*C,  C(0) = 0

        =>  C(t) = (F*dose/Vd) * ka/(ka-k) * (exp(-k*t) - exp(-ka*t))

    Two exponentials: absorption fills the blood, elimination drains it.
    The curve rises to a peak then falls. Once absorption is finished the
    tail is governed by whichever rate is SLOWER -- usually k, but not
    always (see lesson 04).

    F is bioavailability, the fraction of the dose that gets in. It is not
    identifiable from oral data alone: only F/Vd is. Fix it at 1 unless
    you also have IV data.
    """
    t = np.asarray(t, dtype=float)
    if np.isclose(ka, k):                     # limit case, avoids 0/0
        return (F * dose / Vd) * k * t * np.exp(-k * t)
    return (F * dose / Vd) * ka / (ka - k) * (np.exp(-k * t) - np.exp(-ka * t))


def iv_2comp(t, dose, V1, k10, k12, k21):
    """Two compartments, IV dose into the central one.

        central:    dA1/dt = -(k10+k12)*A1 + k21*A2,  A1(0) = dose
        peripheral: dA2/dt = k12*A1 - k21*A2,         A2(0) = 0

    The solution is a sum of TWO exponentials, C = A*exp(-alpha*t) +
    B*exp(-beta*t), with alpha > beta. Early on, drug is both eliminated
    and distributing into tissue, so the curve falls fast; later, tissue
    gives it back and the fall is slower. A log plot bends.
    """
    t = np.asarray(t, dtype=float)
    s = k10 + k12 + k21
    disc = np.sqrt(max(s * s - 4 * k10 * k21, 0.0))
    alpha, beta = (s + disc) / 2, (s - disc) / 2          # fast, slow
    c0 = dose / V1
    A = c0 * (alpha - k21) / (alpha - beta)
    B = c0 * (k21 - beta) / (alpha - beta)
    return A * np.exp(-alpha * t) + B * np.exp(-beta * t)


# ----------------------------------------------------------------------
# 2. Derived quantities -- know these cold
# ----------------------------------------------------------------------
def half_life(k):
    """Time to fall by half. ln(2)/k, independent of dose and of Vd."""
    return np.log(2.0) / k


def clearance(k, Vd):
    """CL = k*Vd. Volume of blood fully cleared per unit time (L/kg/day).

    CL is the physiological quantity -- it is what the kidney and liver
    actually do. k is CL scaled by how big the body's PFAS pool is.
    Two chemicals can share a half-life with very different clearances.
    """
    return k * Vd


def steady_state(dose_rate, CL):
    """Css = dose_rate / CL, for continuous dosing. Vd does not appear.

    Vd controls HOW FAST you get to steady state (via k = CL/Vd), not
    WHERE steady state is.
    """
    return dose_rate / CL


def auc_iv(dose, CL):
    """Area under the curve for an IV bolus = dose/CL. Exact, model-free.

    This is the cleanest way to get CL from data: integrate the observed
    curve, divide the dose by it. No assumption about compartments.
    """
    return dose / CL


# ----------------------------------------------------------------------
# 3. Data
# ----------------------------------------------------------------------
def available():
    return sorted(f[:-4] for f in os.listdir(DATA) if f.endswith(".csv"))


def load(name):
    """Load one CSV from data/, e.g. load("PFOA_Male_primate").

    Columns:
        study       EPA reference id for the source paper
        author      first author
        route       'iv' or 'gavage'
        dose_mgkg   administered dose, mg/kg
        bw_kg       body weight
        time_d      time since dosing, days
        conc_mgL    measured serum concentration, mg/L
        conc_sd     reported SD (0 when individual animals are reported)
        n_animals   animals behind this point (1 = individual)
        animal_id   individual identifier where available
        dataset     study + dose + route: ONE experiment, the unit you fit
    """
    df = pd.read_csv(os.path.join(DATA, f"{name}.csv"))
    return df.sort_values(["dataset", "time_d"]).reset_index(drop=True)


def one_dataset(name, dataset=None, route=None, dose=None):
    """Pull a single experiment out of a file. With no filters, returns
    the dataset with the most observations."""
    df = load(name)
    if route is not None:
        df = df[df.route == route]
    if dose is not None:
        df = df[np.isclose(df.dose_mgkg, dose)]
    if dataset is not None:
        df = df[df.dataset == dataset]
    if df.dataset.nunique() > 1:
        biggest = df.dataset.value_counts().idxmax()
        df = df[df.dataset == biggest]
    return df.reset_index(drop=True)
