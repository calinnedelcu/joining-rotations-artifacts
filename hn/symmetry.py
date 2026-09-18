"""Symmetry of a point set: the group that actually matters.

Two warnings, both learned the hard way.

1. The COMBINATORIAL automorphism group of the graph is not the group Parts
   works with, and using it silently destroys the method.  On induced
   subgraphs of a unit-distance graph it explodes to astronomical order --
   spurious permutations of low-degree vertices with no geometric meaning --
   while the geometric group stays trivial.  Measured on the 510-vertex
   record graph: |Aut_combinatorial| = 1.  Never source orbits from nauty
   or igraph; use them only as a final cross-check.

2. Symmetry lives in the search POOL, not in the answer.  The record graph
   is asymmetric.  You impose symmetry on the pool; you do not detect it in
   the result.  Detecting symmetry breaks it (gain about |G|); imposing it
   restricts the search to symmetric solutions (gain about 2^(n - n/|G|)).
"""
from __future__ import annotations
from .field import K, Pt

_HALF = K.rat(1, 2)
_R3_2 = K.root(3) * K.rat(1, 2)


def rot60(p):
    """Rotation by 60 degrees about the origin."""
    return Pt(p.x * _HALF - p.y * _R3_2, p.x * _R3_2 + p.y * _HALF)


def reflect_x(p):
    return Pt(p.x, -p.y)


def galois(p, mask):
    """One of the 8 Galois maps of Q(sqrt3, sqrt5, sqrt11).

    Every one preserves unit-distance-ness exactly, because the condition
    |p-q|^2 == 1 has a rational right-hand side and Galois fixes rationals.
    Verified on the 510-vertex record graph: all 8 give zero non-unit edges.
    Seven carry the point set somewhere else, so a graph comes with seven
    free congruent copies -- and an 8-fold enlargement of any candidate pool.
    """
    return p.conj(mask)


def isometry_group(points, extra=()):
    """Maps from a candidate list that send the point set onto itself.

    Returns the subset of candidates that are symmetries.  Candidates are
    the 12 dihedral maps (six rotations, with and without reflection),
    optionally composed with the Galois maps.
    """
    S = {p.key() for p in points}

    def rot_k(k):
        def f(p):
            for _ in range(k):
                p = rot60(p)
            return p
        return f

    cands = []
    for k in range(6):
        cands.append((f"rot{60*k}", rot_k(k)))
        cands.append((f"rot{60*k}+refl", lambda p, g=rot_k(k): reflect_x(g(p))))
    for name, f in list(cands):
        for m in (extra or ()):
            cands.append((f"{name}+galois{m}",
                          lambda p, g=f, m=m: galois(g(p), m)))

    return [(n, f) for n, f in cands
            if {f(p).key() for p in points} == S]


def orbits(points, maps):
    """Union-find over the given symmetry maps.  No group library needed."""
    idx = {p.key(): i for i, p in enumerate(points)}
    parent = list(range(len(points)))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for _, f in maps:
        for i, p in enumerate(points):
            j = idx.get(f(p).key())
            if j is not None:
                ra, rb = find(i), find(j)
                if ra != rb:
                    parent[ra] = rb
    out = {}
    for i in range(len(points)):
        out.setdefault(find(i), []).append(i)
    return sorted(out.values(), key=len, reverse=True)
