#!/usr/bin/env python3
"""Per-pattern lower bounds for the small part.

The large part L admits a finite set of colour patterns on its 19 interface
vertices (origin, 12 reference points at radius 2, 6 auxiliary points).  A
small part S works with L iff S blocks every pattern.  So for each pattern
pi, the smallest S-pool subset that blocks pi alone is a LOWER BOUND on any
S that works with L -- and each such problem is a small hitting-set instance
whose oracle is the S-pool plus 19 fixed-colour vertices.

Usage: pattern_side.py [--Lfile v374e1860.vtx] [--pool parts|ball|ball30]
                       [--bound 135] [--time SECONDS per pattern]
"""
import os, sys, glob, argparse, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn import load_vtx, find_triangle
from hn.sat import Colouring
from hn.construct import edges, theta4, dedup, unit_vector_family, ball, ORIGIN
from hn.hitting import search

D = os.path.join(os.path.dirname(__file__), "..", "data", "parts")
ap = argparse.ArgumentParser()
ap.add_argument("--Lfile", default="v374e1860.vtx")
ap.add_argument("--Sfile", default="v136e564.vtx")
ap.add_argument("--pool", default="parts")
ap.add_argument("--bound", type=int, default=None)
ap.add_argument("--time", type=float, default=None)
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--only", type=int, default=None, help="run only pattern index i")
a = ap.parse_args()

L = load_vtx(f"{D}/{a.Lfile}")
S = load_vtx(f"{D}/{a.Sfile}")
Ssizes = (136, 141, 150, 166, 167, 172)
if a.pool == "parts":
    poolS = []
    for f in sorted(glob.glob(f"{D}/v*.vtx")):
        if int(os.path.basename(f)[1:].split("e")[0]) in Ssizes:
            poolS += load_vtx(f)
elif a.pool == "ball":
    poolS = ball(unit_vector_family(1), 3, 2.45)
elif a.pool == "ball30":
    poolS = ball(unit_vector_family(2), 3, 2.45)
poolS = [p for p in dedup(S + poolS) if p.key() != ORIGIN.key()]
RS = [theta4(p) for p in poolS]

# interface of L: its vertices adjacent to some rotated pool vertex
nL = len(L)
P0 = L + RS
E0 = edges(P0)
iface = sorted({a_ for a_, b in E0 if a_ < nL and b >= nL} | {b for a_, b in E0 if b < nL and a_ >= nL})
print(f"L {a.Lfile}: {nL} vertices; S pool {a.pool}: {len(RS)} candidates; interface {len(iface)} vertices", flush=True)

# enumerate the patterns L admits on the interface
EL = edges(L)
C = Colouring(nL, EL, k=4, selectors=False)
C.break_colour_symmetry(find_triangle(nL, EL))
pats = []
while C.colourable():
    col = C.model_colouring()
    pats.append(tuple(col[v] for v in iface))
    C.solver.add_clause([-C.var(v, col[v]) for v in iface])
C.close()
print(f"{len(pats)} patterns", flush=True)

# the working pool: interface points (fixed, coloured by the pattern) + S candidates
P = [L[v] for v in iface] + RS
E = edges(P)
k = len(iface)
fixed = list(range(k))
Skeys = {theta4(p).key() for p in S}
start = [i for i, p in enumerate(P) if i >= k and p.key() in Skeys]
print(f"working pool {len(P)} vertices {len(E)} edges; start (S_136 minus origin) {len(start)} free", flush=True)

results = []
for pi, pat in enumerate(pats):
    if a.only is not None and pi != a.only:
        continue
    fc = {i: pat[i] for i in range(k)}
    t = time.time()
    best, proven = search(P, E, start=start, bound=a.bound, time_limit=a.time, seed=a.seed,
                          log=lambda s: None, fixed=fixed, fixed_colours=fc, grow_every=2,
                          cuts_per_iter=2)
    m = len(best) if best is not None else None
    results.append((pi, m, proven))
    print(f"pattern {pi:2d}: smallest blocker found {m}, proven minimum over pool: {proven}  ({time.time()-t:.0f}s)", flush=True)
ms = [m for _, m, _ in results if m is not None]
print(f"lower bound on |S| (free vertices, origin excluded): max over patterns = {max(ms) if ms else None}; "
      f"all proven: {all(p for _, _, p in results)}", flush=True)
