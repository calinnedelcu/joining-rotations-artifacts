#!/usr/bin/env python3
"""Theorem 4's count, done directly in R/2R.

A homomorphism onto the Klein group killing no unit vector is exactly a subgroup
of index 4 containing 2R that meets none of the 30 unit vectors.  So the whole
question is finite and lives in R/2R = F_2^4:

  * the 30 unit vectors fall into 9 distinct nonzero classes;
  * the index-4 subgroups containing 2R are the 35 two-dimensional subspaces;
  * exactly 2 of the 35 avoid all nine -- which recovers Ducz's count by
    enumeration rather than by his sublattice argument.

This is the enumeration the paper's proof of Theorem 4 replaces; the structural
argument (R/2R = F_4 x F_4, and a plane missing all nine is a union of two
subgroups) is in `moser_is_ov.py`.  The two are then IDENTIFIED here the only way
that settles it, by testing gamma_i(x) = 0 <=> pi_i | x at every point of a ball.

Stability does not identify them, and the script says so rather than concluding
from it: both survivors are O-stable, but so are eleven of the thirty-five, since
multiplication by sqrt33 is the identity on R/2R.  An earlier version of this file
ended "both survivors are O-stable, so they are pi_1 R and pi_2 R", which does not
follow.

The stability of a kernel is tested on real points rather than through a
change-of-basis matrix: the matrix route needs the echelon convention to match
`coords` exactly, and getting that wrong gives a confidently wrong answer.

Run: .venv/bin/python scripts/two_colourings.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.field import set_primes, K, Pt
set_primes((3, 5, 11))
from hn.construct import ball, unit_vector_family
from hn.lattice import Lattice


def mul(a, b):
    return Pt(a.x * b.x - a.y * b.y, a.x * b.y + a.y * b.x)


def main():
    vecs = unit_vector_family(2)
    L = Lattice(vecs)
    assert L.rank == 4, L.rank
    pts = ball(vecs, 3, 2.05)

    def cls(p):
        c = L.coords(p)
        return None if c is None else sum((x & 1) << k for k, x in enumerate(c))

    U = {cls(v) for v in vecs}
    assert 0 not in U
    print(f"R/2R = F_2^4;  the 30 unit vectors give {len(U)} nonzero classes")

    subs = set()
    for a in range(1, 16):
        for b in range(a + 1, 16):
            sp = frozenset({0, a, b, a ^ b})
            if len(sp) == 4:
                subs.add(sp)
    print(f"index-4 subgroups of R containing 2R: {len(subs)}")

    good = sorted((sorted(g) for g in subs if not (g & U)))
    print(f"of those, missing every unit-vector class: {len(good)}")
    for g in good:
        print(f"   {g}")
    assert len(good) == 2, "Ducz's count is not recovered"

    # identify them: gamma_i(x) = 0 <=> pi_i | x, at every point of the ball.
    # 1/pi_1 = (-5 + sqrt33)/4 and 1/pi_2 = (-5 - sqrt33)/4, both exact in K.
    INV = {1: Pt(K.rat(-5, 4) + K.root(33) * K.rat(1, 4), K.zero()),
           2: Pt(K.rat(-5, 4) - K.root(33) * K.rat(1, 4), K.zero())}
    print(f"\ngamma_i(x) = 0 <=> pi_i | x, on the depth-3 ball ({len(pts)} points):")
    named = {}
    for g in good:
        gs = set(g)
        for i, inv in INV.items():
            div = [L.coords(mul(p, inv)) is not None for p in pts]
            zero = [cls(p) in gs for p in pts]
            if div == zero:
                named[i] = g
                print(f"   {g} = ker gamma_{i} = pi_{i} R   "
                      f"({sum(div)} of {len(pts)} divisible, agreement everywhere)")
    assert set(named) == {1, 2} and named[1] != named[2], \
        "the two survivors are not the two prime reductions"

    # and stability does not single them out: eleven of the 35 are O-stable
    omega = Pt(K.rat(1, 2) + K.root(33) * K.rat(1, 2), K.zero())
    s33 = Pt(K.root(33), K.zero())
    print("\nO-stability, tested on the depth-3 ball:")
    for g in good:
        gs = set(g)
        ker = [p for p in pts if cls(p) in gs]
        a = sum(1 for p in ker if cls(mul(omega, p)) in gs)
        b = sum(1 for p in ker if cls(mul(s33, p)) in gs)
        print(f"   {g}: {len(ker):4d} points, (1+sqrt33)/2 keeps {a}, sqrt33 keeps {b}")
        assert a == len(ker) == b, "a kernel is not O-stable"
    # the action of (1+sqrt33)/2 on R/2R, read off the ball rather than off a
    # basis, so that no echelon convention can enter: every point of a class must
    # give the same image class, and the script checks that it does.
    act = {}
    for p in pts:
        w, iw = cls(p), cls(mul(omega, p))
        if w in act: assert act[w] == iw, f"class {w} has two images"
        else: act[w] = iw
    assert len(act) == 16, f"the ball meets only {len(act)} of the 16 classes"
    stable = [g for g in subs if all(act[w] in g for w in g)]
    print(f"   but so are {len(stable)} of the {len(subs)}, since sqrt33 is the "
          f"identity on R/2R -- stability does not identify them")
    assert len(stable) == 11, len(stable)
    print("\nthe two survivors are pi_1 R and pi_2 R, by the divisibility test above")


if __name__ == "__main__":
    main()
