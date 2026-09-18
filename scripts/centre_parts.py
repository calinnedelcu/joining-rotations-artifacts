#!/usr/bin/env python3
"""Split a non-origin construction into its two parts and minimise them exactly.

Usage: centre_parts.py CENTRE_RADIUS [--ball 1.5] [--side L|S|both]
                       [--seed N] [--time SECONDS]

Greedy deletion from a 2600-vertex pool costs hours and only ever reaches a
minimal graph. The pipeline that actually proved things about the record works
differently: split the graph at its interface, hold one part fixed, and let the
exact search settle the other. On Parts' own pool that takes minutes.

That pipeline was written for the origin. This generalises it to any rotation
centre, which is where the unexplored constructions are (docs/ATTEMPTS.md
route 19). Measured: for the centre at radius 0.8759 the interface is 19
vertices, the same size as the record's, so the two sides are comparable
objects and the same method applies.

The parts here are the whole balls, not minimised ones, so this measures what
each side costs from scratch rather than starting from somebody's answer.
"""
import os, sys, time, argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.construct import (unit_vector_family, ball, dedup, edges, rotate, norm,
                          ROT, contains)
from hn.io import save_points, save_edges
from hn.graph import induced
from hn.hitting import search
from hn import verify, find_triangle

OUT = os.path.join(os.path.dirname(__file__), "..", "out")
ap = argparse.ArgumentParser()
ap.add_argument("centre", type=float)
ap.add_argument("--ball", type=float, default=1.5)
ap.add_argument("--side", default="S", choices=["L", "S"])
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--time", type=float, default=None)
ap.add_argument("--bound", type=int, default=None)
ap.add_argument("--grow", type=int, default=2)
a = ap.parse_args()
log = lambda s: print(s, flush=True)

W = unit_vector_family(2)
probe = ball(W, 3, 2.2)
byr = {}
for p in probe:
    byr.setdefault(round(norm(p), 9), p)
key = min(byr, key=lambda r: abs(r - a.centre))
c = byr[key]

V = ball(W, 3, a.ball)
RV = [c + rotate(p - c, ROT["theta4"]) for p in V]
P = dedup(V + RV)
E = edges(P)
n = len(P)
Vk = {p.key() for p in V}
Lidx = [i for i, p in enumerate(P) if p.key() in Vk]
Sidx = [i for i in range(n) if i not in set(Lidx)]
log(f"centre at radius {key:.4f}, ball radius {a.ball}: "
    f"{n} vertices, {len(E)} edges; L side {len(Lidx)}, rotated side {len(Sidx)}")
tri = find_triangle(n, E)
assert verify(P, E, triangle=tri), "this centre and ball are not 5-chromatic"
log("verified 5-chromatic")

fixed = Lidx if a.side == "S" else Sidx
free = Sidx if a.side == "S" else Lidx
log(f"holding the {'L' if a.side == 'S' else 'rotated'} side fixed "
    f"({len(fixed)} vertices), minimising the other ({len(free)} free)")


def save(best):
    tag = f"cp_{key:.4f}_{a.side}_{a.seed}"
    keep = sorted(set(best) | set(fixed))
    Q, F = induced(P, E, keep)
    save_points(f"{OUT}/{tag}.pts", Q)
    save_edges(f"{OUT}/{tag}.edge", len(Q), F)
    log(f"  saved {len(Q)} vertices, {len(F)} edges"
        + ("   <<< BELOW THE 509 RECORD" if len(Q) < 509 else ""))


best, proven = search(P, E, start=free, bound=a.bound, time_limit=a.time,
                      cuts_per_iter=2, seed=a.seed, log=log, on_improve=save,
                      fixed=fixed, grow_every=a.grow,
                      grow_budget=5000, essential_budget=50000)
if best is not None:
    save(best)
    log(f"best: {len(best)} free + {len(fixed)} fixed = {len(best)+len(fixed)} vertices; "
        f"proven minimum over this pool: {proven}")
