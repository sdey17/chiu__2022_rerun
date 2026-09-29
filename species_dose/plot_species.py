"""
Half-life against the serum concentration actually measured, one panel
per chemical.

If low dose were the reason humans have long half-lives, every panel
would show one downward line that humans simply sit at the end of.
Points are labelled with species directly, so identity never depends on
colour; humans are also set apart by hue because they are the comparison
the hypothesis is about.

Usage:  python plot_species.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from test_hypothesis import load

ANIMAL = "#2a78d6"     # validated categorical slot 1
HUMAN = "#eb6834"      # slot 2; pair passes all-pairs CVD and contrast
INK, INK_SOFT, GRID = "#0b0b0b", "#52514e", "#e3e2de"
INITIAL = {"rat": "R", "mouse": "M", "primate": "P", "human": "HUMAN"}


def plot(out="halflife_vs_exposure.png"):
    df = load()
    chems = [c for c in ["PFOA", "PFOS", "PFNA", "PFHxS", "PFHxA", "PFBA", "PFBS", "PFDA"]
             if c in set(df.PFAS)]
    ncol = 4
    nrow = int(np.ceil(len(chems) / ncol))
    fig, axes = plt.subplots(nrow, ncol, figsize=(3.3 * ncol, 3.1 * nrow),
                             sharex=True, sharey=True)
    axes = np.atleast_1d(axes).ravel()

    for ax, chem in zip(axes, chems):
        g = df[df.PFAS == chem]
        for _, r in g.iterrows():
            human = r.species == "human"
            ax.plot(r.serum_median, r.halft_mean, "o", ms=9,
                    color=HUMAN if human else ANIMAL, mec="white", mew=1.5, zorder=3)
            ax.annotate(f"{INITIAL[r.species]}{'' if human else r.sex[0]}",
                        (r.serum_median, r.halft_mean), textcoords="offset points",
                        xytext=(7, -3), fontsize=8,
                        color=HUMAN if human else INK_SOFT,
                        weight="bold" if human else "normal")
        ax.set(xscale="log", yscale="log")
        ax.set_title(chem, fontsize=10, color=INK, loc="left")
        ax.grid(True, which="major", color=GRID, lw=0.8)
        ax.set_axisbelow(True)
        for side in ["top", "right"]:
            ax.spines[side].set_visible(False)
        for side in ["left", "bottom"]:
            ax.spines[side].set_color(GRID)
        ax.tick_params(colors=INK_SOFT, labelsize=8)

    for ax in axes[len(chems):]:
        ax.set_visible(False)

    fig.supxlabel("serum concentration actually measured (ug/L)", fontsize=10, color=INK_SOFT)
    fig.supylabel("half-life (days)", fontsize=10, color=INK_SOFT)
    fig.suptitle("R = rat, M = mouse, P = primate (M/F = sex); humans in orange.\n"
                 "Animals span a wide exposure range at nearly constant half-life.",
                 fontsize=10.5, color=INK, x=0.01, ha="left")
    fig.tight_layout()
    fig.savefig(out, dpi=150, facecolor="#fcfcfb")
    print(f"wrote {out}")


if __name__ == "__main__":
    plot()
