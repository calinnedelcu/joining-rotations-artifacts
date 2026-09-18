#!/usr/bin/env python3
"""Minimise one side of Parts' decomposition  G = L  union  theta_4(S).

Usage: parts_side.py L|S [--pool NAME] [--time SECONDS] [--seed N] [--cuts C] [--tabu N]

  side L: the small part S_136 (data/parts/v136e564.vtx) is fixed; search
          for a large part with < 374 vertices in the L-side pool.
  side S: the large part L_374 (data/parts/v374e1860.vtx) is fixed; search
          for a small part with < 136 vertices in the S-side pool.

Pools (--pool):
  parts   the union of Parts' own published files for that side
          (811 L-side points, 183 S-side points): his explored region
  file:F  just the points of data/parts/F, e.g. file:v412e2106.vtx, which is
          Parts' accumulative L-graph: the union of all his minimal 374- and
          375-vertex large parts.  This is the pool where the answer is DENSE
          (373 wanted out of 412), the regime where the search converges --
          on the 811-point pool it does not
  ball    L: ball(30 vectors, depth 4, r 2.53)  (8131 points)
          S: ball(18 vectors, depth 3, r 2.45)  (499 points)
  ball30  S only: ball(30 vectors, depth 3, r 2.45) (2575 points)

The oracle is the full graph (fixed part + candidate part); every claimed
improvement is re-verified in a fresh solver and saved under out/.
"""
import os, re, sys, glob, argparse, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn import load_vtx, verify, find_triangle
from hn.io import save_points, save_edges, load_points
from hn.graph import induced
from hn.construct import (edges, theta4, dedup, unit_vector_family, ball, contains)
from hn.hitting import search

D = os.path.join(os.path.dirname(__file__), "..", "data", "parts")
OUT = os.path.join(os.path.dirname(__file__), "..", "out")
ap = argparse.ArgumentParser()
ap.add_argument("side", choices=["L", "S"])
ap.add_argument("--pool", default="parts")
ap.add_argument("--time", type=float, default=None)
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--cuts", type=int, default=2)
ap.add_argument("--tabu", type=int, default=20000)
ap.add_argument("--bound", type=int, default=None)
ap.add_argument("--grow", type=int, default=3, help="MCS-growth cut every N iterations (0 = off)")
ap.add_argument("--pairs", type=int, default=0, help="enumerate size-2 correction sets if at most this many non-essential vertices")
ap.add_argument("--budget", type=int, default=20000, help="conflict budget per SAT call while growing correction sets")
ap.add_argument("--ess-budget", type=int, default=None, help="conflict budget for essential-vertex checks (None = exact)")
ap.add_argument("--symmetry", type=int, default=0, help="impose k-fold rotational symmetry on the searched side (3 or 6)")
ap.add_argument("--Lfile", default="v374e1860.vtx")
ap.add_argument("--Sfile", default="v136e564.vtx")
a = ap.parse_args()

L = load_vtx(f"{D}/{a.Lfile}")
S = load_vtx(f"{D}/{a.Sfile}")
Lsizes = (374, 375, 376, 400, 403, 406, 412, 451)


def _load_pool(spec):
    """A pool file: a name in data/parts/, or a path with a slash from the
    repository root; .pts files are read in the native exact format, and
    several names may be joined with '+'."""
    out = []
    for part in spec.split("+"):
        path = part if "/" in part else f"{D}/{part}"
        out += load_points(path) if path.endswith(".pts") else load_vtx(path)
    return out
Ssizes = (136, 141, 150, 166, 167, 172)

def parts_union(sizes):
    pts = []
    for f in sorted(glob.glob(f"{D}/v*.vtx")):
        n = int(os.path.basename(f)[1:].split("e")[0])
        if n in sizes:
            pts += load_vtx(f)
    return dedup(pts)

