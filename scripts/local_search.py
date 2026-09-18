#!/usr/bin/env python3
"""Local search for a smaller 5-chromatic subgraph of a pool.

Usage: local_search.py POOL [--start 510] [--time SECONDS] [--seed S] [--keep FILE]
"""
import os, sys, argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn import load_vtx, load_edges
from hn.io import load_points, save_points, save_edges
from hn.graph import induced
from hn.construct import contains
from hn.search import local_search

D = os.path.join(os.path.dirname(__file__), "..", "data")
OUT = os.path.join(os.path.dirname(__file__), "..", "out")
ap = argparse.ArgumentParser()
ap.add_argument("pool")
ap.add_argument("--start", default="510")
ap.add_argument("--keep", default=None, help="start from a .keep file of pool indices")
ap.add_argument("--time", type=float, default=None)
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--samples", type=int, default=3)
ap.add_argument("--cand", type=int, default=60)
a = ap.parse_args()

P = load_points(f"{OUT}/{a.pool}.pts")
E = load_edges(f"{OUT}/{a.pool}.edge")
if a.keep:
    start = list(map(int, open(a.keep).read().split()))
else:
    G = load_vtx(f"{D}/vtx/{a.start}.vtx")
    keyidx = {p.key(): i for i, p in enumerate(P)}
    start = [keyidx[p.key()] for p in G if p.key() in keyidx]
    assert len(start) == len(G), "start graph not inside the pool"
print(f"pool {a.pool}: {len(P)} vertices {len(E)} edges; start {len(start)}", flush=True)

def save(best):
    tag = f"ls_{a.pool}_{a.seed}"
    with open(f"{OUT}/{tag}.keep", "w") as f:
        f.write(" ".join(map(str, best)) + "\n")
    P2, E2 = induced(P, E, best)
    save_points(f"{OUT}/{tag}.pts", P2)
    save_edges(f"{OUT}/{tag}.edge", len(P2), E2)

best = local_search(P, E, start, time_limit=a.time, seed=a.seed, samples=a.samples,
                    max_candidates=a.cand, log=lambda s: print(s, flush=True), on_improve=save)
save(best)
print(f"best: {len(best)} vertices", flush=True)
