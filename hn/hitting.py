"""Minimum 5-chromatic subgraph of a pool, as an implicit hitting set.

The pool U is a point set with its unit-distance edges.  We want the
smallest S subset of U such that U[S] is not 4-colourable.

    master:  find S with |S| <= bound, every vertex of S having >= 4
             neighbours in S, satisfying every cut learned so far
    oracle:  is U[S] 4-colourable?
             no  -> S is a 5-chromatic graph; shrink it, lower the bound
             yes -> extend the colouring to all of U with as few
                    monochromatic edges as possible, and add the cut
                    "S must contain both ends of one of those edges"

Why the cut is valid: if S avoids every monochromatic pair of a colouring
c of U, then c restricted to S is a proper 4-colouring of U[S].

When the master says UNSAT, no 5-chromatic subgraph of U with <= bound
vertices exists: the last graph found is provably the minimum over U.
Greedy deletion can never say that.  (Same object as co-certificate
learning in SAT modulo symmetries, Kirchweger-Peitl-Szeider 2023, and as
smallest-MUS extraction by hitting-set dualisation, Ignatiev et al. 2015.)

The degree constraint is sound because a minimum 5-chromatic graph is
vertex-critical, and a vertex-critical 5-chromatic graph has minimum
degree >= 4 (Dirac).  It is what stops the master from proposing scattered
sets that no colouring could refute efficiently.

Three safety properties, all enforced here:

  * The oracle pins one triangle's colours only CONDITIONALLY, through the
    selector literals of its three vertices, so its UNSAT cores are sound
    (docs/CONTEXT.md trap (a) is about unconditional pinning).
  * Every graph reported is re-verified by `minimise.verify` in a fresh
    solver with no assumptions and no symmetry breaking.
  * The cardinality bound is imposed by assumption on a totalizer output,
    never by a permanent clause, so the master stays incremental.
"""
from __future__ import annotations
import os
import random
import time
from pysat.solvers import Solver
from pysat.card import CardEnc, EncType, ITotalizer
from .sat import Colouring, find_triangle
from .minimise import verify
from .graph import induced, degrees


# ---------------------------------------------------------------------------
def kcore(n, edges, kmin=4):
    """Vertices surviving iterated deletion of degree < kmin.  Sound pruning:
    a minimum 5-chromatic subgraph is vertex-critical, hence has min degree 4."""
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    alive = set(range(n))
    todo = [v for v in alive if len(adj[v]) < kmin]
    while todo:
        v = todo.pop()
        if v not in alive:
            continue
        alive.discard(v)
        for u in adj[v]:
            adj[u].discard(v)
            if u in alive and len(adj[u]) < kmin:
                todo.append(u)
    return sorted(alive)


# ---------------------------------------------------------------------------
class Oracle:
    """Persistent 4-colourability oracle under selector assumptions."""

    def __init__(self, n, edges, k=4, triangle=None, solver="cadical195",
                 fixed_colours=None):
        self.n, self.k = n, k
        self.C = Colouring(n, edges, k=k, solver=solver, selectors=True)
        for v, c in (fixed_colours or {}).items():
            self.C.solver.add_clause([self.C.var(v, c)])
        if triangle is not None and fixed_colours:
            triangle = None            # colours are already pinned by the pattern
        if triangle is not None:
            sel = [-self.C.s(v) for v in triangle]
            for col, v in enumerate(triangle[:k]):
                # "if all three are selected, they take colours 0,1,2"
                self.C.solver.add_clause(sel + [self.C.var(v, col)])
        self.calls = 0

    def colourable(self, S):
        self.calls += 1
        return self.C.colourable(S)

    def colourable_limited(self, S, conflicts=20000):
        """True / False / None (budget exhausted).  Used where an answer of
        'don't know' is acceptable, e.g. growing correction sets on a big
        pool, where one hard UNSAT proof must not stall the loop."""
        self.calls += 1
        asm = [self.C.s(v) for v in S]
        self.C.solver.conf_budget(conflicts)
        return self.C.solver.solve_limited(assumptions=asm)

    def model(self, S):
        """Colouring of the vertices of S after a SAT answer (-1 elsewhere)."""
        m = set(l for l in self.C.solver.get_model() if l > 0)
        col = [-1] * self.n
        for v in S:
            for c in range(self.k):
                if self.C.var(v, c) in m:
                    col[v] = c
                    break
        return col

    def core(self):
        return self.C.core()

    def close(self):
        self.C.close()


