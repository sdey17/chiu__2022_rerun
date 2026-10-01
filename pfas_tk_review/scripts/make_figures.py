#!/usr/bin/env python3
"""Figures for the rat-versus-mouse half-life analysis.

Four questions, four figures:
  1. how large is the mouse/rat half-life gap, and where does it sit?
  2. does the gap come from distribution (Vd) or from clearance (CL)?
  3. is the rat sex difference present in the mouse?
  4. does the gap survive matching on serum concentration?
"""
import csv
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

HERE = Path(__file__).resolve().parent
DB = HERE.parent / "db"
FIG = HERE.parent / "figures"
FIG.mkdir(parents=True, exist_ok=True)

# Validated categorical slots 1 and 2 (light mode) from the reference palette.
BLUE, ORANGE = "#2a78d6", "#eb6834"
SURFACE = "#fcfcfb"
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#8a8984"

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
    "font.size": 10, "axes.titlesize": 12, "axes.labelsize": 10,
    "text.color": INK, "axes.labelcolor": INK2, "axes.edgecolor": MUTED,
    "xtick.color": INK2, "ytick.color": INK2,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": "#e6e5e1", "grid.linewidth": 0.8,
    "legend.frameon": False, "lines.linewidth": 2.0,
})


def recessive(ax, axis="x"):
    ax.set_axisbelow(True)
    ax.grid(axis=axis, color="#e6e5e1", linewidth=0.8)
    ax.grid(axis="y" if axis == "x" else "x", visible=False)


def titled(ax, title, subtitle):
    """Place a bold title with its subtitle underneath, clear of the axes."""
    ax.set_title(title, loc="left", color=INK, fontweight="bold", pad=34)
    ax.annotate(subtitle, (0, 1.012), xycoords="axes fraction",
                fontsize=9, color=INK2, va="bottom")


def legend_below(ax, ncol=2):
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.145),
              ncol=ncol, fontsize=9)


def load(name):
    return list(csv.DictReader((DB / name).open()))


mr = load("mouse_rat_decomposition.csv")
sx = load("sex_decomposition.csv")
# Longest half-life first, so the eye lands on the big discrepancies.
order = sorted({r["PFAS"] for r in mr},
               key=lambda c: -max(float(r["halflife_mouse_d"]) for r in mr if r["PFAS"] == c))


# ---- Figure 1: the mouse/rat half-life ratio -------------------------------
fig, ax = plt.subplots(figsize=(8.2, 4.6))
h = 0.36
for i, (sex, col) in enumerate((("Male", BLUE), ("Female", ORANGE))):
    ys, vs = [], []
    for j, c in enumerate(order):
        rec = next((r for r in mr if r["PFAS"] == c and r["sex"] == sex), None)
        if rec:
            ys.append(j + (h / 2 if i == 0 else -h / 2))
            vs.append(float(rec["halflife_ratio_mouse_over_rat"]))
    bars = ax.barh(ys, vs, height=h, color=col, label=sex, zorder=3)
    for y, v in zip(ys, vs):
        ax.annotate(f"{v:.1f}x", (v, y), xytext=(5 if v >= 1 else -5, 0),
                    textcoords="offset points", va="center",
                    ha="left" if v >= 1 else "right",
                    fontsize=8.5, color=INK2, zorder=4)
ax.axvline(1.0, color=INK, linewidth=1.4, zorder=2)
ax.annotate("equal half-life", (1.0, 0.012), xycoords=("data", "axes fraction"),
            xytext=(6, 0), textcoords="offset points", fontsize=8.5, color=INK2)
ax.set_xscale("log")
ax.set_yticks(range(len(order)))
ax.set_yticklabels(order)
ax.set_xlim(0.4, 60)
ax.set_xticks([0.5, 1, 2, 5, 10, 20, 50])
ax.set_xticklabels(["0.5x", "1x", "2x", "5x", "10x", "20x", "50x"])
ax.set_xlabel("mouse half-life ÷ rat half-life  (log scale)")
titled(ax, "The mouse–rat half-life gap is a female-rat phenomenon",
       "Male mouse and male rat agree within ~4x for every chemical.\n"
       "Female rats clear PFOA, PFNA and PFHxS 15–31x faster than female mice.")
recessive(ax)
legend_below(ax)
fig.tight_layout()
fig.savefig(FIG / "fig1_mouse_rat_halflife_ratio.png", dpi=200)
plt.close(fig)


