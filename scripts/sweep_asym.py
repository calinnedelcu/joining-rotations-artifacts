#!/usr/bin/env python3
"""Asymmetric lattices, and the rotation centre, together.

Usage: sweep_asym.py [RMIN] [RMAX]

Two assumptions nobody states, now both dropped at once.

The two parts do not have to come from the SAME lattice. The record itself
does not: its large part uses the 30 unit vectors with |j| <= 2 and its small
part only the 18 with |j| <= 1. Every sweep here had been using the symmetric
version, which is a bigger pool for no reason. Measured: the symmetric pool
that works is 3997 vertices, the asymmetric one 2365, a 41 percent cut.

And the rotation need not be about the origin (route 19).

Together they give the smallest pools in which a 5-chromatic graph is known to
sit, which is what the exact search needs.
"""
import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.field import K, Pt
from hn.construct import (unit_vector_family, ball, dedup, edges, rotate, norm, ROT)
from hn import verify, find_triangle

T4, TH1 = ROT["theta4"], ROT["theta1"]
probe = ball(unit_vector_family(2), 3, 2.2)
byr = {}
for p in probe:
    byr.setdefault(round(norm(p), 9), p)
rmin = float(sys.argv[1]) if len(sys.argv) > 1 else 0.0
rmax = float(sys.argv[2]) if len(sys.argv) > 2 else 1.2
radii = [r for r in sorted(byr) if rmin <= r <= rmax]
print(f"{len(radii)} centres; asymmetric lattices (jL, jS) and ball radii", flush=True)
best = []
for cr in radii:
    c = byr[cr]
    found = None
    for jL, jS in ((2, 1), (1, 2), (2, 2), (3, 1), (1, 3)):
        WL, WS = unit_vector_family(jL), unit_vector_family(jS)
        for r in (1.2, 1.4, 1.6, 1.8, 2.0):
            VL = ball(WL, 3, r)
            VS = ball(WS, 3, r)
            if len(VL) < 100 or len(VS) < 100:
                continue
            U = dedup(VL + [c + rotate(p - c, T4) for p in VS])
            if found and len(U) >= found[0]:
                continue
            E = edges(U)
            tri = find_triangle(len(U), E)
            if tri and verify(U, E, triangle=tri):
                if not found or len(U) < found[0]:
                    found = (len(U), jL, jS, r)
                break
    if found:
        mark = "   <<< beats 2365" if found[0] < 2365 else ""
        print(f"  centre {cr:.4f}: union {found[0]:5d}  (jL={found[1]}, jS={found[2]}, "
              f"ball r={found[3]}){mark}", flush=True)
        best.append((found[0], cr) + found[1:])
best.sort()
print(f"\nsmallest pools found:", flush=True)
for b in best[:8]:
    print(f"   {b[0]} vertices: centre {b[1]:.4f}, jL={b[2]}, jS={b[3]}, r={b[4]}", flush=True)
