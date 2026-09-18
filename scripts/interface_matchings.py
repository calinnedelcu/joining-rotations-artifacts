#!/usr/bin/env python3
"""Enumerate every minimum interface of theta_4, and check its shape.

scripts/interface_bound.py proves the minimum is five cross edges.  This
enumerates ALL five-edge sets achieving it and establishes the structure the
paper states: how many there are, that none touches the shared centre, that each
is a perfect matching, the orbit profile of each, and the factorisation of the
count.

Everything is recomputed here; nothing is taken from the prose.

Run: .venv/bin/python scripts/interface_matchings.py    (a few minutes)
"""
import itertools
import math
import os
import sys
import time
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.joins import rational_spindle
from hn.construct import ball, rotate, edges_grid, norm
from hn.lattice import Lattice
from hn.algcolour import klein_colourings, z4_colourings, apply_colouring

DEPTH, RADIUS = 4, 2.53


def main():
    WL, _, cs = rational_spindle(4, 1).build()
    V = ball(WL, DEPTH, RADIUS)
    n = len(V)
    P = V + [rotate(p, cs) for p in V]
    cross = [(x, y - n) if x < n else (y, x - n)
             for x, y in edges_grid(P) if (x < n) != (y < n)]
    print(f"ball {n} points, {len(cross)} cross edges")

    # The cross edges are not a feature of the ball.  Lambda = R (+) theta(R) is
    # a direct sum, so u = p - theta(q) determines (p, q), and cross edges are in
    # bijection with the unit vectors of Lambda -- a finite, exact, ball-free
    # list.  Growing the ball therefore cannot add one.
    from hn.field import Pt
    from hn.lattice import Lattice
    def sub2(a, b):
        return Pt(a.x - b.x, a.y - b.y)
    us = [sub2(V[a], rotate(V[b], cs)) for a, b in cross]
    keys = {u.key() for u in us}
    J = Lattice(list(WL) + [rotate(w, cs) for w in WL])
    JU = J.unit_vectors()
    assert len(keys) == len(cross), "two cross edges share a unit vector"
    assert len(JU) == len(cross), "cross edges do not match the unit vectors"
    print(f"  they biject with the {len(JU)} unit vectors of the rank-{J.rank} "
          f"joint lattice, so the count is ball-free")
    for d, r in ((4, 2.53), (5, 2.53), (4, 3.0)):
        W = ball(WL, d, r)
        m = len(W)
        c2 = sum(1 for x, y in edges_grid(W + [rotate(t, cs) for t in W])
                 if (x < m) != (y < m))
        assert c2 == len(cross), f"depth {d} radius {r} gave {c2}"
        print(f"  depth {d}, radius {r}: {m:6d} points -> {c2} cross edges")

    L0 = Lattice(WL)
    uc = [c for c, _ in L0.unit_vectors()]
    certs = klein_colourings(uc, L0.rank) + z4_colourings(uc, L0.rank)
    coord = [L0.coords(p) for p in V]
    tab = [[apply_colouring(c, coord[i]) for i in range(n)] for c in certs]
    assert apply_colouring(certs[0], (0,) * L0.rank) == 0

    # only the 6 permutations fixing colour 0 give a colouring of a union that
    # shares the centre; the other 18 colour the centre twice over
    perms = [p for p in itertools.permutations(range(4)) if p[0] == 0]
    pats = set()
    for tL in tab:
        for tS in tab:
            for pm in perms:
                mono = frozenset(k for k, (p, q) in enumerate(cross)
                                 if tL[p] == pm[tS[q]])
                assert mono, "an admissible pairing 4-colours the union"
                pats.add(mono)
    pats = sorted(pats, key=sorted)
    print(f"{len(certs)**2 * len(perms)} admissible pairings -> {len(pats)} patterns")

    # an edge out of the centre is never monochromatic, so it hits nothing
    touching = {k for k, (p, q) in enumerate(cross) if norm(V[p]) < 1e-12 or norm(V[q]) < 1e-12}
    usable = [k for k in range(len(cross)) if k not in touching]
    assert not any(k in touching for pat in pats for k in pat)
    print(f"{len(touching)} cross edges touch the centre and appear in no pattern;"
          f" {len(usable)} usable")

    FULL = (1 << len(pats)) - 1
    hit = {k: 0 for k in usable}
    for i, pat in enumerate(pats):
        for k in pat:
            hit[k] |= 1 << i

    t = time.time()
    sols = []
    U = usable
    for a in range(len(U)):
        ma = hit[U[a]]
        for b in range(a + 1, len(U)):
            mb = ma | hit[U[b]]
            for c in range(b + 1, len(U)):
                mc = mb | hit[U[c]]
                for d in range(c + 1, len(U)):
                    md = mc | hit[U[d]]
                    for e in range(d + 1, len(U)):
                        if md | hit[U[e]] == FULL:
                            sols.append((U[a], U[b], U[c], U[d], U[e]))
    print(f"\nfive-edge sets meeting every pattern: {len(sols)}  ({time.time()-t:.0f}s)")

    # each a perfect matching?
    def ends(s):
        return [cross[k][0] for k in s], [cross[k][1] for k in s]
    matchings = sum(1 for s in sols
                    if len(set(ends(s)[0])) == 5 and len(set(ends(s)[1])) == 5)
    print(f"  of those, perfect matchings (10 distinct endpoints): {matchings}")

    # is the usable cross structure itself already a matching?
    lhs = Counter(cross[k][0] for k in usable)
    rhs = Counter(cross[k][1] for k in usable)
    print(f"  the {len(usable)} usable cross edges are themselves a matching: "
          f"{max(lhs.values()) == 1 and max(rhs.values()) == 1}")

    # orbit profile
    R2, RL, RS = 2.0, math.sqrt(11)/2 + math.sqrt(3)/6, math.sqrt(11)/2 - math.sqrt(3)/6
    def kind(k):
        p, q = cross[k]
        a, b = norm(V[p]), norm(V[q])
        if abs(a - R2) < 1e-9 and abs(b - R2) < 1e-9:
            return "reference"
        if {round(a, 6), round(b, 6)} == {round(RL, 6), round(RS, 6)}:
            return "auxiliary"
        return "other"
    prof = Counter(tuple(sorted(Counter(kind(k) for k in s).items())) for s in sols)
    print("\n  orbit profile of the solutions:")
    for pr, c in prof.most_common():
        print(f"    {dict(pr)}  ->  {c}")

    # the factorisation
    refs = {s[i] for s in sols for i in range(5) if kind(s[i]) == "reference"}
    def direction(k):
        p, q = cross[k]
        return 0 if norm(V[p]) < norm(V[q]) else 1
    by_ref = Counter()
    dirsplit = Counter()
    for s in sols:
        r = [k for k in s if kind(k) == "reference"][0]
        aux = [k for k in s if kind(k) == "auxiliary"]
        by_ref[r] += 1
        dirsplit[tuple(sorted(Counter(direction(k) for k in aux).items()))] += 1
    print(f"\n  distinct reference edges used: {len(refs)}")
    print(f"  solutions per reference edge: {sorted(set(by_ref.values()))}")
    print(f"  auxiliary split by crosswise direction: {dict(dirsplit)}")
    # the pairs are admissible RELATIVE TO the reference edge, so count per ref
    per = {}
    for s in sols:
        r = [k for k in s if kind(k) == "reference"][0]
        a0 = frozenset(k for k in s if kind(k)=='auxiliary' and direction(k)==0)
        a1 = frozenset(k for k in s if kind(k)=='auxiliary' and direction(k)==1)
        per.setdefault(r, set()).add((a0, a1))
    n0 = {r: len({a for a, _ in v}) for r, v in per.items()}
    n1 = {r: len({b for _, b in v}) for r, v in per.items()}
    full = {r: len(v) == n0[r]*n1[r] for r, v in per.items()}
    print(f"  per reference edge: {sorted(set(n0.values()))} pairs in one direction, "
          f"{sorted(set(n1.values()))} in the other")
    print(f"  every combination of the two occurring, for every reference edge: "
          f"{all(full.values())}")
    a, b = sorted(set(n0.values()))[0], sorted(set(n1.values()))[0]
    print(f"  => {len(refs)} x {a} x {b} = {len(refs)*a*b}")
    globally0 = {frozenset(k for k in s if kind(k)=='auxiliary' and direction(k)==0) for s in sols}
    print(f"  (across ALL reference edges the direction-0 pairs number "
          f"{len(globally0)}, so the 8 is relative to the reference edge)")
    print(f"\n  C(66,5) = {math.comb(len(usable),5)}, so the solutions are "
          f"{100*len(sols)/math.comb(len(usable),5):.3f}% of all five-subsets")


if __name__ == "__main__":
    main()
