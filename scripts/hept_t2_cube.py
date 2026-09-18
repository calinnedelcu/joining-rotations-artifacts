#!/usr/bin/env python3
"""theta_2 on Haugland's lattice, decided by cube and conquer.

Plain SAT grinds on these instances -- 3193 points and 13440 edges defeated it
for a quarter of an hour -- while cube and conquer settled the same size in 520
seconds yesterday.  Small graphs that are hard for SAT sit near a phase
boundary, which is exactly where the interesting answer lives.
"""
import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import hn.cyclo as CY
from hn.cyclo import Cyc, dedup, ball, edges
from hn.cubes import cube_colourable
log = lambda s: print(s, flush=True)

CY.set_conductor(420)
z = Cyc.zeta
half = Cyc.rat(1, 2)
i_u = z(105)
r3 = z(35) + z(-35)
cpi7 = (z(30) + z(-30)) * half
s2p7 = (z(60) - z(-60)) * (half * z(-105))
rho = ((Cyc.zero() - r3) + i_u * (cpi7 * Cyc.rat(4) - Cyc.rat(1))) \
      * (s2p7 * Cyc.rat(4)).inv() * z(-140)
r7 = CY.gauss_sum(7) * i_u * Cyc.rat(-1)
t2 = Cyc.rat(3, 4) + i_u * r7 * Cyc.rat(1, 4)

depth = int(sys.argv[1]); radius = float(sys.argv[2]); sets = int(sys.argv[3])
split = int(sys.argv[4]) if len(sys.argv) > 4 else 8
gens = []
for s in range(sets):
    rk = Cyc.rat(1)
    for _ in range(s):
        rk = rk * rho
    gens += [rk * z(10 * j) for j in range(42)]
gens = dedup(gens)
V = ball(gens, depth, radius)
U = dedup(list(V) + [t2 * p for p in V])
E = edges(U)
log(f"{sets} set(s), depth {depth}, radius {radius}: union {len(U)} points, "
    f"{len(E)} edges")
t = time.time()
col = cube_colourable(len(U), E, split=split, procs=8, log=log)
log(f"4-colourable: {col}   ({time.time()-t:.0f}s)")
log("VERDICT: " + ("not 5-chromatic" if col else
                   "5-CHROMATIC -- a construction with theta_2"))
