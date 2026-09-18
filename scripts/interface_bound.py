#!/usr/bin/env python3
"""The minimum number of cross edges a type-M construction needs, per rotation.

Usage: interface_bound.py A [--depth D] [--radius R] [--max-bound B]

`results/INTERFACE-BOUND.md` proves that no 5-chromatic `L u theta_4(S)` over
the Moser lattice has eight or fewer cross edges.  Nothing in that argument is
about theta_4.  Both halves are subsets of the SAME Moser lattice -- the
rotation only decides which pairs of points end up at unit distance across the
halves -- so the closed-form colourings of that lattice apply whatever joins the
halves, and the bound can be computed for every joining rotation known.

The argument, unchanged:

  each half is 4-coloured by a homomorphism of the whole infinite lattice (2
  Klein and 6 Z/4 of them, `hn.algcolour`); pair any colouring of L with any
  colouring of S under any of the 6 permutations of the colours that FIX 0 --
  the halves share the origin, both colourings send it to 0, and the other 18
  permutations colour that point twice over -- and the result properly 4-colours
  the union UNLESS some cross edge comes out monochromatic; so a 5-chromatic
  union must use a set of cross edges meeting the monochromatic set of every one
  of the 8 * 8 * 6 = 384 pairings.  Minimum hitting set, decided exactly by SAT.

One-sided in the safe direction: these patterns come from homomorphism
colourings only, and any other colouring of the halves would add patterns, which
can only raise the bound.

Why it is worth having for other rotations: theta_28 creates 150 new unit
vectors against theta_4's 96, and "richer interface" has been read here as
promising.  This says what the richness costs -- whether a rotation needs more
cross edges to be joined, or fewer.
"""
import os, sys, math, time, argparse, itertools
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.joins import rational_spindle

ap = argparse.ArgumentParser()
ap.add_argument("a", help="squared radius of the shell: an integer, or a/b")
ap.add_argument("--depth", type=int, default=None)
ap.add_argument("--radius", type=float, default=None)
ap.add_argument("--max-bound", type=int, default=20)
ap.add_argument("--model", choices=["shared", "disjoint", "both"], default="both",
                help="whether the two halves share the origin, as a type-M "
                     "construction does.  Sharing it forces the colour "
                     "permutation to fix colour 0, because a homomorphism sends "
                     "0 to 0 on both sides -- so only 6 of the 24 permutations "
                     "give a well-defined colouring of the union, and the other "
                     "18 contribute patterns that no real colouring produces")
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
log(f"{J.name} = arccos({J.cos}) in {J.field_str()}; shell at {num}/{den}, "
    f"radius {need:.4f}, depth {depth}")

from hn.construct import ball, rotate, edges_grid, norm
from hn.lattice import Lattice
from hn.algcolour import klein_colourings, z4_colourings, apply_colouring
sys.path.insert(0, os.path.dirname(__file__))
from shells import shell_count

t = time.time()
V = ball(WL, depth, radius)
# The routes 20/44/48 error, guarded: a rotation acts on the shell at squared
# radius a/b, and a ball that does not hold that shell has not been given the
# rotation to test.  A 4-colouring of such a union says nothing about the
# construction, because the construction lives in a bigger ball.  alpha_64/3
# needs depth 7, not the ceil(sqrt(64/3)) = 5 that looks sufficient.
on = sum(1 for p in V if abs(norm(p) ** 2 - num / den) < 1e-9)
total = shell_count(num, den)
log(f"ball: {len(V)} points, {on} of the shell's {total} ({time.time()-t:.0f}s)")
if total == 0:
    log(f"THE SHELL AT {num}/{den} IS EMPTY IN THIS LATTICE -- the rotation has "
        f"nothing to act on and any answer here is meaningless.")
    sys.exit(1)
if on < total:
    log(f"THE BALL HOLDS ONLY {on} OF THE SHELL'S {total} POINTS.")
    log("  A 4-colouring of this union would be about this pool and not about "
        "the construction, which needs the whole shell.  Raise --depth.")
    sys.exit(1)

L0 = Lattice(WL)
units = L0.unit_vectors()
ucoords = [c for c, _ in units]
certs = klein_colourings(ucoords, L0.rank) + z4_colourings(ucoords, L0.rank)
log(f"Moser lattice: rank {L0.rank}, {len(units)} unit vectors, "
    f"{len(certs)} homomorphism colourings")
