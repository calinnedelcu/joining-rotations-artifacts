#!/usr/bin/env python3
"""Rotate about a point that is NOT a lattice point.

Usage: sweep_offlattice.py [BALL_RADIUS] [HOW_MANY]

Route 19 swept the rotation centre over lattice points and found twenty that
work. But the centre does not have to be a lattice point: any point of the
field will do, and the field is dense. Midpoints of edges, centroids of
triangles, and thirds along an edge are all in the field and none of them is in
the lattice.

The trade is explicit. A lattice centre is shared by the two parts, so the
total is |L| + |S| - 1; an off-lattice centre is in neither, so the total is
|L| + |S|, one vertex worse. Everything else about the geometry changes, and
the twenty lattice centres already showed how much that can matter: four of
them reach 5-chromaticity from a pool a third smaller than the origin needs.
"""
import os, sys, time, itertools
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.field import K, Pt
from hn.construct import (unit_vector_family, ball, dedup, edges, rotate, norm,
                          ROT, ORIGIN)
from hn import verify, find_triangle

T4 = ROT["theta4"]
W30, W18 = unit_vector_family(2), unit_vector_family(1)
r = float(sys.argv[1]) if len(sys.argv) > 1 else 2.0
howmany = int(sys.argv[2]) if len(sys.argv) > 2 else 40
VL = ball(W30, 3, r)
VS = ball(W18, 3, r)
n = len(VL)
seed = ball(W30, 2, 1.2)
half, third, twothird, cent = K.rat(1, 2), K.rat(1, 3), K.rat(2, 3), K.rat(1, 3)
cands, seen = [], set()
for p in seed:
    for lab, q in (("midpoint", Pt(p.x * half, p.y * half)),
                   ("third", Pt(p.x * third, p.y * third)),
                   ("two thirds", Pt(p.x * twothird, p.y * twothird))):
        if q.key() in seen or norm(q) < 1e-9 or norm(q) > 1.3:
            continue
        seen.add(q.key())
        cands.append((lab, q))
latt = {p.key() for p in ball(W30, 3, 2.2)}
cands = [(l, q) for l, q in cands if q.key() not in latt]
cands.sort(key=lambda lq: norm(lq[1]))
print(f"{len(cands)} off-lattice centres; testing the nearest {howmany}; "
      f"pool is {n} + {len(VS)}", flush=True)
hits = 0
for lab, c in cands[:howmany]:
    U = dedup(VL + [c + rotate(p - c, T4) for p in VS])
    E = edges(U)
    cross = sum(1 for a, b in E if (a < n) != (b < n))
    if cross <= len(W30):
        continue
    tri = find_triangle(len(U), E)
    if tri and verify(U, E, triangle=tri):
        hits += 1
        print(f"   *** 5-CHROMATIC: {lab} centre at radius {norm(c):.4f}, "
              f"union {len(U)} vertices, {cross} cross edges", flush=True)
print(f"{hits} off-lattice centres give a 5-chromatic union", flush=True)
