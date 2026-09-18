#!/usr/bin/env python3
"""The family {rho*u}, and the fact that neither of our filters can touch it.

Voronov, Neopryatnaya and Dergachev's working rotations are rho*u with rho
Heule's rotation and u a unit vector of the Moser lattice (see
scripts/voronov_rotations.py).  That is a family of 30.  This sweeps all of them
and reports what our two tests say, which is: nothing.

  - the homomorphism criterion of section 2 kills 0 of 30;
  - the periodic filter of section 7, strictly stronger, kills 0 of 30 too,
    degenerating at m = 4 and m = 8 alike.

For contrast, on the integer spindles the law kills three a in four and the
periodic filter kills eleven of the sixteen that survive it.  So the tools are
specific to spindles; whatever decides {rho*u} is not in the paper.

Structure the sweep also pins down:
  - exactly 6 of the 30 u fix R -- the sixth roots of unity -- so those give back
    theta_4's own joint lattice;
  - exactly 2 of the 30 rotations are spindles (rational cosine), rho and -rho;
  - all 30 joint lattices have rank 8, with 126, 108 or 90 unit vectors.

Run: .venv/bin/python scripts/rho_unit_family.py   (about 5 minutes)
"""
import cmath
import math
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from hn.field import set_primes, K, Pt
set_primes((3, 5, 11))
from hn.construct import unit_vector_family, pt_float, ball
from hn.lattice import Lattice
from hn.algcolour import certify

VORONOV = [0.48412291, 0.24642936, 0.21092166, 0.08023868, 0.04383445]


def mul(a, b):
    return Pt(a.x * b.x - a.y * b.y, a.x * b.y + a.y * b.x)


def conj(p):
    return Pt(p.x, K.zero() - p.y)


def main():
    rho = Pt(K.rat(7, 8), K.root(15) * K.rat(1, 8))
    assert rho.norm2().is_one()
    vecs = unit_vector_family(2)
    L = Lattice(vecs)
    pts = ball(vecs, 3, 2.05)

    t0 = time.time()
    fixes = spindles = killed_hom = killed_per = 0
    print(f"{'arg u':>9} {'cos psi':>11} {'fixes R':>8} {'spindle':>8} "
          f"{'rank':>5} {'units':>6} {'homomorphism':>13} {'periodic':>10}  Voronov")
    for u in sorted(vecs, key=lambda v: cmath.phase(complex(*pt_float(v)))):
        psi = mul(rho, u)
        assert psi.norm2().is_one()
        gens = list(vecs) + [mul(psi, w) for w in vecs]

        fix = (all(L.coords(mul(u, p)) is not None for p in pts)
               and all(L.coords(mul(conj(u), p)) is not None for p in pts))
        rat = all(psi.x.n[i] == 0 for i in range(1, 8))
        hom = certify(gens)
        per = certify(gens, groups=(), moduli=(4, 8))
        fixes += fix
        spindles += rat
        killed_hom += hom.dead
        killed_per += per.dead

        assert hom.lattice.rank == 8, "rank-8 hypothesis fails here"
        c = complex(*pt_float(psi))
        known = any(abs(abs(c.imag) - x) < 5e-8 for x in VORONOV)
        print(f"{math.degrees(cmath.phase(complex(*pt_float(u)))):9.3f} {c.real:11.7f} "
              f"{str(fix):>8} {str(rat):>8} {hom.lattice.rank:5d} {len(hom.units):6d} "
              f"{'DEAD' if hom.dead else 'no kill':>13} "
              f"{'DEAD' if per.dead else 'no kill':>10}  {'yes' if known else ''}")

    n = len(vecs)
    print(f"\n  units fixing R (same joint lattice as theta_4): {fixes} of {n}")
    print(f"  spindles (rational cosine):                     {spindles} of {n}")
    print(f"  killed by the homomorphism criterion:           {killed_hom} of {n}")
    print(f"  killed by the periodic filter (m = 4, 8):       {killed_per} of {n}")
    print(f"  ({time.time() - t0:.0f}s)")
    assert fixes == 6 and spindles == 2
    assert killed_hom == 0 and killed_per == 0, \
        "a filter now kills something here -- the paper's limitation claim is stale"
    print("\nboth filters are blind to this family, as the paper states")


if __name__ == "__main__":
    main()
