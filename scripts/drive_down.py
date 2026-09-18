#!/usr/bin/env python3
"""Drive a 5-chromatic graph down with the exact search, one bound at a time.

Usage: drive_down.py GRAPH.pts [--centre R] [--ball 1.5] [--degree 4]
                     [--seed N] [--time SECONDS] [--target 508]

Greedy deletion stops at a MINIMAL graph, one nothing can be removed from
singly. This takes such a graph and builds a dense pool around it -- the graph
plus every lattice point with enough neighbours in it -- then runs the
hitting-set master with the bound set one below the current size, and lowers
the bound every time it succeeds.

Density is what makes this finish (docs/ATTEMPTS.md route 13): choosing 373 of
412 is proven in minutes, choosing 373 of 810 never constrains the master. The
degree threshold is the knob that sets it: raise it for a tighter pool that
settles fast, lower it to search more ground.

An UNSAT answer at bound B proves no 5-chromatic subgraph of the pool has B or
fewer vertices, so the graph in hand is the minimum over that pool.
"""
import os, sys, time, argparse, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.io import load_points, save_points, save_edges
from hn.graph import induced
from hn.construct import (unit_vector_family, ball, dedup, edges_grid, rotate, norm,
                          ROT, contains)
from hn.hitting import search
from hn import verify

OUT = os.path.join(os.path.dirname(__file__), "..", "out")
ap = argparse.ArgumentParser()
ap.add_argument("graph")
ap.add_argument("--centre", type=float, default=0.0,
                help="radius of the rotation centre the graph was built with")
ap.add_argument("--ball", type=float, default=2.2, help="lattice ball radius for candidates")
ap.add_argument("--depth", type=int, default=4,
                help="lattice depth; measured to saturate at 4, depth 5 adds no candidate")
ap.add_argument("--degree", type=int, default=5,
                help="a lattice point joins the pool with this many neighbours in the graph")
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--time", type=float, default=None)
ap.add_argument("--target", type=int, default=508)
ap.add_argument("--jmax", type=int, default=2,
                help="unit-vector family for the AMBIENT lattice the candidates "
                     "come from.  2 is the 30 vectors every part of every record "
                     "graph uses, and every pool ever searched here; 3 is the 42 "
                     "of Heule's 553-vertex large part, a strictly finer rank-4 "
                     "lattice that CONTAINS the 30-vector one -- so the record "
                     "itself lies in it, and the extra points are candidates no "
                     "search in this repository has ever been offered")
ap.add_argument("--max-candidates", type=int, default=None,
                help="keep only this many candidates, the highest degree first.  "
                     "Degree floors are integers, so the pool jumps 585 -> 704 "
                     "with nothing in between, and 704 is at 72% density where "
                     "the master does not converge.  This dials the pool "
                     "continuously, so a ladder can be climbed: prove one, use it "
                     "to constrain the next with --proved-max.")
ap.add_argument("--proved-max", type=int, default=None,
                help="a --max-candidates value already proved to contain no "
                     "answer.  Any answer here must use a candidate beyond it.")
ap.add_argument("--proved-degree", type=int, default=None,
                help="a degree floor at which this same pool construction has "
                     "ALREADY been proved to contain no answer.  Any answer here "
                     "must then use a candidate that the tighter pool lacked, "
                     "which is added to the master as one clause and cuts the "
                     "search space hard.  Only pass a value actually proved.")
ap.add_argument("--pairs", type=int, default=0,
                help="enumerate size-2 correction sets when at most this many vertices are "
                     "non-essential; this is what made yesterday's small-part proof converge")
a = ap.parse_args()
log = lambda s: print(s, flush=True)

G = load_points(a.graph)
log(f"graph {os.path.basename(a.graph)}: {len(G)} vertices")

W = unit_vector_family(a.jmax)
V = ball(W, a.depth, a.ball)
byr = {}
for p in V:
    byr.setdefault(round(norm(p), 9), p)
key = min(byr, key=lambda r: abs(r - a.centre))
c = byr[key]
LAT = dedup(V + [c + rotate(p - c, ROT["theta4"]) for p in V])
log(f"ambient lattice for centre {key:.4f}: {len(LAT)} points")

Gk = {p.key() for p in G}
P = dedup(list(G) + [p for p in LAT if p.key() not in Gk])
E = edges_grid(P)   # linear in space; the blocked pass wants GBs at jmax 4
adj = collections.Counter()
inG = set(range(len(G)))
for u, v in E:
    if (u in inG) != (v in inG):
        adj[v if u in inG else u] += 1
cand = [i for i in range(len(G), len(P)) if adj[i] >= a.degree]
cand.sort(key=lambda i: (-adj[i], i))         # highest degree first, then stable
dropped = []
if a.max_candidates is not None and len(cand) > a.max_candidates:
    dropped = cand[a.max_candidates:]
    cand = cand[:a.max_candidates]
    log(f"keeping the {len(cand)} highest-degree candidates of "
        f"{len(cand) + len(dropped)}")
pool = sorted(inG | set(cand))
P2, E2 = induced(P, E, pool)
start = list(range(len(G)))
log(f"pool {len(P2)} points ({len(cand)} candidates at degree >= {a.degree}), "
    f"{len(E2)} edges; the graph is {len(G)/len(P2):.0%} of it")
assert verify(P2, E2, start, triangle=None), "the graph is not 5-chromatic"


def save(best):
    tag = f"driven_{os.path.basename(a.graph).split('.')[0]}_{a.seed}"
    Q, F = induced(P2, E2, sorted(best))
    save_points(f"{OUT}/{tag}.pts", Q)
    save_edges(f"{OUT}/{tag}.edge", len(Q), F)
    log(f"  saved {len(Q)} vertices, {len(F)} edges"
        + ("   <<< BELOW THE 509 RECORD" if len(Q) < 509 else ""))


require = None
if a.proved_max is not None:
    assert a.max_candidates and a.proved_max < a.max_candidates, \
        "the proved pool must be the smaller one"
    extra = [pool.index(i) for i in cand[a.proved_max:]]
    log(f"already proved with {a.proved_max} candidates: any answer must use one "
        f"of the {len(extra)} beyond that")
    require = extra
elif a.proved_degree is not None:
    assert a.proved_degree > a.degree, "the proved pool must be the tighter one"
    tight = {i for i in range(len(G), len(P)) if adj[i] >= a.proved_degree}
    extra = [pool.index(i) for i in pool if i >= len(G) and i not in tight]
    log(f"already proved at degree >= {a.proved_degree}: any answer must use one "
        f"of the {len(extra)} candidates that pool does not contain")
    require = extra

dump = os.path.join(OUT, f"master_{os.path.basename(a.graph).split('.')[0]}_d{a.degree}.cnf")
best, proven = search(P2, E2, start=start, bound=len(G) - 1, time_limit=a.time,
                      cuts_per_iter=2, seed=a.seed, log=log, on_improve=save,
                      grow_every=2, bootstrap_pairs=a.pairs, dump_unsat=dump,
                      require_any=require)
if best is not None:
    save(best)
    log(f"best {len(best)} vertices; proven minimum over this pool: {proven}")
