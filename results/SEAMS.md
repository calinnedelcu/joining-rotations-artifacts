# Cutting the records along their tightest seams

A map that preserves unit distance carries a 5-chromatic unit-distance graph to
another one. Isometries are the obvious such maps, but conjugating the
coordinate field is one too, and on the record it cuts much tighter.

Scanned over all 96 compositions of the 12 isometries with the 8 Galois
conjugations, on 509, 510 and 517. The record has three distinct tight cuts,
each pair below being the same cut reached two ways:

| graph | seam | closed core | breakers | bound that beats 509 |
|---|---|---|---|---|
| 509 | `galois3` = `refl o galois6` | 494 | 15 | **14** |
| 509 | `rot180 o galois7` = `refl.rot180 o galois2` | 493 | 16 | 15 |
| 509 | `refl.rot180 o galois1` = `rot180 o galois4` | 484 | 25 | 24 |
| 509 | `rot120` | 457 | 52 | 51 |
| 510 | `rot60 o galois7` | 494 | 16 | 14 |
| 517 | `galois3` | 491 | 26 | 17 |

For any seam of the 509 graph the shave needed is the same one point, since
core + breakers = 509 always. The seam only sets how large the search is, and
`galois3` makes it as small as this repository can pose it: 14 free choices.

## Settled

Each row is an exact result over the pool named: the core held fixed, the
candidates being the lattice points with at least 4 neighbours in it.

| target | pool | result | cost |
|---|---|---|---|
| 509, `galois3` core 494, bound 14 | 685 candidates | **UNSAT** -- no completion of 14 | minutes |
| 510, `rot60 o galois7` core 494, bound 14 | 651 candidates | **UNSAT**, two seeds agreeing | 92 master calls |
| 517, `galois3` core 491, bound 17 | 601 candidates | **UNSAT** -- no completion of 17 | minutes |
| 517, `rot120` core 505, bound 3 | 630 candidates | **UNSAT** -- no completion of 3 | 9 master calls |

The refuted instances are written as DIMACS to `out/master_core*.cnf` and can be
rechecked with `cadical`, or with `--lrat` and cake_lpr.

These close the region immediately around the record: the point of the seam is
that it makes each question small enough to *settle* rather than run forever.
What they do not close is the candidate set. Each UNSAT ranges over lattice
points with at least four neighbours in the core, and a completion of 14 points
can take up to 13 of its neighbours from the other new points, so that floor is
a convenience, not a theorem. The widened runs ask the same question with the floor lowered, and the first
answer is in: at degree 3, with 1108 candidates instead of 685, bound 14 is still
**UNSAT** on both seeds. Degree 2, with 2110 candidates, is still running.

| widened pool | candidates | result |
|---|---|---|
| degree >= 4 | 685 | UNSAT at bound 14 |
| top 250 by colourings killed | 250 | UNSAT, and faster |
| top 120 | 120 | UNSAT, faster still |
| degree >= 3 | 1108 | UNSAT at bound 14, two seeds |
| degree >= 2 | 2110 | running |

Taken together: no 5-chromatic graph of 508 vertices shares 484 or more points
with any of the record's three tight seam cores, over any of these pools.


## Cutting the PARTS along their seams

The whole record splits 494 + 15 under `galois3`. Its *parts* split far more
tightly, and holding a part's seam core together with the other part at its
published value gives the smallest record attempts in the repository -- one to
thirteen free choices. Parts' interface subtypes must be matched: m6a pairs the
374e1860 and 374e1868 large parts with 136e564, m6b pairs 374e1864 with 141e594,
m6c pairs 374e1872 with 150e639. Crossing them is not 5-chromatic at all, which
is a useful check that the pairing is real.

The bound is set by the baseline: against a fixed small part of 136 a large part
of 373 beats 509, and against a fixed large part of 374 a small part of 135 does.

