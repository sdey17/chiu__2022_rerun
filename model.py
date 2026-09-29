"""
Chiu et al. 2022 one-compartment PFAS model, rewritten in PyMC.

    python model.py PFNA        # one chemical (PFOA, PFOS, PFNA or PFHxS)
    python model.py all         # all four, then a summary table

The equations are copied from Chiu's MCSim model file; the data and priors
come from data/*.in.R. Units: time in years, concentrations in ug/L,
volume of distribution Vd in L/kg, elimination rate k per year.


WHAT THIS MODEL IS DOING, IF YOU ARE NEW TO THIS
------------------------------------------------
Treat the body as a single bucket of fluid that PFAS enters through
drinking water and leaves from at a rate proportional to how much is
already in it:

    dC/dt = DWI * DWC / Vd  -  k * (C - Cbgd)
            \___ in ____/      \___ out ____/

    C    serum (blood) concentration, ug/L        <- what was measured
    DWC  drinking water concentration, ug/L       <- known from water testing
    DWI  water intake per kg body weight          <- FIXED, not fitted
    Vd   volume of distribution, L/kg             <- fitted
    k    elimination rate, per year               <- fitted; THE ANSWER
    Cbgd background level from food, dust, etc.   <- from NHANES, scaled

Half-life = ln(2) / k. That single number is what regulators use.

Nobody's k can be measured directly, and one person's blood tests cannot
pin it down. So this is a HIERARCHICAL model: each person's k is treated
as a draw from a population distribution, and the population distribution
is estimated from everyone at once. Three levels:

    population   M_ln_k, V_ln_k, M_ln_Vd, SD_ln_Vd     one set, shared
      study      M_ln_Cbgd_sc, M_ln_C_0_sc             one set PER STUDY
      person     k, Vd, DWI, Cbgd, C0                  one set PER PERSON

Everything is parameterised in LOGS, because concentrations, rates and
volumes are positive and vary multiplicatively. "M_ln_k" reads as "the
mean of ln(k)", so exp(M_ln_k) is the population's typical (geometric
mean) k.


WHY THE MODEL IS WRITTEN WITH z-SCORES
---------------------------------------
Each person's value is built as
    k_person = exp(M_ln_k + sqrt(V_ln_k) * z)   with z ~ Normal(0, 1)
rather than drawing k_person directly from its population distribution.
The two are mathematically identical, but sampling the z's gives MCMC a
much easier shape to explore. This is the standard "non-centred"
parameterisation; if a hierarchical model samples badly, it is the first
thing to try.


HOW THIS FILE IS LAID OUT
--------------------------
build_model() constructs the whole thing in four blocks, matching the
hierarchy above plus one block for community-average data:

    1. population parameters (and one measurement error per data type)
    2. study-level parameters
    3. individual people, split into three kinds of measurement:
         (a) Cserum     two blood samples, water level constant
         (b) Cserum_t   two blood samples, water level changed over time
         (c) Cbgd_Css   one blood sample, assumed at steady state
    4. community averages (M_Cserum, M_Cbgd_Css) - not individuals, so
       these need the mean OF a distribution, not the value AT its mean

fit() then runs MCMC and prints the half-life next to the paper's value.
"""
import sys

import numpy as np
import pymc as pm
import pytensor.tensor as pt

from parse_chiu_data import load

