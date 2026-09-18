#!/usr/bin/env python3
"""Is the heptagonal lattice 5-chromatic under a spindle rotation?

Usage: cyclo_sweep.py [--conductor 42] [--depth 3] [--radius 2.2] [--degree 4]

The classical construction is  L union theta_4(L)  with L the hexagonal Moser
lattice, and the three conditions that make theta_4 work (docs/ATTEMPTS.md) are
that it is a spindle rotation, that its radical lives in the field, and that it
moves the lattice off itself.  Nothing in those conditions mentions sqrt5 or the
hexagon: they are conditions on a lattice and a rotation, and the search for
them has only ever been run inside multiquadratic fields.

Q(zeta_42) is the smallest field holding both a lattice of 42 unit directions
and sqrt(-7), so it admits theta_2 = arccos(3/4) -- a joining rotation that no
multiquadratic field can express, in the lattice Haugland's 2026
Moser-spindle-free graph lives in.  This runs the classical test there.
"""
import os, sys, time, argparse, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import hn.cyclo as C
from hn.cyclo import Cyc, ball, edges, dedup, spindle
from hn.sat import find_triangle
from hn.minimise import verify
from hn.graph import induced

ap = argparse.ArgumentParser()
ap.add_argument("--conductor", type=int, default=42)
ap.add_argument("--depth", type=int, default=3)
ap.add_argument("--radius", type=float, default=2.2)
ap.add_argument("--degree", type=int, default=4)
ap.add_argument("--imax", type=int, default=60)
a = ap.parse_args()
log = lambda s: print(s, flush=True)

C.set_conductor(a.conductor)
log(f"Q(zeta_{a.conductor}): degree {C.DEG} over Q")
G = [Cyc.zeta(k) for k in range(a.conductor)]
L = ball(G, a.depth, a.radius)
Lk = {p.key() for p in L}
log(f"lattice: {len(G)} unit directions, depth {a.depth}, radius {a.radius} "
    f"-> {len(L)} points")


def kcore(n, E, dmin):
    adj = collections.defaultdict(set)
    for u, v in E:
        adj[u].add(v)
        adj[v].add(u)
    alive = set(range(n))
    q = [v for v in alive if len(adj[v]) < dmin]
    while q:
        v = q.pop()
        if v not in alive:
            continue
        alive.discard(v)
        for w in adj[v]:
            if w in alive:
                adj[w].discard(v)
                if len(adj[w]) < dmin:
                    q.append(w)
    return sorted(alive)


def report(name, P):
    t = time.time()
    E = edges(P)
    keep = kcore(len(P), E, a.degree)
    P2, E2 = induced(P, E, keep)
    if len(P2) < 10:
        log(f"  {name}: {len(P)} points, {len(E)} edges -> {a.degree}-core empty")
        return None
    tri = find_triangle(len(P2), E2)
    five = verify(P2, E2, triangle=tri)
    log(f"  {name}: {len(P)} points, {len(E)} edges -> {a.degree}-core {len(P2)} "
        f"points/{len(E2)} edges; chi>=5 {five}  ({time.time()-t:.0f}s)"
        + ("   <<<<< 5-CHROMATIC" if five else ""))
    return (P2, E2) if five else None


log("the lattice alone (the classical obstruction: a 4-colourable lattice)")
report("L", L)

sp = [(i, spindle(i)) for i in range(1, a.imax + 1)]
sp = [(i, u) for i, u in sp if u is not None]
log(f"spindle rotations in this field: {[i for i, _ in sp]}")
for i, u in sp:
    RL = [u * p for p in L]
    inside = len(Lk & {p.key() for p in RL})
    U = dedup(L + RL)
    # An edge is a cross edge when it exists only because of the union.  Counting
    # by index instead puts the shared origin in both halves, which credits the
    # rotation with the origin's own 42 edges twice over and hides a union that
    # is really two disjoint copies.
    RLk = {p.key() for p in RL}
    side = [(p.key() in Lk, p.key() in RLk) for p in U]
    cross = sum(1 for x, y in edges(U)
                if not (side[x][0] and side[y][0]) and not (side[x][1] and side[y][1]))
    log(f"theta_{i}: keeps {inside} of {len(L)} images inside the lattice, "
        f"union {len(U)}, cross edges {cross}")
    if inside == len(L):
        log("  the rotation maps the lattice to itself; no new edges possible")
        continue
    if cross == 0:
        # a spindle rotation only bites where the lattice has points at distance
        # sqrt(i) from the centre; without one the union is two disjoint copies
        log(f"  no cross edge: the lattice has no point at distance sqrt({i})")
        continue
    hit = report(f"L + theta_{i}(L)", U)
    if hit:
        from hn.io import save_points
        P2, E2 = hit
        log(f"  *** saving {len(P2)} vertices to out/cyc{a.conductor}_t{i}.txt")
        with open(f"out/cyc{a.conductor}_t{i}.txt", "w") as f:
            for p in P2:
                z = p.complex()
                f.write(f"{z.real!r} {z.imag!r} {p.n} {p.d}\n")
