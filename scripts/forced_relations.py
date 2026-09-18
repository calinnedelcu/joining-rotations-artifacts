#!/usr/bin/env python3
"""Every colour relation the lattice forces between the origin and a point.

Usage: forced_relations.py [DEPTH] [RADIUS]        (default 3 2.2)

Pin the origin to colour 0 and, for every other point q of a lattice ball,
ask the solver twice:

    col(q) = 0 impossible  ->  q must DIFFER from the origin: a VIRTUAL EDGE
    col(q) = 1 impossible  ->  q must AGREE  with the origin: a MONO-PAIR

Why mono-pairs are worth hunting.  If a graph G forces col(q) = col(O) with
|Oq| = sqrt(i), then glue G to theta_i(G) at O, where theta_i is the rotation
with cos = (2i-1)/(2i).  The points q and theta_i(q) are then exactly 1 apart
and both forced to the colour of O, so the union is 5-chromatic -- with
2|G| - 1 vertices, because the two copies share only O.  Anything under 255
vertices would beat the record outright.

Parts tabulated mono-pairs only at distances 8/3 and 8/sqrt3, and neither can
be spindled here: the rotations they need have sin proportional to sqrt247
and sqrt759, which leave Q(sqrt3,sqrt5,sqrt11).  The distances sqrt(i), where
the rotation does stay in the field, were never scanned.

Measured (ball depth 3, radius 2.2, 2263 points): ZERO mono-pairs, and 90
virtual edges, at distances 1, 5/3, 1.5642, 1.8264 and sqrt11/2 = 1.9149.
"""
import os, sys, time, collections, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.construct import unit_vector_family, ball, edges, norm, ORIGIN
from hn.sat import Colouring

SQFREE = (1, 3, 5, 11, 15, 33, 55, 165)
depth = int(sys.argv[1]) if len(sys.argv) > 1 else 3
radius = float(sys.argv[2]) if len(sys.argv) > 2 else 2.2
V = ball(unit_vector_family(2), depth, radius)
o = next(i for i, p in enumerate(V) if p.key() == ORIGIN.key())
E = edges(V)
print(f"ball depth {depth} radius {radius}: {len(V)} points, {len(E)} edges", flush=True)
C = Colouring(len(V), E, k=4, selectors=False)
C.solver.add_clause([C.var(o, 0)])
for c in (1, 2, 3):
    C.solver.add_clause([-C.var(o, c)])
assert C.colourable(), "the ball is not 4-colourable, so nothing below is meaningful"
t = time.time()
mono, virt = [], []
for q in range(len(V)):
    if q == o:
        continue
    if not C.solver.solve(assumptions=[C.var(q, 0)]):
        virt.append(q)
    elif not C.solver.solve(assumptions=[C.var(q, 1)]):
        mono.append(q)
C.close()
print(f"scanned in {time.time()-t:.0f}s\n")


def spindleable(d):
    sq = d * d
    if abs(sq - round(sq)) > 1e-6 or round(sq) < 1:
        return ""
    i, m = round(sq), 4 * round(sq) - 1
    return next((f"  <<< sqrt({i}): theta_{i} is in the field, SPINDLE-ABLE"
                 for s in SQFREE if m % s == 0 and math.isqrt(m // s) ** 2 == m // s), "")


for title, group in (("VIRTUAL EDGES (forced to differ)", virt),
                     ("MONO-PAIRS (forced to agree)", mono)):
    print(f"{title}: {len(group)} points")
    for d, c in sorted(collections.Counter(round(norm(V[q]), 4) for q in group).items()):
        print(f"   |q| = {d:.4f}   {c:4d} points{spindleable(d)}")
    print()
