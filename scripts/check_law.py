#!/usr/bin/env python3
"""Spot-check the divisibility law outside the range it was derived from.

The law -- a spindle with a non-empty shell survives iff 4 divides the numerator
of its squared radius -- was read off 285 cases with squared radius at most 60
(integers) or 30 (rationals).  Extrapolating it is exactly the kind of step this
project has been burned by, so it gets tested.
"""
import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))
from hn.joins import rational_spindle
from hn.algcolour import certify
from hn.construct import rotate
from shells import shell_count

bad = 0
for spec in sys.argv[1:]:
    num, den = (spec.split("/") + ["1"])[:2]
    num, den = int(num), int(den)
    sc = shell_count(num, den)
    if not sc:
        print(f"{spec:8} shell empty -- not a candidate either way", flush=True)
        continue
    J = rational_spindle(num, den)
    b = J.build()
    if b is None:
        print(f"{spec:8} rotation not in its field", flush=True); continue
    WL, WS, cs = b
    t = time.time()
    v = certify(WL + [rotate(p, cs) for p in WS], limit=1)
    survives = not v.dead
    predicted = (num % 4 == 0)
    ok = survives == predicted
    bad += not ok
    print(f"{spec:8} shell {sc:3d}  4|a {str(predicted):5}  filter "
          f"{'survives' if survives else 'dead':8}  {'ok' if ok else '*** LAW FAILS'}"
          f"  ({time.time()-t:.0f}s)", flush=True)
print(f"\n{bad} disagreements")
