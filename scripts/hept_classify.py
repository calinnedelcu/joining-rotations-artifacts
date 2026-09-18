#!/usr/bin/env python3
"""Classify the joining rotations of Haugland's lattice, as we did for Moser's.

The divisibility law -- theta_a joins iff 4 | a -- is now known NOT to transfer:
theta_2 dies on the Moser lattice and survives here.  So the classification has
to be redone from scratch on this lattice, and it can be, because the criterion
costs almost nothing at rank 12.

For each squared radius N with a non-empty shell, the spindle theta_N has
cos = (2N-1)/(2N) and sin = sqrt(4N-1)/(2N), and exists here exactly when
sqrt(4N-1) lies in Q(zeta_420).  That field contains sqrt(m) for m built from
the primes dividing 420 = 4*3*5*7, and i, so the test is concrete.
"""
import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import hn.cyclo as CY
from hn.cyclo import Cyc, dedup
from hn.cyclolat import CycLattice
from hn.algcolour import klein_colourings, z4_colourings
log = lambda s: print(s, flush=True)


def squarefree_part(n):
    s, d = 1, 2
    while d * d <= n:
        e = 0
        while n % d == 0:
            n //= d; e += 1
        if e % 2:
            s *= d
        d += 1
    return s * n


CY.set_conductor(420)
z = Cyc.zeta
half = Cyc.rat(1, 2)
i_u = z(105)
r3 = z(35) + z(-35)
cpi7 = (z(30) + z(-30)) * half
s2p7 = (z(60) - z(-60)) * (half * z(-105))
rho = ((Cyc.zero() - r3) + i_u * (cpi7 * Cyc.rat(4) - Cyc.rat(1))) \
      * (s2p7 * Cyc.rat(4)).inv() * z(-140)

# square roots available: build them from Gauss sums of the primes dividing 420
ROOTS = {1: Cyc.rat(1), 3: r3}
for p in (5, 7):
    g = CY.gauss_sum(p)
    ROOTS[p] = g if p % 4 == 1 else g * i_u * Cyc.rat(-1)
for a in (3, 5, 7):
    for b in (5, 7):
        if a < b:
            ROOTS[a * b] = ROOTS[a] * ROOTS[b]
ROOTS[105] = ROOTS[3] * ROOTS[5] * ROOTS[7]
for m, r in list(ROOTS.items()):
    ok = (r * r - Cyc.rat(m)).is_zero()
    if not ok:
        log(f"  WARNING sqrt{m} does not square to {m}")

sets = int(sys.argv[1]) if len(sys.argv) > 1 else 2
hi = int(sys.argv[2]) if len(sys.argv) > 2 else 12
gens = []
for s in range(sets):
    rk = Cyc.rat(1)
    for _ in range(s):
        rk = rk * rho
    gens += [rk * z(10 * j) for j in range(42)]
gens = dedup(gens)
L0 = CycLattice(gens)
log(f"Haugland lattice, {sets} set(s): rank {L0.rank}, den {L0.den}")
log(f"square roots available in Q(zeta_420): {sorted(ROOTS)}")
log("")
log(f"{'N':>4} {'shell':>6} {'sqrt(4N-1)':>11} {'rank':>5} {'units':>6} "
    f"{'half':>5} {'klein':>6} {'z4':>4}  verdict")
for N in range(1, hi + 1):
    t = time.time()
    sh = L0.shell(N)
    if not sh:
        log(f"{N:4d} {0:6d}  -- no shell")
        continue
    m = squarefree_part(4 * N - 1)
    k = round(((4 * N - 1) // m) ** 0.5)
    if m not in ROOTS or k * k * m != 4 * N - 1:
        log(f"{N:4d} {len(sh):6d} {('sqrt' + str(m)):>11}  not in the field")
        continue
    sn = ROOTS[m] * Cyc.rat(k, 2 * N)
    th = Cyc.rat(2 * N - 1, 2 * N) + i_u * sn
    if not (th * th.conj()).is_one():
        log(f"{N:4d} {len(sh):6d}  rotation does not have modulus 1")
        continue
    # An even integer shell radius passes for free, by the theorem: 2g is a
    # shell point for every generator g, and (2g - theta(2g))/2 = g - theta(g)
    # is a lattice element of modulus 1/2.  No need to build anything.
    rr = N ** 0.5
    if abs(rr - round(rr)) < 1e-12 and round(rr) % 2 == 0:
        log(f"{N:4d} {len(sh):6d} {('sqrt' + str(m)):>11}      -      -     - "
            f"     -    -  SURVIVES trivially (even radius {round(rr)})")
        continue
    L = CycLattice(dedup(gens + [th * g for g in gens]))
    U = L.unit_vectors()
    co = [c for c, _ in U]
    nh = sum(1 for c, _ in U if all(x % 2 == 0 for x in c))
    # The full certificate search is 2^rank, hopeless past about 16.  A
    # half-unit vector settles it outright -- that is the proved half of the
    # theorem -- so only run the search when there is none AND the rank is small.
    if nh:
        nk, nz, surv = 0, 0, True
    elif L.rank <= 16:
        nk = len(klein_colourings(co, L.rank, 1))
        nz = len(z4_colourings(co, L.rank, 1)) if not nk else 0
        surv = not (nk or nz)
    else:
        nk = nz = -1
        surv = None
    log(f"{N:4d} {len(sh):6d} {('sqrt' + str(m)):>11} {L.rank:5d} {len(U):6d} "
        f"{nh:5d} {nk:6d} {nz:4d}  "
        + ("SURVIVES" if surv else ("dead" if surv is False else
           f"undecided (rank {L.rank} too high for the full search)"))
        + ("  (trivially: even radius)" if surv and nh and
           abs(N ** 0.5 - round(N ** 0.5)) < 1e-12 and round(N ** 0.5) % 2 == 0
           else "")
        + f"   ({time.time()-t:.0f}s)")
