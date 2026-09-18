# Deciding a joining rotation with no ball, over the complete cross structure

`scripts/join_filter_residues.py A` answers, in seconds and at every radius at
once, whether any 5-chromatic type-M construction `L u theta_A(S)` can exist over
the Moser lattice.

## Why a ball was thought to be needed, and why it is not

Every earlier test of a rotation built a ball, found its cross edges and ran SAT.
That costs hours for large `A` -- `theta_36` needs a depth-7 ball of 144289 points
-- and it answers only about that ball.  Reading such an answer as an answer about
the lattice is the single error this repository has made three times (routes
20/44/48), and three more times in one sitting on 2026-09-16.

A periodic colouring of `Lambda/m*Lambda` gives a cross pair `(p, q)` its two
colours through `p mod m*Lambda` and `q mod m*Lambda` **alone**.  So the only
thing any such colouring can see is which **residue pairs** occur among cross
pairs, and there are at most `(m^4)^2 = 65536` of those at `m = 4`.

A residue pair `(alpha, beta)` occurs exactly when some `p = alpha`, `q = beta`
mod `m*Lambda` satisfy `|p - theta(q)| = 1`.  Since

    p - theta(q)  in  (alpha - theta(beta)) + m*(Lambda + theta Lambda),

and every element of that coset is reachable -- `Lambda_J = Lambda + theta Lambda`
means any `m*w` splits as `m*alpha' + theta(m*beta')` -- the question is:

> does that coset contain a **unit vector of the joint lattice**?

Those are enumerated exactly by the trace form, as integer points of a
positive-definite ellipsoid.  No ball, no radius, no depth.

Two things make it fast.  `coords` is linear, so
`coords_J(alpha - theta(beta)) = coords_J(alpha) - coords_J(theta(beta))`: that is
`2 * m^4` coordinate computations rather than `m^8`.  And the colourings are the
proper 4-colourings of `Lambda/m*Lambda`, a graph on 256 vertices at `m = 4`, of
which the Moser lattice has exactly **120** with the centre's colour fixed.

If some pair of them disagrees on every occurring residue pair, the whole infinite
union is properly 4-coloured, for every `L` and `S` at every radius, forever.

## The degeneracy this has to check, and nearly did not

If the residue pair `(0, 0)` occurs, the filter can never kill.  Both halves give
the shared centre's coset colour 0, so that pair is monochromatic under **every**
pairing.  `(0,0)` occurs exactly when some joint unit vector lies in
`m*Lambda_J`, that is when `Lambda_J` holds a vector of length `1/m`.

The resulting "survives" is true -- no `m`-periodic colouring 4-colours that union
-- but it is **automatic**: it holds for every rotation with a `1/m` vector, wherever
the halves sit, so it separates nothing.  At `m = 2` the condition is precisely
"the joint lattice has a half-unit vector", which is route 49's own criterion, so
every rotation that criterion passes is degenerate at `m = 2` by construction.
The same caveat is recorded for even shell radii in `results/SHELLS.md`.

The script reports `DEGENERATE AT MODULUS m` rather than `SURVIVES`.  **It was
written without this check, and the first sweep run called `theta_48` and
`theta_64` new survivors on the strength of it.  They are not.**

That note and the verdict table above disagreed for a while, and the paper
inherited the table: `theta_48` and `theta_80` were listed as DEAD with no record
of the modulus, while the note called them degenerate.  Both are true of different
moduli, which is exactly why the modulus has to be recorded.  Rerun 2026-09-18:
`theta_48` and `theta_80` are degenerate at `m = 4` and at `m = 6`, and **DEAD at
`m = 8`**, with witnesses in `results/periodic/`.  `theta_64` is degenerate at
every modulus tried and is not killed at all -- it joins, by the chaining lemma.

## A kill is a certificate, and it is checked

`scripts/verify_kill.py A --depth D --radius R` takes the two colourings the
filter produces, builds a real ball holding the whole shell, colours `L` by the
first and `theta(L)` by the second, recomputes **every** edge of the union from
the coordinates, and counts the monochromatic ones.  It has to be zero.

| rotation | ball | union | edges recomputed | monochromatic |
|---|---|---|---|---|
| `theta_12` | depth 6, all 42 shell points | 78890 | 867054 | **0** |
| `theta_20` | depth 7, all 60 shell points | 176978 | 2076192 | **0** |

