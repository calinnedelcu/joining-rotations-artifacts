#!/usr/bin/env python3
"""Drive any 5-chromatic graph down, with no pool and no lattice.

Usage: descend.py GRAPH.pts [--seed N] [--time SECONDS]

`drive_down.py` surrounds its graph with a candidate pool so the exact master
can trade vertices in as well as out, and to do that it has to build the
ambient lattice -- which ties it to theta_4.  The descent itself needs none of
that.  The vertex-critical pass only ever *removes*: for each vertex in turn it
asks whether the graph minus that vertex is still 5-chromatic, which takes an
UNSAT proof to answer yes and nothing else.  So it runs on a graph from any
rotation, any field, any construction, read straight off disk.

That matters because several floors in `results/` were measured with randomised
trimming and recorded as the basin being "characterised".  On the asymmetric
basin that reading was wrong -- trimming plateaued at 1279 and this pass walked
past it without slowing.  This is how the other floors get the same test.
"""
import os, sys, time, argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

OUT = os.path.join(os.path.dirname(__file__), "..", "out")
ap = argparse.ArgumentParser()
ap.add_argument("graph")
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--time", type=float, default=None)
ap.add_argument("--tag", default=None)
ap.add_argument("--primes", default="3,5,11",
                help="the field the coordinates were written in.  A .pts file "
                     "stores exact field elements, so reading it under the "
                     "wrong primes gives points that are numerically wrong and "
                     "an edge set that is quietly much too small")
a = ap.parse_args()
log = lambda s: print(s, flush=True)

from hn.field import set_primes
set_primes(tuple(int(x) for x in a.primes.split(",")))
import hn.construct as C
C.refresh_field()
from hn.io import load_points, save_points, save_edges
from hn.construct import edges_grid
from hn.graph import induced
from hn.hitting import search
from hn import verify, find_triangle

P = load_points(a.graph)
E = edges_grid(P)
tag = a.tag or f"desc_{os.path.basename(a.graph).split('.')[0]}_{a.seed}"
log(f"{os.path.basename(a.graph)}: {len(P)} vertices, {len(E)} edges")
# Fixing one triangle's three colours breaks the colour symmetry and is what
# makes the refutation affordable: without it the same check on 2901 vertices
# ran for over half an hour.  It is sound -- any proper colouring can be
# permuted to agree with it.
t = time.time()
tri = find_triangle(len(P), E)
assert verify(P, E, list(range(len(P))), triangle=tri), "the graph is not 5-chromatic"
log(f"verified 5-chromatic before starting ({time.time()-t:.0f}s, "
    f"triangle {'fixed' if tri else 'none found'})")


def save(best):
    Q, F = induced(P, E, sorted(best))
    save_points(f"{OUT}/{tag}.pts", Q)
    save_edges(f"{OUT}/{tag}.edge", len(Q), F)
    log(f"  saved {len(Q)} vertices, {len(F)} edges"
        + ("   <<< BELOW THE 509 RECORD" if len(Q) < 509 else ""))


best, proven = search(P, E, start=list(range(len(P))), bound=len(P) - 1,
                      time_limit=a.time, seed=a.seed, log=log, on_improve=save,
                      bootstrap_essential=False)
if best is not None:
    save(best)
    log(f"best {len(best)} vertices; proven minimum over this graph: {proven}")
