#!/usr/bin/env python3
"""Proposition 23's two halves, checked on both lattices of the paper.

At a = 4m^2 the joint lattice automatically holds a vector of length 1/2, namely
h_g = m(1 - theta_a)g for any unit vector g, so Proposition 5 applies and the
criterion cannot kill theta_a.  Both halves of that proposition are unconditional,
because omega = exp(i pi/3) closes both lattices and 1 + omega + omega^2 = 2 omega
gives an odd relation among h, omega h and omega^2 h.

This checks the two ingredients: that both lattices are omega-closed, which the
unit triangles below witness (g1 + g2 = g3 with g2 = omega^2 g1, g3 = omega g1),
and that |h_g| is exactly 1/2 at every a = 4m^2.
"""
import cmath, math

T3 = math.acos(5 / 6)
MOSER = [cmath.exp(1j * (k * math.pi / 3 + j * T3 / 2))
         for k in range(6) for j in (-2, -1, 0, 1, 2)]
HAUG = [cmath.exp(2j * math.pi * j / 42) for j in range(42)]


def triangles(U, tol=1e-9):
    """Ordered (i, j, k) with U[i] + U[j] = U[k].  Matched by distance, not by a
    rounded key: rounding the summands first loses real matches."""
    out = []
    for i, a in enumerate(U):
        for j, b in enumerate(U):
            c = a + b
            for k, d in enumerate(U):
                if abs(c - d) < tol:
                    out.append((i, j, k)); break
    return out


for name, U, want in (("Moser, 30 unit vectors", MOSER, 60),
                      ("Haugland, 42 unit vectors", HAUG, 84)):
    tri = triangles(U)
    i, j, k = tri[0]
    print(f"{name}: {len(tri)} ordered triples with g1 + g2 = g3"
          f"   e.g. #{i} + #{j} = #{k}")
    assert len(tri) == want and len(U) == len(set((round(u.real,9), round(u.imag,9)) for u in U))
    assert all(abs(abs(U[t[2]]) - 1) < 1e-12 for t in tri), "a sum left the unit circle"

print("\nboth lattices carry a unit triangle, so Proposition 23's cyclic half")
print("applies at every a = 4m^2, for either of them.\n")

print(f"{'a':>6} {'m':>3} {'|h_g| = m|1-theta_a|':>22}  {'m even kills Z/4':>17}")
for m in range(1, 7):
    a = 4 * m * m
    c, s = (2 * a - 1) / (2 * a), math.sqrt(4 * a - 1) / (2 * a)
    h = m * abs(complex(1 - c, -s))
    print(f"{a:>6} {m:>3} {h:>22.12f}  {'yes' if m % 2 == 0 else 'needs the triangle':>17}")
    assert abs(h - 0.5) < 1e-12, (a, h)
print("\nevery h_g has length exactly 1/2, so 2h_g is a unit vector of the joint")
print("lattice and any Z/4 homomorphism must give h_g an odd value.")
