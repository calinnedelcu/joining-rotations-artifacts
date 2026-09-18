#!/usr/bin/env python3
"""The rotations spinning Parts' mono-pair distances, as a family.

Three of the rational rotations that work spin shells at distance 8/3, 16/3 and
8/sqrt3.  The first two are Parts' mono-pair lengths.  This walks the family
outward: distance n*(8/3), squared radius 64n^2/9, and the sibling 64n^2/3.
"""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))
from shells import shell_count
from hn.joins import rational_spindle
from hn.algcolour import certify
from hn.construct import rotate
log = lambda s: print(s, flush=True)

for label, base_den in (("n * 8/3", 9), ("n * 8/sqrt3", 3)):
    log(f"family {label}:")
    for n in range(1, 6):
        num, den = 64 * n * n, base_den
        g = math.gcd(num, den); num //= g; den //= g
        sc = shell_count(num, den)
        J = rational_spindle(num, den)
        b = J.build()
        if b is None:
            log(f"  n={n}: {num}/{den}  rotation not in its field"); continue
        if not sc:
            log(f"  n={n}: {num}/{den}  dist {(num/den)**0.5:.3f}  NO SHELL"); continue
        WL, WS, cs = b
        v = certify(WL + [rotate(p, cs) for p in WS], limit=1)
        log(f"  n={n}: {num}/{den}  dist {(num/den)**0.5:.3f}  shell {sc:3d}  "
            f"cos {J.cos}  {J.field_str():18} filter "
            f"{'SURVIVES' if not v.dead else 'dead'}")
