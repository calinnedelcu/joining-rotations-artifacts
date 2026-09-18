#!/usr/bin/env python3
"""Alternating minimisation of the theta_16 construction, one side at a time.

Usage: t16_sides.py GRAPH.pts L|S [--bound N] [--degree 4] [--seed N]

Global greedy deletion reaches a *minimal* graph, not a minimum one, and in the
classical field it stalls between 848 and 1051 -- the record needed the exact
master on one side with the other held fixed.  The theta_16 construction has the
same shape, and the split is exact rather than heuristic: theta_16 introduces
sqrt7, so a point belongs to the rotated side if and only if sqrt7 occurs in its
coordinates.

Measured on the current graph: 2777 points with no sqrt7, 4101 with it, and only
42 edges between the two sides -- the record's own profile, which has 18.

So hold one side and let the master settle the other, exactly as parts_side.py does
for the classical construction.
"""
import os, sys, time, argparse, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.field import set_primes, K
set_primes((3, 7, 11))
import hn.construct as C
C.refresh_field()
from hn.construct import edges, dedup, split_parts, unit_vector_family, ball, rotate
from hn.io import load_points, save_points, save_edges
from hn.graph import induced
from hn.hitting import search
from hn.minimise import verify

OUT = os.path.join(os.path.dirname(__file__), "..", "out")
ap = argparse.ArgumentParser()
ap.add_argument("graph")
ap.add_argument("side", choices=["L", "S"], help="L = the sqrt7-free forcer, S = rotated")
ap.add_argument("--bound", type=int, default=None)
ap.add_argument("--degree", type=int, default=0,
                help="add lattice candidates with this many neighbours in the graph "
                     "(0 = shrink only, no new points)")
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--time", type=float, default=None)
a = ap.parse_args()
log = lambda s: print(f"[{time.strftime('%H:%M:%S')}] {s}", flush=True)

P = load_points(a.graph)
if a.degree:
    cs = (K.rat(31, 32), K.root(7) * K.rat(3, 32))
    W = unit_vector_family(2)
    B0 = ball(W, 4, 4.0)
    LAT = dedup(B0 + [rotate(p, cs) for p in B0])
    have = {p.key() for p in P}
    P0 = list(P) + [p for p in LAT if p.key() not in have]
    E0 = edges(P0)
    inG = set(range(len(P)))
    deg = collections.Counter()
    for u, v in E0:
        if (u in inG) != (v in inG):
            deg[v if u in inG else u] += 1
    cand = [i for i in range(len(P), len(P0)) if deg[i] >= a.degree]
    P = [P0[i] for i in sorted(inG | set(cand))]
    log(f"pool grown with {len(cand)} lattice candidates at degree >= {a.degree}")
E = edges(P)
Lidx, Sidx = split_parts(P)
free = Lidx if a.side == "L" else Sidx
fixed = Sidx if a.side == "L" else Lidx
conn = sum(1 for u, v in E if (u in set(Lidx)) != (v in set(Lidx)))
log(f"{os.path.basename(a.graph)}: {len(P)} points, {len(E)} edges; forcer side "
    f"{len(Lidx)}, rotated side {len(Sidx)}, {conn} connection edges")
log(f"holding the {'rotated' if a.side == 'L' else 'forcer'} side fixed ({len(fixed)}), "
    f"minimising the other ({len(free)} free)")
bound = a.bound if a.bound is not None else len(free) - 1


def save(best):
    keep = sorted(set(best) | set(fixed))
    Q, F = induced(P, E, keep)
    tag = f"t16side{a.side}_{a.seed}"
    save_points(f"{OUT}/{tag}.pts", Q)
    save_edges(f"{OUT}/{tag}.edge", len(Q), F)
    log(f"  {len(Q)} vertices, {len(F)} edges"
        + ("   <<<<< BELOW THE 509 RECORD" if len(Q) < 509 else ""))


best, proven = search(P, E, start=free, bound=bound, time_limit=a.time,
                      cuts_per_iter=2, seed=a.seed, log=log, on_improve=save,
                      fixed=fixed, grow_every=2, bootstrap_pairs=0,
                      bootstrap_essential=False, bootstrap_critical=False)
if best is not None:
    save(best)
    log(f"best: {len(best)} free + {len(fixed)} fixed = {len(best)+len(fixed)}; "
        f"proven minimum over this pool: {proven}")
