#!/usr/bin/env python3
"""Colour patterns a large part leaves on its interface with the small part.

Usage: patterns.py [Lfile ...]      (files under data/parts/, default v374e1860.vtx)

Every 4-colouring of L, restricted to the vertices of L that have an edge to
theta_4(S) -- the origin, the 12 reference points at radius 2 and the
auxiliary points at radii sqrt11/2 -+ sqrt3/6 -- is a pattern.  The small part
works with L iff it blocks every pattern.  So the pattern set is the only
thing about L that the small part sees, and two large parts with the same
pattern set have the same minimum small part.

Measured: Parts' two minimal M6A large parts v374e1860 and v374e1868 leave
the SAME 28 patterns (up to colour permutation); v375e1920 leaves 36;
the accumulative graphs v403e2112 36, v412e2106 and v451e2400 44 on a
25-vertex interface; the M6B v374e1864 leaves 32 of which S_136 blocks 12;
the order-3 symmetric v376e1890 leaves 45 of which S_136 blocks only 43, so
it needs a different small part.
"""
import os, sys, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn import load_vtx, find_triangle
from hn.construct import edges, theta4, norm, ORIGIN
from hn.sat import Colouring

D = os.path.join(os.path.dirname(__file__), "..", "data", "parts")
S = load_vtx(f"{D}/v136e564.vtx")
RS = [theta4(p) for p in S if p.key() != ORIGIN.key()]
ES, nS = edges(RS), len(RS)


def patterns(L):
    """(interface vertex indices, set of patterns keyed by point coordinates)."""
    nL = len(L)
    P = L + RS
    E = edges(P)
    iface = sorted({a for a, b in E if a < nL and b >= nL} | {b for a, b in E if b < nL and a >= nL})
    cross = [(a, b - nL) for a, b in E if a < nL and b >= nL] + [(b, a - nL) for a, b in E if b < nL and a >= nL]
    EL = edges(L)
    C = Colouring(nL, EL, k=4, selectors=False)
    o = next(i for i, p in enumerate(L) if p.key() == ORIGIN.key())
    adj = collections.defaultdict(set)
    for a, b in EL:
        adj[a].add(b)
        adj[b].add(a)
    nb = sorted(adj[o], key=lambda v: L[v].key())
    tri = next((o, u, w) for u in nb for w in nb if u < w and w in adj[u])
    C.break_colour_symmetry(tri)          # same three points in every L: patterns are comparable
    pats = []
    while C.colourable():
        col = C.model_colouring()
        pats.append(tuple(col[v] for v in iface))
        C.solver.add_clause([-C.var(v, col[v]) for v in iface])
    C.close()
    return iface, cross, pats


def blocked_by_S(iface, cross, pat):
    colmap = dict(zip(iface, pat))
    Cs = Colouring(nS, ES, k=4, selectors=False)
    for a, s in cross:
        Cs.solver.add_clause([-Cs.var(s, colmap[a])])
    r = not Cs.colourable()
    Cs.close()
    return r


if __name__ == "__main__":
    for name in sys.argv[1:] or ["v374e1860.vtx"]:
        L = load_vtx(f"{D}/{name}")
        iface, cross, pats = patterns(L)
        radii = sorted(collections.Counter(round(norm(L[v]), 4) for v in iface).items())
        nb = sum(blocked_by_S(iface, cross, p) for p in pats)
        print(f"{name}: {len(L)} vertices, interface {len(iface)} {radii}, "
              f"{len(pats)} patterns, {nb} blocked by S_136")