if a.side == "L":
    if a.pool == "parts":
        poolL = parts_union(Lsizes)
    elif a.pool == "ball":
        poolL = ball(unit_vector_family(2), 4, 2.53)
    elif a.pool.startswith("file:"):
        poolL = _load_pool(a.pool[5:])
    else:
        raise SystemExit("unknown L pool")
    poolL = dedup(L + poolL)
    P = dedup(poolL + [theta4(p) for p in S])
    fixed_keys = {theta4(p).key() for p in S}
    start_keys = {p.key() for p in L}
else:
    if a.pool == "parts":
        poolS = parts_union(Ssizes)
    elif a.pool == "ball":
        poolS = ball(unit_vector_family(1), 3, 2.45)
    elif a.pool == "ball30":
        poolS = ball(unit_vector_family(2), 3, 2.45)
    elif a.pool.startswith("file:"):
        poolS = _load_pool(a.pool[5:])
    else:
        raise SystemExit("unknown S pool")
    poolS = dedup(S + poolS)
    P = dedup(L + [theta4(p) for p in poolS])
    fixed_keys = {p.key() for p in L}
    start_keys = {theta4(p).key() for p in S}
E = edges(P)
idx = {p.key(): i for i, p in enumerate(P)}
fixed = sorted(idx[k] for k in fixed_keys)
start = sorted(idx[k] for k in start_keys if k not in fixed_keys)
tag = "side%s_%s_%d" % (a.side, re.sub(r"[^A-Za-z0-9]+", "-", a.pool).strip("-"), a.seed)
orbits = None
if a.symmetry:
    from hn.symmetry import rot60
    def rot(p, k):
        for _ in range(k):
            p = rot60(p)
        return p
    step = 6 // a.symmetry
    idx = {p.key(): i for i, p in enumerate(P)}
    seen, orbits, dropped = set(), [], 0
    for i in range(len(P)):
        if i in seen or i in set(fixed):
            continue
        orb, q, ok = [], P[i], True
        for _ in range(a.symmetry):
            j = idx.get(q.key())
            if j is None or j in set(fixed):
                ok = False
                break
            orb.append(j)
            q = rot(q, step)
        if not ok:
            dropped += 1
            continue
        orb = sorted(set(orb))
        seen |= set(orb)
        if len(orb) > 1:
            orbits.append(orb)
    print(f"symmetry {a.symmetry}: {len(orbits)} orbits, {dropped} points not in a closed orbit", flush=True)
print(f"side {a.side}, pool {a.pool}: {len(P)} vertices, {len(E)} edges, fixed {len(fixed)}, start {len(start)} free", flush=True)

def save(best):
    keep = sorted(set(best) | set(fixed))
    with open(f"{OUT}/best_{tag}.keep", "w") as f:
        f.write(" ".join(map(str, keep)) + "\n")
    P2, E2 = induced(P, E, keep)
    save_points(f"{OUT}/best_{tag}.pts", P2)
    save_edges(f"{OUT}/best_{tag}.edge", len(P2), E2)
    print(f"  saved out/best_{tag}.* : {len(P2)} vertices, {len(E2)} edges", flush=True)

os.makedirs(OUT, exist_ok=True)
best, proven = search(P, E, start=start, bound=a.bound, time_limit=a.time,
                      cuts_per_iter=a.cuts, tabu_iters=a.tabu, seed=a.seed,
                      log=lambda s: print(s, flush=True), on_improve=save, fixed=fixed,
                      grow_every=a.grow, bootstrap_pairs=a.pairs,
                      grow_budget=a.budget, essential_budget=a.ess_budget,
                      orbits=orbits)
if best is not None:
    save(best)
    total = len(best) + len(fixed)
    if proven and a.bound is not None and a.bound < len(best) - 1:
        print(f"best: {len(best)} free + {len(fixed)} fixed = {total} vertices; PROVEN: no 5-chromatic "
              f"choice with <= {a.bound} free vertices exists over this pool", flush=True)
    else:
        print(f"best: {len(best)} free + {len(fixed)} fixed = {total} vertices; proven optimal over this pool: {proven}", flush=True)
