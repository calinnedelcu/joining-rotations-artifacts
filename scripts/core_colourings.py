#!/usr/bin/env python3
"""Rank the candidates by how many colourings of the fixed core they kill.

Usage: core_colourings.py POOL.pts CORE_SIZE [--samples 300] [--keep 250]

In a fixed-core search the core never changes, so its 4-colourings never change
either -- and they are the only thing the completion has to defeat.  Sample them
once, and every candidate point can be scored before the search starts:

    under a colouring c, a candidate has 4 - |colours of its core neighbours|
    colours available.  Zero available means adding that one point already kills
    c.  One available means it is forced, and two forced neighbours of the same
    colour kill c between them.

Pool density is what decides whether the master converges (route 13): 373 of 412
is proven in minutes, 373 of 810 never settles.  Scoring gives a principled way
to cut the candidate set instead of raising the degree threshold blindly --
keep the points that do the work.
"""
import os, sys, argparse, collections, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.io import load_points, save_points
from hn.construct import edges
from hn.graph import induced
from hn.colour import ConflictColouring

ap = argparse.ArgumentParser()
ap.add_argument("pool")
ap.add_argument("core", type=int)
ap.add_argument("--samples", type=int, default=300)
ap.add_argument("--keep", type=int, default=250)
ap.add_argument("--iters", type=int, default=200000)
ap.add_argument("--out", default=None)
a = ap.parse_args()
log = lambda s: print(s, flush=True)

P = load_points(a.pool)
E = edges(P)
nc = a.core
core_edges = [(u, v) for u, v in E if u < nc and v < nc]
adj = collections.defaultdict(list)
for u, v in E:
    if u < nc <= v:
        adj[v].append(u)
    elif v < nc <= u:
        adj[u].append(v)
log(f"pool {len(P)} points, {len(E)} edges; core {nc} with {len(core_edges)} edges; "
    f"{len(P)-nc} candidates, {sum(len(x) for x in adj.values())} core-candidate edges")

C = ConflictColouring(nc, core_edges, k=4)
rng = random.Random(0)
zero = collections.Counter()
one = collections.Counter()
found = 0
for s in range(a.samples):
    init = [rng.randrange(4) for _ in range(nc)]
    col, conf = C.run(a.iters, init=init)
    if conf:
        continue
    found += 1
    for v in range(nc, len(P)):
        used = {col[u] for u in adj[v]}
        if len(used) == 4:
            zero[v] += 1
        elif len(used) == 3:
            one[v] += 1
log(f"sampled {found} proper 4-colourings of the core out of {a.samples} tries")
if not found:
    log("the core is not 4-colourable by Tabucol -- check it directly, it may be the record")
    sys.exit(0)

killers = [v for v in range(nc, len(P)) if zero[v]]
log(f"candidates that alone kill some colouring: {len(killers)}; "
    f"best kills {max(zero.values()) if zero else 0} of {found}")
score = {v: (zero[v] * found + one[v]) for v in range(nc, len(P))}
ranked = sorted(range(nc, len(P)), key=lambda v: -score[v])
top = ranked[:a.keep]
log(f"score spread: top {score[ranked[0]]}, median {score[ranked[len(ranked)//2]]}, "
    f"bottom {score[ranked[-1]]}; keeping {len(top)}")
keep = sorted(set(range(nc)) | set(top))
P2, E2 = induced(P, E, keep)
out = a.out or a.pool.replace(".pts", f"_top{a.keep}.pts")
save_points(out, P2)
log(f"wrote {out}: {len(P2)} points, core {nc} first, {len(P2)-nc} scored candidates")