# ---------------------------------------------------------------------------
class Master:
    """SAT master: x_v = keep v; z_uv -> x_u & x_v; cuts are clauses over z."""

    def __init__(self, n, edges, degree_min=4, solver="cadical195",
                 allowed=None, fixed=(), orbits=None):
        self.n = n
        self.solver = Solver(name=solver)
        self.top = n
        self.z = {}
        self.cls = []
        self.cuts = 0
        self.units = set()
        self.fixed = set(fixed)
        allowed = set(range(n)) if allowed is None else set(allowed)
        allowed |= self.fixed
        adj = [[] for _ in range(n)]
        for a, b in edges:
            if a in allowed and b in allowed:
                adj[a].append(b)
                adj[b].append(a)
        for v in self.fixed:
            self._add([self.x(v)])
        self.free = [v for v in range(n) if v not in self.fixed]
        for v in self.free:
            nfixed = sum(1 for u in adj[v] if u in self.fixed)
            need = degree_min - nfixed
            if v not in allowed or len(adj[v]) < degree_min:
                self._add([-self.x(v)])
                continue
            lits = [self.x(u) for u in adj[v] if u not in self.fixed]
            if need <= 0:
                continue
            if len(lits) < need:
                self._add([-self.x(v)])
                continue
            enc = CardEnc.atleast(lits=lits, bound=need, top_id=self.top,
                                  encoding=EncType.seqcounter)
            self.top = max(self.top, enc.nv)
            for cl in enc.clauses:
                self._add([-self.x(v)] + cl)
        if orbits:
            # Impose a symmetry on the SEARCH, not on the answer: every orbit
            # is taken whole or not at all.  This is roadmap step 4, and it is
            # only a few equivalence clauses -- the cardinality machinery still
            # counts vertices, so nothing else changes.  It restricts the
            # search to symmetric solutions, which is exponentially stronger
            # than breaking symmetry, and is what lets the pool be thousands of
            # points instead of hundreds.  It can miss an asymmetric optimum:
            # use it to FIND candidates, then re-run without it.
            for orb in orbits:
                rep = orb[0]
                for v in orb[1:]:
                    self._add([-self.x(rep), self.x(v)])
                    self._add([-self.x(v), self.x(rep)])
        self.tot = None
        self.tot_bound = None

    def _add(self, clause):
        """Add a clause and keep a copy, so the instance can be dumped.

        PySAT does not expose the clauses a solver holds, and an UNSAT answer
        from the master is the one claim here that cannot be rechecked without
        rerunning the search.  Keeping them costs a few megabytes and makes the
        instance exportable.
        """
        self.cls.append(list(clause))
        self.solver.add_clause(clause)

    def x(self, v):
        return v + 1

    def zvar(self, u, v):
        e = (u, v) if u < v else (v, u)
        z = self.z.get(e)
        if z is None:
            self.top += 1
            z = self.top
            self.z[e] = z
            self._add([-z, self.x(e[0])])
            self._add([-z, self.x(e[1])])
        return z

    def add_cut(self, mono_edges):
        """S must contain both endpoints of one of these edges."""
        cl = sorted({self.zvar(u, v) for u, v in mono_edges})
        assert cl, "a cut with no edges would be unsatisfiable"
        self._add(cl)
        self.cuts += 1

    def add_vertex_cut(self, vertices):
        """S must contain one of these vertices (weaker, but sometimes free)."""
        vertices = list(vertices)
        self._add([self.x(v) for v in vertices])
        self.cuts += 1
        if len(vertices) == 1:
            self.units.add(vertices[0])

    def _ensure_totalizer(self, bound):
        if self.tot is None or bound > self.tot_bound:
            if self.tot is not None:
                self.tot.delete()
            self.tot = ITotalizer(lits=[self.x(v) for v in self.free],
                                  ubound=bound, top_id=self.top)
            self.top = self.tot.top_id
            self.tot_bound = bound
            for cl in self.tot.cnf.clauses:
                self._add(cl)

    def dump(self, path, bound):
        """Write the master at this bound as DIMACS, for independent checking.

        An UNSAT answer from the master is the one claim here that cannot be
        rechecked without rerunning the search, which is exactly what a referee
        would object to.  Dumping the instance fixes that: the file contains
        every clause the master holds plus the cardinality bound as unit
        clauses, so `cadical file.cnf` re-derives the same UNSAT from scratch,
        and `cadical --lrat=proof file.cnf` emits a certificate that cake_lpr
        can check without trusting any of this code.
        """
        self._ensure_totalizer(bound)
        cls = [list(c) for c in self.cls]
        cls.append([-self.tot.rhs[bound]])
        nv = max(abs(l) for c in cls for l in c)
        with open(path, "w") as f:
            f.write(f"p cnf {nv} {len(cls)}\n")
            for c in cls:
                f.write(" ".join(map(str, c)) + " 0\n")
        return path

    def solve(self, bound, prefer=None):
        """A set S of at most `bound` vertices satisfying every cut, or None."""
        self._ensure_totalizer(bound)
        if prefer is not None:
            pref = set(prefer)
            self.solver.set_phases([self.x(v) if v in pref else -self.x(v)
                                    for v in range(self.n)])
        ok = self.solver.solve(assumptions=[-self.tot.rhs[bound]])
        if not ok:
            return None
        m = self.solver.get_model()
        return [v for v in self.free if m[v] > 0]

    def close(self):
        self.solver.delete()


