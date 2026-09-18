#!/usr/bin/env python3
"""The Z/4 half of Proposition 4, checked on every spindle it applies to.

Proposition 4's cyclic half needs a hypothesis: the images in Lambda/2Lambda of
the half-unit vectors H carry an F2-linear relation of ODD length.  The paper had
this checked against an exhaustive Z/4 search on eleven rotations.  It is much
cheaper than that search, and so can be checked on many more.

  h has |h| = 1/2  iff  2h is a unit vector of Lambda, i.e. iff a unit vector
  lies in 2*Lambda; then h = u/2.

  Asking for a homomorphism phi: Lambda -> F2 with phi(h) = 1 for every h in H is
  a linear system M x = 1 over F2, with M the matrix of images of H.  It has NO
  solution exactly when the LEFT null space of M contains a vector of odd weight
  -- which is the paper's odd-length relation.

So this reports, per rotation: how many half-unit vectors, and whether the odd
relation exists.  It always does, and there is a reason it must: omega = exp(i
pi/3) carries R to itself, so h, omega h and omega^2 h are half-unit vectors
together, and 1 + omega + omega^2 = 2 omega puts their sum in 2*Lambda -- a
relation of weight three.  So the cyclic half of Proposition 5 is unconditional,
and this sweep is a regression test for that rather than a survey of where the
shortcut applies.

Run: .venv/bin/python scripts/z4_relation.py [amax]
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))
from hn.joins import rational_spindle
from hn.lattice import Lattice
from hn.construct import rotate
from shells import shell_count


def rref_f2(rows, ncols):
    """Row-reduce over F2, returning (pivots, reduced rows) with rows as ints."""
    rows = [r for r in rows if r]
    piv, out = [], []
    for col in range(ncols):
        bit = 1 << col
        k = next((i for i, r in enumerate(rows) if r & bit), None)
        if k is None:
            continue
        rows[0], rows[k] = rows[k], rows[0]
        p = rows.pop(0)
        rows = [r ^ p if r & bit else r for r in rows]
        out.append(p)
        piv.append(col)
    return piv, out


def odd_relation(vectors, rank):
    """Is there an odd-size subset of `vectors` summing to 0 in F2^rank?

    Equivalently: does the system  M x = all-ones  have no solution?  Append the
    all-ones column and compare ranks -- the standard Rouche-Capelli test.
    """
    n = len(vectors)
    # columns of M^T are the vectors; solve M x = 1 with x in F2^rank.
    # Build the augmented system row by row: row i is (vectors[i] | 1).
    plain = [v for v in vectors]
    aug = [v | (1 << rank) for v in vectors]
    r1 = len(rref_f2(plain, rank)[0])
    r2 = len(rref_f2(aug, rank + 1)[0])
    return r2 > r1                      # inconsistent  <=>  odd relation exists


def main():
    amax = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    print(f"{'a':>4} {'shell':>6} {'units':>6} {'half-unit':>10} {'odd relation':>13}")
    tested = holds = 0
    for a in range(1, amax + 1):
        if a % 4 or not shell_count(a):
            continue
        built = rational_spindle(a, 1).build()
        if built is None:
            continue
        WL, _, cs = built
        L = Lattice(list(WL) + [rotate(w, cs) for w in WL])
        U = L.unit_vectors()
        H = [tuple(x // 2 for x in c) for c, _ in U if all(x % 2 == 0 for x in c)]
        if not H:
            print(f"{a:>4} {shell_count(a):>6} {len(U):>6} {0:>10} {'--':>13}")
            continue
        img = {sum((x & 1) << i for i, x in enumerate(h)) for h in H}
        # Do NOT discard the zero class.  A half-unit vector lying in 2*Lambda is
        # the strongest obstruction there is -- no phi can send 0 to 1 -- and it
        # is an odd relation of weight one.  Discarding it turned exactly that
        # case into an empty system, which read as "no relation": that is how
        # a = 48, 64 and 80 came to be reported as exceptions when at those three
        # EVERY half-unit vector is in 2*Lambda.
        ok = odd_relation(sorted(img), L.rank)
        tested += 1
        holds += ok
        print(f"{a:>4} {shell_count(a):>6} {len(U):>6} {len(H):>10} "
              f"{('YES' if ok else 'NO'):>13}")
    print(f"\nrotations with a half-unit vector: {tested}")
    print(f"the odd relation holds on: {holds} of {tested}")
    assert holds == tested, "the odd relation should hold wherever a half-unit exists"
    print("It holds everywhere, as the omega-identity says it must.")


if __name__ == "__main__":
    main()
