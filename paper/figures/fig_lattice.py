"""Figure 1: the Moser lattice -- its 30 unit vectors, and a ball of depth 2."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

from hn.field import set_primes
set_primes((3, 5, 11))
from hn.field import K, Pt
from hn.construct import ball, unit_vector_family, pt_float, edges_grid
from style import save, TEXTWIDTH

W = TEXTWIDTH
fig = plt.figure(figsize=(W, W / 2.06))

# ---- left: the origin and its 30 unit neighbours -------------------------
vecs = unit_vector_family(2)
pts = [Pt(K.zero(), K.zero())] + list(vecs)
xy = [pt_float(p) for p in pts]
edges = edges_grid(pts)
print(f"depth-1 star: {len(xy)} vertices, {len(edges)} edges")
assert (len(xy), len(edges)) == (31, 60), "the caption's star"

ax = fig.add_axes([0.0, 0.0, 0.5, 1.0])
ax.set_aspect("equal")
ax.axis("off")
ax.add_collection(LineCollection([(xy[a], xy[b]) for a, b in edges],
                                 linewidths=0.35, colors="0.30", zorder=1))
ax.plot([p[0] for p in xy], [p[1] for p in xy], "o", ms=1.9, color="black",
        zorder=2, markeredgewidth=0, linestyle="none")
ax.set_xlim(-1.09, 1.09)
ax.set_ylim(-1.09, 1.09)

# ---- right: the ball of depth 2 ------------------------------------------
pts2 = ball(vecs, 2, 2.05)
xy2 = [pt_float(p) for p in pts2]
edges2 = edges_grid(pts2)
print(f"depth-2 ball: {len(xy2)} vertices, {len(edges2)} edges")
assert (len(xy2), len(edges2)) == (451, 1920), "the caption's ball"

ax2 = fig.add_axes([0.5, 0.0, 0.5, 1.0])
ax2.set_aspect("equal")
ax2.axis("off")
ax2.add_collection(LineCollection([(xy2[a], xy2[b]) for a, b in edges2],
                                  linewidths=0.14, colors="0.42", zorder=1))
ax2.plot([p[0] for p in xy2], [p[1] for p in xy2], "o", ms=0.6, color="black",
         zorder=2, markeredgewidth=0, linestyle="none")
r = max(max(abs(p[0]), abs(p[1])) for p in xy2) * 1.04
ax2.set_xlim(-r, r)
ax2.set_ylim(-r, r)

save(fig, "lattice")
