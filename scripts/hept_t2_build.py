#!/usr/bin/env python3
"""Build L union theta_2(L) on Haugland's lattice and ask whether it is 5-chromatic.

theta_2 passes the joining criterion here non-trivially: no half-unit vector, and
a full certificate search at rank 12 returns nothing.  So it is a candidate, and
the criterion has done all it can.  This is the other half.

theta_2 = 3/4 + i sqrt7/4 needs sqrt7, which the classical field Q(sqrt3, sqrt5,
sqrt11) does not contain -- docs/ATTEMPTS.md route 18 records that it "has never
been available to anyone working on this problem".
"""
import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import hn.cyclo as CY
from hn.cyclo import Cyc, dedup, ball, edges
from hn.sat import find_triangle
from hn.minimise import verify
from hn.io import save_points, save_edges
log = lambda s: print(s, flush=True)

CY.set_conductor(420)
z = Cyc.zeta
i_unit = z(105)
r7 = CY.gauss_sum(7) * i_unit * Cyc.rat(-1)
t2 = Cyc.rat(3, 4) + i_unit * r7 * Cyc.rat(1, 4)
assert (t2 * t2.conj()).is_one()

depth = int(sys.argv[1]) if len(sys.argv) > 1 else 2
radius = float(sys.argv[2]) if len(sys.argv) > 2 else 1.6
sets = int(sys.argv[3]) if len(sys.argv) > 3 else 1
half = Cyc.rat(1, 2)
r3c = z(35) + z(-35)
cpi7 = (z(30) + z(-30)) * half
s2p7 = (z(60) - z(-60)) * (half * z(-105))
rho = ((Cyc.zero() - r3c) + z(105) * (cpi7 * Cyc.rat(4) - Cyc.rat(1))) \
      * (s2p7 * Cyc.rat(4)).inv() * z(-140)
gens = []
for _s in range(sets):
    rk = Cyc.rat(1)
    for _ in range(_s):
        rk = rk * rho
    gens += [rk * z(10 * j) for j in range(42)]
gens = dedup(gens)
log(f"{sets} set(s) of 42 -> {len(gens)} generators")
t = time.time()
V = ball(gens, depth, radius)
log(f"ball depth {depth} radius {radius}: {len(V)} points  ({time.time()-t:.0f}s)")
U = dedup(list(V) + [t2 * p for p in V])
log(f"union with theta_2: {len(U)} points")
t = time.time()
E = edges(U)
log(f"{len(E)} edges  ({time.time()-t:.0f}s)")
t = time.time()
tri = find_triangle(len(U), E)
five = verify(U, E, triangle=tri) if tri else None
log(f"chi >= 5: {five}  ({time.time()-t:.0f}s)"
    + ("   <<< A 5-CHROMATIC CONSTRUCTION WITH theta_2" if five else ""))
if five:
    out = os.path.join(os.path.dirname(__file__), "..", "out")
    save_points(f"{out}/hept_t2_s{sets}d{depth}.pts", U)
    save_edges(f"{out}/hept_t2_s{sets}d{depth}.edge", len(U), E)
    log(f"saved out/hept_t2_s{sets}d{depth}.pts")
