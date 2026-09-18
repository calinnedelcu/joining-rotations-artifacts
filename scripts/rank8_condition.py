#!/usr/bin/env python3
"""When does the joint lattice have rank 8?  The hypothesis of Theorem 1.

Proposition: theta_a maps the Q-span of R onto itself exactly when
sqrt(4a-1) lies in Q(sqrt3, sqrt11), which happens exactly when 4a-1 = 3k^2 or
11k^2 -- and then the joint lattice has rank 4, not 8.

The proposition's equivalences are proved in the paper.  What is measured here,
and what this script asserts, is the remaining clause: at every OTHER a the rank
is exactly 8, never something between 4 and 8.

Run: .venv/bin/python scripts/rank8_condition.py   (about a minute)
"""
import os
import sys
from fractions import Fraction
from math import isqrt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.joins import rational_spindle
from hn.lattice import Lattice
from hn.construct import rotate

A_MAX = 45
EXTRA = [61, 69, 91, 97, 100]
RATIONALS = [(1, 3), (7, 3), (13, 3), (31, 3), (43, 3), (4, 3), (64, 3),
             (64, 9), (256, 9)]


def excluded(a):
    """4a-1 = 3k^2 or 11k^2 for a RATIONAL k.

    `a` may be a Fraction.  For integer a the rational k is forced integral, but
    Theorem 1 admits rational a and there the rational form genuinely bites --
    a = 1/3, 7/3, 13/3, 31/3, 43/3 all have rank 4 with a non-empty shell.
    """
    v = Fraction(4 * a - 1)
    for m in (3, 11):
        r = v / m
        if r <= 0:
            continue
        pn, pd = isqrt(r.numerator), isqrt(r.denominator)
        if pn * pn == r.numerator and pd * pd == r.denominator:
            return m, Fraction(pn, pd)
    return None


def main():
    print(f"{'a':>4} {'4a-1':>6} {'form':>12} {'rank':>5}  agree")
    seen = mism = 0
    for a in list(range(1, A_MAX + 1)) + EXTRA:
        built = rational_spindle(a, 1).build()
        if built is None:
            continue                      # the rotation is not in its own field
        WL, _, cs = built
        rank = Lattice(list(WL) + [rotate(w, cs) for w in WL]).rank
        ex = excluded(a)
        want = 4 if ex else 8
        ok = rank == want
        mism += not ok
        seen += 1
        print(f"{a:>4} {4*a-1:>6} {(f'{ex[0]}*{ex[1]}^2' if ex else '--'):>12} "
              f"{rank:>5}  {'OK' if ok else '*** MISMATCH ***'}")
    print("\nrational a, where the integer form of the criterion would be wrong:")
    for n, b in RATIONALS:
        built = rational_spindle(n, b).build()
        if built is None:
            continue
        WL, _, cs = built
        rank = Lattice(list(WL) + [rotate(w, cs) for w in WL]).rank
        ex = excluded(Fraction(n, b))
        want = 4 if ex else 8
        ok = rank == want
        mism += not ok
        seen += 1
        print(f"{f'{n}/{b}':>8} {str(Fraction(4*n, b) - 1):>8} "
              f"{(f'{ex[0]}*({ex[1]})^2' if ex else '--'):>14} {rank:>5}  "
              f"{'OK' if ok else '*** MISMATCH ***'}")
    print(f"\n{seen} rotations tested, {mism} mismatches")
    print(f"range: every integer a <= {A_MAX}, then "
          f"{', '.join(str(a) for a in EXTRA)}, and the rational a "
          + ", ".join(f"{n}/{b}" for n, b in RATIONALS))
    print("excluded a <= 100:", [a for a in range(1, 101) if excluded(a)])
    assert mism == 0, "the rank is not what the proposition says"
    print("\nrank 4 exactly at the excluded a, rank 8 everywhere else")


if __name__ == "__main__":
    main()
