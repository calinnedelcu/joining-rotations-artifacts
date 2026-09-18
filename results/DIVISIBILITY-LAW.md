# The classification collapses to a divisibility condition

Across every sweep run -- integer spindles with squared radius at most 60, and
rational ones `a/b <= 30` with `b <= 12` -- restricted to those whose shell is
non-empty:

> **The spindle at squared radius `a/b` (in lowest terms) survives the
> homomorphism filter if and only if `4 | a`.**

**285 spindles with a real shell, zero exceptions.**

## Validated outside the range it was read from

Extrapolating a pattern past its evidence is the exact move this project has
been burned by three times, so the law was spot-checked beyond squared radius
60 with the full homomorphism filter:

| squared radius | shell | 4 divides it | filter |
|---|---|---|---|
| 76 | 60 | yes | survives |
| 80 | 60 | yes | survives |
| 84 | 84 | yes | survives |
| 100 | 90 | yes | survives |
| 61 | 60 | no | dead |
| 63 | 108 | no | dead |
| 65 | 120 | no | dead |

Seven more cases, no disagreement. **292 in total.**

## The candidate list to squared radius 200

Of the 111 non-empty integer shells with `N <= 200`, thirty have `4 | N` and are
therefore candidates:

    4, 12, 16, 20, 28, 36, 44, 48, 52, 60, 64, 76, 80, 84, 92, 100, 108, 112,
    124, 132, 140, 144, 148, 156, 172, 176, 180, 188, 192, 196

and twenty multiples of 4 are eliminated geometrically for having no shell at
all: 8, 24, 32, 40, 56, 68, 72, 88, 96, 104, 116, 120, 128, 136, 152, 160, 164,
168, 184, 200.

Producing that list took no lattice computation: a divisibility test and a
quaternary-form count.

## Why this is the useful form

The criterion as first stated -- does the joint lattice contain a point at
distance 1/2 -- requires building the lattice, enumerating its unit vectors by
the trace form, and running a linear-algebra search. That takes seconds, which
was already a large improvement on building a ball and running SAT for hours.

This takes no computation at all. Read the numerator, look at it mod 4.

## How it fits the geometric form

A spindle at squared radius `a/b` satisfies `|p - theta(p)| = 1` for every shell
point `p`, by construction, and

    (p - theta(p))/2  =  p . [ b - i sqrt(b(4a-b)) ] / (4a).

The rotation dies unless that point lies in the lattice.  The `4a` in the
denominator is presumably where the condition `4 | a` comes from, but we have
not turned that into a proof.

## Status

Empirical, on 285 cases with no exception, and not proved. Two things would
settle it:

1. showing that `4 | a` forces `p . [b - i sqrt(b(4a-b))] / (4a)` into the
   lattice for every shell point `p`;
2. showing that `4` not dividing `a` admits an explicit homomorphism, presumably
   uniform in `a` and `b`.

Both are concrete. The second is the more approachable: the filter already
returns an explicit certificate in every case where one exists, so the pattern
is there to be read off.

## Consequence for the classification

With the divisibility law and the shell test -- `|z|^2 = N/B` requires
`ab + cd = 0` and `a^2 + 33b^2 + 3c^2 + 11d^2 = 144N/B`, hence `B | 144` --
the candidate list for joining rotations is decidable by inspection:

> **`theta` is a candidate iff its shell is non-empty and `4` divides the
> numerator of its squared radius.**

Everything else is dead, permanently, with an explicit 4-colouring of the whole
infinite lattice.

## The proof attempt, and why it failed

`scripts/prove_law.py` carries this out explicitly and reports its own failure.

The plan was: exhibit `q(p) = 9|p|^2` as an integral quadratic form on `R`, note
`q(2r) = 4 q(r)`, and separate the classes of `R/2R` by `q mod 4`.  Two things
break it.

**`|p|^2` is not rational on `R`.**  In a depth-4 ball, 7722 of 8413 lattice
points -- 92% -- have a `sqrt33` component in their squared norm.  That is
exactly the chart's side condition `AB + CD != 0`.  So `{p : |p|^2 rational}` is
a quadric, not a subgroup, and `q` is not a form on `R` at all.

**Its rational part is a form, but not an integral one.**  Projecting the norm
onto `Q` is `Q`-linear, so `ratpart(|p|^2)` IS a rational quadratic form, and it
agrees with `|p|^2` exactly on the points of rational norm -- the shell points
among them.  Its Gram matrix, times 9, on a basis of `R`:

        [     1    -1/2    -1/4    -1/4]
        [  -1/2       1    -1/4     1/2]
        [  -1/4    -1/4       3     5/4]
        [  -1/4     1/2     5/4       3]

Quarter-integer entries.  Scaling to `36 * ratpart` clears them -- but `36 = 4 * 9`,
so the scaling inserts exactly the factor 4 the test has to detect.  After it,
`Q mod 4` is the only class function available (since `Q(x+2y) = Q(x) + 4B(x,y)
+ 4Q(y)` with `B` integral), and `Q mod 4` does **not** separate: six non-zero
classes give `Q = 0 mod 4`.

