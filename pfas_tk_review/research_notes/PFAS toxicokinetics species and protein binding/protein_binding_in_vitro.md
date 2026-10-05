# In vitro measurements of PFAS binding to serum albumin and other toxicokinetically relevant proteins

**Companion files produced by this work stream**
- Structured database: `pfas_tk_review/db/protein_binding.csv`
  (273 rows, 54 distinct study-years, 30 distinct protein/matrix targets, 15 rows flagged
  `is_computational=yes`)
- Retrieval log incl. every failure: `pfas_tk_review/papers/SOURCES_binding.md`
- Full-text `.txt` extractions (tables flattened) for 9 papers in
  `pfas_tk_review/papers/`

**Two cautions for the report writer.** (1) **No PDFs could be downloaded** — the agent
proxy blocked every PMC and publisher PDF endpoint tried, so the deliverable is `.txt`
extractions from JATS full-text XML plus abstract-level records. (2) A large share of the
numbers below are **ranges across congeners taken from the compilation table of a review**
(Starnes & Belcher 2026, Table 1) because the primary papers are paywalled. Every such row
in the CSV carries `source_table = "secondary (Starnes & Belcher 2026 Table 1)"`. Where I
reached the primary paper I say so.

---

## Q1/Q2. For each PFAS and each protein, what is the measured binding affinity?

### Takeaway
The only dataset that covers a wide PFAS space, several proteins, and a physiologically
realistic ligand:protein ratio in one internally consistent experiment is Fischer et al.
2024 (32 PFAS × HSA, BSA, γ-globulin, whole serum, by C18-SPME depletion). Everything else
is fragmentary: albumin dominates the literature (≈85% of my rows), L-FABP and
transthyretin have only rank orders or relative potencies, and for haemoglobin,
thyroxine-binding globulin and lipoproteins there are essentially no absolute constants at all.

### Cited Findings

