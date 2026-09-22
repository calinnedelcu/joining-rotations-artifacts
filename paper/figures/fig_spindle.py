"""The spindle mechanism at squared radius a, drawn for a = 4."""
import sys
from math import sqrt, degrees, atan2, cos, sin, pi
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib.pyplot as plt
from matplotlib.patches import Arc
from style import save, scale

a = 4
ca, sa = (2 * a - 1) / (2 * a), sqrt(4 * a - 1) / (2 * a)
R = sqrt(a)
p = (R, 0.0)
q = (R * ca, R * sa)
h = ((p[0] - q[0]) / 2, (p[1] - q[1]) / 2)
assert abs(sqrt((p[0]-q[0])**2 + (p[1]-q[1])**2) - 1) < 1e-12
assert abs(sqrt(h[0]**2 + h[1]**2) - 0.5) < 1e-12
print(f"  a={a}: |p-theta(p)| = 1, |half| = 1/2, exact")

# Every drawn dimension below is multiplied by K, so the Geombinatorics copy is
# this exact picture enlarged until its 8.5pt type lands on 11pt.  K is 1.0 for
# the default build.
F = 8.5
K = scale(F)
F *= K
fig = plt.figure(figsize=(2.78 * K, 2.78 * K))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_aspect("equal"); ax.axis("off")

ax.add_artist(plt.Circle((0, 0), R, fill=False, lw=0.4 * K, ec="0.64", zorder=0))
for z in (p, q):
    ax.plot([0, z[0]], [0, z[1]], lw=0.45 * K, color="0.42", zorder=1)
ax.plot([p[0], q[0]], [p[1], q[1]], lw=1.3 * K, color="black", zorder=3)
ax.plot([0, h[0]], [0, h[1]], lw=1.3 * K, color="black", zorder=3)
ax.add_artist(Arc((0, 0), 1.1, 1.1, theta1=0, theta2=degrees(atan2(sa, ca)),
                  lw=0.45 * K, color="0.42"))
for z in (p, q, h, (0, 0)):
    ax.plot([z[0]], [z[1]], "o", ms=2.8 * K, color="black", markeredgewidth=0)

ax.text(-0.11, 0.03, "$0$", ha="right", va="bottom", fontsize=F)
ax.text(p[0] + 0.09, p[1] - 0.05, "$p$", ha="left", va="center", fontsize=F)
ax.text(q[0] + 0.08, q[1] + 0.06, r"$\theta_a(p)$", ha="left", va="bottom", fontsize=F)
ax.text((p[0]+q[0])/2 + 0.10, (p[1]+q[1])/2, "$1$", ha="left", va="center", fontsize=F)
ax.text(h[0] + 0.11, h[1] - 0.03, r"$\frac{1}{2}(p-\theta_a(p))$",
        ha="left", va="top", fontsize=F)
m = degrees(atan2(sa, ca)) / 2 * pi / 180
ax.text(0.66 * cos(m), 0.66 * sin(m), r"$\theta_a$", ha="left", va="bottom", fontsize=F)
ax.text(-R * 0.72, R * 0.72, r"$\sqrt{a}$", ha="right", va="bottom",
        fontsize=F, color="0.45")

ax.set_xlim(-R - 0.20, R + 0.86)
ax.set_ylim(-R - 0.36, R + 0.20)
save(fig, "spindle")
