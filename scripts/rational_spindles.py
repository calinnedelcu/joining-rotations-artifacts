#!/usr/bin/env python3
"""Joining rotations at RATIONAL squared radii, which no sweep has ever covered.

Usage: rational_spindles.py [--depth 4] [--radius 5.05] [--only 7/3,13/3]

The spindle condition is not cos = (2i-1)/(2i) for integer i.  A rotation carries a
point at squared distance d^2 = a/b from the centre to unit distance from itself
exactly when

    cos = (2a - b) / (2a),      sin = sqrt(b(4a - b)) / (2a)

and the depth-4 radius-5 ball realises **55 rational squared radii that admit a
spindle, only 10 of which this project ever swept** (route 48).  Several of the
missing ones need nothing but sqrt3 or sqrt11 -- they live in the classical field,
where the record itself lives, and nobody has tested them.
"""
import os, sys, time, math, argparse, collections
from fractions import Fraction
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.field import K
from hn.construct import unit_vector_family, ball, dedup, edges, rotate, to_float
from hn.sat import find_triangle
from hn.minimise import verify
from hn.graph import induced
from hn.io import save_points, save_edges

ap = argparse.ArgumentParser()
ap.add_argument("--depth", type=int, default=4)
ap.add_argument("--radius", type=float, default=5.05)
ap.add_argument("--only", default=None, help="comma-separated d^2 values, e.g. 7/3,13/3")
ap.add_argument("--degree", type=int, default=4)
a = ap.parse_args()
log = lambda s: print(f"[{time.strftime('%H:%M:%S')}] {s}", flush=True)


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


def squarefree(m):
    sq = 1
    for q in range(2, int(math.isqrt(m)) + 1):
        while m % (q * q) == 0:
            m //= q * q
            sq *= q
    return sq, m


W = unit_vector_family(2)
L = ball(W, a.depth, a.radius)
log(f"ball depth {a.depth} radius {a.radius}: {len(L)} points")
shells = collections.Counter()
for p in L:
    n = p.norm2()
    if not any(n.n[1:]):
        shells[Fraction(n.n[0], n.d)] += 1
want = None
if a.only:
    want = {Fraction(x) for x in a.only.split(",")}
for f in sorted(shells):
    A, B = f.numerator, f.denominator
    if 4 * A - B <= 0:
        continue
    if want is not None and f not in want:
        continue
    sq, rad = squarefree(B * (4 * A - B))
    try:
        cs = (K.rat(2 * A - B, 2 * A), K.root(rad) * K.rat(sq, 2 * A))
    except AssertionError:
        log(f"d^2={f}: needs sqrt{rad}, not in this field")
        continue
    if not (cs[0] * cs[0] + cs[1] * cs[1]).is_one():
        log(f"d^2={f}: cos/sin do not have modulus 1 -- skipped")
        continue
    t = time.time()
    R = [rotate(p, cs) for p in L]
    Lk = {p.key() for p in L}
    inside = len(Lk & {p.key() for p in R})
    U = dedup(L + R)
    E = edges(U)
    keep = kcore(len(U), E, a.degree)
    P2, E2 = induced(U, E, keep)
    tri = find_triangle(len(P2), E2)
    five = verify(P2, E2, triangle=tri) if tri else None
    log(f"d^2={str(f):>7} ({shells[f]:3d} shell pts, cos={2*A-B}/{2*A}, "
        f"sin={sq}sqrt{rad}/{2*A}): keeps {inside} inside, union {len(U)}, "
        f"{a.degree}-core {len(P2)}; chi>=5 {five}  ({time.time()-t:.0f}s)"
        + ("   <<<<< A JOINING ROTATION" if five else ""))
    if five:
        tag = f"rs_{A}_{B}"
        save_points(f"out/{tag}.pts", P2)
        save_edges(f"out/{tag}.edge", len(P2), E2)
        log(f"   saved out/{tag}.pts")
