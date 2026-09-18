#!/usr/bin/env python3
"""Rebuild theta_16's union from nothing and re-verify it, then keep the points.

The paper prints 29113 for theta_16 and docs/ATTEMPTS.md records the check, but
the coordinates were never kept -- only the minimised 2901.  This rebuilds the
union from the recipe in that file (Q(sqrt3, sqrt7, sqrt11), the 30-vector
lattice, ball of depth 4 and radius 4.0, glued to its own theta_16 image at the
origin), re-verifies it in a fresh process, and writes out/join16.pts so the size
the paper prints can be checked against coordinates on disk like the others.

Usage: .venv/bin/python scripts/build_join16.py
"""
import os, sys, time, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.joins import rational_spindle
J = rational_spindle(16, 1)
from hn.field import set_primes, K, is_unit
from hn import construct as C
from hn.io import save_points
from hn import verify, find_triangle
log = lambda s: print(s, flush=True)

WL, WS, cs = J.build()
c, s = cs
log(f"theta_16 = arccos({J.cos}) in {J.field_str()}")
log(f"1. rotation modulus exactly 1: {(c*c+s*s).is_one()}")
log(f"2. all {len(WL)} lattice vectors exactly unit: "
    f"{all(is_unit(C.ORIGIN, v) for v in WL)}")
t = time.time()
L = C.ball(WL, 4, 4.0)
log(f"3. ball depth 4 radius 4.0: {len(L)} points  ({time.time()-t:.0f}s)")
n = sum(1 for p in L if abs(C.to_float(p.norm2()) - 16) < 1e-9)
log(f"4. shell points at squared radius exactly 16: {n}")
P = C.dedup(list(L) + [C.rotate(p, cs) for p in L])
log(f"5. union L u theta_16(L): {len(P)} distinct points")
t = time.time(); E = C.edges_grid(P)
log(f"6. edges recomputed from coordinates: {len(E)}  ({time.time()-t:.0f}s)")
bad = sum(1 for i, j in E[::70] if not is_unit(P[i], P[j]))
log(f"7. exact re-check of {len(E[::70])} sampled edges: {bad} wrong")
deg = collections.Counter()
for i, j in E:
    deg[i] += 1; deg[j] += 1
log(f"8. min degree {min(deg[v] for v in range(len(P)))} (critical needs >= 4)")
t = time.time(); tri = find_triangle(len(P), E)
five = verify(P, E, triangle=tri)
log(f"9. NOT 4-colourable, fresh solver: {five}  ({time.time()-t:.0f}s)")
if five:
    save_points("out/join16.pts", P)
    log(f"10. written to out/join16.pts ({len(P)} points)")
log("")
log("VERDICT: theta_16 rebuilt and re-verified" if five else "VERDICT: FAILED")
