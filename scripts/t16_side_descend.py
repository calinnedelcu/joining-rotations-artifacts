#!/usr/bin/env python3
"""Shrink ONE side of the theta_16 graph, with the other side held fixed.

Usage: t16_side_descend.py GRAPH.pts L|S [--seed N] [--rounds 800]

The current graph is 1408 + 1901 with 32 connection edges.  The record's profile
is 374 + 136 with 18 -- its rotated side is the small one, because that side is
only an exploiter: it has to defeat the colourings the forcer allows, and nothing
more.  Here the rotated side is the *bigger* half, which says the descent has not
touched it: global sampling removes points wherever it happens to look.

So sample within one side only and let the UNSAT core throw away what that side
does not need.  Same cost per proof as global sampling, all of it spent where the
slack is.
"""
import os, sys, time, random, argparse, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.field import set_primes
set_primes((3, 7, 11))
import hn.construct as C
C.refresh_field()
from hn.construct import edges, split_parts
from hn.io import load_points, save_points, save_edges
from hn.graph import induced
from hn.minimise import verify
from hn.hitting import Oracle, kcore
from hn.sat import find_triangle

OUT = os.path.join(os.path.dirname(__file__), "..", "out")
ap = argparse.ArgumentParser()
ap.add_argument("graph")
ap.add_argument("side", choices=["L", "S"])
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--rounds", type=int, default=800)
ap.add_argument("--fracs", default="0.9,0.95,0.99,0.85,0.97,0.995,0.92,0.98,0.9,0.99")
a = ap.parse_args()
log = lambda s: print(f"[{time.strftime('%H:%M:%S')}] {s}", flush=True)

P = load_points(a.graph)
E = edges(P)
Lidx, Sidx = split_parts(P)
free = list(Lidx if a.side == "L" else Sidx)
fixed = list(Sidx if a.side == "L" else Lidx)
tri = find_triangle(len(P), E)
log(f"{os.path.basename(a.graph)}: {len(P)} points; shrinking the "
    f"{'forcer' if a.side == 'L' else 'rotated'} side ({len(free)}) with the other "
    f"({len(fixed)}) fixed")
assert verify(P, E, sorted(set(free) | set(fixed)), triangle=tri), "not 5-chromatic"

rng = random.Random(a.seed)
fracs = [float(x) for x in a.fracs.split(",")]
fi = stall = 0
t0 = time.time()
best = len(free) + len(fixed)
for it in range(a.rounds):
    f = fracs[fi]
    k = max(4, int(len(free) * f))
    sub = free if k >= len(free) else rng.sample(free, k)
    cand = sorted(set(sub) | set(fixed))
    t = tri if tri is not None and set(tri) <= set(cand) else None
    o = Oracle(len(P), E, triangle=t)
    ok = o.colourable(cand)
    if not ok:
        core = sorted(set(o.core()) | set(t or ()))
        o.close()
        alive = set(core) if core else set(cand)
        keep = sorted(alive | set(fixed))
        e2 = [(x, y) for x, y in E if x in set(keep) and y in set(keep)]
        keep = sorted(set(keep) & set(kcore(len(P), e2, 4)))
        nf = [v for v in keep if v in set(free)]
        if len(nf) < len(free):
            free = nf
            fixed = [v for v in keep if v not in set(free)]
            stall = 0
            tot = len(free) + len(fixed)
            if tot < best:
                best = tot
                Q, F = induced(P, E, sorted(keep))
                save_points(f"{OUT}/t16sd{a.side}_{a.seed}.pts", Q)
                save_edges(f"{OUT}/t16sd{a.side}_{a.seed}.edge", len(Q), F)
            log(f"  {f:.3f}: side -> {len(free)}, total {tot}  ({time.time()-t0:.0f}s)"
                + ("   <<<<< BELOW THE 509 RECORD" if tot < 509 else ""))
            continue
    else:
        o.close()
    stall += 1
    if stall >= 4:
        stall = 0
        fi = (fi + 1) % len(fracs)
keep = sorted(set(free) | set(fixed))
assert verify(P, E, keep, triangle=tri), "the reduced graph is not 5-chromatic"
Q, F = induced(P, E, keep)
save_points(f"{OUT}/t16sd{a.side}_{a.seed}.pts", Q)
save_edges(f"{OUT}/t16sd{a.side}_{a.seed}.edge", len(Q), F)
log(f"settled: side {len(free)}, total {len(Q)} vertices, {len(F)} edges"
    + ("   <<<<< BELOW THE 509 RECORD" if len(Q) < 509 else ""))
