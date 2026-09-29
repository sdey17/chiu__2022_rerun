"""
Fit the EPA animal-PK model to one chemical / sex / species, keeping the
per-dataset clearance estimates so we can ask whether clearance depends
on dose.

    python fit_animal.py PFOA Male rat
    python fit_animal.py PFHxA Male rat

Their hierarchy's bottom level is the "dataset" = one (study, dose, route),
and each dataset gets its own clearance. So a single fit already gives us
a clearance estimate per dose level, with uncertainty.
"""
import sys, os, warnings
warnings.filterwarnings("ignore")

EPA = os.environ["EPA_REPO"]          # checkout of USEPA/CPHEA-Animal-PFAS-PK
sys.path.insert(0, EPA)
os.chdir(os.path.join(EPA, "pfas_notebooks"))   # their code uses ../ paths

import pymc as pm
# Their code targets an older PyMC, where pm.Data took mutable=True.
_orig_Data = pm.Data
pm.Data = lambda *a, **kw: (kw.pop("mutable", None), _orig_Data(*a, **kw))[1]

import arviz as az
from pfas_prep import PFAS
from PyPKMC import PyPKMC

OUT = os.path.dirname(os.path.abspath(__file__))
CHEM, SEX, SPECIES = (sys.argv[1:4] + ["PFOA", "Male", "rat"][len(sys.argv[1:4]):])
CLC_prior = {"mu": -2.89, "sd": 2.68}      # from their fit_pfoa notebook
Vdss_prior = {"mu": -1.5, "sd": 1.5}

print(f"=== {CHEM} {SEX} {SPECIES}")
prep = PFAS("../PFAS.db", pfas_file="../auxiliary/pfas_master.csv")
data = prep.get_processed_data(chemical=CHEM, sex=SEX, species=SPECIES)
print(f"{len(data)} observations, {data.hero_id.nunique()} studies, "
      f"{data.dataset_str.nunique()} datasets")

traces = {}
for mtype in ["1-compartment", "2-compartment"]:
    # Each fit takes tens of minutes, so reuse one already on disk. Delete the
    # .nc file to force a refit.
    path = f"{OUT}/{CHEM}_{SEX}_{SPECIES}_{mtype[0]}cmpt.nc"
    if os.path.exists(path):
        print(f"=== {mtype}: reusing {os.path.basename(path)}")
        traces[mtype] = az.from_netcdf(path)
        continue

    m = PyPKMC(data, time_label="time_cor", y_obs_label="conc_mean_cor",
               sd_obs_label="conc_sd_cor", route_label="route_idx",
               dose_label="dose_mg", BW_label="BW_cor", study_label="hero_id",
               dataset_label="dataset_str", indiv_label="aidx",
               CLC_prior=CLC_prior, Vdss_prior=Vdss_prior)
    try:
        m.sample(model_type=mtype, target_accept=0.99, nuts_sampler="numpyro",
                 load_trace=False, tune=10000, draws=5000, likelihood="Lognormal",
                 sample_prior=False, sample_posterior=True)
    except Exception as e:
        # Their post-sampling bookkeeping assumes older xarray/PyMC dim names.
        # The samples themselves are fine, so keep them rather than lose the run.
        print(f"!! {mtype}: sampling finished but their post-processing failed: {e}")
    traces[mtype] = m._trace
    m._trace.to_netcdf(path)
    print(f"\n=== {mtype}: divergences={getattr(m, 'N_divergences', '?')} "
          f"ok={getattr(m, 'pass_all_metrics', '?')}")
    try:
        print(m.get_pk_stats().to_string())
    except Exception as e:
        print(f"   (pk stats unavailable: {e})")

cmp = az.compare({"1-compartment": traces["1-compartment"],
                  "2-compartment": traces["2-compartment"]},
                 var_name="combined", ic="loo")
print("\n=== LOO\n", cmp.to_string())
cmp.to_csv(f"{OUT}/{CHEM}_{SEX}_{SPECIES}_loo.csv")
