#!/usr/bin/env python3
"""Minimise a construction whose rotation centre is NOT the origin.

Usage: centre_shrink.py CENTRE_RADIUS [--depth 3] [--radius 2.0] [--seed N]

Heule and Parts always rotate about the shared origin. They never had a reason
to; it is simply how the first construction was written. Measured here, twenty
different lattice points work as rotation centres, each giving a 5-chromatic
union, and each is a different construction family with its own minimum. Only
the origin has ever been minimised.

The two parts still share exactly one vertex, the centre, whichever centre it
is, so the arithmetic of the record is unchanged: the prize is that a different
family might simply have a smaller minimum.
"""
import os, sys, time, argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.field import K, Pt
from hn.construct import unit_vector_family, ball, dedup, edges, rotate, norm, ROT
from hn.io import save_points, save_edges
from hn.graph import induced
from hn import verify, find_triangle
from hn.fastshrink import fast_shrink

OUT = os.path.join(os.path.dirname(__file__), "..", "out")
ap = argparse.ArgumentParser()
ap.add_argument("centre", type=float, help="radius of the rotation centre")
ap.add_argument("--depth", type=int, default=3)
ap.add_argument("--radius", type=float, default=2.0)
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--jL", type=int, default=2, help="unit-vector family of the fixed part")
ap.add_argument("--jS", type=int, default=2, help="unit-vector family of the rotated part")
a = ap.parse_args()

WL, WS = unit_vector_family(a.jL), unit_vector_family(a.jS)
V = ball(WL, a.depth, a.radius)
VS = ball(WS, a.depth, a.radius)
byr = {}
for p in ball(unit_vector_family(2), 3, 2.2):
    byr.setdefault(round(norm(p), 9), p)
key = min(byr, key=lambda r: abs(r - a.centre))
c = byr[key]
RV = [c + rotate(p - c, ROT["theta4"]) for p in VS]
P = dedup(V + RV)
E = edges(P)
print(f"centre {key:.4f}, lattices (jL={a.jL}, jS={a.jS}), ball {a.radius}: "
      f"union {len(P)} vertices, {len(E)} edges", flush=True)
tri = find_triangle(len(P), E)
assert verify(P, E, triangle=tri), "this centre does not give a 5-chromatic union"
print("verified 5-chromatic; shrinking", flush=True)
t = time.time()
keep = fast_shrink(P, E, seed=a.seed, log=lambda s: print(s, flush=True))
P2, E2 = induced(P, E, keep)
print(f"result: {len(P2)} vertices, {len(E2)} edges  ({time.time()-t:.0f}s)"
      + ("   <<< BELOW THE 509 RECORD" if len(P2) < 509 else ""), flush=True)
print("independent check (fresh solver, no assumptions):", verify(P2, E2, triangle=None), flush=True)
tag = f"c{key:.4f}_j{a.jL}{a.jS}_r{a.radius}_{a.seed}"
save_points(f"{OUT}/{tag}.pts", P2)
save_edges(f"{OUT}/{tag}.edge", len(P2), E2)
