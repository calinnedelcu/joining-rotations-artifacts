#!/usr/bin/env python3
"""Decide a joining rotation with no ball at all, over the COMPLETE cross structure.

Usage: join_filter_residues.py A [--modulus M]

`scripts/interface_bound.py` is stronger than the ball-free classifier -- it kills
`theta_12` and `theta_20`, which that filter passes -- but it needs a ball holding
the rotation's whole shell, which costs hours for large `A` and is the single
error this project has made three times.  It does not need one.

A periodic colouring of `Lambda/m*Lambda` gives a cross pair `(p, q)` its two
colours through the residues `p mod m*Lambda` and `q mod m*Lambda` alone.  So the
only thing a colouring can see is WHICH RESIDUE PAIRS occur among cross pairs, and
there are at most `(m^4)^2` of those -- 65536 at `m = 4`.

A residue pair `(alpha, beta)` occurs exactly when some `p = alpha`, `q = beta`
mod `m*Lambda` have `|p - theta(q)| = 1`, and

    p - theta(q)  in  (alpha - theta(beta)) + m * (Lambda + theta Lambda)

with every element of that coset reachable, because `Lambda_J = Lambda + theta
Lambda` means any `m*w` splits as `m*alpha' + theta(m*beta')`.  So the test is:
**does that coset contain a unit vector of the joint lattice?**  The joint
lattice's unit vectors are finitely many and enumerated exactly by the trace form,
with no ball and no radius anywhere.

If some pair of proper colourings of `Lambda/m*Lambda` disagrees on every occurring
residue pair, the whole infinite union `L u theta(S)` is properly 4-coloured, for
every `L` and `S` at every radius -- so no 5-chromatic type-M construction exists
with that rotation, ever.  A failure to find such a pair says nothing: the kill is
one-sided, like every other filter here.
"""
import os, sys, time, argparse, itertools
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.joins import rational_spindle

ap = argparse.ArgumentParser()
ap.add_argument("a")
ap.add_argument("--modulus", type=int, default=4)
ap.add_argument("--max-colourings", type=int, default=400)
a = ap.parse_args()
log = lambda s: print(s, flush=True)

num, den = (a.a.split("/") + ["1"])[:2]
num, den = int(num), int(den)
J = rational_spindle(num, den)
b = J.build()
if b is None:
    log(f"{J.name} does not exist in {J.field_str()}"); sys.exit(1)
WL, _, cs = b
m = a.modulus
log(f"{J.name} = arccos({J.cos}) in {J.field_str()}, modulus {m}")

from hn.construct import rotate
from hn.lattice import Lattice
sys.path.insert(0, os.path.dirname(__file__))
from shells import shell_count
from pysat.formula import IDPool
from pysat.solvers import Solver

total = shell_count(num, den)
if total == 0:
    # An empty shell means no pair p, theta(p) at distance 1 -- the spindle
    # mechanism is absent.  It does NOT mean there are no cross edges: Lambda_J
    # still has unit vectors, they just pair distinct points.  So the filter is
    # valid here and we run it.  An earlier version exited at this point saying
    # "the question does not arise", which was wrong, and hid the three
    # empty-shell multiples of 4 below 100 that survive filter 1.
    log(f"the shell at {num}/{den} is EMPTY: no pair p, theta(p) at distance 1, "
        f"so the spindle mechanism is absent. Cross edges may still exist, and "
        f"the filter is run on them below.")
log(f"shell at {num}/{den}: {total} lattice points"
    + (" (non-empty, so the rotation acts on it)" if total else ""))

t = time.time()
L0 = Lattice(WL)
LJ = Lattice(list(WL) + [rotate(p, cs) for p in WL])
uv0 = L0.unit_vectors()
uvJ = LJ.unit_vectors()
log(f"Lambda: rank {L0.rank}, {len(uv0)} unit vectors; "
    f"Lambda_J: rank {LJ.rank}, {len(uvJ)} unit vectors  ({time.time()-t:.0f}s)")
r = L0.rank

# ---- the proper colourings of Lambda/m*Lambda ------------------------------
n_cos = m ** r
enc = lambda v: sum((c % m) * m ** i for i, c in enumerate(v))
def dec(i):
    out = []
    for _ in range(r):
        out.append(i % m); i //= m
    return tuple(out)

S = {enc(c) for c, _ in uv0}
if 0 in S:
    log(f"a unit vector of Lambda lies in {m}*Lambda: no colouring at this modulus")
    sys.exit(1)
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
        w = enc(tuple(p + q for p, q in zip(dv, ds)))
        if w > v:
            for c in range(4):
                cls.append([-x(v, c), -x(w, c)])
cls.append([x(0, 0)])                       # the shared centre gets colour 0

# ---- which residue pairs occur among cross pairs ---------------------------
# coords is linear, so coords_J(alpha - theta(beta)) = cJ(alpha) - cJ(theta beta):
# 2 * m^r coordinate computations instead of m^(2r).
t = time.time()
reps = [L0.combine_echelon(list(dec(i))) for i in range(n_cos)]
cA = [tuple(c % m for c in LJ.coords(p)) for p in reps]
cB = [tuple(c % m for c in LJ.coords(rotate(p, cs))) for p in reps]
unit_keys = sorted({tuple(c % m for c in cJ) for cJ, _ in uvJ})
# Index the beta side by its residue and look up cA[i] - v for each unit vector
# v, instead of testing all m^(2*rank) pairs: that is n_cos * |unit_keys| lookups
# rather than n_cos^2, which is what makes m = 8 affordable at all.
byB = {}
for j, bj in enumerate(cB):
    byB.setdefault(bj, []).append(j)
occurring = []
for i in range(n_cos):
    ai = cA[i]
    for v in unit_keys:
        want = tuple((p - q) % m for p, q in zip(ai, v))
        for j in byB.get(want, ()):
            occurring.append((i, j))
