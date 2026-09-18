"""Rational squared radii of the Moser lattice, and the spindle each unlocks.

Route 44 enumerated INTEGER radius^2 only.  A spindle rotation exists for any
shell radius d with cos = 1 - 1/(2 d^2) rational, i.e. for any RATIONAL d^2.
"""
import os, sys, collections
from fractions import Fraction
from math import isqrt
sys.path.insert(0, "/Users/calinnedelcu/Documents/universitate/hadwiger-nelson")
from hn.field import K
from hn.construct import unit_vector_family, ball, norm

def squarefree_part(n):
    s, d = 1, 2
    while d * d <= n:
        e = 0
        while n % d == 0:
            n //= d; e += 1
        if e % 2: s *= d
        d += 1
    return s * n

def rational(k):
    return all(x == 0 for x in k.n[1:])

W = unit_vector_family(2)
for depth, radius in ((4, 5.0),):
    P = ball(W, depth, radius)
    print(f"ball depth {depth} radius {radius}: {len(P)} points", flush=True)
    shells = collections.Counter()
    for p in P:
        q = p.norm2()
        if rational(q):
            shells[Fraction(q.n[0], q.d)] += 1
    print(f"{len(shells)} distinct RATIONAL squared radii\n")
    print(f"{'d^2':>10} {'d':>9} {'shell':>6}  {'cos a':>12}  needs sqrt      m (3rd gen)")
    for d2 in sorted(shells):
        if d2 == 0: continue
        a, b = d2.numerator, d2.denominator
        # cos = (2a-b)/(2a);  sin = sqrt(b(4a-b))/(2a)
        rad = b * (4 * a - b)
        s = squarefree_part(rad)
        m = s
        for pr in (3, 11):
            if m % pr == 0: m //= pr
        integer = "int" if b == 1 else ""
        print(f"{str(d2):>10} {float(d2)**.5:9.4f} {shells[d2]:6d}  "
              f"{2*a-b}/{2*a:<10}  sqrt({rad})={s}*sq   m={m:<8} {integer}")
