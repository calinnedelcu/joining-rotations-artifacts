#!/usr/bin/env python3
"""Parts' engine: expansion and reduction around an accumulative graph.

Usage: parts_engine.py GRAPH [--field 3,5,11] [--rot theta4] [--portion 150]
                       [--seeds 3] [--iters 40] [--degree 4]

This repository proves optimality well and searches badly, and searching is what
holds the record.  Parts' method paper (arXiv 2010.12665, docs/ATTEMPTS.md route
45) says why.  Three pieces are missing here, and this adds them:

**Minimization, not reduction.**  Reduction takes a subgraph of what you already
have, so it can never leave the basin of the graph you started from.  Parts insists
the procedure "should not depend heavily on the choice of initial graph and should
include the addition of new vertices to escape local minima".  So each iteration
EXPANDS before it reduces.

**The accumulative graph.**  The carrier of progress is not the best graph found
but the *union of every minimal graph found*.  Two different minimal graphs of the
same size disagree about which vertices to keep; their union lets the next
reduction mix them and reach something neither could.  Without it every iteration
restarts in the same basin -- which is exactly what every search in this repository
did for four days.

**A reserve ordered by degree.**  New points are not arbitrary: a lattice point
earns its place by the number of neighbours it would have in the accumulative
graph, and Parts adds them in order of decreasing degree.

The loop, then:

    A  <- the start graph
    repeat:
        W  <- A + the top `portion` reserve points by degree against A
        {M} <- several minimal subgraphs of W, from independent random descents
        A  <- union of {M}                 (it grows, deliberately)
        keep the smallest M ever seen

His caution applies: "The maximum number of redundant vertices or orbits ... is
usually limited to several tens", so `portion` is a compromise between what the
reduction can chew and how far the expansion can reach.
"""
import os, sys, time, argparse, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import hn.field as F
from hn.field import set_primes, K

ap = argparse.ArgumentParser()
ap.add_argument("graph")
ap.add_argument("--field", default="3,5,11")
ap.add_argument("--rot", default="theta4", help="theta4, theta3, or i:N for the spindle theta_N")
ap.add_argument("--portion", type=int, default=150, help="new points added per iteration")
ap.add_argument("--seeds", type=int, default=3, help="independent descents per iteration")
ap.add_argument("--iters", type=int, default=40)
ap.add_argument("--degree", type=int, default=4)
ap.add_argument("--depth", type=int, default=4)
ap.add_argument("--radius", type=float, default=2.53)
ap.add_argument("--minimal", default=None,
                help="the known MINIMAL graph, which sets the bound.  GRAPH is then the "
                     "accumulative graph -- the pool to search in.  Parts keeps the two "
                     "roles apart and so must this: with the accumulative graph setting "
                     "the bound, the engine hunts for anything under 412 instead of "
                     "anything under 374, which is no search at all")
ap.add_argument("--companion", default=None,
                help="a part held fixed as Parts' 'companion graph C': for an L-graph "
                     "it is an S-graph and vice versa.  His table reports a set of "
                     "minimal graphs and an accumulative graph only for the PARTS "
                     "(1092 minimal 374-vertex L-graphs whose union is 412), never for "
                     "the whole graph -- so this is where the engine has room")
ap.add_argument("--companion-side", default="S", choices=["L", "S"],
                help="S: the companion is rotated by the joining rotation (searching L)")
ap.add_argument("--tag", default=None)
ap.add_argument("--time", type=float, default=600.0, help="seconds per exact reduction")
ap.add_argument("--grow-time", type=float, default=330.0, dest="grow_time",
                help="seconds per grow-set search.  Measured: an alternative minimal "
                     "374-vertex L-graph containing a given new point takes about 280 s "
                     "to find, so anything under that silently reports no alternative")
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--grow-set", type=int, default=4, dest="grow_set",
                help="when nothing beats the bound, force this many new points in one "
                     "at a time and look for an ALTERNATIVE minimal graph of the same "
                     "size.  Parts counts that as a successful iteration too: it is "
                     "what makes the accumulative graph grow, and his set of minimal "
                     "374-vertex L-subgraphs has 1092 members whose union is only 412")
ap.add_argument("--jitter", type=int, default=3,
                help="take the portion from the top `jitter * portion` of the reserve at "
                     "random, so successive iterations see different working graphs")
