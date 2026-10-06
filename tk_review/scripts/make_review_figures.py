"""
Figures 2 and 3 for report/PFAS_TK_review.pdf.

Each panel carries an argument the prose otherwise has to assert. Palette and
mark specs follow the project's existing figure style, validated for
colour-vision deficiency: worst adjacent pair deltaE 9.2 (deutan), normal-vision
floor 27.1. The aqua fails the 3:1 contrast check against the surface, so every
series is directly labelled as well as coloured -- identity is never carried by
colour alone.

Run:  python3 scripts/make_review_figures.py
"""

import csv
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGS = os.path.join(HERE, "figures")

BLUE, ORANGE, AQUA, PURPLE = "#2a78d6", "#eb6834", "#1baf7a", "#7b5ea7"
SURFACE, INK, INK2, MUTED = "#fcfcfb", "#0b0b0b", "#52514e", "#8a8984"
GRID, RULE = "#e6e5e1", "#d8d7d3"

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE, "font.family": "DejaVu Sans", "font.size": 9,
    "axes.edgecolor": RULE, "axes.linewidth": 0.8, "axes.labelcolor": INK2,
    "text.color": INK, "xtick.color": INK2, "ytick.color": INK2,
    "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False, "figure.dpi": 150,
})


def rows(p):
    return list(csv.DictReader(open(os.path.join(HERE, p), newline="")))


# ---------------------------------------------------------------- figure 2
def figure2():
    """A: both ratios in the SAME direction, so the asymmetry is not an
    artefact of how each was written. B: the species gap split into its two
    factors."""
    d = [r for r in rows("db/sex_decomposition.csv")
         if r["vd_ratio_F_over_M"] and r["clearance_ratio_F_over_M"]]
    sp_colour = {"rat": BLUE, "mouse": ORANGE, "primate": PURPLE}

    fig, (axA, axB) = plt.subplots(
        1, 2, figsize=(11.6, 4.5), gridspec_kw=dict(width_ratios=[1.45, 1]))

    # ---- panel A: strip plot of the two ratio distributions ----
    for i, (key, lab) in enumerate([("vd_ratio_F_over_M", "volume of distribution"),
                                    ("clearance_ratio_F_over_M", "clearance")]):
        vals = [float(r[key]) for r in d]
        cols = [sp_colour[r["species"]] for r in d]
        jitter = np.linspace(-0.16, 0.16, len(vals))
        axA.scatter(vals, [i] * len(vals) + jitter, s=60, c=cols, zorder=4,
                    edgecolor=SURFACE, linewidth=1.4)
        lo, hi = min(vals), max(vals)
        axA.plot([lo, hi], [i - 0.30, i - 0.30], color=MUTED, lw=1.4, zorder=2)
        axA.text(math.sqrt(lo * hi), i - 0.47,
                 f"spans {hi/lo:.0f}×" if hi / lo >= 10
                 else f"spans {hi/lo:.1f}×",
                 ha="center", va="top", fontsize=9, color=INK,
                 fontweight="bold")

    axA.axvline(1.0, color=MUTED, lw=1.0, ls=(0, (4, 3)), zorder=1)
    axA.text(1.0, -0.70, "1.0 = no sex difference", fontsize=7.5,
             color=MUTED, ha="center", va="bottom")
    axA.set_xscale("log")
    axA.set_yticks([0, 1])
    axA.set_yticklabels(["volume of\ndistribution", "clearance"], fontsize=9.5)
    axA.set_ylim(-0.75, 1.6)
    axA.set_xlabel("female / male ratio   (log scale, both measures same direction)")
    axA.grid(axis="x", color=GRID, lw=0.8, zorder=0)
    axA.set_axisbelow(True)
    axA.set_title("A · Only one of the two terms varies with sex",
                  loc="left", fontsize=10.5, color=INK, fontweight="bold",
                  pad=10)
    for sp, col in sp_colour.items():
        axA.scatter([], [], s=60, c=col, label=sp, edgecolor=SURFACE,
                    linewidth=1.4)
    axA.legend(loc="upper left", bbox_to_anchor=(0.0, 1.0), fontsize=8,
               ncol=3, handletextpad=0.3, columnspacing=1.1)

    # ---- panel B: the 333x gap decomposed ----
    total, escape, gfr = 333.0, 50.0, 6.5
    le, lg = math.log10(escape), math.log10(gfr)
    axB.barh([0], [le], color=BLUE, height=0.42, zorder=3)
    axB.barh([0], [lg], left=[le + 0.012], color=ORANGE, height=0.42, zorder=3)
    axB.text(le / 2, 0, f"escape fraction\n{escape:.0f}×",
             ha="center", va="center", color="white", fontsize=9,
             fontweight="bold", zorder=5)
    axB.text(le + lg / 2 + 0.012, 0, f"GFR\n{gfr:.1f}×", ha="center",
             va="center", color="white", fontsize=9, fontweight="bold",
             zorder=5)
    axB.text(le / 2, 0.30, f"{100*le/(le+lg):.0f}% of the gap", ha="center",
             fontsize=8.5, color=INK2)
    axB.text(le + lg / 2, 0.30, f"{100*lg/(le+lg):.0f}%", ha="center",
             fontsize=8.5, color=INK2)
    axB.set_xlim(0, (le + lg) * 1.06)
    axB.set_ylim(-0.75, 0.75)
    axB.set_yticks([])
    axB.set_xlabel("log$_{10}$ of the fold-contribution")
    axB.set_title("B · The axis is two factors, not one",
                  loc="left", fontsize=10.5, color=INK, fontweight="bold",
                  pad=10)
    axB.text(0, -0.52,
             f"male mouse → human renal clearance gap: {total:.0f}× total.\n"
             "A third of it is filtration rate, which no transporter\n"
             "mechanism explains.",
             fontsize=8.3, color=INK2, va="top")
    axB.grid(axis="x", color=GRID, lw=0.8, zorder=0)
    axB.set_axisbelow(True)

    fig.suptitle("Where the sex and species differences actually sit",
                 x=0.012, y=0.985, ha="left", fontsize=11.5, color=INK,
                 fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.945])
    out = os.path.join(FIGS, "fig02_sex_and_species_decomposition.png")
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)

    vd = [float(r["vd_ratio_F_over_M"]) for r in d]
    cl = [float(r["clearance_ratio_F_over_M"]) for r in d]
    print(f"  fig02: {len(d)} pairs; Vd spans {max(vd)/min(vd):.1f}x, "
          f"CL spans {max(cl)/min(cl):.0f}x")
    return max(vd) / min(vd), max(cl) / min(cl), len(d)


