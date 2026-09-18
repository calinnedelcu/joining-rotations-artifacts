#!/usr/bin/env python3
"""Minimise the large part of a construction with SEVERAL small parts.

Usage: multi_wing.py [--wings 2] [--pool v412e2106.vtx] [--S v136e564.vtx]
                     [--L v374e1860.vtx] [--time SECONDS] [--seed N]
                     [--symmetry K] [--bound B]

Every small 5-chromatic unit-distance graph published so far has exactly two
parts, a large one and one rotated small one.  The Galois map sqrt5 -> -sqrt5
fixes the large part and carries theta_4(S) to theta_4^{-1}(S), so a mirror
wing comes for free and L union theta_4(S) union theta_4^{-1}(S) is already
5-chromatic.  Two wings constrain the large part from both sides, so it may
admit far more interface patterns and be far smaller.

The arithmetic is unforgiving: the total is |L| + w*(|S|-1), so with two
wings of 136 the large part has to reach 238 to beat 509, against 374 with
one wing.  This measures how far it actually falls.
"""
import os, sys, argparse, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn import load_vtx, load_edges
from hn.io import save_points, save_edges
from hn.graph import induced
from hn.construct import edges, theta4, dedup, rotate, ROT, ORIGIN
from hn.hitting import search

D = os.path.join(os.path.dirname(__file__), "..", "data", "parts")
OUT = os.path.join(os.path.dirname(__file__), "..", "out")
ap = argparse.ArgumentParser()
ap.add_argument("--wings", type=int, default=2)
ap.add_argument("--pool", default="v412e2106.vtx")
ap.add_argument("--S", default="v136e564.vtx")
ap.add_argument("--L", default="v374e1860.vtx")
ap.add_argument("--time", type=float, default=None)
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--grow", type=int, default=2)
ap.add_argument("--bound", type=int, default=None)
ap.add_argument("--symmetry", type=int, default=0)
a = ap.parse_args()

pool = load_vtx(f"{D}/{a.pool}")
S = load_vtx(f"{D}/{a.S}")
L = load_vtx(f"{D}/{a.L}")
wings = []
for w in range(a.wings):
    if w == 0:
        wings += [theta4(p) for p in S]
    elif w == 1:
        wings += [theta4(p, inverse=True) for p in S]
    else:                       # further wings: rotate the first by 60 degrees
        prev = [theta4(p) for p in S]
        for _ in range(w - 1):
            prev = [rotate(p, ROT["theta1"]) for p in prev]
        wings += prev
P = dedup(list(pool) + wings)
E = edges(P)
poolkeys = {p.key() for p in pool}
fixed = sorted(i for i, p in enumerate(P) if p.key() not in poolkeys)
Lkeys = {p.key() for p in L}
start = sorted(i for i, p in enumerate(P) if p.key() in Lkeys and i not in set(fixed))
target = 509 - a.wings * (len(S) - 1)
print(f"{a.wings} wings of {a.S} ({len(S)} points each), large-part pool {a.pool}", flush=True)
print(f"graph {len(P)} vertices {len(E)} edges; {len(fixed)} wing vertices fixed; "
      f"start large part {len(start)} free", flush=True)
print(f"to beat 509 the large part must reach {target} vertices "
      f"({target - 1} free)", flush=True)

orbits = None
if a.symmetry:
    from hn.symmetry import rot60
    step, idx, seen, orbits = 6 // a.symmetry, {p.key(): i for i, p in enumerate(P)}, set(), []
    fx = set(fixed)
    for i in range(len(P)):
        if i in seen or i in fx:
            continue
        orb, q, ok = [], P[i], True
        for _ in range(a.symmetry):
            j = idx.get(q.key())
            if j is None or j in fx:
                ok = False
                break
            orb.append(j)
            for _ in range(step):
                q = rot60(q)
        if ok:
            orb = sorted(set(orb))
            seen |= set(orb)
            if len(orb) > 1:
                orbits.append(orb)
    print(f"symmetry {a.symmetry}: {len(orbits)} orbits", flush=True)


def save(best):
    tag = f"wing{a.wings}_{a.pool.split('.')[0]}_{a.seed}"
    keep = sorted(set(best) | set(fixed))
    P2, E2 = induced(P, E, keep)
    save_points(f"{OUT}/best_{tag}.pts", P2)
    save_edges(f"{OUT}/best_{tag}.edge", len(P2), E2)
    print(f"  saved {len(P2)} vertices, {len(E2)} edges"
          + ("   <<< BELOW 509" if len(P2) < 509 else ""), flush=True)


best, proven = search(P, E, start=start, bound=a.bound, time_limit=a.time,
                      cuts_per_iter=2, seed=a.seed, log=lambda s: print(s, flush=True),
                      on_improve=save, fixed=fixed, grow_every=a.grow, orbits=orbits)
if best is not None:
    save(best)
    print(f"best large part: {len(best)+1} vertices -> total {len(best)+1+a.wings*(len(S)-1)}; "
          f"proven over this pool: {proven}", flush=True)
