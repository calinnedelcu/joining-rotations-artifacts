#!/bin/sh
cd "$(dirname "$0")/.."
.venv/bin/python -u - > out/join28_verify.log 2>&1 <<'PYEOF'
import sys, time, collections; sys.path.insert(0,'.')
from hn.field import set_primes, K, is_unit
set_primes((3,11,37))
from hn import construct as C; C.refresh_field()
from hn.io import load_points
from hn.construct import edges_grid, rotate, unit_vector_family, to_float
from hn.joins import rational_spindle
from hn import verify, find_triangle
log=lambda s: print(s, flush=True)

J = rational_spindle(28,1); WL,WS,cs = J.build()
c,s = cs
log(f"1. rotation modulus exactly 1: {(c*c+s*s).is_one()}")
log(f"2. all {len(WL)} lattice vectors exactly unit: "
    f"{all(is_unit(C.ORIGIN,v) for v in WL)}")
P = load_points('out/join28.pts')
log(f"3. loaded {len(P)} points from disk")
n28 = sum(1 for p in P if (p.norm2()-K.rat(28)).is_zero()) if hasattr(K.rat(28),'is_zero') else \
      sum(1 for p in P if abs(to_float(p.norm2())-28)<1e-9)
log(f"4. points at squared radius exactly 28: {n28}")
t=time.time(); E = edges_grid(P)
log(f"5. edges recomputed from coordinates: {len(E)}  ({time.time()-t:.0f}s)")
bad = sum(1 for i,j in E[::200] if not is_unit(P[i],P[j]))
log(f"6. exact re-check of {len(E[::200])} sampled edges: {bad} wrong")
deg = collections.Counter()
for i,j in E: deg[i]+=1; deg[j]+=1
log(f"7. min degree {min(deg[v] for v in range(len(P)))} (a critical 5-chromatic graph needs >= 4)")
t=time.time(); tri = find_triangle(len(P), E)
five = verify(P, E, triangle=tri)
log(f"8. NOT 4-colourable, fresh solver: {five}  ({time.time()-t:.0f}s)")
log("")
log("VERDICT: theta_28 is a joining rotation" if five else "VERDICT: FAILED to reproduce")
PYEOF
wait
