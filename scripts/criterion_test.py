#!/usr/bin/env python3
"""Test the half-unit criterion against the filter, over many rotations.

CLAIM: theta_a survives the homomorphism filter  <=>  its joint lattice
contains a point at distance exactly 1/2 from the origin.

The kill direction is proved (results/JOIN-CLASSIFICATION.md). The converse --
no half-unit vector implies a certificate exists -- is empirical, and this is
what measures it, on every integer spindle in a range rather than a handful.
"""
import os, sys, time, argparse, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.joins import rational_spindle
from hn.lattice import Lattice
from hn.algcolour import klein_colourings, z4_colourings, _solve_affine
from hn.field import K, Pt
from hn.construct import rotate

ap = argparse.ArgumentParser()
ap.add_argument("--amax", type=int, default=60)
ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "..",
                                              "results", "CRITERION-TEST.json"))
a = ap.parse_args()
rows, bad = [], 0
for n in range(1, a.amax + 1):
    J = rational_spindle(n, 1)
    b = J.build()
    if b is None:
        continue
    WL, WS, cs = b
    t = time.time()
    lam = Lattice(WL + [rotate(p, cs) for p in WS])
    co = [c for c, _ in lam.unit_vectors()]
    H = []
    for c, p in lam.unit_vectors():
        h = Pt(p.x * K.rat(1, 2), p.y * K.rat(1, 2))
        if lam.contains(h):
            H.append(lam.coords(h))
    hrows = sorted({sum((x & 1) << k for k, x in enumerate(hc)) for hc in H})
    psi = _solve_affine(hrows, [1] * len(hrows), lam.rank) is not None
    nk = len(klein_colourings(co, lam.rank, 1))
    nz = len(z4_colourings(co, lam.rank, 1))
    survives = (nk == 0 and nz == 0)
    predict = len(H) > 0 and not psi          # both hypotheses of the theorem
    ok = survives == predict
    bad += not ok
    rows.append(dict(a=n, rank=lam.rank, units=len(co), half=len(H),
                     psi=psi, klein=nk, z4=nz, survives=survives,
                     predicted=predict, agree=ok, secs=round(time.time() - t, 1)))
    print(f"a={n:3d} rank{lam.rank} units{len(co):4d} half{len(H):4d} "
          f"psi={str(psi):5} klein{nk} z4{nz} -> {'survives' if survives else 'dead':8} "
          f"predicted {'survives' if predict else 'dead':8} {'ok' if ok else '*** DISAGREE'}",
          flush=True)
print(f"\n{len(rows)} rotations, {len(rows)-bad} agree, {bad} disagree")
os.makedirs(os.path.dirname(a.out), exist_ok=True)
json.dump(rows, open(a.out, "w"), indent=1)