# Priors from the top of each .in.R file.
#   M_ln_k, M_ln_Vd: Normal(mean, sd) for the log of the population GM
#   V_ln_k: variance of ln(k) between people; SD_ln_Vd: SD of ln(Vd) between people
#
# These encode what was believed BEFORE seeing this data, from earlier
# half-life studies. M_ln_k = -1.8971 means a prior guess of
# exp(-1.8971) = 0.15/yr, i.e. a half-life of ln(2)/0.15 = 4.6 years, and
# sd = 0.4055 makes the prior 95% interval roughly 2.1 to 10.2 years --
# wide enough to cover the published range. PFOA was fitted first because
# it has the most data, and its fitted V_ln_k became the prior for the
# other three; that is why only PFOA uses InverseGamma here.
PRIORS = {
    "PFOA":  dict(M_ln_k=(-1.8971, 0.4055), M_ln_Vd=(-1.7720, 0.2624),
                  V_ln_k=("InverseGamma", 9, 0.75), SD_ln_Vd=0.20),
    "PFOS":  dict(M_ln_k=(-1.8971, 0.4055), M_ln_Vd=(-1.46968, 0.2624),
                  V_ln_k=("LogNormal", 0.2024, 1.261), SD_ln_Vd=0.17),
    "PFNA":  dict(M_ln_k=(-1.80181, 0.4055), M_ln_Vd=(-1.77196, 0.2624),
                  V_ln_k=("LogNormal", 0.20, 1.275), SD_ln_Vd=0.17),
    "PFHxS": dict(M_ln_k=(-2.03422, 0.4055), M_ln_Vd=(-1.38629, 0.2624),
                  V_ln_k=("LogNormal", 0.20, 1.275), SD_ln_Vd=0.17),
}

# Published population half-life, median (95% CI), from Table 3 of the paper
PAPER = {"PFOA": (3.14, 2.69, 3.73), "PFOS": (3.36, 2.52, 4.42),
         "PFNA": (2.35, 1.65, 3.16), "PFHxS": (8.30, 5.38, 13.5)}

# Drinking-water intake per kg body weight is FIXED in Chiu's model, not fitted.
# It comes from a national food-and-water survey, not from this data, so it
# enters as a known distribution: people vary around it (SD on the log scale
# of 0.888, i.e. a spread of about e^0.888 = 2.4x), but the data never
# updates it.
LN_DWI_MEAN, LN_DWI_SD = -4.3955, 0.888     # log(L/kg per day)
DAYS = 365.25                                # intake is per day, k is per year


