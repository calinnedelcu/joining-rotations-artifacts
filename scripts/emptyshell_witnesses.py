#!/usr/bin/env python3
"""Ship the nine empty-shell verdicts as checkable witnesses.

Section 7 settles the nine multiples of 4 below 100 whose shell is empty, and a
reviewer was right that they were the least-checked claims in the paper: they
were reported as verdicts with nothing attached.  The eleven periodic kills ship
as JSON that `check_periodic.py` validates without importing any project code.
These now do the same.

Each verdict gets a witness that is a proof rather than a log:

  killed     an explicit homomorphism Lambda_a -> (Z/2)^2 avoiding every unit
             vector, given as the two functionals cutting out its kernel.  A
             homomorphism 4-colouring properly colours the whole infinite
             lattice, so no subset of it is 5-chromatic.

  survives   a vector of length 1/2.  By Proposition 5 no homomorphism onto a
             group of order 4 can avoid the unit vectors, so the rotation
             survives filter 1 -- and this is a one-line certificate where an
             exhaustive search would only be a log.

Each vector is carried twice: as integer coordinates in the lattice basis, which
is what the colouring is a function of, and as its exact (x, y) in the field,
which is what a length is.  So `check_emptyshell.py` can verify for itself that
the things called unit vectors have length 1 -- it needs the field's
multiplication table, which is four lines for a multiquadratic field, and not
one line of this project.

Run: .venv/bin/python scripts/emptyshell_witnesses.py
"""
import json, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, ROOT)
from hn.joins import rational_spindle
from hn.lattice import Lattice
from hn.construct import rotate
from hn.algcolour import klein_colourings, z4_colourings
import hn.field as F
from hn.field import K
log = lambda s: print(s, flush=True)

def half_pt(p):
    """p/2, as a field point."""
    h = K.rat(1, 2)
    return (p.x * h, p.y * h)

def entry(c, p, halve=False):
    """One vector: basis coordinates, and the exact (x, y) that fixes its length."""
    x, y = half_pt(p) if halve else (p.x, p.y)
    return dict(c=list(c), x=[list(x.n), x.d], y=[list(y.n), y.d])

EMPTY = [8, 24, 32, 40, 56, 68, 72, 88, 96]      # 4 | a, a <= 100, shell empty
if sys.argv[1:]:                                 # redo only these, for a resume
    EMPTY = [int(x) for x in sys.argv[1:]]
OUT = os.path.join(ROOT, "results", "emptyshell")
os.makedirs(OUT, exist_ok=True)

log(f"{'a':>4} {'rank':>5} {'units':>6} {'half':>5} {'klein':>6} {'cyclic':>7}  verdict")
summary = []
for a in EMPTY:
    t = time.time()
    WL, _, cs = rational_spindle(a, 1).build()
    L = Lattice(list(WL) + [rotate(w, cs) for w in WL])
    U = L.unit_vectors()
    coords = [list(c) for c, _ in U]
    klein = klein_colourings([tuple(c) for c in coords], L.rank)
    cyc = z4_colourings([tuple(c) for c in coords], L.rank)
    halfU = [(c, p) for c, p in U if all(x % 2 == 0 for x in c)]
    half = [c for c, _ in halfU]

    rec = dict(rotation=f"theta_{a}", a=a, rank=L.rank, shell_size=0,
               primes=list(F.PRIMES), unit_vectors=[entry(c, p) for c, p in U],
               counts=dict(klein=len(klein), cyclic=len(cyc), half_unit=len(half)))
    if klein:
        rec["verdict"] = "killed"
        rec["klein_kernel"] = [klein[0][1], klein[0][2]]
    else:
        rec["verdict"] = "survives"
        if not halfU:
            raise SystemExit(f"a={a}: no colouring and no half-unit vector -- "
                             f"nothing to certify; this needs a look")
        # the shortest one, for a witness a reader can hold
        c, pt = min(halfU, key=lambda cp: sum(x * x for x in cp[0]))
        rec["half_unit_vector"] = entry(c, pt, halve=True)
    with open(os.path.join(OUT, f"theta_{a}.json"), "w") as f:
        json.dump(rec, f)
    summary.append((a, rec["verdict"], len(half)))
    log(f"{a:>4} {L.rank:>5} {len(U):>6} {len(half):>5} {len(klein):>6} "
        f"{len(cyc):>7}  {rec['verdict']}  ({time.time()-t:.0f}s)")

killed = [a for a, v, _ in summary if v == "killed"]
surv = [a for a, v, _ in summary if v == "survives"]
log(f"\nkilled by a homomorphism colouring: {killed}")
log(f"survive, each by a half-unit vector: {surv}")
log(f"wrote {len(summary)} witnesses to results/emptyshell/")
if len(summary) == 9:
    n = sum(1 for _, _, h in summary if h)
    log(f"\nof the nine, {n} have a half-unit vector; with the sixteen "
        f"occupied-shell candidates that is {16 + n} integer spindles below 100 "
        f"that do.")
else:
    # A partial run must not print a census: counting only the a values it was
    # given would report 18 where the answer is 19, and the log would look like
    # a result.
    log("(partial run -- pass no arguments to rebuild all nine and get the census)")
