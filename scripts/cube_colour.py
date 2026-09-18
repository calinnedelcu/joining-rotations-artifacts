#!/usr/bin/env python3
"""Cube and conquer for 4-colourability, because direct CDCL stops working here.

Usage: cube_colour.py POINTS.pts [--field ...] [--cyclo 420] [--split 6] [--procs 10]

The classical union answers in 19 to 76 seconds at 4525 to 29113 points.  The
heptagonal union of Haugland's lattice does not: 3025 points take 200 s, 3109 take
251 s, and 7057 burned a hundred minutes of CPU without deciding.  That is not a
quirk of this code -- Haugland's own 2131-vertex refutation timed out under kissat
and CaDiCaL on all 22 direct attempts at 30 minutes, and his certificates were
produced by splitting the instance into 14786 cubes, each of which then solved in
under 9 seconds.

Same idea here, in-process.  Pin a triangle to colours 0,1,2, pick `split`
high-degree vertices, and enumerate their colourings as cubes.  A cube that already
conflicts along an edge between two split vertices is dropped without a solve.  Each
worker builds the formula once and solves its share incrementally, so the learned
clauses carry from cube to cube.

  every cube UNSAT  ->  not 4-colourable, so the graph is 5-chromatic
  any cube SAT      ->  4-colourable, and the model is a witness
"""
import os, sys, time, argparse, collections, itertools
from multiprocessing import Pool
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

ap = argparse.ArgumentParser()
ap.add_argument("points")
ap.add_argument("--field", default="3,5,11")
ap.add_argument("--cyclo", type=int, default=0, help="read as Q(zeta_n) instead")
ap.add_argument("--split", type=int, default=6)
ap.add_argument("--procs", type=int, default=10)
ap.add_argument("--solver", default="cadical153")
a = ap.parse_args()


def load():
    if a.cyclo:
        import hn.cyclo as C
        C.set_conductor(a.cyclo)
        from hn.cyclo import edges as cedges
        from hn.cyclo import Cyc
        pts = []
        with open(a.points) as f:
            for line in f:
                parts = line.split()
                n = tuple(int(x) for x in parts[:-1])
                pts.append(Cyc(list(n), int(parts[-1])))
        return len(pts), cedges(pts)
    from hn.field import set_primes
    set_primes(tuple(int(x) for x in a.field.split(",")))
    import hn.construct as C
    C.refresh_field()
    from hn.io import load_points, load_vtx
    from hn.construct import edges
    P = load_vtx(a.points) if a.points.endswith(".vtx") else load_points(a.points)
    return len(P), edges(P)


N, E = load()
from hn.sat import find_triangle
tri = find_triangle(N, E)
adj = collections.defaultdict(set)
for u, v in E:
    adj[u].add(v)
    adj[v].add(u)
print(f"{os.path.basename(a.points)}: {N} points, {len(E)} edges, triangle {tri}", flush=True)

fixed = list(tri) if tri else []
order = sorted((v for v in range(N) if v not in set(fixed)),
               key=lambda v: -len(adj[v]))
split = order[:a.split]
cubes = []
for combo in itertools.product(range(4), repeat=len(split)):
    ok = True
    for i in range(len(split)):
        for j in range(i + 1, len(split)):
            if combo[i] == combo[j] and split[j] in adj[split[i]]:
                ok = False
                break
        if not ok:
            break
    if ok:
        cubes.append(combo)
print(f"splitting on {len(split)} vertices of degree "
      f"{[len(adj[v]) for v in split]} -> {len(cubes)} cubes "
      f"(of {4**len(split)}, the rest conflict on an edge)", flush=True)

_G = {}


def setup():
    from hn.sat import Colouring
    c = Colouring(N, E, k=4, selectors=False)
    if tri:
        c.break_colour_symmetry(list(tri))
    _G["c"] = c


def run(cube):
    c = _G["c"]
    asm = [c.var(v, col) for v, col in zip(split, cube)]
    return cube, c.solver.solve(assumptions=asm)


if __name__ == "__main__":
    t = time.time()
    done = 0
    with Pool(processes=a.procs, initializer=setup) as pool:
        for cube, sat in pool.imap_unordered(run, cubes, chunksize=4):
            done += 1
            if sat:
                print(f"  cube {cube} is SATISFIABLE after {done} cubes "
                      f"({time.time()-t:.0f}s)", flush=True)
                print(f"RESULT: 4-colourable", flush=True)
                pool.terminate()
                sys.exit(0)
            if done % max(1, len(cubes) // 20) == 0:
                print(f"  {done}/{len(cubes)} cubes refuted  ({time.time()-t:.0f}s)",
                      flush=True)
    print(f"RESULT: every one of {len(cubes)} cubes is UNSAT -> NOT 4-colourable, "
          f"the graph is 5-chromatic  ({time.time()-t:.0f}s)", flush=True)
