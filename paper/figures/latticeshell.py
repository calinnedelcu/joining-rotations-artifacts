"""Exact shell points of the Moser lattice, straight from the chart.

    z = (A + B*sqrt33)/12 + i(C*sqrt3 + D*sqrt11)/12,

with R cut out of the integer chart by  A = B = C = D (mod 2)  and
A + B + C + D = 2A (mod 4).  Then |z|^2 is rational exactly when AB + CD = 0,
and equals (A^2 + 33B^2 + 3C^2 + 11D^2)/144.  No ball is built and no floating
point enters the selection: this is the same reduction scripts/shells.py counts
with, returning the points rather than the count.
"""
from math import isqrt, sqrt

S33, S3, S11 = sqrt(33), sqrt(3), sqrt(11)


def shell(num, den=1):
    """Every lattice point at squared radius num/den, as exact (A,B,C,D)."""
    if (144 * num) % den:
        return []
    T = 144 * num // den
    out = []
    for B in range(-isqrt(T // 33), isqrt(T // 33) + 1):
        r1 = T - 33 * B * B
        if r1 < 0:
            continue
        for A in range(-isqrt(r1), isqrt(r1) + 1):
            r2 = r1 - A * A
            if r2 < 0:
                continue
            for D in range(-isqrt(r2 // 11), isqrt(r2 // 11) + 1):
                r3 = r2 - 11 * D * D
                if r3 < 0 or r3 % 3:
                    continue
                c2 = r3 // 3
                c = isqrt(c2)
                if c * c != c2:
                    continue
                for C in ({c, -c} if c else {0}):
                    if A * B + C * D:
                        continue
                    if not (A % 2 == B % 2 == C % 2 == D % 2):
                        continue
                    if (A + B + C + D - 2 * A) % 4:
                        continue
                    out.append((A, B, C, D))
    return out


def to_xy(t):
    A, B, C, D = t
    return ((A + B * S33) / 12, (C * S3 + D * S11) / 12)


if __name__ == "__main__":
    for n, d in ((1, 1), (3, 1), (4, 1), (16, 1), (28, 1), (36, 1),
                 (64, 3), (64, 9), (256, 9)):
        s = shell(n, d)
        r = sqrt(n / d)
        bad = [t for t in s if abs(sqrt(sum(x*x for x in to_xy(t))) - r) > 1e-9]
        print(f"  |z|^2 = {n}/{d}: {len(s):4d} points   radius {r:.4f}"
              f"   {'BAD ' + str(len(bad)) if bad else 'all exact'}")
