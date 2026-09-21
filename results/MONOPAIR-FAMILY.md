# The joining rotations follow Parts' mono-pair distances

Three of the rational rotations that give 5-chromatic unions spin shells at
distance **8/3**, **16/3** and **8/sqrt3**. All three come from Parts' mono-pair
lengths -- the distances at which his gadgets force two points to share a colour
in every 4-colouring. His inventory (`data/parts/graphs.txt`) lists two such
gadgets, at **8/3** (367 vertices) and **8/sqrt3** (421 vertices); 16/3 is twice
the first. An earlier version of this file said only the first two were his,
which is wrong and briefly propagated into the manuscript.

Walking the family outward, squared radius `64n^2/9` for distance `n * 8/3`:

| n | distance | squared radius | shell | cos | field | filter |
|---|---|---|---|---|---|---|
| 1 | 8/3 | 64/9 | 6 | 119/128 | Q(v3,v11,v247) | **survives** -- 5-chromatic, 5809 |
| 2 | 16/3 | 256/9 | 6 | 503/512 | Q(v3,v11,v1015) | **survives** -- 5-chromatic, 158257 |
| 3 | 8 | 64 | 30 | 127/128 | Q(v3,v11,v85) | **survives** -- untested |
| 4 | 32/3 | 1024/9 | 6 | 2039/2048 | Q(v3,v11,v4087) | **survives** -- untested |

**Every member tested survives the filter, and both members small enough to
build are 5-chromatic.**

## Why this is more than a coincidence

The classification finds the surviving rotations one at a time, and they looked
scattered: integer shells 4, 12, 16, 20, 28, 36, 44, 48, 52, 60, plus rational
ones at 64/9, 64/3, 256/9. The mono-pair family explains part of that scatter.
`n = 3` gives squared radius 64, which is outside the `a <= 60` sweep entirely --
so the family predicts candidates the sweep never looked at.

It also ties the classification to Parts' own construction theory rather than
leaving it as an arithmetic accident. A mono-pair at distance `d` is exactly a
pair of points forced to agree in every 4-colouring; rotating one onto the other
is what turns that into a contradiction. That the same distances show up as
*joining* rotations for plain lattice balls is a connection worth stating.

## What is not shown

`n = 3` and `n = 4` survive the filter but are untested: `n = 3` spins a shell at
radius 8, needing a ball beyond what this pipeline can build, and `n = 4` is
further still. Surviving the filter means *candidate*, never construction.

And a family whose first four members all survive is four data points. Whether
every `n` survives, and why, is open.

Reproduce: `scripts/monopair_family.py`.

## The family is exactly the set that works, among denominator 9

All **27** denominator-9 candidates -- every rotation with `b = 9` surviving the
filter and having a real shell -- have now been built and tested, each over a
ball holding its complete shell.

**Exactly two give 5-chromatic unions: 64/9 and 256/9.**

Those are the mono-pair distances `8/3` and `16/3`, the `n = 1` and `n = 2`
members of the family. The other twenty-five, spread over squared radii from 4/9
to 268/9, are all 4-colourable.

So within this denominator the mono-pair family is not merely *contained in* the
set of working rotations -- it **is** that set. The classification produces 27
candidates and the mono-pair structure picks out the 2 that work.

That is the strongest evidence here that the criterion's survivors are not
interchangeable, and that Parts' mono-pair distances are the right organising
idea for which of them actually join.

## n = 3 is reachable in principle, and deliberately not run

`theta_64 = arccos(127/128)` over `Q(sqrt3, sqrt11, sqrt85)` spins the shell at
radius 8, which has 30 points, and a depth-9 ball of **428953** points holds all
30 of them. So unlike `theta_60` this one is buildable: the union would be about
858000 points and roughly 11 million edges.

It was not run. `theta_44` succeeded at 629293 points and 7.9 million edges;
this is about 40% larger, and at the time of the attempt the host had 7.4 GB of
RAM free with 5 of its 6 GB of swap already in use. Pushing a SAT instance of
that size onto a machine in that state would have made it unusable for its
owner, for a test the family already predicts the answer to.

What it needs: a solver driven from a file rather than through Python lists,
which is where the clause memory goes, or simply a larger machine. Both are
straightforward; neither was available tonight.
