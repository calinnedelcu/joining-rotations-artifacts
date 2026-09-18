#!/usr/bin/env python3
"""The colour pairs the cross unit vectors force, which is the whole converse.

Lambda = R (+) theta(R), so a homomorphism 4-colouring is a pair (phi_1, phi_2),
each a Ducz colouring of its summand.  A cross unit vector u = r + theta(s) is
killed exactly when phi_1(r) = phi_2(theta s), i.e. when phi_1(r) = psi(s) for
psi = phi_2 . theta, itself a Ducz colouring of R.

So fix one Ducz colouring gamma of R and record, over all cross unit vectors,
the pair (gamma(r), gamma(s)) in {1,2,3}^2.  A pairing built from automorphisms
pi_1, pi_2 of the Klein group survives iff pi_1(c1) != pi_2(c2) for every pair
(c1,c2) that occurs.  That is a condition on a subset of a 9-element square.
"""
import os, sys, itertools
from fractions import Fraction
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.joins import rational_spindle
from hn.lattice import Lattice, coeff_vector
from hn.algcolour import klein_colourings, apply_colouring
from hn.construct import rotate
log = lambda s: print(s, flush=True)


def solve_decomp(basis, u):
    """Coefficients of u over `basis` (8 points), exactly, or None."""
    n = len(basis)
    cols = [list(coeff_vector(b)) for b in basis]
    rhs = list(coeff_vector(u))
    rows = len(rhs)
    M = [[Fraction(cols[c][r]) for c in range(n)] + [Fraction(rhs[r])] for r in range(rows)]
    piv = []
    r = 0
    for c in range(n):
        p = next((i for i in range(r, rows) if M[i][c]), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        inv = 1 / M[r][c]
        M[r] = [x * inv for x in M[r]]
        for i in range(rows):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        piv.append(c)
        r += 1
    for i in range(r, rows):
        if M[i][n]:
            return None
    out = [Fraction(0)] * n
    for i, c in enumerate(piv):
        out[c] = M[i][n]
    return out


if __name__ == "__main__":
    from hn.field import set_primes
    for a in [int(x) for x in (sys.argv[1:] or "5 6 9 10 11 13 4 12 16 20".split())]:
        J = rational_spindle(a, 1)
        b = J.build()
        if b is None:
            continue
        WL, WS, cs = b
        R = Lattice(WL)
        lam = Lattice(WL + [rotate(p, cs) for p in WS])
        if lam.rank != 8:
            log(f"a={a}: rank {lam.rank}, skipped")
            continue
        duc = klein_colourings([c for c, _ in R.unit_vectors()], R.rank, 1)
        if not duc:
            log(f"a={a}: no Ducz colouring?!"); continue
        g = duc[0]
        basis = list(R.basis) + [rotate(p, cs) for p in R.basis]
        pairs = set()
        bad = 0
        for _, u in lam.unit_vectors():
            co = solve_decomp(basis, u)
            if co is None or any(x.denominator != 1 for x in co):
                bad += 1
                continue
            rpart = R.combine(tuple(int(x) for x in co[:4]))
            spart = R.combine(tuple(int(x) for x in co[4:]))
            if all(x == 0 for x in co[:4]) or all(x == 0 for x in co[4:]):
                continue                      # not a cross vector
            c1 = apply_colouring(g, R.coords(rpart))
            c2 = apply_colouring(g, R.coords(spart))
            pairs.add((c1, c2))
        AUT = list(itertools.permutations([1, 2, 3]))
        # (0,0) kills every pairing: phi(u) = 0 + 0 regardless of automorphisms.
        # (0,c) and (c,0) with c nonzero never kill anything.
        # Only both-nonzero pairs constrain the automorphisms.
        zero_zero = (0, 0) in pairs
        S = sorted(p for p in pairs if p[0] and p[1])
        works = 0 if zero_zero else sum(
            1 for p1 in AUT for p2 in AUT
            if all(p1[c1 - 1] != p2[c2 - 1] for c1, c2 in S))
        log(f"a={a:3d} {'4|a' if a % 4 == 0 else '   '}  (0,0) present: {str(zero_zero):5}  "
            f"both-nonzero pairs: {str(S):26}  surviving: {works:2d}/36"
            + (f"   ({bad} undecomposed)" if bad else ""))
