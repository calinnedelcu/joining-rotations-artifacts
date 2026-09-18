"""Does the lattice force a MONO-triple?  Parts priced only the non-mono side.

His table lists non-mono-triples at sqrt7 (159 vertices -- the cheapest gadget of
any kind he has), sqrt5, sqrt3, sqrt(5/3), 1/sqrt3, all centred at the origin with
the other two points at exp(+-2pi i/3).  The partner -- a graph forcing such a
triple to BE monochromatic -- is priced nowhere, and a mono-triple glued to a
non-mono-triple at the same side length is 5-chromatic at |A| + |B| - 3.

Budget against sqrt7: 509 - 159 + 3 = 353 vertices.
"""
import sys, time, collections
from fractions import Fraction
sys.path.insert(0, "/Users/calinnedelcu/Documents/universitate/hadwiger-nelson")
from hn.field import set_primes
set_primes((3, 11, 5))
import hn.construct as C; C.refresh_field()
from hn.field import K, Pt
from hn.construct import unit_vector_family, ball, edges, to_float, ORIGIN, rotate, norm
from hn.sat import Colouring

def rational(k): return all(x == 0 for x in k.n[1:])
W120 = (K.rat(-1, 2), K.root(3) * K.rat(1, 2))          # exp(2 pi i / 3)

depth  = int(sys.argv[1]) if len(sys.argv) > 1 else 4
radius = float(sys.argv[2]) if len(sys.argv) > 2 else 2.6
V = ball(unit_vector_family(2), depth, radius)
E = edges(V)
idx = {p.key(): i for i, p in enumerate(V)}
print(f"ball depth {depth} radius {radius}: {len(V)} pts, {len(E)} edges", flush=True)

# every 120-degree orbit fully inside the ball, one per (radius, orbit)
seen, trips = set(), []
for p in V:
    if p.key() == ORIGIN.key(): continue
    q = rotate(p, W120); r = rotate(q, W120)
    if q.key() not in idx or r.key() not in idx: continue
    k = tuple(sorted([p.key(), q.key(), r.key()]))
    if k in seen: continue
    seen.add(k)
    trips.append((round(norm(p) * 3 ** .5, 6), idx[p.key()], idx[q.key()], idx[r.key()]))
by_side = collections.defaultdict(list)
for side, a, b, c in trips:
    by_side[side].append((a, b, c))
print(f"{len(trips)} distinct 120-degree orbits, {len(by_side)} side lengths", flush=True)

t = time.time()
Col = Colouring(len(V), E, k=4, selectors=False)
assert Col.colourable()
hits = 0
for side in sorted(by_side):
    forced = None
    for a, b, c in by_side[side][:6]:
        # "not all three equal" -> 4 clauses; ask if the ball can still be coloured
        anc = [Col.solver.add_clause] and None
        lits = []
        ok = True
        for col in range(4):
            # use assumption-style: introduce nothing, just test each colour class
            pass
        # cheaper: the triple is forced mono iff for every colour c the ball is
        # colourable with a,b,c all = col, AND not colourable with a=col, b!=col
        # -> test directly: is there a colouring with a and b differing?
        sat = False
        for c1 in range(4):
            for c2 in range(4):
                if c1 == c2: continue
                if Col.solver.solve(assumptions=[Col.var(a, c1), Col.var(b, c2)]):
                    sat = True; break
            if sat: break
        if not sat:
            forced = (a, b, c); break
    tag = "MONO-TRIPLE <<<<<" if forced else "free"
    hits += bool(forced)
    print(f"  side {side:8.4f}  orbits {len(by_side[side]):3d}   {tag}   ({time.time()-t:.0f}s)",
          flush=True)
Col.close()
print(f"\nforced mono-triples at {hits} side lengths")
