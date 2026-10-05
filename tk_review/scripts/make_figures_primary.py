#!/usr/bin/env python3
"""Figures for the findings that came from the nine primary full texts.

Separate from make_figures.py so the original figure set stays reproducible.
Palette is the project's validated categorical set (blue/orange/aqua), checked
with the dataviz validator against the #fcfcfb surface.

Run:  python3 scripts/make_figures_primary.py   # -> figures/fig10..fig15
"""
import csv
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

HERE = os.path.dirname(os.path.abspath(__file__))
PRIM = os.path.join(HERE, "..", "db", "primary_2026")
OUT = os.path.join(HERE, "..", "figures")

BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
SURFACE = "#fcfcfb"
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#8a8984"
GRID, RULE = "#e6e5e1", "#d8d7d3"

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
    "font.family": "DejaVu Sans", "font.size": 9,
    "axes.edgecolor": RULE, "axes.linewidth": 0.8,
    "axes.labelcolor": INK2, "text.color": INK,
    "xtick.color": INK2, "ytick.color": INK2,
    "xtick.labelsize": 8.5, "ytick.labelsize": 8.5,
    "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False, "legend.fontsize": 8.5,
})


def load(name):
    with open(os.path.join(PRIM, name)) as fh:
        return list(csv.DictReader(fh))


def titles(ax, title, subtitle=None):
    ax.set_title(title, loc="left", fontsize=11, color=INK, pad=18 if subtitle else 8,
                 fontweight="semibold")
    if subtitle:
        ax.text(0, 1.015, subtitle, transform=ax.transAxes, fontsize=8.5,
                color=MUTED, va="bottom")


def grid(ax, axis="y"):
    ax.grid(axis=axis, color=GRID, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=200, bbox_inches="tight")
    plt.close(fig)
    print("wrote", name)


# ---------------------------------------------------------------- fig 10
def fig10_sex_vs_species():
    """Six datasets: the Vd sex ratio is conserved, the clearance ratio is not."""
    kudo = {r["parameter"]: r for r in load("kudo2002_rat_tk.csv")}
    lou = {(r["matrix"], r["parameter"]): r for r in load("lou2009_mouse_tk.csv")}
    sund = load("sundstrom2012_pfhxs_three_species.csv")

    def pick(sp, sex, dose, tbl):
        for r in sund:
            if (r["species"] == sp and r["sex"] == sex
                    and r["dose_mgkg"] == dose and r["source_table"] == tbl):
                return r

    rows = [
        ("rat\nPFOA", "rat",
         float(kudo["volume_of_distribution"]["male"]) / float(kudo["volume_of_distribution"]["female"]),
         float(kudo["total_clearance_per_day"]["female"]) / float(kudo["total_clearance_per_day"]["male"])),
        ("rat\nPFHxS", "rat", None, None),
        ("monkey\nPFHxS", "monkey", None, None),
        ("mouse\nPFOA", "mouse",
         float(lou[("sera", "vd")]["male"]) / float(lou[("sera", "vd")]["female"]),
         float(lou[("sera", "clearance_derived")]["female"]) / float(lou[("sera", "clearance_derived")]["male"])),
        ("mouse\nPFHxS 1", "mouse", None, None),
        ("mouse\nPFHxS 20", "mouse", None, None),
    ]
    spec = {1: ("rat", "10", "Table 2"), 2: ("monkey (cynomolgus)", "10", "Table 5"),
            4: ("mouse", "1", "Table 3"), 5: ("mouse", "20", "Table 3")}
    for i, (sp, dose, tbl) in spec.items():
        m, f = pick(sp, "male", dose, tbl), pick(sp, "female", dose, tbl)
        rows[i] = (rows[i][0], rows[i][1],
                   float(m["vd_mL_kg"]) / float(f["vd_mL_kg"]),
                   float(f["clearance_mL_d_kg"]) / float(m["clearance_mL_d_kg"]))

    COL = {"rat": BLUE, "mouse": ORANGE, "monkey": AQUA}
    labs = [r[0] for r in rows]
    vds = [r[2] for r in rows]
    cls = [r[3] for r in rows]
    cols = [COL[r[1]] for r in rows]
    x = list(range(len(rows)))

    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.6), sharex=True)
    for ax, vals, title, note in (
        (axes[0], vds, "Volume of distribution — male ÷ female",
         "conserved: a 1.6× spread across all six"),
        (axes[1], cls, "Clearance — female ÷ male",
         "not conserved: a 56× spread, and it changes sign"),
    ):
        bars = ax.bar(x, vals, width=0.62, color=cols, zorder=3)
        for b, v in zip(bars, vals):
            ax.annotate(f"{v:.2f}×" if v < 10 else f"{v:.0f}×",
                        (b.get_x() + b.get_width() / 2, v), xytext=(0, 4),
                        textcoords="offset points", ha="center", va="bottom",
                        fontsize=9, color=INK, fontweight="semibold")
        ax.axhline(1, color=RULE, linewidth=1.2, zorder=2)
        ax.set_yscale("log")
        ax.set_ylim(0.45, 160)
        ax.set_xticks(x)
        ax.set_xticklabels(labs, fontsize=8.6)
        ax.set_xlim(-0.7, len(rows) - 0.3)
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _p: f"{v:g}×"))
        grid(ax)
        titles(ax, title, note)

    handles = [plt.Line2D([], [], marker="s", linestyle="", markersize=8,
                          color=c, label=k) for k, c in COL.items()]
    axes[1].legend(handles=handles, loc="upper right", ncol=3)

    fig.suptitle("The sex difference lives in clearance, not distribution",
                 x=0.012, ha="left", fontsize=13, color=INK, fontweight="semibold")
    fig.text(0.012, -0.10,
             "Six datasets measuring BOTH terms in BOTH sexes within single "
             "experiments: three species, two compounds, four laboratories.\n"
             "Kudo 2002 Table 2 (Wistar rat, PFOA); Lou 2009 Table 2 (CD-1 mouse, "
             "PFOA); Sundström 2012 Tables 2, 3 and 5 (Sprague-Dawley rat,\n"
             "CD-1 mouse at 1 and 20 mg/kg, cynomolgus monkey, PFHxS). Log scale. "
             "All three mouse clearance ratios sit below 1 — the female\nmouse "
             "clears these compounds slightly slower than the male, the opposite "
             "sign to the rat.",
             fontsize=7.8, color=MUTED, va="top")
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    save(fig, "fig10_sex_vs_species_decomposition.png")


