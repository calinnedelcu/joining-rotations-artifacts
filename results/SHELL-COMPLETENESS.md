# The negatives were inconclusive, and why

`scripts/shells.py` decides exactly how many lattice points sit at a given
squared radius.  Comparing that against what each test's ball actually held:

| shell | points that exist | points in the ball | verdict reached | status |
|---|---|---|---|---|
| 4 | 30 | 30 | 5-chromatic | complete |
| 16 | 30 | 30 | 5-chromatic | complete |
| 28 | 60 | 60 | 5-chromatic | complete |
| 36 | 54 | 30 | 5-chromatic | **positive, so still sound** |
| 12 | 42 | 30 | 4-colourable | **INCONCLUSIVE** |
| 20 | 60 | 36 | 4-colourable | **INCONCLUSIVE** |
| 44 | 30 | 18 | 4-colourable | **INCONCLUSIVE** |
| 60 | 84 | 36 | 4-colourable | **INCONCLUSIVE** |

A positive needs no completeness: a 5-chromatic subgraph is 5-chromatic
whatever else is absent.  A **negative does**: if the ball holds only part of
the shell, the rotation was never given its whole set of points to act on, and
4-colourability of that union says nothing about the rotation.

**Every negative result obtained so far is of the second kind.**

## What this costs

The threshold claim -- that rotations creating at least 96 new unit vectors are
5-chromatic and those creating at most 90 are not -- rested on the negatives.
Those do not hold up, so the claim is withdrawn as stated. What survives is the
positive half: four rotations are confirmed 5-chromatic, at 96, 96, 120 and 150
new unit vectors, and no rotation below 96 has yet been confirmed either way.

`theta_60` at 114 was run as a genuine test of the threshold and came back
4-colourable -- but with only 36 of its 84 shell points present, so it neither
confirms nor refutes.

## The fix

`scripts/test_join.py` now compares the ball's shell count against
`shell_count` and says plainly when a negative cannot be trusted. The guard
used to check only that the shell was non-empty, which is the same error one
level down: a ball that reaches the shell is not the same as a ball that
contains it.


## Re-run with complete shells

`theta_12` and `theta_20` were cheap to redo once the required depth was known
(5 and 6, not 4 and 5):

| shell | depth | shell points | union | verdict |
|---|---|---|---|---|
| 12 | 5 | **42/42** | 50485 | 4-colourable |
| 20 | 6 | **60/60** | 122245 | 4-colourable |

So both negatives survive the correction. `theta_44` needs depth **9** (314935
points) for its 30 shell points and is running; `theta_60` needs more than 8.

## The residual caveat, stated plainly

A complete shell removes the most obvious defect, not the last one. Even with
every shell point present, a larger ball could still turn out 5-chromatic, so a
negative is always "4-colourable at this ball", never "this rotation cannot
work". Only the positives are permanent.

The threshold, restated honestly, is therefore a pattern between *confirmed
5-chromatic* and *not yet 5-chromatic at the balls tried* -- weaker than it
first looked, and worth keeping only because the two groups still do not
interleave.
