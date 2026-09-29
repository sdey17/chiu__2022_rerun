"""
Collect the exposure actually experienced by each species, to sit next to
the fitted half-lives from harvest_pk.py.

WHY SERUM CONCENTRATION AND NOT APPLIED DOSE
--------------------------------------------
The obvious x-axis is "dose", but the two literatures do not report a
comparable one:

    animals   a single bolus, mg/kg          (one gavage or IV dose)
    humans    a daily intake, mg/kg per day  (drinking water, for years)

Those are different units and cannot be divided. Worse, the mechanism we
would be testing - saturation of a kidney transporter - depends on the
concentration AT the transporter, not on what was administered. A single
10 mg/kg dose to a rat and a lifetime of 10 ng/L water produce wildly
different serum concentrations even before any kinetics.

So the comparable exposure metric is the SERUM CONCENTRATION that was
actually measured, which both literatures report. This script collects it
per species from the raw data behind both papers.

Units: the EPA animal database stores mg/L; Chiu's human files store
ug/L. Everything here is converted to ug/L (= ng/mL).

Usage:  EPA_REPO=/path/to/CPHEA-Animal-PFAS-PK python collect_exposure.py
"""
import os
import sys

import numpy as np
import pandas as pd

CHEMS = ["PFBA", "PFBS", "PFHxA", "PFHxS", "PFOA", "PFOS", "PFNA", "PFDA"]
MG_PER_L_TO_UG_PER_L = 1000.0
# Chiu fixes drinking-water intake at this rate; used to turn a water
# concentration into a human daily dose in mg/kg/day.
HUMAN_DWI_L_PER_KG_D = np.exp(-4.3955)          # 0.0123 L/kg/day


def animal_exposure():
    """Measured serum concentrations and applied doses, per chemical/species/sex."""
    epa = os.environ["EPA_REPO"]
    sys.path.insert(0, epa)
    cwd = os.getcwd()
    os.chdir(os.path.join(epa, "pfas_notebooks"))
    try:
        from pfas_prep import PFAS
        prep = PFAS("../PFAS.db", pfas_file="../auxiliary/pfas_master.csv")
        rows = []
        for chem in CHEMS:
            for species in ["rat", "mouse", "primate"]:
                for sex in ["Male", "Female"]:
                    try:
                        d = prep.get_processed_data(chemical=chem, sex=sex,
                                                    species=species)
                    except Exception:
                        continue
                    if d is None or not len(d):
                        continue
                    serum = d.conc_mean_cor.dropna() * MG_PER_L_TO_UG_PER_L
                    serum = serum[serum > 0]
                    rows.append(dict(
                        PFAS=chem, species=species, sex=sex, n_obs=len(d),
                        serum_median=serum.median(), serum_max=serum.max(),
                        serum_min=serum.min(),
                        dose_min=d.dose.min(), dose_max=d.dose.max(),
                        dose_median=d.dose.median(), dose_units="mg/kg single"))
    finally:
        os.chdir(cwd)
    return pd.DataFrame(rows)


def human_exposure():
    """Measured serum concentrations from Chiu's training data, per chemical."""
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    from parse_chiu_data import load, FILES

    rows = []
    for chem in FILES:
        df = load(chem)
        # every measured serum value, individuals and community means alike
        serum = np.array([v for vals in df["values"] for v in vals], dtype=float)
        serum = serum[serum > 1e-6]            # drop the 1e-30 "C_0 is zero" markers
        # water concentrations the model was given, ug/L; below-MRL records
        # have no number, so use that study's MRL as an upper bound
        dwc = pd.to_numeric(df.get("dwc"), errors="coerce").dropna()
        mrl = pd.to_numeric(df.get("mrl"), errors="coerce").dropna()
        water = pd.concat([dwc, mrl]) if len(mrl) else dwc
        rows.append(dict(
            PFAS=chem, species="human", sex="Male", n_obs=len(serum),
            serum_median=np.median(serum), serum_max=serum.max(),
            serum_min=serum.min(),
            # ug/L water * L/kg/day = ug/kg/day, /1000 -> mg/kg/day
            dose_min=water.min() * HUMAN_DWI_L_PER_KG_D / 1000 if len(water) else np.nan,
            dose_max=water.max() * HUMAN_DWI_L_PER_KG_D / 1000 if len(water) else np.nan,
            dose_median=water.median() * HUMAN_DWI_L_PER_KG_D / 1000 if len(water) else np.nan,
            dose_units="mg/kg per day"))
    return pd.DataFrame(rows)


if __name__ == "__main__":
    a, h = animal_exposure(), human_exposure()
    out = pd.concat([a, h], ignore_index=True)

    pk = pd.read_csv("animal_pk.csv")
    # the human rows in animal_pk.csv carry sex="Male" as a placeholder;
    # Chiu reports one estimate for both sexes
    df = out.merge(pk, on=["PFAS", "species", "sex"], how="left")
    df.to_csv("species_exposure.csv", index=False)

    pd.set_option("display.width", 250)
    cols = ["PFAS", "species", "sex", "n_obs", "serum_median", "serum_max",
            "dose_median", "dose_units", "halft_mean", "CLC_mean"]
    print(df[cols].round(4).to_string(index=False))
    print(f"\nwrote species_exposure.csv ({len(df)} rows)")
