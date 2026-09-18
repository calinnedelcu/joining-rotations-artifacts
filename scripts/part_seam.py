#!/usr/bin/env python3
"""Cut one PART along its seam, hold the other part published, and complete it.

Usage: part_seam.py L|S PARTFILE [--mask 1] [--iso id] [--degree 4] [--bound N]

Today's seam trick applied one level down.  The whole record splits 494 + 15
under galois3, which makes a bound-14 search.  Its *parts* split far more
tightly:

    L v374e1868   galois1   core 372   2 breakers    bound 1
    L v374e1860   galois1   core 368   6 breakers    bound 5
    L v374e1872   galois1   core 366   8 breakers    bound 7
    S v136e564    galois1   core 127   9 breakers    bound 8

A Galois conjugation preserves unit distance, so the closed part of a part is
still a legitimate object to hold fixed.  Hold it, hold the *other* part at its
published value, and ask for one fewer point than the record spends: the record
is 373 free + 136 fixed = 509, so a large part of 373 points total beats it, and a
small part of 135 does.

These are the smallest record attempts in the repository -- one to eight free
choices.
"""
import os, sys, argparse, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn import load_vtx, verify
from hn.symmetry import galois, rot60, reflect_x
from hn.io import save_points, save_edges
from hn.graph import induced
from hn.construct import (unit_vector_family, ball, dedup, edges, theta4, norm)
from hn.hitting import search

D = os.path.join(os.path.dirname(__file__), "..", "data", "parts")
OUT = os.path.join(os.path.dirname(__file__), "..", "out")
ap = argparse.ArgumentParser()
ap.add_argument("side", choices=["L", "S"])
ap.add_argument("part")
ap.add_argument("--mask", type=int, default=1)
ap.add_argument("--iso", default="id")
ap.add_argument("--other", default=None, help="the part held published; defaults to "
                                              "v136e564.vtx for L and v374e1860.vtx for S")
ap.add_argument("--degree", type=int, default=4)
ap.add_argument("--depth", type=int, default=4)
ap.add_argument("--radius", type=float, default=2.53)
ap.add_argument("--bound", type=int, default=None)
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--time", type=float, default=None)
a = ap.parse_args()
log = lambda s: print(s, flush=True)


def isometry(name):
    if name == "id":
        return lambda p: p
    refl = name.startswith("refl")
    k = int(name.split("rot")[1]) // 60 if "rot" in name else 0

    def f(p):
        p = reflect_x(p) if refl else p
        for _ in range(k):
            p = rot60(p)
        return p
    return f


iso = isometry(a.iso)
seam = lambda p: iso(galois(p, a.mask))
A = load_vtx(f"{D}/{a.part}" if "/" not in a.part else a.part)
Ak = {p.key() for p in A}
core = []
for p in A:
    q, ok = seam(p), True
    for _ in range(24):
        if q.key() not in Ak:
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
breakers = [p for p in A if p.key() not in ck]
other = a.other or ("v136e564.vtx" if a.side == "L" else "v374e1860.vtx")
B = load_vtx(f"{D}/{other}")
log(f"{a.part}: {len(A)} points, {a.iso} o galois{a.mask} core {len(core)}, "
    f"{len(breakers)} breakers; other part {other} ({len(B)}) held published")

W = unit_vector_family(2)
LAT = ball(W, a.depth, a.radius)
P0 = list(core) + [p for p in LAT if p.key() not in ck]
E0 = edges(P0)
inC = set(range(len(core)))
deg = collections.Counter()
for x, y in E0:
    if (x in inC) != (y in inC):
        deg[y if x in inC else x] += 1
cand = [i for i in range(len(core), len(P0)) if deg[i] >= a.degree]
part_pool = [P0[i] for i in sorted(inC | set(cand))]
have = {p.key() for p in part_pool}
part_pool += [p for p in breakers if p.key() not in have]

if a.side == "L":
    P = dedup(part_pool + [theta4(p) for p in B])
    fixed_keys = {theta4(p).key() for p in B} | ck
    target = 373                      # a large part of 373 points beats 509
else:
    P = dedup(list(B) + [theta4(p) for p in part_pool])
    fixed_keys = {p.key() for p in B} | {theta4(p).key() for p in core}
    target = 135                      # a small part of 135 beats 509
E = edges(P)
idx = {p.key(): i for i, p in enumerate(P)}
fixed = sorted(idx[k] for k in fixed_keys if k in idx)
fixedset = set(fixed)
bkeys = [p.key() if a.side == "L" else theta4(p).key() for p in breakers]
start = sorted(idx[k] for k in bkeys if k in idx and idx[k] not in fixedset)
bound = a.bound if a.bound is not None else target - len(core) - 1
log(f"pool {len(P)} points, {len(E)} edges; {len(fixed)} fixed "
    f"({len(core)} core + the other part), {len(P)-len(fixed)} candidates; "
    f"the record completes with {len(start)}, so the bound is {bound}")
assert verify(P, E, sorted(set(start) | fixedset), triangle=None), \
    "core plus the record's own completion is not 5-chromatic"
log("core plus the record's completion verified 5-chromatic")


def save(best):
    keep = sorted(set(best) | fixedset)
    Q, F = induced(P, E, keep)
    tag = f"ps_{a.side}_{a.part.split('.')[0]}_{a.iso.replace('.','')}g{a.mask}_{a.seed}"
    save_points(f"{OUT}/{tag}.pts", Q)
    save_edges(f"{OUT}/{tag}.edge", len(Q), F)
    log(f"  saved {len(Q)} vertices, {len(F)} edges"
        + ("   <<< BELOW THE 509 RECORD" if len(Q) < 509 else ""))


best, proven = search(P, E, start=start, bound=bound, time_limit=a.time,
                      cuts_per_iter=2, seed=a.seed, log=log, on_improve=save,
                      fixed=fixed, grow_every=2, bootstrap_pairs=0,
                      bootstrap_essential=False, bootstrap_critical=False,
                      dump_unsat=os.path.join(OUT, f"master_ps_{a.side}_{a.mask}.cnf"))
if best is not None:
    save(best)
    log(f"best completion {len(best)}, part total {len(core)+len(best)}; "
        f"proven minimum over this pool: {proven}")
