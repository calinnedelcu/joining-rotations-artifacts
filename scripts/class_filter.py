#!/usr/bin/env python3
"""Filter 2: the cross-edge class census of a joining rotation.

Usage:
    class_filter.py --validate
    class_filter.py --spindle 4 --primes 3,5,11
    class_filter.py --sweep-shells 5.0

For a join  L union g(S)  whose parts share only the origin, the cross edges
are in bijection with the unit vectors of L + g(L), so the census is exact and
complete over the INFINITE union -- no ball, no radius.  Each edge is labelled
by the squared radii (|p|^2, |g(q)|^2) of its two endpoints; the number of
distinct labels is the class count.

The claim under test is Parts': a lopsided split like the record's 374 + 136
needs the two parts joined by more than one orbit, because the cheap side is
cheap only when it can break a pair the expensive side is forced to create.
That is a heuristic about SIZE, not a theorem about chromatic number, and this
script prints the census rather than a verdict.  `--validate` shows where it
agrees with the known answers and where it does not.
"""
import os, sys, time, argparse, collections
from fractions import Fraction
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.joins import Join, rational_spindle, GROUND_TRUTH

ap = argparse.ArgumentParser()
ap.add_argument("--validate", action="store_true")
ap.add_argument("--spindle", type=int)
ap.add_argument("--shell", help="rational squared radius a/b")
ap.add_argument("--primes", help="e.g. 3,5,11")
ap.add_argument("--jmax", type=int, default=2)
ap.add_argument("--jmax-small", type=int)
ap.add_argument("--sweep-shells", type=float, metavar="RADIUS")
ap.add_argument("--depth", type=int, default=4)
ap.add_argument("--detail", action="store_true")
a = ap.parse_args()
log = lambda s: print(s, flush=True)

HDR = (f"{'rotation':12s} {'field':18s} {'rank':>4s} {'share':>5s} "
       f"{'cross':>6s} {'classes':>7s} {'nontriv':>7s}   sizes")


def run(j):
    from hn.crossclass import census
    built = j.build()
    if built is None:
        return None
    WL, WS, cs = built
    t = time.time()
    c = census(WL, cs, WS)
    return c, time.time() - t


def nontrivial(c):
    """Classes that are not the origin meeting a unit vector.

    Every join has those two -- 0 is in both parts and its unit-distance
    neighbours are in the other -- so they carry no information about whether
    the parts really interlock.
    """
    z = ((0,) * 8, 1)
    return {k: v for k, v in c.classes.items() if k[0] != z and k[1] != z}


def line(j, res, expect=None, why=""):
    if res is None:
        log(f"{j.name:12s} {j.field_str():18s}  not a rotation in this field")
        return None
    c, dt = res
    nt = nontrivial(c)
    sizes = ",".join(str(v) for _, v in sorted(nt.items(), key=lambda kv: -kv[1]))
    share = "1" if c.direct else "many"
    log(f"{j.name:12s} {j.field_str():18s} {c.lattice.rank:>4d} {share:>5s} "
        f"{c.n_edges:>6d} {c.n_classes:>7d} {len(nt):>7d}   {sizes or '-':20s}"
        f" {dt*1000:7.0f} ms")
    if why:
        log(f"             truth: {expect} -- {why}")
    if a.detail:
        from hn.crossclass import _pretty
        for (ka, kb), n in sorted(c.classes.items(), key=lambda kv: -kv[1]):
            log(f"                |p|^2={_pretty(ka):10.5f} "
                f"|gq|^2={_pretty(kb):10.5f}  {n:4d} edges")
    return c


if a.validate:
    log("Filter 2 against the cases whose answers are already known.\n")
    log("The claim: >= 2 NON-TRIVIAL classes is necessary for a lopsided (cheap)")
    log("split.  It says nothing about chromatic number on its own.\n")
    log(HDR)
    for j, expect, why in GROUND_TRUTH:
        line(j, run(j), expect, why)
    sys.exit(0)

if a.sweep_shells:
    from hn.field import set_primes
    import hn.construct as C
    set_primes((3, 5, 11))
    C.refresh_field()
    from hn.construct import unit_vector_family, ball
    P = ball(unit_vector_family(a.jmax), a.depth, a.sweep_shells)
    shells = collections.Counter()
    for p in P:
        q = p.norm2()
        if not any(q.n[1:]):
            shells[Fraction(q.n[0], q.d)] += 1
    cand = [d2 for d2 in sorted(shells) if d2 > 0]
    log(f"ball depth {a.depth} radius {a.sweep_shells}: {len(P)} points, "
        f"{len(cand)} rational shells\n")
    log(HDR)
    keep = []
    for d2 in cand:
        j = rational_spindle(d2.numerator, d2.denominator,
                             jmax_L=a.jmax, jmax_S=a.jmax_small or a.jmax)
        c = line(j, run(j))
        if c is not None and len(nontrivial(c)) >= 2:
            keep.append(j.name)
    log(f"\n{len(keep)} of {len(cand)} shells give >= 2 non-trivial classes: "
        + ", ".join(keep))
    sys.exit(0)

primes = tuple(int(x) for x in a.primes.split(",")) if a.primes else None
if a.spindle:
    j = rational_spindle(a.spindle, 1, primes=primes, jmax_L=a.jmax,
                         jmax_S=a.jmax_small or a.jmax)
elif a.shell:
    n, _, d = a.shell.partition("/")
    j = rational_spindle(int(n), int(d or 1), primes=primes, jmax_L=a.jmax,
                         jmax_S=a.jmax_small or a.jmax)
else:
    ap.error("need --validate, --spindle, --shell or --sweep-shells")
log(HDR)
line(j, run(j))
