"""Exact arithmetic in the multiquadratic field K = Q(sqrt3, sqrt5, sqrt11).

Every Hadwiger-Nelson record graph published to date has coordinates in K.
An element is a rational combination of the 8 basis elements

    index (bitmask over [3,5,11]) -> basis element
      0 -> 1        1 -> sqrt3     2 -> sqrt5     3 -> sqrt15
      4 -> sqrt11   5 -> sqrt33    6 -> sqrt55    7 -> sqrt165

Multiplication is an XOR-indexed convolution:
    sqrt(prod S) * sqrt(prod T) = prod(S & T) * sqrt(prod(S ^ T))

We store 8 integer numerators over one shared positive denominator, kept in
lowest terms.  In the published graphs the numerators fit in 9 bits, so this
is exact, branch-free and hashable -- no CAS, no floating point, ever.
"""
from __future__ import annotations
from math import gcd
from functools import reduce

PRIMES = (3, 5, 11)


def squarefree_divisors(primes=None):
    """The 8 squarefree products of the field's generators, smallest first.

    This follows PRIMES.  Hardcoding it to the classical field made K.sqrt
    silently answer None for sqrt2 in Q(sqrt2, sqrt3), which is the same failure
    mode as a stale float basis: the parser then rejects a perfectly valid
    coordinate file, and Parts' 721-vertex type T graph could not be read at all.
    """
    out = [1]
    for q in (primes if primes is not None else PRIMES):
        out += [d * q for d in out]
    return sorted(out)


def _coef_table(primes):
    return tuple(
        tuple(reduce(lambda a, k: a * (primes[k] if (i & j) >> k & 1 else 1), range(3), 1)
              for j in range(8))
        for i in range(8)
    )


# coef[i][j] = integer factor produced by multiplying basis i with basis j
_COEF = _coef_table(PRIMES)


def set_primes(primes):
    """Work in Q(sqrt p, sqrt q, sqrt r) for a different triple.

    Every published construction lives in Q(sqrt3, sqrt5, sqrt11) because that
    is the field de Grey's graph happened to need, and everyone inherited it.
    Nothing about the problem prefers it.  The representation here is generic:
    three squarefree generators, eight basis elements, multiplication an
    XOR-indexed convolution.  Only this table depends on which three.

    Call once, before building anything.  K values made under one triple are
    meaningless under another, so do not mix them in one process.
    """
    global PRIMES, _COEF
    assert len(primes) == 3 and len(set(primes)) == 3
    PRIMES = tuple(primes)
    _COEF = _coef_table(PRIMES)


