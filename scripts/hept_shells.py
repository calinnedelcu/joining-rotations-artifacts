#!/usr/bin/env python3
"""Which shells does Haugland's lattice have, and which rotations can spin them?

A spindle at squared radius N acts only on the points at that radius, and the
joining criterion is vacuous whenever sqrt(N) is an even integer -- theta_4's
shell is at radius 2, which is why it passes for free here.  The rotations with
content are the ones whose shell radius is odd or irrational, so the first thing
to know is which shells this lattice actually has.
"""
import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import hn.cyclo as CY
from hn.cyclo import Cyc, dedup
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

sets = int(sys.argv[1]) if len(sys.argv) > 1 else 2
hi = int(sys.argv[2]) if len(sys.argv) > 2 else 10
gens = []
for s in range(sets):
    rk = Cyc.rat(1)
    for _ in range(s):
        rk = rk * rho
    for j in range(42):
        gens.append(rk * z(10 * j))
L = CycLattice(dedup(gens))
log(f"Haugland lattice, {sets} set(s): rank {L.rank}, den {L.den}")
log("")
for N in range(1, hi + 1):
    t = time.time()
    sh = L.shell(N)
    r = N ** 0.5
    tag = "   <- even integer radius: the criterion is vacuous here" \
        if abs(r - round(r)) < 1e-12 and round(r) % 2 == 0 else ""
    log(f"  N={N:3d} (radius {r:.4f}): {len(sh):5d} points  "
        f"({time.time()-t:.0f}s){tag}")