# ---- Figure 2: Vd or CL? ---------------------------------------------------
def pearson(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    sxx = sum((a - mx) ** 2 for a in xs)
    syy = sum((b - my) ** 2 for b in ys)
    return sxy / math.sqrt(sxx * syy) if sxx and syy else float("nan")


fig, axes = plt.subplots(1, 2, figsize=(9.4, 4.4), sharey=True)
lt = [math.log(float(r["halflife_ratio_mouse_over_rat"])) for r in mr]
panels = [
    ("ln( Vd mouse / Vd rat )", [math.log(float(r["vd_ratio"])) for r in mr],
     "Distribution volume"),
    ("ln( CL rat / CL mouse )", [-math.log(float(r["clearance_ratio"])) for r in mr],
     "Clearance"),
]
for ax, (xlab, xs, label) in zip(axes, panels):
    for r, x, y in zip(mr, xs, lt):
        col = BLUE if r["sex"] == "Male" else ORANGE
        ax.scatter(x, y, s=70, color=col, edgecolor=SURFACE, linewidth=2, zorder=3)
    lo = min(min(xs), min(lt)) - 0.4
    hi = max(max(xs), max(lt)) + 0.4
    ax.plot([lo, hi], [lo, hi], color=MUTED, linewidth=1.2, linestyle=(0, (4, 3)), zorder=2)
    ax.annotate("y = x", (hi, hi), xytext=(-26, 6), textcoords="offset points",
                fontsize=8.5, color=MUTED)
    ax.axhline(0, color="#d8d7d3", linewidth=1, zorder=1)
    ax.axvline(0, color="#d8d7d3", linewidth=1, zorder=1)
    ax.set_xlabel(xlab)
    ax.set_title(f"{label}   r = {pearson(xs, lt):+.2f}", loc="left",
                 color=INK, fontsize=11)
    ax.set_axisbelow(True)
axes[0].set_ylabel("ln( mouse half-life / rat half-life )")
fig.suptitle("The gap is a clearance difference, not a distribution difference",
             x=0.012, ha="left", fontweight="bold", color=INK, fontsize=12.5)
fig.text(0.012, 0.878,
         "Each point is one chemical × sex. Clearance tracks the half-life gap almost "
         "one-for-one; Vd barely moves.",
         fontsize=9, color=INK2, ha="left")
fig.legend(handles=[Line2D([], [], marker="o", linestyle="", markersize=8,
                           color=c, label=s) for s, c in
                    (("Male", BLUE), ("Female", ORANGE))],
           loc="lower right", bbox_to_anchor=(0.99, 0.02), fontsize=9, ncol=2)
fig.tight_layout(rect=(0, 0.05, 1, 0.855))
fig.savefig(FIG / "fig2_vd_vs_clearance.png", dpi=200)
plt.close(fig)


# ---- Figure 3: the sex effect, rat vs mouse -------------------------------
fig, ax = plt.subplots(figsize=(8.2, 4.6))
sorder = [c for c in order if any(r["PFAS"] == c and r["species"] == "mouse" for r in sx)]
for i, (sp, col) in enumerate((("rat", BLUE), ("mouse", ORANGE))):
    ys, vs = [], []
    for j, c in enumerate(sorder):
        rec = next((r for r in sx if r["PFAS"] == c and r["species"] == sp), None)
        if rec:
            ys.append(j + (h / 2 if i == 0 else -h / 2))
            vs.append(float(rec["clearance_ratio_F_over_M"]))
    ax.barh(ys, vs, height=h, color=col, label=sp, zorder=3)
    for y, v in zip(ys, vs):
        ax.annotate(f"{v:.1f}x", (v, y), xytext=(5, 0), textcoords="offset points",
                    va="center", ha="left", fontsize=8.5, color=INK2, zorder=4)
ax.axvline(1.0, color=INK, linewidth=1.4, zorder=2)
ax.annotate("no sex difference", (1.0, 0.012), xycoords=("data", "axes fraction"),
            xytext=(6, 0), textcoords="offset points", fontsize=8.5, color=INK2)
ax.set_xscale("log")
ax.set_yticks(range(len(sorder)))
ax.set_yticklabels(sorder)
ax.set_xlim(0.3, 90)
ax.set_xticks([0.5, 1, 2, 5, 10, 20, 50])
ax.set_xticklabels(["0.5x", "1x", "2x", "5x", "10x", "20x", "50x"])
ax.set_xlabel("female clearance ÷ male clearance  (log scale)")
titled(ax, "Rats have a female-specific clearance pathway the mouse lacks",
       "Female rats clear PFOA 44x, PFNA 21x and PFHxS 20x faster than males.\n"
       "In mice the same ratios are 1.8x, 1.1x and 0.8x. PFOS escapes it in both.")
recessive(ax)
legend_below(ax)
fig.tight_layout()
fig.savefig(FIG / "fig3_sex_clearance_ratio.png", dpi=200)
plt.close(fig)


# ---- Figure 4: does matching on exposure close the gap? -------------------
fig, ax = plt.subplots(figsize=(7.6, 5.0))
ax.axvspan(0.5, 2.0, color="#eef2f8", zorder=1)
ax.annotate("serum concentrations\nmatched within 2x", (1.0, 0.94),
            xycoords=("data", "axes fraction"), fontsize=8.5, color=INK2,
            ha="center", va="top")
# Male labels go up-right, female labels down-left, so the two sexes of the
# same chemical never print on top of each other. Three pairs sit close enough
# that the default sides still collide, so those are placed explicitly.
UP, DOWN = ((9, 6), "left", "bottom"), ((-9, -7), "right", "top")
NUDGE = {("PFHxA", "Female"): UP, ("PFOA", "Male"): DOWN, ("PFBA", "Female"): UP}
for r in mr:
    sm, sr = float(r["serum_median_mouse_ngml"]), float(r["serum_median_rat_ngml"])
    if sr <= 0:
        continue
    x, y = sm / sr, float(r["halflife_ratio_mouse_over_rat"])
    male = r["sex"] == "Male"
    col = BLUE if male else ORANGE
    ax.scatter(x, y, s=80, color=col, edgecolor=SURFACE, linewidth=2, zorder=4)
    off, ha, va = NUDGE.get((r["PFAS"], r["sex"]), UP if male else DOWN)
    ax.annotate(f"{r['PFAS']}", (x, y), xytext=off, textcoords="offset points",
                fontsize=8, color=INK2, ha=ha, va=va, zorder=5)
ax.axhline(1.0, color=INK, linewidth=1.4, zorder=3)
lim = [0.02, 30]
ax.plot(lim, lim, color=MUTED, linewidth=1.2, linestyle=(0, (4, 3)), zorder=2)
ax.annotate("if exposure alone explained the gap", (0.992, 0.655),
            xycoords="axes fraction", fontsize=8.5, color=MUTED, ha="right")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(*lim)
ax.set_ylim(0.3, 60)
ax.set_xticks([0.05, 0.1, 0.5, 1, 2, 5, 10, 20])
ax.set_xticklabels(["0.05x", "0.1x", "0.5x", "1x", "2x", "5x", "10x", "20x"])
ax.set_yticks([0.5, 1, 2, 5, 10, 20, 50])
ax.set_yticklabels(["0.5x", "1x", "2x", "5x", "10x", "20x", "50x"])
ax.minorticks_off()
ax.set_xlabel("mouse serum ÷ rat serum  (median measured, log scale)")
ax.set_ylabel("mouse half-life ÷ rat half-life  (log scale)")
titled(ax, "Matching on serum concentration does not close the gap",
       "Inside the shaded band the two species reached the same internal "
       "concentration,\nyet half-lives still differ by a median of 2.1x "
       "and by 15.3x for PFHxS.")
ax.set_axisbelow(True)
ax.legend(handles=[Line2D([], [], marker="o", linestyle="", markersize=8,
                          color=c, label=s) for s, c in
                   (("Male", BLUE), ("Female", ORANGE))],
          loc="upper center", bbox_to_anchor=(0.5, -0.135), ncol=2, fontsize=9)
fig.tight_layout()
fig.savefig(FIG / "fig4_matched_exposure.png", dpi=200)
plt.close(fig)

for p in sorted(FIG.glob("*.png")):
    print(f"wrote {p}  ({p.stat().st_size // 1024} KB)")


# ---- Figure 5: the single renal axis --------------------------------------
# Needs reabsorption_axis.csv from scripts/reabsorption_axis.py.
if (DB / "reabsorption_axis.csv").exists():
    ax_rows = load("reabsorption_axis.csv")
    # Panel A restates OEHHA Table A6.4 in full, including species with no
    # fitted Vd, so the ladder is not truncated to the modelled subset.
    LADDER = [
        ("human", "male", 99.8, False), ("mouse", "male", 97.0, False),
        ("mouse", "female", 95.2, False), ("rat", "male", 93.2, False),
        ("macaque", "male", 91.2, False), ("macaque", "female", 81.2, False),
        ("dog", "male", 59.0, False), ("dog", "female", 52.0, False),
        ("rat", "female", None, True), ("rabbit", "male", None, True),
        ("rabbit", "female", None, True),
    ]
    fig, axes = plt.subplots(1, 2, figsize=(11.6, 5.4),
                             gridspec_kw={"width_ratios": [1.2, 1]})

    a = axes[0]
    labels = [f"{sp} {sx}" for sp, sx, _, _ in LADDER]
    ys = list(range(len(labels)))[::-1]
    for y, (sp, sx, pct, sec) in zip(ys, LADDER):
        if sec:
            a.scatter([1.6], [y], s=95, color=ORANGE, marker="D",
                      edgecolor=SURFACE, linewidth=2, zorder=4)
            a.annotate("net secretion", (1.6, y), xytext=(11, 0),
                       textcoords="offset points", va="center", fontsize=8.5,
                       color=ORANGE)
        else:
            esc = 1 - pct / 100
            a.plot([1.5e-3, esc], [y, y], color="#dcdbd6", linewidth=1.6, zorder=2)
            a.scatter([esc], [y], s=95, color=BLUE, edgecolor=SURFACE,
                      linewidth=2, zorder=4)
            a.annotate(f"{pct:.1f}%", (esc, y), xytext=(11, 0),
                       textcoords="offset points", va="center", fontsize=8.5,
                       color=INK2)
    a.set_xscale("log")
    a.set_xlim(1.5e-3, 9)
    a.set_xticks([0.002, 0.01, 0.05, 0.2, 1])
    a.set_xticklabels(["0.2%", "1%", "5%", "20%", "100%"])
    a.set_yticks(ys)
    a.set_yticklabels(labels)
    a.set_xlabel("fraction of filtered PFOA escaping reabsorption (log scale)")
    titled(a, "One axis: what the kidney lets go",
           "Percentages as OEHHA computes them, at an assumed unbound\n"
           "fraction of 0.02. Female rats and rabbits secrete PFOA outright.")
    recessive(a)

    b = axes[1]
    for r in ax_rows:
        if r["species"] == "human":
            continue
        pr, ob = float(r["halflife_predicted_renal_only_d"]), float(r["halflife_observed_d"])
        secreting = r["net_secretion"] == "yes"
        b.scatter(ob, pr, s=95, color=ORANGE if secreting else BLUE,
                  marker="D" if secreting else "o",
                  edgecolor=SURFACE, linewidth=2, zorder=4)
        b.annotate(f"{r['species']} {r['sex'].lower()}", (ob, pr), xytext=(9, -5),
                   textcoords="offset points", fontsize=8.5, color=INK2, zorder=5)

    # The human point under four successively more complete clearance bases.
    hv = next(r for r in ax_rows if r["species"] == "human")
    vd_h, obs_h = float(hv["vd_L_kg"]), float(hv["halflife_observed_d"])
    HUMAN = [("renal only", 0.060), ("+ faecal", 0.095),
             ("EPA 2024", 0.120), ("OEHHA 2024", 0.280)]
    hx = [obs_h] * len(HUMAN)
    hy = [math.log(2) * vd_h / (cl / 1000.0) for _, cl in HUMAN]
    b.plot(hx, hy, color=MUTED, linewidth=1.4, linestyle=(0, (3, 3)), zorder=3)
    # The four human points are nearly stacked, so labels alternate sides.
    for i, ((lab, _), x, y) in enumerate(zip(HUMAN, hx, hy)):
        b.scatter([x], [y], s=95, color=BLUE, edgecolor=SURFACE,
                  linewidth=2, zorder=4)
        right = i % 2 == 0
        b.annotate(f"human, {lab}", (x, y),
                   xytext=(11, 2) if right else (-11, -2),
                   textcoords="offset points", fontsize=8.5, color=INK2,
                   ha="left" if right else "right",
                   va="bottom" if right else "top", zorder=5)

    lim = [0.3, 9000]
    b.plot(lim, lim, color=INK, linewidth=1.4, zorder=3)
    for k in (2, 0.5):
        b.plot(lim, [v * k for v in lim], color=MUTED, linewidth=1,
               linestyle=(0, (4, 3)), zorder=2)
    b.annotate("within 2x", (lim[1], lim[1] * 2), xytext=(-50, -12),
               textcoords="offset points", fontsize=8.5, color=MUTED)
    b.set_xscale("log")
    b.set_yscale("log")
    b.set_xlim(*lim)
    b.set_ylim(*lim)
    for setter, labeller in ((b.set_xticks, b.set_xticklabels),
                             (b.set_yticks, b.set_yticklabels)):
        setter([1, 10, 100, 1000])
        labeller(["1", "10", "100", "1,000"])
    b.minorticks_off()
    b.set_xlabel("observed PFOA half-life (days, log scale)")
    b.set_ylabel("predicted from clearance and Vd (days, log scale)")
    titled(b, "No fitted parameters",
           "Rodents land within 1.7x. The human point only joins them\n"
           "once clearance counts more than urine.")
    b.set_axisbelow(True)

    fig.text(0.012, 0.015,
             "Reabsorption and renal clearance: OEHHA 2024 PHG Table A6.4 "
             "(after Han et al. 2012). Vd and observed half-life: EPA animal PK "
             "fits and Chiu et al. 2022. Faecal share: Andersson et al. 2025.",
             fontsize=8, color=MUTED, ha="left")
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.savefig(FIG / "fig5_reabsorption_axis.png", dpi=200)
    plt.close(fig)
    print(f"wrote {FIG/'fig5_reabsorption_axis.png'}")
