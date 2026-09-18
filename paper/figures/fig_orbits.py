"""The whole theta_4 interface: all 126 cross edges a depth-4 ball offers.

Sixty run to the shared origin, thirty join two points of the shell at radius 2
(the *reference* orbit), and thirty-six run crosswise between radii
sqrt11/2 -+ sqrt3/6 (the *auxiliary* orbit).  Computed from the coordinates,
not assembled by hand; the cache only saves recomputing the ball.
"""
import json
import math
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
sys.path.insert(0, str(HERE))

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from style import save

CACHE = HERE / "crossedges.json"


def compute():
    from collections import defaultdict
    from hn.field import set_primes
    set_primes((3, 5, 11))
    from hn.construct import ball, unit_vector_family, pt_float, theta4, to_float
    L = ball(unit_vector_family(2), 4, 2.05)
    T = [theta4(p) for p in L]
    Lf, Tf = [pt_float(p) for p in L], [pt_float(p) for p in T]
    nL = [to_float(p.norm2()) for p in L]
    nT = [to_float(p.norm2()) for p in T]
    g = defaultdict(list)
    for j, (x, y) in enumerate(Tf):
        g[(math.floor(x), math.floor(y))].append(j)
    out = []
    for i, (x, y) in enumerate(Lf):
        gx, gy = math.floor(x), math.floor(y)
        for dx in (-2, -1, 0, 1, 2):
            for dy in (-2, -1, 0, 1, 2):
                for j in g.get((gx + dx, gy + dy), ()):
                    u, v = Tf[j]
                    if abs(math.hypot(x - u, y - v) - 1) < 1e-9:
                        kind = ("origin" if min(nL[i], nT[j]) < 1e-9 else
                                "reference" if abs(nL[i] - 4) < 1e-6 else "auxiliary")
                        out.append([Lf[i], Tf[j], kind])
    return out


if CACHE.exists():
    E = json.loads(CACHE.read_text())
else:
    E = compute()
    CACHE.write_text(json.dumps(E))

kinds = {k: [e for e in E if e[2] == k] for k in ("origin", "reference", "auxiliary")}
print(f"  {len(E)} cross edges: " +
      ", ".join(f"{len(v)} {k}" for k, v in kinds.items()))
assert len(E) == 126 and [len(kinds[k]) for k in ("origin", "reference", "auxiliary")] == [60, 30, 36]
for p, q, _ in E:
    assert abs(math.hypot(p[0] - q[0], p[1] - q[1]) - 1) < 1e-9

S = 3.30
fig = plt.figure(figsize=(S, S))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_aspect("equal"); ax.axis("off")

R11, R3 = math.sqrt(11) / 2, math.sqrt(3) / 6
for r, ls in ((1.0, ":"), (R11 - R3, ":"), (R11 + R3, ":"), (2.0, "-")):
    ax.add_artist(plt.Circle((0, 0), r, fill=False, ec="0.70", lw=0.35,
                             ls=ls, zorder=0))

STYLE = {"origin": dict(lw=0.30, color="0.62"),
         "reference": dict(lw=0.50, color="0.10"),
         "auxiliary": dict(lw=0.50, color="0.10")}
for k in ("origin", "auxiliary", "reference"):
    ax.add_collection(LineCollection([(e[0], e[1]) for e in kinds[k]],
                                     zorder=2, **STYLE[k]))

# one edge of each orbit, drawn heavy and labelled outside the disc
def nearest(kind, deg):
    t = math.radians(deg)
    return min(kinds[kind],
               key=lambda e: abs(math.atan2((e[0][1] + e[1][1]) / 2,
                                            (e[0][0] + e[1][0]) / 2) - t))

for kind, lab, deg in (("reference", "reference", 8), ("auxiliary", "auxiliary", 152)):
    p, q, _ = nearest(kind, deg)
    ax.plot([p[0], q[0]], [p[1], q[1]], lw=1.7, color="black", zorder=5,
            solid_capstyle="round")
    ax.plot([p[0]], [p[1]], "o", ms=3.4, color="black", mew=0, zorder=6)
    ax.plot([q[0]], [q[1]], "o", ms=3.8, mfc="white", mec="black", mew=0.7, zorder=6)
    mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
    f = 1.0 + 0.62 / math.hypot(mx, my)
    ax.annotate(lab, xy=(mx, my), xytext=(mx * f, my * f), fontsize=7.6,
                ha="center", va="center", zorder=7,
                bbox=dict(boxstyle="round,pad=0.10", fc="white", ec="none"),
                arrowprops=dict(arrowstyle="-", lw=0.4, color="0.45",
                                shrinkA=2, shrinkB=3))

ax.plot([0], [0], "o", ms=2.4, color="black", mew=0, zorder=6)
m = 3.05
ax.set_xlim(-m, m); ax.set_ylim(-m, m)
save(fig, "orbits")
