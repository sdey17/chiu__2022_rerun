# In vitro PFAS transport by renal and hepatic membrane transporters: kinetic parameters and species comparison

Structured database of every number below: `db/transporter_kinetics.csv` (217 rows).
Retrieval log including every failure: `papers/SOURCES_transporters.md`.
Convention used throughout for `n_perfluorinated_carbons`: a PFCA with *n* total carbons has *n*−1
perfluorinated carbons (PFOA = 7); a PFSA with *n* carbons has *n* (PFOS = 8). PFCAs are also named
by total carbon number (C7 = PFHpA, C8 = PFOA, C9 = PFNA, C10 = PFDA) because that is how the
primary papers label them.

## Which transporters mediate REABSORPTION versus SECRETION

### Takeaway
The direction is fixed by membrane localisation, not by the transporter family: basolateral uptake
transporters (OAT1, OAT3, and rat Oat1/Oat3) move PFAS from blood into the proximal tubule cell and
therefore drive **secretion**, which shortens half-life; apical uptake transporters (human OAT4 and
URAT1, rat Oatp1a1, human ASBT) move PFAS from the tubular filtrate back into the cell and therefore
drive **reabsorption**, which lengthens half-life. Apical ABC pumps (P-gp, BCRP, MRP2) efflux into
the filtrate and so add to secretion. The transporters that have been shown most convincingly to
transport PFAS on the reabsorptive side are rat Oatp1a1 and human OAT4.

