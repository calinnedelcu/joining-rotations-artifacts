#!/bin/sh
cd "$(dirname "$0")/.."
.venv/bin/python -u - > out/t16_verify.log 2>&1 <<'PYEOF'
import sys, time, collections; sys.path.insert(0,'.')
from hn.field import set_primes, K, Pt, is_unit
set_primes((3,7,11))
import hn.construct as C; C.refresh_field()
from hn.construct import unit_vector_family, ball, dedup, edges, rotate, to_float
from hn.io import save_points, save_edges
from hn.sat import find_triangle
from hn.minimise import verify, propose_core
from hn.graph import induced
log=lambda s: print(s, flush=True)
log("INDEPENDENT CHECK of theta_16 in Q(sqrt3, sqrt7, sqrt11)")
cs=(K.rat(31,32), K.root(7)*K.rat(3,32))
log(f"  rotation cos 31/32, sin 3*sqrt7/32; modulus exactly 1: "
    f"{(cs[0]*cs[0]+cs[1]*cs[1]).is_one()}")
W=unit_vector_family(2)
log(f"  lattice family: {len(W)} vectors, every one exactly at unit distance from 0: "
    f"{all(is_unit(Pt(K.zero(),K.zero()), w) for w in W)}")
L=ball(W,4,4.0)
shell=[p for p in L if abs(to_float(p.norm2())-16)<1e-9]
log(f"  ball {len(L)} points; {len(shell)} of them at radius exactly 4 "
    f"(exact check: {all(p.norm2()==K.rat(16) for p in shell)})")
R=[rotate(p,cs) for p in L]
U=dedup(L+R)
E=edges(U)
log(f"  union {len(U)} distinct points, {len(E)} edges")
bad=[(i,j) for i,j in E[:4000] if not is_unit(U[i],U[j])]
log(f"  re-checked the first 4000 edges exactly: {len(bad)} wrong")
def kcore(n,Ed,d):
    adj=collections.defaultdict(set)
    for u,v in Ed: adj[u].add(v); adj[v].add(u)
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
keep=kcore(len(U),E,4); P2,E2=induced(U,E,keep)
log(f"  4-core {len(P2)} points, {len(E2)} edges")
t=time.time(); slow=verify(P2,E2,triangle=None)
log(f"  NOT 4-colourable, assumption-free (no triangle pinned): {slow}  ({time.time()-t:.0f}s)")
t=time.time(); five=verify(P2,E2,k=5,triangle=None)
log(f"  5-colourable: {not five}  ({time.time()-t:.0f}s)")
save_points("out/t16_union.pts",P2); save_edges("out/t16_union.edge",len(P2),E2)
log(f"  saved out/t16_union.pts")
# first reduction pass, to see how far it falls
cur=list(range(len(P2)))
for it in range(8):
    t=time.time(); c=propose_core(P2,E2,cur)
    if c is None or len(c)>=len(cur):
        log(f"  core {it}: no smaller ({time.time()-t:.0f}s)"); break
    cur=c; log(f"  core {it}: {len(cur)} points  ({time.time()-t:.0f}s)")
Q,F=induced(P2,E2,sorted(cur))
save_points("out/t16_core.pts",Q); save_edges("out/t16_core.edge",len(Q),F)
log(f"  after core extraction: {len(Q)} vertices, {len(F)} edges"
    + ("   <<<<< BELOW THE 509 RECORD" if len(Q)<509 else ""))
PYEOF
