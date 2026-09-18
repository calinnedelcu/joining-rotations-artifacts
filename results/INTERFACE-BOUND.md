# Every type-M construction needs at least five cross edges

For `G = L u theta(S)` inside the Moser lattice, with `L` and `theta(S)` sharing
only the origin, the only edges between the halves are the cross edges of the
pool.  This file states how many of them a 5-chromatic `G` must use, for each
joining rotation, and corrects the figure it gave for `theta_4`.

## The argument

`hn.algcolour` gives closed-form 4-colourings of the Moser lattice: group
homomorphisms `phi : Lambda -> C` with `|C| = 4` killing no unit vector, so
proper on the whole infinite lattice at every radius.  There are **eight** -- two
Klein and six Z/4.

Both halves are subsets of that same lattice.  The rotation only decides which
pairs end up at unit distance across the halves, so these colourings apply
whatever joins them.  Colour `L` by `phi`, colour `theta(S)` by `pi . psi` where
`pi` permutes the four colours, and the result is a proper 4-colouring of `G`
**unless some cross edge comes out monochromatic**.  A 5-chromatic `G` must
therefore use a set of cross edges meeting the monochromatic set of every
pairing: a minimum hitting set, decided exactly by SAT.

`scripts/interface_bound.py A` does this for the rotation spinning the shell at
squared radius `A`.

### Which permutations are admissible, and why nine was wrong

**An earlier version of this file claimed nine, and nine counts pairings that are
not colourings of `G` at all.**

A homomorphism sends the origin to colour 0, on both sides.  The halves share the
origin, so the union's colouring is well defined there only if `pi(0) = 0`.  Just
**6 of the 24** permutations satisfy that; the other 18 give the shared vertex two
different colours at once and describe no colouring of `G`.  Requiring a
construction to defeat them is an extra constraint with nothing behind it, and it
is what inflated the bound.

Checked rather than argued: over all 1536 pairings, "the permutation fixes colour
0" and "the origin receives one colour" agree in **every single case**, 0
disagreements.  And the explicit 5-edge interface `{62, 65, 67, 68, 84}` hits all
235 admissible patterns while missing 337 of the 1171 that the 24-permutation
count produces -- those 337 being exactly the inadmissible ones.

Counting only admissible pairings: 8 x 8 x 6 = 384 pairings, **235** distinct
patterns, none empty.

## Results

**Theorem 1.** No 5-chromatic `L u theta_4(S)` over this lattice has four or
fewer cross edges, and five is attainable against these colourings.

*Proof.* The hitting-set instance at bound 4 is unsatisfiable, at bound 5
satisfiable.  Any construction with at most four cross edges leaves some
admissible pairing of the closed-form colourings with no monochromatic cross
edge, hence properly 4-colours `G`. ∎

**The cross structure, first, because it explains the rest.**  Of the pool's 126
cross edges, 60 touch the shared centre and 66 do not, and those 66 **are
themselves a perfect matching**: each of the 66 active points on either side has
cross-degree exactly **one**.  The other 8065 of the ball's 8131 points -- 99.2%
of it -- are cross-isolated and can sit in `L` with no effect on the interface at
all.  So every interface avoiding the centre is automatically a matching, and the
only structure left to determine is which edges and how many.

**Theorem 2.** There are exactly **1920** cross-edge sets of size five meeting
every admissible pattern.  No edge is common to all of them; their union is all
**66** non-centre cross edges; and none of them touches the centre -- necessarily,
since a homomorphism sends the centre to colour 0 and no unit vector to 0, so an
edge out of the centre can never come out monochromatic.

**Which is also where "six in `L` and nine in `theta_4(S)`" came from.**  Nine
edges of a matching would need nine distinct endpoints on *each* side, eighteen
vertices, not fifteen.  The old figure's size-nine interfaces landed on fifteen
because they **used the centre-incident edges**, with the centre serving as a
repeated endpoint -- and those are exactly the edges that only ever look
monochromatic under a permutation that gives the centre two colours.  The
inconsistency between "meeting only at the origin" and a 6+9 shape was the
symptom; the 24 permutations were the cause.

**Theorem 3.** Read in Parts' own taxonomy, every one of the 1920 is the same
shape.  He splits the cross edges into a *reference* orbit, both ends at radius
2, an *auxiliary* orbit at radii `sqrt11/2 -+ sqrt3/6` joined crosswise, and the
edges out of the centre -- here 30, 36 and 60 of the 126.  Every minimal
interface is

    exactly 1 reference edge  +  exactly 4 auxiliary edges,

with the four auxiliary edges split two and two between the crosswise
directions: two with the `L` endpoint at `sqrt11/2 + sqrt3/6 = 1.9470` and the
`S` pre-image at `sqrt11/2 - sqrt3/6 = 1.3696`, and two the other way round.
There is no other profile among the 1920 -- not one interface with two reference
edges, none with five auxiliary, none touching the centre.

**Theorem 4, which is the whole list.**  The 1920 factor exactly:

    1920  =  30  x  8  x  8