if not certs:
    log("no closed-form colouring of the lattice: this argument gives nothing here")
    sys.exit(1)

# The cross edges of the pool.  Both halves are the same ball; the second is
# rotated, and the colour of a rotated point is the colour its PRE-IMAGE gets,
# because S is a subset of the lattice and theta(S) only moves it.
t = time.time()
n = len(V)
P = V + [rotate(p, cs) for p in V]
E = edges_grid(P)
cross = [(x, y - n) if x < n else (y, x - n) for x, y in E if (x < n) != (y < n)]
log(f"{len(E)} edges in the union, {len(cross)} of them cross ({time.time()-t:.0f}s)")
if not cross:
    log("no cross edge at all: the halves cannot be joined over this pool")
    sys.exit(1)

coord = [L0.coords(p) for p in V]
assert all(c is not None for c in coord), "a ball point is outside its own lattice"

# One colour table per certificate, so the pattern loop is table lookups.
tab = [[apply_colouring(c, coord[i]) for i in range(n)] for c in certs]

ORIGIN_COLOUR = apply_colouring(certs[0], (0,) * L0.rank)
assert all(apply_colouring(c, (0,) * L0.rank) == ORIGIN_COLOUR for c in certs), \
    "the colourings disagree at the origin"
assert ORIGIN_COLOUR == 0, "a homomorphism should send the origin to colour 0"

from pysat.formula import IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver


def run(perms, label):
    t = time.time()
    patterns, empty = set(), 0
    for iL in range(len(certs)):
        for iS in range(len(certs)):
            tL, tS = tab[iL], tab[iS]
            for perm in perms:
                mono = frozenset(k for k, (p, q) in enumerate(cross)
                                 if tL[p] == perm[tS[q]])
                if not mono:
                    empty += 1
                else:
                    patterns.add(mono)
    log(f"\n[{label}] {len(certs)**2 * len(perms)} pairings -> "
        f"{len(patterns)} distinct patterns, {empty} empty ({time.time()-t:.0f}s)")
    if empty:
        log(f"  an empty pattern is a proper 4-colouring of the whole union:")
        log(f"  no 5-chromatic L u {J.name}(S) exists over this pool, at any size.")
        return "dead"
    always = set.intersection(*[set(p) for p in patterns])
    if always:
        # A cross edge in EVERY pattern is monochromatic under every pairing, so
        # it alone hits everything and the bound is 1 whatever else the geometry
        # does.  That happens when both its endpoints lie in m*Lambda, which needs
        # the joint lattice to hold a vector of length 1/m -- the same degeneracy
        # scripts/join_filter_residues.py reports as the (0,0) residue pair.  The
        # bound is true but says nothing about this rotation as against any other
        # with that property.
        log(f"  DEGENERATE: {len(always)} cross edge(s) are monochromatic under "
            f"every pairing, so the bound is 1 automatically and discriminates "
            f"nothing.")
    pool = IDPool()
    x = [pool.id(("e", k)) for k in range(len(cross))]
    base = [[x[k] for k in sorted(pat)] for pat in patterns]
    for B in range(1, a.max_bound + 1):
        card = CardEnc.atmost(lits=x, bound=B, vpool=pool,
                              encoding=EncType.seqcounter)
        with Solver(name="cadical195", bootstrap_with=base + card.clauses) as s:
            ok = s.solve()
        if ok:
            log(f"  at most {B-1}: UNSAT, at most {B}: SAT  ->  "
                f"needs at least {B} of the {len(cross)} cross edges")
            return B
    log(f"  no hitting set of size <= {a.max_bound}; the bound is above that")
    return None


ALL24 = list(itertools.permutations(range(4)))
FIX0 = [p for p in ALL24 if p[0] == 0]
out = {}
if a.model in ("shared", "both"):
    # The faithful type-M model: the halves meet at the origin, so the origin
    # needs ONE colour, and since both colourings send it to 0 the permutation
    # must fix 0.  The other 18 permutations describe no colouring of the union.
    out["shared"] = run(FIX0, f"halves share the origin, {len(FIX0)} permutations")
if a.model in ("disjoint", "both"):
    # What the published figure computes: all 24, which is the right count only
    # if the two halves share nothing.
    out["disjoint"] = run(ALL24, f"halves disjoint, {len(ALL24)} permutations")
log("")
for k, v in out.items():
    log(f"{J.name} [{k}]: {v}")
