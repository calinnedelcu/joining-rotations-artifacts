#!/usr/bin/env python3
"""Cut a record along its Galois seam, the tightest one it has.

Usage: gal_core.py GRAPH.vtx [--mask 3] [--degree 4] [--out out/galcore.pts]

A Galois conjugation of the coordinate field sends sqrt3 -> -sqrt3 and
sqrt5 -> -sqrt5.  It preserves unit distance (tests/test_all.py), so it maps a
5-chromatic unit-distance graph to another one, and the subset of a graph that
is closed under it is a graph both share.

Measured over the whole isometry group and all seven conjugations, that seam is
much tighter than the 120-degree rotation the search has been using:

    seam        closed core   breakers   completion that beats 509
    galois3         494          15              14
    rot120          457          52              51
    galois2         374         135             134

So the record is 494 points that survive conjugating two of the three radicals,
plus 15 that do not.  Freeing 15 points and asking for 14 is the smallest
record attempt this repository can pose.
"""
import os, sys, argparse, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn import load_vtx
from hn.symmetry import galois, rot60, reflect_x
from hn.construct import (unit_vector_family, ball, dedup, edges, rotate, ROT)
from hn.io import save_points
from hn.graph import induced

ap = argparse.ArgumentParser()
ap.add_argument("graph")
ap.add_argument("--mask", type=int, default=3)
ap.add_argument("--iso", default="id",
                help="isometry composed with the conjugation: id, rot60..rot300, "
                     "refl, refl.rot60..  A twisted symmetry can cut tighter than "
                     "either factor: 510 splits 494+16 under rot60 o galois7, where "
                     "galois3 alone leaves 478+32")
ap.add_argument("--degree", type=int, default=4)
ap.add_argument("--depth", type=int, default=4)
ap.add_argument("--radius", type=float, default=3.2)
ap.add_argument("--out", default=None)
a = ap.parse_args()
log = lambda s: print(s, flush=True)

def rotk(k, p):
    for _ in range(k):
        p = rot60(p)
    return p


def isometry(name):
    if name == "id":
        return lambda p: p
    refl = name.startswith("refl")
    k = int(name.split("rot")[1]) // 60 if "rot" in name else 0
    return lambda p: rotk(k, reflect_x(p) if refl else p)


iso = isometry(a.iso)
seam = lambda p: iso(galois(p, a.mask))

G = load_vtx(a.graph)
Gk = {p.key() for p in G}
core = []
for p in G:
    q, ok = seam(p), True
    for _ in range(24):                 # orbit under the seam, however long
        if q.key() not in Gk:
            ok = False
            break
        if q.key() == p.key():
            break
        q = seam(q)
    else:
        ok = False
    if ok:
        core.append(p)
ck = {p.key() for p in core}
breakers = [p for p in G if p.key() not in ck]
log(f"{os.path.basename(a.graph)}: {len(G)} vertices; {a.iso} o galois{a.mask}-closed core "
    f"{len(core)}, breakers {len(breakers)}; beating 509 needs {508-len(core)} points")

W = unit_vector_family(2)
B = ball(W, a.depth, a.radius)
LAT = dedup(B + [rotate(p, ROT["theta4"]) for p in B])
P = core + [p for p in LAT if p.key() not in ck]
E = edges(P)
inC = set(range(len(core)))
deg = collections.Counter()
for u, v in E:
    if (u in inC) != (v in inC):
        deg[v if u in inC else u] += 1
cand = [i for i in range(len(core), len(P)) if deg[i] >= a.degree]
P2, E2 = induced(P, E, sorted(inC | set(cand)))
have = {p.key() for p in P2}
missing = [p for p in breakers if p.key() not in have]
P2 = list(P2) + missing
tag = f"{a.iso.replace('.','')}g{a.mask}"
out = a.out or f"out/galcore_{tag}_{os.path.basename(a.graph).split('.')[0]}.pts"
save_points(out, P2)
log(f"pool {len(P2)} points: core {len(core)} first, then {len(P2)-len(core)} candidates "
    f"at degree >= {a.degree} ({len(missing)} of the graph's own breakers had to be added back)")
log(f"wrote {out}")
