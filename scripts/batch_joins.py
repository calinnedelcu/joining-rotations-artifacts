#!/usr/bin/env python3
"""Test many candidate joining rotations, each with its COMPLETE shell.

Usage: batch_joins.py a/b a/b ...   [--maxball N]

For each candidate this finds the smallest depth whose ball holds every point
of the rotation's shell, builds the union, and reports.  A ball that merely
reaches the shell is not enough: a negative obtained from a partial shell says
nothing, because the rotation was never given its points (results/SHELL-COMPLETENESS.md).
"""
import os, sys, time, argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))
from hn.joins import rational_spindle
from hn.construct import ball, dedup, edges_grid, rotate, norm
from hn.io import save_points, save_edges
from hn import verify, find_triangle
from shells import shell_count

ap = argparse.ArgumentParser()
ap.add_argument("specs", nargs="+")
ap.add_argument("--maxball", type=int, default=260000)
a = ap.parse_args()
log = lambda s: print(s, flush=True)
OUT = os.path.join(os.path.dirname(__file__), "..", "out")
hits = []
for spec in a.specs:
    num, den = (spec.split("/") + ["1"])[:2]
    num, den = int(num), int(den)
    J = rational_spindle(num, den)
    b = J.build()
    if b is None:
        log(f"{spec:8} rotation not in its field"); continue
    WL, WS, cs = b
    tot = shell_count(num, den)
    r = (num / den) ** 0.5
    V = depth = None
    for d in range(1, 12):
        Vd = ball(WL, d, r + 0.02)
        n = sum(1 for p in Vd if abs(norm(p) ** 2 - num / den) < 1e-9)
        if n == tot:
            V, depth = Vd, d; break
        if len(Vd) > a.maxball:
            break
    if V is None:
        log(f"{spec:8} shell {tot:3d}: no complete ball under {a.maxball} points"); continue
    t = time.time()
    U = dedup(V + [rotate(p, cs) for p in V])
    E = edges_grid(U)
    tri = find_triangle(len(U), E)
    five = verify(U, E, triangle=tri) if tri else None
    log(f"{spec:8} depth {depth} ball {len(V):6d} shell {tot:3d}/{tot} "
        f"union {len(U):7d} edges {len(E):8d} -> chi>=5 {five}"
        + ("   <<< WORKS" if five else "") + f"  ({time.time()-t:.0f}s)")
    if five:
        hits.append(spec)
        tag = f"{num}_{den}" if den != 1 else str(num)
        save_points(f"{OUT}/join{tag}.pts", U)
        save_edges(f"{OUT}/join{tag}.edge", len(U), E)
log(f"\n{len(hits)} of {len(a.specs)} give 5-chromatic unions: {hits}")
