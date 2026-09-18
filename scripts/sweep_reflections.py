#!/usr/bin/env python3
"""Join the two parts by a REFLECTION or a GLIDE, not a rotation.

Usage: sweep_reflections.py [BALL_RADIUS] [DMAX]

Every construction in the literature relates its two parts by a rotation, and
nobody says why. The isometry group of the plane has four classes: rotations,
translations, reflections and glide reflections. Rotations are swept in routes
5, 6, 18 and 19; translations are closed in route 21. Reflections and glides
have never been tried by anyone.

A reflection in the line through the origin at angle phi sends (x, y) to
(x cos 2phi + y sin 2phi, x sin 2phi - y cos 2phi), so it is exact exactly when
(cos 2phi, sin 2phi) is a unit vector of the field, which is the same
enumeration the rotation sweep uses. Reflecting in one of the lattice's own
axes gives the lattice back and nothing happens; every other line gives a
genuinely new point set. A glide adds a translation along the line, and the
composition is the one isometry class with no fixed point at all, so the two
parts would share NO vertex -- which costs one vertex against the record and
might buy more.
"""
import os, sys, math, time
from math import gcd, isqrt
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.field import K, Pt
from hn.construct import unit_vector_family, ball, dedup, edges, norm, to_float
from hn import verify, find_triangle

SQ = (1, 3, 5, 11, 15, 33, 55, 165)


def units(dmax):
    out, seen = [], set()
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
                            if round(ang, 9) not in seen:
                                seen.add(round(ang, 9))
                                out.append((ang, K.root(u) * K.rat(a, d),
                                            K.root(w) * K.rat(b, d),
                                            f"{a}sqrt{u}/{d}, {b}sqrt{w}/{d}"))
                    a += 1
    out.sort()
    return out


def reflect(p, c2, s2):
    return Pt(p.x * c2 + p.y * s2, p.x * s2 - p.y * c2)


if __name__ == "__main__":
    r = float(sys.argv[1]) if len(sys.argv) > 1 else 2.0
    dmax = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    WL, WS = unit_vector_family(2), unit_vector_family(1)
    V = ball(WL, 3, r)
    VS = ball(WS, 3, r)
    n = len(V)
    us = units(dmax)
    print(f"ball {n} (large side) and {len(VS)} (small side), {len(us)} reflection axes",
          flush=True)
    hits = 0
    for ang, c2, s2, lab in us:
        RV = [reflect(p, c2, s2) for p in VS]
        U = dedup(V + RV)
        if len(U) == n:
            continue                        # an axis of the lattice: nothing new
        E = edges(U)
        cross = sum(1 for a, b in E if (a < n) != (b < n))
        if cross <= len(WL):
            continue
        tri = find_triangle(len(U), E)
        if tri and verify(U, E, triangle=tri):
            hits += 1
            print(f"   *** 5-CHROMATIC: reflection axis at {ang/2:.4f} deg "
                  f"(cos2phi, sin2phi = {lab}), union {len(U)} vertices", flush=True)
    print(f"{hits} reflections give a 5-chromatic union", flush=True)

    print("\nglide reflections: reflection then a translation along the axis", flush=True)
    hits = 0
    for ang, c2, s2, lab in us[:14]:
        dirn = Pt(K.root(2) if False else K.rat(1), K.zero())
        for tl in (Pt(K.rat(1, 2), K.zero()), Pt(K.rat(1), K.zero()),
                   Pt(K.rat(1, 3), K.zero()), Pt(K.rat(2, 3), K.zero())):
            t = Pt(tl.x * c2 - tl.y * s2, tl.x * s2 + tl.y * c2)
            RV = [reflect(p, c2, s2) + t for p in VS]
            U = dedup(V + RV)
            E = edges(U)
            cross = sum(1 for a, b in E if (a < n) != (b < n))
            if cross <= len(WL):
                continue
            tri = find_triangle(len(U), E)
            if tri and verify(U, E, triangle=tri):
                hits += 1
                print(f"   *** 5-CHROMATIC glide: axis {ang/2:.4f} deg, "
                      f"shift {norm(tl):.4f}, union {len(U)} vertices", flush=True)
    print(f"{hits} glides give a 5-chromatic union", flush=True)
