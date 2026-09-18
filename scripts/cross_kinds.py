#!/usr/bin/env python3
"""How many KINDS of joining edge each rotation has -- Parts' type-M test.

Parts calls a join type M when its interface carries joining edges of two or
more kinds.  A joining edge is a unit vector of the joint lattice; by
Proposition 18 the whole infinite union has finitely many, enumerated exactly
from the trace form with no ball.  Each one decomposes as u = r + psi(s) in the
direct sum, so it has two endpoints, p = r on one side and psi(q) with q = -s on
the other, and its KIND is the unordered pair of squared radii {|p|^2, |q|^2}.
Edges out of the shared origin are excluded: every join has those thirty each
way, they are the same for all rotations, and Parts' count is of the others.

This settles two claims of Section 7 at once:

  * the four integer spindles have 2, 4, 3 and 2 kinds, so all four are type M;
  * each of the five rotations already known -- Voronov, Neopryatnaya and
    Dergachev's series, which is rho*u for the thirty unit vectors u -- has
    exactly 2, so all five are type M as well.

theta_4 = rho is in both lists, so the constructions give 4 + 5 - 1 = 8 type-M
rotations where Parts recorded one.

Run: .venv/bin/python scripts/cross_kinds.py
"""
import collections, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, HERE)

FAIL = []
def check(label, got, want):
    ok = got == want
    if not ok: FAIL.append((label, got, want))
    print(f"  {'ok ' if ok else 'BAD'} {label:<44} {str(got):>18}"
          + ("" if ok else f"   expected {want}"))


def census(L0, basis, LAM, zero):
    """(total edges, edges at the shared origin, Counter of kinds)."""
    from cross_pairs import solve_decomp
    rows = []
    for _, v in LAM.unit_vectors():
        co = solve_decomp(basis, v)
        assert co is not None and all(x.denominator == 1 for x in co), \
            "a unit vector left the direct sum"
        r = L0.combine(tuple(int(x) for x in co[:L0.rank]))
        q = L0.combine(tuple(-int(x) for x in co[L0.rank:]))
        rows.append((str(r.norm2()), str(q.norm2())))
    off = [t for t in rows if zero not in t]
    return len(rows), len(rows) - len(off), collections.Counter(
        tuple(sorted(t)) for t in off)


def spindles():
    from hn.joins import rational_spindle
    from hn.lattice import Lattice
    from hn.construct import rotate
    from hn.field import K
    zero = str(K.zero())
    print("1. the seven joining spindles of Section 7")
    for a, b, want in ((4, 1, 2), (16, 1, 4), (28, 1, 3), (36, 1, 2),
                       (64, 3, 1), (64, 9, 1), (256, 9, 1)):
        WL, _, cs = rational_spindle(a, b).build()
        L0 = Lattice(WL)
        LAM = Lattice(list(WL) + [rotate(p, cs) for p in WL])
        basis = list(L0.basis) + [rotate(p, cs) for p in L0.basis]
        n, org, kinds = census(L0, basis, LAM, zero)
        name = f"theta_{a}" if b == 1 else f"alpha_{a}/{b}"
        check(f"{name}: {n} edges, {org} at the origin, kinds", len(kinds), want)


def known():
    """Voronov-Neopryatnaya-Dergachev's five, arXiv:2106.11824 Table 5."""
    import cmath
    from hn.field import set_primes, K, Pt
    set_primes((3, 5, 11))
    import hn.construct as C; C.refresh_field()
    from hn.construct import unit_vector_family, pt_float
    from hn.lattice import Lattice
    TABLE5 = [0.48412291, 0.24642936, 0.21092166, 0.08023868, 0.04383445]
    mul = lambda a, b: Pt(a.x*b.x - a.y*b.y, a.x*b.y + a.y*b.x)
    conj = lambda p: Pt(p.x, K.zero() - p.y)
    rho = Pt(K.rat(7, 8), K.root(15) * K.rat(1, 8))
    W = list(unit_vector_family(2))
    L0, zero = Lattice(W), str(K.zero())

    print("\n2. the five rotations already known, each rho times a unit vector")
    for target in TABLE5:
        psi = next(p for u in W for b in (rho, conj(rho))
                   for p in [mul(b, u)]
                   if abs(abs(complex(*pt_float(p)).imag) - target) < 5e-8)
        LAM = Lattice(W + [mul(psi, w) for w in W])
        basis = list(L0.basis) + [mul(psi, b) for b in L0.basis]
        n, org, kinds = census(L0, basis, LAM, zero)
        check(f"Im psi = {target:.8f}: {n} edges, {org} at 0, kinds",
              len(kinds), 2)


if __name__ == "__main__":
    spindles()
    known()
    print("\nSo every one of the eight is type M in Parts' sense "
          "(theta_4 = rho lies in both lists).")
    if FAIL:
        print(f"\n{len(FAIL)} DISAGREEMENT(S):")
        for l, g, w in FAIL: print(f"   {l}: got {g}, expected {w}")
        raise SystemExit(1)
