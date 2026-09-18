#!/usr/bin/env python3
"""Which pair distances can the lattice force, monochromatic or not?

Usage: screen_pairs.py [--radius 2.2] [--depth 4]

A graph forcing a pair (u, v) monochromatic, glued to a graph forcing the same
pair NON-monochromatic, is 5-chromatic and costs |A| + |B| - 2 vertices.  Parts'
inventory gives the minimal gadget for each family only at the distances he
needed, and the two lists never meet:

    mono-pair       367 at 8/3,  421 at 8/sqrt3
    non-mono-pair   214 at 3,  319 at 7/3,  315 at 5/3,  312 at 1/3,  308 at
                    sqrt(11/3)

So each of his gadgets has an unpriced partner, and the budget to beat 509 is
generous where his gadget is cheap: a mono-pair at distance 3 may cost up to 296
and still beat the record against his 214-vertex non-mono-pair.

Before minimising anything, screen: is the forcing even possible in the lattice?
Adding the virtual edge (u, v) tests monochromatic forcing, contracting u and v
tests non-monochromatic forcing, and both are single non-4-colourability calls on
the whole pool.  A pool that cannot force it has no subgraph that can.
"""
import os, sys, time, argparse, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.field import K, Pt
from hn.construct import (unit_vector_family, ball, dedup, edges, rotate, ROT,
                          to_float)
from hn.sat import find_triangle
from hn.minimise import verify
from hn.graph import induced

ap = argparse.ArgumentParser()
ap.add_argument("--radius", type=float, default=2.2)
ap.add_argument("--depth", type=int, default=4)
a = ap.parse_args()
log = lambda s: print(s, flush=True)

r11, r3 = K.root(11), K.root(3)
r12 = r3 * K.rat(2)                                     # sqrt12 = 2 sqrt3
PAIRS = [
    ("8/3   mono-pair 367",    Pt(K.rat(-4, 3), K.zero()),  Pt(K.rat(4, 3), K.zero())),
    ("3     non-mono 214",     Pt(K.rat(-3, 2), K.zero()),  Pt(K.rat(3, 2), K.zero())),
    ("7/3   non-mono 319",     Pt(K.rat(-7, 6), r11 * K.rat(1, 6)),
                               Pt(K.rat(7, 6), r11 * K.rat(1, 6))),
    ("5/3   non-mono 315",     Pt(K.rat(-5, 6), r11 * K.rat(1, 6)),
                               Pt(K.rat(5, 6), r11 * K.rat(1, 6))),
    ("1/3   non-mono 312",     Pt(K.rat(-1, 6), K.zero()),  Pt(K.rat(1, 6), K.zero())),
    ("r11/r3 non-mono 308",    Pt(-r11 / r12, K.rat(1) / r12),
                               Pt(r11 / r12, K.rat(1) / r12)),
    ("2     the record's own", Pt(K.rat(-1), K.zero()),     Pt(K.rat(1), K.zero())),
]

W = unit_vector_family(2)
B = ball(W, a.depth, a.radius)
P = dedup(B + [rotate(p, ROT["theta4"]) for p in B]
          + [rotate(p, ROT["theta3"]) for p in B])
E = edges(P)
idx = {p.key(): i for i, p in enumerate(P)}
log(f"pool: depth {a.depth}, radius {a.radius}, with the theta_4 and theta_3 copies "
    f"-> {len(P)} points, {len(E)} edges")
tri = find_triangle(len(P), E)

for name, u, v in PAIRS:
    iu, iv = idx.get(u.key()), idx.get(v.key())
    d = (to_float((u - v).norm2())) ** 0.5
    if iu is None or iv is None:
        log(f"  {name:24s} distance {d:.4f}: the pair is not in this pool")
        continue
    t = time.time()
    mono = verify(P, sorted(set(E) | {(min(iu, iv), max(iu, iv))}), triangle=tri)
    # contract v into u: every neighbour of v becomes a neighbour of u
    adj = collections.defaultdict(set)
    for x, y in E:
        adj[x].add(y)
        adj[y].add(x)
    E2 = set()
    for x, y in E:
        x = iu if x == iv else x
        y = iu if y == iv else y
        if x != y:
            E2.add((min(x, y), max(x, y)))
    keep = [i for i in range(len(P)) if i != iv]
    P3, E3 = induced(P, sorted(E2), keep)
    tri3 = find_triangle(len(P3), E3)
    nonmono = verify(P3, E3, triangle=tri3)
    log(f"  {name:24s} distance {d:.4f}: pool forces monochromatic {mono}, "
        f"forces non-monochromatic {nonmono}   ({time.time()-t:.0f}s)")
