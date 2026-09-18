#!/usr/bin/env python3
"""Hunt for a cyclotomic perturbation whose powers keep one denominator.

Usage: cyclo_units.py [--support 3] [--coef 3] [--conductors 14,18,21,42]

Route 38 died on denominators, not on depth. The classical lattice is dense
because its 30 generators exp(i(k*60deg + j*theta_3/2)) all lie in ONE lattice:
the perturbation z = (sqrt33 + i*sqrt3)/6 has z^2 = (5 + i*sqrt11)/6, denominator
6 rather than 36, so the powers do not scatter the points across a finer grid.

Kronecker says a cyclotomic ring has no unit-modulus algebraic *integer* except
the roots of unity already in the lattice, so a perturbation must have a
denominator. What it does not forbid is the coincidence above. Write the
perturbation as v/c with v in Z[zeta_n]; then

    |v/c| = 1            means   v * conj(v) = c^2,
    (v/c)^2 keeps c      means   c divides v^2 in the ring.

Both are exact integer conditions, so this is a finite search. Rotating v by a
root of unity changes neither, so the support may be taken to contain zeta^0.
"""
import os, sys, argparse, itertools, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import hn.cyclo as C
from hn.cyclo import Cyc

ap = argparse.ArgumentParser()
ap.add_argument("--coef", type=int, default=3,
                help="search all v with power-basis coefficients in [-coef, coef]; "
                     "a sparse search over roots of unity misses everything that "
                     "matters, since theta_2's numerator 3 + g has support 7")
ap.add_argument("--conductors", default="14,18")
a = ap.parse_args()
log = lambda s: print(s, flush=True)


def rational_int(x):
    """The integer x represents, or None."""
    if any(x.n[1:]):
        return None
    return x.n[0] // x.d if x.n[0] % x.d == 0 else None


def divides(c, x):
    """Is x/c still in the ring?"""
    return all(k % c == 0 for k in x.n) if x.d == 1 else False


for n in [int(t) for t in a.conductors.split(",")]:
    C.set_conductor(n)
    hits, tried = [], 0
    roots = {Cyc.zeta(k).key() for k in range(n)}
    roots |= {(-Cyc.zeta(k)).key() for k in range(n)}
    for t in itertools.product(range(-a.coef, a.coef + 1), repeat=C.DEG):
        if t[0] < 0 or not any(t):        # v and -v are the same rotation
            continue
        tried += 1
        v = Cyc(list(t), 1)
        m = rational_int(v * v.conj())
        if m is None or m < 4:
            continue
        c = math.isqrt(m)
        if c * c != m or c < 2:
            continue
        if not divides(c, v * v):
            continue
        u = v * Cyc.rat(1, c)
        if u.key() in roots:              # a root of unity is already in the lattice
            continue
        hits.append((c, t, u))
    log(f"Q(zeta_{n}) rank {C.DEG}: searched {tried} elements of the power basis box, "
        f"{len(hits)} non-trivial rotations with |v/c| = 1 and c dividing v^2")
    seen = set()
    for c, t, u in sorted(hits, key=lambda h: (h[0], h[1]))[:14]:
        z = u.complex()
        ang = round(math.degrees(math.atan2(z.imag, z.real)), 6)
        if ang in seen:
            continue
        seen.add(ang)
        u2 = u * u
        log(f"    {t}/{c}   angle {ang:9.4f} deg, cos {z.real:.6f}; "
            f"u^2 denominator {u2.d}")
