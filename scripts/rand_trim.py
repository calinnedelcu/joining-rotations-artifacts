#!/usr/bin/env python3
"""Randomised graph trimming: shuffle, trim, repeat.  Heule's loop.

Usage: rand_trim.py GRAPH.pts [--field 3,5,11] [--shuffles 6] [--rounds 60]

A SAT refutation depends on the order the clauses arrive in, so trimming a graph
by its UNSAT core twice the same way gives the same answer twice.  Heule shuffles
the formula between trims and repeats "until randomization cannot further reduce
the size of the graph".

Measured on the classical union (4525 points): the deterministic core is 3877
every single time, while six shuffles give six distinct cores between 3577 and
4027 -- the best of them 300 vertices better than the deterministic one, and the
six differing from each other by 1290 vertices.  That spread is both a better
answer and the diversity the accumulative graph is supposed to be built from.

Each round takes the best core of several shuffles, then trims that.
"""
import os, sys, time, argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.field import set_primes

ap = argparse.ArgumentParser()
ap.add_argument("graph")
ap.add_argument("--field", default="3,5,11")
ap.add_argument("--shuffles", type=int, default=6)
ap.add_argument("--rounds", type=int, default=60)
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--tag", default=None)
a = ap.parse_args()
set_primes(tuple(int(x) for x in a.field.split(",")))
import hn.construct as C
C.refresh_field()
from hn.construct import edges
from hn.io import load_points, load_vtx, save_points, save_edges
from hn.graph import induced
from hn.minimise import verify
from hn.randcore import randomized_core
from hn.sat import find_triangle
from hn.fastshrink import batch_delete

OUT = os.path.join(os.path.dirname(__file__), "..", "out")
tag = a.tag or f"rt_{os.path.basename(a.graph).split('.')[0]}_{a.seed}"
log = lambda s: print(f"[{time.strftime('%H:%M:%S')}] {s}", flush=True)

P = load_vtx(a.graph) if a.graph.endswith(".vtx") else load_points(a.graph)
E = edges(P)
tri = find_triangle(len(P), E)
log(f"{os.path.basename(a.graph)}: {len(P)} points, {len(E)} edges")
assert verify(P, E, triangle=tri), "not 5-chromatic"

keep = list(range(len(P)))
best = len(keep)
stall = 0
for r in range(a.rounds):
    t = time.time()
    cores = []
    for s in range(a.shuffles):
        c = randomized_core(len(P), E, keep, seed=a.seed * 1000 + r * 37 + s)
        if c is not None and len(c) < len(keep):
            cores.append(c)
    if not cores:
        stall += 1
        log(f"round {r}: no shuffle improved on {len(keep)}  ({time.time()-t:.0f}s)")
        if stall >= 3:
            log("randomisation cannot reduce it further")
            break
        continue
    stall = 0
    keep = min(cores, key=len)
    log(f"round {r}: {len(cores)} of {a.shuffles} shuffles improved; "
        f"best {len(keep)} (sizes {sorted(len(c) for c in cores)[:5]})  "
        f"({time.time()-t:.0f}s)")
    if len(keep) < best:
        best = len(keep)
        Q, F = induced(P, E, sorted(keep))
        save_points(f"{OUT}/{tag}.pts", Q)
        save_edges(f"{OUT}/{tag}.edge", len(Q), F)
        if len(Q) < 509:
            log(f"   {len(Q)} vertices   <<<<< BELOW THE 509 RECORD")

keep = batch_delete(P, E, keep, seed=a.seed, log=log)
assert verify(P, E, keep, triangle=tri), "the trimmed graph is not 5-chromatic"
Q, F = induced(P, E, sorted(keep))
save_points(f"{OUT}/{tag}.pts", Q)
save_edges(f"{OUT}/{tag}.edge", len(Q), F)
log(f"settled at {len(Q)} vertices, {len(F)} edges"
    + ("   <<<<< BELOW THE 509 RECORD" if len(Q) < 509 else ""))
