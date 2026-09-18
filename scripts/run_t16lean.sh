#!/bin/sh
cd "$(dirname "$0")/.."
.venv/bin/python -u - > out/t16lean.log 2>&1 <<'PYEOF'
import sys, time, collections; sys.path.insert(0,'.')
from hn.field import set_primes, K
set_primes((3,7,11))
import hn.construct as C; C.refresh_field()
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
cs=(K.rat(31,32), K.root(7)*K.rat(3,32))
W=unit_vector_family(2)
# theta_16 needs the shell at radius exactly 4, so the ball must reach 4 -- but it
# need not be SOLID out to 4.  Clipping the intermediate Minkowski steps keeps the
# shell and throws away the bulk (Heule's V_151 trick).
for step in (3.0, 3.2, 3.5):
    t=time.time()
    L=ball(W,4,4.0,step_radius=step)
    shell=sum(1 for p in L if abs(to_float(p.norm2())-16)<1e-9)
    if not shell:
        log(f"step_radius {step}: {len(L)} points, no radius-4 shell survives"); continue
    U=dedup(L+[rotate(p,cs) for p in L]); E=edges(U)
    keep=kcore(len(U),E,4); P2,E2=induced(U,E,keep); tri=find_triangle(len(P2),E2)
    five=verify(P2,E2,triangle=tri) if tri else None
    log(f"step_radius {step}: ball {len(L)}, shell {shell}, union {len(U)}, "
        f"4-core {len(P2)}/{len(E2)}; chi>=5 {five}  ({time.time()-t:.0f}s)"
        + ("   <<<<< a leaner 5-chromatic start" if five else ""))
    if five:
        save_points(f"out/t16lean_{step}.pts",P2); save_edges(f"out/t16lean_{step}.edge",len(P2),E2)
        log(f"   saved out/t16lean_{step}.pts")
PYEOF
