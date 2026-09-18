#!/usr/bin/env python3
"""Test the spindle rotations whose radius earlier sweeps never reached.

Usage: big_spindles.py [--radius 3.8] [--depth 4] [--spindles 14,19]

Route 20 concluded that theta_4 is the unique joining rotation, over 83 fields and
about 2700 rotations.  Every one of those sweeps used a ball of radius 2.2 to 2.53,
and a spindle rotation theta_i only acts on lattice points at distance sqrt(i) from
the centre.  Measured:

    ball depth 4 radius 2.2: at radius^2 = 1:30, 3:42, 4:30, 7:0
    ball depth 4 radius 2.8: at radius^2 = 1:30, 3:42, 4:30, 7:60

So at radius 2.2 there is not one point for theta_7 to move, and the test that
dismissed it was vacuous.  The same holds for every spindle past theta_4:
theta_7 needs radius 2.646, theta_14 needs 3.742, theta_19 needs 4.359,
theta_25 needs 5.  Only theta_1, theta_3 and theta_4 were ever actually testable,
which is a mundane reason for theta_4 to look unique.

Retested on a ball that reaches the shell, theta_7 fails honestly -- union
4-colourable at 18439 points where theta_4's is 5-chromatic at 18625.  This
script pushes the radius further for the rest.
"""
import os, sys, time, argparse, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.field import K, Pt
from hn.construct import unit_vector_family, ball, dedup, edges, rotate, to_float
from hn.sat import find_triangle
from hn.minimise import verify
from hn.graph import induced

ap = argparse.ArgumentParser()
ap.add_argument("--radius", type=float, default=3.8)
ap.add_argument("--depth", type=int, default=4)
ap.add_argument("--spindles", default="14")
ap.add_argument("--degree", type=int, default=4)
a = ap.parse_args()
log = lambda s: print(s, flush=True)


def kcore(n, E, d):
    adj = collections.defaultdict(set)
    for u, v in E:
        adj[u].add(v)
        adj[v].add(u)
    alive = set(range(n))
    q = [v for v in alive if len(adj[v]) < d]
    while q:
        v = q.pop()
        if v not in alive:
            continue
        alive.discard(v)
        for w in adj[v]:
            if w in alive:
                adj[w].discard(v)
                if len(adj[w]) < d:
                    q.append(w)
    return sorted(alive)


def spindle(i):
    m = 4 * i - 1
    for s in (1, 3, 5, 11, 15, 33, 55, 165):
        if m % s == 0:
            r = round((m // s) ** 0.5)
            if r * r == m // s:
                try:
                    return (K.rat(2 * i - 1, 2 * i), K.root(s) * K.rat(r, 2 * i))
                except AssertionError:
                    return None
    return None


W = unit_vector_family(2)
t = time.time()
L = ball(W, a.depth, a.radius)
log(f"ball depth {a.depth} radius {a.radius}: {len(L)} points  ({time.time()-t:.0f}s)")
for i in [int(x) for x in a.spindles.split(",")]:
    cs = spindle(i)
    if cs is None:
        log(f"theta_{i}: not in this field")
        continue
    shell = sum(1 for p in L if abs(to_float(p.norm2()) - i) < 1e-9)
    log(f"theta_{i}: needs radius {i**0.5:.3f}, ball has {shell} points there")
    if not shell:
        log("  the ball still does not reach the shell; nothing to move")
        continue
    t = time.time()
    U = dedup(L + [rotate(p, cs) for p in L])
    EU = edges(U)
    keep = kcore(len(U), EU, a.degree)
    P2, E2 = induced(U, EU, keep)
    tri = find_triangle(len(P2), E2)
    five = verify(P2, E2, triangle=tri) if tri else None
    log(f"  union {len(U)} points, {a.degree}-core {len(P2)}/{len(E2)}; chi>=5 {five}"
        f"  ({time.time()-t:.0f}s)" + ("   <<<<< A NEW JOINING ROTATION" if five else ""))
