#!/usr/bin/env python3
"""Both filters over every rational shell the lattice has -- the sweep SAT cannot buy.

Usage:
    join_sweep.py --depth 5 --radius 6.0
    join_sweep.py --depth 4 --radius 5.0 --jmax 2 --moduli 2,3

Route 44 swept joining rotations at INTEGER squared radii and found ten.  Route
48 corrected that: a spindle exists at any RATIONAL squared radius d^2 = a/b,
with cos = (2a-b)/(2a) and sin = sqrt(b(4a-b))/(2a), and the depth-4 radius-5
ball realises 56 of them.  Sweeping those by SAT means one 4-colourability test
on a ~30000-point union per candidate -- minutes to hours each -- which is why
it was never run.

Each row here costs one exact unit-vector enumeration instead:

  FILTER 1 (hn.algcolour) asks whether the join lattice has a homomorphism onto
  a group of order 4, or a colourable Cayley quotient, that kills no unit
  vector.  Either one is a PROOF that the whole infinite lattice is
  4-colourable, so the candidate is dead at every radius and depth.  Finding
  none proves nothing.

  FILTER 2 (hn.crossclass) counts the cross-edge classes of the join.  `share`
  says whether the two parts meet only at the origin -- if they do not, there
  is no two-part construction to build.  `nontriv` is the number of cross-edge
  orbits that are not the trivial origin-to-unit-vector ones; Parts' reading is
  that a LOPSIDED, and so cheap, split needs at least two.  That is a heuristic
  about size, not a theorem, and it is reported, not enforced.

A candidate is worth a SAT run only if filter 1 says `unknown` AND filter 2
says the parts are disjoint.
"""
import os, sys, time, argparse, collections
from fractions import Fraction
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn.joins import rational_spindle

ap = argparse.ArgumentParser()
ap.add_argument("--depth", type=int, default=5)
ap.add_argument("--radius", type=float, default=6.0)
ap.add_argument("--jmax", type=int, default=2)
ap.add_argument("--jmax-small", type=int)
ap.add_argument("--moduli", default="2,3,4")
ap.add_argument("--skip-census", action="store_true")
ap.add_argument("--from-d2", default="0",
                help="resume: skip shells with squared radius below this (a/b)")
ap.add_argument("--max-rank", type=int, default=12,
                help="skip candidates whose join lattice is bigger than this")
a = ap.parse_args()
log = lambda s: print(s, flush=True)
MODS = tuple(int(x) for x in a.moduli.split(",") if x.strip())


def shells():
    from hn.field import set_primes
    import hn.construct as C
    set_primes((3, 5, 11))
    C.refresh_field()
    from hn.construct import unit_vector_family, ball
    P = ball(unit_vector_family(a.jmax), a.depth, a.radius)
    sh = collections.Counter()
    for p in P:
        q = p.norm2()
        if not any(q.n[1:]):
            sh[Fraction(q.n[0], q.d)] += 1
    return len(P), sh


npts, sh = shells()
_lo = Fraction(a.from_d2)
cand = [d2 for d2 in sorted(sh) if d2 > 0 and d2 > _lo]
log(f"ball depth {a.depth} radius {a.radius}: {npts} points, "
    f"{len(cand)} rational shells ({sum(1 for d in cand if d.denominator == 1)} integer)\n")
log(f"{'d^2':>9} {'shell':>5} {'field':>16} {'rank':>4} {'units':>5} "
    f"{'F1':>19} {'share':>5} {'cross':>5} {'ntcls':>5}   {'time':>8}")
log("-" * 96)

rows = []
for d2 in cand:
    j = rational_spindle(d2.numerator, d2.denominator,
                         jmax_L=a.jmax, jmax_S=a.jmax_small or a.jmax)
    t0 = time.time()
    built = j.build()
    if built is None:
        log(f"{str(d2):>9} {sh[d2]:5d} {j.field_str():>16}   not a rotation in this field")
        continue
    WL, WS, cs = built
    from hn.construct import rotate
    from hn.lattice import Lattice
    gen = list(WL) + [rotate(p, cs) for p in WS]
    L = Lattice(gen)
    if L.rank > a.max_rank:
        log(f"{str(d2):>9} {sh[d2]:5d} {j.field_str():>16} {L.rank:>4}   "
            f"rank above --max-rank, skipped")
        continue
    from hn.algcolour import certify
    v = certify(gen, moduli=MODS)
    f1 = "DEAD" if v.dead else "unknown"
    if v.dead and not v.certs:
        f1 = f"DEAD (m={v.periodic[1]})"
    share = cross = nt = "-"
    if not a.skip_census:
        from hn.crossclass import census
        c = census(WL, cs, WS)
        z = ((0,) * 8, 1)
        ntc = {k: n for k, n in c.classes.items() if k[0] != z and k[1] != z}
        share, cross, nt = ("1" if c.direct else "many"), c.n_edges, len(ntc)
    dt = time.time() - t0
    log(f"{str(d2):>9} {sh[d2]:5d} {j.field_str():>16} {L.rank:>4} "
        f"{len(v.units):>5} {f1:>19} {str(share):>5} {str(cross):>5} {str(nt):>5}"
        f"   {dt:7.1f}s")
    rows.append((d2, j, v, share, nt))

log("-" * 96)
dead = [r for r in rows if r[2].dead]
live = [r for r in rows if not r[2].dead]
promising = [r for r in live if r[3] == "1" and isinstance(r[4], int) and r[4] >= 2]
log(f"{len(rows)} candidates built, {len(dead)} PROVED 4-colourable by filter 1, "
    f"{len(live)} survive.")
log(f"Of the survivors, {len(promising)} have disjoint parts and >= 2 non-trivial "
    f"cross-edge classes:")
for d2, j, v, share, nt in promising:
    log(f"    d^2 = {d2}   {j.name}  {j.field_str()}  rank {v.lattice.rank}, "
        f"{len(v.units)} units, {nt} classes")
log("\nOnly those need a SAT run.  'survives' means filter 1 found no certificate,")
log("which is not evidence of 5-chromaticity.")