class K:
    """An element of Q(sqrt3, sqrt5, sqrt11)."""
    __slots__ = ("n", "d")

    def __init__(self, num, den=1):
        n = tuple(num)
        assert len(n) == 8 and den != 0
        if den < 0:
            n, den = tuple(-x for x in n), -den
        g = reduce(gcd, n, den)
        if g > 1:
            n, den = tuple(x // g for x in n), den // g
        self.n, self.d = n, den

    # ---- constructors -------------------------------------------------
    @staticmethod
    def zero():
        return K((0,) * 8)

    @staticmethod
    def rat(p, q=1):
        return K((p, 0, 0, 0, 0, 0, 0, 0), q)

    @staticmethod
    def root(m):
        """sqrt(m) for m a product of distinct primes from (3,5,11)."""
        i = sum(1 << k for k, p in enumerate(PRIMES) if m % p == 0)
        assert reduce(lambda a, k: a * (PRIMES[k] if i >> k & 1 else 1), range(3), 1) == m
        return K(tuple(1 if j == i else 0 for j in range(8)))

    # ---- ring ---------------------------------------------------------
    def __add__(self, o):
        return K(tuple(a * o.d + b * self.d for a, b in zip(self.n, o.n)), self.d * o.d)

    def __sub__(self, o):
        return K(tuple(a * o.d - b * self.d for a, b in zip(self.n, o.n)), self.d * o.d)

    def __neg__(self):
        return K(tuple(-a for a in self.n), self.d)

    def __mul__(self, o):
        r = [0] * 8
        for i, a in enumerate(self.n):
            if a:
                ci = _COEF[i]                     # module global: see set_primes
                for j, b in enumerate(o.n):
                    if b:
                        r[i ^ j] += a * b * ci[j]
        return K(r, self.d * o.d)

    def conj(self, mask):
        """Galois automorphism: flip the sign of sqrt(p) for each bit in mask.

        Every one of the 8 maps preserves unit-distance-ness, because the
        condition |p-q|^2 == 1 has a rational right-hand side, which Galois
        fixes.  Seven of them carry a graph to a *different*, congruent copy.
        """
        return K(tuple(-a if bin(i & mask).count("1") & 1 else a
                       for i, a in enumerate(self.n)), self.d)

    def inv(self):
        """Multiplicative inverse, via the Galois norm.

        Multiplying by the seven non-trivial conjugates clears every radical,
        because the product over the whole Galois group is rational.
        """
        assert not self.is_zero(), "division by zero"
        num, den = K.rat(1), self
        for k in range(3):
            c = den.conj(1 << k)
            num, den = num * c, den * c
        assert den.n[1:] == (0,) * 7, "norm did not become rational"
        return K(tuple(x * den.d for x in num.n), num.d * den.n[0])

    def __truediv__(self, o):
        return self * o.inv()

    # ---- square roots ---------------------------------------------------
    def sqrt(self):
        """A square root of self inside K, or None if there is none.

        Recursive denesting.  A rational is a square in K iff it is a
        rational square times a squarefree divisor of 3*5*11.  Otherwise
        split self = a + sqrt(p)*b over the subfield without sqrt(p) and use
        sqrt(a + sqrt(p) b) = sqrt((a+t)/2) +- sqrt((a-t)/2), t = sqrt(a^2 - p b^2),
        checking the candidate exactly.  Needed because Heule's and Parts'
        .vtx files contain radicands such as (5*(7 - Sqrt[33]))/2, which
        denests to (sqrt55 - sqrt15)/2.
        """
        from math import isqrt
        if self.is_zero():
            return K.zero()
        if not any(self.n[1:]):
            p, q = self.n[0], self.d
            if p < 0:
                return None
            N = p * q                          # sqrt(p/q) = sqrt(p*q) / q
            for m in squarefree_divisors():
                if N % m == 0:
                    r = isqrt(N // m)
                    if r * r == N // m:
                        return K.root(m) * K.rat(r, q)
            return None
        for k in range(3):
            bit = 1 << k
            if not any(a for i, a in enumerate(self.n) if i & bit):
                continue
            a = K(tuple(x if not (i & bit) else 0 for i, x in enumerate(self.n)), self.d)
            b = K(tuple(self.n[i | bit] if not (i & bit) else 0 for i in range(8)), self.d)
            D = a * a - K.rat(PRIMES[k]) * b * b
            t = D.sqrt()
            if t is None:
                continue
            half = K.rat(1, 2)
            u = ((a + t) * half).sqrt()
            w = ((a - t) * half).sqrt()
            if u is None or w is None:
                continue
            for s in (u + w, u - w):
                if s * s == self:
                    return s
        return None

    # ---- predicates ---------------------------------------------------
    def is_zero(self):
        return not any(self.n)

    def is_one(self):
        return self.n == (self.d, 0, 0, 0, 0, 0, 0, 0)

    def __eq__(self, o):
        return self.n == o.n and self.d == o.d

    def __hash__(self):
        return hash((self.n, self.d))

    def __repr__(self):
        return f"K({self.n},{self.d})"


class Pt:
    """A point of the plane with both coordinates in K."""
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, o):
        return Pt(self.x + o.x, self.y + o.y)

    def __sub__(self, o):
        return Pt(self.x - o.x, self.y - o.y)

    def norm2(self):
        return self.x * self.x + self.y * self.y

    def conj(self, mask):
        return Pt(self.x.conj(mask), self.y.conj(mask))

    def key(self):
        return (self.x.n, self.x.d, self.y.n, self.y.d)

    def __eq__(self, o):
        return self.key() == o.key()

    def __hash__(self):
        return hash(self.key())

    def __repr__(self):
        return f"Pt({self.x},{self.y})"


def is_unit(p, q):
    """Exact test: is |p - q| == 1?"""
    return (p - q).norm2().is_one()
