# The classification reduces to an elementary statement about the Moser lattice

The divisibility law -- a spindle joins iff `4 | a` -- was found empirically on
292 cases.  It can now be reduced, by exact algebra, to a statement with no
rotation, no joint lattice and no field extension in it.

## The chain

**Step 1 (proved).** A spindle at squared radius `a` is defined by making two
shell points unit distance apart, so `|p - theta(p)| = 1` for every shell point
`p`, and `(p - theta(p))/2` has length exactly 1/2.  By the theorem in
JOIN-CLASSIFICATION.md the rotation is killed unless that point lies in the
joint lattice.

**Step 2 (proved, exact identity).**  With `s = sqrt(4a-1)` and
`mu = 1 + i s`, we have `mu * conj(mu) = 1 + s^2 = 4a`, and

    (p - theta(p))/2  =  p / mu.

Verified exactly in the field on every case tried.

**Step 3 (proved, exact identity).**  Put `nu = mu/2 = (1 + i sqrt(4a-1))/2`.
Then

    e^(i theta)  =  - conj(nu) / nu,          nu * conj(nu) = a.

Verified exactly on every case tried.  So the joint lattice is
`Lambda = R + e^(i theta) R` and `nu * Lambda = nu R + conj(nu) R`.

**Step 4 (proved, one line).**  `nu + conj(nu) = 1`.  So the module
`nu R + conj(nu) R` contains 1, hence equals `R` whenever `nu` and `conj(nu)`
lie in `R`.  Therefore

    p / mu  in  Lambda      <=>      p / 2  in  R.

**Step 5 (measured, 0 mismatches).**  For a lattice point `p` of the Moser
lattice `R` with `|p|^2` an integer,

> **p / 2 lies in R  if and only if  4 divides |p|^2.**

Checked on every complete shell up to squared radius 36 -- twenty shells, from
30 to 120 points each, every point of every shell -- with no exception.

## What step 5 looks like inside R/2R

`R` has rank 4, so `R/2R` has 16 elements.  Sorting each shell by its class:

| squared radius | classes the shell occupies |
|---|---|
| `4 | N` (4, 12, 16, 20, 28, 36) | **exactly one: the zero class** |
| otherwise (1, 3, 5, 7, 9, 11, 13, 15, 19, 21, 23, 25, 27, 31, 33, 35) | **exactly nine, none of them zero** |

Always one or always nine.  And the integer squared norms split cleanly:
the zero class carries `|p|^2 = 0 mod 4`, the non-zero classes carry `1` and `3`
mod 4, and `2 mod 4` never occurs at all -- every shell with `N = 2 mod 4` is
empty.

## What is left to prove

Exactly step 5, and it is now a self-contained question about a rank-4 lattice:

> for `p` in the Moser lattice with `|p|^2` an integer,
> `p in 2R` if and only if `4` divides `|p|^2`.

No rotation, no SAT, no ball.  One direction is nearly immediate -- `p = 2q`
gives `|p|^2 = 4|q|^2` -- provided one knows `|q|^2` is an integer, which is the
part needing the arithmetic of `R`.  The converse is the real content.

## A route that does NOT work

The obvious attempt is to use the chart `z = (A + B sqrt33)/12 + i(C sqrt3 +
D sqrt11)/12` and argue that `p in 2R` means `A, B, C, D` all even.  It fails:
in that chart 14 of the 30 solutions at `N = 1` have all-even coordinates, and
unit vectors are certainly not in `2R`.  The chart describes a superset of the
lattice, and doubling in `R` is not "all chart coordinates even".  Recorded so
the next attempt does not repeat it.

## Step 5, reduced to a finite check and verified

The Moser lattice's squared norms are not integers -- values like `1/9` and
`4/3` occur -- but their denominators divide 9, and

    q(p) := 9 |p|^2

**is an integer at every lattice point with rational norm** (checked on 206311
points). So `(R, q)` is an integral quadratic lattice of rank 4, a standard
object, and the question becomes a congruence in it.

**One direction is immediate.** If `p = 2r` then `q(p) = 4 q(r)`, so `4 | q(p)`;
and `|p|^2` being an integer gives `9 | q(p)`; together `36 | q(p)`, i.e.
`4 | |p|^2`.

**The other direction is a finite check on `R/2R`**, which has 16 elements. Ten
of them carry points of rational norm at all, and on those:

| class | `q(p) mod 4` |
|---|---|
| `0000` (the zero class) | **`0`, always** |
| each of the other nine | **`1` or `3` — never `0`, never `2`** |

So `q(p) = 0 mod 4` happens exactly on the zero class, i.e. exactly when
`p in 2R`. With `9 | q(p)` that is exactly `4 | |p|^2`.

Note `q mod 4` is *not* single-valued on a class -- the non-zero classes carry
both `1` and `3` -- so the bilinear form is half-integral and only `q mod 2`
descends to `R/2R`. What the table says is the weaker and sufficient statement:
`q` is **odd** off the zero class. That is what rules out `q = 0 mod 4` there.

## Status

Steps 1-4 are exact identities, verified symbolically in the field. Step 5 is
reduced to the parity of an integral rank-4 form on the 16 classes of `R/2R`,
and the table above is that check.

What a written proof still needs: representatives of the ten classes exhibited
explicitly with their `q` values, and the argument that the six remaining
classes carry no point of rational norm. Both are finite and mechanical. Until
that is written out properly the law should be described as *reduced to a
finite verified check*, not as a theorem with a proof in hand.
