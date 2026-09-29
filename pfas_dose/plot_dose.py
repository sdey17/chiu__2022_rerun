"""
Clearance vs dose, one panel per study.

Small multiples rather than one scatter coloured by study: the valid
comparison is within a study (comparing doses across labs would confound
dose with laboratory), and one series per panel means identity never
depends on colour.

Usage:  python plot_dose.py PFOA_Male_rat_2cmpt.nc   -> PFOA_Male_rat_2cmpt_dose.png
"""
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from dose_analysis import load_dataset_clearance

SERIES = "#2a78d6"     # validated categorical slot 1
INK = "#0b0b0b"
INK_SOFT = "#52514e"
GRID = "#e3e2de"
MARKERS = {"gavage": "o", "iv": "^"}


def plot(path, out=None):
    # name the picture after the trace it came from
    out = out or path.replace(".nc", "_dose.png")
    df, _ = load_dataset_clearance(path)
    studies = sorted(df.study.unique())
    ncol = min(3, len(studies))
    nrow = int(np.ceil(len(studies) / ncol))
    fig, axes = plt.subplots(nrow, ncol, figsize=(3.6 * ncol, 3.2 * nrow),
                             sharex=True, sharey=True)
    axes = np.atleast_1d(axes).ravel()

    for ax, study in zip(axes, studies):
        g = df[df.study == study].sort_values("dose")
        for route, gg in g.groupby("route"):
            ax.errorbar(gg.dose, gg.clc_median,
                        yerr=[gg.clc_median - gg.clc_lo, gg.clc_hi - gg.clc_median],
                        fmt=MARKERS.get(route, "s"), ms=8, lw=2, capsize=0,
                        color=SERIES, mec="white", mew=1.5,
                        ecolor=SERIES, elinewidth=2, alpha=0.95)
            # label the route directly, so it is never colour-alone
            top = gg.loc[gg.dose.idxmax()]
            ax.annotate(route, (top.dose, top.clc_hi), textcoords="offset points",
                        xytext=(4, 4), fontsize=8, color=INK_SOFT)
        ax.set(xscale="log", yscale="log")
        ax.set_title(f"study {study}", fontsize=10, color=INK, loc="left")
        ax.grid(True, which="major", color=GRID, lw=0.8)
        ax.set_axisbelow(True)
        for side in ["top", "right"]:
            ax.spines[side].set_visible(False)
        for side in ["left", "bottom"]:
            ax.spines[side].set_color(GRID)
        ax.tick_params(colors=INK_SOFT, labelsize=8)

    for ax in axes[len(studies):]:
        ax.set_visible(False)

    fig.supxlabel("dose (mg/kg)", fontsize=10, color=INK_SOFT)
    fig.supylabel("clearance (L/kg per day)", fontsize=10, color=INK_SOFT)
    fig.suptitle("Flat within a panel means clearance does not depend on dose",
                 fontsize=11, color=INK, x=0.01, ha="left")
    fig.tight_layout()
    fig.savefig(out, dpi=150, facecolor="#fcfcfb")
    print(f"wrote {out}")


if __name__ == "__main__":
    plot(sys.argv[1])