log(f"{n_cos}x{n_cos} = {n_cos*n_cos} residue pairs, {len(occurring)} of them "
    f"occur among cross pairs ({time.time()-t:.0f}s)")
if not occurring:
    log("no cross pair exists at all: the halves cannot be joined")
    sys.exit(0)
if (0, 0) in set(occurring):
    # Degenerate, and silently so if not checked.  (0,0) occurring means some unit
    # vector of the joint lattice lies in m*Lambda_J, i.e. Lambda_J holds a vector
    # of length 1/m.  Then a cross pair exists with both residues zero, both halves
    # give the centre's coset colour 0, and that pair is monochromatic under every
    # pairing -- so this modulus can never kill, whatever the geometry.  The
    # statement is true (no m-periodic colouring works) but it is automatic, and
    # tells the rotations apart from nothing.  At m = 2 the condition is exactly
    # "the joint lattice has a half-unit vector", which is route 49's criterion --
    # so every rotation that criterion passes is degenerate at m = 2 by
    # construction, and the same caveat is recorded for even shell radii in
    # results/SHELLS.md.
    log(f"DEGENERATE AT MODULUS {m}: the residue pair (0,0) occurs, so the joint "
        f"lattice holds a vector of length 1/{m}.")
    log(f"  That pair is monochromatic under EVERY {m}-periodic colouring, because "
        f"both halves give the shared centre's coset the same colour.  So the "
        f"rotation does survive -- no {m}-periodic colouring 4-colours the union --")
    log(f"  but it survives automatically, for a reason shared by every rotation "
        f"with a 1/{m} vector, and independent of where the halves sit.  This "
        f"modulus cannot DISCRIMINATE; use another one to learn anything.")
    sys.exit(2)

# ---- is some pair of colourings blind to all of them? ----------------------
# Asked as ONE SAT instance rather than by enumerating colourings and pairing them
# up.  Enumeration has to be capped at some modulus -- Lambda/8Lambda has far too
# many to list -- and a capped "survives" is not a survival, only a failure to
# look.  Here UNSAT is a proof.
t = time.time()
both = []
for lit in cls:                       # the L side, on variables x(v, c)
    both.append(list(lit))
y = lambda v, c: pool.id(("y", v, c))
for lit in cls:                       # the S side, the same clauses on y
    both.append([(-1 if l < 0 else 1) * y(*pool.obj(abs(l))[1:]) for l in lit]
                if lit else [])
for i, j in occurring:                # ... disagreeing on every occurring pair
    for c in range(4):
        both.append([-x(i, c), -y(j, c)])
with Solver(name="cadical195", bootstrap_with=both) as s:
    killed = s.solve()
    model = set(s.get_model()) if killed else None    # keep the witness, not just the verdict
log("")
if killed:
    log(f"{J.name}: DEAD -- two proper periodic colourings disagree on every "
        f"occurring residue pair ({time.time()-t:.0f}s)")
    # --- write the two colourings and the pair list, so the kill is checkable
    # without rerunning the solver.  A verdict with no witness is not a proof
    # anyone else can see.
    import json, os
    def read(side):
        out = []
        for v in range(n_cos):
            cs = [c for c in range(4)
                  if (x(v, c) if side == "L" else y(v, c)) in model]
            assert len(cs) == 1, f"{side} residue {v} got colours {cs}"
            out.append(cs[0])
        return out
    tabL, tabS = read("L"), read("S")
    # re-check both are proper on Lambda/m and that they disagree everywhere
    for v in range(n_cos):
        dv = dec(v)
        for sv in S:
            w = enc(tuple(p + q for p, q in zip(dv, dec(sv))))
            assert tabL[v] != tabL[w] and tabS[v] != tabS[w], \
                "a witness colouring is not proper"
    bad = [(i, j) for i, j in occurring if tabL[i] == tabS[j]]
    assert not bad, f"witness agrees on {len(bad)} occurring pairs"
    # the two halves share the origin, so both colourings must agree there --
    # a pair that disagreed at 0 would not be a colouring of the union at all
    assert tabL[0] == tabS[0] == 0, \
        f"the shared origin gets {tabL[0]} on one side and {tabS[0]} on the other"
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                       "results", "periodic")
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, f"{J.name.replace('/', '_')}_m{m}.json")
    with open(path, "w") as f:
        # The unit steps go in the file.  Without them a reader holding only the
        # JSON cannot test that either colouring is proper -- properness is a
        # statement about unit edges inside each half, and those live in the
        # lattice, not in the colour arrays.  A referee corrupted a witness into
        # a monochromatic unit edge and the standalone checker still passed it.
        json.dump({"rotation": J.name, "modulus": m, "residue_classes": n_cos,
                   "rank": r, "unit_steps": sorted(S),
                   "colouring_L": tabL, "colouring_S": tabS,
                   "occurring_pairs": sorted(set(occurring))}, f)
    log(f"  witness written to results/periodic/{os.path.basename(path)}: "
        f"two colourings of Lambda/{m}Lambda over {n_cos} residue classes and "
        f"all {len(set(occurring))} distinct occurring pairs -- re-checked here: "
        f"both proper, agreeing at the shared origin, disagreeing on every pair")
    log(f"  So the whole infinite union L u {J.name}(S) is properly 4-coloured, "
        f"for every L and S at every radius.")
    log("  No 5-chromatic type-M construction exists with this rotation.")
else:
    log(f"{J.name}: SURVIVES at modulus {m} -- PROVED, not sampled: no pair of "
        f"proper colourings of Lambda/{m}Lambda can 4-colour the union "
        f"({time.time()-t:.0f}s)")
    log("  One-sided: this is a candidate, not a construction.")
