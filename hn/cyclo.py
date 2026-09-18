"""Exact arithmetic in a cyclotomic field, for lattices no quadratic field has.

Every 5-chromatic unit-distance graph before 2026 lives in a multiquadratic
field, and hn/field.py is built for exactly that.  The cost is invisible until
you look for it: the 42 directions at multiples of pi/21, the heptagonal
lattice of Haugland's 2026 Moser-spindle-free construction, are not in any
Q(sqrt a, sqrt b, sqrt c), so nothing in this repository could even write them
down.

Here a point is a single complex number in Q(zeta_n) rather than a pair of
coordinates, which makes rotation by a lattice direction exactly multiplication
by zeta, and the unit-distance test exactly

    (p - q) * conj(p - q) == 1.

What this buys, concretely.  A joining rotation has to be a spindle rotation
theta_i, cos = (2i-1)/(2i) and sin = sqrt(4i-1)/(2i), and sqrt(4i-1) has to
live in the field (docs/ATTEMPTS.md, the three conditions).  For n = 42 the
quadratic subfields give sqrt(-7) as the Gauss sum

    g = sum over quadratic residues of zeta_7^k  -  sum over non-residues,
    g^2 = -7,

and since sin theta_2 = sqrt7/4, the rotation by arccos(3/4) is multiplication
by the algebraic integer (3 + g)/4, of modulus (9 - g^2)/16 = 1.

theta_2 has never been available to anybody working on this problem: it needs
sqrt7 next to a lattice, and the classical field has sqrt3, sqrt5, sqrt11.
Elements are integer vectors over the power basis of Phi_n, so the
representation is canonical and equality is a tuple comparison.
"""
from __future__ import annotations
import cmath
import math
from math import gcd

N = 0
DEG = 0
PHI = ()
_RED = ()
_ZETA = ()
_EMB = ()


def _poly_divmod(a, b):
    """Integer polynomial division, low-order first; b monic."""
    a = list(a)
    q = [0] * max(1, len(a) - len(b) + 1)
    for i in range(len(a) - len(b), -1, -1):
        c = a[i + len(b) - 1]
        if not c:
            continue
        q[i] = c
        for j, bj in enumerate(b):
            a[i + j] -= c * bj
    while len(a) > 1 and not a[-1]:
        a.pop()
    return q, a


def _poly_mul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                out[i + j] += ai * bj
    return out


def cyclotomic(n):
    """Phi_n, low-order first, by dividing x^n - 1 by the proper divisors."""
    num = [-1] + [0] * (n - 1) + [1]
    den = [1]
    for d in range(1, n):
        if n % d == 0:
            den = _poly_mul(den, cyclotomic(d))
    q, r = _poly_divmod(num, den)
    assert all(c == 0 for c in r), "x^n - 1 is not divisible by the lower Phi_d"
    return q


def set_conductor(n):
    """Work in Q(zeta_n).  Rebuilds the reduction and embedding tables."""
    global N, DEG, PHI, _RED, _ZETA, _EMB
    N = n
    PHI = tuple(cyclotomic(n))
    DEG = len(PHI) - 1
    assert PHI[-1] == 1
    # x^j mod Phi_n for every j that a product of two elements can reach
    red = [[0] * DEG for _ in range(2 * DEG)]
    for j in range(DEG):
        red[j][j] = 1
    for j in range(DEG, 2 * DEG):
        prev = red[j - 1]
        cur = [0] + prev[:-1]
        top = prev[-1]
        if top:
            for i in range(DEG):
                cur[i] -= top * PHI[i]
        red[j] = cur
    _RED = tuple(tuple(r) for r in red)
    # zeta^k for every k, by the same reduction
    z = [[0] * DEG for _ in range(n)]
    for k in range(n):
        if k < DEG:
            z[k][k] = 1
        else:
            prev = z[k - 1]
            cur = [0] + prev[:-1]
            top = prev[-1]
            if top:
                for i in range(DEG):
                    cur[i] -= top * PHI[i]
            z[k] = cur
    _ZETA = tuple(tuple(r) for r in z)
    _EMB = tuple(cmath.exp(2j * cmath.pi * k / n) for k in range(DEG))
    return DEG


