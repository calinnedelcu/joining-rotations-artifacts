"""Does the lattice force a mono-pair at 8/3, and is alpha = arccos(119/128)
an exact rotation of Q(sqrt3, sqrt11, sqrt247)?

Route 7 measured the forcing at depth 4 radius 3.0 and then declared the route
closed because sqrt247 is not in Q(sqrt3,sqrt5,sqrt11).  But the lattice lives in
Q(sqrt3,sqrt11) (route 18), so the third generator is free: set it to 247.
"""
import sys, time
sys.path.insert(0, "/Users/calinnedelcu/Documents/universitate/hadwiger-nelson")
import hn.field as F
from hn.field import set_primes
set_primes((3, 11, 247))
import hn.construct as C
C.refresh_field()
from hn.field import K, Pt
from hn.construct import unit_vector_family, ball, edges, norm, ORIGIN, to_float, rotate, dedup
from hn.sat import Colouring

# alpha: cos = 119/128, sin = 3 sqrt247 / 128
cs = (K.rat(119, 128), K.root(247) * K.rat(3, 128))
print("modulus is exactly 1:", (cs[0]*cs[0] + cs[1]*cs[1]).is_one())

depth  = int(sys.argv[1]) if len(sys.argv) > 1 else 4
radius = float(sys.argv[2]) if len(sys.argv) > 2 else 2.8
W = unit_vector_family(2)
V = ball(W, depth, radius)
E = edges(V)
o = next(i for i, p in enumerate(V) if p.key() == ORIGIN.key())
shell = [i for i, p in enumerate(V) if abs(to_float(p.norm2()) - 64/9) < 1e-9]
print(f"ball depth {depth} radius {radius}: {len(V)} points, {len(E)} edges, "
      f"{len(shell)} points on the 8/3 shell", flush=True)

# the rotation really does turn shell points into unit-distance partners
p = V[shell[0]]
q = rotate(p, cs)
d2 = (p - q).norm2()
print("|p - alpha(p)|^2 == 1 exactly:", d2.is_one())

t = time.time()
Col = Colouring(len(V), E, k=4, selectors=False)
Col.solver.add_clause([Col.var(o, 0)])
for c in (1, 2, 3):
    Col.solver.add_clause([-Col.var(o, c)])
assert Col.colourable(), "ball not 4-colourable"
res = []
for i in shell:
    forced = not Col.solver.solve(assumptions=[Col.var(i, 1)])
    res.append(forced)
    print(f"  shell point {i} forced to agree with the origin: {forced}  "
          f"({time.time()-t:.0f}s)", flush=True)
Col.close()
print("\nALL SIX FORCED:", all(res))
