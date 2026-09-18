#!/usr/bin/env python3
"""The exact minimum number of edges on a fixed point set.

Usage: min_edges.py GRAPH.vtx [--bound N] [--seed N] [--pairs 0]

The published edge record is e5 <= 2406 (de Grey & Parts, Geombinatorics 32(2)
2022): they took the 509-vertex graph's 2442 unit pairs and discarded 36 without
an exhaustive search.  Two unrefereed 2026 repositories go further -- 2259 on
Parts' exact points and 2236 on a slightly different drawing -- and both verify
(exact unit distances, not 4-colourable, edge-critical).  Nobody has the *minimum*.

This is the same implicit hitting set as the vertex search with the objects
swapped.  Fix all 509 points; the variables are the 2442 unit pairs; a graph is
5-chromatic iff no 4-colouring of the points leaves every chosen pair bichromatic.
So a colouring that survives gives the cut "choose at least one pair that this
colouring makes monochromatic" -- identical in form to the vertex cuts, and the
search space is far smaller: choosing 2259 of 2442 is about 273 bits, inside the
band where this master converges, where the vertex problem sits at 972.

Edge-criticality, which both repositories prove, is a *local* property: no single
edge can go.  This asks the global question.
"""
import os, sys, time, argparse, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn import load_vtx
from hn.construct import edges
from hn.io import save_edges
from hn.sat import Colouring, find_triangle
from hn.colour import ConflictColouring
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Solver

OUT = os.path.join(os.path.dirname(__file__), "..", "out")
ap = argparse.ArgumentParser()
ap.add_argument("graph")
ap.add_argument("--bound", type=int, default=None)
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--time", type=float, default=None)
ap.add_argument("--tabu", type=int, default=40000)
ap.add_argument("--bootstrap", type=int, default=3000,
                help="Tabucol colourings harvested before the search; one that leaves a "
                     "single monochromatic pair forces it")
a = ap.parse_args()
log = lambda s: print(f"[{time.strftime('%H:%M:%S')}] {s}", flush=True)

P = load_vtx(a.graph)
E = edges(P)
n, m = len(P), len(E)
bound = a.bound if a.bound is not None else m - 1
log(f"{os.path.basename(a.graph)}: {n} points carrying {m} unit pairs; "
    f"looking for a 5-chromatic selection of at most {bound}")

# master: one variable per unit pair, cardinality bound, cuts from colourings
top = m
master = Solver(name="cadical195")
card = CardEnc.atmost(lits=list(range(1, m + 1)), bound=bound, top_id=top,
                      encoding=EncType.kmtotalizer)
for cl in card.clauses:
    master.add_clause(cl)
log(f"master: {m} variables, cardinality encoding {len(card.clauses)} clauses")

tri = find_triangle(n, E)
cc = ConflictColouring(n, E, k=4)

# Bootstrap: a 4-colouring of the point set that leaves exactly ONE unit pair
# monochromatic forces that pair -- any 5-chromatic selection must contain it, so
# the cut is a unit clause.  Tabucol produces these constantly (the logs are full of
# "best extra 1"), and each one is worth more than a thousand long cuts.  Harvest
# them before the search rather than stumbling on them during it.
import random as _r
_rng = _r.Random(a.seed + 77)
forced, seen2, kept = set(), set(), []
t_b = time.time()
for _ in range(a.bootstrap):
    col, _nc = cc.run(a.tabu, init=[_rng.randrange(4) for _ in range(n)])
    mono = tuple(i for i, (x, y) in enumerate(E) if col[x] == col[y])
    if not mono or mono in seen2:
        continue
    seen2.add(mono)
    master.add_clause([i + 1 for i in mono])
    kept.append([i + 1 for i in mono])
    if len(mono) == 1:
        forced.add(mono[0])
log(f"bootstrap: {len(seen2)} distinct colourings, {len(forced)} unit pairs forced "
    f"outright  ({time.time()-t_b:.0f}s)")
cuts_boot = len(seen2)
import random
rng = random.Random(a.seed)
best = None
cuts = cuts_boot
t0 = time.time()
it = 0
while True:
    it += 1
    if a.time and time.time() - t0 > a.time:
        log("time limit")
        break
    # The cardinality constraint only says "at most bound", so the easiest model is a
    # tiny selection -- the search wandered between 883 and 2266 instead of climbing.
    # Preferring every edge TRUE makes the solver hug the bound from below, which is
    # where a 5-chromatic selection can actually be.
    master.set_phases([i + 1 for i in range(m)])
    if not master.solve():
        log(f"master UNSAT at bound {bound}: no 5-chromatic selection has "
            f"{bound} edges or fewer.  The minimum over this point set is {bound+1}.")
        break
    mod = master.get_model()
    S = [i for i in range(m) if mod[i] > 0]
    sub = [E[i] for i in S]
    c = Colouring(n, sub, k=4, selectors=False)
    if tri and all(v in range(n) for v in tri):
        c.break_colour_symmetry(list(tri))
    ok = c.colourable()
    if not ok:
        c.close()
        best = list(S)
        bound = len(S) - 1
        Q = [E[i] for i in best]
        save_edges(f"{OUT}/mine_{a.seed}.edge", n, Q)
        log(f"[{it}] 5-chromatic with {len(S)} edges  <<< "
            + ("BELOW THE PUBLISHED 2406" if len(S) < 2406 else "")
            + (" AND BELOW 2236" if len(S) < 2236 else ""))
        master.delete()
        master = Solver(name="cadical195")
        card = CardEnc.atmost(lits=list(range(1, m + 1)), bound=bound, top_id=top,
                              encoding=EncType.kmtotalizer)
        for cl in card.clauses:
            master.add_clause(cl)
        for cl in kept:
            master.add_clause(cl)
        continue
    col = c.model_colouring()
    c.close()
    # every unit pair this colouring makes monochromatic -- one of them must be chosen
    mono = [i for i, (x, y) in enumerate(E) if col[x] == col[y]]
    master.add_clause([i + 1 for i in mono])
    kept.append([i + 1 for i in mono])
    cuts += 1
    # a second, sharper cut from a conflict colouring that minimises monochromatic pairs
    col2, nc = cc.run(a.tabu, init=[rng.randrange(4) for _ in range(n)])
    mono2 = [i for i, (x, y) in enumerate(E) if col2[x] == col2[y]]
    if mono2 and len(mono2) < len(mono):
        master.add_clause([i + 1 for i in mono2])
        kept.append([i + 1 for i in mono2])
        cuts += 1
    if it % 20 == 0:
        log(f"[{it}] |S|={len(S)} colourable; cut with {len(mono)} mono pairs "
            f"(best extra {len(mono2)}); cuts={cuts}  ({time.time()-t0:.0f}s)")
