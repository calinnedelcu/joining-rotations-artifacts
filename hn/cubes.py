"""Cube and conquer for 4-colourability.

Direct CDCL stops working on the heptagonal lattice long before it stops working
on the classical one: 3025 points take 200 s and 7057 burn a hundred minutes
without deciding, where the classical union answers in 19 to 76 seconds at four to
nine times the size.  That is not this code -- Haugland's own 2131-vertex
refutation timed out under kissat and CaDiCaL on all 22 direct attempts, and his
certificates came from splitting it into 14786 cubes that each solved in under 9
seconds.

Pin a triangle to colours 0,1,2, pick the highest-degree vertices as splitters, and
enumerate their colourings.  A cube whose splitters already clash along an edge is
dropped without a solve.  Each worker builds the formula once and solves its share
incrementally, so learned clauses carry from cube to cube.
"""
from __future__ import annotations
import collections, itertools, time
import multiprocessing as mp

_G = {}


def _setup(n, edges, tri):
    from .sat import Colouring
    c = Colouring(n, edges, k=4, selectors=False)
    if tri:
        c.break_colour_symmetry(list(tri))
    _G["c"] = c
    _G["split"] = None


def _worker(args):
    cube, split = args
    c = _G["c"]
    return cube, c.solver.solve(assumptions=[c.var(v, col)
                                             for v, col in zip(split, cube)])


def cube_colourable(n, edges, split=6, procs=8, log=print):
    """True if 4-colourable, False if not.  Equivalent to `not verify(...)`."""
    from .sat import find_triangle
    tri = find_triangle(n, edges)
    adj = collections.defaultdict(set)
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    fixed = set(tri or ())
    order = sorted((v for v in range(n) if v not in fixed), key=lambda v: -len(adj[v]))
    sp = order[:split]
    cubes = []
    for combo in itertools.product(range(4), repeat=len(sp)):
        if all(not (combo[i] == combo[j] and sp[j] in adj[sp[i]])
               for i in range(len(sp)) for j in range(i + 1, len(sp))):
            cubes.append((combo, sp))
    log(f"  cube and conquer: {len(sp)} splitters, {len(cubes)} cubes of {4**len(sp)}")
    t = time.time()
    done = 0
    # spawn (the macOS default) re-imports the calling module in every worker, so a
    # script that builds its graph at module level rebuilds it once per core and then
    # exits.  fork inherits the already-built data instead.
    ctx = mp.get_context("fork")
    with ctx.Pool(processes=procs, initializer=_setup,
                  initargs=(n, edges, tri)) as pool:
        for cube, sat in pool.imap_unordered(_worker, cubes, chunksize=4):
            done += 1
            if sat:
                log(f"  cube {cube} satisfiable after {done} cubes ({time.time()-t:.0f}s)")
                pool.terminate()
                return True
            if done % max(1, len(cubes) // 8) == 0:
                log(f"  {done}/{len(cubes)} cubes refuted ({time.time()-t:.0f}s)")
    log(f"  all {len(cubes)} cubes refuted ({time.time()-t:.0f}s)")
    return False
