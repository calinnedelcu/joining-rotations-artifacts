#!/usr/bin/env python3
"""Check the repaired step 5 of the divisibility law on every rank-8 spindle.

The step used to claim that every rational `lambda` of a cross unit vector is a
ratio of CONSECUTIVE integers, |p - q| = 1.  That is false: a = 39 gives
lambda = -13/15 and -15/13, both with |p - q| = 2.  It went unnoticed because
the measurement stopped at a <= 35.

What is true, and now proved:

    |u|^2 = 1 with s = lambda r gives  rho = |r|^2 = a q^2 / [a d^2 + p q],
    d = q - p.  Since gcd(p,q) = 1, Bezout puts r/q in R, and
    m = |r/q|^2 = rho / q^2 satisfies

        a d^2 + p q = a / m.

    lambda rational forces rho -- hence m -- RATIONAL, and the only rational
    squared norm of a nonzero lattice point below 1/4 is 1/9 (the norms are
    [(A^2+33B^2+3C^2+11D^2) + 2(AB+CD) sqrt33]/144, rational exactly when
    AB + CD = 0).  With p q >= 1 that gives d^2 < 1/m <= 9, so |d| <= 2, and
    |d| = 2 forces m = 1/9 and p q = 5a, with p and q both odd.

    In that case r = q v and s = -p v with |v|^2 = 1/9, and since the colour
    group has exponent 2 and p, q are odd, gamma(r) = gamma(s) = gamma(v).
    v lying in 2R would need |v/2|^2 = 1/36, which the lattice does not attain,
    so gamma(v) != 0 and the vector imposes the same diagonal condition the
    shell displacements of step 2 already impose.

This script checks all of that against the actual cross unit vectors.
"""
import os, sys, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))
from fractions import Fraction
from hn.field import set_primes
from hn.joins import rational_spindle

amax = int(sys.argv[1]) if len(sys.argv) > 1 else 80
print(f"{'a':>4} {'rank':>4} {'cross':>6}  lambda profile")
bad = []
for A in range(2, amax + 1):
    J = rational_spindle(A, 1)
    set_primes(J.primes)
    import hn.construct as C
    C.refresh_field()
    J = rational_spindle(A, 1)
    b = J.build()
    if b is None:
        continue
    WL, _, cs = b
    from hn.construct import rotate
    from hn.lattice import Lattice
    from hn.algcolour import klein_colourings, apply_colouring
    from cross_pairs import solve_decomp
    R = Lattice(WL)
    LAM = Lattice(list(WL) + [rotate(p, cs) for p in WL])
    if LAM.rank != 8:
        continue
    gs = klein_colourings([c for c, _ in R.unit_vectors()], R.rank)
    basis = list(R.basis) + [rotate(p, cs) for p in R.basis]
    prof = collections.Counter()
    irr = 0
    for _, u in LAM.unit_vectors():
        co = solve_decomp(basis, u)
        if co is None or any(x.denominator != 1 for x in co):
            continue
        if all(x == 0 for x in co[:4]) or all(x == 0 for x in co[4:]):
            continue
        r = R.combine(tuple(int(x) for x in co[:4]))
        s = R.combine(tuple(int(x) for x in co[4:]))
        L = s.x / r.x if not r.x.is_zero() else s.y / r.y
        if any(L.n[i] for i in range(1, 8)):
            irr += 1
            continue
        lam = Fraction(L.n[0], L.d)
        if lam == -1:
            prof["lambda=-1"] += 1
            continue
        p, q = -lam.numerator, lam.denominator
        d = abs(p - q)
        prof[f"|d|={d}"] += 1
        if d > 2:
            bad.append((A, lam, "|d| > 2"))
        if d == 2:
            if p * q != 5 * A:
                bad.append((A, lam, f"pq={p*q} not 5a={5*A}"))
            if p % 2 == 0 or q % 2 == 0:
                bad.append((A, lam, "p or q even"))
            for g in gs:
                c1 = apply_colouring(g, R.coords(r))
                c2 = apply_colouring(g, R.coords(s))
                if c1 != c2 or c1 == 0:
                    bad.append((A, lam, f"gamma {c1},{c2}"))
    tag = " ".join(f"{k}:{v}" for k, v in sorted(prof.items()))
    print(f"{A:>4} {LAM.rank:>4} {sum(prof.values()):>6}  {tag}"
          + (f"   +{irr} irrational" if irr else ""), flush=True)
print()
print(f"violations of the repaired step 5: {len(bad)}")
for x in bad[:20]:
    print("   ", x)
