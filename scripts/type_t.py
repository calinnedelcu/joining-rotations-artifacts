#!/usr/bin/env python3
"""Hubai's type T, minimised with the machinery built here.

Usage: type_t.py [--power 3] [--seed N] [--time SECONDS]

Parts classifies every known construction into four types and says types J and
T were never pushed to their limits. Type T is Hubai's: iterated Minkowski sums
of V_37 = H^1 union theta_4(H^1), a base that already contains the rotation
inside itself rather than joining two parts across one.

Reproduced here exactly: the third power is 6937 points and 5-chromatic, and
clipping it to radius 2.5 leaves 5557 points that are 4-colourable, so the whole
thing is needed. Parts reduced it to about 5000 by hand in Mathematica. Nothing
modern has been pointed at it.

It is 10 times the record, so a large improvement still would not reach 509. It
is run because it is the last construction family nobody has touched.
"""
import os, sys, time, argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.field import K, Pt
from hn.construct import dedup, edges, rotate, ROT, minkowski, ORIGIN
from hn.io import save_points, save_edges
from hn.graph import induced
from hn.fastshrink import sample_descend, batch_delete
from hn import verify, find_triangle

OUT = os.path.join(os.path.dirname(__file__), "..", "out")
ap = argparse.ArgumentParser()
ap.add_argument("--power", type=int, default=3)
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--time", type=float, default=None)
a = ap.parse_args()
log = lambda s: print(s, flush=True)

T4, T1, T32 = ROT["theta4"], ROT["theta1"], ROT["theta3/2"]
H1, seen = [ORIGIN], {ORIGIN.key()}
for j in (-1, 0, 1):
    v = Pt(K.rat(1), K.zero())
    for _ in range(abs(j)):
        v = rotate(v, T32, inverse=j < 0)
    for _ in range(6):
        if v.key() not in seen:
            seen.add(v.key())
            H1.append(v)
        v = rotate(v, T1)
V37 = dedup(H1 + [rotate(p, T4) for p in H1])
P = list(V37)
for _ in range(a.power - 1):
    P = minkowski(P, V37)
E = edges(P)
log(f"(+)^{a.power} V_37: {len(P)} points, {len(E)} edges")
assert verify(P, E, triangle=find_triangle(len(P), E)), "not 5-chromatic"
log("verified 5-chromatic; reducing")
t0 = time.time()
keep = sample_descend(P, E, list(range(len(P))), seed=a.seed, log=log)
keep = batch_delete(P, E, keep, seed=a.seed, log=log)
ok = verify(P, E, keep, triangle=None)
Q, F = induced(P, E, keep)
log(f"result: {len(Q)} vertices, {len(F)} edges; independent check {ok}  "
    f"({time.time()-t0:.0f}s)"
    + ("   <<< BELOW THE 509 RECORD" if len(Q) < 509 and ok else "")
    + ("   (Parts reached about 5000 by hand)" if 509 <= len(Q) < 5000 else ""))
tag = f"typeT{a.power}_{a.seed}"
save_points(f"{OUT}/{tag}.pts", Q)
save_edges(f"{OUT}/{tag}.edge", len(Q), F)
