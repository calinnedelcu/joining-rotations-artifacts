"""The seven joining rotations, each acting on its own shell.

One panel per rotation: the lattice points at squared radius a (filled), their
images under theta_a (open), and the unit edge each pair acquires.  Panels are
drawn to a common circle size, so what varies across them is the shell, not the
scale; the true radius is in the caption.
"""
import sys
from math import sqrt, cos, sin, acos, hypot
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib.pyplot as plt
from latticeshell import shell, to_xy
from style import save, TEXTWIDTH

ROTS = [
    (r"$\theta_4$",          4,   1),
    (r"$\theta_{16}$",      16,   1),
    (r"$\theta_{28}$",      28,   1),
    (r"$\theta_{36}$",      36,   1),
    (r"$\alpha_{64/3}$",    64,   3),
    (r"$\alpha_{64/9}$",    64,   9),
    (r"$\alpha_{256/9}$",  256,   9),
]

W = TEXTWIDTH
PAN = W / 4.0                      # four panels across
LAB = 0.16                         # strip under each row for the label
H = 2 * PAN + 2 * LAB
fig = plt.figure(figsize=(W, H))


def panel(x0, y0, name, num, den):
    pts = [to_xy(t) for t in shell(num, den)]
    a = num / den
    r = sqrt(a)
    th = acos((2 * a - 1) / (2 * a))
    c, s = cos(th), sin(th)
    img = [(c * x - s * y, s * x + c * y) for x, y in pts]
    for (x, y), (u, v) in zip(pts, img):
        assert abs(hypot(x - u, y - v) - 1) < 1e-9, name
    ax = fig.add_axes([x0 / W, (y0 + LAB) / H, PAN / W, PAN / H])
    ax.set_aspect("equal"); ax.axis("off")
    ax.add_artist(plt.Circle((0, 0), r, fill=False, lw=0.35, ec="0.66"))
    for (x, y), (u, v) in zip(pts, img):
        ax.plot([x, u], [y, v], lw=0.4, color="0.10", zorder=3)
    ax.plot([p[0] for p in pts], [p[1] for p in pts], "o", ms=1.5,
            color="black", mew=0, linestyle="none", zorder=4)
    ax.plot([p[0] for p in img], [p[1] for p in img], "o", ms=2.0,
            mfc="white", mec="black", mew=0.4, linestyle="none", zorder=4)
    ax.plot([0], [0], "o", ms=1.2, color="0.45", mew=0)
    m = r * 1.06
    ax.set_xlim(-m, m); ax.set_ylim(-m, m)
    fig.text((x0 + PAN / 2) / W, (y0 + 0.030) / H, name, ha="center",
             va="bottom", fontsize=8.5)
    print(f"  {name:16s} shell {len(pts):3d}   radius {r:.4f}")
    return len(pts)


tot = 0
for i, (name, n, d) in enumerate(ROTS[:4]):
    tot += panel(i * PAN, PAN + LAB, name, n, d)
for i, (name, n, d) in enumerate(ROTS[4:]):
    tot += panel((i + 0.5) * PAN, 0.0, name, n, d)
print(f"  total shell points drawn: {tot}")
save(fig, "shells")