**Fischer et al. 2024 — the backbone dataset (primary, Table S2 recovered in full).**
Protein–water distribution coefficients, log D (L_water per kg_protein), by C18-SPME fibre
depletion, 37 °C, PBS pH 7.4, 48 h, PFAS:protein molar ratio ≤0.004 (HSA/BSA) and ≤0.009
(γ-globulin) — i.e. ~100× below the ratio at which BSA saturation has been observed —
[Fischer et al. 2024, Environ Sci Technol 58:1055–1063](https://doi.org/10.1021/acs.est.3c07415):

| Chemical | η_pfc | log D_HSA/w | log D_BSA/w | log D_glob/w | log D_serum/w |
|---|---|---|---|---|---|
| PFBA | 3 | N.D. | N.D. | N.D. | N.D. |
| PFPeA | 4 | 2.16 | N.D. | N.D. | 2.21 |
| PFHxA | 5 | 3.20 | 2.83 | 1.73 | 1.99 |
| PFHpA | 6 | 4.10 | 3.93 | 1.81 | 2.49 |
| PFOA | 7 | 4.48 | 4.20 | 2.16 | 2.85 |
| PFNA | 8 | 4.49 | 4.54 | 2.81 | 2.99 |
| PFDA | 9 | 4.73 | 4.81 | 3.67 | 3.40 |
| PFUnDA | 10 | 5.18 | 5.17 | 4.64 | 3.87 |
| PFDoDA | 11 | 5.05 | 5.12 | 4.81 | 3.62 |
| PFTriDA | 12 | 4.54 | 4.47 | 4.33 | 3.08 |
| PFTeDA | 13 | 3.87 | 3.87 | 4.00 | 3.00 |
| PFBS | 4 | 3.26 | 2.28 | 2.03 | N.D. |
| PFPeS | 5 | 3.98 | 4.00 | 1.85 | 2.40 |
| PFHxS | 6 | 4.77 | 4.61 | 1.95 | 3.30 |
| PFHpS | 7 | **5.49** | 4.88 | 2.47 | 3.38 |
| PFOS | 8 | 4.62 | 4.76 | 3.33 | 3.09 |
| PFNS | 9 | 4.99 | 5.14 | 4.49 | 3.74 |
| PFDS | 10 | 5.05 | 5.13 | 4.96 | 3.90 |
| FBSA | 4 | N.D. | N.D. | N.D. | N.D. |
| FHxSA | 6 | N.D. | N.D. | 2.21 | 3.01 |
| FOSA | 8 | 4.34 | 4.33 | 3.03 | 2.79 |
| FOSAA | 8 | 4.31 | 4.30 | 2.96 | 3.01 |
| N-MeFOSAA | 8 | 4.27 | 4.29 | 3.45 | 3.02 |
| N-EtFOSAA | 8 | 4.23 | 4.29 | 3.76 | 3.06 |
| FDSA | 10 | 4.64 | 4.69 | 4.95 | 3.65 |
| 4:2 FtS | 4 | N.D. | N.D. | N.D. | N.D. |
| 5:3 FTCA | 5 | 3.48 | 2.90 | 2.30 | 2.62 |
| 6:2 FtS | 6 | 3.35 | 3.44 | 2.43 | 2.55 |
| 7:3 FTCA | 7 | 3.59 | 3.79 | 2.49 | 2.74 |
| 8:2 FtS | 8 | 4.39 | 4.49 | 3.52 | 3.08 |
| 10:2 FtS | 10 | 4.68 | 4.88 | 4.56 | 3.41 |
| **ADONA** | 6 | 3.98 | 3.84 | 2.34 | 2.75 |

N.D. = not detected (binding too high or too low, or insufficient method sensitivity).
Standard errors (±0.02–0.40 log units) are in the CSV's source paper, not reproduced here.
**GenX/HFPO-DA, F-53B/6:2 Cl-PFESA and PFECAs other than ADONA are NOT in this dataset** —
a genuine coverage gap in the single best study.

**Starnes et al. 2024 — the only quantitative cross-species albumin comparison (primary,
Table 2).** Differential scanning fluorimetry (DSF), Kd in **mM**, 0–1000 µM PFAS,
HEPES-buffered saline pH 7.4 — [Starnes et al. 2024, Toxicol Sci 199:132–149](https://doi.org/10.1093/toxsci/kfae028):

| Chemical | HSA Kd (mM) | BSA Kd (mM) | PSA Kd (mM) | RSA Kd (mM) |
|---|---|---|---|---|
| PFBA | 2.64 (0.22) | 3.06 (0.27) | 1.28 (0.03) | 1.90 (0.09) |
| PFHxA | 1.71 (0.22) | 2.17 (0.06) | 0.95 (0.02) | 1.33 (0.02) |
| PFOA | 0.79 (0.09) | 0.99 (0.01) | 0.37 (0.01) | 0.40 (0.01) |
| PFBS | 1.68 (0.09) | 0.80 (0.03) | 1.25 (0.02) | 1.41 (0.03) |
| PFOS | 0.69 (0.02) | 0.86 (0.05) | 0.38 (0.06) | 0.42 (0.10) |
| HFPO-DA (GenX) | 1.57 (0.03) | 2.55 (0.13) | 2.12 (0.03) | 1.64 (0.05) |
| 6:2 FTSA | 0.41 (0.04) | 1.39 (0.04) | 0.52 (0.03) | 0.33 (0.02) |
| 6:2 FTOH | **nonbinding** | nonbinding | nonbinding | nonbinding |

The neutral fluorotelomer alcohol 6:2 FTOH was not bound by albumin of **any** of the four
species, which the authors take as evidence that the charged head group is required for
albumin binding.

**Alesio & Bothun 2024 — BSA, DSF, Ka at 61 °C (primary, Table 2),
[Sci Rep 14:6501](https://doi.org/10.1038/s41598-024-57140-9):** PFOA 2.44 (0.40) ×10⁴ M⁻¹;
PFNA 96.6 (52.8) ×10⁴; PFDA 0.33 (0.26) ×10⁴; GenX 1.98 (0.41) ×10⁴; PFBS 2.08 (0.61) ×10⁴;
PFHxS 9.40 (3.30) ×10⁴; PFOS 2.73 (1.38) ×10⁴. Reference ligands on the same plate:
octanoic acid 0.77×10⁴, nonanoic acid 293×10⁴, decanoic acid 3.62×10⁴, warfarin 9.37×10⁴.

**Peng et al. 2024 — HSA, fluorescence quenching + Sudlow-site competition (primary,
Tables 2–3), [Toxics 12:43](https://doi.org/10.3390/toxics12010043).** Kb (L/mol) at 310 K
and, in brackets, at 298 K; n = number of binding sites at 310 K:
PFNA 9.9×10⁴ [7.81×10⁶], n 1.10; **HFPO-TA 2.31×10⁹** [3.7×10⁶], n 2.09;
PFOA 1.98×10⁶ [2.27×10⁵], n 1.47; PFO3DA 2.99×10⁴ [1.59×10⁵], n 1.10;
PFHpA 7.47×10⁵ [4.53×10³], n 1.50; DFSA 2.07×10⁴ [1.52×10³], n 1.13.
Note the non-monotonic and in places implausible temperature dependence (PFNA falls ~80-fold
from 298→310 K while HFPO-TA rises ~600-fold).

**Wu et al. 2024 — HSA, fluorescence quenching, the low-value outlier (primary, Tables 4–6),
[Toxics 12:46](https://doi.org/10.3390/toxics12010046).** KA in M⁻¹ and n:
PFBA 20.4 (n 0.469); PFPrS 79.5 (0.649); PFOA 103.3 (0.681); PFBS 116.5 (0.699);
9Cl-PF3ONS/F-53B 117.1 (0.724); 11Cl-PF3OUdS 127.6 (0.710); PFHxS 157.9 (0.733);
NaDONA 93.1 (0.672); HFPO-DA 59.0 (0.621); PFOS 394.6 (0.869). These are **two to four orders
of magnitude below every other fluorescence-quenching study** of the same compounds.

**Moro et al. 2022 — defatted HSA, isothermal titration calorimetry (primary, Table 1),
[Chem Res Toxicol 35:2049–2058](https://doi.org/10.1021/acs.chemrestox.2c00211).** KD in µM
at 298 K / 310 K, with n: C6O4 2.4 / 5.4 (n 1.6 / 1.5); PFHxA 4.5 / 5.9 (n 1.02 / 1.03);
HFPO-DA fitted to a **sequential** model, KD1 19.0 / 9.9 and KD2 84.2 / 27.0; PFOA fitted to
**two sets of sites**, high-affinity KD 0.4 / 39.3 (n 0.89 / 0.95) and low-affinity
KD 29.7 / 46.0 (n 4.5 / 9.5).

**Chen & Guo 2009 — HSA, the site-resolved dataset (abstract),
[Arch Toxicol 83:255–261](https://doi.org/10.1007/s00204-008-0359-x).** Trp214 quenching:
PFOA Ka 2.7×10⁵ M⁻¹, PFOS 2.2×10⁴ M⁻¹. **PFBA and PFBS produced no fluorescence change at
all**, so no Ka could be derived by quenching. Fluorescence displacement instead: at Sudlow
site I (dansylamide probe) PFBA Ka 1.0×10⁶ and PFBS 2.2×10⁶ M⁻¹; at Sudlow site II
(dansyl-L-proline) PFBS 6.5×10⁶ and PFDoA 1.2×10⁶ M⁻¹, while PFBA did not bind site II.

**Han et al. 2003 — rat and human albumin, separative + NMR (abstract),
[Chem Res Toxicol 16:775–781](https://doi.org/10.1021/tx034005w).** PFOA Kd 0.3–0.4 mM with
**n = 6–9 binding sites** on both RSA and HSA by microdesalting-column separation; ~0.3 mM by
¹⁹F NMR; no significant RSA vs HSA difference; serum albumin identified as the primary
PFOA-binding plasma protein in both sexes.

**Beesoon & Martin 2015 — isomer-resolved HSA Kd by ultrafiltration (abstract),
[Environ Sci Technol 49](https://doi.org/10.1021/es505399w).** linear PFOS
Kd = 8(±4)×10⁻⁸ M (Ka = 1.25×10⁷ M⁻¹) versus branched PFOS isomers 8(±1)×10⁻⁵ to
4(±2)×10⁻⁴ M — a ~1000–5000-fold isomer difference. linear PFOA Kd = 1(±0.9)×10⁻⁴ M versus
branched PFOA 3–4(±2)×10⁻⁴ M.

**Bischel et al. 2010/2011 — the methodologically careful equilibrium-dialysis work
(abstracts).** BSA/PFOA and BSA/PFNA primary Ka ~10⁶ M⁻¹ with **1–3 primary binding sites**;
by nanoESI-MS on the same systems Ka ~10⁵ M⁻¹ (PFOA, PFNA) and ~10⁴ M⁻¹ (PFDA, PFOS) with
**up to 8 occupied sites at a 4:1 ratio** —
[Environ Sci Technol 44:5263–5269](https://doi.org/10.1021/es101334s). For the short chains,
log K_protein-water = **3.3–4.3** for C4–C12 PFAAs, with PFBS and PFPeA reaching Ka ~10⁶ M⁻¹ —
[Environ Toxicol Chem 30:2423–2430](https://doi.org/10.1002/etc.647).

**Allendorf et al. 2019 — BSA/water partition coefficients incl. the alternatives
(abstract), [Environ Sci Process Impacts 21:1852–1863](https://doi.org/10.1039/C9EM00290A).**
log K_BSA/w = **2.8–4.8** L_water/kg_albumin for the ten classical PFAAs, rising with chain
length; **the alternatives HFPO-DA, DONA, 9Cl-PF3ONS and PFECHS fall in the same range as the
legacy PFAAs**; ether groups in the chain do not reduce albumin sorption, and the chlorine in
9Cl-PF3ONS appears to increase it.

**Other albumin Ka ranges (all secondary, from Starnes & Belcher 2026 Table 1,
[J Xenobiot 16:54](https://doi.org/10.3390/jox16020054)):** Klevens & Ellenbogen 1954
BSA/PFOA equilibrium dialysis Ka = 3.22×10² M⁻¹ (the lowest value in the literature);
Wu et al. 2009 HSA/PFOA equilibrium dialysis 3.12×10⁴; Gao et al. 2019 HSA, 14 PFAS,
equilibrium dialysis 0.24–2.63×10⁴; Li et al. 2021 HSA, 26 AFFF PFAS, equilibrium dialysis
0.10–3.16×10⁵; Alesio et al. 2022 BSA, 7 PFAS, fluorescence quenching 0.07–6.16×10⁶;
Crisalli et al. 2023 HSA, 5 PFCAs, ITC 4×10⁰–9.32×10⁶; Chi et al. 2018 HSA+BSA, ESI-MS
0.52–9.90×10⁵; Fedorenko et al. 2021 BSA, ¹⁹F NMR 0.17–3.57×10⁵; Qin et al. 2010 BSA,
fluorescence quenching 0.22–6.85×10⁵; Sheng et al. 2020 HSA (PFOS, 6:2 Cl-PFESA), filtration
centrifugation 3.26–5.99×10⁴; Jackson et al. 2021 HSA, 24 PFAS, DSF 0.38–2.13×10³;
Starnes et al. 2025 HSA, 65 PFAS, DSF nonbinding–4.17×10³; Jia et al. 2022 HSA, 5 ether PFAS,
microscale thermophoresis 0.09–3.23×10⁴.

**Liver fatty acid-binding protein (L-FABP).** Rat L-FABP: the reference probe
DAUDA–L-FABP complex has Kd = 0.47 nM, and competitive inhibition of DAUDA binding ranks
**PFOS > N-EtFOSA > Wyeth-14643 > N-EtFOSE = PFOA** —
[Luebker et al. 2002, Toxicology 176](https://doi.org/10.1016/s0300-483x(02)00081-1).
Human L-FABP, 17 PFCs by fluorescence displacement: affinity rises with PFCA carbon number
from C4 to C11 and falls slightly above C11; the three PFSAs tested have comparable affinity;
**the two fluorotelomer alcohols do not bind** —
[Zhang et al. 2013, Environ Sci Technol 47](https://doi.org/10.1021/es4026722).
By ITC, PFOA and PFNA bind hL-FABP with moderate affinity at **1:1** stoichiometry, PFHxS
weakly, and **PFHxA not at all**; Asn111 is critical for initial binding at the outer site and
Arg122 is also implicated —
[Sheng et al. 2016, Arch Toxicol 90](https://doi.org/10.1007/s00204-014-1391-7).
For the replacements the hL-FABP affinity order is
**6:2 FTCA < 6:2 FTSA < HFPO-DA < PFOA < PFOS = 6:2 Cl-PFESA = HFPO-TA** —
[Sheng et al. 2018, Arch Toxicol 92](https://doi.org/10.1007/s00204-017-2055-1).

**Transthyretin (TTR) and thyroxine-binding globulin (TBG).** Of 24 PFCs in a ¹²⁵I-T4
radioligand competition assay, potency ran
**PFHxS > PFOS = PFOA > PFHpA > sodium perfluoro-1-octanesulfinate > PFNA**, with the most
potent compounds **12.5–50× weaker than T4** and lower-molecular-weight analogues >100×
weaker — [Weiss et al. 2009, Toxicol Sci 109(2):206](https://doi.org/10.1093/toxsci/kfp055).
By fluorescence displacement, most of 16 PFASs bound TTR with relative potency
**3×10⁻⁴ to 0.24** versus thyroxine, fluorotelomer alcohols did not bind, and
**only PFTrDA and PFTeDA bound TBG, at relative potency 2×10⁻⁴** —
[Ren et al. 2016, Toxicology](https://doi.org/10.1016/j.tox.2016.08.011).

**α2u-globulin (the male-rat hypothesis, tested and rejected).** Both the liver-form and
kidney-form α2u-globulins purified from male rat do bind PFOA in vitro and share a binding
site with a fluorescent-labelled fatty acid, but the estimated dissociation constants are in
the **10⁻³ M range**, which the authors state "cannot adequately explain the sex-dependent
elimination of PFOA in rats" —
[Han et al. 2004, Drug Chem Toxicol 27](https://doi.org/10.1081/dct-200039725).

**Thyroid hormone receptor and PPARα (toxicodynamic, not transport).** 16 PFCs bound human
TR with relative binding potency **0.0003–0.05** versus T3, optimal above 10 fluorinated
carbons with an acid end group —
[Ren et al. 2015, Arch Toxicol 89](https://doi.org/10.1007/s00204-014-1258-y). Six PFCAs and
two PFSAs bound Baikal seal and human PPARα LBD dose-dependently, rank
**PFOS > PFDA > PFNA > PFUnDA > PFOA > PFHxS > PFHpA > PFHxA**, with seal and human relative
binding affinities significantly positively correlated —
[Ishibashi et al. 2019, Environ Sci Technol 53](https://doi.org/10.1021/acs.est.8b07273).

**β-Lactoglobulin.** PFDA binds bovine β-lactoglobulin with **Kd ≈ 3.2 µM** (ΔG =
−7.5 kcal/mol) and competes with retinol for the lipocalin calyx —
[Wilson et al. 2026, Environ Res](https://doi.org/10.1016/j.envres.2026.124118).

**Phospholipid membranes.** Membrane/water partition coefficients K_mem/w were measured by
dialysis for 6 PFCAs, 3 PFSAs and 4 alternatives, and anionic passive permeability P_ion
through planar bilayers for 9 of them; the alternatives sorbed similarly to the legacy PFAAs,
and the measured P_ion values were "high enough to explain observed cellular uptake by passive
diffusion with no need to postulate the existence of active uptake processes" —
[Ebert et al. 2020, Environ Sci Technol 54](https://doi.org/10.1021/acs.est.0c00175).

### Inferences
- The *best-covered* protein is albumin and the *best-measured* condition is Fischer et al.
  2024's, but the two barely overlap with the chemicals regulators need: GenX/HFPO-DA and
  F-53B have albumin values only from DSF, ITC, MST and fluorescence quenching, never from a
  low-ratio partitioning measurement.
- Converting Fischer et al. 2024's log D_HSA/w to an association constant using the relation
  their Methods point to (Ka ≈ D × MW_HSA, with MW_HSA ≈ 66.5 kg/mol) gives, **as my own
  arithmetic and not a reported value**: PFPeA ~1×10⁴, PFHxA ~1×10⁵, PFBS ~1×10⁵,
  ADONA ~6×10⁵, PFOA ~2×10⁶, PFOS ~3×10⁶, PFHxS ~4×10⁶, PFHpS ~2×10⁷ M⁻¹. This places the
  SPME dataset on the *high* side of the literature, with equilibrium dialysis (Bischel) and
  ITC high-affinity sites (Moro), and 3–4 orders above DSF.

### Gaps
- **Haemoglobin**: no in vitro PFAS–haemoglobin binding constant was found in any search.
- **TBG**: relative potencies only; no absolute Ka or Kd found.
- **Lipoproteins**: only the qualitative negative result of Forsthuber et al. 2020; no
  lipoprotein partition coefficients found.
- **Organic anion transporters as binding partners**: the OAT literature reachable here is
  transport kinetics (uptake Km, inhibition IC50), not equilibrium binding; I deferred it to
  the transporter work stream (files already in `papers/`).
- **Surface plasmon resonance**: no SPR-derived PFAS–albumin constant found. Starnes &
  Belcher 2026 mention SPR only as a method not applied at scale.
- Per-congener values behind five important ranges are in Supporting Information I could not
  reach: Li et al. 2021 (26 PFAS), Starnes et al. 2025 (65 PFAS), Allendorf et al. 2019,
  Zhang et al. 2013 (17 PFCs to L-FABP), Weiss et al. 2009 (24 PFCs to TTR), and Jia et al.
  2022 (11 PFAS to hL-FABP and HSA; ACS returned HTTP 403).

---

## Q3/Q4. Which method was used, and how much does method choose the answer?

### Takeaway
Method choice moves the reported albumin affinity for a *single* compound by about **four
orders of magnitude**, and — the more important and less widely appreciated point — the
spread *within* one method family is as large as the spread *between* families. The dominant
controls are not the physical technique but (a) the ligand:protein molar ratio regime and
(b) the binding model fitted to the data.

### Cited Findings
- A review by the DSF group assembled 33 literature rows and states plainly that
  "depending on experimental conditions, calculated affinities can vary over multiple orders
  of magnitude which limits comparison of protein–PFAS binding affinities across studies",
  and that "quantitative values are most meaningful when interpreted as relative affinities
  derived under identical experimental conditions" —
  [Starnes & Belcher 2026, J Xenobiot 16:54](https://doi.org/10.3390/jox16020054).
- **Albumin + PFOA across methods** (assembled here from the rows above; every value traced):
  Wu et al. 2024 fluorescence quenching **1.0×10²**; Klevens & Ellenbogen 1954 equilibrium
  dialysis **3.2×10²**; Jackson et al. 2021 DSF **0.38–2.13×10³**; Starnes et al. 2024 DSF
  Kd 0.79 mM ≈ **1.3×10³**; Han et al. 2003 column separation **2.6–2.8×10³** and ¹⁹F NMR
  **3.5×10³**; Alesio & Bothun 2024 DSF **2.4×10⁴**; Wu et al. 2009 equilibrium dialysis
  **3.1×10⁴**; Beesoon & Martin 2015 ultrafiltration (linear isomer) **1×10⁴**; Chen & Guo
  2009 fluorescence quenching **2.7×10⁵**; Peng et al. 2024 fluorescence quenching
  **2.3×10⁵ (298 K) / 2.0×10⁶ (310 K)**; Bischel et al. 2010 equilibrium dialysis **~10⁶**;
  Moro et al. 2022 ITC high-affinity site at 298 K KD 0.4 µM ≈ **2.5×10⁶**. **Span ≈ 2.5×10⁴-fold.**
- **Equilibrium dialysis spans the whole range by itself**: 3.2×10² (Klevens & Ellenbogen
  1954) to ~10⁶ (Bischel et al. 2010) for the same chemical and protein class. So the
  user's framing — that fluorescence quenching sits at 10⁴–10⁶ while dialysis implies
  something different — is **not supported as a method-family effect**; both families
  straddle the same four decades.
- **Fluorescence quenching spans four orders by itself**: 1.0×10² (Wu et al. 2024,
  [Toxics 12:46](https://doi.org/10.3390/toxics12010046)) to 2.0×10⁶ (Peng et al. 2024,
  [Toxics 12:43](https://doi.org/10.3390/toxics12010043)) for PFOA–HSA.
- **The fitting model alone accounts for ~2 orders of magnitude.** Alesio et al. 2022
  applied the Stern-Volmer, modified Stern-Volmer and Hill equations to the *same*
  fluorescence data for 7 PFAS and obtained Ka spanning 0.07–6.16×10⁶ M⁻¹; the paper is
  explicitly "a critical analysis of three common models" and found the Hill equation
  revealed cooperativity that the Stern-Volmer treatments hide —
  [Chemosphere 287:131979](https://doi.org/10.1016/j.chemosphere.2021.131979) (abstract;
  range from Starnes & Belcher 2026 Table 1).
- **DSF is systematically low, and its own authors say so**: DSF-derived affinities, "although
  consistently within the range of those produced by other methods, tend to yield lower values
  than obtained at a fixed physiological temperature" because the value is derived from a
  temperature-dependent melting shift rather than a measurement at constant temperature;
  DSF values "should be interpreted as relative measures" —
  [Starnes & Belcher 2026](https://doi.org/10.3390/jox16020054). Consistent with this,
  Alesio & Bothun 2024 report their Ka explicitly "at 61 °C" —
  [Sci Rep 14:6501](https://doi.org/10.1038/s41598-024-57140-9).
- **Fluorescence quenching cannot see the short chains at all.** PFBA, PFPeA, PFHxA and PFBS
  "often show minimal fluorescence quenching"; Chen & Guo 2009 reported no fluorescence change
  for PFBA or PFBS; DSF by contrast "reliably detects and quantifies binding for short and
  ultra-short chain PFAS such as PFBA and trifluoroacetic acid" —
  [Starnes & Belcher 2026](https://doi.org/10.3390/jox16020054);
  [Chen & Guo 2009](https://doi.org/10.1007/s00204-008-0359-x).
- **Within one paper, three methods disagree by three orders.** For C8–C11 PFCAs and albumin:
  surface tension titration gave only qualitative complex formation at mM ligand; ¹⁹F NMR gave
  secondary Ka of 10²–10⁴ M⁻¹ at high ligand:protein ratios; fluorescence indicated two
  binding classes at ~10⁵ and ~10² M⁻¹. The authors conclude fluorescence "offers a more
  comprehensive picture" chiefly because it tolerates a wider concentration range —
  [MacManus-Spencer et al. 2010, Anal Chem 82:974–981](https://doi.org/10.1021/ac902238u).
- **Binding constants measured by fluorescence depend on the protein concentration used.**
  Hebert & MacManus-Spencer report at least 2–3 PFAAs bound per HSA with Ka ~10⁴ M⁻¹ and state
  that "these binding strengths exhibit a dependence on protein concentration", and that
  measured PFAA Ka are ~10% of fatty acids of similar chain length, falling to perhaps 2–3%
  after correcting for protein concentration —
  [Anal Chem 82](https://doi.org/10.1021/ac100721e).
- **Inner-filter / Trp corrections**: I found **no** PFAS–albumin fluorescence-quenching paper
  in this set that reports applying an inner-filter correction. Peng et al. 2024 and Wu et al.
  2024 both report Kq values of 10¹⁰–10¹¹ (Wu) and ~10¹² L mol⁻¹ s⁻¹ (Peng) — two to four
  orders above the diffusion-limited collisional quenching limit (~2×10¹⁰), which they use as
  the argument for static rather than dynamic quenching. Peng et al. 2024 add 3D excitation-
  emission matrix characterisation.
- **Separative methods are slow and leaky.** Equilibrium dialysis needs 4–120 h to equilibrate
  (rapid equilibrium dialysis ~4 h); ultrafiltration centrifugation is faster but "often
  results in nonspecific adsorption of PFAS to the membrane, reducing reproducibility";
  size-exclusion/micro-desalting resolved the adsorption problem (>98% PFOA recovery in Han et
  al.) but suffers low protein recovery — [Starnes & Belcher 2026](https://doi.org/10.3390/jox16020054).
- **The SPME depletion method avoids extraction from the protein altogether**, reproduced
  literature D_BSA/w within 0.5 log units, and agreed with its own D_HSA/w within 0.25 log
  units for 23 of 27 PFAS; but D_HSA/w **fell** between 48 and 96 h incubation, particularly
  for η_pfc > 9, which the authors attribute to protein denaturation and which led them to cap
  experiments at 48 h — [Fischer et al. 2024](https://doi.org/10.1021/acs.est.3c07415).
- **Method-specific blind spots are documented**: ITC "has low throughput, requires large
  protein concentrations, and is expensive"; ¹⁹F NMR "is best suited to high-affinity
  interactions, requires large protein volumes"; native ESI-MS suffers "variability, lack of
  reproducibility, and differences in sensitivity across congeners (e.g. short chain and long
  chain) … due to buffer composition effects"; SYPRO Orange cannot be used in DSF with PFAS
  because PFAS are surfactants and albumin's hydrophobic sites bind the dye, forcing intrinsic-
  Trp or molecular-rotor-dye detection instead —
  [Starnes & Belcher 2026](https://doi.org/10.3390/jox16020054).
- **BSA is an imperfect HSA proxy for specific congeners.** D_HSA/w and D_BSA/w agreed within
  0.25 log units for 23 of 27 PFAS, but HSA sorption was 0.5–1.0 log units higher than BSA for
  **PFHxA, 5:3 FTCA, PFBS and PFHpS** —
  [Fischer et al. 2024](https://doi.org/10.1021/acs.est.3c07415). Independently, EPA SeqAPASS
  analysis found BSA (79.5% overall identity to HSA) a **non-match** for Sudlow site I
  susceptibility, whereas rat (78.5%) and porcine (77.8%) albumin matched at both Sudlow sites
  — [Starnes et al. 2024, Table 4](https://doi.org/10.1093/toxsci/kfae028).

### Inferences
- The practical rule the literature supports is: **never compare absolute Ka across studies;
  compare rank orders within a study.** Every rank order I found is consistent (longer chain →
  tighter; sulfonate > carboxylate; neutral head group → no binding), while the absolute
  values are not.
- DSF and the ultra-low fluorescence-quenching values (Wu et al. 2024) are the two families
  that would, if taken at face value in a PBTK model, predict an unbound fraction orders of
  magnitude too high. DSF at least flags its own offset; Wu et al. 2024 does not, and I would
  treat its Ka of 20–400 M⁻¹ as not usable for toxicokinetics.
- Because the only *physiologically-ratioed* measurements (Fischer et al. 2024 SPME; Bischel
  et al. 2010 low-ratio dialysis) both land at the high end (~10⁶ M⁻¹ equivalent for PFOA),
  the low literature values are most parsimoniously read as artefacts of high ligand loading,
  denaturation, or a single-site model forced onto a multi-site protein — not as evidence of
  weak binding.

### Gaps
- No paper in this set reports an inner-filter-corrected quenching constant, so I cannot
  quantify how much of the fluorescence-quenching spread that correction would remove.
- No SPR data found, so the method comparison has no kinetic (k_on/k_off) arm.
- I could not obtain the primary Alesio et al. 2022 text, so the per-model Ka breakdown
  (which would let the model-dependence be quantified per congener rather than as a range)
  remains unquantified at the congener level.

---

## Q5. Chain length, head group, and the switch point in which protein dominates

### Takeaway
Albumin affinity rises steeply with perfluorinated chain length to a maximum at
η_pfc ≈ 7–10 and then *falls* for the longest chains, while globulin affinity keeps rising —
so there is a genuine, measured crossover: albumin carries essentially all of the shorter
PFAS, and globulins become co-equal carriers by η_pfc ≈ 12–13. Sulfonates bind more tightly
than carboxylates of the same chain length, and a charged head group is mandatory.

### Cited Findings
- **The headline switch**: "PFAS with η_pfc < 7 were highly bound to HSA relative to
  globulins, whereas PFAS with η_pfc ≥ 7 showed a greater propensity for binding to globulins"
  — [Fischer et al. 2024](https://doi.org/10.1021/acs.est.3c07415).
- **Quantified crossover**: D_glob/w / D_HSA/w ratios are **<0.1 for PFAS with MW < 500 g/mol**
  (albumin drives serum distribution; **fraction bound to albumin >98%**), rise through
  **0.1–2 for MW > 500**, and reach **~1 for PFAS with η_pfc = 12–13**, with "approximately
  equal contributions of the two proteins to the total binding expected for MW > 600 PFAS".
  The authors set the practical threshold at **D_glob/w/D_HSA/w > 0.1**, above which globulins
  should be considered in bioaccumulation assessment —
  [Fischer et al. 2024](https://doi.org/10.1021/acs.est.3c07415).
- **Albumin affinity plateaus then declines.** log D_HSA/w increased with MW only up to
  ~400 g/mol and then plateaued; the maxima in the table are PFUnDA (5.18, η_pfc 10) among
  carboxylates and PFHpS (5.49, η_pfc 7) among sulfonates, with PFTeDA falling to 3.87. The
  mechanistic reading offered is that HSA cavities accommodate both the electrostatic
  (head group) and hydrophobic (C–F chain) interactions up to η_pfc = 8, while "for η_pfc > 8
  PFAS, reduced molecular flexibility limits their accessibility to the HSA binding pockets" —
  [Fischer et al. 2024](https://doi.org/10.1021/acs.est.3c07415).
- Independently: "Affinity for BSA increases with PFAA hydrophobicity but decreases from the
  C8 to C12 PFCAs, likely due to steric hindrances associated with longer and more rigid
  perfluoroalkyl chains" — [Bischel et al. 2011](https://doi.org/10.1002/etc.647).
- **Globulin affinity keeps rising then falls later**: log D_glob/w was <2 (D_glob/w < 100) for
  MW < 400, increased linearly between MW 400–600, and declined above MW 600. γ-Globulins
  (MW ~1193 kDa vs HSA 67 kDa) are not known to bind fatty acids, so binding of <1 kDa
  molecules is attributed to hydrophobic interaction with their large surface area —
  [Fischer et al. 2024](https://doi.org/10.1021/acs.est.3c07415).
- **Sulfonate > carboxylate at equal chain length** (from the Fischer table above, same
  η_pfc): PFHxS 4.77 vs PFHpA 4.10 (η_pfc 6); PFHpS 5.49 vs PFOA 4.48 (η_pfc 7); PFOS 4.62 vs
  PFNA 4.49 (η_pfc 8). The paper attributes PFHpS's unusually high D_HSA/w to "the additional
  hydrogen bond established by the sulfonic headgroup" —
  [Fischer et al. 2024](https://doi.org/10.1021/acs.est.3c07415). Concordantly: "the
  C₄-sulfonate exhibits increased affinity relative to the equivalent chain-length PFCA"
  — [Bischel et al. 2011](https://doi.org/10.1002/etc.647); and "perfluorinated sulfonates
  sorb more strongly than their carboxylate counterparts" —
  [Allendorf et al. 2019](https://doi.org/10.1039/C9EM00290A).
- **DSF reproduces the chain-length effect within every species tested.** 8-carbon congeners
  bound significantly more tightly than 4-carbon congeners in all four albumins, with large
  effect sizes: HSA PFBA 2.64 → PFOA 0.79 mM (p < .0001, Cohen's d 3.77); BSA 3.06 → 0.99
  (p < .0001, d 3.52); PSA 1.28 → 0.37 (p = .028, d 3.92); RSA 1.90 → 0.40 (p = .0021,
  d 4.86). For the sulfonates PFBS → PFOS the same held in HSA (1.68 → 0.62, p = .034),
  PSA (1.25 → 0.38, p = .04) and RSA (1.41 → 0.42, p = .0049) **but not in BSA**
  (0.80 → 0.86, not significant) — [Starnes et al. 2024, Table 3](https://doi.org/10.1093/toxsci/kfae028).
- **A charged head group is required.** 6:2 FTOH (neutral fluorotelomer alcohol) was not bound
  by human, bovine, porcine or rat albumin —
  [Starnes et al. 2024](https://doi.org/10.1093/toxsci/kfae028). The two fluorotelomer alcohols
  tested against human L-FABP also did not bind —
  [Zhang et al. 2013](https://doi.org/10.1021/es4026722). Fluorotelomer alcohols did not bind
  TTR — [Ren et al. 2016](https://doi.org/10.1016/j.tox.2016.08.011).
- **L-FABP has its own, later optimum**: human L-FABP affinity "increased significantly with
  their carbon number from 4 to 11, and decreased slightly when the number was over 11" —
  [Zhang et al. 2013](https://doi.org/10.1021/es4026722). hL-FABP shows **no binding for
  PFHxA**, weak for PFHxS, moderate 1:1 for PFOA/PFNA —
  [Sheng et al. 2016](https://doi.org/10.1007/s00204-014-1391-7).
- **A second switch point, on the liver side**: liver:serum partition coefficients of 11 PFAS
  in CD-1 mice correlated better with log Kd(hL-FABP)/log Kd(HSA) than with log Kd(hL-FABP)
  alone, i.e. the liver–blood split is set by **competition between hL-FABP and HSA**, not by
  L-FABP affinity on its own. PFSAs accumulated in serum more than PFCAs, yet their
  liver:serum ratios were *lower* than the PFCAs' —
  [Jia et al. 2022, Environ Sci Technol 56:6192–6200](https://doi.org/10.1021/acs.est.1c08493).
- **A third switch point, in the mechanism of elimination**: PBTK sensitivity analysis showed
  "permeability and phospholipid binding strongly influenced the elimination and distribution
  of long-chain PFAA (η_pfc ≥ 7), while elimination for short-chain PFAA (η_pfc ≤ 6) was more
  sensitive to renal transporters and albumin binding" —
  [Fischer et al. 2025, Environ Sci Technol 59:13240–13250](https://doi.org/10.1021/acs.est.5c05473).
- **TTR has an intermediate-chain optimum with a sulfonate preference**: "PFASs with a medium
  chain length and a sulfonate acid group are optimal for TTR binding, and PFASs with lengths
  longer than 12 carbons" are disfavoured — [Ren et al. 2016](https://doi.org/10.1016/j.tox.2016.08.011).
  This is why PFHxS, not PFOS, tops the TTR potency list in
  [Weiss et al. 2009](https://doi.org/10.1093/toxsci/kfp055).
- **Ether and chlorine substitution does not reduce albumin binding.** "Structural
  modifications such as the introduction of ether groups into the chain do not reduce sorption
  to albumin, whereas the chlorine atom in 9Cl-PF3ONS seems to even increase the sorption" —
  [Allendorf et al. 2019](https://doi.org/10.1039/C9EM00290A). In Fischer et al. 2024, ADONA
  (η_pfc 6, ether carboxylate) had log D_HSA/w 3.98, between PFPeS (3.98) and PFHpA (4.10).

### Inferences
- There are **three distinct switch points** and they do not coincide, which matters for how
  the report frames chain length: the *carrier* switches from albumin to albumin+globulin at
  η_pfc ≈ 12 (MW > 600); the *liver/blood split* is governed by L-FABP vs HSA competition
  across the whole range; and the *rate-limiting elimination mechanism* switches from
  renal transporters + albumin binding to permeability + phospholipid binding at η_pfc = 7.
- The albumin affinity maximum at η_pfc ≈ 7–10 and decline thereafter means albumin binding
  **cannot** explain the monotonic increase in half-life with chain length on its own; the
  globulin and phospholipid arms are needed, which is exactly the conclusion
  [Ng & Hungerbühler 2014](https://doi.org/10.1021/es404008g) reach from the modelling side.

### Gaps
- No measured albumin or globulin distribution coefficient for GenX/HFPO-DA or
  F-53B/6:2 Cl-PFESA at a physiological ligand:protein ratio, so the alternatives cannot be
  placed on the Fischer chain-length curve.
- The PFECA class is represented only by ADONA (Fischer et al. 2024), HFPO-TA/HFPO-TeA/PFEESA
  (Jia et al. 2022, MST) and PFO3DA/HFPO-TA (Peng et al. 2024, fluorescence quenching).

---

## Q6. Which albumin binding sites are occupied, and what does the structural evidence show?

### Takeaway
Crystallography puts PFOS at fatty-acid sites FA3/FA4 and FA5 and PFOA's high-affinity site
in subdomain IIIA, while solution site-marker competition most often implicates Sudlow site I
(subdomain IIA). The two lines of evidence are **in open conflict for PFOA**, and the
literature has not resolved it.

### Cited Findings
- **The site map.** HSA contains seven fatty-acid binding sites (FA1–FA7) plus two drug sites:
  Sudlow site I in subdomain IIA, overlapping FA7, the classical warfarin site, binding bulky
  heterocyclic anions; Sudlow site II in subdomain IIIA, overlapping FA3 and FA4, smaller and
  more rigid, favouring extended aromatic carboxylic acids such as ibuprofen. "Sudlow sites I
  and II, multiple FA sites, and even interstitial regions between FA sites have all been
  identified as PFAS binding domains on albumin" —
  [Starnes & Belcher 2026](https://doi.org/10.3390/jox16020054).
- **PFOS crystal structure.** The HSA–PFOS complex crystal structure shows PFOS binding "at a
  molar ratio of 2:1" and that "PFOS binding renders the HSA structure more compact" —
  [Luo et al. 2012, Chem Res Toxicol](https://doi.org/10.1021/tx300112p). The site assignment
  is reported downstream: redocking PFOS onto that structure (PDB entry **4E99**), "originally
  complexed with two PFOS in fatty-acid binding site (FA) 3/4 and 5", reproduced the
  experimental pose with atomic RMSD < 2 Å —
  [Li et al. 2021, Toxics 9:63](https://doi.org/10.3390/toxics9030063).
- **PFOA crystal structure.** The hSA–PFOA structure (co-crystallised with a medium-chain
  fatty acid) identified "a total of eight distinct binding sites, four occupied by PFOAs and
  four by FAs". Solution studies confirmed **4:1 PFOA:hSA stoichiometry** and "the presence of
  one high and three low affinity binding sites", and "competition experiments with known
  hSA-binding drugs allowed locating the high affinity binding site in **sub-domain IIIA**"
  (i.e. the Sudlow site II / FA3-FA4 region) —
  [Maso et al. 2021, Protein Sci 30](https://doi.org/10.1002/pro.4036).
- **Solution competition says Sudlow site I for PFOA.** Displacement experiments with site
  markers plus docking "revealed that the binding of PFOA to BSA took place in sub-domain IIA
  (Sudlow site I) whereas PFOS was mainly located in the sub-domain IIIA (Sudlow site II) and
  partially bound into site I" —
  [Chen et al. 2015, Chemosphere 129:217–224](https://doi.org/10.1016/j.chemosphere.2014.11.040).
- **And Sudlow site I for six PFAS, strongly.** Warfarin (site I) reduced the HSA binding
  constant by 93.3–99.6% for all six compounds tested, versus 13.8–42.7% for ibuprofen
  (site II) and 8.1–48.8% for lidocaine: PFNA 98.3% / 13.8% / 43.9%;
  HFPO-TA 99.6% / 23.8% / 35.3%; PFOA **96.1%** / 40.8% / 8.1%; PFO3DA 95.1% / 25.8% / 11.8%;
  PFHpA 98.9% / 42.7% / 48.8%; DFSA 93.3% / 25.4% / 31.7% —
  [Peng et al. 2024, Table 3](https://doi.org/10.3390/toxics12010043).
- **Probe displacement shows short chains occupy both Sudlow sites.** PFBA and PFBS displaced
  the site I probe dansylamide (Ka 1.0×10⁶ and 2.2×10⁶ M⁻¹); PFBS and PFDoA displaced the
  site II probe dansyl-L-proline (6.5×10⁶ and 1.2×10⁶ M⁻¹); PFBA did not bind site II —
  [Chen & Guo 2009](https://doi.org/10.1007/s00204-008-0359-x). This is the clearest evidence
  that short-chain PFAS *do* occupy specific albumin sites even when they produce no
  detectable Trp quenching.
- **The Trp214 pocket is involved but is not the whole story.** Native ESI-MS plus fluorescence,
  CD and docking indicated "the hydrophobic pocket proximate to Trp 214 in human serum albumin
  might be one of the dominated binding sites" while PFOA and PFOS "were likely to bind with
  serum albumins in more than one pocket" —
  [Chi et al. 2018, Chemosphere 198:442–449](https://doi.org/10.1016/j.chemosphere.2018.01.152).
  ¹⁹F NMR on BSA showed "the hydrophobic tails exhibit greater binding affinity relative to the
  headgroup" — [Fedorenko et al. 2021](https://doi.org/10.1016/j.chemosphere.2020.128083).
- **Binding changes albumin conformation, reversibly.** Multiple PFOA sites on HSA — "one with
  strong affinity and others with low affinity" — were evident from Trp fluorescence lifetimes,
  and CD showed structural change on PFOA titration; adding β-cyclodextrin **reversed** both
  the fluorescence and CD changes —
  [Weiss-Errico et al. 2018, Chem Res Toxicol 31](https://doi.org/10.1021/acs.chemrestox.8b00002).
  PFOS destroyed both tertiary and secondary BSA structure with loss of α-helix, made the
  Trp/Tyr microenvironment more hydrophobic, **increased** BSA thermal stability, and reduced
  BSA relative activity — [Wang et al. 2016, J Photochem Photobiol B 159](https://doi.org/10.1016/j.jphotobiol.2016.03.024).
  α-Helix content fell on PFOA and PFDA binding to BSA —
  [Qin et al. 2010](https://doi.org/10.1021/jf100412q); and on PFOA/PFOS binding to both
  albumins — [Chi et al. 2018](https://doi.org/10.1016/j.chemosphere.2018.01.152).
- **Docking contact residues (computational, flagged as such in the CSV).** HSA docking gave
  binding energies −6.2 to −8.3 kcal/mol with contacts at MET548 (PFOA), ASN405 (PFOS),
  ASN405/TYR401 (PFHxS), ARG117 (PFBA), LYS137 (PFBS), LEU14/ASN18 (PFPrS), LEU155 (NaDONA),
  SER287 (HFPO-DA), ARG410/ALA406 (9Cl-PF3ONS), ARG410 (11Cl-PF3OUdS) —
  [Wu et al. 2024, Table 7](https://doi.org/10.3390/toxics12010046). MM/GBSA ΔG_bind for
  HSA complexes: PFNA −38.83, HFPO-TA −35.20, PFOA −28.04, PFO3DA −22.46, PFHpA −21.31,
  DFSA −17.98 kcal/mol — [Peng et al. 2024, Table 4](https://doi.org/10.3390/toxics12010043).
- **Cross-species site conservation.** EPA SeqAPASS level 1/3 analysis: BSA 79.5% overall
  identity to HSA, **no** predicted susceptibility match at Sudlow site I but yes at Sudlow
  site II and Trp214; RSA 78.5% and PSA 77.8%, both matching at Sudlow site I, Sudlow site II
  and Trp214 — [Starnes et al. 2024, Table 4](https://doi.org/10.1093/toxsci/kfae028).

### Inferences
- The PFOA site conflict is probably real rather than an error: the crystal structure
  interrogates the *highest*-affinity site under co-crystallisation with a competing fatty
  acid, while warfarin-displacement interrogates whichever site the fluorophore reports on at
  the (much higher) ligand loadings used in quenching experiments. A multi-site ligand will
  give different "the" site depending on which site the experiment is sensitive to.
- Because Sudlow site I overlaps FA7 and Sudlow site II overlaps FA3/FA4, the apparently
  conflicting assignments are not as far apart as the names suggest — PFOS at FA3/FA4 (crystal)
  and PFOS "mainly in subdomain IIIA" (competition) are **the same region**. The genuine
  disagreement is confined to PFOA.
- The BSA Sudlow-site-I mismatch is a concrete reason to prefer HSA over BSA when the endpoint
  is site I occupancy or warfarin/drug displacement, and it lines up with the four congeners
  (PFHxA, 5:3 FTCA, PFBS, PFHpS) for which Fischer et al. 2024 found HSA and BSA sorption to
  diverge by 0.5–1 log unit.

### Gaps
- No crystal structure found for any short-chain PFAS, any ether PFAS (GenX, ADONA), or
  F-53B bound to albumin.
- FA1, FA2 and FA6 have not been assigned to any PFAS by direct structural evidence in the
  papers I reached.

---

## Q7. Stoichiometry at physiological versus experimental albumin:PFAS ratios

### Takeaway
This is the single most important methodological caveat in the whole field, and it is
quantifiable: human serum runs at a PFAS:albumin molar ratio of roughly 10⁻⁵–10⁻⁴, whereas
most in vitro studies run at 0.4–8 or higher — **four to six orders of magnitude above
physiological**. Reported stoichiometry tracks the ratio used, from ~1 site at low loading to
8 or even 45 sites at mM ligand.

### Cited Findings
- **The physiological ratio.** Median NHANES 2017–18 serum albumin was **41 g/L** and globulin
  **31 g/L**, corresponding to volume fractions VF_HSA = 4.1%, VF_glob = 3.1%, VF_water = 92.8%;
  γ-globulin MW is 1193 kDa and HSA 67 kDa —
  [Fischer et al. 2024](https://doi.org/10.1021/acs.est.3c07415). (41 g/L ÷ 67 kg/mol ≈ **0.61 mM
  albumin**, consistent with the ~600 µM figure.) Fischer et al. selected their experimental
  ratios "to mimic binding in serum at PFAS concentrations relevant to human exposure, based on
  ratios of **≤0.0005** that were estimated from PFAS concentrations reported in human sera."
- **Where saturation sets in.** "Nonlinearity of BSA binding has been observed for PFBA, PFOA,
  PFHxS, and PFOS at molar ratios of **≥0.39**", and the Fischer experiments were run at ratios
  "approximately **100 times lower** than the molar ratio at which saturation was observed for
  BSA" — i.e. ≤0.004 for HSA/BSA (261 mol protein per mol PFAS) and ≤0.009 for γ-globulin
  (111 mol protein per mol PFAS) —
  [Fischer et al. 2024](https://doi.org/10.1021/acs.est.3c07415). The authors warn explicitly:
  "This should be considered when applying these distribution coefficients to systems with
  higher PFAS-to-protein ratios, **such as in vitro toxicity tests**."
- **Stoichiometry rises with loading — same paper, same protein, two methods.** Equilibrium
  dialysis at low PFAA:albumin ratios gave Ka ~10⁶ M⁻¹ with **1–3 primary binding sites**,
  whereas nanoESI-MS "data reveal PFAA-BSA complexes with **up to eight occupied binding sites
  at a 4:1 PFAA:albumin mole ratio**" and Ka only 10⁴–10⁵ M⁻¹. The authors conclude "the results
  reported here suggest binding through specific high affinity interactions **at low
  PFAA:albumin mole ratios**" —
  [Bischel et al. 2010](https://doi.org/10.1021/es101334s).
- **Up to 8 sites by ESI-MS "at high mole ratios of PFOA/PFOS"** —
  [Chi et al. 2018](https://doi.org/10.1016/j.chemosphere.2018.01.152).
- **45 sites at mM ligand.** Equilibrium dialysis fitted to a Langmuir two-step sequential
  model gave "the saturation binding number of PFOS was **45 per molecule of SA**", with
  effects reported at 1.2 mmol/L PFOS —
  [Zhang et al. 2009, BMC Mol Biol 10:16](https://doi.org/10.1186/1471-2199-10-16). At a
  nanomolar serum PFOS concentration this is ~5–6 orders of magnitude off the physiological
  loading; the number describes surfactant coating, not physiological transport.
- **Methods that structurally require supra-physiological loading.** "Limitations associated
  with instrumentation and methods require high PFCA concentrations in both surface tension and
  ¹⁹F NMR experiments" — and the ¹⁹F NMR constants obtained there are explicitly labelled
  "**secondary** association constants ranging from 10² to 10⁴ M⁻¹ … at high PFCA:albumin mole
  ratios" — [MacManus-Spencer et al. 2010](https://doi.org/10.1021/ac902238u). Equilibrium
  dialysis is also "limited by poor solubility of large or hydrophobic PFAS, **necessitating
  higher concentrations**"; and ITC "requires large protein concentrations" —
  [Starnes & Belcher 2026](https://doi.org/10.3390/jox16020054).
- **n values near 1 at moderate loading.** Fluorescence-quenching n values cluster around
  unity: 0.88–1.51 across six PFAS and three temperatures
  ([Peng et al. 2024, Table 2](https://doi.org/10.3390/toxics12010043)) and 0.47–0.87 across
  ten PFAS ([Wu et al. 2024, Tables 4–6](https://doi.org/10.3390/toxics12010046)). ITC at
  µM loading likewise gave n = 1.02–1.6 for PFHxA and C6O4, but PFOA required two site classes
  with n 0.89–0.95 (high affinity) and 4.5–9.5 (low affinity)
  ([Moro et al. 2022, Table 1](https://doi.org/10.1021/acs.chemrestox.2c00211)).
- **Experimental ligand concentrations actually used** (from the CSV): Fischer et al. 2024,
  0.2–42 µg/L; Ryu et al. 2024, 5 µM with 1% DMSO; Starnes et al. 2024 and Jackson et al. 2021
  DSF, 0–1000 µM; Bischel et al. 2010 nanoESI-MS, 4:1 mol/mol; MacManus-Spencer et al. 2010
  surface tension and ¹⁹F NMR, mM; Zhang et al. 2009, up to 1.2 mM.
- **Average-affinity caveat for multi-site proteins.** "The affinity values for albumin, and
  other such proteins with numerous binding sites, represent the **average** affinity of
  binding and does not inform on specific binding strength of a specific site"; DSF "alone does
  not provide binding-site resolution" — [Starnes & Belcher 2026](https://doi.org/10.3390/jox16020054).

### Inferences
- A reader comparing an n of 1 (fluorescence quenching, moderate loading), 1–3 (low-ratio
  dialysis), 6–9 (microdesalting columns), 8 (nanoESI-MS at 4:1) and 45 (dialysis at mM) is not
  looking at a disagreement about albumin — they are looking at a **titration curve read at
  five different points**. For toxicokinetics only the low-ratio end is relevant, which argues
  for n ≈ 1–3 high-affinity sites and Ka ~10⁶ M⁻¹ for PFOA/PFNA.
- The practical consequence for PBTK work: a Ka measured at a supra-physiological ratio is an
  *apparent average* over high- and low-affinity sites and will be biased low, predicting an
  unbound fraction biased high. This is a systematic, directional error, not noise.
- It also means in vitro *toxicity* assays (typically µM PFAS with ~30 µM albumin from 10% FBS,
  i.e. ratios near 0.03–1) sit in the saturating regime, so the free concentration in those
  assays is not predictable from the low-ratio distribution coefficients — exactly the warning
  Fischer et al. 2024 give.

### Gaps
- I found no study that measured albumin binding across the full ratio range *and* reported the
  resulting apparent Ka as a function of ratio, which is the experiment that would convert this
  qualitative caveat into a correction factor.

---

## Q8. Measured unbound fraction in real human serum/plasma, and its interindividual variation

### Takeaway
In serum, measured f_unbound for PFAS is **0.01–1.2%** (Fischer et al. 2024), and
interindividual variation driven by albumin and globulin concentrations is modest — at most a
factor of 2.5, CV 6–10%. There is a large and unresolved conflict with the older
column-separation estimate of ">90% bound" (f_unbound <10%), which is an order of magnitude
higher.

### Cited Findings
- **The range.** "Values for D_serum/w suggest that PFAS are generally strongly bound to
  proteins in human serum (**f_unbound 0.01–1.2%**)", and f_unbound fell with increasing MW to
  an inflection at 600 g/mol and then rose again. Per-compound:
  **PFHpS 0.035% < PFHxS 0.041% ≈ PFOS 0.042% < PFOA 0.061%** —
  [Fischer et al. 2024](https://doi.org/10.1021/acs.est.3c07415).
- **The prediction from protein concentrations works.** Experimental log D_serum/w agreed with
  values predicted from measured D_HSA/w, D_glob/w and NHANES average albumin/globulin levels
  with slope 0.97 (95% CI 0.94–1.01) and **R² = 0.99**. Three fluorotelomers (5:3 FTCA, 7:3
  FTCA, 6:2 FtS) were under-predicted, suggesting other serum constituents (α-globulins,
  phospholipids) matter for them; PFHpS was over-predicted, possibly because of competition
  with serum fatty acids — [Fischer et al. 2024](https://doi.org/10.1021/acs.est.3c07415).
- **Interindividual variability, quantified** (NHANES 2017–18, n = 1919, albumin and globulin
  measured): albumin ranged **21–52 g/L** (CV 8.5%) and globulin **20–55 g/L** (CV 14%), and
  the two were inversely correlated. Maximum variability in f_unbound across individuals was a
  factor of **1.6 (10:2 FtS) to 2.5 (PFHxS)**; the 99th-percentile f_unbound exceeded the
  1st-percentile value by **1.3× (PFTriDA) to 1.6× (PFHxS)**; CVs of f_unbound ran
  **6.3% (PFTriDA) to 9.5% (PFHpS)**. Variability was greatest for MW < 500 g/mol (factor
  2.0–2.5, CV 8.1–9.5%) and smaller for MW 500–600 (factor 1.6, CV 6.3%), because above
  MW 500 the inversely-correlated albumin and globulin concentrations buffer each other —
  [Fischer et al. 2024](https://doi.org/10.1021/acs.est.3c07415).
- **Consequence for exposure ranking.** Individuals with albumin/globulin ratios below 1.4
  could have higher bioavailable C_unbound of PFOA, PFHxS, PFNA and PFOS relative to their total
  serum concentration, shifting **up to 12% of individuals in rank** —
  [Fischer et al. 2024](https://doi.org/10.1021/acs.est.3c07415).
- **The conflicting older value.** "On the basis of these binding parameters and the estimated
  plasma concentration of serum albumin, **greater than 90%** of PFOA would be bound to serum
  albumin in both rat and human blood" — i.e. f_unbound < 0.10, versus Fischer's 0.00061 for
  PFOA — [Han et al. 2003](https://doi.org/10.1021/tx034005w). The discrepancy follows directly
  from the Kd used (0.3–0.4 mM, equivalent to Ka ~3×10³ M⁻¹) versus Fischer's effective
  ~10⁶ M⁻¹.
- **The other extreme.** "PFNA was greater than 99.9% bound to BSA or HSA at a physiological
  PFAA:albumin mole ratio (≈4)", i.e. f_unbound < 0.001 —
  [Bischel et al. 2010](https://doi.org/10.1021/es101334s).
- **Which plasma fraction actually carries PFAS.** Using Cohn-method protein fractionation plus
  serial ultracentrifugation of native plasma from four healthy volunteers (2 women, 2 men,
  23–31 y) and HPLC-MS/MS of 11 PFAS, "albumin is the most important carrier protein for PFOS,
  PFOA, PFHxS, PFNA and PFDA in native human plasma. These five compounds have very little or
  no affinity for lipoproteins." The authors caution that "the data are based on a small sample"
  and "must be verified by the examination of a larger number of persons" —
  [Forsthuber et al. 2020, Environ Int art. 105324](https://doi.org/10.1016/j.envint.2019.105324).
- **Tissue f_unbound, as opposed to serum.** Rapid equilibrium dialysis of 16 PFAS
  (η_pfc = 3–13) in human, mouse (C57BL/6, CD-1) and rat (Wistar Han) liver, lung, kidney,
  heart and brain homogenates at 5 µM ligand (1% DMSO) showed f_unbound decreasing with
  increasing chain length and hydrophobicity, with binding greatest in
  **brain > liver ≈ kidney ≈ heart > lungs**. Rat liver was identified as a suitable surrogate
  for predicting human tissue f_unbound (**R² ≥ 0.98**) —
  [Ryu et al. 2024, Environ Sci Technol 58:14641–14650](https://doi.org/10.1021/acs.est.4c04050).
- **Isomer-specific binding in whole serum.** The higher binding affinities of linear PFOS and
  PFOA to total serum protein were confirmed when both calf serum and human serum were spiked
  with technical mixtures — [Beesoon & Martin 2015](https://doi.org/10.1021/es505399w).

### Inferences
- The Fischer f_unbound values (0.01–1.2%) and the Bischel value (<0.1% for PFNA) are mutually
  consistent and both come from low-ratio measurements; the Han et al. 2003 ">90% bound"
  estimate comes from a method (microdesalting column, n = 6–9 sites, Kd 0.3–0.4 mM) that sits
  in the low-affinity/high-loading regime. **The report should use ~0.01–1% as the serum
  f_unbound and flag the 10% figure as superseded**, while noting that older PBPK models
  parameterised on Han et al. 2003 will have an unbound fraction roughly 100× too high.
- Interindividual variation in f_unbound (≤2.5-fold) is **much smaller** than the reported
  interindividual variation in half-life (factor 5.6 for PFHxS and 3.5 for PFOS, as cited by
  Fischer et al. 2024), so protein-concentration variability can contribute to but cannot by
  itself explain half-life variability.

### Gaps
- **Kerstner-Wood, Coward & Gorman (2003), Southern Research Institute Study ID 9921.7** — the
  most-cited source for directly measured plasma protein binding of PFHxS, PFOS and PFOA in
  human, rat and monkey plasma and in human-derived plasma protein fractions — is an
  unpublished contract report with no DOI or PMID and **could not be retrieved**. If the report
  needs measured f_unbound in *neat* human plasma rather than a surrogate serum, this remains
  the key missing primary source.
- No study measured f_unbound in individual human sera across a cohort; Fischer et al. 2024
  measured D_serum/w in **a single donor** and modelled the rest from NHANES protein
  concentrations, which they acknowledge.
- Per-congener f_unbound values from Ryu et al. 2024 are in figures/SI and were not extracted.

---

## Q9. How do authors connect binding to toxicokinetics?

### Takeaway
The standard mechanistic chain — binding raises the bound fraction, reduces the fraction
available for glomerular filtration, and lengthens half-life — is asserted widely and holds
within a chemical series, but it **fails across species**: the species with the tightest
albumin binding is not the species with the longest half-life. Several authors have explicitly
tested and rejected specific binding-based explanations.

### Cited Findings
- **The mechanism as stated.** "PFAS bound to proteins are thought to be inaccessible to
  biomolecules involved in transformation and elimination processes and are recirculated in the
  bloodstream, thereby extending elimination half-lives", while "the unbound fraction of a
  toxicant in blood is typically more available for transport to organs and more likely to
  reach molecular targets" — [Fischer et al. 2024](https://doi.org/10.1021/acs.est.3c07415).
- **It works within a chemical series.** "Longer elimination half-lives in human serum have
  been reported for the PFAS with the greatest binding to serum proteins (lowest f_unbound)
  reported in this work (**PFHpS ≈ PFHxS > PFOS > PFOA**)" —
  [Fischer et al. 2024](https://doi.org/10.1021/acs.est.3c07415).
- **It fails across species.** The DSF group tabulated their Kd against reported half-lives:
  human PFOA Kd 0.79 mM / 2.3–8.5 y; cow 0.99 mM / 0.8–1.3 d; pig 0.37 mM / 236 d;
  rat 0.40 mM / 0.1–15 d. For PFOS: human 0.69 mM / 3.3–5.4 y; cow 0.86 mM / 39–120 d;
  pig 0.38 mM / 1.7 y; rat 0.42 mM / 24–83 d —
  [Starnes et al. 2024, Table 5](https://doi.org/10.1093/toxsci/kfae028) (half-life sources
  cited there as Pizzurro et al. 2019, Lau 2015, Death et al. 2021, Numata et al. 2014,
  Russell et al. 2013). **Rat albumin binds PFOA roughly twice as tightly as human albumin yet
  the rat half-life is ~1000× shorter.**
- **A binding-based explanation tested and rejected.** PFOA does bind both the liver- and
  kidney-form rat α2u-globulins at a shared fatty-acid site, but with Kd in the 10⁻³ M range,
  "indicating that bindings of PFOA to either A2U(L) or A2U(K) **cannot adequately explain the
  sex-dependent elimination of PFOA in rats**, and it is unlikely that PFOA-A2U(K) binding
  would induce A2U nephropathy" — [Han et al. 2004](https://doi.org/10.1081/dct-200039725).
- **A binding-based explanation that succeeded.** Isomer-specific HSA Kd values "provide a
  mechanistic explanation for the longer biological half-life" of linear versus branched PFOS
  and PFOA isomers — [Beesoon & Martin 2015](https://doi.org/10.1021/es505399w).
- **Albumin binding is only rate-controlling for the short chains.** PBTK sensitivity analysis
  on 9 PFAA (η_pfc 4–10) in wild-type and knockout mice: "permeability and phospholipid binding
  strongly influenced the elimination and distribution of long-chain PFAA (η_pfc ≥ 7), while
  elimination for short-chain PFAA (η_pfc ≤ 6) was more sensitive to renal transporters and
  albumin binding" — [Fischer et al. 2025](https://doi.org/10.1021/acs.est.5c05473). The same
  paper notes albumin-deficient mice exhibited significantly elevated liver:blood concentration
  ratios while FABP-deficient mice showed PFAA toxicokinetics similar to wild-type.
- **Protein binding is necessary but not sufficient in bioaccumulation models.** The first
  mechanistic protein-binding bioconcentration model for PFAAs in fish "considers PFAA uptake
  via passive diffusion at the gills, association with serum albumin in the circulatory and
  extracellular spaces, association with FABP in the liver, and **renal elimination and
  reabsorption facilitated by OAT proteins**" —
  [Ng & Hungerbühler 2013](https://doi.org/10.1021/es400981a). Comparing the
  phospholipid-partitioning and protein-interaction hypotheses against tissue distribution
  patterns, the chain-length/bioaccumulation relationship, and species- and sex-specific
  half-lives, they conclude "the models need not be mutually exclusive, but that **protein
  interactions are needed** to explain some important features of PFAA bioaccumulation" —
  [Ng & Hungerbühler 2014](https://doi.org/10.1021/es404008g).
- **Albumin binding is a key predictive parameter in PBPK models.** "The PBPK models developed
  by Ng and Hungerbühler and Cheng and Ng highlight **serum albumin as a key predictive
  parameter** for PFAA concentrations and tissue distributions", and the permeability-limited
  Cheng & Ng model's "high predictive accuracy for PFOA tissue distribution in rats — validated
  against in vivo data — was attributed to the inclusion of protein interactions" —
  [Starnes & Belcher 2026](https://doi.org/10.3390/jox16020054). A systematic parameter-
  availability review for a zebrafish PFOA PBPK model (including hepatobiliary circulation for
  the first time) found protein-binding parameters to be a principal data gap —
  [Khazaee & Ng 2018](https://doi.org/10.1039/c7em00474e).
- **Binding data are offered directly as PBTK inputs.** "The f_unbound data resulting from this
  work and the rat liver prediction method offer **input parameters and tools for toxicokinetic
  models** for legacy and emerging PFAS" — [Ryu et al. 2024](https://doi.org/10.1021/acs.est.4c04050).
  And: "Binding data reported in this study are useful for parametrizing physiologically based
  toxicokinetic (PBTK) models … In combination with PBTK models, analyses of individual
  C_unbound could reveal the role of variable blood protein concentrations … to susceptibility
  to PFAS toxicity and elimination half-lives in humans" —
  [Fischer et al. 2024](https://doi.org/10.1021/acs.est.3c07415).
- **PFAS are weaker albumin ligands than the endogenous fatty acids they displace.** Measured
  PFAA binding constants "are approximately 10% of those values reported for fatty acids of
  similar chain length; correcting for protein concentration suggests the binding strengths may
  be as low as 2-3%" — [Hebert & MacManus-Spencer 2010](https://doi.org/10.1021/ac100721e).
  Independently, Fischer et al. 2024 attributed their over-prediction of PFHpS binding in serum
  to "competitive binding between these PFAS and fatty acids contained in human serum", and
  Allendorf et al. 2019 specifically investigated binding competition with medium- and
  long-chain fatty acids.
- **Where the binding→effect link is argued not to matter.** "Median human blood levels of the
  most potent TTR-binding PFCs are one to two orders of magnitude lower than concentration at
  50% inhibition (IC50) values" — [Weiss et al. 2009](https://doi.org/10.1093/toxsci/kfp055);
  and T4 displacement from TTR by PFOS and PFOA "would be significant for the occupationally
  exposed workers but not the general population" —
  [Ren et al. 2016](https://doi.org/10.1016/j.tox.2016.08.011).
- **A therapeutic corollary.** β-Cyclodextrin reversed PFOA binding to HSA, investigated "with
  potential therapeutic applications toward exposure to PFOA" —
  [Weiss-Errico et al. 2018](https://doi.org/10.1021/acs.chemrestox.8b00002).
- **A route of elimination that binding predicts.** Albumin binding is invoked as the mechanism
  for PFAS excretion into milk in livestock, which is why cross-species albumin affinities were
  measured — [Alesio & Bothun 2024](https://doi.org/10.1038/s41598-024-57140-9) and
  [Starnes et al. 2024](https://doi.org/10.1093/toxsci/kfae028).

### Inferences
- The cross-species failure in Starnes et al. 2024 Table 5 is the most useful single fact here
  for the parent review: it shows that albumin binding affinity is **not** the variable that
  sets the species difference in half-life. Since f_unbound varies only ~2.5-fold between
  humans and perhaps a few-fold between species, while half-lives vary by 10³, the species
  difference must come from the clearance side — renal transporter complement and reabsorption
  — with binding setting only the concentration of substrate presented for filtration.
- The two mechanisms are coupled, not alternatives: binding determines the filtered load
  (f_unbound × GFR) while transporters determine what fraction of the filtered load is
  reabsorbed. A model with correct binding and no transporters, or correct transporters and
  Han-era binding (100× too weak), will both fail.
- Because PFAS albumin affinity is only 2–10% of that of similar-chain fatty acids, albumin
  binding of PFAS at physiological loading is occurring **in the presence of a large excess of
  higher-affinity endogenous competitors**. This is a plausible, under-tested source of
  disagreement between fatty-acid-free in vitro albumin (what nearly every study uses) and real
  serum, and it runs in the direction of making in vitro Ka too high relative to in vivo.

### Gaps
- No study found that measured PFAS albumin binding in the presence of physiological fatty acid
  loading *and* reported the resulting f_unbound; Allendorf et al. 2019 addressed competition
  but the per-condition results were not retrievable.
- Nothing found that directly measures glomerular filtration of the unbound PFAS fraction
  against an independently measured f_unbound in the same animal.
- Cheng & Ng 2018 (molecular-dynamics prediction of relative protein affinity), named in the
  assignment, **could not be located** — the DOI I tried returned not-found and I did not
  identify the correct record. It is cited second-hand via Starnes & Belcher 2026 only.
