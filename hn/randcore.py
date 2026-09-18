"""Randomised UNSAT-core extraction, the trick behind Heule's 553.

A SAT solver's refutation depends heavily on the order the clauses arrive in, so
the same graph refuted twice the same way yields the same core and the same
subgraph.  Heule's method is explicit about this: "we shuffle the input formula
and apply graph trimming on the result... This process is repeated until
randomization cannot further reduce the size of the graph."

hn.minimise.propose_core is deterministic, which quietly made every "independent"
descent in this repository dependent: the engine's several seeds were extracting
the same core and the accumulative graph could not grow.  Permuting the vertex
labels and shuffling the edges before building the formula fixes that, and
mapping the core back is a relabelling.
"""
from __future__ import annotations
import random
from .sat import Colouring, find_triangle
from .graph import induced


def randomized_core(n, edges, keep, seed=0, protect=(), k=4):
    """An UNSAT core of `keep`, under a random clause order.  None if colourable.

    Returns vertex indices in the ORIGINAL labelling.
    """
    rng = random.Random(seed)
    keep = sorted(keep)
    perm = list(range(n))
    rng.shuffle(perm)                      # new label for each vertex
    back = [0] * n
    for old, new in enumerate(perm):
        back[new] = old
    e2 = [(min(perm[u], perm[v]), max(perm[u], perm[v])) for u, v in edges]
    rng.shuffle(e2)                        # and a new clause order
    k2 = sorted(perm[v] for v in keep)
    prot = {perm[v] for v in protect}
    c = Colouring(n, e2, k=k)
    tri = find_triangle(n, e2)
    if tri and set(tri) <= set(k2):
        c.break_colour_symmetry(list(tri))
        prot |= set(tri)
    try:
        if c.colourable(k2):
            return None
        return sorted({back[v] for v in set(c.core()) | prot})
    finally:
        c.close()


def many_cores(n, edges, keep, seeds=8, protect=(), k=4, log=None):
    """Distinct minimal-ish subgraphs from independent shuffles.

    This is what the accumulative graph is supposed to be built from: several
    genuinely different answers to the same question, whose union holds more
    structure than any one of them.
    """
    out, seen = [], set()
    for s in range(seeds):
        c = randomized_core(n, edges, keep, seed=s, protect=protect, k=k)
        if c is None:
            continue
        key = tuple(c)
        if key in seen:
            continue
        seen.add(key)
        out.append(c)
        if log:
            log(f"   shuffle {s}: core {len(c)}")
    return out
