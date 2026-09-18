#!/usr/bin/env python3
"""Relax an imposed symmetry: shrink a symmetric graph without it.

Usage: relax.py GRAPH.pts [--seed N]

Parts' own recipe, and the one that produced the record: minimise with an
output symmetry imposed, then minimise again with the symmetry dropped. He
calls the reason for it the overcompression effect -- a minimal asymmetric
graph is usually not a subgraph of a minimal symmetric one -- so the symmetric
answer is a place to start from, not an answer.

Measured here: the 2365-point pool reduces to 1081 vertices under 6-fold
symmetry. This drops the symmetry and shrinks from there, with one persistent
oracle proposing and a fresh solver confirming.
"""
import os, sys, time, argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.io import load_points, save_points, save_edges
from hn.graph import induced
from hn.construct import edges
from hn.fastshrink import sample_descend, batch_delete
from hn import verify

OUT = os.path.join(os.path.dirname(__file__), "..", "out")
ap = argparse.ArgumentParser()
ap.add_argument("graph")
ap.add_argument("--seed", type=int, default=0)
a = ap.parse_args()
log = lambda s: print(s, flush=True)
P = load_points(a.graph)
E = edges(P)
log(f"{os.path.basename(a.graph)}: {len(P)} vertices, {len(E)} edges")
keep = sample_descend(P, E, list(range(len(P))), seed=a.seed, log=log)
keep = batch_delete(P, E, keep, seed=a.seed, log=log)
ok = verify(P, E, keep, triangle=None)
Q, F = induced(P, E, keep)
log(f"result: {len(Q)} vertices, {len(F)} edges; independent check {ok}"
    + ("   <<< BELOW THE 509 RECORD" if len(Q) < 509 and ok else ""))
tag = f"relaxed_{os.path.basename(a.graph).split('.')[0]}_{a.seed}"
save_points(f"{OUT}/{tag}.pts", Q)
save_edges(f"{OUT}/{tag}.edge", len(Q), F)
