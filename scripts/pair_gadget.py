#!/usr/bin/env python3
"""Price the partner gadget Parts never priced.

Usage: pair_gadget.py --pair NAME --mode mono|nonmono --bound N [--radius 2.0]

A graph forcing a pair (u, v) monochromatic, glued to one forcing the same pair
non-monochromatic, is 5-chromatic on |A| + |B| - 2 vertices.  Parts' inventory
prices one side per distance and never the other:

    distance     he has                 budget for the partner to beat 509
    8/3          mono-pair 367          non-mono <= 143
    7/3          non-mono-pair 319      mono     <= 191
    5/3          non-mono-pair 315      mono     <= 195
    sqrt(11/3)   non-mono-pair 308      mono     <= 202
    2            374 and 136 -- the record itself

scripts/screen_pairs.py established that the lattice forces both ways at every
one of those distances, so each partner exists and the only question is its size.
At distance 2 the two sides cost 374 and 136, wildly lopsided, and a cheap
partner is exactly what the other distances might be hiding.

Both questions are non-4-colourability, so the master runs unchanged: forcing
monochromatic is the graph plus a virtual edge (u, v); forcing non-monochromatic
is the graph with v contracted into u, and the gadget is then the answer plus v.
"""
import os, sys, time, argparse, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.field import K, Pt
from hn.construct import unit_vector_family, ball, dedup, edges, rotate, ROT, to_float
from hn.io import save_points, save_edges
from hn.graph import induced
from hn.hitting import search
from hn.minimise import verify, propose_core
from hn.fastshrink import sample_descend, batch_delete
from hn.sat import find_triangle

OUT = os.path.join(os.path.dirname(__file__), "..", "out")
r11, r3 = K.root(11), K.root(3)
r12 = r3 * K.rat(2)
PAIRS = {
    "8_3":  (Pt(K.rat(-4, 3), K.zero()), Pt(K.rat(4, 3), K.zero())),
    "7_3":  (Pt(K.rat(-7, 6), r11 * K.rat(1, 6)), Pt(K.rat(7, 6), r11 * K.rat(1, 6))),
    "5_3":  (Pt(K.rat(-5, 6), r11 * K.rat(1, 6)), Pt(K.rat(5, 6), r11 * K.rat(1, 6))),
    "r11r3": (Pt(-r11 / r12, K.rat(1) / r12), Pt(r11 / r12, K.rat(1) / r12)),
    "2":    (Pt(K.rat(-1), K.zero()), Pt(K.rat(1), K.zero())),
}
ap = argparse.ArgumentParser()
ap.add_argument("--pair", required=True, choices=sorted(PAIRS))
ap.add_argument("--mode", required=True, choices=["mono", "nonmono"])
ap.add_argument("--bound", type=int, required=True)
ap.add_argument("--radius", type=float, default=2.0)
ap.add_argument("--depth", type=int, default=4)
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--time", type=float, default=None)
ap.add_argument("--exact", action="store_true",
                help="after the greedy descent, run the exact master one below it")
a = ap.parse_args()
log = lambda s: print(s, flush=True)

u, v = PAIRS[a.pair]
W = unit_vector_family(2)
B = ball(W, a.depth, a.radius)
P = dedup(B + [rotate(p, ROT["theta4"]) for p in B]
          + [rotate(p, ROT["theta3"]) for p in B])
E = edges(P)
idx = {p.key(): i for i, p in enumerate(P)}
iu, iv = idx[u.key()], idx[v.key()]
log(f"pair {a.pair} at distance {to_float((u-v).norm2())**0.5:.4f}, mode {a.mode}; "
    f"pool {len(P)} points, {len(E)} edges")

if a.mode == "mono":
    EE = sorted(set(E) | {(min(iu, iv), max(iu, iv))})
    PP, fixed, offset = P, [iu, iv], 0
    back = list(range(len(P)))
else:
    merged = set()
    for x, y in E:
        x = iu if x == iv else x
        y = iu if y == iv else y
        if x != y:
            merged.add((min(x, y), max(x, y)))
    back = [i for i in range(len(P)) if i != iv]
    PP, EE = induced(P, sorted(merged), back)
    fixed = [back.index(iu)]
    offset = 1                      # the contracted twin is part of the gadget
tri = find_triangle(len(PP), EE)
t = time.time()
assert verify(PP, EE, triangle=tri), "the pool does not force this pair; nothing to minimise"
log(f"the whole pool forces it, verified in {time.time()-t:.0f}s; "
    f"looking for at most {a.bound - offset} vertices (+{offset}) against bound {a.bound}")


def save(best):
    keep = sorted(set(best) | set(fixed))
    orig = sorted({back[i] for i in keep} | {iu, iv})
    Q, F = induced(P, E, orig)
    tag = f"pg_{a.pair}_{a.mode}_{a.seed}"
    save_points(f"{OUT}/{tag}.pts", Q)
    save_edges(f"{OUT}/{tag}.edge", len(Q), F)
    log(f"  gadget now {len(Q)} vertices, {len(F)} edges -> glued total would be "
        f"{len(Q) + {'8_3': 367, '7_3': 319, '5_3': 315, 'r11r3': 308, '2': 136}[a.pair] - 2}"
        + ("   <<< BELOW THE 509 RECORD"
           if len(Q) + {'8_3': 367, '7_3': 319, '5_3': 315, 'r11r3': 308, '2': 136}[a.pair] - 2 < 509
           else ""))


# Starting the master from the whole pool means starting from nothing: with
# 15599 free choices and a bound of 191 its first proposal is the empty set, and
# it has to discover a gadget from scratch.  So extract an UNSAT core first --
# one refutation names a subset that already forces the pair -- iterate that to a
# fixed point, then descend greedily.  Only then is the exact master worth running.
OTHER = {"8_3": 367, "7_3": 319, "5_3": 315, "r11r3": 308, "2": 136}[a.pair]
keep = list(range(len(PP)))
for it in range(12):
    t = time.time()
    c = propose_core(PP, EE, keep, protect=fixed)
    assert c is not None, "the set stopped forcing the pair"
    if len(c) >= len(keep):
        log(f"  core {it}: {len(c)} vertices, no smaller  ({time.time()-t:.0f}s)")
        break
    keep = c
    log(f"  core {it}: {len(keep)} vertices  ({time.time()-t:.0f}s)")
log(f"after core extraction: {len(keep)} vertices (+{offset}) -> "
    f"glued total {len(keep)+offset+OTHER-2}")
keep = sample_descend(PP, EE, keep, seed=a.seed, log=log)
log(f"after sampling: {len(keep)} (+{offset}) -> glued total {len(keep)+offset+OTHER-2}")
keep = batch_delete(PP, EE, keep, seed=a.seed, log=log)
assert verify(PP, EE, keep, triangle=None), "the reduced gadget stopped forcing the pair"
log(f"MINIMAL gadget: {len(keep)+offset} vertices")
save(keep)

if a.exact and len(keep) + offset - 1 > 2:
    log(f"exact master over the same pool, bound {len(keep)+offset-1}")
    best, proven = search(PP, EE, start=keep, bound=len(keep) - 1, time_limit=a.time,
                          cuts_per_iter=2, seed=a.seed, log=log, on_improve=save,
                          fixed=fixed, grow_every=2, bootstrap_pairs=0,
                          bootstrap_essential=False, bootstrap_critical=False)
    if best is not None:
        save(best)
        log(f"best {len(best)+offset} vertices; proven minimum over this pool: {proven}")