def build_model(chem):
    df = load(chem)
    if "dwc" not in df:
        df["dwc"] = np.nan
    # Each record belongs to a study (a contaminated town). Number them 0,1,2...
    # so study-level parameters can be indexed by position.
    studies = list(dict.fromkeys(df["study"]))
    df["s"] = df["study"].map(studies.index)          # study number, 0, 1, 2, ...
    p = PRIORS[chem]

    with pm.Model() as model:
        # ---------- 1. Population level: shared by everyone ----------
        # M_ln_k is the log of the typical elimination rate; V_ln_k is how
        # much ln(k) VARIES between people (a variance, not an SD - hence
        # sqrt(V_ln_k) wherever a standard deviation is needed).
        M_ln_k = pm.Normal("M_ln_k", *p["M_ln_k"])
        M_ln_Vd = pm.Normal("M_ln_Vd", *p["M_ln_Vd"])
        dist, gm, gsd = p["V_ln_k"]
        if dist == "InverseGamma":
            V_ln_k = pm.InverseGamma("V_ln_k", alpha=gm, beta=gsd)
        else:                    # MCSim writes LogNormal as (GM, GSD)
            # MCSim's LogNormal(a, b) means median a and geometric SD b, so
            # translating to PyMC's (mu, sigma) on the log scale needs logs
            # of both. Getting this convention wrong is an easy silent bug.
            V_ln_k = pm.LogNormal("V_ln_k", mu=np.log(gm), sigma=np.log(gsd))
        SD_ln_Vd = pm.HalfNormal("SD_ln_Vd", p["SD_ln_Vd"])

        # Deterministic = not sampled, just computed from the above and
        # recorded, so the posterior comes out in useful units.
        pm.Deterministic("halflife", np.log(2) / pt.exp(M_ln_k))   # the answer we want
        pm.Deterministic("halflife_GSD", pt.exp(pt.sqrt(V_ln_k)))  # spread between people
        pm.Deterministic("Vd", pt.exp(M_ln_Vd))

        # Measurement error, one per data type. LogUniform(1.1, 10) prior.
        # This is the scatter left between prediction and measurement after
        # person-to-person differences are accounted for. It is a GSD, so
        # 1.1 means "predictions land within about 10%". Each data type gets
        # its own: a single blood draw is noisier than a time course, and a
        # community average is noisier still.
        def error_gsd(name):
            return pt.exp(pm.Uniform(f"log_GSD_{name}", np.log(1.1), np.log(10)))

        # ---------- 2. Study level: one value PER STUDY ----------
        # Background serum level scale and initial level scale.
        #
        # `shape=n` is the whole point: MCSim declares these inside its
        # "Studies" Level, which gives one copy per study, and the fitted
        # values really do differ between towns (Decatur +0.57, Arnsberg
        # -0.69, Minnesota -0.77 in Chiu's own chains). Collapsing them to
        # one shared number is what broke the earlier version of this
        # replication - see README section 4.
        n = len(studies)
        M_ln_Cbgd_sc = pm.Normal("M_ln_Cbgd_sc", -0.22314, 0.4055, shape=n)
        M_ln_C_0_sc = pm.Normal("M_ln_C_0_sc", 0.0, 0.4055, shape=n)

        # Water concentration of each record: a known number, or, when it was
        # only reported as "below the MRL", a free parameter per study.
        # MRL = minimum reporting level, the lowest concentration the water
        # test could resolve. "Below the MRL" means the true value is
        # somewhere in [0, MRL], so the model fits it as an unknown with a
        # flat prior over that range rather than guessing a number.
        dwc_free = {s: pm.Uniform(f"DWC_below_MRL_{s}", 0, mrl)
                    for s, mrl in df.groupby("s")["mrl"].first().dropna().items()}

        def water_conc(rows):
            return [dwc_free[r.s] if np.isnan(r.dwc) else r.dwc for r in rows.itertuples()]

        # ---------- 3. Individual level: one value PER PERSON ----------
        def person_params(rows, name):
            """Each person's k, Vd, intake, background and starting level.

            One standard-normal z per person per quantity (the non-centred
            trick from the module docstring), turned into real values by
            the population mean and spread. `rows["s"]` picks out which
            study each person belongs to, so they get that study's
            background scale.
            """
            z = {v: pm.Normal(f"z_{v}_{name}", 0, 1, shape=len(rows))
                 for v in ["k", "Vd", "DWI", "Cbgd", "C0"]}
            s = rows["s"].values
            k = pt.exp(M_ln_k + pt.sqrt(V_ln_k) * z["k"])
            Vd = pt.exp(M_ln_Vd + SD_ln_Vd * z["Vd"])
            DWI = pt.exp(LN_DWI_MEAN + LN_DWI_SD * z["DWI"])
            # Cbgd_in_gm / Cbgd_in_gsd are this person's NHANES-based prior
            # background, already in the data file; the study-level scale
            # shifts the whole study's backgrounds up or down together.
            Cbgd = rows["Cbgd_in_gm"].values * pt.exp(
                M_ln_Cbgd_sc[s] + np.log(rows["Cbgd_in_gsd"].values) * z["Cbgd"])
            C0 = rows["C_0_in_gm"].values * pt.exp(
                M_ln_C_0_sc[s] + np.log(rows["C_0_in_gsd"].values) * z["C0"])
            return k, Vd, DWI, Cbgd, C0

        # (a) Two blood samples, t = 0 and t = T, constant water (PFNA, PFHxS)
        # Closed-form solution of the differential equation for constant DWC:
        # start at C0, decay toward the steady state Css at rate k.
        rows = df[df.endpoint == "Cserum"]
        if len(rows):
            k, Vd, DWI, Cbgd, C0 = person_params(rows, "Cserum")
            T = np.array([r[-1] for r in rows["times"]])
            Css = DWI * DAYS * pt.stack(water_conc(rows)) / (k * Vd)      # steady state from water
            C_T = Cbgd + (C0 - Cbgd) * pt.exp(-k * T) + Css * (1 - pt.exp(-k * T))
            observe("Cserum", C0, C_T, rows, error_gsd("Cserum"))

        # (b) Two blood samples, water level changed over time (PFOA, PFOS)
        # Here DWC is a step function: the town's water was tested repeatedly
        # and the level changed (contamination, then filters installed, etc).
        rows = df[df.endpoint == "Cserum_t"]
        if len(rows):
            k, Vd, DWI, Cbgd, C0 = person_params(rows, "Cserum_t")
            T, start, end, conc = dose_table(rows)
            # dC/dt = DWI*DWC(t)/Vd - k*(C - Cbgd), solved exactly for a water
            # level that is constant within each segment [start, end]:
            #
            # the equation is linear, so the answer is the decayed starting
            # level plus the sum of each segment's contribution, each one
            # decayed from its own time to the blood-draw time T. No
            # numerical integration needed - and this is much faster than
            # stepping through segments in a loop.
            kc = k[:, None]
            washin = pt.sum(conc * (pt.exp(-kc * (T[:, None] - end)) -
                                    pt.exp(-kc * (T[:, None] - start))), axis=1)
            C_T = Cbgd + (C0 - Cbgd) * pt.exp(-k * T) + DWI * DAYS / (k * Vd) * washin
            observe("Cserum_t", C0, C_T, rows, error_gsd("Cserum"))

        # (c) One blood sample at steady state (t ~ 0), known water level (Minnesota)
        # With only one sample there is no decay curve to observe, so the
        # model assumes the person had reached steady state. Note this
        # constrains only the PRODUCT k*Vd, not k by itself -- these records
        # help pin down clearance, while the time courses above are what
        # actually identify k.
        rows = df[df.endpoint == "Cbgd_Css"]
        if len(rows):
            k, Vd, DWI, Cbgd, _ = person_params(rows, "Cbgd_Css")
            C = Cbgd + DWI * DAYS * rows["dwc"].values / (k * Vd)
            pm.LogNormal("obs_Cbgd_Css", mu=pt.log(C), sigma=pt.log(error_gsd("Cbgd_Css")),
                         observed=np.array([v[0] for v in rows["values"]]))

        # ---------- 4. Population averages (whole-community means) ----------
        # E[X] of a lognormal X is exp(mu + var/2). Formulas from Chiu's
        # CalcOutputs{} block; t is time since the water was cleaned up.
        #
        # Some studies report only "the average blood level in this town",
        # not individuals. The average OF a population is not the value you
        # get by plugging in average parameters: for a lognormal quantity
        # E[X] = exp(mu + var/2), which exceeds exp(mu). Ignoring that
        # (Jensen's inequality) would bias the fit.
        def lognormal_mean(mu, var):
            return pt.exp(mu + var / 2)

        for endpoint in ["M_Cserum", "M_Cbgd_Css"]:
            rows = df[df.endpoint == endpoint]
            if not len(rows):
                continue
            preds, obs = [], []
            for r, dwc in zip(rows.itertuples(), water_conc(rows)):
                sd_bg, sd_c0 = np.log(r.Cbgd_in_gsd), np.log(r.C_0_in_gsd)
                mu_bg = np.log(r.Cbgd_in_gm) + M_ln_Cbgd_sc[r.s]
                mu_c0 = np.log(r.C_0_in_gm) + M_ln_C_0_sc[r.s]
                mu_ss = LN_DWI_MEAN + pt.log(DAYS * dwc) - M_ln_k - M_ln_Vd
                var_ss = LN_DWI_SD**2 + V_ln_k + SD_ln_Vd**2
                for t, y in zip(r.times, r.values):
                    # -k*t treated as normal with matching mean and variance
                    # (an approximation Chiu makes: exp(-k*t) has no neat
                    # closed-form average over a lognormal k, so he matches
                    # the first two moments instead. He reports errors under
                    # 10% for t up to about twice the half-life.)
                    mu_kt = -t * pt.exp(M_ln_k + V_ln_k / 2)
                    var_kt = (pt.exp(V_ln_k) - 1) * mu_kt**2
                    bg = lognormal_mean(mu_bg, sd_bg**2)
                    ss_decayed = lognormal_mean(mu_ss + mu_kt, var_ss + var_kt)
                    if endpoint == "M_Cbgd_Css":
                        # background + what is left of the steady-state load
                        preds.append(bg + ss_decayed)
                    else:
                        # the same curve as (a), but every term averaged
                        # across the population one at a time
                        preds.append(bg
                                     + lognormal_mean(mu_c0 + mu_kt, sd_c0**2 + var_kt)
                                     - lognormal_mean(mu_bg + mu_kt, sd_bg**2 + var_kt)
                                     + lognormal_mean(mu_ss, var_ss)
                                     - ss_decayed)
                    obs.append(y)
            pm.LogNormal(f"obs_{endpoint}", mu=pt.log(pt.stack(preds)),
                         sigma=pt.log(error_gsd(endpoint)), observed=np.array(obs))
    return model