# ---------------------------------------------------------------------------
def mono_edges(edges, col):
    return [(a, b) for a, b in edges if col[a] >= 0 and col[a] == col[b]]


class Extender:
    """Extend a proper colouring of S to all of U with few monochromatic
    edges: greedy first, then Tabucol with S frozen."""

    def __init__(self, n, edges, k=4, iters=20000, seed=0):
        from .colour import ConflictColouring, greedy_extend
        self.n, self.edges, self.k, self.iters = n, edges, k, iters
        self.greedy = greedy_extend
        self.tabu = ConflictColouring(n, edges, k=k, seed=seed)

    def extend(self, col, frozen, iters=None):
        full = self.greedy(self.n, self.edges, self.k, col)
        best, conf = self.tabu.run(self.iters if iters is None else iters,
                                   init=full, fixed=frozen)
        return best


# ---------------------------------------------------------------------------
def shrink_verified(points, edges, S, fixed, triangle, rng, check=verify):
    """Greedy deletion inside S (never touching `fixed`), each step verified
    in a fresh solver.  Returns the surviving free vertices."""
    fixed = set(fixed)
    order = [v for v in S if v not in fixed and (triangle is None or v not in triangle)]
    rng.shuffle(order)
    kept = set(S) - fixed
    for v in order:
        trial = sorted((kept - {v}) | fixed)
        if check(points, edges, trial, triangle=triangle):
            kept.discard(v)
    return sorted(kept)


