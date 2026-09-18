#!/usr/bin/env python3
"""Which squared radii the Moser lattice occupies -- a closed criterion.

Call a prime p != 3, 11 OBSTRUCTED when it splits in Q(sqrt33) and is inert in
Q(sqrt-3); for odd p that is (33|p) = 1 and (-3|p) = -1.  Two is obstructed too
-- 33 = 1 mod 8 splits it, -3 = 5 mod 8 keeps it inert -- and lands in the same
residue class list, so it is not a separate case.  Then, verified here:

    R has a point at squared radius a = n/b, in lowest terms
        <=>  b in {1,3,9}, and v_p(n) is even at every obstructed p.

The denominator contributes nothing beyond being admissible -- 3 is ramified in
Q(sqrt33), hence never obstructed, so no power of it can matter.

The mechanism: the Q-span of R is V = Q(sqrt33)(sqrt-3), and |z|^2 = z*conj(z)
is the norm of that quadratic extension, so a is a squared radius in V exactly
when a = x^2 + 3y^2 is soluble over Q(sqrt33).  Above an obstructed p the local
extension is unramified quadratic and its norm group is the even-valuation
elements, which is where the parity comes from.

One half of the passage is proved and lives in the paper as a lemma: at an
INTEGER squared radius the congruences are automatic, because AB+CD = 0 together
with 16 | S forces them -- an exhaustive check over the 4096 residue classes mod
8, of which 320 have 16 | S while failing the congruences and none of those 320
has AB+CD = 0 mod 8.  So the chart and R have literally the same points there;
this script also checks that, as equal counts.

Still missing: solubility over Q(sqrt33) is governed by local conditions, and we
have not shown those suffice for representation by the INTEGRAL form S = 144a
with AB+CD = 0.  Hence "verified", not "proved".

Run: .venv/bin/python scripts/shell_criterion.py [amax]
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))
from shells import shell_count

TARGETS = [289, 578, 867, 841, 1681, 493, 867, 1156, 1445, 2023, 2312, 3179,
           4913, 10201, 64, 128, 256]


def legendre(a, p):
    r = pow(a % p, (p - 1) // 2, p)
    return -1 if r == p - 1 else r


def factor(n):
    f, d = {}, 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


OBSTRUCTED_CLASSES = (2, 8, 17, 29, 32)       # mod 33


def obstructed(p):
    """p splits in Q(sqrt33) and is inert in Q(sqrt-3).

    Since 33 = 1 mod 4, reciprocity makes (33|p) = (p|33), and (-3|p) = 1 iff
    p = 1 mod 3; both are fixed by p mod 33, and five of the twenty coprime
    classes qualify.  The symbol form and the residue form are asserted equal
    below for every ODD prime under 20000; p = 2 is obstructed by the two
    splitting conditions directly, and 2 mod 33 = 2 is in the list anyway.
    """
    return p not in (3, 11) and p % 33 in OBSTRUCTED_CLASSES


def obstructed_by_symbols(p):
    return p not in (2, 3, 11) and legendre(33, p) == 1 and legendre(-3, p) == -1


def predict(a):
    f = factor(a)
    return all(e % 2 == 0 for q, e in f.items() if obstructed(q))


def main():
    amax = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    diff = [p for p in range(5, 20000)
            if all(p % d for d in range(2, int(p ** .5) + 1))
            and obstructed(p) != obstructed_by_symbols(p)]
    print(f"residue form vs Legendre symbols, primes < 20000: "
          f"disagreements = {len(diff)}  {diff[:5] if diff else ''}")
    assert not diff, "the residue classes do not match the symbols"
    bad = []
    for a in range(1, amax + 1):
        if predict(a) != (shell_count(a) > 0):
            bad.append(a)
    print(f"a = 1 to {amax}: mismatches = {len(bad)}  {bad if bad else ''}")
    from shells import chart_count
    same = [a for a in range(1, min(amax, 300) + 1) if chart_count(a) != shell_count(a)]
    print(f"chart and R counts differ at: {len(same)} values "
          f"(Lemma: they never should, at integer radii)  {same if same else ''}")
    # the rational radii too: denominator must lie in {1,3,9} and is otherwise inert
    from math import gcd
    rat = []
    for b in (1, 3, 9, 2, 4, 6, 12, 5):
        for n in range(1, 201):
            if gcd(n, b) != 1:
                continue
            if ((b in (1, 3, 9)) and predict(n)) != (shell_count(n, b) > 0):
                rat.append((n, b))
    print(f"rational radii n/b, b in 1,3,9,2,4,6,12,5 and n <= 200: "
          f"mismatches = {len(rat)}  {rat[:6] if rat else ''}")
    tb = [a for a in sorted(set(TARGETS)) if predict(a) != (shell_count(a) > 0)]
    print(f"targeted values {sorted(set(TARGETS))}")
    print(f"  mismatches = {len(tb)}  {tb if tb else ''}")
    print("\nobstructed primes below 200:",
          [p for p in range(2, 200)
           if all(p % d for d in range(2, int(p ** .5) + 1)) and obstructed(p)])
    assert not bad and not tb, "the shell criterion failed"
    assert not same, "chart and lattice disagree at an integer radius"
    assert not rat, "the criterion fails at a rational radius"

    # the closed form of the paper's central question: law AND shell together
    closed = []
    for a in range(1, amax + 1):
        f = factor(a)
        pred = f.get(2, 0) >= 2 and all(
            e % 2 == 0 for q, e in f.items() if obstructed(q))
        if pred != (a % 4 == 0 and shell_count(a) > 0):
            closed.append(a)
    print(f"closed form (candidate <=> v_p even at every obstructed p, v_2 >= 2): "
          f"mismatches = {len(closed)}  {closed[:6] if closed else ''}")
    assert not closed, "the closed form fails"
    print("\ncriterion holds on every value tested")


if __name__ == "__main__":
    main()