# ---------------------------------------------------------------- fig 11
def fig11_cl_vs_vss():
    """11 PFAS in one cocktail: clearance spans 5,254x, Vss spans 7.7x."""
    rows = [r for r in load("argoul2026_mouse_tk.csv") if r["cl_mL_kg_day"]]
    rows.sort(key=lambda r: float(r["cl_mL_kg_day"]))
    names = [r["chemical"] for r in rows]
    cl = [float(r["cl_mL_kg_day"]) for r in rows]
    vss = [float(r["vss_L_kg"]) * 1000 for r in rows]       # L/kg -> mL/kg
    y = list(range(len(rows)))

    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    for yi, c, v in zip(y, cl, vss):
        ax.plot([min(c, v), max(c, v)], [yi, yi], color=GRID, linewidth=1.6, zorder=2)
    ax.scatter(vss, y, s=62, color=AQUA, zorder=4, label="Vss (mL/kg)",
               edgecolor=SURFACE, linewidth=1.4)
    ax.scatter(cl, y, s=62, color=BLUE, zorder=4, label="clearance (mL/kg-day)",
               edgecolor=SURFACE, linewidth=1.4)
    ax.annotate("PFHxA's Vss is 4.0 L/kg — a deep compartment;\n"
                "the paper puts it at 0.12 L/kg without one",
                (vss[-1], y[-1]), xytext=(0.03, 0.80),
                textcoords="axes fraction", fontsize=7.8, color=MUTED,
                ha="left", va="center",
                arrowprops=dict(arrowstyle="-", color=RULE, linewidth=0.9))
    ax.set_xscale("log")
    ax.set_yticks(y)
    ax.set_yticklabels(names)
    ax.set_xlabel("mL/kg  or  mL/kg-day   (log scale)")
    ax.legend(loc="lower right", ncol=1)
    grid(ax, axis="x")
    titles(ax, "Clearance varies over a range 81× wider than volume of distribution",
           "11 PFAS dosed as one cocktail to female CD-1 mice — "
           "Argoul 2026 Table 1. Clearance spans 5,254×; Vss spans 7.7× "
           "excluding PFHxA.")
    fig.tight_layout()
    save(fig, "fig11_argoul_clearance_vs_vss.png")


