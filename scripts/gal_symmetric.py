#!/usr/bin/env python3
"""Impose a GALOIS symmetry on the search, where a geometric one costs too much.

Usage: gal_symmetric.py [--mask 3] [--bound 508] [--degree 4] [--seed N]

Imposing a rotation on the whole answer settles at 1081 vertices (route 22),
because a geometrically symmetric graph has to pay for every vertex three times
and the record is 52 points away from having the symmetry at all.

A Galois conjugation is a different kind of symmetry. It preserves unit distance,
so it is a legitimate constraint to impose, but it is not an isometry: a
galois3-symmetric graph can look completely irregular in the plane and pays no
geometric price. And the record is only **15** points away from having it, which
is the strongest evidence in this repository that small graphs with this symmetry
exist.

So: start from G union galois3(G), which is 524 points, galois3-closed and
5-chromatic because it contains the record; constrain the master to take each
orbit {p, galois3(p)} whole; and ask for 508.
"""
import os, sys, argparse, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn import load_vtx, verify
from hn.symmetry import galois
from hn.io import save_points, save_edges
from hn.graph import induced
from hn.construct import unit_vector_family, ball, dedup, edges, rotate, ROT
from hn.hitting import search

OUT = os.path.join(os.path.dirname(__file__), "..", "out")
ap = argparse.ArgumentParser()
ap.add_argument("--graph", default="data/vtx/509.vtx")
ap.add_argument("--mask", type=int, default=3)
ap.add_argument("--bound", type=int, default=508)
ap.add_argument("--degree", type=int, default=4)
ap.add_argument("--depth", type=int, default=4)
ap.add_argument("--radius", type=float, default=3.2)
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--time", type=float, default=None)
ap.add_argument("--pairs", type=int, default=0)
a = ap.parse_args()
log = lambda s: print(s, flush=True)
g = lambda p: galois(p, a.mask)

G = load_vtx(a.graph)
U = dedup(list(G) + [g(p) for p in G])
log(f"{os.path.basename(a.graph)}: {len(G)} vertices; with its galois{a.mask} image, "
    f"{len(U)} -- and that union is closed under the conjugation")

W = unit_vector_family(2)
B = ball(W, a.depth, a.radius)
LAT = dedup(B + [rotate(p, ROT["theta4"]) for p in B])
Uk = {p.key() for p in U}
P = list(U) + [p for p in LAT if p.key() not in Uk]
E = edges(P)
inU = set(range(len(U)))
deg = collections.Counter()
for u, v in E:
    if (u in inU) != (v in inU):
        deg[v if u in inU else u] += 1
cand = [i for i in range(len(U), len(P)) if deg[i] >= a.degree]
P, E = induced(P, E, sorted(inU | set(cand)))

# close the pool under the conjugation, so that no orbit is half in it
for _ in range(3):
    have = {p.key() for p in P}
    add = [q for p in P for q in (g(p),) if q.key() not in have]
    if not add:
        break
    P = dedup(list(P) + add)
E = edges(P)
idx = {p.key(): i for i, p in enumerate(P)}
orbits, seen = [], set()
for i, p in enumerate(P):
    if i in seen:
        continue
    j = idx[g(p).key()]
    orbits.append(sorted({i, j}))
    seen |= {i, j}
fixed_pts = sum(1 for o in orbits if len(o) == 1)
start = sorted(idx[p.key()] for p in U)
log(f"pool {len(P)} points, {len(E)} edges; {len(orbits)} orbits "
    f"({fixed_pts} fixed by the conjugation), so {len(orbits)} decisions for {len(P)} points")
assert verify(P, E, start, triangle=None), "the symmetrised start is not 5-chromatic"
log(f"start: {len(start)} vertices, verified 5-chromatic, bound {a.bound}")


def save(best):
    Q, F = induced(P, E, sorted(best))
    tag = f"galsym{a.mask}_{a.seed}"
    save_points(f"{OUT}/{tag}.pts", Q)
    save_edges(f"{OUT}/{tag}.edge", len(Q), F)
    log(f"  saved {len(Q)} vertices, {len(F)} edges"
        + ("   <<< BELOW THE 509 RECORD" if len(Q) < 509 else ""))


best, proven = search(P, E, start=start, bound=a.bound, time_limit=a.time,
                      cuts_per_iter=2, seed=a.seed, log=log, on_improve=save,
                      orbits=orbits, grow_every=2, bootstrap_pairs=a.pairs,
                      bootstrap_essential=False, bootstrap_critical=False)
if best is not None:
    save(best)
    log(f"best {len(best)} vertices; proven minimum over this symmetric pool: {proven}")
