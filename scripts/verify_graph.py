#!/usr/bin/env python3
"""Independent check of a claimed 5-chromatic unit-distance graph.

Usage: verify_graph.py FILE.pts|FILE.vtx [--slow]

Reads the points, recomputes every unit-distance pair EXACTLY in
Q(sqrt3, sqrt5, sqrt11), then asks a fresh SAT solver -- no selector
literals, no assumptions -- whether the graph is 4-colourable.  With
--slow it also omits the triangle colour pinning (78 s instead of 2 s on the
510 graph).  Also reports 5-colourability, minimum degree, and whether the
graph is vertex-critical (every single deletion 4-colourable), which a
minimum graph must be.  Exit status 0 iff chi = 5.
"""
import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn import load_vtx, verify, find_triangle
from hn.io import load_points
from hn.construct import edges, split_parts
from hn.graph import degrees
from hn.hitting import Oracle

path = sys.argv[1]
slow = "--slow" in sys.argv
P = load_points(path) if path.endswith(".pts") else load_vtx(path)
assert len({p.key() for p in P}) == len(P), "duplicate points"
E = edges(P)
d = degrees(len(P), E)
L, S = split_parts(P)
print(f"{len(P)} distinct points, {len(E)} exact unit edges, min degree {min(d)}, "
      f"sqrt5-free part {len(L)}, rotated part {len(S)}")
tri = None if slow else find_triangle(len(P), E)
t = time.time()
five = verify(P, E, triangle=tri)
print(f"not 4-colourable: {five}  ({time.time()-t:.1f}s{', no symmetry breaking' if slow else ''})")
print(f"5-colourable: {not verify(P, E, k=5)}")
if five:
    o = Oracle(len(P), E, triangle=find_triangle(len(P), E))
    crit = all(o.colourable([u for u in range(len(P)) if u != v]) for v in range(len(P)))
    o.close()
    print(f"vertex-critical: {crit}")
    print(f"RESULT: chi = 5 with {len(P)} vertices and {len(E)} edges" +
          ("   <-- BELOW THE 509 RECORD" if len(P) < 509 else ""))
sys.exit(0 if five else 1)