# ---------------------------------------------------------------- figure 3
def figure3():
    """A: the structure-activity endpoint by compound. B: how far the whole
    endpoint moves on one contested input."""
    q = [r for r in rows("db/qsar/qsar_endpoint_table.csv")
         if r["log10R_gfr_argoul"]]
    q.sort(key=lambda r: float(r["log10R_gfr_argoul"]))

    head_colour = {"carboxylate": BLUE, "sulfonate": ORANGE,
                   "ether-carboxylate": AQUA}
    fig, (axA, axB) = plt.subplots(
        1, 2, figsize=(11.6, 4.6), gridspec_kw=dict(width_ratios=[1.5, 1]))

    y = np.arange(len(q))
    vals = [float(r["log10R_gfr_argoul"]) for r in q]
    cols = [head_colour[r["head_group"]] for r in q]
    axA.hlines(y, 0, vals, color=GRID, lw=1.6, zorder=2)
    axA.scatter(vals, y, s=85, c=cols, zorder=4, edgecolor=SURFACE,
                linewidth=1.6)
    axA.axvline(0, color=INK, lw=1.0, zorder=3)
    # Compound identity goes on the axis rather than into floating labels, so
    # nothing can collide as the values move.
    axA.set_yticks(y)
    axA.set_yticklabels([f"{r['chemical']}   C{r['n_fluorinated_c']}"
                         for r in q], fontsize=8.8)
    axA.tick_params(axis="y", length=0)
    axA.set_ylim(-0.95, len(q) - 0.1)
    axA.set_xlim(-3.15, 1.5)
    axA.set_xlabel(r"log$_{10}$ R   (R = CL$_{renal}$ / f$_u \cdot$ GFR)")
    axA.grid(axis="x", color=GRID, lw=0.8, zorder=0)
    axA.set_axisbelow(True)
    axA.text(-0.08, -0.86, "← reabsorbed", fontsize=8, color=INK2,
             ha="right")
    axA.text(0.08, -0.86, "secreted →", fontsize=8, color=INK2)
    axA.set_title("A · Chain length alone does not order the endpoint",
                  loc="left", fontsize=10.5, color=INK, fontweight="bold",
                  pad=24)
    for h, col in head_colour.items():
        axA.scatter([], [], s=85, c=col, label=h.replace("-", " "),
                    edgecolor=SURFACE, linewidth=1.6)
    axA.legend(loc="lower left", bbox_to_anchor=(0.0, 1.005), fontsize=8.2,
               ncol=3, handletextpad=0.3, columnspacing=1.2)
    # bracket the three five-carbon compounds: same chain length, 1.4 apart
    c5 = [i for i, r in enumerate(q) if r["n_fluorinated_c"] == "5"]
    xb = 1.05
    axA.plot([xb, xb], [min(c5), max(c5)], color=MUTED, lw=1.1, zorder=3)
    for i in c5:
        axA.plot([vals[i] + 0.07, xb], [i, i], color=GRID, lw=0.9, zorder=1)
        axA.plot([xb - 0.05, xb], [i, i], color=MUTED, lw=1.1, zorder=3)
    axA.text(xb + 0.1, (min(c5) + max(c5)) / 2,
             "all C5,\n1.4 log units\napart", fontsize=7.8, color=INK2,
             va="center", ha="left")

    # ---- panel B: the fu sensitivity ----
    fus = [(0.10, "read as\n'~90% bound'", -3.93, 354),
           (0.02, "assumed\n(Han 2012)", -3.23, 71),
           (0.00061, "measured\n(Fischer)", -1.72, 2.2)]
    mouse = -1.384
    xs = np.arange(len(fus))
    axB.axhline(mouse, color=ORANGE, lw=2.0, zorder=3)
    axB.text(2.42, mouse + 0.10, "female mouse PFOA", fontsize=8.4,
             color=ORANGE, ha="right", fontweight="bold")
    for x, (fu, lab, lr, gap) in zip(xs, fus):
        axB.vlines(x, lr, mouse, color=GRID, lw=2.2, zorder=2)
        axB.scatter([x], [lr], s=95, c=BLUE, zorder=5, edgecolor=SURFACE,
                    linewidth=1.6)
        axB.text(x, lr - 0.17, f"{gap:g}×", ha="center", va="top",
                 fontsize=9.5, color=INK, fontweight="bold")
        axB.text(x, lr - 0.46, "gap to mouse", ha="center", va="top",
                 fontsize=7.4, color=MUTED)
    axB.set_xticks(xs)
    axB.set_xticklabels([f"f$_u$ = {f:g}\n{l}" for f, l, _, _ in fus],
                        fontsize=8.2)
    axB.set_xlim(-0.6, 2.6)
    axB.set_ylim(-4.6, -0.95)
    axB.set_ylabel("log$_{10}$ R, human PFOA")
    axB.grid(axis="y", color=GRID, lw=0.8, zorder=0)
    axB.set_axisbelow(True)
    axB.set_title("B · One contested input moves the species gap 160-fold",
                  loc="left", fontsize=10.5, color=INK, fontweight="bold",
                  pad=10)

    fig.suptitle("The structure-activity endpoint, and how much it rests "
                 "on one number",
                 x=0.012, y=0.985, ha="left", fontsize=11.5, color=INK,
                 fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.945])
    out = os.path.join(FIGS, "fig03_structure_activity_and_sensitivity.png")
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"  fig03: {len(q)} compounds; span "
          f"{max(vals)-min(vals):.2f} log units; fu sensitivity 2.21 log units")


if __name__ == "__main__":
    os.makedirs(FIGS, exist_ok=True)
    figure2()
    figure3()
    print("  wrote figures/fig02_*.png and figures/fig03_*.png")
