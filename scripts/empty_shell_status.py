#!/usr/bin/env python3
"""The multiples of 4 below 100 whose shell is EMPTY, and what decides them.

Theorem 1 excludes 4 | a only when the shell is non-empty; an empty shell leaves
the criterion silent, so those a are survivors until something else disposes of
them.  Section 7's sieve counts only the sixteen with an occupied shell, and the
nine empty ones fall out of the accounting.  This script puts them back.

For each, run filter 1 on the joint lattice directly -- every homomorphism onto
either group of order 4, over the exact unit-vector list -- and report whether a
colouring exists.  Where one does, the rotation is dead and the story ends.
Where none does, the rotation is a candidate and the periodic filter is the next
instrument; those are named at the end so they can be run.

Run: .venv/bin/python scripts/empty_shell_status.py
"""
import os, sys, time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from hn.joins import rational_spindle
log = lambda s: print(s, flush=True)

EMPTY = [8, 24, 32, 40, 56, 68, 72, 88, 96]     # 4 | a, a <= 100, shell empty
survivors, dead, absent = [], [], []

log(f"{'a':>4} {'shell':>6} {'rank':>5} {'units':>6} {'verdict':>9}   colourings")
for a in EMPTY:
    J = rational_spindle(a, 1)
    built = J.build()
    if built is None:
        absent.append(a)
        log(f"{a:>4} {'--':>6} {'--':>5} {'--':>6} {'NO ROTN':>9}   theta_a not in its own field")
        continue
    WL, _, cs = built
    from hn import construct as C
    from hn.construct import rotate
    from hn.algcolour import certify
    from hn.lattice import Lattice
    shell = sum(1 for p in C.ball(WL, 2, (a ** 0.5) + 0.01)
                if abs(C.to_float(p.norm2()) - a) < 1e-9)
    v = certify(list(WL) + [rotate(p, cs) for p in WL])
    (dead if v.dead else survivors).append(a)
    log(f"{a:>4} {shell:>6} {v.lattice.rank:>5} {len(v.units):>6} "
        f"{('DEAD' if v.dead else 'candidate'):>9}   {len(v.certs)}")

log(f"\nshell empty and a homomorphism 4-colouring exists (dead): {dead}")
log(f"shell empty and none exists (still candidates):          {survivors}")
if absent:
    log(f"rotation does not exist in its field:                    {absent}")
log("\nSo Section 7's sieve, which counts only the occupied-shell candidates,")
log(f"leaves {len(survivors)} value(s) undisposed of. Those need the periodic filter:")
for a in survivors:
    log(f"    .venv/bin/python scripts/join_filter_residues.py {a}")
