"""Forced mono-pairs on every RATIONAL shell, at radii route 7 never reached.

Route 7 scanned depth 4 radius 3.0 and found mono-pairs at exactly one distance,
8/3.  Every rational squared radius a/b carries a spindle rotation
cos = (2a-b)/(2a), sin = sqrt(b(4a-b))/(2a), which lies in Q(sqrt3,sqrt11,sqrt m)
for exactly one squarefree m.  So a forced mono-pair on ANY rational shell gives a
5-chromatic union at once.  Radii above 3.0 were never scanned.
"""
import sys, time, collections
from fractions import Fraction
sys.path.insert(0, "/Users/calinnedelcu/Documents/universitate/hadwiger-nelson")
from hn.field import set_primes
set_primes((3, 11, 5))
import hn.construct as C
C.refresh_field()
from hn.construct import unit_vector_family, ball, edges, to_float, ORIGIN, norm
from hn.sat import Colouring

def rational(k): return all(x == 0 for x in k.n[1:])

depth  = int(sys.argv[1]) if len(sys.argv) > 1 else 4
radius = float(sys.argv[2]) if len(sys.argv) > 2 else 4.05
lo     = float(sys.argv[3]) if len(sys.argv) > 3 else 2.6
W = unit_vector_family(2)
V = ball(W, depth, radius)
E = edges(V)
o = next(i for i, p in enumerate(V) if p.key() == ORIGIN.key())
print(f"ball depth {depth} radius {radius}: {len(V)} pts, {len(E)} edges", flush=True)

shells = collections.defaultdict(list)
for i, p in enumerate(V):
    q = p.norm2()
    if rational(q):
        d2 = Fraction(q.n[0], q.d)
        if d2 > 0 and float(d2) ** .5 >= lo:
            shells[d2].append(i)
print(f"{len(shells)} rational shells at radius >= {lo}", flush=True)

t = time.time()
Col = Colouring(len(V), E, k=4, selectors=False)
Col.solver.add_clause([Col.var(o, 0)])
for c in (1, 2, 3):
    Col.solver.add_clause([-Col.var(o, c)])
assert Col.colourable(), "ball not 4-colourable"
print(f"base solve {time.time()-t:.0f}s", flush=True)
for d2 in sorted(shells):
    pts = shells[d2]
    # one representative per shell first; if forced, check them all
    res = []
    for i in pts:
        mono = not Col.solver.solve(assumptions=[Col.var(i, 1)])
        virt = (not mono) and (not Col.solver.solve(assumptions=[Col.var(i, 0)]))
        res.append((mono, virt))
        if mono: break
    mono = any(m for m, v in res); virt = all(v for m, v in res)
    tag = "MONO-PAIR <<<<<" if mono else ("virtual edge" if virt else "free")
    print(f"  d^2={str(d2):>8} d={float(d2)**.5:7.4f} shell {len(pts):3d}  {tag}"
          f"   ({time.time()-t:.0f}s)", flush=True)
Col.close()
