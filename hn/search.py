"""Colouring-guided local search over subsets of a pool.

Deletion alone gets stuck at a vertex-critical graph.  Parts escaped that by
ADDING vertices and deleting again.  Done naively that is |S| * |U - S|
SAT calls per step.  The colourings tell us which additions can possibly
help, and that is the whole trick:

    S - v is 4-colourable (S is critical).  Let c be one of its colourings.
    Adding w to S - v can only restore 5-chromaticity if w cannot be
    coloured under c, i.e. all four colours occur among w's neighbours in
    S - v.  If some sampled colouring of S - v leaves a colour free at w,
    then S - v + w is 4-colourable and the SAT call is not worth making.

So each step: pick v, sample a few colourings of S - v, keep only the w that
are blocked by every sample, and SAT-check S - v + w for those.  A success
is a sideways move to another critical graph of the same size; from there,
try to delete a second vertex.  The persistent solver keeps its learnt
clauses across all of these queries, which is where the speed comes from.

Every improvement is re-verified in a fresh solver before being reported.
"""
from __future__ import annotations
import random
import time
from .sat import find_triangle
from .minimise import verify
from .hitting import Oracle, kcore


def _adjacency(n, edges):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    return adj


def sample_colourings(oracle, S, rng, samples=3):
    """A few different 4-colourings of the (colourable) set S."""
    out = []
    n = oracle.n
    for _ in range(samples):
        oracle.C.solver.set_phases([rng.choice((1, -1)) * (4 * v + c + 1)
                                    for v in range(n) for c in range(4)])
        if not oracle.colourable(S):
            return None
        out.append(oracle.model(S))
    return out


def blocked(adj, col, w, inside):
    """All four colours among w's neighbours that lie in `inside`?"""
    seen = 0
    for u in adj[w]:
        if u in inside and col[u] >= 0:
            seen |= 1 << col[u]
            if seen == 15:
                return True
    return False


def local_search(points, edges, S, time_limit=None, seed=0, samples=3,
                 max_candidates=60, log=print, on_improve=None,
                 solver="cadical195"):
    """Returns the best vertex list found (verified 5-chromatic)."""
    rng = random.Random(seed)
    n = len(points)
    adj = _adjacency(n, edges)
    core = set(kcore(n, edges, 4))
    tri = find_triangle(n, edges)
    if tri is not None and not set(tri) <= core:
        tri = None
    oracle = Oracle(n, edges, triangle=tri, solver=solver)
    t0 = time.time()

    S = set(S) & core
    assert not oracle.colourable(S), "start is not 5-chromatic"

    def descend(S):
        """Delete while 5-chromatic; returns (S, deleted count)."""
        order = list(S)
        rng.shuffle(order)
        removed = 0
        for v in order:
            T = S - {v}
            if not oracle.colourable(T):
                S = T
                removed += 1
        return S, removed

    S, r = descend(S)
    best = sorted(S)
    log(f"start {len(best)} after descent (removed {r})")
    tabu = {}          # vertex -> step until which it may not be re-added
    step = 0
    stats = {"checks": 0, "sideways": 0, "improve": 0}
    while True:
        if time_limit and time.time() - t0 > time_limit:
            break
        step += 1
        v = rng.choice(sorted(S))
        Sv = S - {v}
        cols = sample_colourings(oracle, Sv, rng, samples)
        if cols is None:
            # S - v is still 5-chromatic: free improvement
            S = Sv
            best = sorted(S)
            stats["improve"] += 1
            log(f"[{step}] free deletion -> {len(best)}")
            if on_improve:
                on_improve(best)
            continue
        cand = [w for w in core if w not in S and tabu.get(w, 0) <= step
                and all(blocked(adj, c, w, Sv) for c in cols)]
        rng.shuffle(cand)
        moved = False
        for w in cand[:max_candidates]:
            T = Sv | {w}
            stats["checks"] += 1
            if not oracle.colourable(T):
                # sideways move accepted
                tabu[v] = step + 10
                S = T
                stats["sideways"] += 1
                S, r = descend(S)
                if len(S) < len(best):
                    assert verify(points, edges, sorted(S), triangle=None), "fresh verify failed"
                    best = sorted(S)
                    stats["improve"] += 1
                    log(f"[{step}] *** improved to {len(best)} vertices  "
                        f"(swap {v}->{w}, then deleted {r})  {time.time()-t0:.0f}s")
                    if on_improve:
                        on_improve(best)
                moved = True
                break
        if step % 20 == 0:
            log(f"[{step}] |S|={len(S)} best={len(best)} candidates {len(cand)} "
                f"checks={stats['checks']} sideways={stats['sideways']} "
                f"oracle calls={oracle.calls}  {time.time()-t0:.0f}s")
        if not moved and cand:
            pass
    oracle.close()
    return best
