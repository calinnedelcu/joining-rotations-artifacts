#!/usr/bin/env python3
"""The lemma that closes step 5, checked on every rank-8 spindle.

    LEMMA.  Let pi be a prime of O = Z[(1+sqrt33)/2] above 2, and let
    u = r + theta(s) be a cross unit vector with s = lambda r, lambda != -1,
    written lambda = alpha/beta with alpha, beta coprime in O and v = r/beta.
    If pi divides none of v, alpha, beta then a is ODD.

    Proof.  The residue field is F_2, so alpha = beta = 1 there, hence
    alpha - beta = 0 and alpha beta = 1, and

        W = a (alpha - beta)^2 + (4a-1) alpha beta = 4a - 1 = 1   (mod pi),

    so pi does not divide W.  From |v|^2 W = a we get v_pi(|v|^2) = v_2(a),
    and pi not dividing v makes the left side 0.  So a is odd.

    CONTRAPOSITIVE, which is what step 5 needs:  a EVEN implies pi divides one
    of v, alpha, beta, hence pi divides r = beta v or s = alpha v, hence
    gamma_pi(r) = 0 or gamma_pi(s) = 0 -- because ker gamma_pi = pi R.

This checks the contrapositive directly against the cross vectors: for every
one with lambda != -1, and each of the two primes, whether pi divides r or s,
against the parity of a.

It also checks the trichotomy that now carries steps 4 and 5.  Corollary 12
says pi does not divide v when 4 does not divide a, so gamma_i(r) and
gamma_i(s) are each either 0 or gamma_i(v) != 0, and alpha, beta being coprime
they are never both 0.  So for 4 not dividing a, no cross vector has pi
dividing BOTH r and s.  That is the second counter below.
"""
import os, sys, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))
from fractions import Fraction
from hn.field import set_primes
from hn.joins import rational_spindle

amax = int(sys.argv[1]) if len(sys.argv) > 1 else 60
bad, both, seen = [], [], 0
print(f"{'a':>4} {'par':>4} {'cross':>6}  pi_1 divides r or s / pi_2 divides r or s")
for A in range(2, amax + 1):
    J = rational_spindle(A, 1)
    set_primes(J.primes)
    import hn.construct as C
    C.refresh_field()
    from hn.field import K as KK
    J = rational_spindle(A, 1)
    b = J.build()
    if b is None:
        continue
    WL, _, cs = b
    from hn.construct import rotate, Pt
    from hn.lattice import Lattice
    from cross_pairs import solve_decomp
    R = Lattice(WL)
    LAM = Lattice(list(WL) + [rotate(p, cs) for p in WL])
    if LAM.rank != 8:
        continue
    r33 = KK.root(33)
    pis = [(KK.rat(5) + r33) * KK.rat(1, 2), (KK.rat(5) - r33) * KK.rat(1, 2)]
    invs = [p.inv() for p in pis]
    def div(i, p):
        return R.contains(Pt(p.x * invs[i], p.y * invs[i]))
    basis = list(R.basis) + [rotate(p, cs) for p in R.basis]
    cnt = collections.Counter()
    n = 0
    for _, u in LAM.unit_vectors():
        co = solve_decomp(basis, u)
        if co is None or any(x.denominator != 1 for x in co):
            continue
        if all(x == 0 for x in co[:4]) or all(x == 0 for x in co[4:]):
            continue
        r = R.combine(tuple(int(x) for x in co[:4]))
        s = R.combine(tuple(int(x) for x in co[4:]))
        L = s.x / r.x if not r.x.is_zero() else s.y / r.y
        rational = not any(L.n[i] for i in range(1, 8))
        if rational and Fraction(L.n[0], L.d) == -1:
            continue
        n += 1
        seen += 1
        for i in (0, 1):
            covered = div(i, r) or div(i, s)
            cnt[(i, covered)] += 1
            if A % 2 == 0 and not covered:
                bad.append((A, i, "a even but pi divides neither r nor s"))
            if A % 4 != 0 and div(i, r) and div(i, s):
                both.append((A, i, "4 does not divide a but pi divides BOTH r and s"))
    if n:
        c1 = cnt[(0, True)], cnt[(0, False)]
        c2 = cnt[(1, True)], cnt[(1, False)]
        print(f"{A:>4} {'even' if A%2==0 else 'odd':>4} {n:>6}  "
              f"pi1 {c1[0]}/{n}, pi2 {c2[0]}/{n}", flush=True)
print()
print(f"cross vectors with lambda != -1 examined: {seen}")
print(f"counterexamples to the contrapositive (a even, neither divisible): {len(bad)}")
for x in bad[:10]:
    print("   ", x)
print(f"counterexamples to the trichotomy (4 does not divide a, both divisible):"
      f" {len(both)}")
for x in both[:10]:
    print("   ", x)
