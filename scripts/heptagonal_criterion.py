#!/usr/bin/env python3
"""Apply the joining criterion to Haugland's heptagonal lattice.

de Grey asked publicly (Polymath16 thread 18, 13 Sep 2026) for someone to
explore Haugland's construction as a route past 509, "using more than just two
sets of 42 vectors".  The approach so far -- ours included -- has been to build
sets and run SAT for hours.  This asks the question the other way round.

The criterion, in the geometric form proved for the Moser lattice: a spindle
makes |p - theta(p)| = 1 for every point p of its shell, so (p - theta(p))/2 has
length exactly 1/2, and the rotation admits no homomorphism 4-colouring of the
joint lattice precisely when that point LIES IN the lattice.

Here the rotation is theta_4 = (7 + i sqrt15)/8 -- Haugland's own joining map,
the record's rotation -- whose shell is at squared radius 4.  So the test is:
take a lattice point at distance 2 from the origin and ask whether half its
displacement is a lattice point.

Membership needs the lattice, not its unit vectors, so this runs without porting
the trace-form ellipsoid to conductor 420 (degree 96).
"""
import os, sys, time, argparse
from fractions import Fraction
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import hn.cyclo as CY
from hn.cyclo import Cyc, ball, dedup

ap = argparse.ArgumentParser()
ap.add_argument("--sets", type=int, default=2, help="how many sets of 42 vectors")
ap.add_argument("--depth", type=int, default=2)
ap.add_argument("--radius", type=float, default=2.05)
a = ap.parse_args()
log = lambda s: print(s, flush=True)

CY.set_conductor(420)
log(f"Q(zeta_420), degree {CY.DEG}")
z = Cyc.zeta
half = Cyc.rat(1, 2)

# ---- rho, exactly, as in scripts/haugland_sets.py -------------------------
r3 = z(35) + z(-35)                                   # sqrt3
r15 = (z(42) - z(-42)) * (z(105) - z(-105)) * Cyc.rat(-1)   # placeholder, checked below
cpi7 = (z(30) + z(-30)) * half                        # cos(pi/7)
s2p7 = (z(60) - z(-60)) * (half * z(-105))            # sin(2pi/7)
vec = (Cyc.zero() - r3) + z(105) * (cpi7 * Cyc.rat(4) - Cyc.rat(1))
rho = vec * (s2p7 * Cyc.rat(4)).inv() * z(-140)
log(f"rho has modulus 1: {(rho * rho.conj()).is_one()}")

# ---- theta_4 = (7 + i sqrt15)/8 -------------------------------------------
# sqrt15 = sqrt3 * sqrt5 ; sqrt5 = 2 cos(pi/5) + ... build from zeta_5 Gauss sum
g5 = CY.gauss_sum(5)                                   # sqrt5 (up to sign)
r5 = g5
log(f"sqrt5 squares to 5: {(r5 * r5 - Cyc.rat(5)).is_zero()}")
r15 = r3 * r5
t4 = Cyc.rat(7, 8) + z(105) * r15 * Cyc.rat(1, 8)      # z(105) = i
log(f"theta_4 has modulus 1: {(t4 * t4.conj()).is_one()}")
log("")

# ---- the lattice ----------------------------------------------------------
gens = []
for s in range(a.sets):
    rk = Cyc.rat(1)
    for _ in range(s):
        rk = rk * rho
    for j in range(42):
        gens.append(rk * z(10 * j))                    # zeta_42^j = zeta_420^(10j)
gens = dedup(gens)
log(f"{a.sets} sets of 42 -> {len(gens)} distinct unit vectors")
allunit = all((g * g.conj()).is_one() for g in gens)
log(f"every generator has modulus exactly 1: {allunit}")
