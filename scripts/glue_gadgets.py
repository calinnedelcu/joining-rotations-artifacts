#!/usr/bin/env python3
"""Glue Parts' gadgets to each other, across families, and look for 5-chromatic.

Usage: glue_gadgets.py [--max 700] [--rotations id,theta4,...] [--limit N]

Parts' data comes with an inventory (data/parts/graphs.txt) of the MINIMAL graph
for each forcing family, every one anchored at the origin in the same lattice:

    mono-pair        367 at distance 8/3,  421 at 8/sqrt3
    non-mono-pair    214 at distance 3,  308 to 319 at four other distances
    non-mono-triple  159 at sqrt7,  221 at sqrt3,  250, 265

He minimised each family on its own, and built the record from one L and one S.
Nothing in the literature glues two of these to each other -- and since they
share a lattice and an origin, their union is a unit-distance graph for free.
The arithmetic is inviting: 159 + 214 = 373, 159 + 250 = 409, 214 + 265 = 479,
all comfortably under 509, and a union is 5-chromatic as soon as the two
gadgets force contradictory things about the same points.

This tries every pair, optionally under a rotation of the second gadget, and
reports any 5-chromatic union.  Cheap: the 4-colourable answer comes back in
well under a second, so only a genuine hit costs anything.
"""
import os, sys, glob, time, argparse, collections, itertools
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.io import load_vtx, save_points, save_edges
from hn.construct import edges, dedup, rotate, ROT, refresh_field
from hn.sat import find_triangle
from hn.minimise import verify
from hn.graph import induced
from hn.symmetry import rot60, reflect_x, galois

OUT = os.path.join(os.path.dirname(__file__), "..", "out")
ap = argparse.ArgumentParser()
ap.add_argument("--max", type=int, default=700, help="skip unions bigger than this")
ap.add_argument("--rotations", default="id")
ap.add_argument("--degree", type=int, default=4)
ap.add_argument("--limit", type=int, default=0)
a = ap.parse_args()
log = lambda s: print(s, flush=True)


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


def rotk(k, p):
    for _ in range(k):
        p = rot60(p)
    return p


MAPS = {"id": lambda p: p}
for k in range(1, 6):
    MAPS[f"rot{60*k}"] = (lambda k: (lambda p: rotk(k, p)))(k)
MAPS["refl"] = reflect_x
for m in (1, 2, 3, 4, 5, 6, 7):
    MAPS[f"galois{m}"] = (lambda m: (lambda p: galois(p, m)))(m)
for name in ("theta3", "theta4", "theta3/2"):
    if name in ROT:
        MAPS[name] = (lambda cs: (lambda p: rotate(p, cs)))(ROT[name])

files = sorted(glob.glob("data/parts/*.vtx")) + sorted(glob.glob("data/vtx/*.vtx"))
G = {}
for f in files:
    try:
        G[f] = load_vtx(f)
    except Exception:
        pass                      # T721 lives in another field; not gluable to these
log(f"{len(G)} gadgets loaded, {len(MAPS)} maps available; "
    f"rotations requested: {a.rotations}")

names = sorted(G, key=lambda f: len(G[f]))
rots = [r.strip() for r in a.rotations.split(",")]
tested = hits = 0
t0 = time.time()
for rname in rots:
    if rname not in MAPS:
        log(f"  no such map: {rname}")
        continue
    f_ = MAPS[rname]
    for fa, fb in itertools.combinations_with_replacement(names, 2):
        if fa == fb and rname == "id":
            continue
        A, B = G[fa], G[fb]
        if len(A) + len(B) > a.max:
            continue
        U = dedup(list(A) + [f_(p) for p in B])
        if len(U) > a.max:
            continue
        E = edges(U)
        keep = kcore(len(U), E, a.degree)
        if len(keep) < 10:
            continue
        P2, E2 = induced(U, E, keep)
        tri = find_triangle(len(P2), E2)
        if tri is None:
            continue
        tested += 1
        if verify(P2, E2, triangle=tri):
            hits += 1
            log(f"  *** 5-CHROMATIC: {os.path.basename(fa)} + {rname}"
                f"({os.path.basename(fb)}) -> union {len(U)}, 4-core {len(P2)}"
                + ("   <<<<< BELOW THE 509 RECORD" if len(P2) < 509 else ""))
            tag = f"glue_{len(P2)}_{os.path.basename(fa).split('.')[0]}_{rname.replace('/','')}"
            save_points(f"{OUT}/{tag}.pts", P2)
            save_edges(f"{OUT}/{tag}.edge", len(P2), E2)
        if a.limit and tested >= a.limit:
            break
    log(f"  [{rname}] {tested} unions tested, {hits} five-chromatic "
        f"({time.time()-t0:.0f}s)")
log(f"done: {tested} tested, {hits} five-chromatic")
