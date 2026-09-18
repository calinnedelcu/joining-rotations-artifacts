#!/usr/bin/env python3
"""The interface bound with no ball at all, straight from Proposition 18.

Usage: interface_bound_exact.py A [B]        (the rotation theta_{A/B})

`interface_bound.py` builds a ball, finds its cross edges and runs the hitting
set on those.  That is sound only when the ball realises EVERY cross edge the
infinite union has, and for theta_4 it does -- 126 on every ball tried.  For
theta_28 it does not: the joint lattice has 180 unit vectors, of which a depth-6
ball of radius 5.31 realises 156.  Patterns computed on a subset are subsets, so
they are harder to hit, and the minimum comes out too LARGE: the pool bound is an
upper bound on the lattice bound, not a lower one.

Proposition 18 removes the ball.  A cross edge is a unit vector u of Lambda_a;
writing u = r + theta(s) in the direct sum gives its two endpoints, p = r in the
first half and theta(q) with q = -s in the second; and what the edge contributes
to a pairing depends only on the colours of p and q.  So the complete pattern
table is a loop over the unit vectors of the joint lattice -- enumerated exactly
from the trace form, no ball, no radius, no depth.
"""
import os, sys, time, itertools
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))
from hn.joins import rational_spindle
from hn.lattice import Lattice
from hn.algcolour import klein_colourings, z4_colourings, apply_colouring
log = lambda s: print(s, flush=True)

A = int(sys.argv[1]); B = int(sys.argv[2]) if len(sys.argv) > 2 else 1
J = rational_spindle(A, B)
built = J.build()
assert built is not None, "the rotation does not exist in its own field"
WL, WS, cs = built
from hn.construct import rotate
from cross_pairs import solve_decomp

L0 = Lattice(WL)
units = L0.unit_vectors()
certs = klein_colourings([c for c, _ in units], L0.rank) \
      + z4_colourings([c for c, _ in units], L0.rank)
LAM = Lattice(list(WL) + [rotate(p, cs) for p in WL])
log(f"{J.name} in {J.field_str()}: lattice rank {L0.rank}, {len(units)} unit "
    f"vectors, {len(certs)} homomorphism colourings")
assert LAM.rank == 2 * L0.rank, f"joint rank {LAM.rank}, not {2*L0.rank}"

basis = list(L0.basis) + [rotate(p, cs) for p in L0.basis]
cross, origin = [], 0
for _, u in LAM.unit_vectors():
    co = solve_decomp(basis, u)
    assert co is not None and all(x.denominator == 1 for x in co), "u left the direct sum"
    # co is in the basis L0.basis + theta(L0.basis); rebuild the points and ask
    # the lattice for ITS coordinates, which is what the colourings are written in
    r = L0.combine(tuple(int(x) for x in co[:L0.rank]))
    q = L0.combine(tuple(-int(x) for x in co[L0.rank:]))     # q = -s
    rc, qc = L0.coords(r), L0.coords(q)
    if all(x == 0 for x in rc) or all(x == 0 for x in qc):
        origin += 1                                   # an edge out of the shared origin
    else:
        cross.append((tuple(rc), tuple(qc)))
log(f"cross edges of the whole union, by Proposition 18: {origin + len(cross)}"
    f"  ({origin} at the shared origin, {len(cross)} usable)")

tab = [[apply_colouring(c, p) for p, _ in cross] for c in certs]
tabq = [[apply_colouring(c, q) for _, q in cross] for c in certs]
FIX0 = [p for p in itertools.permutations(range(4)) if p[0] == 0]
t = time.time()
patterns, empty = set(), 0
for iL in range(len(certs)):
    for iS in range(len(certs)):
        for perm in FIX0:
            mono = frozenset(k for k in range(len(cross))
                             if tab[iL][k] == perm[tabq[iS][k]])
            if mono: patterns.add(mono)
            else: empty += 1
log(f"{len(certs)**2 * len(FIX0)} pairings -> {len(patterns)} distinct patterns,"
    f" {empty} empty  ({time.time()-t:.0f}s)")
if empty:
    log(f"  an empty pattern 4-colours the whole union: no 5-chromatic "
        f"L u {J.name}(S) exists, at any size.")
    sys.exit(0)

from pysat.formula import IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver
pool = IDPool()
x = [pool.id(("e", k)) for k in range(len(cross))]
base = [[x[k] for k in sorted(p)] for p in patterns]
for bnd in range(1, 21):
    card = CardEnc.atmost(lits=x, bound=bnd, vpool=pool, encoding=EncType.seqcounter)
    with Solver(name="cadical195", bootstrap_with=base + card.clauses) as s:
        if s.solve():
            log(f"at most {bnd-1}: UNSAT, at most {bnd}: SAT  ->  needs at least "
                f"{bnd} of the {len(cross)} usable cross edges, over the LATTICE")
            break
