#!/usr/bin/env python3
"""The cheap half of the criterion on Haugland's lattice.

A unit vector lying in 2*Lambda kills every Klein homomorphism -- that is the
proved half of the divisibility theorem, and it costs O(|U|) rather than the
O(2^rank) of the full certificate search, which is hopeless at rank 24.
"""
import os, sys, time
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

for sets in [int(x) for x in (sys.argv[1:] or ["1", "2"])]:
    gens = []
    for s in range(sets):
        rk = Cyc.rat(1)
        for _ in range(s):
            rk = rk * rho
        for j in range(42):
            gens.append(rk * z(10 * j))
    gens = dedup(gens)
    t = time.time()
    L = CycLattice(dedup(gens + [t4 * g for g in gens]))
    U = L.unit_vectors()
    inhalf = sum(1 for c, _ in U if all(x % 2 == 0 for x in c))
    log(f"{sets} set(s) joined by theta_4: rank {L.rank}, den {L.den}, "
        f"{len(U)} unit vectors, {inhalf} of them in 2*Lambda  "
        f"({time.time()-t:.0f}s)")
    log("   -> " + ("SURVIVES: no Klein homomorphism can 4-colour it"
                    if inhalf else
                    "no half-unit vector -- the full search would decide"))
