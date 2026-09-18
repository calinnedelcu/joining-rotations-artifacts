#!/usr/bin/env python3
"""A large-part pool that is both wider than Parts' region and dense.

Usage: wide_dense_pool.py [--degree 4] [--radius 2.53] [--depth 4]

Route 2 leaves exactly one thing open: "a large-part pool substantially outside
his region".  Route 13 says why every attempt at one failed -- density decides
convergence.  Choosing 373 of 412 is proven in minutes; choosing 373 of the
8131-point ball never constrains the master at all.

Those two are not in conflict, they are a recipe: take the wide ball, and keep
only the candidates that are dense against the answer.  A lattice point with at
least four neighbours in the record's own large part is a plausible member of a
better one; a point with none is noise that only widens the master's search.

The result reaches outside Parts' 412-point accumulative pool -- the ball has
radius 2.53 where his large part stops at 2.024 -- while staying in the density
regime where the search settles.
"""
import os, sys, argparse, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn import load_vtx
from hn.io import save_points, load_points
from hn.construct import unit_vector_family, ball, dedup, edges, norm

D = os.path.join(os.path.dirname(__file__), "..", "data", "parts")
ap = argparse.ArgumentParser()
ap.add_argument("--degree", type=int, default=4)
ap.add_argument("--radius", type=float, default=2.53)
ap.add_argument("--depth", type=int, default=4)
ap.add_argument("--Lfile", default="v374e1860.vtx")
ap.add_argument("--side", default="L", choices=["L", "S"],
                help="S builds the dual pool: the small part plus dense candidates, "
                     "in its own unrotated frame, since parts_side applies theta_4")
ap.add_argument("--Sfile", default="v136e564.vtx")
ap.add_argument("--out", default=None)
a = ap.parse_args()
log = lambda s: print(s, flush=True)

if a.side == "S":
    a.Lfile, a.radius, a.depth = a.Sfile, min(a.radius, 2.45), 3
L = load_vtx(f"{D}/{a.Lfile}")
Lk = {p.key() for p in L}
W = unit_vector_family(2)
B = ball(W, a.depth, a.radius)
log(f"{a.Lfile}: {len(L)} points, max radius {max(norm(p) for p in L):.3f}; "
    f"wide ball depth {a.depth} radius {a.radius}: {len(B)} points")
P = list(L) + [p for p in B if p.key() not in Lk]
E = edges(P)
inL = set(range(len(L)))
deg = collections.Counter()
for u, v in E:
    if (u in inL) != (v in inL):
        deg[v if u in inL else u] += 1
cand = [i for i in range(len(L), len(P)) if deg[i] >= a.degree]
keep = sorted(inL | set(cand))
Q = [P[i] for i in keep]
out = a.out or f"out/wide{a.side}_d{a.degree}.pts"
save_points(out, Q)
outside = sum(1 for p in Q if norm(p) > (2.03 if a.side == "L" else 2.432))
log(f"pool {len(Q)} points = {len(L)} of the record's large part + {len(cand)} "
    f"candidates at degree >= {a.degree}; {outside} of them lie outside Parts' "
    f"region, and the answer would be {len(L)/len(Q):.0%} of the pool")
log(f"wrote {out}")
