"""Shared drawing style for the figures of joining-rotations.tex.

The register is the one the subject's papers use (Parts, Voronov et al.): a
figure is a *drawing of the object*, not a diagram about it -- black dots, thin
black lines, no colour, no axes, and no label that the caption could carry
instead.  Text inside a figure is set in Computer Modern, which matplotlib
ships, so it matches amsart rather than sitting next to it.

Figures are drawn at their final printed size and included at natural size
(no width= key), so a point in here is a point on the page.
"""
import os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

HERE = Path(__file__).resolve().parent

# amsart 11pt sets a 30pc text block; stay inside it so nothing overflows.
TEXTWIDTH = 4.75

# Geombinatorics is camera-ready and reproduces illustrations WITHOUT reduction,
# and asks for "11 pt fonts for any letters and text that is a part of
# illustrations".  Ours are set at 6.8 to 8.5, so they have to grow.
#
# Growing the type alone would drop large labels onto an unchanged drawing and
# wreck every figure's proportions.  Instead the whole drawing is enlarged by
# 11/base, which leaves the picture identical and lands its type on exactly
# 11pt.  Nothing is scaled at inclusion time: the .tex uses no width= key, so a
# point here stays a point on the page, which is the only way the 11pt survives.
#
# GEOM_FIGURES=1 writes the enlarged set to figures/geom/.  Without it the
# scripts are byte-for-byte what they were, because the 10pt build has to keep
# reproducing the PDF deposited at 10.5281/zenodo.22895457.
GEOM = bool(os.environ.get("GEOM_FIGURES"))
GEOM_PT = 11.0
OUTDIR = HERE / "geom" if GEOM else HERE
# The real Geombinatorics measure is 346.9pt = 4.818in; TEXTWIDTH is the
# narrower figure budget, and an enlargement may use the difference.
MAXWIDTH = 4.81


def scale(base_fs):
    """The enlargement that puts type of size `base_fs` onto 11pt.

    Returns 1.0 unless GEOM_FIGURES is set, so the default figures never move.
    """
    return GEOM_PT / base_fs if GEOM else 1.0

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
    OUTDIR.mkdir(exist_ok=True)
    fig.savefig(OUTDIR / f"{name}.pdf")
    fig.savefig(OUTDIR / f"{name}.png", dpi=260)
    plt.close(fig)
    print(f"  wrote {name}.pdf / .png")
