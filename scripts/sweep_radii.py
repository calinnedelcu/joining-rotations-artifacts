#!/usr/bin/env python3
"""Independent ball radii for the two parts.

Usage: sweep_radii.py [JL] [JS] [CENTRE]

The record is asymmetric in every parameter, and each one was assumed
symmetric here until it was measured. Its large part needs depth 4 and radius
2.024; its small part needs depth 3 and radius 2.432. Different families,
different depths, different radii.

Route 20 dropped the shared family and cut the pool from 3997 to 2365. This
drops the shared radius as well, sweeping the two independently.
"""
import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.construct import unit_vector_family, ball, dedup, edges, rotate, norm, ROT
from hn import verify, find_triangle

jL = int(sys.argv[1]) if len(sys.argv) > 1 else 2
jS = int(sys.argv[2]) if len(sys.argv) > 2 else 1
cr = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
T4 = ROT["theta4"]
byr = {}
for p in ball(unit_vector_family(2), 3, 2.2):
    byr.setdefault(round(norm(p), 9), p)
key = min(byr, key=lambda r: abs(r - cr))
c = byr[key]
WL, WS = unit_vector_family(jL), unit_vector_family(jS)
RS = (1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.5)
print(f"centre {key:.4f}, families ({jL}, {jS}); rows are the large part's radius, "
      f"columns the small part's", flush=True)
print("    " + "".join(f"{r:>8}" for r in RS), flush=True)
best = None
cacheL = {r: ball(WL, 3, r) for r in RS}
cacheS = {r: ball(WS, 3, r) for r in RS}
for rL in RS:
    row = f"{rL:4}"
    for rS in RS:
        VL, VS = cacheL[rL], cacheS[rS]
        if len(VL) < 100 or len(VS) < 100:
            row += "       -"
            continue
        U = dedup(VL + [c + rotate(p - c, T4) for p in VS])
        if len(U) > 12000:
            row += "     big"
            continue
        E = edges(U)
        tri = find_triangle(len(U), E)
        five = verify(U, E, triangle=tri) if tri else False
        row += f"{len(U) if five else 0:>8}"
        if five and (best is None or len(U) < best[0]):
            best = (len(U), rL, rS)
    print(row, flush=True)
print(f"\nzeros are not 5-chromatic; smallest pool: {best}", flush=True)
