#!/usr/bin/env python3
"""Recover each construction's ball from its own coordinates.

Section 6 says the six new unions are a ball of R glued to its own image, and
the table gives a depth and a radius for each.  Those two numbers are not taken
from a build log: they are measured here from the shipped .pts, so a reader can
check them against the graph rather than against a claim.

For each union: split off the half that lies in R, report its size, its radius,
and the smallest generation depth d for which ball(W, d, r) is exactly that half.

Run: .venv/bin/python scripts/ball_params.py [name ...]
"""
import os, sys, math, subprocess, json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
JOINS = [("theta_4", 4, 1), ("theta_16", 16, 1), ("theta_28", 28, 1),
         ("theta_36", 36, 1), ("alpha_64/3", 64, 3), ("alpha_64/9", 64, 9),
         ("alpha_256/9", 256, 9)]
STEM = {4: "join4", 16: "join16", 28: "join28", 36: "join36"}

WORKER = r'''
import json, math, os, sys
sys.path.insert(0, %r)
A, B, path = json.loads(sys.argv[1])
from hn.joins import rational_spindle
WL, _, cs = rational_spindle(A, B).build()
from hn import construct as C
from hn.lattice import Lattice
from hn.io import load_points
P = load_points(path)
L0 = Lattice(WL)
half = [p for p in P if L0.coords(p) is not None]
r2 = max(C.to_float(p.norm2()) for p in half)
r = math.sqrt(r2)
want = {(str(p.x), str(p.y)) for p in half}
found = None
for d in range(2, 10):
    B2 = C.ball(WL, d, r + 1e-9)
    if {(str(p.x), str(p.y)) for p in B2} == want:
        found = d; break
    if len(B2) > len(half) * 1.5:
        break
print(json.dumps({"union": len(P), "half": len(half), "r2": r2, "r": r,
                  "depth": found}))
''' % os.path.abspath(ROOT)


def main():
    pick = sys.argv[1:]
    print(f"{'rotation':<12} {'union':>8} {'half':>7} {'radius':>8} {'|z|^2':>10} {'depth':>6}")
    for name, A, B in JOINS:
        if pick and name not in pick:
            continue
        stem = f"join{A}" if B == 1 else f"join{A}_{B}"
        cand = [os.path.join(ROOT, "out", stem + ".pts"),
                os.path.join(ROOT, "graphs", stem + ".pts")]
        src = next((p for p in cand if os.path.exists(p)), None)
        if src is None:
            why = ("Parts' minimised 509, not a ball union -- the table's depth "
                   "and radius do not apply") if A == 4 else \
                  "no coordinates for it here; see graphs/"
            print(f"{name:<12}  ({why})")
            continue
        out = subprocess.run([sys.executable, "-c", WORKER,
                              json.dumps([A, B, src])],
                             capture_output=True, text=True)
        try:
            d = json.loads(out.stdout.strip().splitlines()[-1])
        except Exception:
            print(f"{name:<12}  failed: {out.stderr.strip().splitlines()[-1:]}")
            continue
        print(f"{name:<12} {d['union']:>8} {d['half']:>7} {d['r']:>8.4f} "
              f"{d['r2']:>10.4f} {str(d['depth']):>6}")
        assert 2 * d["half"] - 1 == d["union"], "the union is not the half doubled"


if __name__ == "__main__":
    main()
