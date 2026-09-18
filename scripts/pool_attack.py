#!/usr/bin/env python3
"""Attack a given pool for a graph below a given size.

Usage: pool_attack.py POOL.pts [--start data/vtx/509.vtx] [--bound 508]
                      [--pairs 250] [--seed N] [--time SECONDS]

drive_down.py grows its own pool out of the lattice around one graph. This
takes a pool as it is, which is what the interesting ones are: the UNION of two
different record graphs. Those unions are 547 to 599 points and 5-chromatic,
they hold two different published structures at once, and the answer sits at 92
percent of them, which is the density where the exact search finishes.

Nobody has searched a union of two records. Each published graph has been
minimised on its own; the combinations of their structures have not.
"""
import os, sys, argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn import load_vtx, verify
from hn.io import load_points, save_points, save_edges
from hn.graph import induced
from hn.construct import edges
from hn.hitting import search

OUT = os.path.join(os.path.dirname(__file__), "..", "out")
ap = argparse.ArgumentParser()
ap.add_argument("pool")
ap.add_argument("--start", default="data/vtx/509.vtx")
ap.add_argument("--bound", type=int, default=508)
ap.add_argument("--pairs", type=int, default=250)
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--time", type=float, default=None)
ap.add_argument("--symmetry", type=int, default=0,
                help="impose k-fold rotational symmetry on the search (3 or 6)")
ap.add_argument("--ess-budget", type=int, default=None,
                help="conflict budget per essential check; keeps one hard proof from stalling")
ap.add_argument("--no-start", action="store_true",
                help="search with no anchor graph at all")
a = ap.parse_args()
log = lambda s: print(s, flush=True)

P = load_points(a.pool) if a.pool.endswith(".pts") else load_vtx(a.pool)
G = load_vtx(a.start) if a.start.endswith(".vtx") else load_points(a.start)
E = edges(P)
idx = {p.key(): i for i, p in enumerate(P)}
missing = [p for p in G if p.key() not in idx]
assert not missing, f"{len(missing)} vertices of the start graph are not in the pool"
start = sorted(idx[p.key()] for p in G)
orbits = None
if a.symmetry:
    from hn.symmetry import rot60
    step, seen, orbits, dropped = 6 // a.symmetry, set(), [], 0
    for i in range(len(P)):
        if i in seen:
            continue
        orb, q, ok = [], P[i], True
        for _ in range(a.symmetry):
            j = idx.get(q.key())
            if j is None:
                ok = False
                break
            orb.append(j)
            for _ in range(step):
                q = rot60(q)
        if not ok:
            dropped += 1
            continue
        orb = sorted(set(orb))
        seen |= set(orb)
        if len(orb) > 1:
            orbits.append(orb)
    log(f"symmetry {a.symmetry}: {len(orbits)} orbits, {dropped} points outside a closed orbit")
log(f"pool {os.path.basename(a.pool)}: {len(P)} points, {len(E)} edges; "
    f"start {len(start)} ({len(start)/len(P):.0%} of the pool); bound {a.bound}")
assert verify(P, E, start, triangle=None), "the start graph is not 5-chromatic"
if a.no_start:
    log("searching with no anchor: any 5-chromatic subgraph at or below the bound wins")
    start = None


def save(best):
    tag = f"pa_{os.path.basename(a.pool).split('.')[0]}_{a.seed}"
    Q, F = induced(P, E, sorted(best))
    save_points(f"{OUT}/{tag}.pts", Q)
    save_edges(f"{OUT}/{tag}.edge", len(Q), F)
    log(f"  saved {len(Q)} vertices, {len(F)} edges"
        + ("   <<< BELOW THE 509 RECORD" if len(Q) < 509 else ""))


best, proven = search(P, E, start=start, bound=a.bound, time_limit=a.time,
                      cuts_per_iter=2, seed=a.seed, log=log, on_improve=save,
                      grow_every=2, bootstrap_pairs=a.pairs, orbits=orbits,
                      essential_budget=a.ess_budget)
if best is not None:
    save(best)
    log(f"best {len(best)} vertices; proven minimum over this pool: {proven}")
