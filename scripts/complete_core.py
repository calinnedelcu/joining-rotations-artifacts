#!/usr/bin/env python3
"""Fix the record's symmetric core and search for a cheaper completion.

Usage: complete_core.py POOL.pts CORE_SIZE [--bound B] [--pairs N] [--seed N]

The 509-vertex record is asymmetric, its automorphism group is trivial, and yet
rotating it by 120 degrees fixes 477 of its points. Its maximal
120-degree-closed subset is 457 points, and the remaining 52 are what break the
symmetry.

That splits the record at a seam nobody has cut it along, and turns the question
into the best-posed search in this repository. Hold the 457-point core fixed. It
is 4-colourable on its own, so something must be added. The record adds 52. Is
there a completion of 51, drawn from the 615 lattice points that have at least
four neighbours in the core? A few dozen free choices out of a few hundred, with
the rest of the graph nailed down.
"""
import os, sys, argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.io import load_points, save_points, save_edges
from hn.graph import induced
from hn.construct import edges
from hn.hitting import search
from hn import load_vtx, verify

OUT = os.path.join(os.path.dirname(__file__), "..", "out")
ap = argparse.ArgumentParser()
ap.add_argument("pool")
ap.add_argument("core", type=int, help="the first this many points of the pool are the core")
ap.add_argument("--bound", type=int, default=None)
ap.add_argument("--pairs", type=int, default=400)
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--time", type=float, default=None)
ap.add_argument("--start", default="data/vtx/509.vtx")
ap.add_argument("--search", action="store_true",
                help="skip the bootstraps that only help a PROOF and go straight to\n"
                     "     the loop; this is a hunt for a completion, not a bound")
a = ap.parse_args()
log = lambda s: print(s, flush=True)

P = load_points(a.pool)
G_ = load_vtx(a.start)
have = {p.key() for p in P}
missing = [p for p in G_ if p.key() not in have]
if missing:
    # the record's own symmetry-breaking points must be in the pool, or the
    # start is not the record and is not 5-chromatic
    P = list(P) + missing
    print(f"added {len(missing)} points of the start graph that the degree filter "
          f"had excluded", flush=True)
E = edges(P)
fixed = list(range(a.core))
G = load_vtx(a.start)
idx = {p.key(): i for i, p in enumerate(P)}
start = sorted(idx[p.key()] for p in G if p.key() in idx and idx[p.key()] >= a.core)
bound = a.bound if a.bound is not None else len(start) - 1
log(f"pool {len(P)} points, {len(E)} edges; core {a.core} held fixed, "
    f"{len(P)-a.core} candidates; the record completes it with {len(start)}, "
    f"so the bound is {bound}")
assert verify(P, E, sorted(set(start) | set(fixed)), triangle=None), \
    "core plus the record's own completion is not 5-chromatic"
log("core plus the record's completion verified 5-chromatic")


def save(best):
    tag = f"core{a.core}_{a.seed}"
    keep = sorted(set(best) | set(fixed))
    Q, F = induced(P, E, keep)
    save_points(f"{OUT}/{tag}.pts", Q)
    save_edges(f"{OUT}/{tag}.edge", len(Q), F)
    log(f"  saved {len(Q)} vertices, {len(F)} edges"
        + ("   <<< BELOW THE 509 RECORD" if len(Q) < 509 else ""))


best, proven = search(P, E, start=start, bound=bound, time_limit=a.time,
                      cuts_per_iter=2, seed=a.seed, log=log, on_improve=save,
                      fixed=fixed, grow_every=2, bootstrap_pairs=a.pairs,
                      bootstrap_essential=not a.search,
                      bootstrap_critical=not a.search,
                      dump_unsat=os.path.join(OUT, f"master_core{a.core}.cnf"))
if best is not None:
    save(best)
    log(f"best completion: {len(best)} points, total {len(best)+a.core}; "
        f"proven minimum over this pool: {proven}")