**A third route, also closed -- and its premise was false.**  This route opened
`R = Z[w1, w3]` is a *ring*, on the strength of a check that the conjugate of
every basis vector is back in `R`.  That check is real and `R` is closed under
conjugation, but it is not the check the claim needed, and the claim is **wrong**:
`R` is not closed under multiplication.  `w3^2 = 7/18 + 5*sqrt11/18 i` is not in
`R` -- it is not even in the chart, needing `A = 14/3` -- and of the 900 products
of pairs of unit vectors only **684** land back in `R`.  `R` is a rank-4 additive
group and a module over `O = Z[(1+sqrt33)/2]` (verified: multiplication by
`(1+sqrt33)/2` fixes all 2083 points of the depth-3 ball), and that module
structure is what the proof actually uses.  The ring generated by `w1` and `w3`
is the strictly larger *Moser ring*, with denominators `3^k`.

So `N(p) = p * conj(p)` is still a norm form on `R`, but `R/2R` is a group, not a
ring.  The route fails anyway, for the reason below.  The hope was to make the
statement purely mod 2, which is
legitimate here because **no shell has `a = 2 mod 4`** -- squared radii 2, 6, 10,
14, 18, 22, 26, 30, 34 are all empty -- so for shell points `2 | a` and `4 | a`
are the same condition.  It fails for the same reason: `N` is not a class
function mod 2 either, because lattice points carry norms like `1/9`, `1/3` and
`5/9`, so `N(p + 2q) = N(p) + 4 Re(p conj(q)) + 4 N(q)` has a correction term
that is only a ninth-integer.

**The common obstruction, stated once.**  The inner product on `R` takes
quarter-integer values -- that is intrinsic, not an artefact of the basis, since
integrality of a form does not depend on one.  The statement to prove is about
a power of 2.  Scaling the form to make it integral multiplies by 4 and destroys
exactly the two powers of 2 the test has to see.  The denominators of 9 in the
norms add a second layer on top.  All three attempts fail at this same point,
and it is recorded here so a fourth does not rediscover it.

**Retraction of an estimate.**  This was described as "a day of work, finite and
mechanical".  That was wrong.  The finite check on `R/2R` is real and stands,
but turning it into a proof is not mechanical -- both natural routes close.

## The certificates are 3-periodic, which is the proof strategy

Reading a Klein certificate off in canonical coordinates -- indexed by the 30
unit vectors `w(k, j) = exp(i(k*60deg + j*theta_3/2))`, `k = 0..5`, `j = -2..2`,
rather than by a lattice basis -- shows the same shape every time. Grouping the
30 values by `j`:

    a=1   W:  132132 | 321321 | 213213 | 132132 | 321321
    a=3   W:  123123 | 312312 | 231231 | 123123 | 312312
    a=7   W:  312312 | 123123 | 231231 | 312312 | 123123
    a=15  W:  321321 | 132132 | 213213 | 321321 | 132132

Within each `j`-block the colour has period 3 in `k`; across blocks it has
period 3 in `j`. So

    phi(w(k, j))  depends only on  (k mod 3, j mod 3),

takes values in `{1, 2, 3}` -- the three non-zero elements of the Klein group,
never 0 -- and the different rows above are the same map up to renaming colours.
The rotated generators `theta(w(k, j))` follow the same law with a shift that is
what varies with `a`.

That turns the empirical divisibility law into a concrete proof obligation:

1. **Construct** `phi` by the rule `phi(w(k,j)) = f(k mod 3, j mod 3)` with `f`
   into the three non-zero Klein elements, together with its value on the
   rotated generators.
2. **Show it is well defined**: the images must respect every additive relation
   among `W u theta(W)`, and those relations are where `a` enters.
3. **Show it kills no unit vector**: the unit vectors are the trace-form
   ellipsoid points, a finite explicit set.

Step 2 is the whole content, and the claim to prove there is that the relations
are compatible with a 3-periodic assignment exactly when `4` does not divide `a`.

## The proof obligation, sharpened to a parity question

Writing `d = p - theta(p)` for a shell point `p`, the condition "`d/2` lies in
the lattice" is, in coordinates over a lattice basis, exactly "**every
coordinate of `d` is even**".

Measured on single shell points:

| squared radius | 4 divides it | coordinates of `d` |
|---|---|---|
| 4 | yes | all even (`d/2` is a lattice point) |
| 12 | yes | all even |
| 16 | yes | all even |
| 5 | no | 5 odd entries |
| 9 | no | 1 odd entry |
| 13 | no | 5 odd entries |

So the law to prove is a parity statement:

> the lattice coordinates of `p - theta(p)` are all even **iff** `4 | a`.

The obstacle to writing this down directly is that the reduced basis this
repository uses is badly skewed -- coordinates run to tens of digits -- so a
proof wants either the Moser chart `z = (a + b sqrt33)/12 + i(c sqrt3 +
d sqrt11)/12` in place of an LLL basis, or a direct argument on

    d = p . [ b - i sqrt(b(4a-b)) ] / (2a)

showing when multiplication by that algebraic number lands in `2 Lambda`. The
`2a` in the denominator against a `2` in `2 Lambda` is where the factor of 4
plausibly comes from, and that is as far as we take it here.
