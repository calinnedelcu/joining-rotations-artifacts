#!/usr/bin/env python3
"""Sweep the joining rotations that a radius-2.2 ball could never reach.

Usage: new_rotations.py [--radius 4.0] [--depth 4] [--fields 19,17,43,47,59,35]

The 30-vector Moser lattice needs sqrt33, so the field must contain sqrt3 and
sqrt11; the third generator m is free.  Whatever m is, the lattice realises the
same integer squared radii -- measured, 1, 3, 4, 5, 7, 9, 11, 12, 13, 15, 16 --
and a spindle theta_i acts on the shell at radius sqrt(i) if and only if
sqrt(4i-1) lies in the field.  That pairs each radius with the one m that unlocks
it:

    i = 4   needs sqrt15 = sqrt3*sqrt5     m = 5    theta_4, the classical record
    i = 16  needs sqrt63 = 3*sqrt7         m = 7    theta_16, found in route 44
    i = 5   needs sqrt19                   m = 19
    i = 9   needs sqrt35                   m = 35
    i = 11  needs sqrt43                   m = 43
    i = 12  needs sqrt47                   m = 47
    i = 13  needs sqrt51 = sqrt3*sqrt17    m = 17
    i = 15  needs sqrt59                   m = 59

Two of those eight are known to work and six have never been tested, because every
sweep in this repository used a ball of radius 2.2 to 2.53 and the shells for
i > 4 are all outside it.
"""
import os, sys, time, argparse, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import hn.field as F
from hn.field import set_primes, K

ap = argparse.ArgumentParser()
ap.add_argument("--radius", type=float, default=4.0)
ap.add_argument("--depth", type=int, default=4)
ap.add_argument("--fields", default="19,17,43,47,59,35")
a = ap.parse_args()
log = lambda s: print(s, flush=True)
# The radius-4 ball that built this table could not reach the shells at 20, 21 and
# 23 -- a sum of four unit vectors cannot exceed radius 4, so --radius 5 was a no-op.
# Depth 5 realises them: 36, 60 and 36 points.  That is route 44's own bug one notch
# out, and route 44 exists because the same bug hid theta_16 from everyone for years.
WANT = {19: 5, 35: 9, 43: 11, 47: 12, 17: 13, 59: 15, 7: 16, 5: 4,
        79: 20, 83: 21, 91: 23}


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


for m in [int(x) for x in a.fields.split(",")]:
    i = WANT[m]
    set_primes((3, 11, m))
    import hn.construct as C
    C.refresh_field()
    from hn.construct import unit_vector_family, ball, dedup, edges, rotate, to_float
    from hn.sat import find_triangle
    from hn.minimise import verify
    from hn.graph import induced
    from hn.io import save_points, save_edges
    mm = 4 * i - 1
    sq = None
    for s in F.squarefree_divisors():
        if mm % s == 0 and round((mm // s) ** 0.5) ** 2 == mm // s:
            sq = (s, round((mm // s) ** 0.5))
            break
    if sq is None:
        log(f"Q(sqrt3,sqrt11,sqrt{m}): theta_{i} needs sqrt{mm}, not in this field")
        continue
    cs = (K.rat(2 * i - 1, 2 * i), K.root(sq[0]) * K.rat(sq[1], 2 * i))
    if not (cs[0] * cs[0] + cs[1] * cs[1]).is_one():
        log(f"Q(sqrt3,sqrt11,sqrt{m}): theta_{i} is not a rotation here")
        continue
    t = time.time()
    W = unit_vector_family(2)
    L = ball(W, a.depth, a.radius)
    shell = sum(1 for p in L if abs(to_float(p.norm2()) - i) < 1e-9)
    if not shell:
        log(f"Q(sqrt3,sqrt11,sqrt{m}): theta_{i} has no shell at radius sqrt{i}")
        continue
    U = dedup(L + [rotate(p, cs) for p in L])
    E = edges(U)
    keep = kcore(len(U), E, 4)
    P2, E2 = induced(U, E, keep)
    tri = find_triangle(len(P2), E2)
    five = verify(P2, E2, triangle=tri) if tri else None
    log(f"Q(sqrt3,sqrt11,sqrt{m}): theta_{i} = arccos({2*i-1}/{2*i}), "
        f"sin = {sq[1]}sqrt{sq[0]}/{2*i}; {shell} shell points; union {len(U)}, "
        f"4-core {len(P2)}/{len(E2)}; chi>=5 {five}  ({time.time()-t:.0f}s)"
        + ("   <<<<< A NEW JOINING ROTATION" if five else ""))
    if five:
        save_points(f"out/rot_m{m}_t{i}.pts", P2)
        save_edges(f"out/rot_m{m}_t{i}.edge", len(P2), E2)
        log(f"    saved out/rot_m{m}_t{i}.pts")