* any one of the **30** reference edges, with no restriction;
* then one of exactly **8** admissible pairs from the 18 auxiliary edges in one
  crosswise direction;
* and one of exactly **8** admissible pairs from the 18 in the other.

Every reference edge carries exactly 64 interfaces, and every combination of the
three choices occurs, so this is a product and not a list of coincidences.  Out of
the `C(66,5) = 8936928` five-subsets of the usable cross edges, these 1920 are the
0.021% that work, and they are described completely by the three choices above.

So the interface is pinned down to the radius of all ten of its vertices and to a
choice from 30 x 8 x 8.  That is a much sharper starting point for synthesis than
"six in `L` and nine in `theta_4(S)`", and it lands on exactly the orbits whose
subtypes M6A/M6B/M6C Parts calls under-explored.

## The same bound for every joining rotation

Each ball must hold the **whole** shell the rotation spins, or the rotation has
not been given the points it acts on and the answer is about the wrong pool.
That is the routes 20/44/48 error, and `interface_bound.py` now refuses rather
than reports when the ball falls short.

| rotation | shell | ball | cross edges in the ball | needs at least |
|---|---|---|---|---|
| `theta_4` | 30/30 | depth 4, r 2.53 | 126 | **5** |
| `theta_28` | 60/60 | depth 6, r 5.31 | 156 | **5** |
| `theta_36` | 54/54 | depth 7, r 6.02 | -- | **5** |
| `theta_16` | 30/30 | depth 4, r 4.05 | 126 | 1 |
| `alpha_64/9` | 6/6 | depth 3 | 66 | 1 |
| `alpha_256/9` | 6/6 | depth 6, r 5.35 | 66 | 1 |
| `alpha_64/3` | 18/18 | depth 7, r 4.64 | 78 | 1 |
| `theta_12` | 42/42 | depth 6, r 3.5 | 102 | **none exists** |
| `theta_20` | 60/60 | depth 7, r 4.5 | -- | **none exists** |

### The ball can fall short, and for `theta_28` it does

`theta_28`'s joint lattice has **180** unit vectors, and the depth-6 ball above
realises **156** of them.  That is the wrong direction for a lower bound:
patterns computed on a subset of the cross edges are subsets, so they are harder
to hit and the minimum comes out too large -- a pool bound is an upper bound on
the lattice bound, not a lower one.  The guard in `interface_bound.py` checks the
SHELL, not the cross-edge count, so it did not catch this.

Proposition 18 removes the ball entirely: a cross edge *is* a unit vector of the
joint lattice, and what it contributes depends only on that vector.
`scripts/interface_bound_exact.py` does the whole computation that way -- no
depth, no radius, instant -- and reproduces `theta_4` exactly (126 cross edges,
60 at the origin and 66 usable, 384 pairings, 235 patterns, UNSAT at 4 and SAT
at 5).  Over the complete lists:

| rotation | cross edges | at the origin | usable | patterns | bound |
|---|---|---|---|---|---|
| `theta_4` | 126 | 60 | 66 | 235 | **5** |
| `theta_16` | 126 | 60 | 66 | 157 | 1 |
| `theta_28` | **180** | 60 | **120** | 220 | **5** |
| `theta_36` | 150 | 60 | 90 | 85 | **5** |
| `alpha_64/9` | 66 | 60 | 6 | **1** | 1 |
| `theta_12` | 102 | 60 | 42 | 25, **48 empty** | none exists |
| `theta_20` | 120 | 60 | 60 | 25, **48 empty** | none exists |

So `theta_28` does tie `theta_4` at five, and now over the lattice rather than
over a 156-edge pool.

`theta_12` and `theta_20` produce 48 **empty** patterns each -- admissible
pairings with no monochromatic cross edge, so a proper 4-colouring of the whole
union.  No 5-chromatic `L u theta(S)` exists over that lattice at any size, for
either.  Both agree with what `results/alpha64_3/README.md` already records for
them by a different route, which is the check that matters: the method reaches the
known answer where there is one to compare against.  `theta_9` and `theta_3`, both
known 4-colourable, are killed the same way.

`theta_24` is not in the table because the shell at squared radius 24 is
**empty** in this lattice: that rotation has nothing to act on.

## Verification

The chain from lattice coordinates to patterns is checked against the
repository's own exact edge finder rather than trusted:

1. Twelve admissible pairings, each used to colour the whole union, checked
   against all **150138** exactly recomputed edges of the pool: **zero**
   monochromatic internal edges, so every closed-form colouring really is proper
   on each half, and the monochromatic cross edges match the predicted pattern
   count in every case.
2. `theta_4` returns its bound over a pool with 126 cross edges as well as over
   the original's 96, so the number is not an artefact of one ball.
3. Every rotation's ball is checked to hold its **whole** shell before anything
   is reported; the script exits rather than answers when it does not.
4. The two rotations killed here over shell-complete balls, `theta_12` and
   `theta_20`, are independently known 4-colourable.
5. On the 509-vertex record itself, all 384 admissible pairings are non-empty --
   an empty one would have 4-coloured a graph known to be 5-chromatic.