# ---------------------------------------------------------------- fig 12
def fig12_reabsorption_axis():
    """Han 2012's axis, with Argoul's independent mouse recomputation."""
    han = load("han2012_table4_reabsorption_axis.csv")
    arg = load("argoul2026_mouse_tk.csv")

    labs, vals = [], []
    for r in han:
        if not r["pct_reabsorption"]:
            labs.append(f"{r['species']} {r['sex']}".replace(" both", ""))
            vals.append(None)
        else:
            labs.append(f"{r['species']} {r['sex']}".replace(" both", ""))
            vals.append(float(r["pct_reabsorption"]))
    order = sorted(range(len(labs)),
                   key=lambda i: (vals[i] is not None, vals[i] or 0))
    labs = [labs[i] for i in order]
    vals = [vals[i] for i in order]

    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(10.4, 4.4),
                                  gridspec_kw={"width_ratios": [1.35, 1]})
    y = list(range(len(labs)))
    for yi, v, lab in zip(y, vals, labs):
        if v is None:
            ax.barh(yi, 100, height=0.6, color="#f2f1ed", zorder=3)
            ax.text(2, yi, "net secretion", fontsize=8, color=ORANGE,
                    va="center", fontweight="semibold")
            continue
        col = ORANGE if "human" in lab else BLUE
        ax.barh(yi, v, height=0.6, color=col, zorder=3)
        ax.text(v - 1.5, yi, f"{v:.2f}%", fontsize=8.5, color="#ffffff",
                va="center", ha="right", fontweight="semibold")
    ax.set_yticks(y)
    ax.set_yticklabels(labs)
    ax.set_xlim(0, 104)
    ax.set_xlabel("% of filtered PFOA reabsorbed")
    grid(ax, axis="x")
    titles(ax, "One axis, seven species",
           "Han 2012 Table 4 — the source OEHHA's Table A6.4 adapts.")

    chems = [r for r in arg
             if r["fu_pct"] and r["cl_renal_measured_mL_kg_day"]
             and not r["cl_renal_measured_mL_kg_day"][0].isalpha()]
    pts = []
    for r in chems:
        try:
            clr = float(r["cl_renal_measured_mL_kg_day"])
        except ValueError:
            continue
        fr = (1 - clr / float(r["cl_gfr_free_mL_kg_day"])) * 100
        pts.append((r["chemical"], fr))
    pts.sort(key=lambda t: t[1])
    y2 = list(range(len(pts)))
    for yi, (c, fr) in zip(y2, pts):
        col = AQUA if fr > 0 else ORANGE
        ax2.barh(yi, fr, height=0.6, color=col, zorder=3)
        ha = "right" if fr > 0 else "left"
        off = -2 if fr > 0 else 2
        ax2.text(fr + off, yi, f"{fr:.1f}", fontsize=8, color=INK2,
                 va="center", ha=ha)
    ax2.axvline(0, color=RULE, linewidth=1.2, zorder=4)
    ax2.axhspan(-0.5, len(pts) - 0.5, xmin=0, xmax=0, color=SURFACE)
    ax2.set_yticks(y2)
    ax2.set_yticklabels([c for c, _ in pts])
    ax2.set_xlim(-185, 112)
    ax2.set_xlabel("% reabsorbed (negative = net secretion)")
    grid(ax2, axis="x")
    titles(ax2, "The same axis, recomputed from scratch",
           "Argoul 2026 Table 4, female mouse. Mouse PFOA → 95.9%, "
           "inside Han's 95.2–97.0%.")
    fig.tight_layout()
    save(fig, "fig12_reabsorption_axis_two_sources.png")


