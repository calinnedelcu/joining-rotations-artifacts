#!/usr/bin/env python3
"""Which integer shells exist in the Moser lattice -- decided exactly.

A spindle rotation theta_a acts only on the lattice points at squared radius a.
If the lattice has none, the rotation has nothing to move and cannot join
anything, however well it passes the arithmetic filter.  Absence from a ball is
not a proof, so this decides it by the form instead.

In the chart  z = (a + b sqrt33)/12 + i(c sqrt3 + d sqrt11)/12,

BUT the chart is a SUPERSET of the Moser lattice: integer (a,b,c,d) describe a
group containing R with index 16.  Reading a chart count as a lattice count
overcounts -- measured, the chart claims 28 points at squared radius 7/4 where
the lattice has none.  R is cut out by congruences, extracted from the lattice
itself and pinned by a test:

    a = b = c = d  (mod 2)      and      a + b + c + d = 2a  (mod 4)

which selects exactly the 16 residue classes mod 4 that occur, of 256.


    |z|^2 = [ (a^2 + 33 b^2 + 3 c^2 + 11 d^2) + 2 (ab + cd) sqrt33 ] / 144,

so |z|^2 = N is a rational integer exactly when

    ab + cd = 0    and    a^2 + 33 b^2 + 3 c^2 + 11 d^2 = 144 N.

The left side is positive definite, so for each N this is a finite search and
the answer is exact.  N = 1 must return the 30 unit vectors.
"""
import sys
from collections import defaultdict
from math import isqrt

def chart_count(N, B=1):
    """Points at squared radius N/B.  Returns 0 immediately if B does not
    divide 144: |z|^2 is always an integer over 144, so no other denominator
    can occur, whatever the numerator."""
    if (144 * N) % B:
        return 0
    T = 144 * N // B
    A = defaultdict(int)                     # (a^2+33b^2, ab) -> count
    amax = isqrt(T)
    bmax = isqrt(T // 33)
    for b in range(-bmax, bmax + 1):
        r = T - 33 * b * b
        if r < 0:
            continue
        am = isqrt(r)
        for a in range(-am, am + 1):
            A[(a * a + 33 * b * b, a * b)] += 1
    tot = 0
    cmax = isqrt(T // 3)
    dmax = isqrt(T // 11)
    for d in range(-dmax, dmax + 1):
        r = T - 11 * d * d
        if r < 0:
            continue
        cm = isqrt(r // 3)
        for c in range(-cm, cm + 1):
            v = 3 * c * c + 11 * d * d
            tot += A.get((T - v, -c * d), 0)
    return tot


def in_lattice(a, b, c, d):
    """Is the chart point (a,b,c,d) actually in the Moser lattice?"""
    return (a % 2 == b % 2 == c % 2 == d % 2) and (a + b + c + d - 2 * a) % 4 == 0


def shell_count(N, B=1):
    """Points of the MOSER LATTICE at squared radius N/B, with the congruences."""
    if (144 * N) % B:
        return 0
    T = 144 * N // B
    out = 0
    bmax = isqrt(T // 33)
    for b in range(-bmax, bmax + 1):
        r = T - 33 * b * b
        if r < 0:
            continue
        am = isqrt(r)
        for a in range(-am, am + 1):
            rem = T - a * a - 33 * b * b
            if rem < 0:
                continue
            P = a * b
            dmax = isqrt(rem // 11)
            for d in range(-dmax, dmax + 1):
                r2 = rem - 11 * d * d
                if r2 < 0 or r2 % 3:
                    continue
                cs = isqrt(r2 // 3)
                if 3 * cs * cs != r2:
                    continue
                for c in ({cs, -cs} if cs else {0}):
                    if P + c * d == 0 and in_lattice(a, b, c, d):
                        out += 1
    return out

def denominator_possible(B):
    """Can any lattice point have |z|^2 with denominator exactly B?"""
    return 144 % B == 0


if __name__ == "__main__":
    hi = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    assert shell_count(1) == 30, f"N=1 must give the 30 unit vectors, got {shell_count(1)}"
    assert shell_count(7, 4) == 0, "the congruences must exclude the quarter shells"
    print("N=1 gives 30 points: the form is right\n")
    occ, emp = [], []
    for N in range(1, hi + 1):
        n = shell_count(N)
        (occ if n else emp).append(N)
        if n:
            print(f"  shell {N:3d}: {n:5d} points")
    print(f"\nOCCUPIED: {occ}")
    print(f"EMPTY:    {emp}")
