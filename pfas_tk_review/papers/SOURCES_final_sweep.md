# SOURCES - Final Sweep

Started 2026-10-02.

## Priority 1 - DOG (only completely empty species column)

### On-disk hits (no new download needed)
1. **NJ DWQI 2017 PFOA health-based MCL support document** (`papers/NJ DWQI 2017 PFOA health-based MCL support document.txt`, line 2105)
   - Table 4 "Serum/plasma elimination half-lives of PFOA" (adapted from Lau 2012), p.45.
   - Dog: females 8-13 days, males 20-30 days. Cites **Hanhijarvi et al. (1988)**.
   - Full citation found at line 10376: "...excretion of perfluorooctanoic acid in the beagle dog and rat. In: Beynen, A.C. Solleveld, H.A. (Eds.), New Developments in Biosciences..."
2. **OEHHA 2024 PFOA PFOS PHG** (`papers/OEHHA 2024 PFOA PFOS PHG.txt`)
   - line 1850, Section 4.1 narrative: "PFOA T1/2 was 5.5-7 hours in the rabbit, **10.6-20.1 days in the dog** and 2.7-5.6 days in the Japanese macaque (Hanhijarvi et al., 1988; Kudo and Kawashima, 2003; Harada et al., 2005a)."
   - line 18249+, **Table A6.4** "Estimate of net renal tubular reabsorption of PFOA in different species" (adapted from Han et al. 2012), p.327: dog female CLR 50.8 mL/kg-day, dog male CLR 43 mL/kg-day, GFR 5300 mL/day-kg, net reabsorption 55 / 63 mL/kg-day, 52% / 59% reabsorbed. Cites **Kudo and Kawashima (2003)**.
   - Same table also present in OEHHA 2021 PFOA PFOS PHG first draft (line 18378).
   - 5 dog rows appended to db/final_sweep.csv.

### Negative results
- `ATSDR 2021 Toxicological Profile Perfluoroalkyls.txt` (2.9 MB): "dog", "dogs", "beagle", "canine" appear ONLY inside the literature-search strategy Boolean strings (lines 38974, 39087, 39170). ATSDR 2021 does **not** tabulate any dog TK value. Griffith and Long 1980 is cited ~10x in ATSDR but exclusively for **rat and mouse** acute/28-day toxicity (LC50, LD50, mortality), not dog and not TK.
- EPA 2024 PFOA and PFOS assessments mention "dogs" once each, only as the source of an assumed 20% renal blood-flow fraction for the PBPK model - not a PFAS measurement.
- EPA 2024 PFOA appendix volume, EPA 2025 IRIS PFHxS, EFSA 2020: no dog TK.
