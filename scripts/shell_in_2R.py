#!/usr/bin/env python3
"""Test the reduction: a shell point lies in 2R iff 4 divides its squared radius.

This is the divisibility law with the rotation removed.  The chain is

    theta survives
      <=>  (p - theta(p))/2 lies in the joint lattice        [geometric form]
      <=>  p/2 lies in R                                      [this file]
      <=>  4 | a                                              [the law]

the middle step because e^(i.theta) = -conj(nu)/nu with nu = (1 + i sqrt(4a-1))/2
and nu + conj(nu) = 1, so nu R + conj(nu) R contains 1.

R here is the Moser lattice itself: no rotation, no joint lattice, no field
extension.  That is the whole point -- the statement to prove no longer mentions
the construction at all.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))
from hn.field import set_primes, K, Pt
set_primes((3, 5, 11))
from hn import construct as C
C.refresh_field()
from hn.construct import unit_vector_family, ball, norm
from hn.lattice import Lattice
from shells import shell_count

hi = int(sys.argv[1]) if len(sys.argv) > 1 else 36
W = unit_vector_family(2)
R = Lattice(W)
depth = int(hi ** 0.5) + 2
V = ball(W, depth, hi ** 0.5 + 0.02)
print(f"ball depth {depth}: {len(V)} points", flush=True)
bad = 0
for N in range(1, hi + 1):
    tot = shell_count(N)
    if not tot:
        continue
    shell = [p for p in V if abs(norm(p) ** 2 - N) < 1e-9]
    if not shell:
        print(f"N={N:3d}: shell of {tot} not reached by this ball"); continue
    inhalf = sum(1 for p in shell if R.contains(Pt(p.x * K.rat(1, 2), p.y * K.rat(1, 2))))
    allin = inhalf == len(shell)
    pred = N % 4 == 0
    ok = allin == pred and inhalf in (0, len(shell))
    bad += not ok
    print(f"N={N:3d}  4|N {str(pred):5}  shell {len(shell):3d}/{tot:3d}  "
          f"p/2 in R for {inhalf:3d}  {'ok' if ok else '*** MISMATCH'}", flush=True)
print(f"\n{bad} mismatches")
