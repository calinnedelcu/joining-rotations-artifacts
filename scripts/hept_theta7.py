#!/usr/bin/env python3
"""The verdict for theta_7 and theta_9 on Haugland's lattice, without the shell.

By Proposition (cyclotomic rank), theta_7 has 4N-1 = 27 = 3*3^2, so it lies in
Q(zeta_42) and the join stays at rank 12 -- the cheap case.  theta_9 has
4N-1 = 35, neither 3k^2 nor 7k^2, so its join is rank 24.

The shell is a separate question and is not touched here: a verdict is about the
joint lattice, and the shell only says whether the rotation has points to move.
"""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import hn.cyclo as CY
from hn.cyclo import Cyc, dedup
from hn.cyclolat import CycLattice
from hn.algcolour import klein_colourings, z4_colourings

CY.set_conductor(420)
z = Cyc.zeta
i_u = z(105)
r3 = z(35) + z(-35)
gens = dedup([z(10 * j) for j in range(42)])

ROOTS = {3: r3}
g7 = CY.gauss_sum(7)
ROOTS[7] = g7 * i_u * Cyc.rat(-1)       # 7 = 3 mod 4


def theta(N, m, k):
    """theta_N with 4N-1 = m*k^2."""
    return Cyc.rat(2 * N - 1, 2 * N) + i_u * (ROOTS[m] * Cyc.rat(k, 2 * N))


def main():
    L0 = CycLattice(gens)
    print(f"base lattice: rank {L0.rank}, den {L0.den}", flush=True)
    for N, m, k in ((7, 3, 3),):
        th = theta(N, m, k)
        assert (th * th.conj()).is_one(), "not a rotation"
        t = time.time()
        L = CycLattice(dedup(gens + [th * g for g in gens]))
        print(f"\ntheta_{N}: joint rank {L.rank}, den {L.den}  "
              f"({time.time()-t:.0f}s)", flush=True)
        t = time.time()
        U = L.unit_vectors()
        print(f"  unit vectors: {len(U)}  ({time.time()-t:.0f}s)", flush=True)
        co = [c for c, _ in U]
        nh = sum(1 for c, _ in U if all(x % 2 == 0 for x in c))
        print(f"  half-unit vectors: {nh}", flush=True)
        if nh:
            print("  -> SURVIVES by the free-pass proposition", flush=True)
            continue
        nk = len(klein_colourings(co, L.rank, 1))
        nz = len(z4_colourings(co, L.rank, 1)) if not nk else 0
        verdict = "dead" if (nk or nz) else "SURVIVES"
        print(f"  klein {nk}, z4 {nz}  ->  {verdict}", flush=True)


if __name__ == "__main__":
    main()