def observe(name, C0, C_T, rows, gsd):
    """Likelihood for BOTH blood samples of each person (t = 0 and t = T).

    Both samples matter. The prediction at t = 0 is simply C0, so that
    first point is what pins down where each person started; without it C0
    drifts and drags the elimination rate with it. Dropping it is exactly
    what went wrong in the earlier version of this replication (README
    section 4).

    LogNormal because concentrations are positive and the error is
    multiplicative -- "within 20%", not "within 2 ug/L".
    """
    first = np.array([v[0] for v in rows["values"]])
    last = np.array([v[-1] for v in rows["values"]])
    pm.LogNormal(f"obs_{name}_t0", mu=pt.log(C0), sigma=pt.log(gsd), observed=first)
    pm.LogNormal(f"obs_{name}_T", mu=pt.log(C_T), sigma=pt.log(gsd), observed=last)


def dose_table(rows):
    """Water-level segments per person, clipped at the blood-draw time T.

    Returns three (people x segments) arrays plus the draw times. People
    have different numbers of segments, so shorter rows are left as zeros,
    which contribute nothing to the sum in block (b).

    The clipping matters: some dosing records run past the date the blood
    was actually taken, and a segment after the measurement must not
    contribute to it.
    """
    T = np.array([r[-1] for r in rows["times"]])
    width = max(len(c) for c in rows["dose_conc"])
    start, end, conc = (np.zeros((len(rows), width)) for _ in range(3))
    for i, (times, c) in enumerate(zip(rows["dose_times"], rows["dose_conc"])):
        edges = np.minimum(list(times) + [T[i]], T[i])   # nothing after the draw
        start[i, :len(c)], end[i, :len(c)], conc[i, :len(c)] = edges[:-1], edges[1:], c
    return T, start, end, conc


