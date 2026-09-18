#!/usr/bin/env python3
"""Rotate about a point other than the origin.

Usage: sweep_centres.py [DEPTH] [RADIUS] [MMAX]     (HN_JMAX widens the lattice)

Every sweep so far rotates the lattice about the origin, so the two parts share
the origin and nothing else. That is how Heule and Parts build, but it is NOT
how de Grey's original graph is built: there the last rotation, theta_16, is
about a point at distance 2 from the centre, not about the centre.

Rotating about a lattice point c gives a genuinely different union, because the
ball is centred at the origin and c is not its centre: the second copy is
c + rho(V - c), which is not a translate of rho(V). So the rotation centre is a
free parameter, and this sweeps it together with the rotation.
"""
import os, sys, math, time
from math import gcd, isqrt
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.field import K, Pt, set_primes


def squarefree(n):
    d = 2
    while d * d <= n:
        if n % (d * d) == 0:
            return False
        d += 1
    return True


def run(m, depth, radius, dmax, jmax, ncentres):
    set_primes((3, 11, m))
    from hn.construct import ball, dedup, edges, rotate, refresh_field, to_float, norm
    from hn import verify, find_triangle
    refresh_field()
    th1 = (K.rat(1, 2), K.root(3) * K.rat(1, 2))
    gen = (K.root(33) * K.rat(1, 6), K.root(3) * K.rat(1, 6))
    W, seen = [], set()
    for j in range(-jmax, jmax + 1):
        v = Pt(K.rat(1), K.zero())
        for _ in range(abs(j)):
            v = rotate(v, gen, inverse=j < 0)
        for _ in range(6):
            if v.key() not in seen:
                seen.add(v.key())
                W.append(v)
            v = rotate(v, th1)
    V = ball(W, depth, radius)
    n = len(V)
    SQ = sorted({1, 3, 11, 33, m, 3 * m, 11 * m, 33 * m})
    rots, seenr = [], set()
    for d in range(2, dmax + 1):
        for u in SQ:
            for w in SQ:
                a = 1
                while a * a * u < d * d:
                    rem = d * d - a * a * u
                    if rem % w == 0:
                        b = isqrt(rem // w)
                        if b * b == rem // w and b > 0 and gcd(gcd(a, b), d) == 1:
                            ang = math.degrees(math.atan2(b * math.sqrt(w), a * math.sqrt(u)))
                            if 0 < ang < 180 and round(ang, 9) not in seenr:
                                seenr.add(round(ang, 9))
                                rots.append((ang, (K.root(u) * K.rat(a, d),
                                                   K.root(w) * K.rat(b, d)),
                                             f"{a}sqrt{u}/{d}, {b}sqrt{w}/{d}"))
                    a += 1
    # centres: one representative per distinct radius, nearest first
    byr = {}
    for p in V:
        r = round(norm(p), 9)
        if r not in byr:
            byr[r] = p
    centres = [byr[r] for r in sorted(byr)[:ncentres]]
    print(f"m={m}: lattice {len(W)} vectors, ball {n}, {len(rots)} rotations, "
          f"{len(centres)} centres (radii {[round(norm(c),4) for c in centres]})", flush=True)
    hits, t0 = [], time.time()
    for ci, c in enumerate(centres):
        for ang, cs, lab in rots:
            RV = [c + rotate(p - c, cs) for p in V]
            P = V + RV
            E = edges(P)
            if sum(1 for a, b in E if (a < n) != (b < n)) <= len(W):
                continue
            U = dedup(P)
            EU = edges(U)
            tri = find_triangle(len(U), EU)
            if tri and verify(U, EU, triangle=tri):
                hits.append((round(norm(c), 4), ang, len(U)))
                print(f"   *** 5-CHROMATIC: m={m}, centre at radius {norm(c):.4f}, "
                      f"rotation {ang:.4f} ({lab}), union {len(U)} vertices", flush=True)
    print(f"m={m}: {len(hits)} working (centre, rotation) pairs  ({time.time()-t0:.0f}s)",
          flush=True)
    return hits


if __name__ == "__main__":
    depth = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    radius = float(sys.argv[2]) if len(sys.argv) > 2 else 2.0
    mmax = int(sys.argv[3]) if len(sys.argv) > 3 else 20
    dmax = int(os.environ.get("HN_DMAX", 12))
    jmax = int(os.environ.get("HN_JMAX", 2))
    ncentres = int(os.environ.get("HN_CENTRES", 8))
    ms = [m for m in range(2, mmax + 1) if squarefree(m) and m % 3 and m % 11]
    lo, hi = int(os.environ.get("HN_M_LO", 0)), int(os.environ.get("HN_M_HI", 99))
    total = []
    for m in ms[lo:hi]:
        total += run(m, depth, radius, dmax, jmax, ncentres)
    print(f"\nTOTAL: {len(total)} working (centre, rotation) pairs", flush=True)
