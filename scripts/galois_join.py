"""Galois conjugation as a JOINING map, not as a search seam.

sigma preserves unit distance (1 is rational), so G u sigma(G) is a unit-distance
graph -- but sigma is not an isometry, so sigma(G) is not a congruent copy and the
pair is outside every type in the A/M/J/T classification.  Route 39 used sigma to
CUT the record; route 30 unioned the record with its images.  Nobody has used it to
JOIN a 4-colourable graph to itself, which is what a construction would do.
"""
import sys, collections, time
sys.path.insert(0, "/Users/calinnedelcu/Documents/universitate/hadwiger-nelson")
from hn.field import set_primes
set_primes((3, 11, 5))
import hn.construct as C; C.refresh_field()
from hn.field import K, Pt
from hn.construct import unit_vector_family, ball, edges, dedup, rotate, ROT, norm
from hn.minimise import verify
from hn.sat import find_triangle
from hn.graph import induced

depth  = int(sys.argv[1]) if len(sys.argv) > 1 else 3
radius = float(sys.argv[2]) if len(sys.argv) > 2 else 2.2
L = ball(unit_vector_family(2), depth, radius)
print(f"ball {len(L)} points", flush=True)
ISO = {"id": None, "t4": ROT["theta4"], "t3": ROT["theta3"]}
for mask in range(1, 8):
    for iname, cs in ISO.items():
        S = [p.conj(mask) for p in L]
        if cs is not None:
            S = [rotate(p, cs) for p in S]
        kL = {p.key(): i for i, p in enumerate(L)}
        share = sum(1 for p in S if p.key() in kL)
        U = dedup(L + S)
        if len(U) == len(L):
            print(f"  mask {mask} o {iname:>3}: identity on the lattice"); continue
        E = edges(U)
        idx = {p.key(): i for i, p in enumerate(U)}
        inL = set(idx[p.key()] for p in L); inS = set(idx[p.key()] for p in S)
        cls = collections.Counter(); n = 0
        for u, v in E:
            if (u in inL) != (v in inL) and (u in inS) != (v in inS):
                n += 1
                cls[tuple(sorted((round(norm(U[u]), 3), round(norm(U[v]), 3))))] += 1
        five = ""
        if n:
            t = time.time()
            tri = find_triangle(len(U), E)
            five = f"  chi>=5 {verify(U, E, triangle=tri)}  ({time.time()-t:.0f}s)"
        print(f"  mask {mask} o {iname:>3}: union {len(U):6d} share {share:6d} "
              f"cross {n:5d} classes {len(cls):3d}{five}", flush=True)
