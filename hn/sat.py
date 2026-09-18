"""SAT encoding of k-colourability, with incremental selector literals.

The encoding is the direct one and deliberately omits at-most-one clauses:
they are redundant (a vertex assigned two colours can always be projected
down) and dropping them removes 6|V| clauses.

Selector literals are what make the minimisation loop cheap.  One solver
instance keeps its learnt clauses for the whole run, and "is this subgraph
k-colourable?" becomes a single solve() under assumptions instead of a
fresh solver launch.  Parts paid a full restart on every one of millions of
queries; this is where most of the available speedup lives.
"""
from __future__ import annotations
from pysat.solvers import Solver

DEFAULT_SOLVER = "cadical153"


class Colouring:
    def __init__(self, n, edges, k=4, solver=DEFAULT_SOLVER, selectors=True):
        self.n, self.k, self.edges = n, k, edges
        self.sel = selectors
        cls = []
        for v in range(n):
            lits = [self.var(v, c) for c in range(k)]
            cls.append(([-self.s(v)] if selectors else []) + lits)
        for a, b in edges:
            for c in range(k):
                cls.append([-self.var(a, c), -self.var(b, c)])
        self.solver = Solver(name=solver, bootstrap_with=cls)

    def var(self, v, c):
        return self.k * v + c + 1

    def s(self, v):
        return self.k * self.n + v + 1

    def break_colour_symmetry(self, triangle):
        """Fix a triangle to colours 0,1,2.

        This removes the whole S_k colour-permutation group at zero encoding
        cost.  Measured on the 510-vertex graph: UNSAT in 2.6 s with it,
        78.1 s without -- a factor of 30.
        """
        for c, v in enumerate(triangle[: self.k]):
            self.solver.add_clause([self.var(v, c)])

    def colourable(self, keep=None):
        """Is the subgraph induced by `keep` k-colourable?"""
        asm = [self.s(v) for v in (range(self.n) if keep is None else keep)] if self.sel else []
        return self.solver.solve(assumptions=asm)

    def core(self):
        """After an UNSAT solve: the vertices the solver actually needed.

        This is a smaller non-k-colourable subgraph, obtained for free.
        """
        c = self.solver.get_core() or []
        return sorted(l - self.k * self.n - 1 for l in c)

    def model_colouring(self):
        """After a SAT solve: colour of each vertex."""
        m = set(l for l in self.solver.get_model() if l > 0)
        return [next(c for c in range(self.k) if self.var(v, c) in m)
                for v in range(self.n)]

    def close(self):
        self.solver.delete()


def find_triangle(n, edges):
    adj = {i: set() for i in range(n)}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    for a, b in edges:
        common = adj[a] & adj[b]
        if common:
            return (a, b, next(iter(common)))
    return None