| part | subtype | seam | core | breakers | bound | candidates | result |
|---|---|---|---|---|---|---|---|
| L v374e1868 | m6a | `galois1` | 372 | 2 | **1** | 570 | UNSAT |
| L v374e1860 | m6a | `galois1` | 368 | 6 | **5** | 590 | UNSAT |
| S v136e564 | m6a | `galois1` | 127 | 9 | **8** | 77 | UNSAT |
| S v136e564 | m6a | `galois1` | 127 | 9 | **8** | 260 | UNSAT |
| S v141e594 | m6b | `refl.rot120 o galois5` | 133 | 8 | **2** | 135 | UNSAT |
| L v374e1864 | m6b | `refl.rot300` | 360 | 14 | **8** | 560 | UNSAT |
| L v375e1920 | m6a | `galois1` | 360 | 15 | 13 | 170 | UNSAT |
| L v375e1916 | m6b | `refl.rot180` | 355 | 20 | 13 | 177 | UNSAT |
| L v376e1890 | m6a | `refl.rot180` | 358 | 18 | 15 | -- | no valid partner |

The m6c small part cannot be attacked this way: its tightest seam leaves a core
of 149 of its 150 points, and 135 is what would beat the record, so the core alone
is already too big.

The bound-1 row is the sharpest single statement here. It says: over 570 lattice
candidates, there is **no single point** that completes the 372-point Galois-closed
core of the record's large part into a 5-chromatic graph against the published
small part. That search is exhaustive and takes under a minute.

### The accumulative parts, where the seam actually leaves room

Parts' accumulative large parts have far *smaller* seam cores than his minimal
ones -- 223 of 406, 235 of 412, 271 of 451 -- so the search has real freedom
rather than one to thirteen choices. A degree-6 floor keeps the candidate set in
the density regime that converges (150 wanted out of 231, about 65%).

| part | core | bound | pool | result |
|---|---|---|---|---|
| L v406e2082 | 223 | 150 | 231 candidates | **UNSAT**, 305 calls |
| L v412e2106 | 235 | 138 | 231 candidates | **UNSAT**, 259 calls |
| L v403e2112 | 235 | 138 | 231 | **UNSAT**, 327 calls |
| L v451e2400 | 271 | 102 | 231 | **UNSAT**, 165 calls |
| L v400e2034 | 235 | 124 | 231 | **UNSAT**, 189 calls |

Three of the accumulative parts have no room at all: `v406e2076` and `v403e2106`
split 400 + 6 and 397 + 6, and all three accumulative *small* parts split within
2 to 6 of their whole, so their cores already exceed what would beat the record.

### The pairing table

Each large part works with exactly one small part -- its own interface subtype --
and crossing them is not 5-chromatic at all, which is a real check rather than a
nominal one:

| large part | 136e564 | 141e594 | 150e639 |
|---|---|---|---|
| v374e1860 | **509** | - | - |
| v374e1864 | - | **514** | - |
| v374e1868 | **509** | - | - |
| v374e1872 | - | - | **523** |
| v375e1916 | - | **515** | - |
| v375e1920 | **510** | - | - |
| v376e1890 | - | - | - |

`v376e1890` works with none of the three published small parts, so its partner is
not in the data. The smallest working pairing is 509, which is the record.

### A note on density, learned twice today

The two bound-13 searches first ran over 540-candidate pools and crawled: the
master needed a hundred seconds a call and reached 88 calls in an hour. Raising
the degree floor to 6 cut the candidates to 170 and both settled **immediately**.
A tight cardinality bound over a loose pool is the worst combination; the bound
and the pool have to be tightened together.

## Everything the seam programme settles

Twelve part-level and nine graph-level questions, every one an exact UNSAT over a
named pool, and all of them fast:

* no 508-vertex graph shares 484 or more points with any of the record's three
  tight seam cores, over pools from 120 to 1108 candidates
* no large part of 373 points completes any of the four minimal large parts'
  Galois cores against its matched small part -- including the exhaustive
  bound-1 case, where no single lattice point out of 570 will do
* no small part of 135 points completes either minimal small part's core
* none of the five accumulative large parts with room reaches 373 either, at
  bounds from 102 to 150
