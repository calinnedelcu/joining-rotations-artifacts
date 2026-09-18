#!/usr/bin/env python3
"""How the joint lattice's rank grows with the number of 42-vector sets.

The trace-form enumeration is a Fincke-Pohst search in that many dimensions, so
the rank decides whether de Grey's question is answerable at all.

The rank does not grow -- 12 for one set and for four, 24 joined either way.
What does change is the covolume, and this reports it too: relative to one set it
is 1, 1/7, 1/49, 1/343, so each extra set makes the lattice seven times finer.
That is why de Grey's suggestion is not cosmetic, and it is the claim the paper
makes on his behalf, so it is measured here rather than quoted.
"""
import os, sys, time
from fractions import Fraction
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import hn.cyclo as CY
from hn.cyclo import Cyc, dedup, gauss_sum
from hn.cyclolat import CycLattice
log = lambda s: print(s, flush=True)

CY.set_conductor(420)
z = Cyc.zeta
half = Cyc.rat(1, 2)
r3 = z(35) + z(-35)
cpi7 = (z(30) + z(-30)) * half
s2p7 = (z(60) - z(-60)) * (half * z(-105))
rho = ((Cyc.zero() - r3) + z(105) * (cpi7 * Cyc.rat(4) - Cyc.rat(1))) \
      * (s2p7 * Cyc.rat(4)).inv() * z(-140)
t4 = Cyc.rat(7, 8) + z(105) * (r3 * gauss_sum(5)) * Cyc.rat(1, 8)

for sets in (1, 2, 3, 4):
    gens = []
    for s in range(sets):
        rk = Cyc.rat(1)
        for _ in range(s):
            rk = rk * rho
        for j in range(42):
            gens.append(rk * z(10 * j))
    gens = dedup(gens)
    t = time.time()
    plain = CycLattice(gens)
    joint = CycLattice(dedup(gens + [t4 * g for g in gens]))
    piv = 1
    for row in plain.basis:
        piv *= row[next(j for j in range(len(row)) if row[j])]
    cov = Fraction(abs(piv), plain.den ** plain.rank)
    if sets == 1:
        cov0 = cov
    log(f"{sets} set(s): lattice rank {plain.rank}, joined by theta_4 rank "
        f"{joint.rank}, den {joint.den}, covolume {cov / cov0} of one set's"
        f"   ({time.time()-t:.0f}s)")
    assert cov / cov0 == Fraction(1, 7 ** (sets - 1)), "seven times finer per set"
