"""Shared drawing style for the figures of joining-rotations.tex.

The register is the one the subject's papers use (Parts, Voronov et al.): a
figure is a *drawing of the object*, not a diagram about it -- black dots, thin
black lines, no colour, no axes, and no label that the caption could carry
instead.  Text inside a figure is set in Computer Modern, which matplotlib
ships, so it matches amsart rather than sitting next to it.

Figures are drawn at their final printed size and included at natural size
(no width= key), so a point in here is a point on the page.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

HERE = Path(__file__).resolve().parent

# amsart 11pt sets a 30pc text block; stay inside it so nothing overflows.
TEXTWIDTH = 4.75

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["cmr10"],
    "mathtext.fontset": "cm",
    "axes.unicode_minus": False,
    "pdf.fonttype": 42,
    "pdf.compression": 9,
    "savefig.pad_inches": 0.01,
})


def canvas(w, h):
    """A bare drawing surface: no axes, no frame, no margins, equal aspect."""
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_aspect("equal", adjustable="datalim")
    ax.axis("off")
    return fig, ax


def draw_graph(ax, xy, edges, lw=0.18, ms=0.7, ecolor="0.35", alpha=1.0):
    """A unit-distance graph the way the literature draws one."""
    segs = [(xy[a], xy[b]) for a, b in edges]
    ax.add_collection(LineCollection(segs, linewidths=lw, colors=ecolor,
                                     alpha=alpha, capstyle="round", zorder=1))
    ax.plot([p[0] for p in xy], [p[1] for p in xy], linestyle="none",
            marker="o", markersize=ms, color="black", zorder=2,
            markeredgewidth=0)


def frame(ax, xy, pad=0.04):
    """Fit the view to the drawing with a small uniform margin."""
    xs = [p[0] for p in xy]
    ys = [p[1] for p in xy]
    dx, dy = max(xs) - min(xs), max(ys) - min(ys)
    m = pad * max(dx, dy)
    ax.set_xlim(min(xs) - m, max(xs) + m)
    ax.set_ylim(min(ys) - m, max(ys) + m)


def save(fig, name):
    fig.savefig(HERE / f"{name}.pdf")
    fig.savefig(HERE / f"{name}.png", dpi=260)
    plt.close(fig)
    print(f"  wrote {name}.pdf / .png")
