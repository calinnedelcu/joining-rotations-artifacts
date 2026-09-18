"""Unit-distance graphs over point sets in K."""
from __future__ import annotations
from .field import Pt, is_unit


def unit_vectors(points):
    """The distinct difference vectors of length 1 occurring in `points`.

    Returns a list of Pt, closed under negation.  In the 510-vertex record
    graph there are only 72 of them.  Knowing the set turns edge extraction
    from O(n^2) exact tests into O(n*|S|) hash lookups, which is what makes
    larger candidate pools affordable.
    """
    seen, out, n = set(), [], len(points)
    for i in range(n):
        for j in range(i + 1, n):
            for d in (points[j] - points[i], points[i] - points[j]):
                if d.norm2().is_one() and d.key() not in seen:
                    seen.add(d.key())
                    out.append(d)
    return out


def edges_bruteforce(points):
    """All unit-distance pairs, by exact test on every pair. O(n^2)."""
    n = len(points)
    return [(i, j) for i in range(n) for j in range(i + 1, n)
            if is_unit(points[i], points[j])]


def edges_by_vectors(points, vectors):
    """All unit-distance pairs, by probing p + d for each known vector d.

    `vectors` is a collection of Pt.  Much faster than the O(n^2) sweep once
    the vector set of the ambient ring is known.
    """
    index = {p.key(): i for i, p in enumerate(points)}
    out = set()
    for i, p in enumerate(points):
        for d in vectors:
            j = index.get((p + d).key())
            if j is not None and j != i:
                out.add((min(i, j), max(i, j)))
    return sorted(out)


def degrees(n, edges):
    d = [0] * n
    for a, b in edges:
        d[a] += 1
        d[b] += 1
    return d


def induced(points, edges, keep):
    """Restrict to the vertex set `keep` (an iterable of indices)."""
    keep = sorted(set(keep))
    remap = {v: i for i, v in enumerate(keep)}
    pts = [points[v] for v in keep]
    es = [(remap[a], remap[b]) for a, b in edges if a in remap and b in remap]
    return pts, es