def search(points, edges, start=None, bound=None, max_iters=10**9,
           time_limit=None, cuts_per_iter=2, tabu_iters=20000, seed=0,
           log=print, degree_min=4, bootstrap_critical=True,
           solver="cadical195", on_improve=None, fixed=(),
           bootstrap_essential=True, grow_every=10, bootstrap_pairs=0,
           fixed_colours=None, grow_budget=20000, essential_budget=None,
           orbits=None, dump_unsat=None, require_any=None):
    """The loop.  Returns (best_vertex_list or None, proven_optimal: bool).

    `start`: a vertex list known (or believed) to induce a 5-chromatic graph
    together with `fixed`; it seeds the bound and the vertex-critical
    bootstrap cuts.  `fixed`: companion vertices that are always kept and
    not counted -- e.g. the small part S_136 while the large part is
    minimised.  All vertex lists returned exclude the fixed vertices.
    """
    rng = random.Random(seed)
    n = len(points)
    t0 = time.time()
    fixed = sorted(set(fixed))
    fixedset = set(fixed)
    core = kcore(n, edges, degree_min)
    coreset = set(core) | fixedset
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    log(f"pool {n} vertices, {len(edges)} edges; {degree_min}-core has {len(core)}; fixed {len(fixed)}")
    tri = find_triangle(n, edges)
    if tri is not None and not set(tri) <= coreset:
        tri = None
    oracle = Oracle(n, edges, triangle=tri, solver=solver, fixed_colours=fixed_colours)
    master = Master(n, edges, degree_min=degree_min, solver=solver, allowed=core,
                    fixed=fixed, orbits=orbits)
    if require_any:
        # "at least one of these vertices is used".  Sound whenever a SUBSET of
        # this pool has already been proved to contain no answer at this bound:
        # an answer here must then use something the smaller pool lacked.  It is
        # how a proof over a dense pool buys search in the next one out.
        master._add([master.x(v) for v in sorted(set(require_any))])
        log(f"constraint: any answer must use one of {len(set(require_any))} "
            f"specified vertices")
    ext = Extender(n, edges, iters=tabu_iters, seed=seed)

    def full(S):
        return sorted(set(S) | fixedset)

    check = verify
    if fixed_colours:
        # independent re-verification must impose the same colour pattern
        from .sat import Colouring as _Col
        from .graph import induced as _ind

        def check(points, edges, keep, triangle=None, k=4):
            keep = sorted(keep)
            pts, es = _ind(points, edges, keep)
            idx = {v: i for i, v in enumerate(keep)}
            c = _Col(len(pts), es, k=k, selectors=False)
            for v, col in fixed_colours.items():
                if v in idx:
                    c.solver.add_clause([c.var(idx[v], col)])
            try:
                return not c.colourable()
            finally:
                c.close()

    def ok_tri(S):
        return tri if tri and set(tri) <= set(S) else None

    best = None
    if start is not None:
        start = sorted((set(start) & coreset) - fixedset)
        assert check(points, edges, full(start), triangle=ok_tri(full(start))), \
            "start (with the fixed vertices) is not 5-chromatic"
        best = start
        log(f"start: {len(best)} free vertices (+{len(fixed)} fixed), verified 5-chromatic")
    if bound is None:
        bound = (len(best) - 1) if best is not None else len(core)

    def learn(S):
        """S (+ fixed) is 4-colourable (oracle just said SAT).  Add cuts.

        Cut 1 freezes S and the fixed part and repairs the rest: it cuts S
        off.  Cut 2 keeps only the fixed part frozen and lets Tabucol move
        S's own colours too: usually fewer monochromatic edges, so a
        stronger cut, though not necessarily one that excludes S.
        """
        F = full(S)
        col = oracle.model(F)
        ext_col = ext.extend(col, F)
        M = mono_edges(edges, ext_col)
        assert M, "an extension with no conflicts would 4-colour the pool"
        master.add_cut(M)
        first = len(M)
        for j in range(1, cuts_per_iter):
            ext_col = ext.extend(ext_col, fixed, iters=tabu_iters // 2)
            M2 = mono_edges(edges, ext_col)
            if M2 and set(M2) != set(M):
                master.add_cut(M2)
        return first

    def grow(S, M, col, max_calls=60):
        """Minimal-ish correction set.  Start from T = S + fixed + every pool
        vertex not touched by a monochromatic edge of the extension `col`
        (c is proper there).  Add back touched vertices greedily whenever a
        colour is free at them (no SAT call), then by SAT calls, at most
        `max_calls` of them.  Whatever is left is D: T = pool - D is
        4-colourable, so every 5-chromatic subgraph contains a vertex of D.
        """
        touched = {u for e in M for u in e} - fixedset
        T = set(full(S)) | (set(core) - touched)
        col = list(col)
        # greedy: a touched vertex with a free colour among T-neighbours joins T
        changed = True
        while changed:
            changed = False
            for v in list(touched):
                used = {col[u] for u in adj[v] if u in T}
                if len(used) < 4:
                    col[v] = next(c for c in range(4) if c not in used)
                    T.add(v)
                    touched.discard(v)
                    changed = True
        rest = sorted(touched, key=lambda v: rng.random())
        D = []
        calls = 0
        for v in rest:
            if calls >= max_calls:
                D.append(v)
                continue
            calls += 1
            if oracle.colourable_limited(T | {v}, grow_budget):
                T.add(v)
            else:
                D.append(v)          # UNSAT or unknown: leaving v out keeps T colourable
        if D:
            master.add_vertex_cut(D)
        return len(D), calls

    def peel(S):
        """Remove vertices of degree < degree_min, cascading.  Free and exact.

        If G is 5-chromatic and deg(v) < degree_min = 4, then G - v is still
        5-chromatic: a proper 4-colouring of G - v leaves one of the 4 colours
        unused among v's <= 3 neighbours, so it would extend to G.  So these
        vertices can be dropped with no SAT call at all, and each drop can put
        a neighbour below the threshold -- hence the cascade.
        """
        keep = set(S)
        deg = {v: sum(1 for u in adj[v] if u in keep or u in fixedset)
               for v in keep}
        stack = [v for v in keep if deg[v] < degree_min]
        while stack:
            v = stack.pop()
            if v not in keep:
                continue
            keep.discard(v)
            for u in adj[v]:
                if u in keep:
                    deg[u] -= 1
                    if deg[u] < degree_min:
                        stack.append(u)
        return sorted(keep)

    # bootstrap: vertex-critical cuts from the start graph
    if best is not None and bootstrap_critical:
        t = time.time()
        sizes = []
        # The order decides where a greedy pass lands: two runs over the same
        # graph in index order do the same work and reach the same graph, which
        # is waste when several are running.  Shuffling with the run's own rng
        # makes each seed explore a different minimal graph, and costs nothing.
        todo = list(best)
        rng.shuffle(todo)
        bestset = set(best)
        for i, v in enumerate(todo):
            if v not in bestset:
                continue            # already taken by a cascade
            if i and i % 100 == 0:
                # Without this the log is silent for hours on a graph that is
                # already critical, and there is no way to tell a slow pass
                # from a stuck one.
                log(f"  [{i}/{len(todo)}] {len(best)} vertices, {master.cuts} "
                    f"cuts  ({time.time()-t:.0f}s)")
            S = [u for u in best if u != v]
            if oracle.colourable(full(S)):
                sizes.append(learn(S))
            else:
                # best minus v is still 5-chromatic: best was not critical.
                # Peeling costs nothing and often takes several more with it.
                S2 = peel(S)
                free = len(S) - len(S2)
                best = S2
                bestset = set(best)
                bound = min(bound, len(best) - 1)
                log(f"  [{i+1}/{len(todo)}] start graph not critical: "
                    f"dropped {v}" + (f" +{free} peeled" if free else "")
                    + f" -> {len(best)}")
                # Save every drop.  This pass costs one SAT call per vertex and
                # can run for hours; without this, a crash or a stray kill
                # throws the whole descent away (it happened).
                if on_improve is not None:
                    on_improve(best)
        log(f"bootstrap: {master.cuts} cuts from {len(best)} critical colourings, "
            f"mono edges per cut min/avg/max {min(sizes)}/{sum(sizes)/len(sizes):.1f}/{max(sizes)}  ({time.time()-t:.0f}s)")

    # bootstrap: essential vertices.  If pool - v is 4-colourable then every
    # 5-chromatic subgraph of the pool contains v: a unit clause, plus the
    # edge cut of that colouring (all of whose monochromatic edges touch v).
    if bootstrap_essential:
        t = time.time()
        ess = 0
        pool_free = [v for v in core if v not in fixedset]
        # With a symmetry imposed, orbits are taken whole or not at all, so the
        # question that matters is whether the pool survives losing a whole
        # ORBIT, not one vertex.  That is also what makes it affordable: one
        # UNSAT proof per orbit instead of per vertex, and on a 2365-vertex pool
        # with 788 orbits the difference is hours against days.
        groups = ([sorted(set(o) & set(pool_free)) for o in orbits]
                  if orbits else [[v] for v in pool_free])
        groups = [g for g in groups if g]
        unknown = 0
        for g in groups:
            gs = set(g)
            S = [u for u in pool_free if u not in gs]
            r = (oracle.colourable(full(S)) if essential_budget is None
                 else oracle.colourable_limited(full(S), essential_budget))
            if r:
                master.add_vertex_cut(g)
                learn(S)
                ess += 1
            elif r is None:
                unknown += 1
            if time_limit and time.time() - t0 > time_limit:
                break
        log(f"bootstrap: {ess} essential {'orbits' if orbits else 'vertices'} "
            f"out of {len(groups)}"
            f"{f', {unknown} undecided' if unknown else ''} "
            f"(cuts={master.cuts})  ({time.time()-t:.0f}s)")
        # size-2 minimal correction sets: pairs of non-essential vertices
        # whose joint removal 4-colours the pool (Parts' degree-2
        # hyperedges).  Only affordable on small pools: bootstrap_pairs is
        # the maximum number of non-essential vertices to enumerate over.
        if bootstrap_pairs and ess < len(pool_free):
            t = time.time()
            cand = [v for v in pool_free if v not in master.units]
            # Enumerating every pair is quadratic, so on a pool with hundreds of
            # non-essential vertices it is unaffordable.  Skipping it entirely
            # is worse: without size-2 correction sets these pools never
            # converge at all.  So above the cap, SAMPLE pairs at random up to
            # the same budget the cap implies.  Fewer cuts, but the right kind.
            budget = bootstrap_pairs * (bootstrap_pairs - 1) // 2
            if len(cand) <= bootstrap_pairs:
                todo = [(cand[i], w) for i in range(len(cand)) for w in cand[i + 1:]]
            else:
                todo = []
                seen_pair = set()
                while len(todo) < budget:
                    u, w = rng.sample(cand, 2)
                    k = (min(u, w), max(u, w))
                    if k not in seen_pair:
                        seen_pair.add(k)
                        todo.append(k)
                log(f"bootstrap: sampling {len(todo)} of "
                    f"{len(cand)*(len(cand)-1)//2} pairs among {len(cand)} "
                    f"non-essential vertices")
            pairs = 0
            base = list(pool_free)
            for u, w in todo:
                S = [x for x in base if x != u and x != w]
                if oracle.colourable(full(S)):
                    master.add_vertex_cut([u, w])
                    # The vertex cut is the whole value of a pair.  The edge cut
                    # from learn() costs a Tabucol run each time and, on a pool
                    # with hundreds of non-essential vertices, that alone is most
                    # of the bootstrap.  Take it only every tenth pair.
                    if pairs % 10 == 0:
                        learn(S)
                    pairs += 1
                if time_limit and time.time() - t0 > time_limit:
                    break
            log(f"bootstrap: {pairs} size-2 correction sets from {len(todo)} pairs "
                f"among {len(cand)} non-essential vertices "
                f"(cuts={master.cuts})  ({time.time()-t:.0f}s)")

    it = 0
    proven = False
    while it < max_iters:
        if time_limit and time.time() - t0 > time_limit:
            log("time limit")
            break
        it += 1
        t = time.time()
        S = master.solve(bound, prefer=best)
        tm = time.time() - t
        if S is None:
            log(f"[{it}] master UNSAT at bound {bound}: no 5-chromatic subgraph "
                f"of the pool has <= {bound} vertices.  ({tm:.1f}s)")
            if dump_unsat:
                path = master.dump(dump_unsat, bound)
                log(f"  wrote the refuted instance to {path}: check it with "
                    f"`cadical {os.path.basename(path)}`, or with "
                    f"`cadical --lrat=proof.lrat {os.path.basename(path)}` and cake_lpr")
            proven = True
            break
        t = time.time()
        if oracle.colourable(full(S)):
            to = time.time() - t
            m = learn(S)
            d = ""
            if grow_every and it % grow_every == 0:
                tg = time.time()
                oracle.colourable(full(S))
                ext_col = ext.extend(oracle.model(full(S)), full(S))
                dsize, calls = grow(S, mono_edges(edges, ext_col), ext_col)
                d = f", MCS cut |D|={dsize} ({calls} calls, {time.time()-tg:.1f}s)"
            log(f"[{it}] |S|={len(S)} colourable; cut with {m} mono edges{d} "
                f"(cuts={master.cuts}, master {tm:.1f}s, oracle {to:.2f}s, {time.time()-t0:.0f}s)")
        else:
            to = time.time() - t
            # candidate!  verify independently, then shrink
            if not check(points, edges, full(S), triangle=None):
                log(f"[{it}] oracle said UNSAT but fresh verify disagrees -- BUG, stopping")
                break
            S2 = shrink_verified(points, edges, S, fixedset, ok_tri(full(S)), rng, check)
            best = S2
            bound = len(best) - 1
            log(f"[{it}] *** 5-chromatic |S|={len(S)} -> shrunk to {len(best)}, "
                f"new bound {bound}  (master {tm:.1f}s, oracle {to:.2f}s, {time.time()-t0:.0f}s)")
            if on_improve:
                on_improve(best)
            # its own vertex-critical cuts
            for v in best:
                Sv = [u for u in best if u != v]
                if oracle.colourable(full(Sv)):
                    learn(Sv)
    oracle.close()
    master.close()
    return best, proven