def fit(chem, draws=1000, cores=4):
    """Run MCMC and report the half-life next to the published value.

    NUTS (PyMC's default sampler) explores the posterior by simulating a
    particle rolling over the log-posterior surface. `tune` steps are spent
    learning a good step size and then discarded; `draws` are kept. Four
    chains start from different points so that r_hat can check they agree.
    """
    with build_model(chem):
        idata = pm.sample(draws, tune=draws, chains=4, cores=cores,
                          target_accept=0.95, random_seed=1)
    post = idata.posterior
    hl = np.percentile(post["halflife"], [50, 2.5, 97.5])
    gsd = np.median(post["halflife_GSD"])
    div = int(idata.sample_stats["diverging"].sum())
    print(f"\n{chem}: half-life {hl[0]:.2f} yr (95% CI {hl[1]:.2f}-{hl[2]:.2f}), "
          f"paper {PAPER[chem][0]} ({PAPER[chem][1]}-{PAPER[chem][2]}); "
          f"GSD between people {gsd:.2f}; divergences {div}")
    idata.to_netcdf(f"results_{chem}.nc")
    return hl, gsd


if __name__ == "__main__":
    chems = list(PRIORS) if sys.argv[1:] in ([], ["all"]) else sys.argv[1:]
    results = {c: fit(c) for c in chems}
    print("\nChemical  Python median (95% CI)    Paper median (95% CI)")
    for c, (hl, _) in results.items():
        p = PAPER[c]
        print(f"{c:8s}  {hl[0]:5.2f} ({hl[1]:.2f}-{hl[2]:.2f})        {p[0]:5.2f} ({p[1]}-{p[2]})")
