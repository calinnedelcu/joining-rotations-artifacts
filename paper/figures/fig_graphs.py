"""The 1408-vertex minimised graph of alpha_{64/9}, drawn from its own coordinates."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from hn.field import set_primes
from style import canvas, draw_graph, frame, save, TEXTWIDTH

ROOT = Path(__file__).resolve().parents[2]


def load_edge_file(path):
    edges = []
    for line in open(path):
        if line.startswith("e "):
            _, a, b = line.split()
            edges.append((int(a) - 1, int(b) - 1))
    return edges


def fig_alpha649():
    """The 1408-vertex vertex-critical graph of alpha_{64/9}."""
    set_primes((3, 11, 247))
    from hn.io import load_points
    from hn.construct import pt_float
    pts = load_points(ROOT / "results/alpha64_9/minimised.pts")
    edges = load_edge_file(ROOT / "results/alpha64_9/minimised.edge")
    xy = [pt_float(p) for p in pts]
    print(f"alpha_64/9: {len(xy)} vertices, {len(edges)} edges")
    assert (len(xy), len(edges)) == (1408, 7013), "the caption's counts"

    fig, ax = canvas(TEXTWIDTH, TEXTWIDTH)
    draw_graph(ax, xy, edges, lw=0.11, ms=0.5, ecolor="0.52", alpha=0.75)
    frame(ax, xy)
    save(fig, "alpha649")


if __name__ == "__main__":
    fig_alpha649()
