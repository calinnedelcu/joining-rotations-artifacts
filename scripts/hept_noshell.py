#!/usr/bin/env python3
"""The heptagonal verdicts for N = 7, 9, 16, without enumerating the shell.

scripts/hept_classify.py computes the shell at squared radius N before anything
else, and that is the wall: Fincke-Pohst in twelve dimensions whose cost grows
like the sixth power of the target, so N = 7 never finishes.

The shell is not needed for the verdict.  A verdict is a statement about the
joint lattice -- whether it admits a homomorphism onto a four-element group
killing no unit vector -- and the shell only says whether the rotation has
anything to act on.  So the two questions separate, and this script answers the
one that is reachable, reporting the other as open.

N = 16 needs nothing at all: its shell radius is 4, so a = 4m^2 with m = 2 and
the free-pass proposition applies.

Run: .venv/bin/python scripts/hept_noshell.py
"""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import hn.cyclo as CY
from hn.cyclo import Cyc, dedup
from hn.cyclolat import CycLattice
from hn.algcolour import klein_colourings, z4_colourings


def squarefree_part(n):
    """The squarefree part of n.  Dividing out d*d and multiplying s by d is
    WRONG for a prime at odd power >= 3: it sends 27 to 9 and 63 to 21, which is
    exactly 4N-1 for N = 7 and N = 16, so those two rotations get rejected as
    absent from the field when sqrt27 = 3 sqrt3 and sqrt63 = 3 sqrt7 are both in
    it.  Count the exponent parity instead, as hn.joins does."""
    s, d = 1, 2
    while d * d <= n:
        e = 0
        while n % d == 0:
            n //= d
            e += 1
        if e % 2:
            s *= d
        d += 1
    return s * n


CY.set_conductor(420)
z = Cyc.zeta
half = Cyc.rat(1, 2)
i_u = z(105)
r3 = z(35) + z(-35)

ROOTS = {1: Cyc.rat(1), 3: r3}
for p in (5, 7):
    g = CY.gauss_sum(p)
    ROOTS[p] = g if p % 4 == 1 else g * i_u * Cyc.rat(-1)
for a in (3, 5, 7):
    for b in (5, 7):
        if a < b:
            ROOTS[a * b] = ROOTS[a] * ROOTS[b]
ROOTS[105] = ROOTS[3] * ROOTS[5] * ROOTS[7]
for m, r in list(ROOTS.items()):
    assert (r * r - Cyc.rat(m)).is_zero(), f"sqrt{m} is wrong"

gens = dedup([z(10 * j) for j in range(42)])
L0 = CycLattice(gens)
print(f"Haugland lattice, 1 set: rank {L0.rank}")
print(f"{'N':>4} {'sqrt(4N-1)':>11} {'rank':>5} {'units':>6} {'half':>5} "
      f"{'klein':>6} {'z4':>4}  verdict")

for N in (7, 9, 16):
    t = time.time()
    rr = N ** 0.5
    if abs(rr - round(rr)) < 1e-12 and round(rr) % 2 == 0:
        print(f"{N:4d} {'--':>11} {'--':>5} {'--':>6} {'--':>5} {'--':>6} {'--':>4}"
              f"  SURVIVES free (radius {round(rr)} even, a = 4m^2)")
        continue
    m = squarefree_part(4 * N - 1)
    k = round(((4 * N - 1) // m) ** 0.5)
    if m not in ROOTS or k * k * m != 4 * N - 1:
        print(f"{N:4d} {('sqrt' + str(m)):>11}   not in Q(zeta_420)")
        continue
    th = Cyc.rat(2 * N - 1, 2 * N) + i_u * (ROOTS[m] * Cyc.rat(k, 2 * N))
    assert (th * th.conj()).is_one(), "not a rotation"
    L = CycLattice(dedup(gens + [th * g for g in gens]))
    U = L.unit_vectors()
    co = [c for c, _ in U]
    nh = sum(1 for c, _ in U if all(x % 2 == 0 for x in c))
    if nh:
        nk = nz = 0
        verdict = "SURVIVES (half-unit vector)"
    elif L.rank <= 16:
        nk = len(klein_colourings(co, L.rank, 1))
        nz = len(z4_colourings(co, L.rank, 1)) if not nk else 0
        verdict = "dead" if (nk or nz) else "SURVIVES"
    else:
        nk = nz = -1
        verdict = f"certificate search skipped, rank {L.rank} too large"
    print(f"{N:4d} {('sqrt' + str(m)):>11} {L.rank:5d} {len(U):6d} {nh:5d} "
          f"{nk:6d} {nz:4d}  {verdict}   ({time.time()-t:.0f}s)")

print("\nThe shell is a separate question and is NOT answered here.")
