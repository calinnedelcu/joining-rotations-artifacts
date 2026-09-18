# alpha_64/9 = arccos(119/128): the sixth joining rotation, and the smallest union

Over **Q(sqrt3, sqrt11, sqrt247)**, spinning the 6 lattice points at squared
radius 64/9 (that is, at distance 8/3),

    L  union  alpha(L),   L = ball(30 vectors, depth 3, radius 2.69)

is **5-chromatic on 5809 vertices with 41982 edges** -- by a wide margin the
smallest union any joining rotation produces.

| rotation | union |
|---|---|
| **alpha_64/9** | **5809** |
| theta_4 (the record's) | 18625 |
| theta_16 | 29113 |
| theta_28 | 156577 |
| theta_36 | 175825 |
| alpha_64/3 | 187225 |

## What is new

The rotation is route 48's: `cos = 119/128`, the rotation that turns Parts'
367-vertex mono-pair gadget at distance 8/3 into a 733-vertex graph. What is new
is that it also works as a **plain union of a lattice ball with its image**, the
type-M construction, with no gadget involved.

That matters for the record. A gadget doubling gives `2|F| - 1` and stops there;
a ball union is a pool, and pools are what minimisation works on.

## Verification

1. rotation modulus exactly 1 in the field
2. all 30 lattice vectors exactly at unit distance
3. 5809 points loaded from disk
4. 12 at squared radius exactly 64/9 (6 original, 6 rotated -- the whole shell)
5. 41982 edges recomputed from the coordinates
6. 0 wrong among 840 edges re-tested exactly in K
7. minimum degree 5
8. not 4-colourable, fresh solver, nothing carried over

Reproduce: `scripts/batch_joins.py 64/9` (about 5 seconds).


## Minimised

Randomised trimming on three seeds, run to exhaustion:

| seed | settled at |
|---|---|
| b | 1424 vertices, 7184 edges |
| **c** | **1408 vertices, 7013 edges** |
| a | still descending from 1717 when stopped |

`minimised.pts` / `.edge` is the 1408-vertex graph.  Verified: minimum degree 4,
no wrong edge among those re-tested exactly in the field, and not 4-colourable in
a fresh solver.

**1408 is 2.77 times the 509 record.**  The descent from 5809 stalled there, and
the stall was predicted: the cost per deleted vertex tripled every 200 vertices,
which pointed at 1400-1500 before either run finished.

## 1408 is vertex-critical, and that is why it holds

Two seeds agreeing was the original reason for calling the basin characterised.
That reasoning is not sound -- on the asymmetric pool four trimmings agreed
within 27 vertices and the exact pass went 43% below them
(`results/asym/README.md`).  So the same test was run here.

`scripts/descend.py` asks, for every vertex in turn, whether the graph minus that
vertex is still 5-chromatic, which takes an UNSAT proof to answer yes.  Over all
**1408** vertices, in 3164 seconds, it found **not one** that can be dropped:

    best 1408 vertices; proven minimum over this graph: True

So every vertex of this graph is necessary.  `1408` is not a plateau where a
greedy method happened to stop -- it is a **vertex-critical** graph, and the
earlier claim was right for a reason it did not give.  This is the contrast that
makes the asymmetric correction meaningful: the same pass on a graph of nearly the
same size (1279 vertices, 7927 edges against 1408 and 7013) shed 386 vertices.

What this is: the first minimisation of this rotation's family.  Parts had the
733-vertex graph from doubling his 367-vertex gadget, and never minimised the
family; the ball-union construction reaches 1408 from a different direction.
The two are not comparable -- 733 is a gadget doubling, 1408 a trimmed pool --
and neither approaches 509.
