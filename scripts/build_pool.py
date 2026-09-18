#!/usr/bin/env python3
"""Build a candidate pool  L  union  theta_4(S)  and save it under out/.

Usage:  build_pool.py NAME [--L403 | --dL D --rL R] [--dS D --rS R --jS J]

    small   L403 union theta_4(ball(18 vectors, depth 3, r 2.45))      ~900
    mid     ball(30, d3, r2.53) + ball(30, d4, r1.0)  union  same S    ~3900
    big     ball(30, d4, r2.53)  union  theta_4(ball(30, d3, r2.45))   ~10700

`mid` and `big` contain the 509-vertex record (its large part reaches
radius 2.5243 and needs depth 4 only near the origin); `small` contains 510.
So the record is always an upper bound for the minimum over the pool.
"""
import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn import load_vtx
from hn.io import save_points, save_edges
from hn.construct import (unit_vector_family, ball, dedup, theta4, edges,
                          contains, ORIGIN)

D = os.path.join(os.path.dirname(__file__), "..", "data")
OUT = os.path.join(os.path.dirname(__file__), "..", "out")
name = sys.argv[1] if len(sys.argv) > 1 else "small"
W30, W18 = unit_vector_family(2), unit_vector_family(1)
t = time.time()
if name == "small":
    L = load_vtx(f"{D}/vtx/L403.vtx")
    S = ball(W18, 3, 2.45)
elif name == "mid":
    L = dedup(ball(W30, 3, 2.53) + ball(W30, 4, 1.0))
    S = ball(W18, 3, 2.45)
elif name == "big":
    L = ball(W30, 4, 2.53)
    S = ball(W30, 3, 2.45)
else:
    raise SystemExit("unknown pool " + name)
P = dedup(L + [theta4(p) for p in S])
E = edges(P)
print(f"pool {name}: |L|={len(L)} |S|={len(S)} -> {len(P)} vertices, {len(E)} edges  ({time.time()-t:.1f}s)")
for g in ["509", "510", "517", "529"]:
    found, missing = contains(P, load_vtx(f"{D}/vtx/{g}.vtx"))
    print(f"  contains {g}: {len(found)}/{len(found)+len(missing)}")
os.makedirs(OUT, exist_ok=True)
save_points(f"{OUT}/{name}.pts", P)
save_edges(f"{OUT}/{name}.edge", len(P), E)
print(f"saved out/{name}.pts and out/{name}.edge")
