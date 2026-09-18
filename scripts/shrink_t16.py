#!/usr/bin/env python3
"""Minimise the theta_16 construction, the first new joining rotation since 2018.

Usage: shrink_t16.py [--radius 4.0] [--seed N]

theta_16 = arccos(31/32), with sin = 3*sqrt7/32, lives in Q(sqrt3, sqrt7, sqrt11)
and acts on the 30 lattice points at radius exactly 4.  Route 20 concluded theta_4
was the unique joining rotation over 83 fields and some 2700 rotations, and that
conclusion was an artifact of ball size: every sweep used radius 2.2 to 2.53, where
there is not one point at radius 4 for theta_16 to move.

Given a ball that reaches the shell, L union theta_16(L) is 5-chromatic at 29113
vertices -- a 5-chromatic unit-distance graph in a field nobody has used for this
problem, reached by a rotation nobody could have tested.

Its minimum is unknown.  This runs the pipeline that took the classical union down
to 509: iterated UNSAT-core extraction, then sampled descent.
"""
import os, sys, time, argparse, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.field import set_primes, K
set_primes((3, 7, 11))
import hn.construct as C
C.refresh_field()
from hn.construct import unit_vector_family, ball, dedup, edges, rotate
from hn.io import save_points, save_edges
from hn.graph import induced
from hn.minimise import verify, propose_core
from hn.fastshrink import sample_descend, batch_delete
from hn.sat import find_triangle

OUT = os.path.join(os.path.dirname(__file__), "..", "out")
ap = argparse.ArgumentParser()
ap.add_argument("--radius", type=float, default=4.0)
ap.add_argument("--depth", type=int, default=4)
ap.add_argument("--seed", type=int, default=0)
a = ap.parse_args()
log = lambda s: print(f"[{time.strftime('%H:%M:%S')}] {s}", flush=True)

cs = (K.rat(31, 32), K.root(7) * K.rat(3, 32))
assert (cs[0] * cs[0] + cs[1] * cs[1]).is_one()
W = unit_vector_family(2)
L = ball(W, a.depth, a.radius)
U = dedup(L + [rotate(p, cs) for p in L])
E = edges(U)
log(f"union {len(U)} points, {len(E)} edges")
tri = find_triangle(len(U), E)
keep = list(range(len(U)))
for it in range(20):
    t = time.time()
    c = propose_core(U, E, keep)
    assert c is not None, "the set became 4-colourable"
    if len(c) >= len(keep):
        log(f"core {it}: {len(c)}, no smaller  ({time.time()-t:.0f}s)")
        break
    keep = c
    log(f"core {it}: {len(keep)} points  ({time.time()-t:.0f}s)")
    Q, F = induced(U, E, sorted(keep))
    save_points(f"{OUT}/t16_s{a.seed}.pts", Q)
    save_edges(f"{OUT}/t16_s{a.seed}.edge", len(Q), F)
    if len(Q) < 509:
        log(f"  {len(Q)} vertices   <<<<< BELOW THE 509 RECORD")

keep = sample_descend(U, E, keep, seed=a.seed, log=log)
Q, F = induced(U, E, sorted(keep))
save_points(f"{OUT}/t16_s{a.seed}.pts", Q)
save_edges(f"{OUT}/t16_s{a.seed}.edge", len(Q), F)
log(f"after sampling: {len(Q)} vertices, {len(F)} edges"
    + ("   <<<<< BELOW THE 509 RECORD" if len(Q) < 509 else ""))
keep = batch_delete(U, E, keep, seed=a.seed, log=log)
assert verify(U, E, keep, triangle=tri), "the reduced graph is not 5-chromatic"
Q, F = induced(U, E, sorted(keep))
save_points(f"{OUT}/t16_s{a.seed}.pts", Q)
save_edges(f"{OUT}/t16_s{a.seed}.edge", len(Q), F)
log(f"MINIMAL: {len(Q)} vertices, {len(F)} edges"
    + ("   <<<<< BELOW THE 509 RECORD" if len(Q) < 509 else ""))
