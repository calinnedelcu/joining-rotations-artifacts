#!/usr/bin/env python3
"""Join a lattice ball to SEVERAL rotated copies of itself at once.

Usage: multi_join.py FIELD_M a/b a/b ...   [--depth D] [--radius R]

Route 24 tested two rotations and closed the idea, but the second rotation it
used was theta_3, which is not a candidate at all -- it fails the divisibility
law.  With the classification in hand the test is different: combine rotations
that each pass the criterion, so each brings its own shell and its own family of
cross edges.

Every rotation must have its complete shell inside the ball, or its contribution
is partial and a negative answer means nothing.
"""
import os, sys, math, time, argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))
from hn.joins import rational_spindle
from shells import shell_count

ap = argparse.ArgumentParser()
ap.add_argument("m", type=int, help="third generator of the shared field")
ap.add_argument("specs", nargs="+")
ap.add_argument("--depth", type=int, default=None)
ap.add_argument("--radius", type=float, default=None)
a = ap.parse_args()
log = lambda s: print(s, flush=True)

from hn.field import set_primes, K
set_primes((3, 11, a.m))
from hn import construct as C
C.refresh_field()
from hn.construct import unit_vector_family, ball, dedup, edges_grid, rotate, norm
from hn.io import save_points, save_edges
from hn import verify, find_triangle

rots = []
need = 0.0
for spec in a.specs:
    num, den = (spec.split("/") + ["1"])[:2]
    num, den = int(num), int(den)
    J = rational_spindle(num, den, primes=(3, 11, a.m))
    b = J.build()
    if b is None:
        log(f"{spec}: not a rotation in Q(v3,v11,v{a.m})"); sys.exit(1)
    rots.append((spec, num, den, b[2], shell_count(num, den)))
    need = max(need, (num / den) ** 0.5)
set_primes((3, 11, a.m)); C.refresh_field()
W = unit_vector_family(2)
depth = a.depth or math.ceil(need)
radius = a.radius or (need + 0.02)
t = time.time(); V = ball(W, depth, radius)
log(f"field Q(v3,v11,v{a.m}), ball depth {depth} radius {radius:.2f}: "
    f"{len(V)} points  ({time.time()-t:.0f}s)")
ok = True
for spec, num, den, cs, tot in rots:
    on = sum(1 for p in V if abs(norm(p) ** 2 - num / den) < 1e-9)
    log(f"  rotation {spec:8} shell {on}/{tot}" + ("" if on == tot else "   INCOMPLETE"))
    ok &= on == tot
if not ok:
    log("at least one shell is incomplete -- a negative answer would be meaningless")

P = list(V)
for spec, num, den, cs, tot in rots:
    P += [rotate(p, cs) for p in V]
U = dedup(P)
log(f"union of {1+len(rots)} copies: {len(U)} points; finding edges")
t = time.time(); E = edges_grid(U)
log(f"{len(E)} edges  ({time.time()-t:.0f}s); testing 4-colourability")
t = time.time(); tri = find_triangle(len(U), E)
five = verify(U, E, triangle=tri) if tri else None
log(f"chi >= 5: {five}  ({time.time()-t:.0f}s)"
    + ("   <<< A MULTI-ROTATION CONSTRUCTION WORKS" if five else ""))
if five:
    tag = "multi_" + "_".join(s.replace("/", "-") for s, *_ in rots)
    out = os.path.join(os.path.dirname(__file__), "..", "out")
    save_points(f"{out}/{tag}.pts", U)
    save_edges(f"{out}/{tag}.edge", len(U), E)
    log(f"saved out/{tag}.pts")
