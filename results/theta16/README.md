# theta_16: a second joining rotation

`theta_16 = arccos(31/32)`, with `sin = 3*sqrt7/32`, is a joining rotation of the
30-vector Moser lattice over **Q(sqrt3, sqrt7, sqrt11)**. It acts on the 30
lattice points at radius exactly 4, and

    L  union  theta_16(L),   L = ball(30 vectors, depth 4, radius 4)

is 5-chromatic on 29113 vertices with 285294 edges.

**Minimised to 2901 vertices, 16735 edges** (`t16_best.pts`), verified: every
edge recomputed from the coordinates and re-tested exactly, minimum degree 4,
not 4-colourable in a fresh solver.

## Why it was never found

A spindle rotation `theta_i` moves only the lattice points at distance `sqrt(i)`
from the centre. Every sweep in this repository -- 83 fields, about 2700 rotations
(docs/ATTEMPTS.md route 20) -- used a ball of radius 2.2 to 2.53, and such a ball
contains integer squared radii 1, 3 and 4 only. `theta_16` needs radius 4 and
`theta_7` needs 2.646, so neither had a single point to move.  A ball must reach the
shell to reveal the rotation even though the minimised graph no longer contains it. They were never
tested, and the conclusion that `theta_4` is unique was an artifact of ball size.

## The complete sweep

The lattice needs `sqrt33`, so the field is `Q(sqrt3, sqrt11, sqrt m)` and the
realisable integer radii do not depend on `m`. Each radius is unlocked by exactly
one `m`, so the sweep is finite -- and run at radius 4 and 5, where the shells
exist, it gives **exactly two** joining rotations:

    theta_4  in Q(sqrt3, sqrt5, sqrt11)   union 18625   5-chromatic   the record's
    theta_16 in Q(sqrt3, sqrt7, sqrt11)   union 29113   5-chromatic   new

and eight failures: `theta_5` (m=19), `theta_9` (m=35), `theta_11` (m=43),
`theta_12` (m=47), `theta_13` (m=17), `theta_15` (m=59), plus `theta_7`,
`theta_19` and `theta_25`, which live in the classical field itself and fail there
at up to 79891 points. So the classical field really does admit only `theta_4`.

## Verification

Checked in a fresh process, with the field switched and every table rebuilt:

* the rotation has modulus exactly 1 in the field, not to a tolerance
* all 30 lattice generators are exactly at unit distance from the origin
* the 30 shell points have norm exactly 16
* 29113 distinct points, 285294 edges, 0 wrong among 4000 re-checked exactly
* every vertex has degree at least 4
* **not 4-colourable with no triangle pinned** -- the assumption-free check, 1047 s

## Minimisation

Iterated UNSAT-core extraction took 29113 to 6878; sampled descent with long mixed
schedules reached 3309; shrinking one side with the other held fixed reached 2999.
`t16_best.pts` here is the smallest found so far, and it splits into a forcer side
with no `sqrt7` and a rotated side that has it, joined by a few dozen edges -- the
same profile as the record, which is 374 + 136 with 18 connection edges.

One thing the descent revealed: the reduced graph has **no point left at radius 4**.
The shell that `theta_16` spindles, and that is the whole reason the rotation was
worth testing, is gone -- so the surviving subgraph is 5-chromatic through some
leaner structure, and the textbook forcer/exploiter decomposition cannot be used to
speed the descent up. That also means the shell mechanism is how to *find* such a
family, not necessarily how its small members work.

This is **not** a record: 509 still stands. What is new is the family, and its
minimum is unknown. Greedy deletion reaches a minimal graph rather than a minimum
one and stalls between 848 and 1051 even in the classical field, so the exact
hitting-set master has to finish the job.

## Reproducing

```bash
.venv/bin/python scripts/big_spindles.py --radius 4.0          # find it
.venv/bin/python scripts/new_rotations.py --radius 4.0         # the full sweep
.venv/bin/python scripts/shrink_t16.py --radius 4.0 --seed 0   # minimise it
```
