#!/bin/sh
cd "$(dirname "$0")/.."
HN_TEST=1 .venv/bin/python -u - > out/t16_37_11.log 2>&1 <<'PYEOF'
import sys, time, collections; sys.path.insert(0,'.')
from hn.field import set_primes, K, Pt
set_primes((3,7,11))
import hn.construct as C; C.refresh_field()
from hn.construct import unit_vector_family, ball, dedup, edges, rotate, to_float
from hn.sat import find_triangle
from hn.minimise import verify
from hn.graph import induced
def kcore(n,E,d):
    adj=collections.defaultdict(set)
    for u,v in E: adj[u].add(v); adj[v].add(u)
    alive=set(range(n)); q=[v for v in alive if len(adj[v])<d]
    while q:
        v=q.pop()
        if v not in alive: continue
        alive.discard(v)
        for w in adj[v]:
            if w in alive:
                adj[w].discard(v)
                if len(adj[w])<d: q.append(w)
    return sorted(alive)
def spindle(i):
    import math
    from hn.field import squarefree_divisors
    m=4*i-1
    for s in squarefree_divisors():
        if m%s==0 and math.isqrt(m//s)**2==m//s:
            return (K.rat(2*i-1,2*i), K.root(s)*K.rat(math.isqrt(m//s),2*i))
    return None
W=unit_vector_family(2)
for depth,r in ((4,4.0),(4,2.2)):
    t=time.time(); L=ball(W,depth,r)
    print(f"Q(sqrt3,sqrt7,sqrt11) ball depth {depth} radius {r}: {len(L)} points "
          f"({time.time()-t:.0f}s)", flush=True)
    for i in (3,7,16):
        cs=spindle(i)
        if cs is None: print(f"  theta_{i}: not in this field", flush=True); continue
        mod=(cs[0]*cs[0]+cs[1]*cs[1])
        shell=sum(1 for p in L if abs(to_float(p.norm2())-i)<1e-9)
        if not shell:
            print(f"  theta_{i}: modulus 1 {mod.is_one()}, but 0 points at radius sqrt{i}",
                  flush=True); continue
        t=time.time()
        U=dedup(L+[rotate(p,cs) for p in L]); EU=edges(U)
        keep=kcore(len(U),EU,4); P2,E2=induced(U,EU,keep); tri=find_triangle(len(P2),E2)
        five=verify(P2,E2,triangle=tri) if tri else None
        print(f"  theta_{i}: {shell} points at radius sqrt{i}; union {len(U)}, "
              f"4-core {len(P2)}/{len(E2)}; chi>=5 {five}  ({time.time()-t:.0f}s)"
              + ("   <<<<< NEW JOINING ROTATION IN A NEW FIELD" if five else ""), flush=True)
PYEOF
