#!/usr/bin/env python3
"""Test whether a surviving joining rotation actually gives a 5-chromatic union.

Usage: test_join.py A [--depth D] [--radius R]

`classify_joins.py` says which rotations CAN work -- the filter is a one-sided
kill, so a survivor is a candidate and nothing more.  This is the other half:
build the union and ask.

The ball must REACH the shell the rotation spins, at radius sqrt(a), or the
rotation has no point to move and the answer is meaningless -- that is the
routes 20/44/48 error.  Depth d reaches radius d at most, so a needs depth
ceil(sqrt(a)): theta_16 is fine at depth 4, theta_28 needs 6, theta_60 needs 8.

Edges come from `edges_grid`, which is linear in space; the blocked finder
wants 2.5 GB per block at this scale.
"""
import os, sys, math, time, argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.joins import rational_spindle
from hn.construct import ball, dedup, edges_grid, rotate, norm
from hn.io import save_points, save_edges
from hn import verify, find_triangle
sys.path.insert(0, os.path.dirname(__file__))
from shells import shell_count

ap = argparse.ArgumentParser()
ap.add_argument("a", help="squared radius of the shell: an integer, or a/b")
ap.add_argument("--depth", type=int, default=None)
ap.add_argument("--radius", type=float, default=None)
a = ap.parse_args()
log = lambda s: print(s, flush=True)

num, den = (a.a.split("/") + ["1"])[:2]
num, den = int(num), int(den)
need = math.sqrt(num / den)
depth = a.depth or math.ceil(need)
radius = a.radius or (need + 0.02)
J = rational_spindle(num, den)
tag = f"{num}_{den}" if den != 1 else str(num)
b = J.build()
if b is None:
    log(f"theta_{a.a} does not exist in {J.field_str()}"); sys.exit(1)
WL, WS, cs = b
log(f"{J.name} = arccos({J.cos}) in {J.field_str()}; shell at squared radius "
    f"{num}/{den}, radius {need:.4f}, needs depth {depth}")

t = time.time(); V = ball(WL, depth, radius)
on = sum(1 for p in V if abs(norm(p) ** 2 - num / den) < 1e-9)
total = shell_count(num, den)
log(f"ball depth {depth} radius {radius:.2f}: {len(V)} points, {on} of the "
    f"shell's {total} ({time.time()-t:.0f}s)")
if not on:
    log("THE BALL DOES NOT REACH THE SHELL -- any answer here would be meaningless")
    sys.exit(1)
if on < total:
    log(f"WARNING: the ball holds only {on} of the {total} points the shell has.")
    log("  A 5-chromatic answer is still sound -- a 5-chromatic subgraph is one")
    log("  whatever else is missing.  A 4-colourable answer is NOT a refutation:")
    log("  the rotation has not been given its whole shell to act on.")

t = time.time(); U = dedup(V + [rotate(p, cs) for p in V])
log(f"union {len(U)} points ({time.time()-t:.0f}s); finding edges")
t = time.time(); E = edges_grid(U)
log(f"{len(E)} edges ({time.time()-t:.0f}s); testing 4-colourability")
t = time.time(); tri = find_triangle(len(U), E)
five = verify(U, E, triangle=tri) if tri else None
log(f"chi >= 5: {five}   ({time.time()-t:.0f}s)"
    + ("   <<< A NEW JOINING ROTATION WORKS" if five else ""))
if five:
    out = os.path.join(os.path.dirname(__file__), "..", "out")
    save_points(f"{out}/join{tag}.pts", U)
    save_edges(f"{out}/join{tag}.edge", len(U), E)
    log(f"saved out/join{tag}.pts")
