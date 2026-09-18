"""Heuristic k-colouring by tabu search, for colouring co-certificates.

Why.  The hitting-set reformulation (README, "The plan") learns one cut per
4-colouring the oracle returns: "at least one monochromatic edge of this
colouring must lose a vertex".  A SAT model has whatever monochromatic
edges the solver happened to leave; a colouring with *few* of them gives a
short cut, and short cuts are what make the master problem bite.
Minimising monochromatic edges under a fixed number of colours is exactly
the objective of Tabucol (Hertz & de Werra 1987), still the standard local
search for graph colouring.

What.  `ConflictColouring` keeps a k-colouring col[v], the matrix
gamma[v][c] = number of neighbours of v with colour c, and the list of
vertices that currently sit on a monochromatic edge.  One iteration scans
every (conflicting vertex, other colour) pair, takes the best non-tabu move
(a tabu move is allowed when it beats the best count seen -- aspiration),
applies it, updates gamma along that vertex's adjacency, and makes the
reverse move tabu for  int(0.6 * conflicts) + random(0..9)  iterations
(the dynamic tenure of Galinier & Hao 1999).  Vertices can be frozen: their
colour never changes but still counts, which is how a proper colouring of a
subgraph is extended to the whole graph and then repaired around it.
`greedy_extend` is the DSATUR-order greedy that builds the starting point:
most saturated vertex first, colour with the fewest conflicts.

Speed.  Pure Python.  gamma and tabu are lists of k-element rows; every
name used inside the loop is a local; the conflict list is kept up to date
incrementally with a position index (swap-with-last removal), so a scan
touches only conflicting vertices and a move costs O(deg v).  numpy was
measured and rejected: the work is one scalar access at a time, and a
numpy element read costs 184 ns against 27 ns for a list; a vectorised
move evaluation costs 4.5 us per iteration at |C| = 20, more than a whole
pure-Python iteration on the 510 graph (2 us).

The one departure from the textbook: an iteration scans at most
`scan_limit` conflicting vertices (a random window of the conflict list;
default 32, None for the full scan).  Below the limit this is exactly
Tabucol.  Above it -- the initial descent on a big graph, where thousands
of vertices are in conflict -- the full scan costs 3|C| evaluations per
move for no benefit, since almost any improving move will do.  Measured on
a planted-4-colourable G(20000, 200000): the full scan needs 180 s to reach
0 conflicts (600 it/s), the window 1.3 s (85 000 it/s), in about the same
number of moves.  On a hard random G(5000, 22500) the window is also
*better* (157 vs 315 conflicts after 200 000 moves): it randomises a stuck
search more than the tabu list alone.

Measured (Python 3.11, Apple Silicon, seed 0, DSATUR start, k=4):
  510-vertex / 2504-edge record graph:   ~500 000 it/s   (|C| is 148 at
      the DSATUR start with 87 conflicts, ~2 near the optimum)
  planted-4-colourable G(5000, 50000):    ~130 000 it/s, 0 conflicts after
      20 000 moves (0.2 s) from a 5685-conflict start
  planted-4-colourable G(20000, 200000):   ~85 000 it/s, 0 conflicts after
      112 000 moves (1.3 s) from a 22 710-conflict start
  hard random G(5000, 22500), avg degree 9: ~200 000 it/s, stuck at ~150
On the 510 graph k=5 is solved in 113 moves; k=4 (the graph is
5-chromatic) bottoms out within 200 000 moves (0.4 s) at 1 monochromatic
edge for 6 of 8 seeds, 2 for seed 0 and 6 for seed 4 (a basin the tabu
list does not leave; restart on another seed).  With scan_limit=None seeds
0, 1, 2 all reach 1.  A one-edge colouring is a one-literal cut for the
master problem.
"""
from __future__ import annotations
import heapq
import random

__all__ = ["ConflictColouring", "greedy_extend"]


def _adjacency(n, edges):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    return adj


def _as_list(n, partial):
    """A partial colouring as a list with -1 for uncoloured."""
    if partial is None:
        return [-1] * n
    if isinstance(partial, dict):
        col = [-1] * n
        for v, c in partial.items():
            col[v] = c
        return col
    col = list(partial)
    assert len(col) == n, (len(col), n)
    return col


def _dsatur(adj, k, col, rnd):
    """Colour every v with col[v] == -1, most saturated first, fewest conflicts.

    Saturation = number of distinct colours on coloured neighbours; ties by
    degree, then randomly.  The heap holds stale entries which are skipped
    when popped (a vertex is re-pushed each time its saturation grows).
    `rnd` is a random() callable.  Returns a new list.
    """
    n = len(adj)
    col = list(col)
    cnt = [[0] * k for _ in range(n)]
    for v in range(n):
        c = col[v]
        if c >= 0:
            for u in adj[v]:
                cnt[u][c] += 1
    sat = [k - cnt[v].count(0) for v in range(n)]
    heap = [(-sat[v], -len(adj[v]), rnd(), v) for v in range(n) if col[v] < 0]
    heapq.heapify(heap)
    push, pop = heapq.heappush, heapq.heappop
    colours = range(k)
    while heap:
        s, _, _, v = pop(heap)
        if col[v] >= 0 or -s != sat[v]:
            continue
        row = cnt[v]
        lo = min(row)
        choices = [c for c in colours if row[c] == lo]
        c = choices[int(rnd() * len(choices))]
        col[v] = c
        for u in adj[v]:
            if col[u] < 0:
                urow = cnt[u]
                urow[c] += 1
                if urow[c] == 1:
                    sat[u] += 1
                    push(heap, (-sat[u], -len(adj[u]), rnd(), u))
    return col


