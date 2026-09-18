#!/usr/bin/env python3
"""Delete whole ORBITS from a symmetric pool, keeping it 5-chromatic.

Usage: orbit_shrink.py POOL.pts [--symmetry 3] [--seed N]

A minimising master searches from below: it returns the smallest set that
satisfies the cuts learned so far, and since 5-chromatic graphs only exist
above five hundred vertices, every proposal it makes is 4-colourable and every
iteration merely raises a lower bound. Climbing from 420 to 500 that way is the
same work as proving a lower bound of 500 for the pool.

Descending is the right direction. The pool is symmetric and 5-chromatic to
begin with, so delete orbits from it while it stays 5-chromatic, one persistent
oracle proposing and one fresh solver confirming the answer. What comes out is a
minimal symmetric 5-chromatic graph, of size 1 + k*(orbits kept), and if that is
under 509 it is a record.

Parts' best symmetric result was a 376-vertex large part, but he only ever
imposed symmetry on one part at a time. This imposes it on the whole graph.
"""
import os, sys, time, random, argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.io import load_points, save_points, save_edges
from hn.graph import induced
from hn.construct import edges
from hn.symmetry import rot60
from hn.hitting import Oracle, kcore
from hn import verify, find_triangle

OUT = os.path.join(os.path.dirname(__file__), "..", "out")
ap = argparse.ArgumentParser()
ap.add_argument("pool")
ap.add_argument("--symmetry", type=int, default=3)
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--time", type=float, default=None)
a = ap.parse_args()
rng = random.Random(a.seed)
log = lambda s: print(s, flush=True)

P = load_points(a.pool)
E = edges(P)
idx = {p.key(): i for i, p in enumerate(P)}
step = 6 // a.symmetry
seen, orbits = set(), []
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
        continue
    orb = sorted(set(orb))
    seen |= set(orb)
    orbits.append(orb)
log(f"pool {len(P)} points, {len(E)} edges; {len(orbits)} orbits under the "
    f"{a.symmetry}-fold rotation")
assert verify(P, E, triangle=find_triangle(len(P), E)), "the pool is not 5-chromatic"
log("pool verified 5-chromatic")

tri = find_triangle(len(P), E)
o = Oracle(len(P), E, triangle=tri)
kept = set(range(len(P)))
protected = set(tri or ())
t0, removed, rounds = time.time(), 0, 0
changed = True
while changed:
    changed = False
    rounds += 1
    order = [g for g in orbits if set(g) <= kept and not (set(g) & protected)]
    rng.shuffle(order)
    for g in order:
        gs = set(g)
        if not gs <= kept:
            continue
        if not o.colourable(sorted(kept - gs)):
            kept -= gs
            removed += len(g)
            changed = True
    live = set(kcore(len(P), [(x, y) for x, y in E if x in kept and y in kept], 4))
    kept &= live
    log(f"  round {rounds}: {len(kept)} vertices left "
        f"({removed} removed, {time.time()-t0:.0f}s)")
    if a.time and time.time() - t0 > a.time:
        break
o.close()
keep = sorted(kept)
ok = verify(P, E, keep, triangle=None)
Q, F = induced(P, E, keep)
log(f"result: {len(Q)} vertices, {len(F)} edges; independent check {ok}"
    + ("   <<< BELOW THE 509 RECORD" if len(Q) < 509 and ok else ""))
tag = f"orb{a.symmetry}_{os.path.basename(a.pool).split('.')[0]}_{a.seed}"
save_points(f"{OUT}/{tag}.pts", Q)
save_edges(f"{OUT}/{tag}.edge", len(Q), F)
