# The wide pool made dense: the last opening in the classical field

Everything else about the two-part structure is nailed down. `theta_4(L)` meets
`L` in exactly the origin, so a two-part graph always costs `|L| + |S| - 1`;
`theta_4` was believed the unique joining rotation across 83 multiquadratic
fields -- route 44 corrects that, and seven are now known; the
19-vertex interface admits 28 colour patterns and blocking them is nearly free
(100 vertices for one pattern, 135 for all 28), so the large part carries the
whole cost. What is *not* settled is the pool.

Route 2 closes the large-part search over Parts' own pools and names the one
thing that would revive it: a pool substantially outside his region. Route 13
says why every attempt failed -- density decides convergence. Those combine into
a recipe: take the wide ball (radius 2.53, against his large part's 2.024) and
keep only candidates with at least `d` neighbours in the record's own large part.

## The accounting

`parts_side.py` counts the record as **373 free + 136 fixed**, the shared origin
going with the small part. So the bound that beats 509 is **372** on the L side
and **134** on the S side. At 373 and 135 the search re-finds the record.

## Large part, bound 372

| degree floor | pool | answer as share of pool | outside Parts' region | result |
|---|---|---|---|---|
| >= 7 | 641 | 58% | some | **proven optimal at 509**, two seeds |
| >= 6 | 673 | 55% | some | running, proposals down to 370 free |
| >= 5 | 841 | 53% | 53 | running, proposals down to 351 free |
| >= 4 | 1103 | 39% | 85 | running, proposals down to 350 free |

For scale: the pool that converges in minutes is 373 of 412, i.e. 90%; the
8131-point ball that never constrains the master is 4.6%.

The densest pool closes, and it closes fast -- which is the expected shape. The
looser pools stay open and keep proposing candidate graphs in the 486 to 506
range. Every one of those proposals is a genuine candidate for a record and every
one so far is 4-colourable.

## Small part, bound 134

| degree floor | pool | answer as share | result |
|---|---|---|---|
| >= 6 | 164 | 83% | narrow, 28 new candidates |
| >= 3 | 646 | 50% | running |
| >= 2 | 796 | 32% | running |

## The pool saturates, which bounds how far this can be pushed

Rebuilding the degree-5 pool from a ball of radius **3.0** instead of 2.53 gives
**the same 706 points**. No lattice point beyond radius 2.53 has five or more
neighbours in the record's large part, so the candidate set is saturated and the
pool cannot be widened by reaching further out -- only by lowering the degree
floor, which trades reach for the density that makes the search converge.

That is the real boundary of this route: reach and convergence are the same knob.

## What a negative here would mean

Taken with the seam proofs in SEAMS.md, a full set of UNSAT answers would say:
no 508-vertex two-part graph exists whose large part is dense against the
record's, over pools reaching a half-radius beyond Parts' region. That is
strictly stronger than anything published about 509's optimality, and it is the
honest boundary of what this machinery can decide.


## The union of every published part, which is a bigger accumulative graph than his

Parts' method carries progress in an *accumulative graph*: the union of every
minimal graph found. His table reports one per family -- 412 points for the m6a
L-subgraph whose minimal member is 374, and 166 for the S-subgraph whose minimal
member is 136. Choosing 373 of his 412 is already proven impossible here.

But he published fourteen L-side graphs and six S-side ones, and nothing in his
method ranges over their union, because each of his searches sat inside one family:

| side | union of every published graph | the answer as a share | his own accumulative graph |
|---|---|---|---|
| L | **613** points | 61% | 412, where it is 91% |
| S | **183** points | 74% | 166, where it is 82% |

Both unions are 5-chromatic against the matched fixed companion, so both are
legitimate pools, and both reach past where his search went.

**Settled: the S side.** Over the union of all six published S-graphs, with L_374
fixed, there is **no small part of 134 vertices** -- 509 is proven optimal, two
seeds agreeing. That is strictly stronger than the same statement over his
166-point accumulative graph.

The L side, 613 points with the answer at 61%, is running.


## Across families, which no search of his does

Parts' searches each sit inside one family -- an L-subgraph search ranges over
L-subgraphs, an S-subgraph search over S-subgraphs. But every published graph of
every family lives in the same lattice, so their union is a legitimate pool and
nothing in the literature has ever searched it.

| pool | points | the record as a share |
|---|---|---|
| all 43 published graphs | 1577 | 32% |
| points in >= 2 of them | 1306 | 39% |
| record + points in >= 6 | **731** | 70% |
| record + points in >= 5 | 770 | 66% |
| record + points in >= 4 | 830 | 61% |

The frequency threshold has to be paired with the record itself: at threshold 3 and
above the pool is dense but **135 of the record's own vertices are missing from it**,
because the small part's points appear in few published graphs. Unioning the record
back in fixes that and keeps the density.

Within the L family alone the same count is revealing: of the 613 points in the
union of all fourteen published L-graphs, **208 appear in every one of them** -- the
skeleton they all agree on -- and the distribution is sharply bimodal, 208 in all
fourteen and 134 in exactly four.
