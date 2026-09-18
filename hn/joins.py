"""Joining maps as data, so a filter can be handed a candidate instead of a ball.

A joining rotation for this lattice is pinned by one rational number: the
squared radius d^2 = a/b of the shell it spins.  Then

    cos = (2a - b) / (2a),      sin = sqrt(b(4a - b)) / (2a)

and the rotation exists in Q(sqrt3, sqrt11, sqrt m) exactly when the squarefree
part of b(4a - b), divided by whatever it shares with 3 and 11, is m.  Integer
d^2 gives the classical spindles theta_i (a = i, b = 1, cos = (2i-1)/(2i)); the
generalisation to rational d^2 is route 48's correction, and route 44's
integer-only sweep is what it corrects.

The lattice itself only ever needs sqrt33, so the third generator is free --
that was route 41's mistake, inheriting m = 5 from theta_4 and concluding a
rotation did not exist when only the field had been chosen wrongly.  Here the
field is part of the candidate, never a default.
"""
from __future__ import annotations
from fractions import Fraction
from math import isqrt


def squarefree_part(n):
    s, d = 1, 2
    while d * d <= n:
        e = 0
        while n % d == 0:
            n //= d
            e += 1
        if e % 2:
            s *= d
        d += 1
    return s * n


class Join:
    """A candidate joining rotation: a field and an exact (cos, sin).

    `sin = coeff * sqrt(radicand) / den`, with radicand squarefree.
    """

    def __init__(self, name, primes, cos_num, cos_den, radicand, coeff, den,
                 jmax_L=2, jmax_S=2, note=""):
        self.name = name
        self.primes = tuple(primes)
        self.cos = Fraction(cos_num, cos_den)
        self.radicand, self.coeff, self.den = radicand, coeff, den
        self.jmax_L, self.jmax_S = jmax_L, jmax_S
        self.note = note

    def __repr__(self):
        return f"<Join {self.name} Q{self.primes}>"

    def field_str(self):
        return "Q(" + ",".join(f"v{p}" for p in self.primes) + ")"

    def build(self):
        """Switch the process into this candidate's field and return (W_L, W_S, cs).

        Always rebuilds: K values made under one prime triple are meaningless
        under another, so nothing may be carried across a call to this.
        """
        from .field import set_primes, K
        from . import construct as C
        set_primes(self.primes)
        C.refresh_field()
        try:
            s = (K.root(self.radicand) if self.radicand > 1 else K.rat(1)) \
                * K.rat(self.coeff, self.den)
        except AssertionError:
            return None                       # sqrt(radicand) not in this field
        c = K.rat(self.cos.numerator, self.cos.denominator)
        if not (c * c + s * s).is_one():
            return None                       # not a rotation here
        WL = C.unit_vector_family(self.jmax_L)
        WS = C.unit_vector_family(self.jmax_S) if self.jmax_S != self.jmax_L else WL
        return WL, WS, (c, s)


def spindle(i, **kw):
    """theta_i: cos = (2i-1)/(2i), sin = sqrt(4i-1)/(2i)."""
    return rational_spindle(i, 1, **kw)


def rational_spindle(a, b, name=None, primes=None, **kw):
    """The rotation spinning the shell at squared radius a/b, in its own field."""
    rad = b * (4 * a - b)
    s = squarefree_part(rad)
    t = isqrt(rad // s)
    assert s * t * t == rad
    m = s
    for pr in (3, 11):
        if m % pr == 0:
            m //= pr
    if m <= 1:
        m = 5                                  # sqrt already in Q(sqrt3,sqrt11)
    if primes is None:
        primes = (3, 11, m)
    if name is None:
        name = f"theta_{a}" if b == 1 else f"alpha_{a}/{b}"
    return Join(name, primes, 2 * a - b, 2 * a, s, t, 2 * a, **kw)


# ---- the cases whose answers are already known ----------------------------
# Every filter in this repository is validated against these before it is used
# on anything.  The verdicts come from docs/ATTEMPTS.md as cited.
GROUND_TRUTH = [
    (rational_spindle(4, 1, primes=(3, 5, 11), name="theta_4"),
     "5-chromatic", "the record's own rotation, 509 = 374+136-1 (routes 1-5)"),
    (rational_spindle(3, 1, primes=(3, 5, 11), name="theta_3"),
     "4-colourable", "generates the lattice; 553 joins by theta_4, not this (route 5)"),
    (rational_spindle(16, 1, primes=(3, 7, 11), name="theta_16"),
     "5-chromatic", "route 44, union 29113"),
    (Join("alpha_8/3", (3, 11, 247), 119, 128, 247, 3, 128),
     "5-chromatic", "route 48, 733 = 2*367-1 from Parts' mono-pair gadget"),
    (rational_spindle(7, 1, primes=(3, 5, 11), name="theta_7"),
     "4-colourable", "route 44, union 18439/28843"),
    (rational_spindle(19, 1, primes=(3, 5, 11), name="theta_19"),
     "4-colourable", "route 44, union 79837"),
    (rational_spindle(25, 1, primes=(3, 5, 11), name="theta_25"),
     "4-colourable", "route 44, union 79891"),
    (rational_spindle(28, 1, primes=(3, 11, 37), name="theta_28"),
     "5-chromatic", "route 52, union 156577, depth 6; richest interface known"),
    (rational_spindle(9, 1, name="theta_9"),
     "4-colourable", "route 44 row m=35, union 29113; filter 2's other >=2-class rotation"),
]
