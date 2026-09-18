"""Fast reduction of a large pool to a minimal 5-chromatic subgraph.

`minimise.shrink` re-verifies every candidate in a fresh solver, which is the
right default but costs a full solver launch per test.  On a 2600-vertex pool
that is hours.  Here the PROPOSING is done by one persistent oracle under
selector assumptions, and only the final graph is re-verified from scratch, in
a fresh solver with no assumptions.  That is sound for the same reason the
hitting-set loop is: the oracle only ever suggests, and the answer is checked.

Two accelerations beyond the persistent solver, both from Parts:

  * iterate core extraction and 4-core pruning to a fixed point first.  A
    vertex of degree below 4 cannot be in a vertex-critical 5-chromatic graph,
    so dropping it is sound, and dropping it can expose others.
  * delete in BATCHES.  Try removing eight vertices at once; if the graph
    survives, eight tests became one.  If not, split into fours, then pairs,
    then singles.  Parts calls this 8-4-2-1.
"""
from __future__ import annotations
import random
import time
from .hitting import Oracle, kcore
from .minimise import verify
from .sat import find_triangle


def reduce_pool(points, edges, log=print, tries=60, seed=0):
    """Randomised UNSAT-core extraction with 4-core pruning, to a fixed point.

    One core extraction cuts hundreds of vertices in a single solve, which is
    worth thousands of one-at-a-time deletions.  The catch is that a solver
    asked the same question twice returns the same core, so the plain loop
    stalls almost immediately.  Randomising the phase before each solve makes
    it find a different proof and therefore a different core, which is exactly
    Heule's clause-shuffling trick in a cheaper form.  Keep the smallest core
    seen and keep going until several tries in a row fail to improve.
    """
    rng = random.Random(seed)
    keep = list(range(len(points)))
    tri = find_triangle(len(points), edges)
    stall = 0
    while stall < tries:
        n0 = len(keep)
        t = tri if tri is not None and set(tri) <= set(keep) else None
        o = Oracle(len(points), edges, triangle=t)
        o.C.solver.set_phases([rng.choice((1, -1)) * (4 * v + c + 1)
                               for v in range(len(points)) for c in range(4)])
        if o.colourable(keep):
            o.close()
            raise AssertionError("the pool is 4-colourable")
        core = sorted(set(o.core()) | set(t or ()))
        o.close()
        cand = [v for v in keep if v in set(core)] if core else keep
        sub = set(cand)
        e2 = [(a, b) for a, b in edges if a in sub and b in sub]
        cand = sorted(sub & set(kcore(len(points), e2, 4)))
        if len(cand) < n0:
            keep = cand
            stall = 0
            log(f"  reduce: {n0} -> {len(keep)}")
        else:
            stall += 1
    log(f"  reduce settled at {len(keep)}")
    return keep


def sample_descend(points, edges, keep, seed=0, log=print, rounds=600,
                   fracs=(1.0, 0.995, 0.99, 0.98, 0.96, 0.93, 0.88, 0.8)):
    """Drop a random slice, and if the graph survives, keep only its core.

    Deleting one vertex at a time is expensive in exactly the case that
    succeeds: the graph is still 5-chromatic, so the solver must produce a full
    UNSAT proof, and on a 2600-vertex pool that is twenty seconds for one
    vertex.  Asking instead whether a random 80 percent of the pool is still
    5-chromatic costs the same one proof and, when the answer is yes, its UNSAT
    core throws away hundreds of vertices at once.

    The schedule runs from gentle to aggressive, which is the opposite of the
    obvious order and was chosen after watching it: on a pool already close to
    minimal, dropping thirty percent destroys 5-chromaticity outright, so the
    aggressive slices simply fail and waste a two-minute proof each time.
    """
    rng = random.Random(seed)
    tri = find_triangle(len(points), edges)
    keep = sorted(keep)
    t0 = time.time()
    fi = 0
    stall = 0
    for it in range(rounds):
        f = fracs[fi]
        k = max(8, int(len(keep) * f))
        sub = keep if k >= len(keep) else sorted(rng.sample(keep, k))
        t = tri if tri is not None and set(tri) <= set(sub) else None
        o = Oracle(len(points), edges, triangle=t)
        ok = o.colourable(sub)
        if not ok:
            core = sorted(set(o.core()) | set(t or ()))
            o.close()
            cand = core if core else sub
            s2 = set(cand)
            e2 = [(x, y) for x, y in edges if x in s2 and y in s2]
            cand = sorted(s2 & set(kcore(len(points), e2, 4)))
            if len(cand) < len(keep):
                log(f"  sample {f:.2f}: {len(keep)} -> {len(cand)}  "
                    f"({time.time()-t0:.0f}s)")
                keep = cand
                stall = 0
                continue
        else:
            o.close()
        stall += 1
        if stall >= (3 if f >= 1.0 else 5):
            stall = 0
            fi += 1
            if fi >= len(fracs):
                break
    log(f"  sampling settled at {len(keep)}  ({time.time()-t0:.0f}s)")
    return keep


def batch_delete(points, edges, keep, seed=0, log=print, batch=8):
    """Greedy deletion in 8-4-2-1 batches, proposed by one persistent oracle."""
    rng = random.Random(seed)
    tri = find_triangle(len(points), edges)
    if tri is not None and not set(tri) <= set(keep):
        tri = None
    o = Oracle(len(points), edges, triangle=tri)
    kept = set(keep)
    protected = set(tri or ())
    t0, removed = time.time(), 0

    def survives(s):
        return not o.colourable(sorted(kept - s))

    changed = True
    while changed:
        changed = False
        order = [v for v in kept if v not in protected]
        rng.shuffle(order)
        i = 0
        while i < len(order):
            group = [v for v in order[i:i + batch] if v in kept]
            i += batch
            if not group:
                continue
            stack = [group]
            while stack:
                g = stack.pop()
                g = [v for v in g if v in kept]
                if not g:
                    continue
                if survives(set(g)):
                    kept -= set(g)
                    removed += len(g)
                    changed = True
                elif len(g) > 1:
                    h = len(g) // 2
                    stack.append(g[:h])
                    stack.append(g[h:])
            if removed and removed % 200 < batch:
                log(f"  deleted {removed}, {len(kept)} left, "
                    f"{o.calls} oracle calls, {time.time()-t0:.0f}s")
    o.close()
    return sorted(kept)


def fast_shrink(points, edges, seed=0, log=print):
    """Sample down, then batch-delete, then ONE fresh verification.

    reduce_pool is kept for reference but sample_descend subsumes it: its first
    schedule entry is the whole set, which is exactly a core extraction.
    """
    keep = sample_descend(points, edges, list(range(len(points))),
                          seed=seed, log=log)
    keep = batch_delete(points, edges, keep, seed=seed, log=log)
    assert verify(points, edges, keep, triangle=None), \
        "the reduced graph failed independent verification"
    return keep
