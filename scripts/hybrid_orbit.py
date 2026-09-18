#!/usr/bin/env python3
"""Search the record's own SHAPE: a symmetric bulk plus a few breakers.

Usage: hybrid_orbit.py [--bound 508] [--seed N] [--ring 1] [--time S]

Imposing the 120-degree rotation on the whole answer gives 1081 vertices
(route 22): a fully symmetric graph is expensive, because every vertex it needs
costs three.  Freezing the record's symmetric core instead (complete_core.py)
is the opposite extreme -- 457 of the 509 points are nailed down and only the
52 breakers may move.

The record is neither.  It is a 457-point core closed under the rotation plus
52 points that break it, and every published record has the same profile (510:
466 + 44, 517: 505 + 12).  So search for exactly that: let the bulk be chosen
one ORBIT at a time, and let a designated set of points near the seam be chosen
one POINT at a time.

That is the record's shape with none of the record's choices.  It contains the
record as a feasible solution -- its core is a union of constrained orbits, its
breakers are all free -- and the symmetry is a restriction on the search only,
so the count of vertices is unchanged and a solution at 508 is a solution.

The free set is the breakers together with everything within `ring` edges of
them, closed under the rotation so that no orbit is half free.  Widening the
ring searches more ground and constrains the master less.
"""
import os, sys, argparse, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.io import load_points, save_points, save_edges
from hn.graph import induced
from hn.construct import edges, dedup
from hn.symmetry import rot60
from hn.hitting import search
from hn import load_vtx, verify

OUT = os.path.join(os.path.dirname(__file__), "..", "out")
ap = argparse.ArgumentParser()
ap.add_argument("--pool", default="out/symcore.pts")
ap.add_argument("--start", default="data/vtx/509.vtx")
ap.add_argument("--bound", type=int, default=508)
ap.add_argument("--ring", type=int, default=1, help="how many edges out from the breakers is free")
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--time", type=float, default=None)
ap.add_argument("--pairs", type=int, default=0)
a = ap.parse_args()
log = lambda s: print(s, flush=True)


def r120(p):
    return rot60(rot60(p))


G = load_vtx(a.start)
Gk = {p.key() for p in G}
P = load_points(a.pool)
P = dedup(list(P) + [p for p in G if p.key() not in {q.key() for q in P}])

# close the pool under the rotation, so that every orbit is whole
for _ in range(3):
    have = {p.key() for p in P}
    add = [q for p in P for q in (r120(p),) if q.key() not in have]
    if not add:
        break
    P = dedup(list(P) + add)
E = edges(P)
idx = {p.key(): i for i, p in enumerate(P)}
n = len(P)

orb_of, orbits = {}, []
for i, p in enumerate(P):
    if i in orb_of:
        continue
    cyc, q = [], p
    for _ in range(3):
        cyc.append(idx[q.key()])
        q = r120(q)
    cyc = sorted(set(cyc))
    for v in cyc:
        orb_of[v] = len(orbits)
    orbits.append(cyc)

core = {i for i, p in enumerate(P) if p.key() in Gk and
        all(r120i.key() in Gk for r120i in (r120(p), r120(r120(p))))}
breakers = {idx[p.key()] for p in G} - core
log(f"pool {n} points, {len(E)} edges, {len(orbits)} rotation orbits; "
    f"start {len(G)} = core {len(core)} + breakers {len(breakers)}")

adj = collections.defaultdict(set)
for u, v in E:
    adj[u].add(v)
    adj[v].add(u)
free = set(breakers)
for _ in range(a.ring):
    free |= {w for v in free for w in adj[v]}
for _ in range(3):                       # close the free set under the rotation
    free |= {v for u in free for v in orbits[orb_of[u]]}
keep_orbits = [o for o in orbits if not (set(o) & free)]
log(f"free set {len(free)} points (breakers + {a.ring} edge ring, rotation-closed); "
    f"{len(keep_orbits)} orbits constrained, "
    f"{len(free) + len(keep_orbits)} decisions instead of {n}")

start = sorted(idx[p.key()] for p in G)
assert verify(P, E, start, triangle=None), "the start graph is not 5-chromatic"
assert all(set(o) <= set(start) or not (set(o) & set(start)) for o in keep_orbits), \
    "the start is not representable: a constrained orbit is only partly in it"
log(f"start verified 5-chromatic and representable under the orbit constraints")


def save(best):
    tag = f"hyb{a.ring}_{a.seed}"
    Q, F = induced(P, E, sorted(best))
    save_points(f"{OUT}/{tag}.pts", Q)
    save_edges(f"{OUT}/{tag}.edge", len(Q), F)
    log(f"  saved {len(Q)} vertices, {len(F)} edges"
        + ("   <<< BELOW THE 509 RECORD" if len(Q) < 509 else ""))


best, proven = search(P, E, start=start, bound=a.bound, time_limit=a.time,
                      cuts_per_iter=2, seed=a.seed, log=log, on_improve=save,
                      orbits=keep_orbits, grow_every=2, bootstrap_pairs=a.pairs,
                      bootstrap_essential=False, bootstrap_critical=False)
if best is not None:
    save(best)
    log(f"best {len(best)} vertices; proven minimum over this pool: {proven}")
