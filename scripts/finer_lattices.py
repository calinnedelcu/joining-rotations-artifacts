#!/usr/bin/env python3
"""Section 10's nested family: 30 < 42 < 54 < ..., index 9^(J-2), units 6(2J+1).

Taking |j| <= J instead of |j| <= 2 in the generating family gives, for each J, a
rank-4 lattice.  Section 10 claims three things about them and none had a check:
the generators number 6(2J+1), the lattices nest with index 9^(J-2) over the
30-vector one, and each has exactly its own generators as unit vectors -- which is
what stops the law being claimed for the finer members without recomputation.

Denominators grow: omega^3 = (sqrt33 + 4 i sqrt3)/9, so J = 3 already needs 36
where J = 2 needs 12.  The index computation uses one common denominator for all
of them; the unit-vector counts use the smallest that works for each.
"""
from fractions import Fraction as F
from math import isqrt

def mul(x, y):                       # basis 1, sqrt33, i sqrt3, i sqrt11
    a1, a2, a3, a4 = x; b1, b2, b3, b4 = y
    return (a1*b1 + 33*a2*b2 - 3*a3*b3 - 11*a4*b4,
            a1*b2 + a2*b1 - (a3*b4 + a4*b3),
            a1*b3 + a3*b1 + 11*(a2*b4 + a4*b2),
            a1*b4 + a4*b1 + 3*(a2*b3 + a3*b2))

ONE = (F(1), F(0), F(0), F(0))
ZETA = (F(1, 2), F(0), F(1, 2), F(0))          # exp(i 60 deg)
OM = (F(0), F(1, 6), F(1, 6), F(0))            # exp(i theta_3 / 2)

def powr(x, n):
    r = ONE
    for _ in range(abs(n)): r = mul(r, x)
    return r if n >= 0 else (r[0], r[1], -r[2], -r[3])

def gens(J, den):
    out = []
    for k in range(6):
        for j in range(-J, J + 1):
            v = tuple(den * c for c in mul(powr(ZETA, k), powr(OM, j)))
            assert all(x.denominator == 1 for x in v), f"denominator {den} too small at J={J}"
            out.append(tuple(int(x) for x in v))
    return out

def hnf(rows):
    rows = [list(r) for r in rows]; piv = 0
    for c in range(4):
        r = next((i for i in range(piv, len(rows)) if rows[i][c]), None)
        if r is None: continue
        rows[piv], rows[r] = rows[r], rows[piv]
        for i in range(piv + 1, len(rows)):
            while rows[i][c]:
                q = rows[piv][c] // rows[i][c]
                rows[piv] = [a - q*b for a, b in zip(rows[piv], rows[i])]
                rows[piv], rows[i] = rows[i], rows[piv]
        if rows[piv][c] < 0: rows[piv] = [-a for a in rows[piv]]
        piv += 1
    B = rows[:piv]
    for i in range(piv - 1, -1, -1):
        c = next(j for j in range(4) if B[i][j])
        for k in range(i):
            q = B[k][c] // B[i][c]
            B[k] = [a - q*b for a, b in zip(B[k], B[i])]
    return B

COMMON = 12 * 9**4
base = 1
for row in hnf(gens(2, COMMON)): base *= row[next(j for j in range(4) if row[j])]
print(f"{'J':>2} {'generators':>11} {'6(2J+1)':>8} {'index over the 30-vector lattice':>32} {'9^(J-2)':>9}")
for J in (2, 3, 4, 5):
    d = 1
    for row in hnf(gens(J, COMMON)): d *= row[next(j for j in range(4) if row[j])]
    idx = F(base, d)
    print(f"{J:>2} {len(gens(J, COMMON)):>11} {6*(2*J+1):>8} {str(idx):>32} {9**(J-2):>9}")
    assert len(gens(J, COMMON)) == 6*(2*J+1) and idx == 9**(J-2)

print()
for J, den in ((2, 12), (3, 36)):
    B = hnf(gens(J, den))
    def inL(v):
        x = list(v)
        for row in B:
            c = next(j for j in range(4) if row[j])
            if x[c] % row[c]: return False
            q = x[c] // row[c]; x = [a - q*b for a, b in zip(x, row)]
        return all(a == 0 for a in x)
    S0 = den * den; units = set()
    for A in range(-isqrt(S0), isqrt(S0) + 1):
        for Bb in range(-isqrt(S0 // 33) - 1, isqrt(S0 // 33) + 2):
            t = S0 - A*A - 33*Bb*Bb
            if t < 0: continue
            for C in range(-isqrt(t // 3) - 1, isqrt(t // 3) + 2):
                t2 = t - 3*C*C
                if t2 < 0 or t2 % 11: continue
                q = t2 // 11; D0 = isqrt(q)
                if D0*D0 != q: continue
                for D in {D0, -D0}:
                    if A*Bb + C*D == 0 and inL((A, Bb, C, D)): units.add((A, Bb, C, D))
    print(f"J = {J}: {len(units)} unit vectors, against {6*(2*J+1)} generators")
    assert len(units) == 6*(2*J+1)
print("\nall three claims hold where they were checked")
