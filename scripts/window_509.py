#!/usr/bin/env python3
"""Decidable windows: the record plus ~76 candidates, at bound 508.

Usage: window_509.py [--window 76] [--seed N] [--rounds 40] [--harvest 1500]

The convergence law measured over 88 runs of this project: the master decides when
`log2 C(free, bound)` is under about 325 bits and never when it is over. Beating 509
over a 978-point pool with both parts free is 972 bits, which is why every such run
here has ground forever. The record plus **76 candidates** is about 320 bits -- right
at the frontier, and decidable.

So instead of one pool too large to settle, take many windows small enough to settle,
each a different 76-candidate neighbourhood of the record, and decide them one after
another. A hit is a 508-vertex graph. A refutation removes that window for good.

**The bootstrap, carried over from the edge search where it tripled the rate.** A
4-colouring of the pool that leaves exactly one monochromatic edge is a unit clause:
in the vertex encoding it forces *both* endpoints to be kept, since dropping either
would let that colouring through. Tabucol produces such colourings constantly on
these graphs. Harvesting them before the search, rather than meeting them during it,
is worth more than any number of long cuts.
"""
import os, sys, time, random, argparse, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn import load_vtx, verify
from hn.io import load_points, save_points, save_edges
from hn.graph import induced
from hn.construct import unit_vector_family, ball, dedup, edges, rotate, ROT
from hn.colour import ConflictColouring
from hn.hitting import search
from hn.sat import find_triangle

OUT = os.path.join(os.path.dirname(__file__), "..", "out")
ap = argparse.ArgumentParser()
ap.add_argument("--window", type=int, default=76)
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--rounds", type=int, default=40)
ap.add_argument("--harvest", type=int, default=1500)
ap.add_argument("--degree", type=int, default=3)
ap.add_argument("--time", type=float, default=900.0)
a = ap.parse_args()
log = lambda s: print(f"[{time.strftime('%H:%M:%S')}] {s}", flush=True)

G = load_vtx("data/vtx/509.vtx")
gk = {p.key() for p in G}
W = unit_vector_family(2)
B = ball(W, 4, 2.53)
LAT = dedup(B + [rotate(p, ROT["theta4"]) for p in B])
cands = [p for p in LAT if p.key() not in gk]
P0 = list(G) + cands
E0 = edges(P0)
inG = set(range(len(G)))
deg = collections.Counter()
for u, v in E0:
    if (u in inG) != (v in inG):
        deg[v if u in inG else u] += 1
pool_c = [i for i in range(len(G), len(P0)) if deg[i] >= a.degree]
log(f"record 509 + {len(pool_c)} candidates at degree >= {a.degree}; "
    f"windows of {a.window} are about "
    f"{a.window * 2.9:.0f} bits, the frontier is 325")

# Random windows out of 1091 candidates cover a vanishing fraction of the space, so
# let the colourings choose.  Harvest 4-colourings of the record's own pool once; a
# candidate is useful exactly when it kills some of them, i.e. when all four colours
# already appear among its neighbours in the record, because then that colouring
# cannot be extended to it.  Windows drawn from the top scorers are the only windows
# where a replacement structure could live.
rng = random.Random(a.seed)
adjG = collections.defaultdict(list)
for u, v in E0:
    if u in inG and v not in inG:
        adjG[v].append(u)
    elif v in inG and u not in inG:
        adjG[u].append(v)
# The record has no proper 4-colouring -- it is 5-chromatic -- so scoring against
# its colourings scores against nothing.  A 508-vertex graph is the record with some
# vertices removed and others put back, so the colourings that matter are the ones
# a REMOVAL opens up: delete a handful of record vertices, 4-colour what is left, and
# a candidate earns its place by killing that colouring.
Eg = [(u, v) for u, v in E0 if u in inG and v in inG]
score = collections.Counter()
t = time.time()
got = 0
for _ in range(a.harvest):
    drop = set(rng.sample(range(len(G)), rng.randint(4, 14)))
    sub = [v for v in range(len(G)) if v not in drop]
    idx = {v: k for k, v in enumerate(sub)}
    es = [(idx[u], idx[v]) for u, v in Eg if u not in drop and v not in drop]
    cc2 = ConflictColouring(len(sub), es, k=4)
    colr, nc = cc2.run(30000, init=[rng.randrange(4) for _ in range(len(sub))])
    if nc:
        continue
    got += 1
    full = {}
    for v, k in idx.items():
        full[v] = colr[k]
    for i in pool_c:
        used = {full[u] for u in adjG[i] if u in full}
        if len(used) == 4:
            score[i] += 1
ranked = sorted(pool_c, key=lambda i: -score[i])
top = [i for i in ranked if score[i]] or ranked
log(f"scored candidates against {got} proper 4-colourings of the record: "
    f"{len(top)} kill at least one, best kills {score[ranked[0]]}  ({time.time()-t:.0f}s)")
pool_c = top[:max(a.window * 3, 240)]
log(f"drawing windows of {a.window} from the {len(pool_c)} that do the work")

for r in range(a.rounds):
    take = rng.sample(pool_c, min(a.window, len(pool_c)))
    keep = sorted(inG | set(take))
    P, E = induced(P0, E0, keep)
    tri = find_triangle(len(P), E)
    start = sorted(range(len(G)))
    if not verify(P, E, start, triangle=tri):
        log(f"round {r}: window is not 5-chromatic, skipped")
        continue
    # harvest colourings that leave a single monochromatic edge: each forces both ends
    cc = ConflictColouring(len(P), E, k=4)
    forced, seen = set(), set()
    t = time.time()
    for _ in range(a.harvest):
        col, nc = cc.run(30000, init=[rng.randrange(4) for _ in range(len(P))])
        mono = tuple(sorted((x, y) for x, y in E if col[x] == col[y]))
        if not mono or mono in seen:
            continue
        seen.add(mono)
        if len(mono) == 1:
            forced.add(mono[0])
    log(f"round {r}: window {len(P)} points; harvested {len(seen)} colourings, "
        f"{len(forced)} edges forced whole  ({time.time()-t:.0f}s)")

    def save(best):
        Q, F = induced(P, E, sorted(best))
        save_points(f"{OUT}/win_{a.seed}_{r}.pts", Q)
        save_edges(f"{OUT}/win_{a.seed}_{r}.edge", len(Q), F)
        log(f"  {len(Q)} vertices" + ("   <<<<< BELOW THE 509 RECORD" if len(Q) < 509 else ""))

    best, proven = search(P, E, start=start, bound=508, time_limit=a.time,
                          cuts_per_iter=2, seed=a.seed * 31 + r, log=lambda _: None,
                          on_improve=save, grow_every=2, bootstrap_pairs=0,
                          bootstrap_essential=False, bootstrap_critical=True)
    if best is not None and len(best) < 509:
        save(best)
        log(f"round {r}: FOUND {len(best)} vertices")
        break
    log(f"round {r}: nothing under 509 here"
        + ("  (proven over this window)" if proven else "  (time limit)"))
