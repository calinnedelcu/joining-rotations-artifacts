#!/usr/bin/env python3
"""The interface bound using EVERY periodic 4-colouring, not only the linear ones.

Usage: interface_bound_periodic.py A [--depth D] [--radius R] [--modulus M]

`interface_bound.py` uses the group homomorphisms Lambda -> (Z/2)^2 and Z/4 that
`hn.algcolour` finds -- 8 of them for the Moser lattice.  Those are exactly the
LINEAR proper colourings of Lambda/m*Lambda.  Every proper colouring of that
finite quotient pulls back to a proper colouring of the whole lattice, linear or
not, so every one of them is a legitimate colouring of a half, and each adds
patterns a 5-chromatic union must defeat.  More patterns can only RAISE the bound,
so this strengthens the result rather than restating it.

At m = 2 the Moser lattice has exactly 12 proper 4-colourings with the zero coset
fixed, which is precisely 2 Klein kernels x 6 permutations: at that modulus every
colouring is linear and nothing is gained.  At m = 3 it has none.  At **m = 4** it
has **120**, against the 48 the homomorphisms provide -- so 72 valid colourings
were missing from the count.

Normalisation: the halves share the centre, which is the zero coset, so a
colouring of the union needs both sides to give it the same colour, and relabelling
both sides together changes no monochromatic edge.  So it is exactly the pairs of
colourings that both send the zero coset to colour 0 -- no separate permutation
factor, it is already absorbed.
"""
import os, sys, math, time, argparse, itertools
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.joins import rational_spindle

ap = argparse.ArgumentParser()
ap.add_argument("a")
ap.add_argument("--depth", type=int, default=None)
ap.add_argument("--radius", type=float, default=None)
ap.add_argument("--modulus", type=int, default=4)
ap.add_argument("--max-bound", type=int, default=30)
ap.add_argument("--max-colourings", type=int, default=400)
a = ap.parse_args()
log = lambda s: print(s, flush=True)

num, den = (a.a.split("/") + ["1"])[:2]
num, den = int(num), int(den)
need = math.sqrt(num / den)
depth = a.depth or math.ceil(need)
radius = a.radius or (need + 0.02)
J = rational_spindle(num, den)
b = J.build()
if b is None:
    log(f"{J.name} does not exist in {J.field_str()}"); sys.exit(1)
WL, _, cs = b
log(f"{J.name} = arccos({J.cos}) in {J.field_str()}; shell at {num}/{den}")

from hn.construct import ball, rotate, edges_grid, norm
from hn.lattice import Lattice
sys.path.insert(0, os.path.dirname(__file__))
from shells import shell_count
from pysat.formula import IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

t = time.time()
V = ball(WL, depth, radius)
on = sum(1 for p in V if abs(norm(p) ** 2 - num / den) < 1e-9)
total = shell_count(num, den)
log(f"ball: {len(V)} points, {on} of the shell's {total} ({time.time()-t:.0f}s)")
if total == 0 or on < total:
    log("THE BALL DOES NOT HOLD THE WHOLE SHELL -- refusing to report.")
    sys.exit(1)

L0 = Lattice(WL)
r, m = L0.rank, a.modulus
units = [c for c, _ in L0.unit_vectors()]
n_cos = m ** r


def enc(v):
    i = 0
    for c in reversed(v):
        i = i * m + (c % m)
    return i


def dec(i):
    out = []
    for _ in range(r):
        out.append(i % m); i //= m
    return tuple(out)


S = {enc(u) for u in units}
S.discard(0)
pool = IDPool()
x = lambda v, c: pool.id(("x", v, c))
cls = []
for v in range(n_cos):
    cls.append([x(v, c) for c in range(4)])
    for c in range(4):
        for d in range(c + 1, 4):
            cls.append([-x(v, c), -x(v, d)])
for v in range(n_cos):
    dv = dec(v)
    for s in S:
        ds = dec(s)
        w = enc(tuple((p + q) % m for p, q in zip(dv, ds)))
        if w == v:
            log(f"a unit vector lies in {m}*Lambda: no colouring at this modulus")
            sys.exit(1)
        if w > v:
            for c in range(4):
                cls.append([-x(v, c), -x(w, c)])
cls.append([x(0, 0)])                     # normalise: the centre gets colour 0
t = time.time()
cols = []
with Solver(name="cadical195", bootstrap_with=cls) as s:
    while s.solve() and len(cols) < a.max_colourings:
        mod = set(l for l in s.get_model() if l > 0)
        asg = tuple(next(c for c in range(4) if x(v, c) in mod)
                    for v in range(n_cos))
        cols.append(asg)
        s.add_clause([-x(v, asg[v]) for v in range(n_cos)])
log(f"periodic 4-colourings at m={m} with the centre fixed: {len(cols)} "
    f"({time.time()-t:.0f}s)")
if len(cols) >= a.max_colourings:
    log(f"  (capped at {a.max_colourings}; the bound below is still valid, since "
        f"leaving colourings out can only lower it)")

t = time.time()
nV = len(V)
P = V + [rotate(p, cs) for p in V]
E = edges_grid(P)
cross = [(p, q - nV) if p < nV else (q, p - nV)
         for p, q in E if (p < nV) != (q < nV)]
log(f"{len(E)} edges in the union, {len(cross)} cross ({time.time()-t:.0f}s)")
cidx = [enc(L0.coords(p)) for p in V]
tab = [[col[j] for j in cidx] for col in cols]

t = time.time()
pats, empty = set(), 0
for cL in tab:
    for cS in tab:
        mono = frozenset(k for k, (p, q) in enumerate(cross) if cL[p] == cS[q])
        if not mono:
            empty += 1
        else:
            pats.add(mono)
log(f"{len(tab)**2} pairings -> {len(pats)} distinct patterns, {empty} empty "
    f"({time.time()-t:.0f}s)")
if empty:
    log("an empty pattern is a proper 4-colouring of the whole union:")
    log(f"no 5-chromatic L u {J.name}(S) exists over this pool, at any size.")
    sys.exit(0)

pool2 = IDPool()
y = [pool2.id(("e", k)) for k in range(len(cross))]
base = [[y[k] for k in sorted(p)] for p in pats]
for B in range(1, a.max_bound + 1):
    card = CardEnc.atmost(lits=y, bound=B, vpool=pool2,
                          encoding=EncType.seqcounter)
    with Solver(name="cadical195", bootstrap_with=base + card.clauses) as s:
        if s.solve():
            log(f"  at most {B-1}: UNSAT, at most {B}: SAT")
            log(f"\n{J.name}: needs at least {B} of the {len(cross)} cross edges "
                f"(periodic colourings at m={m})")
            break
        log(f"  at most {B}: UNSAT")
else:
    log(f"no hitting set of size <= {a.max_bound}")