a = ap.parse_args()
set_primes(tuple(int(x) for x in a.field.split(",")))
import hn.construct as C
C.refresh_field()
from hn.construct import unit_vector_family, ball, dedup, edges, rotate, ROT
from hn.io import load_points, load_vtx, save_points, save_edges
from hn.graph import induced
from hn.minimise import verify
from hn.fastshrink import sample_descend, batch_delete
from hn.hitting import search
import random
from hn.sat import find_triangle

OUT = os.path.join(os.path.dirname(__file__), "..", "out")
tag = a.tag or f"pe_{os.path.basename(a.graph).split('.')[0]}"
log = lambda s: print(f"[{time.strftime('%H:%M:%S')}] {s}", flush=True)


def spindle(i):
    import math
    m = 4 * i - 1
    for s in F.squarefree_divisors():
        if m % s == 0 and math.isqrt(m // s) ** 2 == m // s:
            return (K.rat(2 * i - 1, 2 * i), K.root(s) * K.rat(math.isqrt(m // s), 2 * i))
    return None


cs = spindle(int(a.rot.split(":")[1])) if a.rot.startswith("i:") else ROT[a.rot]
G = load_vtx(a.graph) if a.graph.endswith(".vtx") else load_points(a.graph)
W30 = unit_vector_family(2)
B0 = ball(W30, a.depth, a.radius)
LAT = dedup(B0 + [rotate(p, cs) for p in B0])
log(f"{os.path.basename(a.graph)}: start {len(G)} vertices; ambient lattice {len(LAT)} "
    f"points (depth {a.depth}, radius {a.radius}, rotation {a.rot})")

COMP = []
if a.companion:
    Cg = load_vtx(a.companion) if a.companion.endswith(".vtx") else load_points(a.companion)
    COMP = [rotate(q, cs) for q in Cg] if a.companion_side == "S" else list(Cg)
    log(f"companion: {len(COMP)} vertices held fixed"
        f"{' (rotated)' if a.companion_side == 'S' else ''}")

A = list(G)
if a.minimal:
    Mg = load_vtx(a.minimal) if a.minimal.endswith(".vtx") else load_points(a.minimal)
    if a.companion and a.companion_side == "L":
        Mg = [rotate(q, cs) for q in Mg]          # an S part only meets L once rotated
    best = list(Mg)
    best_n = len(Mg)
    ak = {p.key() for p in A}
    A = A + [p for p in best if p.key() not in ak]
    log(f"minimal graph {best_n} vertices sets the bound; accumulative graph {len(A)}")
else:
    best = list(G)
    best_n = len(G)                 # the bound starts at the graph we were given
for it in range(a.iters):
    # ---- expansion: the reserve, ordered by the degree a point would gain ----
    ak = {p.key() for p in A}
    P = list(A) + [p for p in LAT if p.key() not in ak]
    E = edges(P)
    inA = set(range(len(A)))
    deg = collections.Counter()
    for u, v in E:
        if (u in inA) != (v in inA):
            deg[v if u in inA else u] += 1
    reserve = sorted((i for i in range(len(A), len(P)) if deg[i] >= a.degree),
                     key=lambda i: -deg[i])
    rng = random.Random(it * 7919 + a.seed)
    pool_top = reserve[:max(a.portion, a.portion * a.jitter)]
    take = sorted(rng.sample(pool_top, min(a.portion, len(pool_top)))) if pool_top else []
    order = sorted(inA | set(take))
    W = [P[i] for i in order]
    nfree = len(W)
    if COMP:
        wk = {q.key() for q in W}
        W = W + [q for q in COMP if q.key() not in wk]
    # `take` indexes P; everything below indexes W.  Mixing them fixed the wrong
    # vertex in the grow-set search and crashed induced() once an index ran past
    # the end of W.
    wmap = {pi: wi for wi, pi in enumerate(order)}
    take_w = [wmap[i] for i in take]
    EW = edges(W)
    triW = find_triangle(len(W), EW)
    comp_idx = list(range(nfree, len(W)))
    if not verify(W, EW, triangle=triW):
        log(f"iter {it}: working graph is not 5-chromatic -- stopping")
        break
    log(f"iter {it}: A {len(A)} + {len(take)} reserve points (best degree "
        f"{deg[take[0]] if take else 0}) -> W {len(W)}")

    # ---- reduction: EXACT, bounded by the best so far ----
    # Greedy descent from W lands at 517 and 526 when 509 is sitting inside it:
    # random deletion order picks a worse minimal graph and cannot see the better
    # one.  Parts' reduction is not greedy either -- he checks subgraphs "whose
    # order does not exceed the order of the minimum graph M found at the previous
    # iteration", which is an exact search with a cardinality bound.  That is this
    # repository's master, and on a working graph of A plus a small portion the
    # answer sits at about 90% of the pool, the density where it converges.
    idx = {p.key(): i for i, p in enumerate(W)}
    st = sorted(idx[p.key()] for p in (best or A) if p.key() in idx)
    st = [v for v in st if v < nfree]
    if not verify(W, EW, sorted(set(st) | set(comp_idx)), triangle=triW):
        st = list(range(nfree))
    found = []

    def keep_it(S):
        found.append(sorted(S))

    res, proven = search(W, EW, start=st, bound=best_n - 1, time_limit=a.time,
                         cuts_per_iter=2, seed=it * 97 + a.seed, log=lambda _: None,
                         on_improve=keep_it, fixed=comp_idx, grow_every=2,
                         bootstrap_pairs=0, bootstrap_essential=False,
                         bootstrap_critical=False)
    if res is not None:
        found.append(sorted(res))
    # the start graph itself arrives through on_improve; only a genuine improvement
    # counts here, or the grow-set branch below never runs and A never grows
    Ms = [M for M in found if len(M) < best_n and verify(W, EW, M, triangle=triW)]
    # A timeout and a proof both used to print "0 graph(s) under N", so a run that
    # never finished a single reduction read exactly like a run that proved every
    # window clean.  Measured afterwards: at the part level, where Parts actually
    # points his engine, 1 of 13 iterations had proved anything.
    log(f"   exact reduction: {len(Ms)} graph(s) under {best_n} -- "
        + ("PROVEN minimum over this working graph" if proven
           else f"TIMEOUT after {a.time:.0f}s, nothing concluded"))
    if Ms:
        m = min(Ms, key=len)
        if len(m) < best_n:
            best_n = len(m)
            Q, Fe = induced(W, EW, m)
            best = Q
            save_points(f"{OUT}/{tag}.pts", Q)
            save_edges(f"{OUT}/{tag}.edge", len(Q), Fe)
            log(f"   NEW BEST {len(Q)} vertices, {len(Fe)} edges"
                + ("   <<<<< BELOW THE 509 RECORD" if len(Q) < 509 else ""))
        union = sorted({v for M in Ms for v in M} | set(st))
        A = [W[i] for i in union]
        log(f"   accumulative graph: {len(A)} vertices from {len(Ms)} minimal graph(s) "
            f"(sizes {sorted(len(M) for M in Ms)[:6]})")
    else:
        # Nothing beats the bound here.  Parts' iteration still succeeds if it
        # ENLARGES the set of minimal graphs, so look for an alternative graph of
        # the same size that uses a new point: force one in and ask for |best|.
        grown = []
        for p in take_w[:a.grow_set]:
            alt = []
            # search() returns the FREE part, excluding the fixed vertex, so the
            # graph is M + {p} and the bound on M must be one lower -- otherwise the
            # "alternatives" are one vertex bigger than the best and A grows with junk
            r2, _ = search(W, EW, start=st, bound=best_n - 1, time_limit=a.grow_time,
                           cuts_per_iter=2, seed=it * 131 + p, log=lambda _: None,
                           on_improve=lambda S: alt.append(sorted(S)),
                           fixed=comp_idx + [p], grow_every=2, bootstrap_pairs=0,
                           bootstrap_essential=False, bootstrap_critical=False)
            if r2 is not None:
                alt.append(sorted(r2))
            for M in alt:
                if len(set(M) | {p}) <= best_n and verify(W, EW, sorted(set(M) | {p}), triangle=triW):
                    grown.append(sorted(set(M) | {p}))
                    break
        if grown:
            union = sorted({v for M in grown for v in M} | set(st))
            A = [W[i] for i in union]
            log(f"   no improvement, but {len(grown)} alternative minimal graph(s) "
                f"of size {[len(M) for M in grown]} -> accumulative graph {len(A)}")
        else:
            log(f"   nothing under {best_n} here, and no alternative of that size; "
                f"expanding elsewhere")
log(f"done: best {best_n} vertices")
