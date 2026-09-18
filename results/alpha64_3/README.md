# alpha_64/3 = arccos(125/128): a fifth joining rotation, and the one that broke the heuristic

Over **Q(sqrt3, sqrt11, sqrt23)**, spinning the 18 lattice points at squared
radius 64/3,

    L  union  alpha(L),   L = ball(30 vectors, depth 7, radius 4.64)

is **5-chromatic on 187225 vertices with 2207478 edges**, over a ball holding
all 18 points of the shell.

## What is and is not new

The rotation itself appears in route 48: `cos = 125/128`, `sin = sqrt759/128`
with `759 = 3*11*23`, as the rotation that doubles Parts' 421-vertex mono-pair
gadget at distance `8/sqrt3` into an 841-vertex graph. What is new is that it
works as a **plain union of a lattice ball with its image** -- the type-M
construction -- which is a different and stronger statement than doubling a
gadget.

## Why it matters beyond being a fifth

It creates only **48** new unit vectors, the fewest of any candidate, and three
other rotations at 48 are 4-colourable while `theta_44`, `theta_12` and
`theta_20` at 60, 72 and 90 are also 4-colourable. So it refutes the ranking
heuristic outright (results/RICHNESS-THRESHOLD.md): the successes and failures
interleave, and density does not decide which rotations join.

## Verification

End to end in a fresh process, from the coordinates on disk:

1. rotation modulus exactly 1 in the field
2. all 30 lattice vectors exactly at unit distance
3. 187225 points loaded
4. 36 at squared radius exactly 64/3 (18 original, 18 rotated -- the whole shell)
5. 2207478 edges recomputed from the coordinates, identical to the original
6. 0 wrong among 11038 edges re-tested exactly in K
7. minimum degree 6
8. not 4-colourable, fresh solver, nothing carried over

Reproduce: `scripts/test_join.py 64/3 --depth 7` (about 8 minutes).
