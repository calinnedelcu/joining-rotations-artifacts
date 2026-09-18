# alpha_256/9 = arccos(503/512): a seventh joining rotation, in a field nobody has used

Over **Q(sqrt3, sqrt11, sqrt1015)** -- and 1015 = 5 * 7 * 29, a field no
construction for this problem has used -- spinning the 6 lattice points at
squared radius 256/9, that is at distance **16/3**,

    L  union  alpha(L),   L = ball(30 vectors, depth 6, radius 5.35)

is **5-chromatic on 158257 vertices with 1857114 edges**, over a ball holding
all 6 points of its shell.

## Verification

1. rotation modulus exactly 1 in the field
2. all 30 lattice vectors exactly at unit distance
3. 158257 points loaded from disk
4. 12 at squared radius exactly 256/9 (6 original, 6 rotated -- the whole shell)
5. 1857114 edges recomputed from the coordinates
6. 0 wrong among 9286 edges re-tested exactly in K
7. minimum degree 6
8. not 4-colourable, fresh solver, nothing carried over

Reproduce: `scripts/batch_joins.py 256/9`.
