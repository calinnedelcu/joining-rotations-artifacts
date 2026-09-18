#!/usr/bin/env python3
"""theta_2 on Haugland's lattice: a rotation nobody has had, where the test bites.

theta_4's shell sits at radius 2, an even integer, so the joining criterion
passes for free on any lattice and says nothing -- that is what closed the cheap
route to de Grey's question.  The rotations with content are those whose shell
radius is not an even integer.

Haugland's lattice has shells at squared radius 1, 2, 3 and 4.  Radius sqrt2 and
sqrt3 are irrational, so the spindles there are the informative ones:

    theta_2:  cos = 3/4,  sin = sqrt7 / 4    -- sqrt7 IS in Q(zeta_420), since
                                                7 divides 420 and i is present
    theta_3:  cos = 5/6,  sin = sqrt11 / 6   -- sqrt11 is NOT: 11 does not divide 420

So theta_2 is the one to test.  docs/ATTEMPTS.md route 18 records that theta_2
"has never been available to anyone working on this problem", because the
classical field Q(sqrt3, sqrt5, sqrt11) does not contain sqrt7.
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

# sqrt7 from the quadratic Gauss sum of 7: it gives sqrt(-7), and i is in the field
g7 = CY.gauss_sum(7)
i_unit = z(105)
r7 = g7 * i_unit * Cyc.rat(-1)
log(f"sqrt7 squares to 7: {(r7 * r7 - Cyc.rat(7)).is_zero()}")
t2 = Cyc.rat(3, 4) + i_unit * r7 * Cyc.rat(1, 4)
log(f"theta_2 = 3/4 + i sqrt7/4 has modulus exactly 1: {(t2 * t2.conj()).is_one()}")
log("")

sets = int(sys.argv[1]) if len(sys.argv) > 1 else 2
gens = []
for s in range(sets):
    rk = Cyc.rat(1)
    for _ in range(s):
        rk = rk * rho
    for j in range(42):
        gens.append(rk * z(10 * j))
gens = dedup(gens)
t = time.time()
L = CycLattice(dedup(gens + [t2 * g for g in gens]))
log(f"{sets} set(s) joined by theta_2: rank {L.rank}, den {L.den}  "
    f"({time.time()-t:.0f}s to build)")
t = time.time()
U = L.unit_vectors()
inhalf = sum(1 for c, _ in U if all(x % 2 == 0 for x in c))
log(f"  unit vectors: {len(U)}, of which {inhalf} lie in 2*Lambda  "
    f"({time.time()-t:.0f}s)")
log("  -> " + ("SURVIVES: no Klein homomorphism can 4-colour it -- a genuine candidate"
               if inhalf else
               "no half-unit vector: the full certificate search would decide"))

# rank 12 makes the full certificate search cheap: 2^12 functionals, not 2^24
from hn.algcolour import klein_colourings, z4_colourings
co = [c for c, _ in U]
t = time.time()
nk = len(klein_colourings(co, L.rank))
nz = len(z4_colourings(co, L.rank))
log("")
log(f"FULL certificate search at rank {L.rank}: klein {nk}, z4 {nz}  "
    f"({time.time()-t:.0f}s)")
log("VERDICT: " + ("DEAD -- the whole infinite lattice is 4-colourable, so no "
                  "subset of it is 5-chromatic, at any size, forever"
                  if (nk or nz) else
                  "SURVIVES -- theta_2 is a genuine candidate on this lattice"))
