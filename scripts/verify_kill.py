#!/usr/bin/env python3
"""Check a kill from join_filter_residues.py against the exact edge finder.

Usage: verify_kill.py A --depth D --radius R [--modulus M]

The filter kills a rotation by producing two periodic colourings of
`Lambda/m*Lambda` that disagree on every occurring residue pair.  That is a proof
on paper.  This builds a real ball, colours `L` by the first and `theta(L)` by the
second, recomputes every edge of the union from the coordinates, and counts the
monochromatic ones.  The answer has to be zero.
"""
import os, sys, time, math, argparse, itertools
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.joins import rational_spindle

ap = argparse.ArgumentParser()
ap.add_argument("a")
ap.add_argument("--depth", type=int, required=True)
ap.add_argument("--radius", type=float, required=True)
ap.add_argument("--modulus", type=int, default=4)
a = ap.parse_args()
log = lambda s: print(s, flush=True)

num, den = (a.a.split("/") + ["1"])[:2]
num, den = int(num), int(den)
J = rational_spindle(num, den)
WL, _, cs = J.build()
m = a.modulus
from hn.construct import ball, rotate, edges_grid, norm
from hn.lattice import Lattice
sys.path.insert(0, os.path.dirname(__file__))
from shells import shell_count
from pysat.formula import IDPool
from pysat.solvers import Solver

L0 = Lattice(WL)
LJ = Lattice(list(WL) + [rotate(p, cs) for p in WL])
r = L0.rank
n_cos = m ** r
enc = lambda v: sum((c % m) * m ** i for i, c in enumerate(v))
def dec(i):
    o = []
    for _ in range(r):
        o.append(i % m); i //= m
    return tuple(o)

S = {enc(c) for c, _ in L0.unit_vectors()}
pool = IDPool()
x = lambda v, c: pool.id(("x", v, c))
y = lambda v, c: pool.id(("y", v, c))
cl = []
for f in (x, y):
    for v in range(n_cos):
        cl.append([f(v, c) for c in range(4)])
        for c in range(4):
            for d in range(c + 1, 4):
                cl.append([-f(v, c), -f(v, d)])
    for v in range(n_cos):
        dv = dec(v)
        for s in S:
            ds = dec(s)
            w = enc(tuple(p + q for p, q in zip(dv, ds)))
            if w > v:
                for c in range(4):
                    cl.append([-f(v, c), -f(w, c)])
    cl.append([f(0, 0)])
reps = [L0.combine_echelon(list(dec(i))) for i in range(n_cos)]
cA = [tuple(c % m for c in LJ.coords(p)) for p in reps]
cB = [tuple(c % m for c in LJ.coords(rotate(p, cs))) for p in reps]
uk = sorted({tuple(c % m for c in cJ) for cJ, _ in LJ.unit_vectors()})
byB = {}
for j, bj in enumerate(cB):
    byB.setdefault(bj, []).append(j)
occ = 0
for i in range(n_cos):
    ai = cA[i]
    for v in uk:
        want = tuple((p - q) % m for p, q in zip(ai, v))
        for j in byB.get(want, ()):
            occ += 1
            for c in range(4):
                cl.append([-x(i, c), -y(j, c)])
log(f"{J.name}: {occ} occurring residue pairs at m={m}")
with Solver(name="cadical195", bootstrap_with=cl) as s:
    if not s.solve():
        log("no killing pair of colourings exists: nothing to verify")
        sys.exit(1)
    mod = set(l for l in s.get_model() if l > 0)
cL = [next(c for c in range(4) if x(v, c) in mod) for v in range(n_cos)]
cS = [next(c for c in range(4) if y(v, c) in mod) for v in range(n_cos)]
log("extracted the two colourings; now checking them on a real ball")

t = time.time()
V = ball(WL, a.depth, a.radius)
on = sum(1 for p in V if abs(norm(p) ** 2 - num / den) < 1e-9)
tot = shell_count(num, den)
log(f"ball: {len(V)} points, {on} of the shell's {tot} ({time.time()-t:.0f}s)")
assert on == tot, "the ball must hold the whole shell for this to mean anything"
nV = len(V)
P = V + [rotate(p, cs) for p in V]
t = time.time()
E = edges_grid(P)
idx = [enc(L0.coords(p)) for p in V]
colour = [cL[idx[i]] for i in range(nV)] + [cS[idx[i]] for i in range(nV)]
mono = [(p, q) for p, q in E if colour[p] == colour[q]]
inL = sum(1 for p, q in mono if p < nV and q < nV)
inS = sum(1 for p, q in mono if p >= nV and q >= nV)
log(f"union: {len(P)} points, {len(E)} edges recomputed from the coordinates "
    f"({time.time()-t:.0f}s)")
log(f"MONOCHROMATIC EDGES: {len(mono)}  (inside L: {inL}, inside theta(S): {inS}, "
    f"cross: {len(mono)-inL-inS})")
if mono:
    log("  THE KILL IS WRONG.")
    sys.exit(1)
log(f"  zero -- the two colourings properly 4-colour the whole union.")
log(f"  {J.name} is dead, and this is the certificate checked on real coordinates.")
