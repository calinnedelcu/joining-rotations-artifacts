#!/usr/bin/env python3
"""The five working rotations of Voronov, Neopryatnaya and Dergachev, checked.

Their first series (arXiv:2106.11824, Table 5) is built on the Moser spindle with
generators 1/2 + sqrt3/2 i and sqrt33/6 + sqrt3/6 i -- that is, on the Moser
lattice R -- and reports five rotations carrying a 5-chromatic graph.  So five
type-M rotations were known, not one, and the paper says so.

This script establishes the three facts the paper then claims about them:

  1. all five are rho*u, with rho = 7/8 + i sqrt15/8 Heule's rotation and u one
     of the 30 unit vectors of R;
  2. only one of the five u fixes R, so the other four joins are genuinely
     different lattices -- being "rho times a unit" does NOT collapse them;
  3. exactly one of the five rotations has rational cosine, so exactly one is a
     spindle, namely rho = theta_4 itself.

and one check on us:

  4. the criterion of section 2 returns "unknown" on all five.  Every one of them
     carries a verified 5-chromatic graph, so a DEAD verdict on any would mean
     the criterion is unsound.

Run: .venv/bin/python scripts/voronov_rotations.py
"""
import cmath
import math
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from hn.field import set_primes, K, Pt
set_primes((3, 5, 11))
from hn.construct import unit_vector_family, pt_float, ball
from hn.lattice import Lattice
from hn.algcolour import certify

# Table 5 of arXiv:2106.11824, the imaginary parts of the five rotations.
TABLE5 = [0.48412291, 0.24642936, 0.21092166, 0.08023868, 0.04383445]


def mul(a, b):
    return Pt(a.x * b.x - a.y * b.y, a.x * b.y + a.y * b.x)


def conj(p):
    return Pt(p.x, K.zero() - p.y)


def main():
    rho = Pt(K.rat(7, 8), K.root(15) * K.rat(1, 8))
    assert rho.norm2().is_one(), "rho is not a rotation"
    vecs = unit_vector_family(2)
    L = Lattice(vecs)
    pts = ball(vecs, 3, 2.05)

    # 1. match each table entry to rho * (unit vector)
    matched = []
    for target in TABLE5:
        for u in vecs:
            for base in (rho, conj(rho)):
                psi = mul(base, u)
                if abs(abs(complex(*pt_float(psi)).imag) - target) < 5e-8:
                    matched.append((target, u, psi))
                    break
            else:
                continue
            break
    assert len(matched) == 5, f"only matched {len(matched)} of 5"
    print("1. all five are rho * (a unit vector of R):")
    for target, u, psi in matched:
        print(f"     Im psi = {target:.8f}   arg u = "
              f"{math.degrees(cmath.phase(complex(*pt_float(u)))):8.3f} deg")

    # 2. which of those units fix R?
    print("\n2. does multiplying by u fix R?")
    fixes = 0
    for target, u, _ in matched:
        fwd = all(L.coords(mul(u, p)) is not None for p in pts)
        bwd = all(L.coords(mul(conj(u), p)) is not None for p in pts)
        same = fwd and bwd
        fixes += same
        print(f"     Im psi = {target:.8f}   {'fixes R' if same else 'MOVES R'}")
    assert fixes == 1, f"expected exactly one, got {fixes}"
    print(f"     -> {fixes} of 5, so four joint lattices genuinely differ")

    # 3. a spindle is exactly a rotation of rational cosine
    print("\n3. which are spindles (rational cosine)?")
    spindles = 0
    for target, _, psi in matched:
        rat = all(psi.x.n[i] == 0 for i in range(1, 8))
        spindles += rat
        if rat:
            c = Fraction(psi.x.n[0], psi.x.d)
            print(f"     Im psi = {target:.8f}   cos = {c}  -> a = "
                  f"{Fraction(1, 2) / (1 - c)}")
        else:
            print(f"     Im psi = {target:.8f}   cos irrational, not a spindle")
    assert spindles == 1, f"expected exactly one spindle, got {spindles}"

    # 4. the criterion must not kill any of them
    print("\n4. the criterion of section 2 on all five:")
    for target, _, psi in matched:
        v = certify(list(vecs) + [mul(psi, w) for w in vecs])
        print(f"     Im psi = {target:.8f}   rank {v.lattice.rank}, "
              f"{len(v.units):3d} unit vectors -> {v.verdict}")
        assert not v.dead, "criterion killed a rotation known to work -- UNSOUND"
    print("\nall four checks passed")


if __name__ == "__main__":
    main()
