"""Filter 2: the cross-edge class census of a join, with no ball anywhere.

A type-M construction is  G = L_part  union  g(S_part),  the two parts sharing
only the origin.  What makes the record CHEAP is not that the union is
5-chromatic but that the split is LOPSIDED: 509 = 374 + 136 - 1.  Parts'
explanation is that the two parts are joined by more than one orbit of cross
edges -- a reference orbit at radius 2 and an auxiliary one -- and the small
part is small because it only has to break one of the pairs the large part
guarantees.  So: count the orbits.

THE POINT OF THIS MODULE is that the census needs no ball.  Route 9 measured
126 cross edges in 5 classes over a 14557-point ball and concluded "nothing
else exists at any radius"; that conclusion was a ball-sized extrapolation of
exactly the kind that has already gone wrong three times here.  It is in fact a
theorem, and this is the proof:

    L and g(L) are both SUBGROUPS of Lambda = L + g(L).  A cross edge is a pair
    (a, b), a in L, b in g(L), |a - b| = 1 -- so a - b is a unit vector of
    Lambda.  Conversely the pairs giving a fixed u are
    {(p + w, g(q) + w) : w in L n g(L)}.  So when the parts share only the
    origin, cross edges correspond ONE TO ONE with the unit vectors of Lambda,
    and there are exactly |U(Lambda)| of them in the whole infinite union.

For theta_4 over the 30-vector lattice |U(Lambda)| = 126, which is route 9's
number, now derived instead of sampled.  The classes are the (|p|, |q|) radius
pairs of the unique decomposition.

WHAT THIS PROVES, AND WHAT IT DOES NOT.  The census is exact.  The inference
"one class ==> no lopsided split" is a HEURISTIC read off the known cases, not
a theorem, and `census` reports the numbers rather than a verdict.  See
docs/ATTEMPTS.md route 49 for what it is measured to get right and wrong.
"""
from __future__ import annotations
from fractions import Fraction
import collections
from .field import K, Pt
from .lattice import Lattice, coeff_vector, _gcd


class Census:
    def __init__(self, lam, L, gL, direct, edges, classes):
        # When `direct` is False the parts share more than the origin, the
        # decomposition u = p - g(q) is not unique, and `edges`/`classes` are
        # EMPTY rather than zero: there is no two-part construction to census.
        # Callers must read `direct` before reading anything else.
        self.lattice = lam
        self.L = L
        self.gL = gL
        self.direct = direct          # do the parts share only the origin?
        self.edges = edges            # list of (u, p, gq, |p|^2, |gq|^2)
        self.classes = classes        # Counter over ordered (|p|^2, |gq|^2)

    @property
    def n_edges(self):
        return len(self.edges)

    @property
    def n_classes(self):
        return len(self.classes)

    @property
    def n_unordered(self):
        c = collections.Counter()
        for (a, b), k in self.classes.items():
            c[tuple(sorted((a, b)))] += k
        return len(c)

    def __repr__(self):
        if not self.direct:
            return "<Census parts overlap: no two-part construction>"
        return (f"<Census edges={self.n_edges} classes={self.n_classes} "
                f"direct=True>")


def _norm2_key(p: Pt):
    q = p.norm2()
    return (q.n, q.d)


def _pretty(key):
    """A readable |p|^2 from its exact key."""
    n, d = key
    from .construct import to_float
    return round(to_float(K(n, d)), 6)


def census(vectors, cs, vectors_small=None):
    """Cross-edge classes of  <vectors>  union  g(<vectors_small or vectors>).

    `cs` is the (cos, sin) pair of the joining rotation, exact in K.  Returns a
    Census.  Cost is one unit-vector enumeration -- milliseconds.
    """
    from .construct import rotate
    WS = vectors if vectors_small is None else vectors_small
    gW = [rotate(p, cs) for p in WS]
    L, gL = Lattice(vectors), Lattice(gW)
    lam = Lattice(list(vectors) + gW)
    direct = lam.rank == L.rank + gL.rank

    rowsL, rowsG, D = _common_rows(L, gL)
    M = rowsL + rowsG
    edges, classes = [], collections.Counter()
    if not direct:
        return Census(lam, L, gL, False, edges, classes)
    for coord, u in lam.unit_vectors():
        n = _solve_rows(M, _scaled(u, D))
        if n is None:                       # not a direct sum: skip decomposition
            continue
        p = _from_rows(rowsL, n[:L.rank], D)
        negq = _from_rows(rowsG, n[L.rank:], D)
        gq = Pt(K.zero(), K.zero()) - negq
        assert (p - gq).norm2().is_one(), "decomposition is not the unit vector"
        ka, kb = _norm2_key(p), _norm2_key(gq)
        edges.append((u, p, gq, ka, kb))
        classes[(ka, kb)] += 1
    return Census(lam, L, gL, direct, edges, classes)


# ---- exact linear algebra over the two sublattices -------------------------
def _common_rows(L, gL):
    D = L.scale * gL.scale // _gcd(L.scale, gL.scale)
    a, b = D // L.scale, D // gL.scale
    return ([[x * a for x in r] for r in L.echelon],
            [[x * b for x in r] for r in gL.echelon], D)


def _scaled(p: Pt, D):
    v = coeff_vector(p)
    out = []
    for c in v:
        t = c * D
        assert t.denominator == 1, "point does not scale to integers"
        out.append(int(t))
    return out


def _from_rows(rows, n, D):
    acc = [0] * 16
    for c, row in zip(n, rows):
        if c:
            for k in range(16):
                acc[k] += c * row[k]
    return Pt(K(tuple(acc[:8]), D), K(tuple(acc[8:]), D))


def _solve_rows(M, target):
    """The unique rational n with n . M == target, or None if there is none.

    M's rows are independent exactly when the two parts share only the origin;
    when they are not, the decomposition is not unique and this returns None
    rather than an arbitrary one.
    """
    r = len(M)
    if r == 0:
        return None
    A = [[Fraction(x) for x in row] + [Fraction(0)] * r for row in M]
    for i in range(r):
        A[i][16 + i] = Fraction(1)
    piv = []
    row = 0
    for col in range(16):
        sel = next((i for i in range(row, r) if A[i][col]), None)
        if sel is None:
            continue
        A[row], A[sel] = A[sel], A[row]
        inv = A[row][col]
        A[row] = [x / inv for x in A[row]]
        for i in range(r):
            if i != row and A[i][col]:
                f = A[i][col]
                A[i] = [x - f * y for x, y in zip(A[i], A[row])]
        piv.append(col)
        row += 1
        if row == r:
            break
    if row < r:
        return None                      # rows dependent: not a direct sum
    t = [Fraction(x) for x in target]
    n = [Fraction(0)] * r
    for i, col in enumerate(piv):
        n[i] = t[col]
    # n is expressed against the reduced rows; map back through the transform
    coef = [sum(n[i] * A[i][16 + j] for i in range(r)) for j in range(r)]
    chk = [sum(coef[j] * M[j][k] for j in range(r)) for k in range(16)]
    if chk != [Fraction(x) for x in target]:
        return None
    if any(c.denominator != 1 for c in coef):
        return None
    return [int(c) for c in coef]