class Cyc:
    """sum(num[i] * zeta^i) / den, canonical: gcd(num, den) = 1, den > 0."""
    __slots__ = ("n", "d")

    def __init__(self, num, den=1):
        if den < 0:
            num, den = [-c for c in num], -den
        g = den
        for c in num:
            g = gcd(g, c if c >= 0 else -c)
        if g > 1:
            num = [c // g for c in num]
            den //= g
        self.n = tuple(num)
        self.d = den

    @staticmethod
    def rat(p, q=1):
        return Cyc([p] + [0] * (DEG - 1), q)

    @staticmethod
    def zero():
        return Cyc([0] * DEG, 1)

    @staticmethod
    def zeta(k):
        return Cyc(list(_ZETA[k % N]), 1)

    def __add__(self, o):
        d = self.d * o.d
        return Cyc([a * o.d + b * self.d for a, b in zip(self.n, o.n)], d)

    def __sub__(self, o):
        d = self.d * o.d
        return Cyc([a * o.d - b * self.d for a, b in zip(self.n, o.n)], d)

    def __neg__(self):
        return Cyc([-a for a in self.n], self.d)

    def __mul__(self, o):
        a, b = self.n, o.n
        raw = [0] * (2 * DEG - 1)
        for i, ai in enumerate(a):
            if ai:
                for j, bj in enumerate(b):
                    raw[i + j] += ai * bj
        out = list(raw[:DEG])
        for j in range(DEG, 2 * DEG - 1):
            c = raw[j]
            if c:
                r = _RED[j]
                for i in range(DEG):
                    out[i] += c * r[i]
        return Cyc(out, self.d * o.d)

    def conj(self):
        """Complex conjugation: zeta -> zeta^-1."""
        out = [0] * DEG
        for i, a in enumerate(self.n):
            if a:
                r = _ZETA[(N - i) % N]
                for j in range(DEG):
                    out[j] += a * r[j]
        return Cyc(out, self.d)

    def inv(self):
        """1/self, by solving the linear system x * y = 1 over the power basis.

        Needed because Haugland's generators are unit vectors obtained by dividing
        by 4 sin(2 pi/7), and a ring with no division cannot write them down.  The
        multiplication-by-self matrix is DEG x DEG over Q; Gaussian elimination on
        Fractions is exact and costs one solve.
        """
        from fractions import Fraction
        n = DEG
        cols = []
        for k in range(n):                       # self * zeta^k, as a column
            e = [0] * n
            e[k] = 1
            cols.append((self * Cyc(e, 1)).n)
        M = [[Fraction(cols[k][r], 1) for k in range(n)] + [Fraction(1 if r == 0 else 0)]
             for r in range(n)]
        for c in range(n):                       # forward elimination
            piv = next((r for r in range(c, n) if M[r][c]), None)
            if piv is None:
                raise ZeroDivisionError("not invertible")
            M[c], M[piv] = M[piv], M[c]
            pv = M[c][c]
            M[c] = [v / pv for v in M[c]]
            for r in range(n):
                if r != c and M[r][c]:
                    f = M[r][c]
                    M[r] = [a - f * b for a, b in zip(M[r], M[c])]
        num = [M[r][n] for r in range(n)]
        den = 1
        for f in num:
            den = den * f.denominator // math.gcd(den, f.denominator)
        out = [int(f * den) for f in num]
        return Cyc(out, self.d * den) if self.d != 1 else Cyc(out, den)

    def __truediv__(self, o):
        return self * o.inv()

    def is_one(self):
        return self.d == 1 and self.n[0] == 1 and not any(self.n[1:])

    def is_zero(self):
        return not any(self.n)

    def __eq__(self, o):
        return self.d == o.d and self.n == o.n

    def __hash__(self):
        return hash((self.n, self.d))

    def key(self):
        return (self.n, self.d)

    def complex(self):
        z = sum(a * e for a, e in zip(self.n, _EMB))
        return z / self.d

    def __repr__(self):
        return f"Cyc({self.complex():.6f})"


def gauss_sum(p):
    """The quadratic Gauss sum over zeta_p: squares to p or -p as p is 1 or 3 mod 4."""
    assert N % p == 0, f"zeta_{p} is not in Q(zeta_{N})"
    step = N // p
    res = {(k * k) % p for k in range(1, p)}
    g = Cyc.zero()
    for k in range(1, p):
        z = Cyc.zeta(step * k)
        g = g + z if k % p in res else g - z
    return g


def spindle(i, g=None):
    """Multiplication by exp(i*theta_i), theta_i = arccos((2i-1)/(2i)), or None.

    sin theta_i = sqrt(4i-1)/(2i), so the rotation is (2i-1 + sqrt(-(4i-1)) *
    ...)/(2i) -- and in a cyclotomic field the imaginary unit is already inside
    the Gauss sum, which is why this is a single ring element with no separate
    sqrt(-1): for i = 2, (3 + g_7)/4 with g_7^2 = -7.
    """
    m = 4 * i - 1
    for p in (m, m // 9 if m % 9 == 0 else 0, m // 25 if m % 25 == 0 else 0,
              m // 49 if m % 49 == 0 else 0):
        if p <= 1 or p % 4 != 3 or N % p:
            continue
        r = 1
        while r * r * p < m:
            r += 1
        if r * r * p != m:
            continue
        u = (Cyc.rat(2 * i - 1) + gauss_sum(p) * Cyc.rat(r)) * Cyc.rat(1, 2 * i)
        if (u * u.conj()).is_one():
            return u
    return None


def is_unit(p, q):
    d = p - q
    return (d * d.conj()).is_one()


def dedup(points):
    seen, out = set(), []
    for p in points:
        k = p.key()
        if k not in seen:
            seen.add(k)
            out.append(p)
    return out


def ball(gens, depth, radius):
    """Sums of at most `depth` generators with |p| <= radius."""
    r2 = radius * radius + 1e-9
    S = {Cyc.zero().key(): Cyc.zero()}
    G = list(gens)
    for _ in range(depth):
        new = dict(S)
        for p in S.values():
            for g in G:
                q = p + g
                if abs(q.complex()) ** 2 <= r2:
                    new.setdefault(q.key(), q)
        S = new
    return list(S.values())


def edges(points, tol=1e-9):
    """Unit-distance pairs, float prefilter then the exact ring test."""
    import numpy as np
    n = len(points)
    if n < 2:
        return []
    Z = np.array([p.complex() for p in points])
    X = np.stack([Z.real, Z.imag], axis=1)
    out = []
    B = 2048
    for i0 in range(0, n, B):
        xi = X[i0:i0 + B]
        d2 = ((xi[:, None, :] - X[None, :, :]) ** 2).sum(-1)
        ii, jj = np.nonzero(np.abs(d2 - 1.0) < tol)
        for a, b in zip(ii.tolist(), jj.tolist()):
            i, j = a + i0, b
            if i < j and is_unit(points[i], points[j]):
                out.append((i, j))
    out.sort()
    return out


set_conductor(42)