**This check is not ceremony -- it caught the bug that invalidated the first
version.**  `Lattice.combine` sums over the LLL basis while `Lattice.coords`
reads off the echelon one, so `combine(coords(p))` is a *different* lattice
point.  The filter built its coset representatives by pairing the two, which made
every residue pair wrong; the first `theta_12` certificate left four
monochromatic cross edges on a real ball.  `combine_echelon` is the actual
inverse, `tests/test_lattice.py` pins the distinction, and with it the same
certificate leaves zero.  (The published verdicts happened not to change, but
they were not sound until this was fixed.)

## Validated against every known answer

| must DIE (4-colourable by other routes) | verdict |
|---|---|
| `theta_3`, `theta_7`, `theta_9`, `theta_12`, `theta_20`, `theta_44` | all **DEAD** |

| must SURVIVE (verified 5-chromatic union on record) | verdict |
|---|---|
| `theta_4`, `theta_28`, `theta_36` | all **SURVIVE**, discriminatingly |
| `theta_16`, `alpha_64/3`, `alpha_64/9`, `alpha_256/9` | **degenerate at m = 4** -- undecided |

So eight decided cases, eight correct, no error; and four the modulus cannot
reach.  It is strictly stronger than route 49's ball-free homomorphism
classifier, which passes `theta_12` and `theta_20`.  Like every filter here the
kill is **one-sided**: a survivor is a candidate, never a construction.

## The integer spindles, swept to 100

Only `4 | A` with a non-empty shell gets this far; the divisibility law and the
shell form settle the rest.

| verdict | A |
|---|---|
| **DEAD** at `m = 4` | 12, 20, 44, 52, 60, 76, 84, 92, 100 |
| **DEAD** at `m = 8`, degenerate at 4 and 6 | 48, 80 |
| **SURVIVES** | 4, 16, 28, 36 |
| degenerate at every modulus tried (4, 6, 8, 12) | 64 |
| empty shell, nothing to act on | 24, 32, 40, 56, 68, 72, 88, 96 |

`theta_12`, `theta_20` and `theta_44` were already known 4-colourable by ball
tests over their complete shells, and are the method's check.  The other **eight
kills are new**.

**`theta_60` is the one to point at.**  The commit that tested `theta_44` -- a
depth-9 ball of 314647 points, a union of 629293 and 7948074 edges -- closed with:

> *"theta_60 at 114 is the only untested candidate above the line and needs depth
> 10 -- a union over a million points -- so it stays out of reach."*

It is not out of reach.  It takes seconds, and it is dead.  `theta_76`, `80`,
`84`, `92` and `100` are further out still and die the same way.

## What a kill certificate can and cannot be checked against

The two colourings are checked on a real ball wherever one can be built
(`theta_12`, `theta_20` above).  For the larger spindles that is exactly the cost
the filter exists to avoid: `theta_44`'s shell is not reached at all by a depth-7
ball of 163519 points, and a depth-8 ball of 237805 holds 18 of its 30 points, so
confirming its certificate needs the depth-9 ball the earlier test used.  Those
kills rest on the argument and on the method's record against the cases that could
be checked, not on a ball of their own.

### An observation that did not survive its own decomposition

Every dead rotation has exactly **69** occurring residue pairs and no survivor
does, which looked like an invariant worth chasing.  Splitting the count by type
kills it:

| rotation | `beta = 0` | `alpha = 0` | neither | total | verdict |
|---|---|---|---|---|---|
| `theta_12` | 30 | 30 | **9** | 69 | DEAD |
| `theta_20` | 30 | 30 | **9** | 69 | DEAD |
| `theta_36` | 48 | 48 | **9** | 105 | SURVIVES |
| `theta_4` | 30 | 30 | 45 | 105 | SURVIVES |
| `theta_28` | 48 | 48 | 21 | 117 | SURVIVES |

`theta_36` survives with the **same nine** mixed pairs as the dead rotations,
differing only in having 48 distinct residues among its joint unit vectors rather
than 30.  So it is not the mixed pairs that decide it, the pairs through the centre
are not inert, and 69 is a coincidence of two quantities rather than a quantity.
The verdicts are not explained by any count found so far.
