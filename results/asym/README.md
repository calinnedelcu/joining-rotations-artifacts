# The asymmetric basin: trimming stops at 1279, the exact descent does not

Route 20 observed that every sweep in the literature builds both halves of a
type-M construction from the same unit-vector family, while the record itself
does not -- its large part uses 30 vectors and its small part 18.  Dropping the
symmetric default gives the smallest pool in which a 5-chromatic graph is known
to sit: **2365 points**, against 3997 for the symmetric one.

## What randomised trimming finds

| search | settles at |
|---|---|
| randomised trimming, seed 1 | 1279 |
| seed 3 | 1289 |
| seed 2 | 1301 |
| the exact hitting-set master, separately | 1306 |

Four searches within 27 vertices of each other.  That agreement was read, in an
earlier version of this file, as the basin being *characterised* at 1279.

## That reading was wrong

Agreement between greedy searches measures where greedy stops, not where the
graph stops.  Feeding the 1279-vertex graph to the exact search's
vertex-critical bootstrap -- which asks, for each vertex in turn, whether the
graph minus that vertex is still 5-chromatic, and needs an UNSAT proof to say
yes -- walks straight past 1279 and keeps going:

| stage | vertices |
|---|---|
| randomised trimming plateau | 1279 |
| exact bootstrap, waypoint verified independently | 1146 |
| the pass, run to completion, seed 31 | 893 |
| **the same pass, a different pool and shuffle** | **889** |

`minimised889.pts` is the best: **889 vertices, 4390 edges**, minimum degree 4.
Re-checked from disk in a fresh process -- edges recomputed from the coordinates,
4000 of them re-tested exactly in the field with none wrong, and not 4-colourable
in a solver that saw none of the search's clauses.  It is vertex-critical over its
pool: the pass ends only when no single vertex can be dropped, and it closed with
1778 cuts from 889 critical colourings.

Two independent lineages -- different candidate pools, different shuffles -- landed
at **893** and **889**, four vertices apart.  That agreement is worth more than the
four trimmings agreeing at 1279 was, because these are the stopping points of an
exact pass rather than of a greedy one; but on this pool's own record, agreement
between searches has already been read as a floor once and been wrong, so it is
reported as the best known and not as the floor.

Randomised trimming stopped **44% above** where the exact pass stops.

Two further passes over the 893-vertex graph, with different shuffles, tested
**500 and 600 of its vertices between them and dropped none**.  They were stopped
short of completing, so this is evidence rather than the proof that
`results/alpha64_9/` has for its 1408, but 1100 vertex tests without a drop is
what a vertex-critical graph looks like and not what a plateau looks like.

Two cheap things make this pass affordable, both in `hn/hitting.py`:

* **Peeling.**  If G is 5-chromatic and some vertex has degree < 4, then G minus
  that vertex is still 5-chromatic -- a 4-colouring of the rest leaves one of the
  four colours unused among its at most three neighbours, so it would extend.
  Every drop can push a neighbour below the threshold, so the removals cascade,
  and none of them costs a SAT call.
* **Saving every drop.**  The pass runs for hours and its intermediate graph used
  to live only in memory; it is now written out at each drop, so a run can be
  resumed from where it stopped instead of restarted from the top.

## What this does to the number we refuted

An earlier version of this file refuted the landscape table's claim that this
pool minimises to "848 to 1051", on the grounds that four searches put the floor
near 1280.  That refutation is withdrawn.  The exact descent is below 1071 while
this is being written, inside the range it was said to have refuted.  The
landscape figure is still unsourced and still not reproduced -- but it is no
longer contradicted by anything measured here.

## What it is not

The 2365-point pool does **not** contain the 509-vertex record -- its small part
reaches a radius this ball does not -- so whatever this basin's floor turns out
to be, it is the floor of a different basin, not a step toward the record.