## The record's own interface, measured against the bound

Parts' 509-vertex graph is `L u theta_4(S)` with `|L| = 374`, `|S| = 136`, one
shared vertex, 2442 edges and exactly **18 cross edges**.  Running the same
computation on that graph rather than on a ball:

* **384 admissible pairings, none empty.**  This is the strongest check the
  method gets: an empty pattern would be a proper 4-colouring of the record, and
  the record is 5-chromatic.
* **Six of the 18 cross edges suffice** to defeat every closed-form colouring --
  edges 0, 1, 2, 5, 6, 7 -- and they form a perfect matching, 6 endpoints in `L`
  and 6 in `theta_4(S)`, the same shape Theorem 2 forces.  Five is not reachable
  inside the record's own interface; the 1920 five-edge matchings live among the
  ball's 126 cross edges, and the record carries only 18 of them.
* All 18 appear in some pattern, so none is idle.

So the bound accounts for **6 of the record's 18 cross edges**, and the remaining
**12 are there to defeat colourings that are not homomorphisms** -- which is
precisely the part of the problem this argument cannot see, and a measurement of
how far a lower bound of this kind can reach.

## Is five an artefact of using only homomorphisms?  No.

The homomorphism colourings are exactly the **linear** proper colourings of
`Lambda/m*Lambda`.  Every proper colouring of that finite quotient pulls back to a
proper colouring of the whole lattice, linear or not, so every one is a legitimate
colouring of a half and adds patterns -- which can only raise the bound.
`scripts/interface_bound_periodic.py` uses all of them.

The Moser lattice has rank 4, so the quotients are small enough to enumerate
outright:

| modulus | cosets | proper 4-colourings (centre fixed) | bound |
|---|---|---|---|
| 2 | 16 | 12 -- exactly 2 Klein kernels x 6 permutations | 1 |
| 3 | 81 | **none** | -- |
| **4** | 256 | **120**, against the 48 the homomorphisms give | **5** |
| 6 | 1296 | 12 | 1 |
| 8 | 4096 | 300 enumerated (capped) | **5** |

At `m = 2` every proper colouring is linear, so nothing is lost there.  At `m = 4`
there are **72 valid colourings the homomorphism count misses**, giving 14400
pairings and 1237 patterns against 384 and 235 -- and the bound is still **5**.
So five survives a strictly larger and, at `m = 4`, complete class of colourings.
Nine is not recoverable by strengthening.

The same holds for the other rotations: at `m = 4`, `theta_16` stays at 1 (433
patterns from 14400 pairings) and `alpha_64/9` stays at 1 -- from a striking **single**
distinct pattern across all 14400 pairings, meaning one fixed set of cross edges
comes out monochromatic under every periodic colouring of that join.

(The smaller numbers at `m = 2` and `m = 6` are not weaker claims about the
lattice; they are smaller colouring families, and a smaller family gives a lower
bound.  `m = 4` is the one that contains the homomorphisms.)

## Every "1" in that table is degenerate, and means nothing

The four rotations reported at 1 are not weakly constrained -- they are not
constrained at all by this argument, and the 1 is an artefact.  Each has cross
edges that are monochromatic under **every** pairing: 30 of them for `theta_16`,
6 for `alpha_64/9`.  One such edge hits every pattern by itself, so the hitting
set is 1 whatever the rest of the geometry does.

The cause is arithmetic.  An edge is always monochromatic when both its endpoints
lie in `m*Lambda`, since both halves then give the shared centre's coset colour 0,
and that needs the joint lattice to hold a vector of length `1/m`.
`scripts/join_filter_residues.py` reports the same condition as the residue pair
`(0, 0)` occurring.  `theta_4`, `theta_28` and `theta_36` have no such edge.

So the table has two kinds of entry and not two values:

| a real bound | degenerate, no bound |
|---|---|
| `theta_4` = 5, `theta_28` = 5, `theta_36` = 5 | `theta_16`, `alpha_64/3`, `alpha_64/9`, `alpha_256/9` |

The three real ones all come out at **5**.  Whether that is a coincidence of three
cases is open, and the bound predicts nothing about construction size either way --
`theta_28` and `theta_36` share `theta_4`'s bound with smallest known unions of
156577 and larger against 509.

The script now says `DEGENERATE` rather than reporting the 1 silently.

## What the bound does not do

It does not predict construction size.  `theta_28` ties `theta_4` at five, and the
smallest 5-chromatic union known for it is 156577 vertices against `theta_4`'s
509.  `theta_16` needs only one cross edge -- the weakest obstruction measured --
and its best graph is 2901.  So the interface bound measures how hard the
closed-form colourings are to defeat, and that is not the same quantity as how
small a construction can be.

## Direction

One-sided in the safe direction: these patterns come from homomorphism colourings
only, and any colouring of the halves that is not of that form would add
patterns, which can only raise the bound.  Five is a floor.

Theorem 2 constrains synthesis rather than minimisation: choose a perfect
matching of five cross edges avoiding the origin, and ask what `L` and `S` must
contain to realise it.
