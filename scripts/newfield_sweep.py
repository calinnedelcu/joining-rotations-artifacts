#!/usr/bin/env python3
"""Does the new field's lattice force anything, at any spindle?

Usage: newfield_sweep.py [--primes 2,3,5] [--depth 4] [--radius 2.2]

Q(sqrt2, sqrt3) is reachable now (see route 40) and is structurally the closest
thing to the classical field found so far: it has 45-degree rotations
(sqrt2/2, sqrt2/2) as well as 60-degree ones, so the 24 directions at multiples of
15 degrees are all exact, and Q(sqrt2, sqrt3, sqrt5) admits theta_4 because
sin theta_4 = sqrt15/8.  Degree 4 over Q, so the lattice has Z-rank 8, the same as
the Moser lattice.

Measured, it is also DENSER than the Moser lattice -- 9.2 to 10.2 edges per point
against 7.1 -- and the union L + theta_4(L) is still 4-colourable at 9649 points
where the classical one is 5-chromatic at 4525.  Density is not the missing
ingredient.

What the classical union really needs is that L forces the ORIGIN and some
radius-2 point to share a colour; then rotating about the origin fixes one end and
sends the other to unit distance from itself.  So test that directly, at every
spindle the field admits, with the virtual-edge test rather than the union: it is
the same cost and it says which pair fails.
"""
import os, sys, time, argparse, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.field import set_primes, K, Pt
ap = argparse.ArgumentParser()
ap.add_argument("--primes", default="2,3,5")
ap.add_argument("--depth", type=int, default=4)
ap.add_argument("--radius", type=float, default=2.2)
ap.add_argument("--dirs", default="15", help="15 for the 24 directions at 15 degrees, "
                                            "or t721 for the ones that graph uses")
a = ap.parse_args()
set_primes(tuple(int(t) for t in a.primes.split(",")))
import hn.construct as C
C.refresh_field()
from hn.construct import edges, dedup, ball, rotate, to_float
from hn.io import load_vtx
from hn.sat import find_triangle
from hn.minimise import verify
from hn.graph import induced
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


def spindles():
    """theta_i available in this field, with the squared radius it spindles."""
    from math import isqrt
    from hn.field import squarefree_divisors
    out = []
    for i in range(1, 60):
        m = 4 * i - 1
        for s in squarefree_divisors():
            if m % s == 0 and isqrt(m // s) ** 2 == m // s:
                out.append((i, (K.rat(2 * i - 1, 2 * i),
                                K.root(s) * K.rat(isqrt(m // s), 2 * i))))
                break
    return out


if a.dirs == "15":
    r2, r6 = K.root(2), K.root(6)
    step = ((r6 + r2) * K.rat(1, 4), (r6 - r2) * K.rat(1, 4))
    W, v = [], Pt(K.rat(1), K.zero())
    for _ in range(24):
        W.append(v)
        v = rotate(v, step)
else:
    G = load_vtx("data/vtx/T721.vtx")
    E0 = edges(G)
    W = dedup([G[j] - G[i] for i, j in E0] + [G[i] - G[j] for i, j in E0])
L = ball(W, a.depth, a.radius)
EL = edges(L)
log(f"field Q(sqrt{a.primes.replace(',', ', sqrt')}), {len(W)} directions, depth "
    f"{a.depth}, radius {a.radius}: {len(L)} points, {len(EL)} edges "
    f"({2*len(EL)/max(1,len(L)):.1f} per point)")
idx = {p.key(): i for i, p in enumerate(L)}
origin = idx.get(Pt(K.zero(), K.zero()).key())
sp = spindles()
log(f"spindles here: {[i for i, _ in sp]}")
for i, cs in sp:
    if i == 1:
        continue
    # a point at squared distance i from the origin, if the lattice has one
    targets = [j for j, p in enumerate(L)
               if abs(to_float(p.norm2()) - i) < 1e-9]
    if not targets or origin is None:
        log(f"  theta_{i}: no lattice point at radius sqrt{i}")
        continue
    j = targets[0]
    EV = sorted(set(EL) | {(min(origin, j), max(origin, j))})
    keep = kcore(len(L), EV, 4)
    if origin not in keep or j not in keep:
        log(f"  theta_{i}: the pair does not survive the 4-core")
        continue
    P2, E2 = induced(L, EV, keep)
    tri = find_triangle(len(P2), E2)
    t = time.time()
    forced = verify(P2, E2, triangle=tri)
    log(f"  theta_{i}: {len(targets)} points at radius sqrt{i}; the ball forces the "
        f"origin and one of them monochromatic: {forced}  ({time.time()-t:.0f}s)"
        + ("   <<<<< a forcer in this field" if forced else ""))
