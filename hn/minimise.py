"""Shrinking a 5-chromatic unit-distance graph.

SAFETY RULE, and it is not optional
-----------------------------------
Every candidate produced here is re-verified from scratch by `verify`,
in a fresh solver, with NO symmetry-breaking clauses and NO selector
literals.  Nothing is ever reported on the strength of an UNSAT core alone.

The reason is a real trap, hit while building this module.  The core of an
UNSAT solve tells you which assumptions the proof used -- but the proof also
uses the symmetry-breaking unit clauses that pin a triangle to colours
0,1,2.  If the core drops one of those triangle vertices, the unit clause
still constrains it, so the "core subgraph" is easier for the solver than
the induced subgraph really is.  Measured on the 510-vertex record graph:
the core came back at 507 vertices, and the induced subgraph on those 507
turned out to be 4-COLOURABLE.  A 507-vertex "record" that is not a record.

So: cores are a heuristic for *proposing* smaller sets.  `verify` decides.
"""
from __future__ import annotations
import random
from .graph import induced
from .sat import Colouring, find_triangle


def verify(points, edges, keep=None, k=4, triangle=None):
    """Independent check: is the induced subgraph NOT k-colourable?

    Fresh solver, no selector literals.  Colour symmetry may be broken only
    by pinning a triangle that is guaranteed to be inside `keep` -- that is
    sound for every subgraph containing it, and turns a 78 s check into a
    2.6 s one on the 510-vertex graph.  Pass triangle=None for the slow,
    assumption-free check when you want belt and braces.
    """
    keep = list(range(len(points))) if keep is None else sorted(keep)
    if triangle is not None and not set(triangle) <= set(keep):
        triangle = None
    pts, es = induced(points, edges, keep)
    idx = {v: i for i, v in enumerate(keep)}
    c = Colouring(len(pts), es, k=k, selectors=False)
    try:
        if triangle is not None:
            c.break_colour_symmetry([idx[v] for v in triangle])
        return not c.colourable()
    finally:
        c.close()


def propose_core(points, edges, keep=None, protect=()):
    """Use an UNSAT core to propose a smaller vertex set.

    `protect` must contain any vertex whose colour is pinned, so that
    symmetry breaking cannot corrupt the core.  Returns None if the set is
    already colourable.
    """
    keep = list(range(len(points))) if keep is None else sorted(keep)
    c = Colouring(len(points), edges, k=4)
    tri = find_triangle(len(points), edges)
    if tri and all(v in set(keep) for v in tri):
        c.break_colour_symmetry(tri)
        protect = set(protect) | set(tri)
    try:
        if c.colourable(keep):
            return None
        return sorted(set(c.core()) | set(protect))
    finally:
        c.close()


def shrink(points, edges, keep=None, seed=0, verbose=True):
    """Core extraction, then greedy vertex deletion, everything verified.

    Returns the surviving vertex list.  This reaches a *minimal* subgraph
    (nothing more can be removed one at a time), not a *minimum* one -- see
    the project notes on why that gap is the whole problem.
    """
    rng = random.Random(seed)
    keep = list(range(len(points))) if keep is None else sorted(keep)
    tri = find_triangle(len(points), edges)
    if tri and not set(tri) <= set(keep):
        tri = None
    assert verify(points, edges, keep, triangle=tri), "input is not 5-chromatic"

    prop = propose_core(points, edges, keep, protect=tri or ())
    if prop and len(prop) < len(keep) and verify(points, edges, prop, triangle=tri):
        if verbose:
            print(f"  nucleu: {len(keep)} -> {len(prop)}")
        keep = prop

    protected = set(tri or ())
    order = [v for v in keep if v not in protected]
    rng.shuffle(order)
    kept = set(keep)
    removed = 0
    for v in order:
        trial = sorted(kept - {v})
        if verify(points, edges, trial, triangle=tri):
            kept = set(trial)
            removed += 1
            if verbose and removed % 25 == 0:
                print(f"  sters {removed}, ramas {len(kept)}")
    keep = sorted(kept)
    if verbose:
        print(f"  stergere: -> {len(keep)} varfuri")
    return keep
