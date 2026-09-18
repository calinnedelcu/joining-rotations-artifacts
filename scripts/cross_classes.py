"""Cross-edge CLASS census for every rational-shell spindle rotation.

Parts: type M needs "additional unit edges of two or more kinds"; the auxiliary
(second-kind) triangles are essential.  theta_4 makes 5 classes / 126 edges and
splits 374+136; alpha_{8/3} makes 1 class / 6 edges and cannot split at all.
So the number of cross-edge classes is the cheap screening test for whether a
joining rotation can ever give a lopsided L+S construction.  Pure geometry.
"""
import sys, collections
from fractions import Fraction
sys.path.insert(0, "/Users/calinnedelcu/Documents/universitate/hadwiger-nelson")
import hn.field as F
from hn.field import set_primes

def squarefree_part(n):
    s, d = 1, 2
    while d * d <= n:
        e = 0
        while n % d == 0:
            n //= d; e += 1
        if e % 2: s *= d
        d += 1
    return s * n

def rational(k): return all(x == 0 for x in k.n[1:])

depth  = int(sys.argv[1]) if len(sys.argv) > 1 else 3
radius = float(sys.argv[2]) if len(sys.argv) > 2 else 2.6

# pass 1: find the rational shells (field-independent, lattice is in Q(sqrt3,sqrt11))
set_primes((3, 11, 5)); import hn.construct as C; C.refresh_field()
from hn.construct import unit_vector_family, ball
W = unit_vector_family(2); L0 = ball(W, depth, radius)
shells = collections.Counter()
for p in L0:
    q = p.norm2()
    if rational(q):
        shells[Fraction(q.n[0], q.d)] += 1
cand = []
for d2 in sorted(shells):
    if d2 == 0: continue
    a, b = d2.numerator, d2.denominator
    s = squarefree_part(b * (4 * a - b))
    m = s
    for pr in (3, 11):
        if m % pr == 0: m //= pr
    if m in (3, 11) or m == 0: continue
    cand.append((d2, a, b, s, m if m > 1 else 5))
print(f"ball depth {depth} radius {radius}: {len(L0)} pts, {len(cand)} rational shells\n")
print(f"{'d^2':>8} {'d':>7} {'shell':>5} {'cos':>12} {'field m':>8} {'share':>6} "
      f"{'cross':>6} {'classes':>8}   class sizes")

for d2, a, b, s, m in cand:
    set_primes((3, 11, m)); C.refresh_field()
    from hn.field import K
    from hn.construct import unit_vector_family, ball, edges, norm, dedup, rotate
    # sin = sqrt(s) * t / (2a)  where b(4a-b) = s*t^2
    t2 = (b * (4 * a - b)) // s
    t = round(t2 ** 0.5)
    if t * t != t2: print(f"{str(d2):>8}  bad square"); continue
    try:
        cs = (K.rat(2 * a - b, 2 * a), K.root(s if s > 1 else 1) * K.rat(t, 2 * a))
    except AssertionError:
        print(f"{str(d2):>8}  sqrt({s}) not in Q(sqrt3,sqrt11,sqrt{m})"); continue
    if not (cs[0] * cs[0] + cs[1] * cs[1]).is_one():
        print(f"{str(d2):>8}  not a rotation in this field"); continue
    W = unit_vector_family(2); L = ball(W, depth, radius)
    R = [rotate(p, cs) for p in L]
    kL = {p.key(): i for i, p in enumerate(L)}
    share = sum(1 for p in R if p.key() in kL)
    U = dedup(L + R); E = edges(U)
    idx = {p.key(): i for i, p in enumerate(U)}
    inL = set(idx[p.key()] for p in L); inR = set(idx[p.key()] for p in R)
    cls = collections.Counter()
    n = 0
    for u, v in E:
        if (u in inL) != (v in inL) and (u in inR) != (v in inR):
            n += 1
            cls[tuple(sorted((round(norm(U[u]), 4), round(norm(U[v]), 4))))] += 1
    sizes = ",".join(str(c) for _, c in cls.most_common())
    print(f"{str(d2):>8} {float(d2)**.5:7.4f} {shells[d2]:5d} {2*a-b:>6}/{2*a:<5} "
          f"{m:>8} {share:>6} {n:>6} {len(cls):>8}   {sizes}", flush=True)
