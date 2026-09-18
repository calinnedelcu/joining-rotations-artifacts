# The richness ranking does NOT predict success -- withdrawn

An earlier version of this file proposed that a rotation creating at least 96
new unit vectors gives a 5-chromatic union and one creating at most 90 does not.
It held on fourteen tests. **The fifteenth broke it and the claim is withdrawn.**

## The counterexample

`alpha_64/3 = arccos(125/128)` over `Q(sqrt3, sqrt11, sqrt23)` creates only
**48** new unit vectors -- tied for the fewest of any candidate -- and its union

    L  union  alpha(L),   L = ball(30 vectors, depth 7, radius 4.64)

is **5-chromatic on 187225 vertices with 2207478 edges**, over a ball holding
all 18 points of its shell.

That is below every rotation the threshold called too poor, including several
that are 4-colourable:

| rotation | new unit vectors | result |
|---|---|---|
| theta_28 | 150 | 5-chromatic |
| theta_36 | 120 | 5-chromatic |
| theta_4, theta_16 | 96 | 5-chromatic |
| theta_20 | 90 | 4-colourable |
| theta_12 | 72 | 4-colourable |
| alpha_20/3, alpha_28/3, alpha_52/3, alpha_80/3 | 66 | 4-colourable |
| theta_44 | 60 | 4-colourable |
| **alpha_64/3** | **48** | **5-chromatic** |
| alpha_4/3, alpha_16/3, alpha_44/3 | 48 | 4-colourable |

So the count of new unit vectors does not order the candidates by whether they
work: 48 contains both a success and three failures, and 60, 66, 72 and 90 are
all failures sitting above it.

## What is left of it

Only this, and it is weak: every rotation at or above 96 that has been tested is
5-chromatic. That is four rotations, and with `alpha_64/3` showing the
implication does not run the other way, there is no reason to expect the
converse either. The right reading is that richness is one ingredient among
several and not a predictor.

`theta_60` at 114 was going to be the decisive test of the threshold. It is no
longer decisive of anything, which removes the main reason to spend a
million-point ball on it.

## What it cost, and what it is worth

The pattern was recorded, tested, and broken within a few hours, which is the
correct outcome for a guess stated precisely enough to fail. It is kept here
rather than deleted because the failure is the informative part: the obvious
density heuristic, which is also the one Parts states informally when he
describes a good rotation as raising the average vertex degree, does **not**
decide which rotations join.
