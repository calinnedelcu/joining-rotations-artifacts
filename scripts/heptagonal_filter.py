#!/usr/bin/env python3
"""The joining criterion, applied to Haugland's heptagonal lattice.

de Grey asked (Polymath16 thread 18, 13 Sep 2026) for someone to explore
Haugland's construction as a route past 509, "using more than just two sets of
42 vectors".  Everyone's approach, ours included, has been to build sets and run
SAT for hours.  This asks the decidable question instead: can the joint lattice
be 4-coloured by a homomorphism?  If it can, no subset of it is 5-chromatic, at
any size, forever -- and that closes the direction.

Runs because Haugland's lattice has Q-rank 12, not the 96 its field suggests.
"""
import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import hn.cyclo as CY
from hn.cyclo import Cyc, dedup, gauss_sum
from hn.cyclolat import CycLattice
from hn.algcolour import klein_colourings, z4_colourings
log = lambda s: print(s, flush=True)

CY.set_conductor(420)
z = Cyc.zeta
half = Cyc.rat(1, 2)
r3 = z(35) + z(-35)
cpi7 = (z(30) + z(-30)) * half
s2p7 = (z(60) - z(-60)) * (half * z(-105))
rho = ((Cyc.zero() - r3) + z(105) * (cpi7 * Cyc.rat(4) - Cyc.rat(1))) \
      * (s2p7 * Cyc.rat(4)).inv() * z(-140)
r5 = gauss_sum(5)
t4 = Cyc.rat(7, 8) + z(105) * (r3 * r5) * Cyc.rat(1, 8)
log(f"rho modulus exactly 1: {(rho * rho.conj()).is_one()}")
log(f"theta_4 modulus exactly 1: {(t4 * t4.conj()).is_one()}")
log("")

for sets in [int(x) for x in (sys.argv[1:] or ["1", "2", "3"])]:
    gens = []
    for s in range(sets):
        rk = Cyc.rat(1)
        for _ in range(s):
            rk = rk * rho
        for j in range(42):
            gens.append(rk * z(10 * j))
    gens = dedup(gens)
    joint = dedup(gens + [t4 * g for g in gens])
    t = time.time()
    L = CycLattice(joint)
    log(f"{sets} set(s) joined by theta_4: rank {L.rank}, den {L.den}"
        f"  ({time.time()-t:.0f}s to build)")
    t = time.time()
    U = L.unit_vectors()
    log(f"   unit vectors: {len(U)}  ({time.time()-t:.0f}s)")
    co = [c for c, _ in U]
    t = time.time()
    nk = len(klein_colourings(co, L.rank, 1))
    nz = len(z4_colourings(co, L.rank, 1)) if not nk else 0
    log(f"   klein {nk}, z4 {nz}  ->  "
        + ("DEAD: 4-colourable forever, no subset is 5-chromatic"
           if (nk or nz) else "SURVIVES -- a genuine candidate")
        + f"  ({time.time()-t:.0f}s)")
