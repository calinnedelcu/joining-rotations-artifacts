#!/usr/bin/env python3
"""Minimise a monochromatic-pair gadget, in whatever field it lives in.

Usage: shrink_gadget.py GRAPH.vtx --primes 2,3,5 --pair 0,1 [--seed N]

data/vtx/T721.vtx never parsed until now: its coordinates use sqrt2, sqrt3 and
sqrt6, and K.sqrt had the squarefree divisors of the classical field hardcoded,
so it answered None for sqrt2 and the strict parser refused the file.  With the
field set to Q(sqrt2, sqrt3) it reads, and what it is turns out to be worth the
fix: 721 vertices, 3948 edges, 4-colourable, and every 4-colouring gives
(-1, 0) and (1, 0) the same colour.

That is a distance-2 monochromatic-pair gadget -- the role L_374 plays in the
record, since a pair at distance 2 = sqrt4 is what theta_4 = arccos(7/8) spindles
into a unit edge.  Q(sqrt2, sqrt3, sqrt5) admits theta_4 (sin = sqrt15/8), so a
gadget of F vertices here plus an exploiter gives a 5-chromatic graph, and
nobody has minimised in this field.

Forcing the pair is literally non-4-colourability of the graph plus the virtual
edge between the two points, so the whole minimiser applies unchanged: add that
edge, protect its ends, and shrink.
"""
import os, sys, time, argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.field import set_primes
import hn.construct as CC
ap = argparse.ArgumentParser()
ap.add_argument("graph")
ap.add_argument("--primes", default="2,3,5")
ap.add_argument("--pair", default="0,1")
ap.add_argument("--seed", type=int, default=0)
a = ap.parse_args()
set_primes(tuple(int(t) for t in a.primes.split(",")))
CC.refresh_field()
from hn.io import load_vtx, save_points, save_edges
from hn.construct import edges
from hn.minimise import verify
from hn.fastshrink import sample_descend, batch_delete
from hn.sat import find_triangle
from hn.graph import induced

OUT = os.path.join(os.path.dirname(__file__), "..", "out")
log = lambda s: print(f"[{time.strftime('%H:%M:%S')}] {s}", flush=True)
i0, j0 = (int(t) for t in a.pair.split(","))
G = load_vtx(a.graph)
E = edges(G)
virtual = (min(i0, j0), max(i0, j0))
EV = sorted(set(E) | {virtual})
log(f"{os.path.basename(a.graph)}: {len(G)} vertices, {len(E)} unit edges in "
    f"Q(sqrt{a.primes.replace(',', ', sqrt')})")
# Pin a triangle.  Without one the refutation has to explore all 4! colour
# permutations and the same check costs two minutes instead of seconds -- and
# sample_descend then pays that on every round.
tri = find_triangle(len(G), EV)
t = time.time()
assert verify(G, EV, triangle=tri), "this graph does not force the pair monochromatic"
log(f"forces the pair {virtual} monochromatic, verified in {time.time()-t:.0f}s "
    f"(triangle {tri} pinned)")

keep = sample_descend(G, EV, list(range(len(G))), seed=a.seed, log=log)
log(f"after sampling: {len(keep)} vertices")
keep = batch_delete(G, EV, keep, seed=a.seed, log=log)
log(f"after batch deletion: {len(keep)} vertices")
assert verify(G, EV, keep, triangle=tri), "the reduced gadget stopped forcing the pair"
Q, F = induced(G, E, sorted(keep))          # the REAL edges, not the virtual one
tag = f"gadget_{os.path.basename(a.graph).split('.')[0]}_{a.seed}"
save_points(f"{OUT}/{tag}.pts", Q)
save_edges(f"{OUT}/{tag}.edge", len(Q), F)
log(f"minimal gadget here: {len(Q)} vertices, {len(F)} edges, saved as {tag}"
    + ("   <<< SMALLER THAN THE CLASSICAL L_374" if len(Q) < 374 else ""))
