#!/usr/bin/env python3
"""Greedy shrink of a pool built by build_pool.py.  Usage: shrink_pool.py small [seed]

Writes the surviving vertex indices to out/shrink_NAME_SEED.keep.
"""
import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn import load_edges, shrink, verify
from hn.io import load_points
from hn.graph import induced

OUT = os.path.join(os.path.dirname(__file__), "..", "out")
name = sys.argv[1] if len(sys.argv) > 1 else "small"
seed = int(sys.argv[2]) if len(sys.argv) > 2 else 0
P = load_points(f"{OUT}/{name}.pts")
E = load_edges(f"{OUT}/{name}.edge")
print(f"start: {len(P)} vertices, {len(E)} edges, seed {seed}", flush=True)
t = time.time()
keep = shrink(P, E, seed=seed)
P2, E2 = induced(P, E, keep)
print(f"result: {len(P2)} vertices, {len(E2)} edges  ({time.time()-t:.0f}s)", flush=True)
print("final independent check (no symmetry breaking):", verify(P2, E2, triangle=None), flush=True)
with open(f"{OUT}/shrink_{name}_{seed}.keep", "w") as f:
    f.write(" ".join(map(str, keep)) + "\n")
