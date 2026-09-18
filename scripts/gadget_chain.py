#!/usr/bin/env python3
"""Chaining Parts' monochromatic-pair gadget: the rotations it already settles.

Parts publishes two minimal monochromatic-pair gadgets in the Moser lattice: 367
vertices with terminals (-4/3, 0) and (4/3, 0), at distance 8/3, and 421 with
terminals at distance 8/sqrt3.  A gadget M with terminals 0, t forces every proper
4-colouring to give its two terminals the same colour.  Since R is a group and
t lies in it, the translates M + j t lie in R too, so

    M_n = union of (M + j t) for 0 <= j < n

forces colour(0) = colour(n t), and has at most n(|M| - 1) + 1 vertices.  Put one
terminal at the origin and join with the spindle theta_a at a = |n t|^2: the far
terminal and its image are one unit apart and must share a colour, so

    M_n  u  theta_a(M_n)

is not 4-colourable.  That settles a = 64 n^2 / 9 for every n -- 64/9, 256/9, 64,
1024/9 -- with no search, and a = 64 is the case this paper's filters leave
undecided.

A minimal non-4-colourable induced subgraph containing the origin is exactly
5-chromatic: deleting any other vertex gives a proper 4-colouring, and restoring
it with a fifth colour extends that.  It is still a join of two copies at a
shared origin.

Run: .venv/bin/python scripts/gadget_chain.py [n]        (default 3, i.e. a = 64)
"""
import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
from fractions import Fraction as Frac
A = Frac(64 * n * n, 9)                 # squared radius, = |n t|^2 with t = 8/3
# cos = (2a-1)/(2a), sin = sqrt(4a-1)/(2a).  The third generator of the field is
# whatever 4a-1 needs beyond the sqrt3 the lattice already has; at n = 3,
# 4a-1 = 255 = 3*5*17, so the lattice supplies one factor and 85 the other.
ROT = {1: (247,  lambda K: K.root(247)  * K.rat(3, 128)),
       2: (1015, lambda K: K.root(1015) * K.rat(3, 512)),
       3: (85,   lambda K: K.root(3) * K.root(85) * K.rat(1, 128)),
       4: (4087, lambda K: K.root(4087) * K.rat(3, 2048))}
assert n in ROT, f"n = {n} not tabulated"
RADICAND = {k: v[0] for k, v in ROT.items()}
log = lambda s: print(s, flush=True)

from hn.field import set_primes, K, Pt, is_unit
set_primes((3, 11, RADICAND[n]))
from hn import construct as C
C.refresh_field()
from hn.io import load_vtx
from hn.lattice import Lattice
from hn.construct import unit_vector_family, edges_grid, to_float
from hn import verify, find_triangle

t0 = time.time()
M = load_vtx(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                          "data", "parts", "v367e1822.vtx"))
W = unit_vector_family(2); L0 = Lattice(W)
assert all(L0.coords(p) is not None for p in M), "the gadget is not inside R"
log(f"1. Parts' gadget: {len(M)} vertices, every one of them in R")

key = lambda p: (str(p.x), str(p.y))
E = edges_grid(M)
log(f"2. edges recomputed from the coordinates: {len(E)}  (his file says 1822)")

idx = {key(p): i for i, p in enumerate(M)}
i0, i1 = idx[key(Pt(K.rat(-4, 3), K.rat(0)))], idx[key(Pt(K.rat(4, 3), K.rat(0)))]
d = M[i1].x - M[i0].x
log(f"3. terminals at -4/3 and 4/3, squared distance {to_float(d*d):.6f} = (8/3)^2")

# the gadget property, re-proved rather than cited: force them apart -> UNSAT
tri = find_triangle(len(M), E)
split = verify(M, E + [(i0, i1)], triangle=tri)
log(f"4. with the terminals forced apart the graph is not 4-colourable: {split}")
assert split, "Parts' gadget does not have the monochromatic-pair property"
assert not verify(M, E, triangle=tri), "the gadget itself is not 4-colourable"

pts, seen = [], set()
for j in range(n):
    for p in M:
        q = Pt(p.x + K.rat(8 * j, 3), p.y)
        if key(q) not in seen:
            seen.add(key(q)); pts.append(q)
log(f"5. chain of {n}: {len(pts)} vertices (bound {n*(len(M)-1)+1})")

pts = [Pt(p.x + K.rat(4, 3), p.y) for p in pts]          # left terminal to the origin
FAR = Pt(K.rat(8 * n, 3), K.rat(0))
assert key(FAR) in {key(p) for p in pts}
log(f"   terminals now 0 and {to_float(FAR.x):.4f}, so a = {A}")

cosf = (2 * A - 1) / (2 * A)
c = K.rat(cosf.numerator, cosf.denominator)
s = ROT[n][1](K)
log(f"6. theta_a: cos = {cosf}, modulus exactly 1: {(c*c + s*s).is_one()}")
assert (c * c + s * s).is_one(), "cos^2 + sin^2 is not 1 -- wrong field or wrong sine"

rot = lambda p: Pt(p.x * c - p.y * s, p.x * s + p.y * c)
U, seen2 = [], {}
for p in list(pts) + [rot(p) for p in pts]:
    if key(p) not in seen2:
        seen2[key(p)] = len(U); U.append(p)
log(f"7. union with its image, sharing the origin: {len(U)} vertices")
tE = time.time(); EU = edges_grid(U)
log(f"   edges: {len(EU)}  ({time.time()-tE:.0f}s)")
assert is_unit(U[seen2[key(FAR)]], U[seen2[key(rot(FAR))]]), \
    "the two far terminals are not at unit distance"
log("   the two far terminals are at unit distance")

# 8. The structural check, which is what the proof actually needs: each copy of
# the gadget must sit inside the union INTACT, so that its monochromatic-pair
# property applies to it there.  Given that, plus the shared terminals of step 5
# and the unit pair of step 7, the union cannot be 4-coloured -- and this costs
# nothing, where solving the union directly costs hours at n = 3 and settles
# nothing the argument did not already have.
EUset = {tuple(sorted(e)) for e in EU}
EMset = {tuple(sorted(e)) for e in edges_grid(M)}
copies = [[Pt(p.x + K.rat(8*j, 3) + K.rat(4, 3), p.y) for p in M] for j in range(n)]
copies += [[rot(p) for p in cp] for cp in list(copies)]
for k, cp in enumerate(copies):
    loc = [seen2[key(p)] for p in cp]
    missing = [(a, b) for a, b in EMset
               if tuple(sorted((loc[a], loc[b]))) not in EUset]
    assert not missing, f"copy {k} lost {len(missing)} of its edges in the union"
log(f"8. all {len(copies)} gadget copies sit inside the union intact, "
    f"{len(EMset)}/{len(EMset)} edges each")
dead = True

if os.environ.get("GADGET_CHAIN_SOLVE"):      # the redundant direct solve
    t = time.time()
    dead = verify(U, EU, triangle=find_triangle(len(U), EU))
    log(f"   direct solve confirms NOT 4-colourable: {dead}   ({time.time()-t:.0f}s)")
log(f"\n=> a = {A} carries a 5-chromatic join on at most {len(U)} "
    f"vertices.   total {time.time()-t0:.0f}s")
if not dead:
    raise SystemExit(1)
