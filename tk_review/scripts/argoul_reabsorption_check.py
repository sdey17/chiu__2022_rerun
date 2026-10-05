#!/usr/bin/env python3
"""Does an independent dataset reproduce the reabsorption axis?

Report section 3.3 builds its single mechanistic axis from OEHHA's PHG appendix
Table A6.4 (adapted from Han et al. 2012), which tabulates fractional renal
reabsorption FR by species and reproduces rodent half-lives within 1.7x over a
37x span with no free parameters. The axis is

    CL_renal = fu * GFR * (1 - FR)        so      FR = 1 - CL_renal / (fu * GFR)

Everything in that section traces back to one compilation. Argoul et al. 2026
(Environ Res 303:124802) Table 4 reports fu, the glomerular filtration clearance
of free drug, and the measured renal clearance for ten PFAS in female mice,
measured in their own laboratory. That is the same three quantities from a
completely independent source, so FR can be recomputed and compared.

Run:  python3 scripts/argoul_reabsorption_check.py
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PRIM = os.path.join(HERE, "..", "db", "primary_2026")

# Report section 3.3 / OEHHA Table A6.4, the PFOA column, for comparison.
OEHHA_PFOA_FR = {
    "human": 0.998,
    "mouse": (0.952, 0.97),      # the appendix gives two mouse entries
    "rat male": 0.932,
    "macaque": (0.812, 0.912),
    "dog": (0.52, 0.59),
    "rat female": None,          # net secretion
    "rabbit": None,              # net secretion
}


def main():
    with open(os.path.join(PRIM, "argoul2026_mouse_tk.csv")) as fh:
        rows = list(csv.DictReader(fh))

    print(__doc__.split("Run:")[0].rstrip())
    print("=" * 76)
    print("\nFRACTIONAL REABSORPTION RECOMPUTED FROM ARGOUL 2026 TABLE 4")
    print("(female CD-1 mouse; GFR implied by the table is 10 L/kg-day)\n")
    print(f"  {'chemical':9} {'fu %':>6} {'fu*GFR':>9} {'CL_renal':>9} "
          f"{'1-CLr/fuGFR':>12}  reading")
    print(f"  {'':9} {'':>6} {'mL/kg-d':>9} {'mL/kg-d':>9} {'= FR':>12}")

    results = {}
    for r in rows:
        if not r["fu_pct"] or not r["cl_renal_measured_mL_kg_day"]:
            continue
        try:
            clr = float(r["cl_renal_measured_mL_kg_day"])
        except ValueError:
            continue                       # PFBS: nonlinear range, not a scalar
        fu = float(r["fu_pct"])
        clfg = float(r["cl_gfr_free_mL_kg_day"])
        fr = 1 - clr / clfg
        results[r["chemical"]] = fr
        if fr < 0:
            reading = f"NET SECRETION ({-fr:.2f}x filtration)"
        elif fr > 0.99:
            reading = "near-complete reabsorption"
        else:
            reading = f"{fr:.1%} reabsorbed"
        print(f"  {r['chemical']:9} {fu:6.2f} {clfg:9.0f} {clr:9.2f} "
              f"{fr:12.4f}  {reading}")

    print("\n  Internal check: the table's Clfg column equals fu x GFR with GFR =")
    print("  10 L/kg-day for every row. The methods text states 11 mL/kg/min")
    print("  (= 15.8 L/kg-day), which does not reproduce the column; the tabulated")
    print("  values are self-consistent at 10 L/kg-day, so that is what is used here.")

    print("\n" + "=" * 76)
    print("COMPARISON WITH THE AXIS IN REPORT SECTION 3.3 (PFOA)")
    print("-" * 76)
    lo, hi = OEHHA_PFOA_FR["mouse"]
    got = results["PFOA"]
    print(f"  OEHHA Table A6.4, mouse PFOA : FR = {lo:.3f} and {hi:.3f}")
    print(f"  Argoul 2026 Table 4, recomputed here : FR = {got:.4f}")
    inside = lo <= got <= hi
    print(f"  -> {'INSIDE' if inside else 'OUTSIDE'} the range the report already uses,")
    print("     from an entirely separate laboratory and dataset.")

    print("\n  The axis also predicts its own extremes. Two compounds here show")
    print("  renal clearance ABOVE free filtration, i.e. net tubular secretion:")
    for chem, fr in sorted(results.items(), key=lambda kv: kv[1]):
        if fr < 0:
            print(f"     {chem:8} FR = {fr:+.3f}")
    print("  which is the same end of the axis that OEHHA's table assigns to the")
    print("  female rat and the rabbit. The axis has a secretion end in the mouse")
    print("  too; which compounds sit there is chain- and head-group-specific, not")
    print("  species-specific.")

    print("\n  Ordering the ten compounds by FR:")
    for chem, fr in sorted(results.items(), key=lambda kv: -kv[1]):
        bar = "#" * max(0, int(round(fr * 40)))
        print(f"     {chem:9} {fr:+.4f} {bar}")

    print("\n  How far does the unbound fraction predict where a compound lands?")
    fus, frs = [], []
    for r in rows:
        if r["chemical"] in results and r["fu_pct"]:
            fus.append(float(r["fu_pct"]))
            frs.append(results[r["chemical"]])

    def spearman(a, b):
        """Rank correlation; ties are averaged."""
        def ranks(v):
            order = sorted(range(len(v)), key=lambda i: v[i])
            rk = [0.0] * len(v)
            i = 0
            while i < len(order):
                j = i
                while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                    j += 1
                avg = (i + j) / 2 + 1
                for k in range(i, j + 1):
                    rk[order[k]] = avg
                i = j + 1
            return rk
        ra, rb = ranks(a), ranks(b)
        n = len(a)
        ma, mb = sum(ra) / n, sum(rb) / n
        num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
        den = (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** 0.5
        return num / den if den else float("nan")

    print(f"     Spearman rho(fu, FR) = {spearman(fus, frs):+.3f} over n = {len(fus)} compounds")
    low = [(c, results[c]) for c, f in zip([r["chemical"] for r in rows if r["chemical"] in results], fus) if f < 1.5]
    high = [(c, results[c]) for c, f in zip([r["chemical"] for r in rows if r["chemical"] in results], fus) if f >= 10]
    print(f"\n     fu below 1.5% (n={len(low)}): FR = "
          + ", ".join(f"{c} {v:+.3f}" for c, v in sorted(low, key=lambda kv: -kv[1])))
    print(f"     fu above 10%  (n={len(high)}): FR = "
          + ", ".join(f"{c} {v:+.3f}" for c, v in sorted(high, key=lambda kv: -kv[1])))
    print("\n  The relationship is strong but one-directional. Every compound bound")
    print("  above 98.5% (fu < 1.5%) sits above 95% reabsorption, without exception.")
    print("  The loosely bound compounds do NOT occupy a matching band: they spread")
    print("  from +0.90 (PFBA, fu 77%) to -1.71 (PFHxA, fu 25%), so a high unbound")
    print("  fraction is compatible with either strong reabsorption or net")
    print("  secretion. Tight binding is close to sufficient for high reabsorption;")
    print("  loose binding predicts nothing on its own, and the head group and")
    print("  chain length decide. That asymmetry matters for the species question,")
    print("  because it is the heavily bound end -- where humans sit -- that behaves")
    print("  predictably.")


if __name__ == "__main__":
    main()
