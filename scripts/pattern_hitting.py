#!/usr/bin/env python3
"""Minimum small part for a given large part, through its colour patterns.

The large part L is replaced by the finite set of colour patterns it leaves
on its interface (scripts/patterns.py): S works with L iff S blocks every
pattern.  One master (hn.hitting.Master) proposes S; one oracle PER PATTERN
-- the S-pool plus the 19 interface points with their colours fixed -- says
whether S blocks that pattern.  Every pattern S fails to block yields cuts
(a Tabucol extension and a grown minimal correction set), so an iteration
learns up to one cut per unblocked pattern, and each oracle call is on a
~200-vertex graph instead of the 556-vertex L union theta_4(S-pool).

Usage: pattern_hitting.py [--Lfile v374e1860.vtx] [--pool parts|ball|ball30]
                          [--bound B] [--time SECONDS] [--seed N] [--grow N]
"""
import os, sys, glob, argparse, time, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn import load_vtx, verify
from hn.io import save_points, save_edges
from hn.graph import induced
from hn.sat import Colouring
from hn.construct import edges, theta4, dedup, unit_vector_family, ball, ORIGIN
from hn.hitting import Master, Oracle, Extender, kcore, mono_edges
from patterns import patterns as enumerate_patterns

D = os.path.join(os.path.dirname(__file__), "..", "data", "parts")
OUT = os.path.join(os.path.dirname(__file__), "..", "out")
ap = argparse.ArgumentParser()
ap.add_argument("--Lfile", default="v374e1860.vtx")
ap.add_argument("--Sfile", default="v136e564.vtx")
ap.add_argument("--pool", default="parts")
ap.add_argument("--bound", type=int, default=None)
ap.add_argument("--time", type=float, default=None)
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--grow", type=int, default=1)
ap.add_argument("--tabu", type=int, default=10000)
a = ap.parse_args()
rng = random.Random(a.seed)
log = lambda s: print(s, flush=True)

L = load_vtx(f"{D}/{a.Lfile}")
S = load_vtx(f"{D}/{a.Sfile}")
Ssizes = (136, 141, 150, 166, 167, 172)
if a.pool == "parts":
    poolS = []
    for f in sorted(glob.glob(f"{D}/v*.vtx")):
        if int(os.path.basename(f)[1:].split("e")[0]) in Ssizes:
            poolS += load_vtx(f)
elif a.pool == "ball":
    poolS = ball(unit_vector_family(1), 3, 2.45)
elif a.pool == "ball30":
    poolS = ball(unit_vector_family(2), 3, 2.45)
poolS = [p for p in dedup(S + poolS) if p.key() != ORIGIN.key()]
RS = [theta4(p) for p in poolS]

iface, _, pats = enumerate_patterns(L)
k = len(iface)
P = [L[v] for v in iface] + RS
E = edges(P)
n = len(P)
fixed = list(range(k))
fixedset = set(fixed)
Skeys = {theta4(p).key() for p in S}
start = sorted(i for i, p in enumerate(P) if i >= k and p.key() in Skeys)
log(f"L {a.Lfile}: {len(pats)} patterns on {k} interface vertices; S pool {a.pool}: "
    f"{len(RS)} candidates; working graph {n} vertices {len(E)} edges; start {len(start)} free")

core = kcore(n, E, 4)
adj = [[] for _ in range(n)]
for u, v in E:
    adj[u].append(v)
    adj[v].append(u)
oracles = [Oracle(n, E, fixed_colours={i: pat[i] for i in range(k)}) for pat in pats]
master = Master(n, E, degree_min=4, allowed=core, fixed=fixed)
ext = Extender(n, E, iters=a.tabu, seed=a.seed)
t0 = time.time()


def blocks_all(Sfree):
    """Index of the first pattern S does not block, or None."""
    F = sorted(set(Sfree) | fixedset)
    for j, o in enumerate(oracles):
        if o.colourable(F):
            return j
    return None


