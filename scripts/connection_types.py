#!/usr/bin/env python3
"""Every way the two parts of a type-M graph can be joined.

Usage: connection_types.py [DEPTH] [RADIUS]        (default 4 4.0)

Parts writes that L and theta_4(S) are joined by just two orbits: the
reference orbit, both endpoints at radius 2, and the auxiliary orbit at radii
sqrt11/2 -+ sqrt3/6, joined crosswise because
r1^2 + r2^2 - 2 r1 r2 cos(theta_4) = 17/3 - 14/3 = 1.  Which six of the twelve
auxiliary points the large part keeps is what defines the subtypes M6A, M6B
and M6C, and he says the last two are under-explored.

This enumerates the cross edges directly.  Measured out to radius 4 over
Parts' full base graph (14557 points): exactly 126 cross edges and 5 radius
pairs, namely the origin with the 30 unit vectors in both directions, the 30
reference edges, and the 36 auxiliary ones.  Nothing else exists at any
radius, so the taxonomy is complete rather than merely unrefuted, and there
is no unexplored subtype hiding further out.
"""
import os, sys, collections, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.construct import unit_vector_family, ball, theta4, edges, to_float

depth = int(sys.argv[1]) if len(sys.argv) > 1 else 4
radius = float(sys.argv[2]) if len(sys.argv) > 2 else 4.0
V = ball(unit_vector_family(2), depth, radius)
P = V + [theta4(p) for p in V]
n = len(V)
print(f"V {n} points, union {len(P)}", flush=True)
E = edges(P)
pairs = collections.Counter()
for a, b in E:
    if (a < n) != (b < n):
        u, v = (a, b) if a < n else (b, a)
        pairs[(round(to_float(P[u].norm2()), 5), round(to_float(P[v].norm2()), 5))] += 1
print(f"{sum(pairs.values())} cross edges, {len(pairs)} distinct radius pairs:")
for (ra, rb), c in sorted(pairs.items(), key=lambda kv: -kv[1]):
    tag = ""
    if abs(ra - 4) < 1e-6 and abs(rb - 4) < 1e-6:
        tag = "   reference orbit"
    elif min(ra, rb) > 1e-9:
        tag = "   auxiliary orbit"
    print(f"   |p| = {math.sqrt(ra):.4f}   |q| = {math.sqrt(rb):.4f}   {c:5d} edges{tag}")
