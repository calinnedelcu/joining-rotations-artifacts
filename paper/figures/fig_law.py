"""The divisibility law as a sieve over the integer spindles a <= 100.

Top row: the shells the lattice actually has.  Middle row: the multiples of 4.
Bottom row: their intersection, which by Theorem 1 is exactly the set of
joining rotations.  Nothing here is drawn by hand -- the top row is
scripts/shells.py's exact count, the bottom row is the intersection taken in
code.
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from shells import shell_count          # scripts/shells.py, the exact counter
from style import save, TEXTWIDTH

HI = 100
occupied = {a for a in range(1, HI + 1) if shell_count(a)}
div4 = {a for a in range(1, HI + 1) if a % 4 == 0}
cand = sorted(occupied & div4)
# the three verdicts of results/BALL-FREE-TYPE-M.md, which the figure must agree with
BUILT = {4, 16, 28, 36}                          # 5-chromatic union exhibited
DEAD = {12, 20, 44, 48, 52, 60, 76, 80, 84, 92, 100}   # killed by the section 7 filter
OPEN = {64}                                      # filter degenerates at every modulus
assert BUILT | DEAD | OPEN == set(cand), set(cand) ^ (BUILT | DEAD | OPEN)
print(f"  occupied {len(occupied)}, 4|a {len(div4)}, candidates {len(cand)}: {cand}")
print(f"  empty multiples of 4: {sorted(div4 - occupied)}")
print(f"  built {len(BUILT)}, dead {len(DEAD)}, undecided {len(OPEN)}")

W, H = TEXTWIDTH, 1.30
fig = plt.figure(figsize=(W, H))
LEFT = 0.86 / W
ax = fig.add_axes([LEFT, 0.20, 1 - LEFT - 0.018, 0.74])
ax.set_xlim(0.2, HI + 0.8)
ax.set_ylim(-0.55, 2.62)
ax.axis("off")

ROWS = [(2, occupied, r"shell $\neq\emptyset$"),
        (1, div4,     r"$4\mid a$"),
        (0, set(cand), "candidates")]
w, h = 0.66, 0.46
for y, S, lab in ROWS:
    ax.plot([0.5, HI + 0.5], [y - 0.30, y - 0.30], lw=0.3, color="0.80", zorder=0)
    for a in sorted(S):
        # the bottom row carries the verdict, which the law alone does not give:
        # filled = built, grey = killed later, outline = still undecided.
        fc, ec = "black", "black"
        if y == 0 and a in DEAD:
            fc = ec = "0.66"
        elif y == 0 and a in OPEN:
            fc = "white"
        ax.add_patch(Rectangle((a - w / 2, y - 0.23), w, h,
                               facecolor=fc, edgecolor=ec, lw=0.4, zorder=2))
    ax.text(-0.8, y, lab, ha="right", va="center", fontsize=7.6)

for a in range(10, HI + 1, 10):
    ax.plot([a, a], [-0.42, -0.34], lw=0.4, color="black")
    ax.text(a, -0.50, str(a), ha="center", va="top", fontsize=6.8)
ax.plot([1, 1], [-0.42, -0.34], lw=0.4, color="black")
ax.text(1, -0.50, "1", ha="center", va="top", fontsize=6.8)

save(fig, "law")
