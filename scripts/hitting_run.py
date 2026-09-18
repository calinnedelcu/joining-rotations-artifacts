#!/usr/bin/env python3
"""Run the hitting-set search on a pool.

Usage: hitting_run.py POOL [--start 510] [--bound B] [--time SECONDS] [--seed S]
                            [--cuts C] [--tabu N] [--extra K]

POOL is a name under out/ (built by build_pool.py) or 'g510' for the record
graph itself, or 'g510+K' for the record graph plus K random extra pool
vertices from out/small (a controlled test of convergence).
"""
import os, sys, time, argparse, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn import load_vtx, load_edges
from hn.io import load_points, save_points, save_edges
from hn.graph import induced
from hn.construct import edges as exact_edges, contains
from hn.hitting import search

D = os.path.join(os.path.dirname(__file__), "..", "data")
OUT = os.path.join(os.path.dirname(__file__), "..", "out")
ap = argparse.ArgumentParser()
ap.add_argument("pool")
ap.add_argument("--start", default="510")
ap.add_argument("--bound", type=int, default=None)
ap.add_argument("--time", type=float, default=None)
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--cuts", type=int, default=2)
ap.add_argument("--tabu", type=int, default=20000)
ap.add_argument("--extra", type=int, default=0)
ap.add_argument("--no-bootstrap", action="store_true")
ap.add_argument("--grow", type=int, default=3)
a = ap.parse_args()

G = load_vtx(f"{D}/vtx/{a.start}.vtx")
if a.pool.startswith("g510"):
    small = load_points(f"{OUT}/small.pts")
    keys = {p.key() for p in G}
    others = [p for p in small if p.key() not in keys]
    rng = random.Random(a.seed)
    rng.shuffle(others)
    P = G + others[:a.extra]
    E = exact_edges(P)
    tag = f"g510+{a.extra}"
else:
    P = load_points(f"{OUT}/{a.pool}.pts")
    E = load_edges(f"{OUT}/{a.pool}.edge")
    tag = a.pool
found, missing = contains(P, G)
keyidx = {p.key(): i for i, p in enumerate(P)}
start = [keyidx[p.key()] for p in G if p.key() in keyidx]
print(f"pool {tag}: {len(P)} vertices {len(E)} edges; start graph {a.start} has {len(found)}/{len(G)} inside", flush=True)
if missing:
    start = None
    print("start graph not fully inside the pool; running without a start", flush=True)

def save(best):
    with open(f"{OUT}/best_{tag}_{a.seed}.keep", "w") as f:
        f.write(" ".join(map(str, best)) + "\n")
    P2, E2 = induced(P, E, best)
    save_points(f"{OUT}/best_{tag}_{a.seed}.pts", P2)
    save_edges(f"{OUT}/best_{tag}_{a.seed}.edge", len(P2), E2)

best, proven = search(P, E, start=start, bound=a.bound, time_limit=a.time,
                      cuts_per_iter=a.cuts, tabu_iters=a.tabu, seed=a.seed,
                      log=lambda s: print(s, flush=True),
                      bootstrap_critical=not a.no_bootstrap, on_improve=save, grow_every=a.grow)
if best is not None:
    save(best)
    print(f"best: {len(best)} vertices, proven optimal over the pool: {proven}", flush=True)