def learn(Sfree, j, grow):
    """Pattern j is not blocked by S: cuts from its colouring."""
    F = sorted(set(Sfree) | fixedset)
    o = oracles[j]
    col = o.model(F)
    ext_col = ext.extend(col, F)
    M = mono_edges(E, ext_col)
    if not M:
        return 0, 0
    master.add_cut(M)
    d = 0
    if grow:
        touched = {u for e in M for u in e} - fixedset
        T = set(F) | (set(core) - touched)
        colx = list(ext_col)
        changed = True
        while changed:
            changed = False
            for v in list(touched):
                used = {colx[u] for u in adj[v] if u in T}
                if len(used) < 4:
                    colx[v] = next(c for c in range(4) if c not in used)
                    T.add(v)
                    touched.discard(v)
                    changed = True
        Dset = []
        for v in sorted(touched, key=lambda v: rng.random()):
            if o.colourable(T | {v}):
                T.add(v)
            else:
                Dset.append(v)
        if Dset:
            master.add_vertex_cut(Dset)
            d = len(Dset)
    return len(M), d


# sanity: the start blocks every pattern
assert blocks_all(start) is None, "start small part does not block every pattern"
best = start
bound = a.bound if a.bound is not None else len(best) - 1

# bootstrap 1: vertex-critical colourings of the start, for every pattern
t = time.time()
cnt = 0
for v in best:
    Sv = [u for u in best if u != v]
    for j in range(len(pats)):
        if oracles[j].colourable(sorted(set(Sv) | fixedset)):
            learn(Sv, j, grow=True)
            cnt += 1
log(f"bootstrap: {cnt} (vertex, pattern) certificates, cuts={master.cuts}  ({time.time()-t:.0f}s)")
# bootstrap 2: essential vertices per pattern
t = time.time()
free = [v for v in core if v not in fixedset]
ess = 0
for v in free:
    Sv = [u for u in free if u != v]
    for j in range(len(pats)):
        if oracles[j].colourable(sorted(set(Sv) | fixedset)):
            master.add_vertex_cut([v])
            learn(Sv, j, grow=True)
            ess += 1
            break
log(f"bootstrap: {ess} essential vertices out of {len(free)}, cuts={master.cuts}  ({time.time()-t:.0f}s)")


def save(best):
    tag = f"pat_{a.Lfile.split('.')[0]}_{a.pool}_{a.seed}"
    keep = sorted(set(best) | fixedset)
    P2, E2 = induced(P, E, keep)
    save_points(f"{OUT}/best_{tag}.pts", P2)
    save_edges(f"{OUT}/best_{tag}.edge", len(P2), E2)


it = 0
proven = False
while True:
    if a.time and time.time() - t0 > a.time:
        log("time limit")
        break
    it += 1
    t = time.time()
    Sp = master.solve(bound, prefer=best)
    tm = time.time() - t
    if Sp is None:
        log(f"[{it}] master UNSAT at bound {bound}: no small part with <= {bound} free vertices "
            f"blocks all {len(pats)} patterns over this pool.  ({tm:.1f}s, total {time.time()-t0:.0f}s)")
        proven = True
        break
    j = blocks_all(Sp)
    if j is None:
        # blocks every pattern: verify against the real large part, then shrink
        Lfull = L + [P[v] for v in Sp]
        Ef = edges(Lfull)
        ok = verify(Lfull, Ef, triangle=None)
        log(f"[{it}] *** candidate with {len(Sp)} free vertices blocks all patterns; "
            f"full graph L union theta_4(S) with {len(Lfull)} vertices: chi=5 is {ok}")
        if not ok:
            log("BUG: pattern oracle and full verification disagree")
            break
        # greedy shrink
        kept = set(Sp)
        for v in sorted(Sp, key=lambda v: rng.random()):
            if blocks_all(kept - {v}) is None:
                kept.discard(v)
        best = sorted(kept)
        bound = len(best) - 1
        save(best)
        log(f"[{it}] *** small part shrunk to {len(best)} free vertices -> graph on "
            f"{len(L) + len(best)} vertices; new bound {bound}")
        continue
    # learn from every unblocked pattern
    learned = 0
    msum = 0
    for jj in range(j, len(pats)):
        F = sorted(set(Sp) | fixedset)
        if oracles[jj].colourable(F):
            m, d = learn(Sp, jj, grow=(a.grow and it % a.grow == 0))
            learned += 1
            msum += m
    if it % 10 == 0 or it < 5:
        log(f"[{it}] |S|={len(Sp)} unblocked patterns {learned}, avg mono edges {msum/max(learned,1):.1f} "
            f"(cuts={master.cuts}, master {tm:.1f}s, {time.time()-t0:.0f}s)")
log(f"best: {len(best)} free vertices (+ origin) -> {len(L) + len(best)} total; proven: {proven}")
