#!/usr/bin/env python3
"""Madore's finite-field obstruction: a complete kill-test for a coordinate field.

Usage: madore.py [QMAX]

Madore, arXiv:1509.07023, Corollary 3.4: if p is a maximal ideal of the ring of
integers of a number field K with norm q congruent to 3 mod 4, then there is a
graph homomorphism from the unit-distance graph of K^2 onto the unit-distance
graph of (F_q)^2, so

    chi(K^2) <= chi((F_q)^2).

That is an obstruction of a kind nothing else here provides. Every other
negative result in this repository says a particular pool turned out
4-colourable. This says an entire field is 4-colourable, so no subgraph of any
pool over it can ever be 5-chromatic, and it is decided by colouring a graph on
q^2 vertices, which takes milliseconds.

Gamma((F_q)^2) has F_q^2 as its vertices and joins x to y when
(x1-y1)^2 + (x2-y2)^2 = 1 in F_q; for q = 3 mod 4 it is (q+1)-regular.

Known: chi((F_3)^2) = 3 and chi((F_11)^2) = 5, which is why Q(sqrt3, sqrt11) is
not excluded and is the field every record lives in.
"""
import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from pysat.solvers import Solver


def chromatic_at_most(n, edges, k):
    cls = [[k * v + c + 1 for c in range(k)] for v in range(n)]
    for a, b in edges:
        for c in range(k):
            cls.append([-(k * a + c + 1), -(k * b + c + 1)])
    for c, v in enumerate(range(min(k, n))):        # pin a few to break colour symmetry
        if c < k:
            cls.append([k * v + c + 1])
    s = Solver(name="cadical195", bootstrap_with=cls)
    r = s.solve()
    s.delete()
    return r


def field_plane(q):
    sq = {}
    for x in range(q):
        sq.setdefault((x * x) % q, []).append(x)
    pts = [(x, y) for x in range(q) for y in range(q)]
    idx = {p: i for i, p in enumerate(pts)}
    E = set()
    for i, (x, y) in enumerate(pts):
        for dx in range(q):
            need = (1 - dx * dx) % q
            for dy in sq.get(need, ()):
                j = idx[((x + dx) % q, (y + dy) % q)]
                if i < j:
                    E.add((i, j))
                elif j < i:
                    E.add((j, i))
    return len(pts), sorted(E)


if __name__ == "__main__":
    qmax = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    qs = [q for q in range(3, qmax + 1) if q % 4 == 3 and
          all(q % d for d in range(2, int(q ** .5) + 1))]
    print(f"{'q':>5} {'vertices':>9} {'edges':>8} {'degree':>7}  chi <= 4 ?  verdict", flush=True)
    for q in qs:
        t = time.time()
        n, E = field_plane(q)
        deg = 2 * len(E) / n
        four = chromatic_at_most(n, E, 4)
        three = chromatic_at_most(n, E, 3) if four else None
        chi = "<= 3" if three else ("= 4" if four else ">= 5")
        verdict = ("KILLS any field with an ideal of norm %d" % q) if four \
            else "no obstruction from this q"
        print(f"{q:5d} {n:9d} {len(E):8d} {deg:7.1f}  {str(four):9s}  chi {chi}, {verdict}"
              f"  ({time.time()-t:.1f}s)", flush=True)


def residue_degree_one(primes, q):
    """Does Q(sqrt p, sqrt q, sqrt r) have a prime of norm exactly `q`?

    For an odd prime q not dividing any generator, a prime of the multiquadratic
    field above q has residue degree 1 exactly when q splits in every quadratic
    subfield, which is to say every generator is a quadratic residue mod q. If
    one generator is a non-residue the residue degree is 2, the norm is q^2, and
    q^2 = 1 mod 4 always, so Madore's corollary does not apply.
    """
    sq = {(x * x) % q for x in range(1, q)}
    return all(m % q != 0 and (m % q) in sq for m in primes)


def kill_test(primes, killers=(3, 7)):
    """Which killer prime, if any, proves this field's plane 4-colourable."""
    for q in killers:
        if residue_degree_one(primes, q):
            return q
    return None
