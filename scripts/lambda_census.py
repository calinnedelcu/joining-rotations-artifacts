#!/usr/bin/env python3
"""Every lambda = s/r that occurs across the cross unit vectors, over many spindles.

Step 5 of the theorem says: for lambda != -1, one of gamma(r), gamma(s) vanishes.
The rational lambda are settled by the parity of numerator and denominator.  If
the irrational ones form a FINITE set across all spindles, the step closes by
checking that set.
"""
import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.joins import rational_spindle
from hn.lattice import Lattice
from hn.algcolour import klein_colourings, apply_colouring
from hn.construct import rotate
from cross_pairs import solve_decomp
log = lambda s: print(s, flush=True)

rats, irrs = {}, {}
for a in [int(x) for x in (sys.argv[1:] or "2 5 6 9 10 11 13 14 15 17 18 21 22 23 26 27 29 30 31 33 34 35".split())]:
    J = rational_spindle(a, 1)
    b = J.build()
    if b is None:
        continue
    WL, WS, cs = b
    R = Lattice(WL)
    lam = Lattice(WL + [rotate(p, cs) for p in WS])
    if lam.rank != 8:
        continue
    import hn.field as F
    g = klein_colourings([c for c, _ in R.unit_vectors()], R.rank, 1)[0]
    basis = list(R.basis) + [rotate(p, cs) for p in R.basis]
    n_irr = 0
    for _, u in lam.unit_vectors():
        co = solve_decomp(basis, u)
        if co is None or any(x.denominator != 1 for x in co):
            continue
        if all(x == 0 for x in co[:4]) or all(x == 0 for x in co[4:]):
            continue
        r = R.combine(tuple(int(x) for x in co[:4]))
        s = R.combine(tuple(int(x) for x in co[4:]))
        L = s.x / r.x if not r.x.is_zero() else s.y / r.y
        c1 = apply_colouring(g, R.coords(r))
        c2 = apply_colouring(g, R.coords(s))
        key = (tuple(L.n), L.d)
        if any(L.n[i] for i in range(1, 8)):
            n_irr += 1
            irrs.setdefault(key, set()).add((a, c1 == 0, c2 == 0))
        else:
            if L.n[0] == -L.d:            # lambda = -1
                continue
            rats.setdefault((L.n[0], L.d), set()).add((c1 == 0, c2 == 0))
    log(f"a={a:3d}: {n_irr} cross vectors with irrational lambda")
log("")
log(f"DISTINCT rational lambda (excluding -1): {len(rats)}")
for k in sorted(rats):
    log(f"   {k[0]}/{k[1]}   zero-pattern {sorted(rats[k])}")
log("")
log(f"DISTINCT irrational lambda: {len(irrs)}")
for k in sorted(irrs, key=lambda t: (t[1], t[0])):
    aa = sorted({x[0] for x in irrs[k]})
    pat = sorted({(x[1], x[2]) for x in irrs[k]})
    log(f"   {k[0]}/{k[1]}  occurs at a = {aa}, zero-pattern {pat}")
