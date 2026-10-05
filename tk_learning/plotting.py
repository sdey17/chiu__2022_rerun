"""
Shared plotting style for the lessons.

Every lesson writes its figures into figures/ and prints the path. The
style choices here are not decoration -- they are the ones that stop PK
plots from lying to you:

  * a LOG y-axis by default, because the late points carry the
    elimination information and a linear axis hides them
  * data as open markers, model as a line, so you can always tell which
    is which
  * residual panels underneath the fit, on the same x-axis, because the
    residual pattern is the diagnostic and a fit shown alone hides it

Import `setup()` once at the top of a lesson, then use the helpers.
"""
import os
import sys

import matplotlib

# In a plain script there is no display, so write files with the Agg
# backend. Inside Jupyter, leave the backend alone so figures render in
# the notebook as well as being saved.
IN_NOTEBOOK = "ipykernel" in sys.modules
if not IN_NOTEBOOK:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

FIGDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")

# A small categorical palette that survives greyscale printing and the
# common forms of colour-vision deficiency. Never encode meaning in
# colour alone -- every plot here also labels or shapes its series.
BLUE, ORANGE, GREEN, PURPLE, GREY = (
    "#2a78d6", "#eb6834", "#2e8b57", "#7b5ea7", "#8a8a86")
INK, SOFT, GRID = "#111111", "#55534f", "#e2e1dd"
CYCLE = [BLUE, ORANGE, GREEN, PURPLE, GREY]


def setup():
    plt.rcParams.update({
        "figure.facecolor": "white", "axes.facecolor": "white",
        "axes.edgecolor": GRID, "axes.labelcolor": INK,
        "axes.titlesize": 10, "axes.titlelocation": "left",
        "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.7,
        "axes.axisbelow": True, "axes.spines.top": False,
        "axes.spines.right": False,
        "xtick.color": SOFT, "ytick.color": SOFT,
        "font.size": 9, "legend.frameon": False, "legend.fontsize": 8,
        "figure.dpi": 130,
    })
    os.makedirs(FIGDIR, exist_ok=True)


def save(fig, name, note=None):
    """Save into figures/ and print where it went."""
    if note:
        # negative y puts the caption BELOW the axes; bbox_inches="tight"
        # then grows the canvas to include it, so it never overlaps.
        fig.text(0.01, -0.04, note, fontsize=7.5, color=SOFT, va="top")
    path = os.path.join(FIGDIR, name)
    fig.savefig(path, bbox_inches="tight")
    if IN_NOTEBOOK:
        plt.show()               # render inline as well as saving
    else:
        plt.close(fig)
        print(f"   [figure] figures/{name}")
    # Return the repo-relative form, not `path`. Nothing uses this as a real
    # filesystem path; it is echoed as a cell's last expression in the
    # committed notebooks, where an absolute path would go stale.
    return f"figures/{name}"


def data_points(ax, t, C, label="observed", color=INK, **kw):
    """Measurements: open circles, never joined by a line."""
    kw.setdefault("mfc", "none")
    kw.setdefault("ms", 5)
    kw.setdefault("mew", 1.2)
    return ax.plot(t, C, "o", color=color, linestyle="none", label=label, **kw)


def model_line(ax, t, C, label="model", color=BLUE, **kw):
    # linestyle goes through setdefault rather than a "-" fmt string, so a
    # caller passing linestyle= overrides it instead of colliding with it
    # (matplotlib warns and silently prefers the keyword).
    kw.setdefault("lw", 1.8)
    kw.setdefault("linestyle", "-")
    return ax.plot(t, C, color=color, label=label, **kw)


def fit_and_residuals(t_obs, C_obs, t_grid, C_pred, C_pred_at_obs,
                      title, name, ylabel="serum conc (mg/L)",
                      xlabel="days since dose", note=None, logy=True):
    """The standard two-panel PK figure: fit on top, log residuals below.

    Always look at the bottom panel first. A good model scatters its
    residuals around zero with no run of same-signed points.
    """
    fig, (a, b) = plt.subplots(2, 1, figsize=(6.2, 5.2), sharex=True,
                               height_ratios=[2.4, 1], constrained_layout=True)
    data_points(a, t_obs, C_obs)
    model_line(a, t_grid, C_pred)
    if logy:
        a.set_yscale("log")
    a.set_ylabel(ylabel)
    a.set_title(title)
    a.legend(loc="upper right")

    res = np.log(np.asarray(C_obs) / np.asarray(C_pred_at_obs))
    b.axhline(0, color=SOFT, lw=1)
    b.vlines(t_obs, 0, res, color=GREY, lw=1)
    b.plot(t_obs, res, "o", color=ORANGE, ms=4.5)
    b.set_ylabel("ln(obs/pred)")
    b.set_xlabel(xlabel)
    lim = max(0.3, 1.1 * np.abs(res).max())
    b.set_ylim(-lim, lim)
    return save(fig, name, note)
