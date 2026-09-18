"""The two geometric 4-colourings of the Moser lattice, on a depth-2 ball.

They are the reductions modulo the two primes above 2 in Q(sqrt33), and the
Galois conjugation sqrt33 -> -sqrt33 that exchanges those primes exchanges the
two pictures exactly -- asserted below, on all 451 points, with no colour
permutation needed.  Both are checked proper against the repository's own exact
edge finder before anything is drawn.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib.pyplot as plt

from hn.field import set_primes
set_primes((3, 5, 11))
from hn.construct import ball, unit_vector_family, edges_grid, pt_float
from hn.algcolour import certify, apply_colouring, verify_on_ball
from style import save, TEXTWIDTH

vecs = unit_vector_family(2)
v = certify(vecs, groups=("klein",))
assert len(v.certs) == 2, v.certs
pts = ball(vecs, 2, 2.05)
E = edges_grid(pts)
L, xy = v.lattice, [pt_float(p) for p in pts]

cols = []
for cert in v.certs:
    bad, colour = verify_on_ball(cert, L, pts, E)
    assert not bad, f"{len(bad)} monochromatic edges"
    cols.append([colour[i] for i in range(len(pts))])
print(f"  {len(pts)} points, {len(E)} edges, 0 monochromatic in each colouring")

# the conjugation that swaps the two primes swaps the two pictures, on the nose
conj = [p.conj(1) for p in pts]                     # bit 0 is sqrt3, so sqrt33 flips
assert all(L.coords(q) is not None for q in conj)
assert cols[0] == [apply_colouring(v.certs[1], L.coords(q)) for q in conj]
print("  conjugation carries one colouring onto the other, colour for colour")

# Four glyphs rather than four colours, so the figure survives a grey print.
# The unit edges are left out: at 1920 of them in this span they are a wash that
# hides the very pattern the figure is for, and the colouring is checked against
# them in code instead.
STYLE = [dict(marker="o", ms=2.0, mfc="black", mec="black", mew=0),
         dict(marker="o", ms=2.2, mfc="white", mec="black", mew=0.45),
         dict(marker="s", ms=1.8, mfc="black", mec="black", mew=0),
         dict(marker="s", ms=2.1, mfc="white", mec="black", mew=0.45)]

W = TEXTWIDTH
fig = plt.figure(figsize=(W, W / 2.06))
r = max(max(abs(p[0]), abs(p[1])) for p in xy) * 1.045
for k, colour in enumerate(cols):
    ax = fig.add_axes([0.5 * k, 0.0, 0.5, 1.0])
    ax.set_aspect("equal"); ax.axis("off")
    for c in range(4):
        sel = [xy[i] for i in range(len(xy)) if colour[i] == c]
        ax.plot([p[0] for p in sel], [p[1] for p in sel], linestyle="none",
                zorder=3 + (c == 1 or c == 3), **STYLE[c])
    ax.set_xlim(-r, r); ax.set_ylim(-r, r)
save(fig, "colourings")
