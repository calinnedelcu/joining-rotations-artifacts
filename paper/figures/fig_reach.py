"""Why six of the seven were never found: they are out of reach.

The seven shells at their true relative radii, against the reach of the record
graph itself.  A rotation theta_a moves nothing but the points at distance
sqrt(a), so a search whose ball stops short of that radius cannot see it however
carefully it enumerates rotations.  The two radii are measured, not assumed:
Parts' 509 vertices lie inside 2.5244 and its large part inside 2.0238, both
recomputed from data/vtx/509.vtx by scripts/audit_numbers.py.
"""
import sys
from math import sqrt, cos, sin, pi
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib.pyplot as plt
from latticeshell import shell, to_xy
from style import save

ROTS = [(r"$\theta_4$", 4, 1), (r"$\alpha_{64/9}$", 64, 9),
        (r"$\theta_{16}$", 16, 1), (r"$\alpha_{64/3}$", 64, 3),
        (r"$\theta_{28}$", 28, 1), (r"$\alpha_{256/9}$", 256, 9),
        (r"$\theta_{36}$", 36, 1)]
SEARCHED_LO, SEARCHED_HI = 2.0238, 2.5244     # record: large part, whole graph

S = 3.45
fig = plt.figure(figsize=(S, S))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_aspect("equal"); ax.axis("off")

ax.add_artist(plt.Circle((0, 0), SEARCHED_HI, facecolor="0.90",
                         edgecolor="none", zorder=0))
for r in (SEARCHED_LO, SEARCHED_HI):
    ax.add_artist(plt.Circle((0, 0), r, fill=False, ec="0.55", lw=0.45,
                             ls=(0, (2.5, 1.8)), zorder=1))

ANG = [102, 160, 74, 208, 46, 256, 20]
reach, sizes = [], []
for (name, n, d), deg in zip(ROTS, ANG):
    r = sqrt(n / d)
    pts = [to_xy(t) for t in shell(n, d)]
    reach.append((name, r <= SEARCHED_HI)); sizes.append(len(pts))
    ax.add_artist(plt.Circle((0, 0), r, fill=False, ec="0.62", lw=0.35, zorder=2))
    ax.plot([p[0] for p in pts], [p[1] for p in pts], "o", ms=1.6,
            color="black", mew=0, linestyle="none", zorder=4)
    t = deg * pi / 180
    ax.text(r * cos(t), r * sin(t), name, ha="center", va="center", fontsize=7.4,
            zorder=6,
            bbox=dict(boxstyle="round,pad=0.14", fc="white", ec="none", alpha=0.94))
    print(f"  {name:16s} radius {r:.4f}  shell {len(pts):3d}"
          f"  {'reachable' if r <= SEARCHED_HI else 'out of reach'}")

ax.plot([0], [0], "o", ms=1.6, color="black", mew=0)
m = 6.28
ax.set_xlim(-m, m); ax.set_ylim(-m, m)
inside = [nm for nm, ok in reach if ok]
assert inside == [r"$\theta_4$"], f"the caption says only theta_4 is reachable, got {inside}"
assert abs(sqrt(4) - 2) < 1e-12 and sizes == [30, 6, 30, 18, 60, 6, 54], sizes
save(fig, "reach")