### Cited Findings
- Rat proximal tubule localisation, stated explicitly: basolateral = Oat1, Oat3, Oatp4c1; brush
  border (apical) = Oat2, Urat1, Oat5, Oatp1a1, Mdr1a/b, Mrp2, Mrp4 — [Weaver 2010, Introduction](https://pmc.ncbi.nlm.nih.gov/articles/PMC2807038/)
- "Oat1 and Oat3 are involved in renal secretion of C7–C9, while Oatp1a1 can contribute to the
  reabsorption of C8 through C10, with highest affinities for C9 and C10." — [Weaver 2010, Abstract](https://pmc.ncbi.nlm.nih.gov/articles/PMC2807038/)
- "Among the three transporters expressed at the apical membrane, Oatp1a1 is the major player in the
  reabsorption of PFCAs." — [Weaver 2010, Discussion](https://pmc.ncbi.nlm.nih.gov/articles/PMC2807038/)
- "OAT4 and URAT1 are key transporters in renal reabsorption of PFCs in humans and, as a result, may
  contribute significantly to the long half-life of PFO in humans." — [Yang 2010, Abstract](https://doi.org/10.1093/toxsci/kfq219)
- Human OAT1 and OAT3 "transport perfluorooctanoic acid through the basolateral membrane of proximal
  tubular cells in vivo in both human beings and rats" — i.e. the secretory limb — [Nakagawa 2008, Abstract](https://doi.org/10.1111/j.1742-7843.2007.00155.x)
- Argoul 2026 states the direction explicitly for both species: "Uptake of short- and medium-chain
  PFASs by human OAT1, OAT3, and rat Oat1, located on the basolateral membrane, supports their roles
  in active secretion, whereas their interaction with human OAT4 and rat Oatp1a1, in the apical
  membranes of proximal tubular cells, indicates a potential contribution to tubular reabsorption."
  — [Argoul 2026, Abstract](https://doi.org/10.1007/s00204-026-04508-7)
- On the hepatic/enterohepatic side the direction is retention: NTCP (sinusoidal hepatic uptake),
  ASBT (apical ileal/renal/cholangiocyte reabsorption) and OSTα/β (basolateral export back to blood)
  together constitute enterohepatic recirculation; Zhao 2015 showed human NTCP transports PFBS,
  PFHxS and PFOS, human ASBT transports PFOS, and human OSTα/β transports all three —
  [Zhao 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4607751/)
- Efflux pumps add to secretion: Niu 2026 found PFOA, PFOS, HFPO-TA and F53B to be substrates of
  human P-gp (ABCB1) and BCRP (ABCG2) in membrane vesicles — [Niu 2026, Abstract](https://doi.org/10.1021/envhealth.6c00088)
- A caution on direction for rat Oat2: Kudo 2002 found renal Oat2 mRNA strongly female-predominant
  (male level only 13% of female) and its multiple regression partly attributed the clearance
  difference to Oat2 — [Kudo 2002, Abstract](https://doi.org/10.1016/s0009-2797(02)00006-6) — but
  both Nakagawa 2008 (hOAT2 and rOAT2, no transport) and Weaver 2010 (no net rat Oat2-mediated
  uptake of C7–C10 at 100 µM) showed PFOA is **not an Oat2 substrate**, so Oat2 cannot carry the sex
  effect — [Nakagawa 2008](https://doi.org/10.1111/j.1742-7843.2007.00155.x); [Weaver 2010, Figs 8A/9A](https://pmc.ncbi.nlm.nih.gov/articles/PMC2807038/)

### Inferences
- Because Oat1 and Oat3 sit on the secretory limb and both are *male*-predominant in rat kidney
  (Buist 2002), they push in the wrong direction to explain the longer male rat PFOA half-life. That
  is the structural reason the field converged on apical Oatp1a1 instead.
- Rat Oat2 and human OAT2 sit on opposite membranes (apical in rat, basolateral in human per Weaver
  2010 Introduction), so even if a PFAS were an OAT2 substrate its direction of effect would differ
  between species. This is a latent species-extrapolation trap that happens not to bite for PFOA.

### Gaps
- No in vitro transport data were located for OATP4C1 (basolateral, kidney), NaDC-3, MRP4 (ABCC4) or
  rat Oatp1a4/1b2 with any PFAS. Rat Oatp1b2 was tested with PFSAs by Zhao 2017 (all three
  transported) but without kinetic parameters; rat Oatp1a4 was not tested with PFAS in any paper
  retrieved. MRP2 and BCRP appear only as inhibition targets in Zhao 2015 and as efflux substrates
  in Niu 2026; NaPi-IIa/Npt2 appears only as a negative result relayed through OEHHA.
- No paper located measures net transepithelial flux direction in a polarised PFAS assay for the
  renal transporters, so "reabsorption" and "secretion" are inferred from localisation plus uptake
  direction, not measured as vectorial transport.

## Measured kinetic parameters, by transporter and PFAS

### Takeaway
There is a coherent quantitative dataset for seven renal and six hepatic/intestinal transporters.
Nearly every measured Km falls between 20 and 310 µM; the only substantially lower values are the
Caco-2 OATP Km for PFOA (8.3 µM) and the efflux-pump Km values of Niu 2026 (1.3–7.9 µM). The
chain-length pattern is sharply transporter-specific: rat Oatp1a1 affinity *increases* with chain
length (C8 126 µM → C9 20.5 µM → C10 28.5 µM), whereas rat Oat1 is tuned to C6–C8 and rat Oat3 to
C8–C9.

### Cited Findings — rat renal transporters

Weaver 2010, Table 1 (HEK293 transient transfection, 1 min, LC-MS/MS, vector-subtracted) — [source](https://pmc.ncbi.nlm.nih.gov/articles/PMC2807038/)

| Transporter | PFCA | Km (µM) | Vmax (nmol/mg protein/min) | Vmax/Km (ml/mg protein/min) |
|---|---|---|---|---|
| rat Oat1 | C7 PFHpA | 50.5 ± 13.9 | 2.2 ± 0.2 | 0.04 ± 0.01 |
| rat Oat1 | C8 PFOA | 43.2 ± 15.5 | 2.6 ± 0.3 | 0.06 ± 0.02 |
| rat Oat3 | C8 PFOA | 65.7 ± 12.1 | 3.8 ± 0.5 | 0.06 ± 0.01 |
| rat Oat3 | C9 PFNA | 174.5 ± 32.4 | 8.7 ± 0.8 | 0.05 ± 0.01 |

Weaver 2010, Table 2 (CHO cells stably expressing rat Oatp1a1, 1 min) — [source](https://pmc.ncbi.nlm.nih.gov/articles/PMC2807038/)

| Transporter | PFCA | Km (µM) | Vmax (nmol/mg protein/min) | Vmax/Km (ml/mg protein/min) |
|---|---|---|---|---|
| rat Oatp1a1 | C8 PFOA | 126.4 ± 23.9 | 9.3 ± 1.4 | 0.07 ± 0.02 |
| rat Oatp1a1 | C9 PFNA | 20.5 ± 6.8 | 3.6 ± 0.5 | 0.18 ± 0.06 |
| rat Oatp1a1 | C10 PFDA | 28.5 ± 5.6 | 3.8 ± 0.3 | 0.13 ± 0.03 |

- Rat Oatp1a1–PFOA Km independently measured as 162.2 ± 20.2 µM in a separate CHO line —
  [Yang 2009, Abstract](https://doi.org/10.1016/j.toxlet.2009.07.011). Weaver 2010 explicitly calls
  its own 126.4 µM "comparable" to this.
- Yang 2009 apparent inhibition constants (Ki,app) for inhibition of Oatp1a1-mediated
  estrone-3-sulfate uptake, quoted verbatim in the Weaver 2010 Discussion: **C6 1857.8 µM; C7 398.9 µM;
  C8 83.8 µM; C9 44.6 µM; C10 26.8 µM**; no apparent inhibition by C4 or C5 even at 1 mM —
  [Weaver 2010, Discussion](https://pmc.ncbi.nlm.nih.gov/articles/PMC2807038/); the PFHxA value is
  independently quoted as "Ki of 1,858 µM … as compared with 84 µM for PFOA" in
  [EPA 2023 IRIS PFHxA review, p. 3-11](papers/EPA%202023%20IRIS%20PFHxA%20toxicological%20review.txt)
- Rat Oat2: no significant net uptake of C7–C10 at 100 µM in either CHO-Oat2 or HEK-Oat2; most PFCAs
  did inhibit Oat2-mediated PAH uptake by 40–60% at 10 µM but with **no chain-length dependence**,
  which Weaver attributed to a poor signal-to-noise ratio — [Weaver 2010, Figs 8A, 9A](https://pmc.ncbi.nlm.nih.gov/articles/PMC2807038/)
- Rat Urat1: uric acid uptake not strongly inhibited by any PFCA at 10 µM; at 100 µM C8 gave ~30%
  inhibition, and direct C8 uptake was ~one third higher than empty vector — too weak to
  characterise — [Weaver 2010, Figs 8B, 9B](https://pmc.ncbi.nlm.nih.gov/articles/PMC2807038/)
- Rat Oat3 and Oatp1a1 (as "Oatp1") both transported PFOA in *Xenopus laevis* oocytes —
  Katakura 2007, reported second-hand in [Weaver 2010, Discussion](https://pmc.ncbi.nlm.nih.gov/articles/PMC2807038/)
  and tabulated as "both active" in [OEHHA 2021 PHG Table A6.3](papers/OEHHA%202021%20PFOA%20PFOS%20PHG%20first%20draft.txt)

### Cited Findings — human renal transporters

Louisse 2023, Table 1 (baculovirus-transduced HEK293, OAT4 vs eYFP control, 1 min, LC-MS/MS,
control-subtracted; SE in brackets) — [source](https://pmc.ncbi.nlm.nih.gov/articles/PMC9968691/)

| Transporter | PFAS | Km (µM) | Vmax (nmol/min/mg protein) | Vmax/Km (µL/min/mg protein) |
|---|---|---|---|---|
| human OAT4 | PFHpA (C7) | 60 (15) | 4.5 (0.4) | 75 |
| human OAT4 | PFOA (C8) | 47 (15) | 4.5 (0.5) | 96 |
| human OAT4 | PFNA (C9) | 58 (15) | 8.5 (0.7) | 147 |
| human OAT4 | PFDA (C10) | 39 (15) | 6.0 (0.7) | 154 |
| human OAT4 | PFBS (C4) | not transported (NA) | NA | NA |
| human OAT4 | PFHxS (C6) | 92 (33) | 7.3 (1.0) | 79 |
| human OAT4 | PFOS (C8) | 48 (24) | 2.2 (0.4) | 46 |

- Human OAT4–PFOA Km is pH-dependent: 172.3 ± 45.9 µM at pH 6 versus 310.3 ± 30.2 µM at pH 7.4
  (OAT4-mediated uptake is stimulated by low extracellular pH) —
  [Yang 2010, Abstract](https://doi.org/10.1093/toxsci/kfq219). Louisse 2023 (47 µM at the standard
  HBSS-HEPES pH 7.4) is therefore **6.6-fold lower than Yang 2010's pH 7.4 value** — a real
  inter-laboratory discrepancy, not a pH artefact.
- Human URAT1–PFOA Km = 64.1 ± 30.5 µM, measured in the absence of extracellular Cl⁻ (transport is
  driven by an outward Cl⁻ gradient) — [Yang 2010, Abstract](https://doi.org/10.1093/toxsci/kfq219).
  Louisse 2023 quotes the corresponding Vmax values as OAT4 37 and URAT1 0.32 nmol/min/mg protein,
  making URAT1's transporter efficiency 24-fold lower than OAT4's.
- **Direct contradiction on URAT1**: Louisse 2023 found "virtually no transport of PFASs … in
  URAT1-transfected HEK cells" for all seven congeners at both 1 µM and 10 µM (<2-fold over control)
  and its molecular-dynamics simulations showed no PFAS reaching the inner funnel of URAT1 —
  [Louisse 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC9968691/). Weaver 2010 similarly found rat
  Urat1 essentially inactive. Yang 2010's URAT1 Km of 64.1 µM required a non-physiological
  chloride-free buffer.
- Human OATP1A2 did **not** mediate saturable PFOA uptake (HEK293, 30 s, pH 6/7/8) — it only
  inhibited OATP1A2-mediated estrone-3-sulfate uptake — [Yang 2010, Abstract and Fig 1](https://doi.org/10.1093/toxsci/kfq219)
- Human OAT4 transports PFOA, reported without kinetic parameters —
  Nakagawa 2009 (no PubMed abstract available); characterised as "active; uptake was reported but no
  kinetic characteristics" in [OEHHA 2021 PHG Table A6.3](papers/OEHHA%202021%20PFOA%20PFOS%20PHG%20first%20draft.txt)
- Human OAT substrate/non-substrate map from OAT-transduced HEK293: OAT1 — only PFHpA and PFOA;
  OAT2 — none of the six tested; OAT3 — PFHpA, PFOA, PFNA and PFHxS but not PFBS or PFOS —
  [Louisse 2024, Abstract](https://doi.org/10.1016/j.tox.2024.153961)

Ryu 2024, HEK293 transfectant uptake-ratio screen of 14 PFAS at 5 µM, FDA 2-fold cut-off
(uptake ratio = transfected area-ratio per mg protein ÷ wild-type), with probenecid confirmation —
[source](https://pmc.ncbi.nlm.nih.gov/articles/PMC11774580/)

| Transporter | Substrates (≥2-fold) | Fold range | Weak (<2-fold) | Not above control |
|---|---|---|---|---|
| hOAT1 | PFHxA (~2×), 6:2 FTS (~15×) | 2–15× | PFHpA, PFOA, PFBS, PFPeA (5–60% above) | PFNA, PFDA, PFUnDA, PFDoDA, PFHxS, PFOS, PFOSA |
| hOAT2 | none of 14 | — | — | all 14 |
| hOAT3 | PFPeA, PFHxA, PFHpA, PFOA, PFNA, PFBS, PFHxS, 6:2 FTS | ~2.5–12× | PFBA, PFDA, PFOS (30–50% above; PFBA significant but <2×) | PFUnDA, PFDoDA, PFOSA |
| hOAT4 | PFOA, PFNA, PFBS, PFHxS, 6:2 FTS | >2× (2–4× in the probenecid follow-up) | PFHxA, PFHpA, PFOS (~20% above) | the rest |
| hOCT2 | none | — | PFDoDA, PFOSA (~10% above) | 12 of 14 |

- Niu 2026, human efflux pumps in membrane vesicles (mixed orientation; only the inside-out fraction
  supports ATP-dependent transport): BCRP Km across five PFAS spans **1.29–7.92 µmol/L** and P-gp Km
  spans **1.41–2.78 µmol/L**; Vmax/Km for P-gp was PFOA 279 > HFPO-TA 234 > PFOS 24, and for BCRP
  HFPO-TA 227 > PFOA 212 > PFOS 139 pmol/mg protein/min/(µmol/L). HFPO-DA (GenX) was transported by
  none of OAT1, P-gp or BCRP; OAT1 net PFOA uptake was 150 ± 40 pmol/mg protein at 10 µmol/L, 1 min
  — [Niu 2026, Abstract and Figs 1f, 2b,d](https://doi.org/10.1021/envhealth.6c00088)

### Cited Findings — hepatic and enterohepatic transporters

Zhao 2015, Table 2 (hNTCP in stable CHO Flp-In; rNTCP in transiently transfected HEK293;
Na⁺-dependent net uptake) — [source](https://pmc.ncbi.nlm.nih.gov/articles/PMC4607751/)

| Transporter | PFAS | Km (µM) | Vmax (nmol/mg protein/min) | Vmax/Km (ml/mg protein/min) |
|---|---|---|---|---|
| human NTCP | PFBS | 39.6 ± 8.2 | 3.7 ± 0.3 | 0.1 ± 0.02 |
| human NTCP | PFHxS | 112 ± 32.9 | 23.2 ± 3.0 | 0.2 ± 0.07 |
| human NTCP | PFOS | 130 ± 32.9 | 30.7 ± 3.2 | 0.2 ± 0.06 |
| rat Ntcp | PFBS | 76.2 ± 23.6 | 2.2 ± 0.3 | 0.03 ± 0.01 |
| rat Ntcp | PFHxS | 294 ± 121 | 8.1 ± 1.8 | 0.03 ± 0.01 |

Zhao 2017, Tables 3 and 4 — [source](https://pmc.ncbi.nlm.nih.gov/articles/PMC6075085/)

| Transporter | PFAS | Km (µM) | Vmax (nmol/mg protein/min) | Vmax/Km (µL/mg protein/min) |
|---|---|---|---|---|
| human OATP1B1 | PFBS | 80 ± 47 | 0.25 ± 0.06 | 2.5 |
| human OATP1B1 | PFHxS | 101 ± 32 | 2.10 ± 0.31 | 21 |
| human OATP1B1 | PFOS | 23 ± 6 | 0.80 ± 0.07 | 35 |
| human OATP1B3 | PFBS | 63 ± 37 | 0.24 ± 0.07 | 3.2 |
| human OATP1B3 | PFHxS | 86 ± 24 | 2.43 ± 0.27 | 28 |
| human OATP1B3 | PFOS | 32 ± 19 | 1.02 ± 0.24 | 31 |
| human OATP2B1 | PFBS | 122 ± 57 | 0.56 ± 0.11 | 4.9 |
| human OATP2B1 | PFHxS | 53 ± 19 | 1.99 ± 0.22 | 38 |
| human OATP2B1 | PFOS | 48 ± 19 | 4.73 ± 0.65 | 99 |
| rat Oatp1a1 | PFHxS | 256 ± 69 | 1.01 ± 0.14 | 3.9 |
| rat Oatp1a1 | PFOS | 37 ± 19 | 0.66 ± 0.14 | 19 |
| rat Oatp1a5 | PFBS | 117 ± 41 | 0.23 ± 0.04 | 1.7 |
| rat Oatp1a5 | PFHxS | 160 ± 122 | 1.24 ± 0.47 | 7.5 |
| rat Oatp1a5 | PFOS | 55 ± 18 | 1.18 ± 0.13 | 22 |

- Rat Oatp1b2 and rat Oatp2b1 transported all three PFSAs; net uptake of PFBS was about 10-fold
  lower than PFHxS and PFOS (10 µM, 1 and 5 min) — [Zhao 2017, Fig 6](https://pmc.ncbi.nlm.nih.gov/articles/PMC6075085/)
- For the carboxylates, the same three human OATPs "can transport the longer chain PFOA (C8) and
  perfluorononanoate (C9), but not the shorter chain perfluoroheptanoate (C7)" —
  [EPA 2024 PFOA assessment §3.3.1.4.2, citing Zhao 2017b](papers/EPA%202024%20PFOA%20human%20health%20toxicity%20assessment.txt)
- Freshly isolated rat hepatocytes, saturable active PFOA uptake after subtracting the non-saturable
  partition measured on ice: male Km 88.0 ± 9.1 µM, Vmax 5.61 ± 0.88 nmol/min/10⁶ cells, active
  clearance 64.8 ± 15.7 µL/min/10⁶ cells; female Km 76.1 ± 12.0 µM, Vmax 3.59 ± 0.29, clearance
  47.6 ± 4.7; sulfobromophthalein inhibition Ki 85.9 ± 25.1 (male) and 29.3 ± 19.2 µM (female); when
  albumin was added, uptake fell but stayed proportional to the unbound fraction —
  [Han 2008, Abstract](https://doi.org/10.1016/j.toxlet.2008.07.002)
- Caco-2 apical PFOA uptake: Km 8.3 µM, saturable uptake clearance (Vmax/Km) 55.0 µL/mg protein/min,
  about 3-fold the non-saturable clearance of 18.1 µL/mg protein/min; Na⁺-independent; competitively
  inhibited by sulfobromophthalein with Ki 23.1 µM; inhibited by BSP, glibenclamide,
  estrone-3-sulfate, cyclosporin A and rifamycin SV but **not** by probenecid or p-aminohippurate
  (so OATPs, not OATs) and not by lactate or benzoate (not MCTs) —
  [Kimura 2017, Abstract](https://doi.org/10.1016/j.toxlet.2017.05.012)
- Caco-2 OATP inhibition is medium-chain selective: C7–C11 PFCAs decreased sulfobromophthalein
  uptake by 27–55%, while C3–C6 and C12–C14 had only slight effects; Dixon-plot competitive Ki =
  PFOA 62.2 ± 1.3, PFNA 35.3 ± 0.1, PFDA 43.2 ± 0.3 µM; PFOS at 100 µM reduced BSP uptake to
  46.1 ± 4.5% of control. The authors propose OATP2B1, the most abundant OATP in Caco-2 —
  [Kimura 2020, Table 1 and Fig 4](https://pmc.ncbi.nlm.nih.gov/articles/PMC7490525/)
- Efflux-pump inhibition in Sf9 membrane vesicles (no PFAS transport demonstrated, inhibition only):
  human MRP2-mediated CDCF transport was unaffected by PFBS, inhibited by 100 µM PFHxS, and
  inhibited >80% by 100 µM PFOS (significant also at 10 µM); human BCRP-mediated estrone-3-sulfate
  transport fell with all three PFAS but only 100 µM PFHxS reached significance; BSEP-mediated
  taurocholate transport was inhibited only by 100 µM PFOS —
  [Zhao 2015, Fig 6](https://pmc.ncbi.nlm.nih.gov/articles/PMC4607751/)
- Requested non-transporter target, for completeness: human carboxylesterase IC50 values are
  CES1 — PFDoA 10.6, PFTA 13.4, PFOcDA 12.6 µM; CES2 — PFDoA 9.56, PFTA 17.2, PFOcDA 8.73 µM, all
  noncompetitive (Ki 4.04–29.1 µM). The paper's own IVIVE put the plasma thresholds for in vivo
  interference at 0.40–2.91 µM — [Liu 2020, Abstract](https://doi.org/10.1016/j.envpol.2020.114463)

### Inferences
- Rat Oatp1a1 is the only transporter whose affinity ordering (C9 ≈ C10 > C8 ≫ C7 ≫ C6, no C4/C5
  interaction) matches the in vivo rank order of rat renal retention, and Yang 2009 reported a
  positive linear relationship between log Ki,app and log total clearance in male rats. That
  structure-activity match, not the absolute Km, is the strongest single piece of evidence tying a
  specific transporter to the rat sex and chain-length pattern.
- Transporter efficiency (Vmax/Km) varies far less across congeners than Km does — Louisse 2023 found
  only a 3.3-fold spread in OAT4 efficiency across six PFAS while human half-lives for the same
  congeners span from ~0.17 y (PFHpA) to 8.5 y (PFHxS). The authors concluded explicitly that "no
  direct correlation between these two parameters exists".

### Gaps
- Louisse 2024's actual Km and Vmax table for human OAT1/OAT2/OAT3 could not be retrieved (Elsevier
  paywall, no PMC record). Only the substrate/non-substrate classification from the abstract is in
  the database. This is the single largest numeric gap.
- Niu 2026's per-congener Km and Vmax for P-gp, BCRP and OAT1 live only inside figures, so the
  database holds the ranges and the Vmax/Km ratios but not the individual Km values.
- No Km was located for any PFAS with MRP4, OATP4C1, NaDC-3, or rat Oatp1a4.

## Direct human-vs-rat-vs-mouse orthologue comparisons in the same expression system

### Takeaway
Three studies measured human and rat orthologues side by side, and all three reached the same
conclusion: the orthologue *affinities* differ by less than ~2–4-fold and cannot explain the
10–100-fold species differences in PFAS half-life. The one qualitative species difference found
(human ASBT transports PFOS, rat Asbt transports none of the PFSAs) runs opposite to the direction
needed. No study was found that measured mouse orthologue transport kinetics at all.

### Cited Findings
- **Nakagawa 2008** measured human and rat OAT1, OAT2 and OAT3 in the same transient expression
  system with [¹⁴C]PFOA: hOAT1 48.0 ± 6.4, rOAT1 51.0 ± 12.0, hOAT3 49.1 ± 21.4, rOAT3 80.2 ± 17.8 µM;
  neither hOAT2 nor rOAT2 transported PFOA. Conclusion: "the species differences in its renal
  elimination are not attributable to affinity differences in these OATs between human beings and
  rats … the difference between the perfluorooctanoic acid half-lives in human beings and rats is not
  likely to be attributable to differences in the affinities of these transporters" —
  [Nakagawa 2008, Abstract](https://doi.org/10.1111/j.1742-7843.2007.00155.x).
  Largest human/rat ratio: rOAT3/hOAT3 Km = 1.6-fold.
- **Zhao 2015** compared human and rat NTCP and ASBT. hNTCP vs rNTCP Km: PFBS 39.6 vs 76.2 µM
  (1.9-fold), PFHxS 112 vs 294 µM (2.6-fold); hNTCP Vmax values were 2.8–6.3-fold higher than rNTCP,
  giving hNTCP a 3–7-fold higher efficiency. For ASBT the difference was qualitative: Na⁺-dependent
  uptake of PFOS was seen with human ASBT but **none of PFBS, PFHxS or PFOS was transported by rat
  ASBT** — [Zhao 2015, Table 2 and Fig 7](https://pmc.ncbi.nlm.nih.gov/articles/PMC4607751/)
- **Zhao 2017** compared human OATP1B1/1B3/2B1 against rat Oatp1a1/1a5/1b2/2b1 for the same three
  PFSAs. For PFOS the human efficiencies were 35, 31 and 99 µL/mg protein/min against rat Oatp1a1 19
  and Oatp1a5 22 — the same order of magnitude — [Zhao 2017, Tables 3 and 4](https://pmc.ncbi.nlm.nih.gov/articles/PMC6075085/)
- **Argoul 2026** tested ten PFAS against eight human and four rat renal transporters and found the
  same chain-length threshold in both species: "The comparable PFAS chain-length threshold for the
  uptake of PFASs by homologous human and rat renal transporters suggests that additional mechanisms
  may account for interspecies differences in PFAS renal clearance" —
  [Argoul 2026, Abstract](https://doi.org/10.1007/s00204-026-04508-7)
- Pharmacology-level corroboration of the mismatch: human serum half-lives for PFHxS and PFOS are
  7.3 y (95% CI 5.8–9.2) and 4.8 y (4.0–5.8) against ~1 month for PFOS and 30 days (male) / 2 days
  (female) for PFHxS in Sprague-Dawley rats — [Zhao 2015, Introduction](https://pmc.ncbi.nlm.nih.gov/articles/PMC4607751/)

### Inferences
- The species difference in PFAS half-life is therefore unlikely to be an affinity (Km) effect. The
  remaining candidate explanations are differences in transporter *abundance* per gram kidney,
  differences in which orthologue occupies which membrane (rat has apical Oatp1a1, which humans
  lack entirely as a renal apical reabsorptive OATP), differences in GFR per kg, and differences in
  plasma protein binding and free fraction.
- Human ASBT transporting PFOS while rat Asbt does not is the one measured species difference whose
  sign is right for a longer human half-life (more enterohepatic reabsorption in humans), though no
  kinetic parameters exist for it.

### Gaps
- **No mouse orthologue transport kinetics were found for any PFAS and any transporter.** Every
  mouse datum located is an mRNA-expression study. The mouse limb of the requested three-way
  kinetic comparison does not exist in the retrieved literature.

## Is rat Oatp1a1 androgen-regulated, is the mouse orthologue the same, and is there a direct rat-vs-mouse kidney comparison?

### Takeaway
Yes for rat: renal Oatp1a1 is male-predominant and androgen-controlled, and this is the mechanism
invoked for the large rat sex difference in PFOA elimination. Critically, **mouse renal Oatp1a1 is
also male-predominant and also androgen-induced**, so the Oatp1a1 argument is not rat-specific — which
weakens any attempt to use Oatp1a1 regulation alone to explain a rat-versus-mouse difference. One
abstract in the mouse literature contradicts itself on the direction, and the reported magnitude of
the rat male/female Oatp1a1 difference varies several-fold between secondary sources.

### Cited Findings — the rat side
- Male rat PFOA half-life is 70× the female; renal clearance is the locus; castration raised male
  renal clearance **14-fold** to the female level and testosterone reversed it; estradiol raised male
  clearance; ovariectomy raised female clearance and estradiol lowered it; testosterone lowered
  female clearance. Renal *oatp1* (Oatp1a1) and OAT-K mRNA were significantly higher in males, and
  castration or estradiol reduced both — [Kudo 2002, Abstract](https://doi.org/10.1016/s0009-2797(02)00006-6)
- "Oatp1a1 is an important transporter expressed on the apical membrane of proximal tubule cells with
  a male-dominant expression pattern" — [Weaver 2010, Discussion](https://pmc.ncbi.nlm.nih.gov/articles/PMC2807038/)
- "Due to the sex-dependent expression of Oatp1a1 in rat kidney, Oatp1a1-mediated tubular
  reabsorption is suggested to be the mechanism for the sex-dependent renal elimination of PFO in
  rats" — [Yang 2009, Abstract](https://doi.org/10.1016/j.toxlet.2009.07.011)
- Regulatory syntheses: "In rats, kidney Oatp1a1 is expressed at the apical membrane of the proximal
  tubule … In male rats, Oatp1a1 mRNA expression was 2.5-fold greater than in females, undetectable
  in castrated rats … Gotoh et al. (2002) confirmed that Oatp1a1 protein levels were undetectable
  from female rat kidney and highly expressed in male rat kidney" —
  [EPA 2023 IRIS PFHxA review, p. 3-11](papers/EPA%202023%20IRIS%20PFHxA%20toxicological%20review.txt)
- **Conflicting magnitude** from the other EPA document: "The level of messenger ribonucleic acid
  (mRNA) of OATP1a1 in male rat kidney is 5–20-fold higher than in female rat kidney and is regulated
  by sex hormones" — [EPA 2024 PFOA assessment §3.3.1.4.2](papers/EPA%202024%20PFOA%20human%20health%20toxicity%20assessment.txt).
  Neither 2.5-fold nor 5–20-fold appears in the Kudo 2002 abstract, which gives no fold value for
  oatp1 at all; Gotoh 2002 reported the protein as simply undetectable in females.
- The rat secretory Oats run the *other* way: renal Oat1 is male-predominant and renal Oat2 strongly
  female-predominant, and the Oat1 difference is androgen-driven while the Oat2 difference is driven
  by the female growth-hormone secretion pattern, not by sex steroids —
  [Buist 2002](https://doi.org/10.1124/jpet.301.1.145); [Buist 2003](https://doi.org/10.1124/dmd.31.5.559)
- Weaver 2010 adds an important caveat: "the rats used in the C8 renal elimination study done by Kudo
  et al. (2002) did not show marked differences at the mRNA level for either Oat1 or Oat3 … additional
  transporters must be involved in the observed gender-dependent renal excretion pattern" —
  [Weaver 2010, Discussion](https://pmc.ncbi.nlm.nih.gov/articles/PMC2807038/)

### Cited Findings — the mouse side
- Mouse tissue survey of all 15 Oatps: "In kidney, expression of Oatp1a1, 3a1, and 4c1 was higher in
  males than in females"; Oatp1a1, 1a6, 3a1 and 4c1 are the highly expressed renal mouse Oatps; in
  liver Oatp1a1 is male-predominant while Oatp1a4 and 1a6 are female-predominant —
  [Cheng 2005, Abstract](https://doi.org/10.1124/dmd.105.003640)
- Mouse hormone manipulation (gonadectomised, *lit/lit*, hypophysectomised mice with sex-hormone or
  GH replacement): "Androgens increased Oatp1a1 mRNA in liver and kidney, whereas male-pattern GH
  administration increased Oatp1a1 mRNA in livers but not in kidneys … In kidney, gender-divergent
  Oatp expression is exclusively caused by stimulation by androgens" —
  [Cheng 2006, Abstract](https://doi.org/10.1124/mol.106.025122)
- ⚠ **Internal contradiction to flag for the report writer**: the same Cheng 2006 abstract also states
  "in kidneys, Oatp1a1 and Oatp3a1 are both female-predominant", which conflicts with Cheng 2005 from
  the same laboratory and with Cheng 2006's own androgen-stimulation conclusion. The weight of
  evidence (the 2005 tissue survey plus the androgen-induction experiment) supports
  **male-predominant mouse renal Oatp1a1**.

### Cited Findings — direct rat-vs-mouse kidney comparison
- The only direct rat-vs-mouse renal transporter comparison located is for the Oats, not the Oatps:
  "Mouse Oat1 mRNA was primarily expressed in kidney of both strains, with male predominance. Mouse
  Oat2 mRNA levels were highest in kidney of both strains **without gender predominance** … The most
  notable species differences in Oat mRNA expression were a lack of Oat2 female predominance in mouse
  kidney and a less dramatic Oat3 male predominance in mouse liver. With the exception of a
  significant species difference in Oat2 expression, many similarities were found between rat and
  mouse Oat mRNA levels." — [Buist & Klaassen 2004, Abstract](https://doi.org/10.1124/dmd.32.6.620)
- Regulatory framing: "In rats and mice, expression of OAT1, OAT3, and OATP1a1 is controlled by male
  sex hormones and shows higher activities in males (Buist and Klaassen 2004; Gotoh et al. 2002;
  Kobayashi et al. 2002; Li et al. 2002; Lu et al. 1996; Lubojevic et al. 2004)" —
  [ATSDR 2021, Section 3](papers/ATSDR%202021%20Toxicological%20Profile%20Perfluoroalkyls.txt)
- Net tubular handling by species, from the OEHHA compilation of Han 2012 (Table A6.4): male rat
  93.7% of filtered PFOA reabsorbed vs net secretion in female rats; male mouse 97% reabsorbed and
  female mouse 95.2%; human 99.8% — [OEHHA 2021 PHG Table A6.4](papers/OEHHA%202021%20PFOA%20PFOS%20PHG%20first%20draft.txt)

### Inferences
- The androgen-regulated, male-predominant, apical Oatp1a1 story is **shared by rat and mouse**, so it
  cannot by itself explain a rat-versus-mouse difference in PFOA kinetics. The OEHHA/Han 2012
  reabsorption figures are consistent with that: mice reabsorb 95–97% of filtered PFOA in *both*
  sexes, with no female "net secretion" state of the kind rats show. Something other than Oatp1a1
  presence/absence — most plausibly the balance between apical reabsorption and basolateral secretory
  capacity, or GFR per kg — must set the rat/mouse difference.
- The "~20–40× faster PFOA elimination in female rats" framing in the assignment is roughly
  consistent with the primary data but the primary number is larger: Kudo 2002 reported a 70-fold
  half-life ratio and a 14-fold change in renal clearance on castration. Worley & Fisher's PBPK model
  needed a ~25,800-fold male/female ratio in the *fitted* apical relative activity factor to
  reproduce the observed data, which is far larger than any measured Oatp1a1 expression difference.

### Gaps
- No study was found that measures rat and mouse renal **Oatp1a1** side by side in the same assay. The
  Buist & Klaassen 2004 direct comparison covers Oat1–Oat3 only.
- No study was found that measures mouse Oatp1a1 (or any mouse transporter) PFAS transport kinetics,
  so the inference above rests on expression plus the rat kinetic data.
- The 2.5-fold (EPA PFHxA) versus 5–20-fold (EPA PFOA) discrepancy in the rat male/female Oatp1a1
  mRNA ratio could not be resolved, because Kudo 2002's full text is paywalled and the abstract gives
  no fold value. **Do not state a single fold value for this in the report without first obtaining
  Kudo 2002 or Lu 1996 in full.**

## Km values versus realistic serum concentrations: can transporter saturation occur at human exposures?

### Takeaway
No. Measured Km values are tens to hundreds of µM while general-population serum PFAS are low nM, a
gap of roughly 3.5–4.5 orders of magnitude. Even the most highly exposed fluorochemical workers sit
~170-fold below the human OAT4 Km for PFOA. Transporter kinetics are therefore effectively
first-order at all realistic human exposures, so saturation cannot be invoked to explain
dose-dependence in humans — and in a PBPK model the transporter terms reduce to a linear clearance.

### Cited Findings
Serum concentrations (all from documents in `papers/`):

| PFAS | Serum (ng/mL) | Serum (nM) | Serum (µM) | Source |
|---|---|---|---|---|
| PFOA | 1.56 | 3.8 | 0.0038 | NHANES 2015–2016 geometric mean, CDC 2018 via [ATSDR 2021](papers/ATSDR%202021%20Toxicological%20Profile%20Perfluoroalkyls.txt) |
| PFOA | 3.61 | 8.7 | 0.0087 | NHANES 2009–2010 adult males geometric mean, via [ATSDR 2021](papers/ATSDR%202021%20Toxicological%20Profile%20Perfluoroalkyls.txt) |
| PFOA | 5.2 | 12.6 | 0.0126 | NHANES 1999–2000 geometric mean, CDC 2018 via [ATSDR 2021](papers/ATSDR%202021%20Toxicological%20Profile%20Perfluoroalkyls.txt) |
| PFOA | 9.7 | 23.4 | 0.0234 | NHANES 2007–2008 95th percentile, [EPA 2024](papers/EPA%202024%20PFOA%20human%20health%20toxicity%20assessment.txt) |
| PFOA | 113 | 272.9 | 0.273 | median serum in fluorochemical workers, 2005, [EPA 2024](papers/EPA%202024%20PFOA%20human%20health%20toxicity%20assessment.txt) |
| PFOS | 4.72 | 9.4 | 0.0094 | NHANES 2013–2014 geometric mean, CDC 2018 via [ATSDR 2021](papers/ATSDR%202021%20Toxicological%20Profile%20Perfluoroalkyls.txt) |
| PFOS | 30.4 | 60.8 | 0.0608 | NHANES 1999–2000 geometric mean, CDC 2018 via [ATSDR 2021](papers/ATSDR%202021%20Toxicological%20Profile%20Perfluoroalkyls.txt) |

Km-to-serum ratios (molecular weights from [Ryu 2024, Table 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC11774580/):
PFOA 414.07, PFOS 500.13, PFHxS 400.12 g/mol; conversions performed by this reviewer):

| Transporter | PFAS | Km (µM) | Serum used (µM) | Km ÷ serum | Km source |
|---|---|---|---|---|---|
| human OAT4 | PFOA | 47 | 0.0038 (NHANES 2015–16 GM) | ~12,500× | Louisse 2023 Table 1 |
| human OAT4 | PFOA | 310.3 | 0.0038 | ~82,000× | Yang 2010, pH 7.4 |
| human URAT1 | PFOA | 64.1 | 0.0038 | ~17,000× | Yang 2010 |
| human OAT1 | PFOA | 48.0 | 0.0038 | ~12,700× | Nakagawa 2008 |
| human OAT3 | PFOA | 49.1 | 0.0038 | ~13,000× | Nakagawa 2008 |
| rat Oatp1a1 | PFOA | 126.4 | 0.0038 | ~33,600× | Weaver 2010 Table 2 |
| human OAT4 | PFOS | 48 | 0.0094 (NHANES 2013–14 GM) | ~5,100× | Louisse 2023 Table 1 |
| human NTCP | PFOS | 130 | 0.0094 | ~13,800× | Zhao 2015 Table 2 |
| human OATP1B1 | PFOS | 23 | 0.0094 | ~2,400× | Zhao 2017 Table 3 |
| human OATP2B1 | PFOS | 48 | 0.0094 | ~5,100× | Zhao 2017 Table 3 |
| human OAT4 | PFHxS | 92 | 0.0054 (2.16 ng/mL GM) | ~17,000× | Louisse 2023 Table 1; serum GM from [ATSDR 2021](papers/ATSDR%202021%20Toxicological%20Profile%20Perfluoroalkyls.txt) |
| Caco-2 OATP | PFOA | 8.3 | 0.0038 | ~2,200× | Kimura 2017 |
| human OAT4 | PFOA | 47 | 0.273 (fluorochemical workers) | ~170× | Louisse 2023 Table 1 |

- The regulatory documents make the same point qualitatively and raise one important caveat: the
  concentration the apical transporter actually sees is the *tubular fluid* concentration, not serum.
  "As most of the water is resorbed from the renal filtrate, however, the concentration of PFHxA in
  the remaining fluid will increase proportionately. Thus, the PFHxA concentrations in the proximal
  tubule of these rats (where Oatp1a1 is expressed) could be high enough for significant transporter
  activity, but below the level of saturation." —
  [EPA 2023 IRIS PFHxA review, p. 3-11](papers/EPA%202023%20IRIS%20PFHxA%20toxicological%20review.txt)
- Where saturation *has* plausibly been observed, it is at therapeutic/occupational doses, not
  environmental ones: "saturation of this transporter could result in an increase in urinary
  elimination of perfluoroalkyls due to decreased tubular reabsorption. This is consistent with the
  apparent plateau in plasma concentration with increasing dose observed in cancer patients treated
  with PFOA (Convertino et al. 2018)." — [ATSDR 2021, Section 3](papers/ATSDR%202021%20Toxicological%20Profile%20Perfluoroalkyls.txt)
- Worley & Fisher's rat PBPK model explicitly assumed saturable proximal tubule transporters and the
  model "predicts an increase in" urinary elimination at high doses as a result —
  [EPA 2024, citing Worley and Fisher](papers/EPA%202024%20PFOA%20human%20health%20toxicity%20assessment.txt);
  the model's own Km values were 27.20 µg/mL (basolateral) and 52.3 µg/mL (apical), i.e. 65.7 and
  126.3 µM — [Worley 2015, Table 3](https://pmc.ncbi.nlm.nih.gov/articles/PMC4662604/)
- Liu 2020's IVIVE for carboxylesterase inhibition reaches the same conclusion for a different target
  class: in vivo interference was predicted only above plasma concentrations of 0.40–2.91 µM,
  i.e. 100–750× above current general-population PFOA serum levels —
  [Liu 2020, Abstract](https://doi.org/10.1016/j.envpol.2020.114463)

### Inferences
- Because serum concentrations are 3.5–4.5 orders of magnitude below Km, the saturable Michaelis-Menten
  terms in a transporter-based PBPK model operate in their linear regime at human exposures, so
  Vmax/Km (the transporter efficiency) rather than Km or Vmax separately is the parameter that matters
  for human dosimetry. This is also why Louisse 2023 reported efficiencies rather than Km alone.
- The tubular-concentration caveat matters quantitatively: with ~99% water reabsorption the filtrate
  can concentrate roughly 100-fold, which closes about two of the four orders of magnitude but still
  leaves general-population exposures ~100× below Km. Saturation of apical reabsorption at
  environmental exposures remains implausible; at occupational levels (113 ng/mL serum) with tubular
  concentration it becomes arguable.
- The inter-laboratory spread in OAT4–PFOA Km (47 µM in Louisse 2023 against 310 µM in Yang 2010 at
  the same nominal pH) is a 6.6-fold uncertainty that propagates directly into any Vmax/Km-based
  IVIVE. The report should carry both values rather than choosing.

### Gaps
- Human tubular-fluid PFAS concentrations have not been measured, so the concentration factor between
  serum and the apical surface is an assumption rather than a datum.
- No source located reports a measured concentration-dependence of human renal PFAS clearance across
  a range wide enough to test for saturation directly; the Convertino 2018 PFOA plateau is cited
  second-hand through ATSDR.

## Which PFAS are substrates versus only inhibitors; chain-length and head-group dependence

### Takeaway
Substrate status is sharply bounded on both sides. Short chains (≤C5 PFCA, PFBS) interact weakly or
not at all with the reabsorptive transporters; long chains (PFDA, PFUnDA, PFDoDA, PFOS, PFOSA) are
increasingly excluded from the OATs even though they inhibit them, and the newest study (Argoul 2026)
reports them as substrates of nothing. The most transported window is C6–C9 carboxylates and
C4–C6 sulfonates. Several PFAS are inhibitors of transporters that do not transport them.

### Cited Findings
- Clear inhibitor-but-not-substrate cases: rat Oat2 (40–60% inhibition of PAH uptake at 10 µM by most
  PFCAs, but no net uptake of C7–C10 at 100 µM) and rat Urat1 — [Weaver 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC2807038/);
  human OATP1A2 (inhibits estrone-3-sulfate uptake but does not transport PFOA) —
  [Yang 2010](https://doi.org/10.1093/toxsci/kfq219); human MRP2, BCRP and BSEP in Sf9 vesicles
  (inhibition of model substrates only) — [Zhao 2015, Fig 6](https://pmc.ncbi.nlm.nih.gov/articles/PMC4607751/)
- Chain-length window for apical reabsorption in rat: Oatp1a1 Ki,app falls monotonically from
  1857.8 µM (C6) through 398.9 (C7), 83.8 (C8), 44.6 (C9) to 26.8 µM (C10), with no interaction at all
  for C4 and C5 even at 1 mM — [Yang 2009 values quoted in Weaver 2010, Discussion](https://pmc.ncbi.nlm.nih.gov/articles/PMC2807038/)
- Chain-length window for basolateral secretion in rat: Oat1 inhibited significantly only by C6, C7
  and C8 at 10 µM (C7 strongest); Oat3 by C8 and C9 (then C7, C10) — [Weaver 2010, Fig 2](https://pmc.ncbi.nlm.nih.gov/articles/PMC2807038/)
- Head-group effect on the same transporter: human OAT4 transported PFHpA, PFOA, PFNA and PFDA
  (carboxylates, all four) and PFHxS and PFOS (sulfonates) but **not PFBS**; the authors attributed the
  PFBS exclusion to a post-recognition step — PFBS docked like a substrate but in molecular dynamics
  slid laterally off the transporter mouth rather than moving inward, whereas PFHxS drew "a clear
  inward trajectory" — [Louisse 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC9968691/)
- Head-group effect across transporters: human OAT3 took PFHpA, PFOA, PFNA and PFHxS but not PFBS or
  PFOS; human OAT1 took only PFHpA and PFOA — [Louisse 2024, Abstract](https://doi.org/10.1016/j.tox.2024.153961)
- Upper chain-length cut-off, from the largest screen: in Ryu 2024 none of PFDA, PFUnDA, PFDoDA or
  PFOSA reached the 2-fold uptake-ratio threshold for any of hOAT1, hOAT2, hOAT3, hOAT4 or hOCT2, and
  these were exactly the compounds classified as ECCS class 1B (high permeability) with Papp values of
  8.4–41.4 ×10⁻⁶ cm/s against 0.9–4.1 for the shorter chains. "In line with expectations, no Class 1B
  PFAS were shown to be substrates for hOAT1–3" — [Ryu 2024, Table 1 and Results](https://pmc.ncbi.nlm.nih.gov/articles/PMC11774580/)
- Independent confirmation of the upper cut-off: "long-chain PFASs (PFDA, PFOS, PFDS) were not
  substrates for any tested transporter in either species" (eight human and four rat renal
  transporters) — [Argoul 2026, Abstract](https://doi.org/10.1007/s00204-026-04508-7). Note this
  conflicts with Louisse 2023 (PFDA and PFOS *are* OAT4 substrates, Km 39 and 48 µM) and with
  Weaver 2010 (rat Oatp1a1 transports C10 with Km 28.5 µM) — a substantive unresolved disagreement.
- Novel/replacement PFAS: HFPO-DA (GenX) was transported by none of human OAT1, P-gp or BCRP, whereas
  HFPO-TA and both components of F53B were substrates of all three —
  [Niu 2026, Abstract](https://doi.org/10.1021/envhealth.6c00088). Argoul 2026, in contrast, reports
  GenX and PFO2OA as "likely substrates for human OAT3, rat Oat1, and rat Oatp1a1" —
  [Argoul 2026](https://doi.org/10.1007/s00204-026-04508-7). The fluorotelomer sulfonate 6:2 FTS was
  the single strongest hOAT1 substrate in Ryu 2024 (~15-fold uptake ratio).
- Intestinal/hepatic OATPs show the same medium-chain preference: C7–C11 PFCAs inhibited Caco-2
  sulfobromophthalein uptake by 27–55%, while C3–C6 and C12–C14 had only slight effects —
  [Kimura 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7490525/)

### Inferences
- The upper chain-length cut-off is likely an assay artefact as much as a biological fact: as Papp
  rises with chain length (Ryu 2024: 0.9 → 41 ×10⁻⁶ cm/s from PFBA to PFOSA) the passive component
  swamps the transporter-mediated component, so the transfected-minus-control ratio collapses toward
  1 even if the transporter is working. Ebert 2020's finding that measured passive permeabilities are
  "high enough to explain observed cellular uptake by passive diffusion with no need to postulate the
  existence of active uptake processes" makes this the single most serious threat to the validity of
  the whole uptake-ratio literature — [Ebert 2020](https://doi.org/10.1021/acs.est.0c00175)
- Sulfonates behave like carboxylates one or two carbons longer, consistent with the sulfonate head
  group adding hydrophobic bulk: PFHxS (6 perfluorinated C) is handled by OAT4 and OAT3 much as PFOA
  (7 perfluorinated C) is, and PFBS behaves like a short-chain carboxylate.

### Gaps
- The Argoul 2026 versus Louisse 2023 / Weaver 2010 disagreement about whether PFDA and PFOS are
  substrates at all could not be resolved because Argoul 2026 is paywalled; only its abstract was
  obtained.

## In vitro systems used and their limitations for extrapolating to in vivo clearance

### Takeaway
Six system types appear: transiently or stably transfected HEK293 and CHO cells (the workhorse, used
by Weaver, Nakagawa, Yang, Zhao, Louisse, Ryu and Niu), *Xenopus* oocytes (Katakura 2007), Caco-2
monolayers (Kimura), freshly isolated primary rat hepatocytes (Han 2008), Sf9 and commercial
mammalian membrane vesicles (Zhao 2015; Niu 2026), and human RPTEC proximal-tubule models in 2D,
Transwell and Transwell-with-flow formats (Lin 2024; Sakolish 2026). The decisive limitation shared by
all transfectant uptake-ratio assays is that PFAS passive permeability is high enough to generate or
mask apparent transporter effects.

### Cited Findings
- Transfectant assays define substrate status by a ratio against an empty-vector or wild-type control,
  with a 2-fold threshold taken from FDA guidance; the ratio is
  (transfected area-ratio per mg protein) ÷ (wild-type per mg protein) —
  [Ryu 2024, Methods](https://pmc.ncbi.nlm.nih.gov/articles/PMC11774580/). Weaver 2010 and Louisse 2023
  both subtract the control value rather than dividing, then fit Michaelis-Menten to the remainder.
- Weaver 2010 names the sensitivity limit explicitly for rat Oat2: "The general inhibition by PFCAs
  observed could be due to the low signal to noise ratio since the amount of PAH transported into
  Oat2-expressing cells is only about twice as much as that of wild-type cells" —
  [Weaver 2010, Discussion](https://pmc.ncbi.nlm.nih.gov/articles/PMC2807038/)
- Han 2008 shows how to handle the passive component in a primary system: non-saturable partition was
  measured by on-ice incubation and subtracted before fitting the active Km and Vmax; and when albumin
  was present, uptake "were reduced, but were proportional to the unbound fractions of PFO" —
  [Han 2008, Abstract](https://doi.org/10.1016/j.toxlet.2008.07.002)
- Kimura 2017 quantified both components in Caco-2: saturable clearance 55.0 against non-saturable
  18.1 µL/mg protein/min, i.e. the carrier accounts for only ~3-fold more than passive —
  [Kimura 2017](https://doi.org/10.1016/j.toxlet.2017.05.012)
- Membrane vesicles measure only the inside-out fraction: "P-gp and BCRP efflux activities were
  evaluated using membrane vesicles with mixed orientation, in which only the inside-out vesicle
  fraction supports ATP-dependent transport" — [Niu 2026, Methods](https://doi.org/10.1021/envhealth.6c00088).
  Vesicle Km values (1.3–7.9 µM) are an order of magnitude lower than whole-cell Km values from the
  same compounds, which may reflect the absence of the plasma-membrane permeability barrier.
- Culture format changes the answer by 10–100-fold in human RPTEC: "the Transwell-based models,
  regardless of whether the flow/shear stress were present, had the best human in vivo concordance in
  terms of predicting absolute values for renal clearance, with estimates within about 10-fold",
  whereas "our results from 2D culture suggested a systematic underprediction of clearance under this
  protocol, which could warrant development of a scaling factor" —
  [Lin 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11585971/)
- Even OAT1 over-expression can backfire: "the predicted renal clearance of tenofovir using
  OAT1-overexpressing cells was significantly lower than that using parental cells, which corresponded
  to a roughly 100-fold lower P ratio" — [Sakolish 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC12951621/)
- The fundamental challenge to the field: Ebert 2020 measured membrane/water partition coefficients and
  anionic membrane permeabilities and concluded permeabilities "were high enough to explain observed
  cellular uptake by passive diffusion with no need to postulate the existence of active uptake
  processes" — [Ebert 2020](https://doi.org/10.1021/acs.est.0c00175). EPA 2024 picks this up:
  "movement across interface membranes was thought to be dominated by transporters or … however,
  support transporter-independent uptake through passive diffusion processes. Ebert et [al.]" —
  [EPA 2024](papers/EPA%202024%20PFOA%20human%20health%20toxicity%20assessment.txt)
- Species-of-origin limitation named by the IVIVE authors themselves: human cells are required because
  of "the vast inter-species differences in PFAS clearance which would limit the utility of the data
  from non-human cells, and the fact that existing models have not been confirmed with extremely long
  half-life compounds" — [Lin 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11585971/)

### Inferences
- The uptake-ratio threshold of 2-fold is a *detection* threshold, not a biological one. For a compound
  whose passive flux dominates (long-chain PFAS, high Papp), a real transporter contribution can fall
  below 2-fold. "Not a substrate" in Ryu 2024 and Argoul 2026 should be read as "not detectable above
  passive flux in this system", which also explains why the long-chain negatives conflict with
  Louisse 2023's control-subtracted Michaelis-Menten fits.
- Protein-free buffer in essentially all transfectant assays means the nominal concentration is also
  the free concentration, whereas in vivo >90% of PFOA is albumin-bound (Weaver 2010 cites Han 2003 for
  >90%). Km values are therefore free-concentration Km values and should be compared to *unbound*
  plasma concentrations, which widens the Km-to-exposure gap in the section above by roughly another
  order of magnitude.

### Gaps
- No study located measures PFAS transport in human primary proximal tubule cells or in human kidney
  membrane vesicles at the level of an individual transporter, so there is no bridge between the
  transfectant Km values and a physiologically scaled abundance.
- Relative abundance (REF/RAF) of each transporter in human kidney has not been measured for any of
  these transporters in the PFAS context; Worley & Fisher had to fit it.

## In vitro to in vivo extrapolation: attempts and performance

### Takeaway
Three IVIVE lines exist. The transporter-Km-based PBPK route (Worley & Fisher 2015) reproduces rat
data but only after fitting activity factors that differ by ~4–5 orders of magnitude between sexes,
so it is a calibration rather than a prediction. The cell-model route (Lin 2024; Sakolish 2026) gets
human absolute renal clearance within about 10-fold with Transwell RPTEC models, and correctly ranks
28 PFAS into day/month/year half-life classes. The pure transporter-efficiency route (Louisse 2023)
failed: OAT4 efficiency did not correlate with human half-life.

### Cited Findings
- Worley & Fisher took Km directly from the in vitro literature — Km_baso 27.20 µg/mL (= 65.7 µM) and
  Km_apical 52.3 µg/mL (= 126.3 µM, from Weaver 2010) — and Vmax_basoC 0.04 and Vmax_apicalC
  0.947 mg/h/kg BW^0.75 — [Worley 2015, Table 3](https://pmc.ncbi.nlm.nih.gov/articles/PMC4662604/)
- The fitted scaling factors carry the sex difference, not the in vitro kinetics: RAFapi was fitted to
  **35.0 in males and 0.001356 in females** (a ~25,800-fold ratio) and RAFbaso to **4.07 vs 0.01356**
  (300-fold), against a starting value of 0.01356 for both sexes taken from Yamada 2007; the free
  fraction was also fitted, from 0.006 to 0.09 — [Worley 2015, Tables 3 and 4](https://pmc.ncbi.nlm.nih.gov/articles/PMC4662604/)
- Model fit after calibration (RMSE, male/female): serum at 0.1 mg/kg 0.06/0.17 and at 1 mg/kg oral
  0.89/0.78, degrading to 9.00/18.88 at 25 mg/kg; urine RMSE was consistently worse in females
  (15.99–20.86) than males (4.48–6.75) — [Worley 2015, Table 5](https://pmc.ncbi.nlm.nih.gov/articles/PMC4662604/)
- ⚠ Attribution discrepancy to flag: Worley & Fisher label Km_baso as "Km of basolateral transporters
  (Oat1 and Oat3)" sourced from "Nakagawa et al., 2007", but 27.20 µg/mL ÷ 414.07 g/mol = 65.7 µM,
  which is exactly Weaver 2010's rat **Oat3-only** PFOA Km, not an average of Oat1 (43.2 µM) and Oat3
  (65.7 µM), which would be 54.5 µM = 22.6 µg/mL. Likewise Km_apical 52.3 µg/mL = 126.3 µM is
  Weaver 2010's Oatp1a1 value, correctly attributed.
- Cell-model IVIVE performance: Transwell RPTEC predicted absolute human renal clearance "within about
  10-fold"; 96-well 2D systematically under-predicted (health-protective); a prior published approach
  "severely overpredicted renal clearance, which is not health protective and could lead to an
  underestimation of the body burden" — [Lin 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11585971/)
- Lin 2024's own framing of the gain: existing read-across approaches "has only been able to categorize
  PFAS into 4 bins based on half-life (Bin 1: <12 hour; Bin 2: <1 week; Bin 3: <2 months; Bin 4:
  >2 months), rather than providing a continuum of quantitative predictions. Thus, even though our in
  vitro-in silico models have errors up to 10-fold, they still represent an improvement over existing
  approaches for PFAS" — [Lin 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11585971/)
- Sakolish 2026 extended this to 28 PFAS using PFOA as index chemical (human half-life 3.14 y from
  Chiu et al. 2022), predicting relative renal clearance factors spanning six orders of magnitude:
  PFBS 2000 and PFPeA/PFBA 500 (days) at one end, PFOA 1 (index, years), through PFOS 0.1, PFDA 0.04
  and PFUnDA 0.002 (years) at the other — [Sakolish 2026, Table 2](https://pmc.ncbi.nlm.nih.gov/articles/PMC12951621/)
- Where that validation study disagreed with itself: the model-development and validation studies gave
  materially different relative clearance factors for the same compounds (PFBS 2000 vs 20; PFHxA 200
  vs 6; PFBA 500 vs 300), and "the absolute results from the validation study shows a greater degree of
  underprediction as compared to the published data – about 100-fold rather than 10-fold" —
  [Sakolish 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC12951621/)
- Sakolish 2026's own benchmark for acceptability: "Although absolute renal clearance values for such
  compounds were slightly underpredicted in our model by on average about 3-fold, they are no more
  uncertain than allometric scaling of drugs from animal studies, which have been found to have
  geometric fold errors of 2- to 7-fold" — [Sakolish 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC12951621/)
- The negative result for pure transporter-efficiency IVIVE: comparing OAT4 transporter efficiencies
  (PFHpA 75, PFOA 96, PFHxS 79, PFOS 46 µL/min/mg protein) against reported human half-lives
  (0.17, 1.8–3.8, 2.9–8.5 and 1.8–5.4 y) "indicated that no direct correlation between these two
  parameters exists", although within a head-group class the efficiencies "correctly predicted shorter
  half-lives for PFHpA compared to PFOA and for PFHxS compared to PFOS" —
  [Louisse 2023, Discussion and Table 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC9968691/)
- A positive in vitro-to-in vivo correlation does exist for the rat: the log of Yang 2009's Oatp1a1
  Ki,app values "exhibited … a positive linear relationship to the log values of the total clearance of
  perfluorocarboxylates in male rats. This in vitro-to-in vivo correlation strongly supports a tubular
  reabsorptive role of Oatp1a1" — [Yang 2009, Abstract](https://doi.org/10.1016/j.toxlet.2009.07.011);
  ATSDR reports the strength as r² = 0.98 —
  [ATSDR 2021, Section 3](papers/ATSDR%202021%20Toxicological%20Profile%20Perfluoroalkyls.txt)
- Barrier identified by EFSA/Louisse for human PBPK: the EFSA CONTAM assessment had to assume PFNA
  behaves like PFOA and PFHxS like PFOS because congener-specific models do not exist; "information
  generated using in vitro methods on transporter kinetics … as well as plasma protein binding, are
  essential to develop such models" — [Louisse 2023, Discussion](https://pmc.ncbi.nlm.nih.gov/articles/PMC9968691/)
- Regulatory assessment of the Worley & Fisher approach: parameters "for apical and basolateral
  transport of PFOA were derived from in vitro estimates for OATP1a1 (apical) and OAT1 and OAT3
  (basolateral) (Nakagawa et al. 2008; Weaver et al. 2010; Yamada et al. 2007)" and fitting to male and
  female rat observations "resulted in lower values for activity of both transporters" in females —
  [ATSDR 2021, Section 3](papers/ATSDR%202021%20Toxicological%20Profile%20Perfluoroalkyls.txt). The
  human counterpart used OAT4 for the apical side — same source.

### Inferences
- The Worley & Fisher result is best read as a *falsification* of naive transporter-Km IVIVE for the
  rat sex difference: if in vitro Km and Vmax were sufficient, the male/female difference would emerge
  from the kinetics, not from a 25,800-fold fitted activity factor. Measured renal Oatp1a1 expression
  differences are at most 1–2 orders of magnitude (and undetectable protein in females per Gotoh 2002),
  which could plausibly cover a large part of that factor but not with the precision the model implies.
- The two IVIVE routes have complementary failure modes. Transporter-level IVIVE (Louisse) fails
  because it covers only one of several parallel processes (glomerular filtration of the unbound
  fraction, OAT-mediated secretion, apical reabsorption, enterohepatic recirculation, albumin binding).
  Whole-cell IVIVE (Lin/Sakolish) succeeds to ~10-fold precisely because it integrates them, but at the
  cost of not telling you which transporter is responsible.
- For the species/sex question the practical implication is that in vitro transporter kinetics identify
  the *mechanism* (apical Oatp1a1 reabsorption, androgen-regulated, chain-length-selective) but cannot
  currently supply the *magnitude*. Any quantitative species or sex scaling in the report should come
  from in vivo clearance and net-reabsorption data (e.g. OEHHA Table A6.4) with the transporter data
  cited as mechanistic support.

### Gaps
- No IVIVE attempt was located that predicts the *rat* sex difference forward from in vitro Oatp1a1
  kinetics plus measured male/female Oatp1a1 abundance. That is the experiment that would close the
  loop, and it does not appear to have been done.
- Chou & Lin (2019/2021) transporter-containing PBPK models, requested in the assignment, could not be
  located from this container; they are not represented here.