def greedy_extend(n, edges, k, partial, seed=0):
    """Extend a partial colouring (dict, or list with -1) to all n vertices.

    Uncoloured vertices are taken in DSATUR order and given the colour with
    the fewest conflicts among already-coloured neighbours.  The coloured
    part is left untouched, so a proper colouring of a subgraph stays proper
    and every new conflict lies on an edge with at least one new vertex.
    """
    return _dsatur(_adjacency(n, edges), k, _as_list(n, partial),
                   random.Random(seed).random)


class ConflictColouring:
    """Tabucol on a fixed graph.  Build once, run() as often as needed.

    scan_limit: at most this many conflicting vertices are examined per
    move (None: all of them, the textbook algorithm; see module docstring).
    """

    def __init__(self, n, edges, k=4, seed=0, scan_limit=32):
        self.n, self.k = n, k
        self.scan_limit = scan_limit
        self.edges = list(edges)
        self.adj = _adjacency(n, self.edges)
        self.rng = random.Random(seed)
        self.best_col, self.best_conf, self.iters = None, None, 0

    def mono_edges(self, colouring):
        """The edges (u, v) with colouring[u] == colouring[v]."""
        return [(a, b) for a, b in self.edges if colouring[a] == colouring[b]]

    def conflicts(self, colouring):
        return sum(1 for a, b in self.edges if colouring[a] == colouring[b])

    def greedy(self, partial=None):
        """DSATUR completion of `partial` (None = colour everything)."""
        return _dsatur(self.adj, self.k, _as_list(self.n, partial), self.rng.random)

    def run(self, max_iters, init=None, fixed=None):
        """Tabu search for up to max_iters moves.

        init:  starting colouring (list, or dict / list with -1 for vertices
               to be filled in greedily); None means a DSATUR start.
        fixed: iterable of vertex indices whose colour never changes.
        Returns (best colouring seen, its number of monochromatic edges).
        Stops early at 0 conflicts, or when the only conflicts left are
        between frozen vertices.
        """
        n, k, adj = self.n, self.k, self.adj
        rnd = self.rng.random
        col = _as_list(n, init)
        if -1 in col:
            col = _dsatur(adj, k, col, rnd)

        gamma = [[0] * k for _ in range(n)]
        for v in range(n):
            row = gamma[v]
            for u in adj[v]:
                row[col[u]] += 1
        nconf = sum(gamma[v][col[v]] for v in range(n)) // 2

        # pos[v]: index of v in the conflict list, -1 if absent, -2 if frozen
        pos = [-1] * n
        for v in (fixed or ()):
            pos[v] = -2
        conf = [v for v in range(n) if pos[v] == -1 and gamma[v][col[v]]]
        for i, v in enumerate(conf):
            pos[v] = i

        tabu = [[0] * k for _ in range(n)]
        others = [tuple(c for c in range(k) if c != cur) for cur in range(k)]
        S = self.scan_limit or 0
        best_conf, best_col = nconf, col[:]
        it = 0
        while nconf and it < max_iters and conf:
            # --- pick the move: min delta over conflicting v, colour c != col[v]
            asp = best_conf - nconf          # a tabu move needs delta < asp
            best, bv, bc, ties = 1 << 30, -1, -1, 0
            scan = conf
            if S and len(conf) > S:          # big conflict set: a random window
                off = int(rnd() * (len(conf) - S + 1))
                scan = conf[off:off + S]
            for v in scan:
                row = gamma[v]
                cur = col[v]
                base = row[cur]
                trow = tabu[v]
                for c in others[cur]:
                    d = row[c] - base
                    if d > best:
                        continue
                    if trow[c] > it and d >= asp:
                        continue
                    if d < best:
                        best, bv, bc, ties = d, v, c, 1
                    else:
                        ties += 1
                        if rnd() * ties < 1.0:
                            bv, bc = v, c
            if bv < 0:                       # every move tabu: random one
                bv = conf[int(rnd() * len(conf))]
                bc = others[col[bv]][int(rnd() * (k - 1))]

            # --- apply it
            old = col[bv]
            col[bv] = bc
            row = gamma[bv]
            nconf += row[bc] - row[old]
            it += 1
            tabu[bv][old] = it + int(0.6 * nconf) + int(rnd() * 10)
            for u in adj[bv]:
                urow = gamma[u]
                urow[old] -= 1
                urow[bc] += 1
                cu = col[u]
                if cu == old:
                    if urow[old] == 0 and pos[u] >= 0:
                        i = pos[u]
                        last = conf.pop()
                        if last != u:
                            conf[i] = last
                            pos[last] = i
                        pos[u] = -1
                elif cu == bc:
                    if urow[bc] == 1 and pos[u] == -1:
                        pos[u] = len(conf)
                        conf.append(u)
            if row[bc] == 0:
                i = pos[bv]
                last = conf.pop()
                if last != bv:
                    conf[i] = last
                    pos[last] = i
                pos[bv] = -1
            if nconf < best_conf:
                best_conf, best_col = nconf, col[:]

        self.iters += it
        self.best_col, self.best_conf = best_col, best_conf
        return best_col, best_conf
