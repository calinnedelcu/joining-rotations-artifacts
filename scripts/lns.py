#!/usr/bin/env python3
"""Large neighbourhood search: destroy a region, rebuild it optimally.

Usage: lns.py [--start 509] [--radius 0.45] [--seed N] [--time SECONDS]
              [--pool-depth 4] [--pool-radius 2.7] [--minutes-per-window 2]

Every exact result in this repository holds one part of the graph fixed and
minimises the other, so a move that rewires BOTH parts at once escapes them
all. Searching both at once over a whole pool does not converge, because the
answer is not dense in it (docs/ATTEMPTS.md route 13).

This gets both properties at once. Take the current best graph, pick a disc in
the plane, and free every vertex inside it: those of the graph, which may
leave, and those of the surrounding lattice, which may join. Everything
outside the disc stays. The subproblem has a few dozen free variables and the
answer is dense in it, so the master settles it in seconds -- and when it
answers UNSAT it has PROVEN that no rewiring of that disc improves the graph.
Thousands of discs per hour, each one exact.

A disc that straddles the two parts rewires both of them together, which is
exactly the move the one-sided proofs cannot see.
"""
import os, sys, time, random, argparse, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn import load_vtx, verify, find_triangle
from hn.io import save_points, save_edges, load_points
from hn.graph import induced
from hn.construct import (unit_vector_family, ball, dedup, edges, theta4,
                          contains, pt_float, ORIGIN)
from hn.hitting import Master, Oracle, Extender, mono_edges
from hn.symmetry import rot60

D = os.path.join(os.path.dirname(__file__), "..", "data")
OUT = os.path.join(os.path.dirname(__file__), "..", "out")
ap = argparse.ArgumentParser()
ap.add_argument("--start", default="509",
                help="a name under data/vtx/, or a path to a .pts / .vtx file")
ap.add_argument("--radius", type=float, default=0.45, help="unused; kept for older commands")
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--time", type=float, default=None)
ap.add_argument("--pool-depth", type=int, default=4)
ap.add_argument("--pool-radius", type=float, default=2.7)
ap.add_argument("--max-free", type=int, default=70, help="window size: how many nearest points are freed")
ap.add_argument("--window-budget", type=float, default=120)
ap.add_argument("--pool", default=None, help="a .pts file to use as the pool instead")
ap.add_argument("--mode", default="disc", choices=["disc", "orbit", "hop"],
                help="window shape: a geometric disc, a union of rotation orbits, or a graph ball")
a = ap.parse_args()
rng = random.Random(a.seed)
log = lambda s: print(s, flush=True)

if a.start.endswith(".pts"):
    G = load_points(a.start)
elif a.start.endswith(".vtx"):
    G = load_vtx(a.start)
else:
    G = load_vtx(f"{D}/vtx/{a.start}.vtx")
if a.pool:
    P = load_points(a.pool)
else:
    W = unit_vector_family(2)
    L = ball(W, a.pool_depth, a.pool_radius)
    S = ball(W, 3, 2.5)
    P = dedup(L + [theta4(p) for p in S])
found, missing = contains(P, G)
if missing:
    P = dedup(list(P) + [G[i] for i in missing])
E = edges(P)
idx = {p.key(): i for i, p in enumerate(P)}
best = sorted(idx[p.key()] for p in G)
xy = [pt_float(p) for p in P]
log(f"pool {len(P)} points, {len(E)} edges; start {a.start} with {len(best)} vertices")
assert verify(P, E, best, triangle=None), "the start graph is not 5-chromatic"
log("start verified 5-chromatic")

adj = [[] for _ in range(len(P))]
for u, v in E:
    adj[u].append(v)
    adj[v].append(u)


def candidates(bestset, kmin=3):
    """Pool points worth adding: at least kmin neighbours already in the graph.

    Parts' own expansion rule, and without it a geometric window is useless --
    the lattice is about twenty times denser than the graph, so any disc big
    enough to hold a few graph vertices holds hundreds of lattice points.
    """
    out = []
    for v in range(len(P)):
        if v in bestset:
            continue
        c = 0
        for u in adj[v]:
            if u in bestset:
                c += 1
                if c >= kmin:
                    out.append(v)
                    break
    return out


def orbit_table(universe):
    """Group the universe into orbits of the 60-degree rotation.

    Parts worked on orbits, never on discs, and an orbit is a genuinely
    different neighbourhood: its six points are spread right around the graph,
    so freeing a few orbits rewires positions that no disc ever frees
    together.
    """
    idx = {P[i].key(): i for i in universe}
    seen, orbs = set(), []
    for i in universe:
        if i in seen:
            continue
        orb, q = [], P[i]
        for _ in range(6):
            j = idx.get(q.key())
            if j is not None:
                orb.append(j)
            q = rot60(q)
        orb = sorted(set(orb))
        seen |= set(orb)
        orbs.append(orb)
    return orbs


def hop_window(seed_v, size, uni):
    """A ball in the graph, grown breadth-first from one vertex."""
    out, frontier, seen = [], [seed_v], {seed_v}
    while frontier and len(out) < size:
        nxt = []
        for v in frontier:
            if v in uni:
                out.append(v)
                if len(out) >= size:
                    break
            for u in adj[v]:
                if u not in seen:
                    seen.add(u)
                    nxt.append(u)
        frontier = nxt
    return out


