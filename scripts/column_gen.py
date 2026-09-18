#!/usr/bin/env python3
"""Column generation: let the learned colourings choose the pool.

Usage: column_gen.py [--rounds 6] [--add 40] [--seed N] [--ball 3.2]

Roadmap step 5 in docs/CONTEXT.md, and the one step never implemented. Every pool
in this repository is fixed before the search starts, which makes the pool the
binding constraint: if the answer is not inside it, the search learns nothing
about the record.

Exoo and Ismailescu do it the other way round (arXiv:1805.00157). They enumerate
the 4-colourings that survive, and for each one examine its rainbow triples and
add the circumcentre whenever the circumradius is exactly 1 -- points generated
BY the certificates rather than guessed in advance.

The same idea, stated for this machinery: a lattice point x kills a colouring c
when all four colours already appear among x's neighbours, since then c cannot be
extended to x at all. So run the master, collect the colourings it learns, score
every lattice point by how many of them it kills, and add the best scorers. That
is column generation with the colourings as the dual.
"""
import os, sys, time, argparse, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn import load_vtx, verify
from hn.io import load_points, save_points, save_edges
from hn.graph import induced
from hn.construct import unit_vector_family, ball, dedup, edges, rotate, ROT
from hn.hitting import Oracle, Master, Extender, mono_edges, kcore
from hn.colour import ConflictColouring, greedy_extend

OUT = os.path.join(os.path.dirname(__file__), "..", "out")
ap = argparse.ArgumentParser()
ap.add_argument("--graph", default="data/vtx/509.vtx")
ap.add_argument("--rounds", type=int, default=6)
ap.add_argument("--add", type=int, default=40)
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--ball", type=float, default=3.2)
ap.add_argument("--degree", type=int, default=6)
ap.add_argument("--pairs", type=int, default=300)
ap.add_argument("--colourings", type=int, default=400)
a = ap.parse_args()
log = lambda s: print(s, flush=True)

G = load_vtx(a.graph)
W = unit_vector_family(2)
V = ball(W, 4, a.ball)
LAT = dedup(V + [rotate(p, ROT["theta4"]) for p in V])
Gk = {p.key() for p in G}
outside = [p for p in LAT if p.key() not in Gk]
log(f"graph {len(G)} vertices; ambient lattice {len(LAT)}; {len(outside)} points outside it")

# the starting pool: the usual degree filter
P = list(G) + outside
E = edges(P)
adjc = collections.Counter()
inG = set(range(len(G)))
for u, v in E:
    if (u in inG) != (v in inG):
        adjc[v if u in inG else u] += 1
pool = sorted(inG | {i for i in range(len(G), len(P)) if adjc[i] >= a.degree})
log(f"round 0 pool: {len(pool)} points ({len(pool)-len(G)} candidates at degree >= {a.degree})")

for rnd in range(1, a.rounds + 1):
    P2, E2 = induced(P, E, pool)
    start = [pool.index(i) for i in range(len(G))]
    n2 = len(P2)
    # collect colourings of the pool that the oracle actually produces
    o = Oracle(n2, E2)
    ext = Extender(n2, E2, iters=6000, seed=a.seed + rnd)
    cols = []
    import random
    rng = random.Random(a.seed + rnd)
    for _ in range(a.colourings):
        o.C.solver.set_phases([rng.choice((1, -1)) * (4 * v + c + 1)
                               for v in range(n2) for c in range(4)])
        sub = sorted(rng.sample(start, max(8, int(len(start) * 0.97))))
        if o.colourable(sub):
            cols.append(ext.extend(o.model(sub), sub))
    o.close()
    if not cols:
        log(f"round {rnd}: the pool admits no 4-colouring of a 97% sample, nothing to learn")
        break
    # score every lattice point outside the pool by how many colourings it kills
    poolset = set(pool)
    idxP = {P[i].key(): i for i in range(len(P))}
    adj = collections.defaultdict(list)
    for u, v in E:
        adj[u].append(v)
        adj[v].append(u)
    back = {i: k for k, i in enumerate(pool)}
    score = collections.Counter()
    for i in range(len(P)):
        if i in poolset:
            continue
        nb = [back[u] for u in adj[i] if u in back]
        if len(nb) < 4:
            continue
        for c in cols:
            if len({c[u] for u in nb if c[u] >= 0}) == 4:
                score[i] += 1
    if not score:
        log(f"round {rnd}: no outside point kills any of the {len(cols)} colourings")
        break
    top = [i for i, _ in score.most_common(a.add)]
    log(f"round {rnd}: {len(cols)} colourings learned; best outside point kills "
        f"{score[top[0]]} of them; adding {len(top)} points "
        f"(scores {score[top[0]]} down to {score[top[-1]]})")
    pool = sorted(set(pool) | set(top))
    P2, E2 = induced(P, E, pool)
    save_points(f"{OUT}/colgen_r{rnd}.pts", P2)
    save_edges(f"{OUT}/colgen_r{rnd}.edge", len(P2), E2)
    log(f"  pool is now {len(pool)} points; saved out/colgen_r{rnd}.pts")
log("done; attack the generated pools with scripts/pool_attack.py")
