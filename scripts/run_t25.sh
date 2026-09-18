#!/bin/sh
cd "$(dirname "$0")/.."
.venv/bin/python -u - > out/t19_t25.log 2>&1 <<'PYEOF'
import sys, time, collections; sys.path.insert(0,'.')
from hn.field import K
from hn.construct import unit_vector_family, ball, dedup, edges, rotate, to_float
from hn.io import save_points, save_edges
from hn.sat import find_triangle
from hn.minimise import verify
from hn.graph import induced
log=lambda s: print(f"[{time.strftime('%H:%M:%S')}] {s}", flush=True)
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
W=unit_vector_family(2)
t=time.time(); L=ball(W,5,5.0)
log(f"classical field, depth 5 radius 5: {len(L)} points ({time.time()-t:.0f}s)")
# theta_19: sin = 5 sqrt3/38 ; theta_25: sin = 3 sqrt11/50 -- both in Q(sqrt3,sqrt5,sqrt11)
for i,cs in ((19,(K.rat(37,38), K.root(3)*K.rat(5,38))),
             (25,(K.rat(49,50), K.root(11)*K.rat(3,50)))):
    assert (cs[0]*cs[0]+cs[1]*cs[1]).is_one()
    shell=sum(1 for p in L if abs(to_float(p.norm2())-i)<1e-9)
    log(f"theta_{i} = arccos({2*i-1}/{2*i}): {shell} points at radius sqrt{i}")
    if not shell: continue
    t=time.time()
    U=dedup(L+[rotate(p,cs) for p in L])
    log(f"  union {len(U)} points, computing edges...")
    E=edges(U)
    log(f"  {len(E)} edges ({time.time()-t:.0f}s); reducing and colouring...")
    t=time.time()
    keep=kcore(len(U),E,4); P2,E2=induced(U,E,keep); tri=find_triangle(len(P2),E2)
    five=verify(P2,E2,triangle=tri) if tri else None
    log(f"  4-core {len(P2)}/{len(E2)}; chi>=5 {five}  ({time.time()-t:.0f}s)"
        + ("   <<<<< NEW JOINING ROTATION IN THE CLASSICAL FIELD" if five else ""))
    if five:
        save_points(f"out/cl_t{i}.pts",P2); save_edges(f"out/cl_t{i}.edge",len(P2),E2)
        log(f"    saved out/cl_t{i}.pts")
PYEOF