def window(centre, size, universe):
    """The `size` points of `universe` nearest the centre.

    A fixed radius wastes most attempts: the graph and the candidate set are
    unevenly spread, so a disc is either too poor to be worth solving or too
    rich to solve. Taking a fixed COUNT makes every window the right size, and
    the subproblem's difficulty stays predictable.
    """
    cx, cy = centre
    near = sorted(universe,
                  key=lambda i: (xy[i][0] - cx) ** 2 + (xy[i][1] - cy) ** 2)
    return near[:size]


def solve_window(bestset, free, budget):
    """Exactly minimise inside `free`, everything else in bestset kept.

    Returns a strictly better vertex set, or None if the window cannot be
    improved (which the master proves rather than guesses).
    """
    fixed = sorted(bestset - set(free))
    keepable = sorted(set(free) | set(fixed))
    remap = {v: i for i, v in enumerate(keepable)}
    pts, es = induced(P, E, keepable)
    nsub = len(keepable)
    fsub = [remap[v] for v in fixed]
    inside = [v for v in bestset if v in set(free)]
    bound = len(inside) - 1
    if bound < 0:
        return None
    oracle = Oracle(nsub, es)
    master = Master(nsub, es, degree_min=4, fixed=fsub)
    ext = Extender(nsub, es, iters=4000, seed=rng.randrange(1 << 30))
    startsub = sorted(remap[v] for v in inside)
    fixedset = set(fsub)

    def learn(Ssub):
        F = sorted(set(Ssub) | fixedset)
        col = oracle.model(F)
        M = mono_edges(es, ext.extend(col, F))
        if M:
            master.add_cut(M)
            return True
        return False

    # every single deletion from the start gives a cut for free
    for v in startsub:
        Sv = [u for u in startsub if u != v]
        if oracle.colourable(sorted(set(Sv) | fixedset)):
            learn(Sv)
    t0, out = time.time(), None
    while time.time() - t0 < budget:
        Ssub = master.solve(bound, prefer=startsub)
        if Ssub is None:
            break                                  # proven: this window cannot improve
        F = sorted(set(Ssub) | fixedset)
        if oracle.colourable(F):
            if not learn(Ssub):
                break
            continue
        cand = sorted(keepable[i] for i in F)
        if verify(P, E, cand, triangle=None):
            out = cand
            break
        log("   oracle and fresh verification disagree -- stopping this window")
        break
    oracle.close()
    master.close()
    return out


def save(bestset):
    tag = "lns_%s_%s_%d" % (os.path.basename(a.start).split(".")[0], a.mode, a.seed)
    P2, E2 = induced(P, E, sorted(bestset))
    save_points(f"{OUT}/{tag}.pts", P2)
    save_edges(f"{OUT}/{tag}.edge", len(P2), E2)


bestset = set(best)
cand = candidates(bestset)
universe = sorted(bestset | set(cand))
log(f"{len(cand)} pool points have >= 3 neighbours in the graph; "
    f"windows are drawn from {len(universe)} points")
orbs = orbit_table(universe) if a.mode == "orbit" else None
if orbs:
    log(f"orbit mode: {len(orbs)} orbits of the 60-degree rotation")
uniset = set(universe)
t0 = time.time()
step = proven = improved = skipped = 0
while a.time is None or time.time() - t0 < a.time:
    step += 1
    if a.mode == "orbit":
        free, pick = [], rng.sample(orbs, min(len(orbs), 1 + a.max_free // 6))
        for o in pick:
            free += o
        free = free[:a.max_free]
    elif a.mode == "hop":
        free = hop_window(rng.choice(sorted(bestset)), a.max_free, uniset)
    else:
        centre = xy[rng.choice(sorted(bestset))]
        centre = (centre[0] + rng.uniform(-0.15, 0.15), centre[1] + rng.uniform(-0.15, 0.15))
        free = window(centre, a.max_free, universe)
    inside = [v for v in free if v in bestset]
    if len(inside) < 4:
        skipped += 1
        continue
    res = solve_window(bestset, free, a.window_budget)
    if res is not None and len(res) < len(bestset):
        bestset = set(res)
        improved += 1
        cand = candidates(bestset)
        universe = sorted(bestset | set(cand))
        uniset = set(universe)
        if a.mode == "orbit":
            orbs = orbit_table(universe)
        save(bestset)
        log(f"[{step}] *** IMPROVED to {len(bestset)} vertices"
            + ("   <<< BELOW THE 509 RECORD" if len(bestset) < 509 else "")
            + f"  ({time.time()-t0:.0f}s)")
    else:
        proven += 1
    if step % 25 == 0:
        log(f"[{step}] best {len(bestset)} | windows proven optimal {proven} | "
            f"improvements {improved} | skipped {skipped} | {time.time()-t0:.0f}s")
log(f"done: best {len(bestset)} vertices after {step} windows, "
    f"{proven} of them proven unimprovable")
save(bestset)