# ---------------------------------------------------------------- fig 13
def fig13_route_by_chain_length():
    """The renal-to-faecal hand-off, replicated in rat and mouse."""
    kudo = load("kudo2001_chain_length_elimination.csv")
    arg = load("argoul2026_mouse_tk.csv")

    rat_m = [(int(r["n_carbons"]), float(r["pct_dose_urine_120h"]))
             for r in kudo if r["sex"] == "male" and r["pct_dose_urine_120h"]]
    rat_f = [(int(r["n_carbons"]), float(r["pct_dose_urine_120h"]))
             for r in kudo if r["sex"] == "female" and r["pct_dose_urine_120h"]]
    pfca = {"PFBA": 4, "PFHxA": 6, "PFOA": 8, "PFNA": 9, "PFDA": 10}
    mouse = sorted((pfca[r["chemical"]], float(r["cl_urinary_pct"]))
                   for r in arg if r["chemical"] in pfca and r["cl_urinary_pct"])

    fig, ax = plt.subplots(figsize=(8.0, 4.4))
    for data, col, lab, mk in (
        (mouse, AQUA, "mouse, % of clearance that is renal (Argoul 2026, 119 d)", "o"),
        (rat_m, BLUE, "male rat, % of dose in urine (Kudo 2001, 120 h)", "s"),
        (rat_f, ORANGE, "female rat, same (Kudo 2001)", "D"),
    ):
        xs = [d[0] for d in data]
        ys = [d[1] for d in data]
        ax.plot(xs, ys, color=col, linewidth=2, marker=mk, markersize=8,
                markeredgecolor=SURFACE, markeredgewidth=1.4, label=lab, zorder=4)
    # Direct value labels on the two PFNA points, and the explanation parked in
    # the empty lower-left quadrant rather than on a leader line across the series.
    ax.annotate("51%", (9, 51.0), xytext=(11, 0), textcoords="offset points",
                fontsize=8.5, color=ORANGE, va="center", fontweight="semibold")
    ax.annotate("2.0%", (9, 2.0), xytext=(9, 13), textcoords="offset points",
                fontsize=8.5, color=BLUE, va="center", fontweight="semibold")
    ax.text(4.1, 42,
            "At C9 the rat splits by sex:\nPFNA is a renal compound in females\n"
            "(51% of dose in urine) and a faecal\none in males (2.0%) — the same\n"
            "androgen-regulated step as §3.4.",
            fontsize=8, color=INK2, va="top", linespacing=1.5)
    ax.set_xlim(3.6, 10.5)
    ax.set_xticks([4, 6, 7, 8, 9, 10])
    ax.set_xlabel("perfluorinated carbons")
    ax.set_ylabel("renal share (%)")
    ax.set_ylim(-4, 108)
    ax.legend(loc="lower left", bbox_to_anchor=(0, -0.42))
    grid(ax)
    titles(ax, "Elimination hands off from kidney to gut as the chain lengthens",
           "Two species, two laboratories, 25 years apart. The two y-quantities "
           "are not identical (see caption) but the shape is.")
    fig.tight_layout()
    save(fig, "fig13_route_split_by_chain_length.png")


# ---------------------------------------------------------------- fig 14
def fig14_thompson():
    """The 170 mL/kg human Vd is proportional to an assumed half-life."""
    rows = load("thompson2010_vd_calibration.csv")
    lh = rows[0]
    dose, serum = (float(lh["daily_dose_ng_kg_day"]),
                   float(lh["serum_pfoa_ng_mL"]))
    ts = [1.5 + 0.05 * i for i in range(53)]
    vds = [dose / (serum * (math.log(2) / (t * 365.25))) for t in ts]

    fig, ax = plt.subplots(figsize=(8.0, 4.4))
    ax.plot(ts, vds, color=BLUE, linewidth=2, zorder=4)
    marks = [(2.37, "as used (kP = 0.0008/d)\nBartell 2010", BLUE),
             (3.3, "Olsen 2007\n(used in the preprint)", ORANGE),
             (3.8, "kP = 0.0005/d as printed", ORANGE)]
    for t, lab, col in marks:
        v = dose / (serum * (math.log(2) / (t * 365.25)))
        ax.scatter([t], [v], s=70, color=col, zorder=6,
                   edgecolor=SURFACE, linewidth=1.5)
        ax.annotate(f"{v:.0f} mL/kg\n{lab}", (t, v), xytext=(12, -26),
                    textcoords="offset points", fontsize=7.8, color=INK2,
                    va="center")
    ax.axhspan(165, 173, color="#eef2f8", zorder=1)
    ax.text(5.05, 169, "the published 165–173 mL/kg", fontsize=8, color=BLUE,
            va="center", ha="right", fontweight="semibold")
    ax.set_xlabel("half-life assumed in the calibration (years)")
    ax.set_ylabel("volume of distribution implied (mL/kg)")
    ax.set_xlim(1.4, 5.1)
    grid(ax)
    titles(ax, "The human Vd that ten studies assign is a function of an assumption",
           "Thompson 2010 Eq. 2c applied to its own supplementary Table S1 "
           "(Little Hocking: 62 ng/kg-day, 448 ng/mL).")
    fig.tight_layout()
    save(fig, "fig14_thompson_vd_vs_assumed_halflife.png")


