#!/usr/bin/env python3
"""Continue the theta_16 descent from a saved point set, on an independent path.

Usage: descend_t16.py FILE.pts --seed N

Core extraction is deterministic, so every worker would repeat it.  This picks up
from what it produced and runs sampled descent with its own seed: greedy deletion
reaches a *minimal* graph, not a minimum one, and which minimal graph depends
entirely on the order, so independent paths are the cheapest way to get a better
answer.
"""
import os, sys, time, argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.field import set_primes
set_primes((3, 7, 11))
import hn.construct as C
C.refresh_field()
from hn.construct import edges
from hn.io import load_points, save_points, save_edges
from hn.graph import induced
from hn.minimise import verify
from hn.fastshrink import sample_descend, batch_delete
from hn.sat import find_triangle

OUT = os.path.join(os.path.dirname(__file__), "..", "out")
ap = argparse.ArgumentParser()
ap.add_argument("pts")
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--fracs", default=None,
                help="comma-separated sampling schedule.  At fraction 1.0 the sample "
                     "IS the whole set, so the seed changes nothing and every worker "
                     "repeats the same deterministic work; starting below 1.0 is what "
                     "makes independent paths independent")
a = ap.parse_args()
log = lambda s: print(f"[{time.strftime('%H:%M:%S')}] {s}", flush=True)

P = load_points(a.pts)
E = edges(P)
tri = find_triangle(len(P), E)
log(f"{os.path.basename(a.pts)}: {len(P)} points, {len(E)} edges, seed {a.seed}")
assert verify(P, E, triangle=tri), "this point set is not 5-chromatic"
log("verified 5-chromatic")


def snap(keep, tag):
    Q, F = induced(P, E, sorted(keep))
    save_points(f"{OUT}/t16_d{a.seed}.pts", Q)
    save_edges(f"{OUT}/t16_d{a.seed}.edge", len(Q), F)
    log(f"{tag}: {len(Q)} vertices, {len(F)} edges"
        + ("   <<<<< BELOW THE 509 RECORD" if len(Q) < 509 else ""))
    return Q


kw = {}
if a.fracs:
    kw["fracs"] = tuple(float(x) for x in a.fracs.split(","))
    log(f"schedule {kw['fracs']}")
keep = sample_descend(P, E, list(range(len(P))), seed=a.seed, log=log, **kw)
snap(keep, "after sampling")
keep = batch_delete(P, E, keep, seed=a.seed, log=log)
assert verify(P, E, keep, triangle=tri), "the reduced graph is not 5-chromatic"
snap(keep, "MINIMAL")
