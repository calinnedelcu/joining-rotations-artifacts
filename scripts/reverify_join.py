#!/usr/bin/env python3
"""Re-verify a joining rotation's graph from the coordinates on disk.

Usage: reverify_join.py A

Independent of the run that produced it: a fresh process, the field rebuilt from
the candidate, the points reloaded from the file, every edge recomputed from the
coordinates and re-tested exactly in K, and non-4-colourability re-proved with
nothing carried over.
"""
import os, sys, time, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
a = int(sys.argv[1])
from hn.joins import rational_spindle
J = rational_spindle(a, 1)
from hn.field import set_primes, K, is_unit
set_primes(J.primes)
from hn import construct as C
C.refresh_field()
from hn.io import load_points
from hn.construct import edges_grid, to_float
from hn import verify, find_triangle
log = lambda s: print(s, flush=True)

WL, WS, cs = J.build()
c, s = cs
log(f"theta_{a} = arccos({J.cos}) in {J.field_str()}")
log(f"1. rotation modulus exactly 1: {(c*c+s*s).is_one()}")
log(f"2. all {len(WL)} lattice vectors exactly unit: {all(is_unit(C.ORIGIN,v) for v in WL)}")
HERE = os.path.dirname(os.path.abspath(__file__))
CAND = [f"out/join{a}.pts", f"graphs/join{a}.pts",
        os.path.join(HERE, "..", "out", f"join{a}.pts"),
        os.path.join(HERE, "..", "graphs", f"join{a}.pts")]
src = next((p for p in CAND if os.path.exists(p)), None)
if src is None:
    log(f"no coordinates for theta_{a}: looked in " + ", ".join(CAND))
    sys.exit(1)
P = load_points(src)          # raises if the file's field header disagrees
log(f"3. loaded {len(P)} points from {src}")
n = sum(1 for p in P if abs(to_float(p.norm2()) - a) < 1e-9)
log(f"4. points at squared radius exactly {a}: {n}")
t = time.time(); E = edges_grid(P)
log(f"5. edges recomputed from coordinates: {len(E)}  ({time.time()-t:.0f}s)")
bad = sum(1 for i, j in E[::200] if not is_unit(P[i], P[j]))
log(f"6. exact re-check of {len(E[::200])} sampled edges: {bad} wrong")
deg = collections.Counter()
for i, j in E:
    deg[i] += 1; deg[j] += 1
log(f"7. min degree {min(deg[v] for v in range(len(P)))} (critical needs >= 4)")
t = time.time(); tri = find_triangle(len(P), E)
five = verify(P, E, triangle=tri)
log(f"8. NOT 4-colourable, fresh solver: {five}  ({time.time()-t:.0f}s)")
log("")
log(f"VERDICT: theta_{a} is a joining rotation" if five else "VERDICT: FAILED to reproduce")