# ---------------------------------------------------------------- fig 15
def fig15_saturation():
    """In vitro Km and PBPK-fitted KT disagree by three orders of magnitude."""
    MW = 414.07
    serum = [("general population\n~4 ng/mL", 4.0),
             ("Lubeck WV\n68 ng/mL", 68.0),
             ("Little Hocking OH\n448 ng/mL", 448.0),
             ("occupational\n~1000 ng/mL", 1000.0)]
    yang = load("yang2010_human_apical_transporters.csv")
    kms = [(r["transporter"] + f" ({r['condition']})", float(r["km_uM"]) * MW)
           for r in yang if r["km_uM"]]
    kt = 0.055 * 1000      # mg/L -> ng/mL... 0.055 mg/L = 55 ng/mL

    fig, ax = plt.subplots(figsize=(9.6, 4.4))
    ax.axhline(1, color=GRID, linewidth=1.0, zorder=1)
    for i, (lab, v) in enumerate(serum):
        ax.scatter([v], [1], s=70, color=BLUE, zorder=5,
                   edgecolor=SURFACE, linewidth=1.5)
        ax.annotate(lab, (v, 1), xytext=(0, -30 if i % 2 == 0 else 12),
                    textcoords="offset points", fontsize=7.5, color=INK2,
                    ha="center")
    ax.text(1.5, 1.16, "human serum", fontsize=8.5, color=BLUE,
            va="center", ha="left", fontweight="semibold")

    ax.scatter([kt], [0.35], s=95, marker="v", color=ORANGE, zorder=5,
               edgecolor=SURFACE, linewidth=1.5)
    ax.annotate("human PBPK KT = 55 ng/mL\nHan 2012 Table 7, fitted — "
                "three of the four\npopulations above sit AT or ABOVE it",
                (kt, 0.35), xytext=(14, -4), textcoords="offset points",
                fontsize=8, color=ORANGE, ha="left", va="center",
                fontweight="semibold")

    # Stagger the Km markers so their labels cannot collide.
    kms.sort(key=lambda t: t[1])
    for j, (lab, v) in enumerate(kms):
        yv = 1.52 + 0.16 * j
        ax.scatter([v], [yv], s=95, marker="^", color=AQUA, zorder=5,
                   edgecolor=SURFACE, linewidth=1.5)
        ax.annotate(lab, (v, yv), xytext=(12, 0), textcoords="offset points",
                    fontsize=7.8, color=INK2, ha="left", va="center")
    ax.text(1.5, 1.68, "in vitro Km, human apical transporters",
            fontsize=8.5, color=AQUA, va="center", ha="left",
            fontweight="semibold")
    ax.set_xscale("log")
    ax.set_xlim(1.2, 2.2e6)
    ax.set_ylim(0.05, 2.05)
    ax.set_yticks([])
    ax.set_xlabel("PFOA concentration (ng/mL, log scale)")
    ax.spines["left"].set_visible(False)
    grid(ax, axis="x")
    titles(ax, "Does reabsorption saturate? The two parameter families disagree 500–2,300×",
           "All four populations sit far below every measured Km; three of the "
           "four sit at or above the KT that PBPK models run on.")
    fig.tight_layout()
    save(fig, "fig15_saturation_margin.png")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    fig10_sex_vs_species()
    fig11_cl_vs_vss()
    fig12_reabsorption_axis()
    fig13_route_by_chain_length()
    fig14_thompson()
    fig15_saturation()
