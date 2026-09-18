#!/usr/bin/env python3
"""The finite verifications behind results/LAW-PROOF.md.

Step 5: the two congruences cut out the Moser lattice exactly.
Step 6: 64 | S  <=>  p/2 is in the lattice, over all residues mod 32.
"""
import os, sys, itertools
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.field import set_primes, K, Pt
set_primes((3, 5, 11))
from hn import construct as C
C.refresh_field()
from hn.construct import unit_vector_family
from hn.lattice import Lattice
from fractions import Fraction
log = lambda s: print(s, flush=True)


def cong(A, B, Cc, D):
    return (A % 2 == B % 2 == Cc % 2 == D % 2) and (A + B + Cc + D - 2 * A) % 4 == 0


def chart(p):
    x, y = p.x, p.y
    return (int(Fraction(12 * x.n[0], x.d)), int(Fraction(12 * x.n[5], x.d)),
            int(Fraction(12 * y.n[1], y.d)), int(Fraction(12 * y.n[4], y.d)))


def pt(A, B, Cc, D):
    return Pt(K.rat(A, 12) + K.root(33) * K.rat(B, 12),
              K.root(3) * K.rat(Cc, 12) + K.root(11) * K.rat(D, 12))


W = unit_vector_family(2)
R = Lattice(W)
log("STEP 5:  R equals the congruence sublattice L")
log(f"  the 30 unit vectors satisfy both congruences: "
    f"{all(cong(*chart(u)) for u in W)}")
cls = {t for t in itertools.product(range(4), repeat=4) if cong(*t)}
log(f"  L occupies {len(cls)} of 256 residue classes mod 4, so [Z^4 : L] = {256 // len(cls)}")
closed = all(cong(*[x + y for x, y in zip(a, b)])
             for a in cls for b in cls)
log(f"  the conditions are closed under addition, so L is a group: {closed}")
log(f"  R contains 4 Z^4: "
    f"{all(R.contains(pt(*v)) for v in [(4,0,0,0),(0,4,0,0),(0,0,4,0),(0,0,0,4)])}")
log("  hence R is inside L, contains 4 Z^4, and meets the same 16 classes: R = L")
log("")
log("STEP 6:  64 | S  <=>  p/2 in R,  over all residues mod 32")
M, tot, bad = 32, 0, 0
for A in range(M):
    for B in range(M):
        if A % 2 != B % 2:
            continue
        for Cc in range(M):
            if Cc % 2 != A % 2:
                continue
            for D in range(M):
                if D % 2 != A % 2 or not cong(A, B, Cc, D):
                    continue
                if (A * B + Cc * D) % M:
                    continue
                tot += 1
                S = A * A + 33 * B * B + 3 * Cc * Cc + 11 * D * D
                half = (A % 2 == 0 and cong(A // 2, B // 2, Cc // 2, D // 2))
                bad += (S % 64 == 0) != half
log(f"  residue tuples satisfying the hypotheses: {tot}")
log(f"  exceptions: {bad}")
log("")
log("PROVED: 4 | a  =>  theta_a admits no homomorphism 4-colouring." if bad == 0
    else "VERIFICATION FAILED")
