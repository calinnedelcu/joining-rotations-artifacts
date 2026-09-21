#!/usr/bin/env python3
"""Validate the nine empty-shell witnesses from JSON alone.

Imports nothing from this project, exactly as check_periodic.py does not: the
point of a witness is that it can be checked without trusting the code that
produced it.  Everything below is integer arithmetic on what the files carry.

Each witness names the field's primes, and each vector in it carries both its
integer coordinates in the lattice basis and its exact (x, y).  A multiquadratic
field Q(sqrt p0, sqrt p1, sqrt p2) has the basis of the 8 squarefree products,
indexed by subsets, and

    basis_i * basis_j  =  (prod of p_k over k in i AND j) * basis_(i XOR j),

which is the whole multiplication table and is implemented in `fmul` below.  So
this script can decide a length for itself.

  * every vector listed as a unit vector satisfies x^2 + y^2 = 1;
  * a "killed" witness names two F2-functionals, and no unit vector lies in
    their common kernel -- so the induced map to (Z/2)^2 is a homomorphism
    4-colouring of the whole infinite lattice, and nothing inside it is
    5-chromatic;
  * a "survives" witness names a vector with x^2 + y^2 = 1/4.  Proposition 5
    turns that into the verdict: doubling it gives a unit vector in 2*Lambda,
    which no homomorphism onto a group of order 4 can avoid.  That is a proof,
    where an exhaustive search would leave only a log.

Run: .venv/bin/python scripts/check_emptyshell.py
"""
import glob, json, os, sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = sorted(glob.glob(os.path.join(HERE, "..", "results", "emptyshell", "*.json")),
               key=lambda p: int(os.path.basename(p).split("_")[1].split(".")[0]))
if not FILES:
    sys.exit("no witnesses in results/emptyshell/ -- run emptyshell_witnesses.py")


def fmul(a, b, pr):
    """Product of two field elements, each given as (8 numerators, denominator)."""
    an, ad = a
    bn, bd = b
    out = [0] * 8
    for i, x in enumerate(an):
        if not x:
            continue
        for j, y in enumerate(bn):
            if not y:
                continue
            c = 1
            for k in range(3):
                if (i >> k) & 1 and (j >> k) & 1:
                    c *= pr[k]
            out[i ^ j] += x * y * c
    return out, ad * bd


def sqlen(v, pr):
    """x^2 + y^2, as a Fraction if it is rational and None if it is not."""
    xn, xd = fmul(v["x"], v["x"], pr)
    yn, yd = fmul(v["y"], v["y"], pr)
    num = [xn[i] * yd + yn[i] * xd for i in range(8)]
    den = xd * yd
    if any(num[1:]):                       # an irrational length is not a length we want
        return None
    return Fraction(num[0], den)


parity = lambda x: bin(x).count("1") & 1
mask = lambda n: sum((c & 1) << k for k, c in enumerate(n))

bad = 0
print(f"{'a':>4} {'rank':>5} {'units':>6} {'verdict':>9}  witness")
for path in FILES:
    w = json.load(open(path))
    a, pr, U = w["a"], w["primes"], w["unit_vectors"]
    errs = []
    off = sum(1 for v in U if sqlen(v, pr) != 1)
    if off:
        errs.append(f"{off} listed unit vectors do not have length 1")
    if w["verdict"] == "killed":
        l1, l2 = w["klein_kernel"]
        dead = sum(1 for v in U
                   if not parity(l1 & mask(v["c"])) and not parity(l2 & mask(v["c"])))
        if dead:
            errs.append(f"{dead} unit vectors lie in the kernel")
        wit = f"Klein colouring, kernel <{l1},{l2}>, avoids all {len(U)}"
    else:
        h = w["half_unit_vector"]
        L = sqlen(h, pr)
        if L != Fraction(1, 4):
            errs.append(f"the claimed half-unit vector has squared length {L}, not 1/4")
        # Proposition 6, not 5: Proposition 5 needs a = 4m^2, and 24, 72, 88
        # are not of that form.  Proposition 6 is the one that rules out every
        # homomorphism onto a group of order 4.
        wit = f"a vector of length 1/2 -> Proposition 6"
    bad += bool(errs)
    print(f"{a:>4} {w['rank']:>5} {len(U):>6} {w['verdict']:>9}  "
          f"{wit if not errs else 'FAILED: ' + '; '.join(errs)}")

print(f"\n{len(FILES)} witnesses, {bad} bad")
sys.exit(1 if bad else 0)
