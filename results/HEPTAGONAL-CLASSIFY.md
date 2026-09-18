# The joining rotations of Haugland's lattice, as far as they are reachable

The divisibility law classifies the spindles of the Moser lattice.  It does not
transfer, so the same question has to be asked again here -- and can be, because
the criterion costs almost nothing at rank 12.

## Which spindles exist here at all

`theta_N` needs `sqrt(4N-1)` in the field.  `Q(zeta_420)` contains `sqrt(m)` only
for `m` in `{1, 3, 5, 7, 15, 21, 35, 105}`, the squarefree products of the primes
dividing 420.  So of `N <= 16` only

    N = 1 (sqrt3), 2 (sqrt7), 4 (sqrt15), 7 (sqrt27), 9 (sqrt35), 16 (sqrt63)

give a rotation at all.  Every other `N` is excluded before any computation.

## The verdicts

| N | shell | sqrt(4N-1) | rank | units | in 2L | klein | z4 | verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | 84 | sqrt3 | 12 | 84 | 0 | 1 | 0 | **dead** |
| 2 | 168 | sqrt7 | 12 | 168 | **0** | **0** | **0** | **SURVIVES** |
| 4 | 252 | sqrt15 | -- | -- | -- | -- | -- | survives trivially (radius 2) |
| 7, 9, 16 | -- | -- | -- | -- | -- | -- | -- | past the enumeration wall |

`N = 2` is the only **non-trivial** survivor found: no half-unit vector, so the
free pass does not apply, and a **full** certificate search -- affordable at rank
12, where this lattice's own rank-24 joins are not -- returns nothing at all.

`N = 4` is `theta_4`, Haugland's own joining rotation, and it passes for free:
its shell radius is the even integer 2, and then `(2g - theta(2g))/2 = g -
theta(g)` is a lattice element of modulus 1/2 for every generator `g`.

## The wall

The shell enumeration is Fincke-Pohst in 12 dimensions with target
`96 * N * den^2`, and the joint lattice's denominator is 1 at `N = 1`, 2 at
`N = 2`, 7 at `N = 7` and 16 at `N = 16`.  So the targets stand at 96, 768, 32928
and 393216 -- `N = 7` searches 343 times `N = 1`'s, where `N = 2` searches 8
times it.  `N = 7` did not finish in ninety minutes.

(An earlier line here turned that into "roughly `7^6` times the work", from the
count inside growing like the sixth power of the target.  The exponent is right
for a rank-12 lattice but the model is not predictive at these sizes: it would
make `N = 2` a quarter of a million times `N = 1`, and both finish in about a
second.  The target ratio is what is measured; the work is not.)  Reaching `N = 7, 9, 16` needs the shell described
arithmetically rather than enumerated -- the cyclotomic analogue of the Moser
chart, which exists but is not written.

## What the answer is worth

`theta_2` is a rotation **nobody has been able to use**: it needs `sqrt7`, absent
from the classical field, and docs/ATTEMPTS.md route 18 records it as
unavailable from the start.  Here it is available, and it passes a test that has
content.

Its union is still not 5-chromatic at the sizes reachable -- cube and conquer
settles 3193 points as 4-colourable in 4926 seconds -- so it joins the list of
filter survivors that do not materialise.  The criterion is one-sided and this is
what that means in practice.
