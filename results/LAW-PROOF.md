# One direction of the divisibility law, proved

**Theorem.**  Let `R` be the Moser lattice and `theta_a` the spindle at squared
radius `a`, whose shell is non-empty.  If `4 | a` then the joint lattice
`Lambda = R + theta_a(R)` admits **no homomorphism 4-colouring**, so `theta_a` is
a candidate joining rotation.

The converse -- that `4` not dividing `a` forces a certificate to exist -- was
verified on 292 spindles and is now **proved** for rank-8 spindles; see "The
converse, closed" below.

## The chain

**1.  `|p - theta(p)| = 1` for every shell point.**  That is the definition of a
spindle: with `|p|^2 = a` and `2|p| sin(theta/2) = 1`.

**2.  `(p - theta(p))/2 = p / mu`, where `mu = 1 + i sqrt(4a-1)`.**  Exact
identity, since `1 - e^(i theta) = [1 - i sqrt(4a-1)] / (2a)` and
`mu * conj(mu) = 1 + (4a-1) = 4a`.  Verified symbolically in the field.

**3.  `e^(i theta) = - conj(nu) / nu` with `nu = mu/2`,** so `nu conj(nu) = a` and
`nu Lambda = nu R + conj(nu) R`.  Verified symbolically.

**4.  `nu + conj(nu) = 1`,** hence for every `r` in `R`,
`r = nu r + conj(nu) r`, giving `R` inside `nu R + conj(nu) R`.  Therefore

        p/2 in R   ==>   p/mu in Lambda,

i.e. a half-unit vector exists and, by the criterion, no homomorphism
4-colouring does.  (Only this inclusion holds: the reverse would need `nu` in
`R`, and `nu` carries `sqrt(4a-1)`, which is not in `Q(sqrt3, sqrt11)`.  That is
exactly why the converse of the theorem is not obtained here.)

**5.  `R` is a congruence sublattice of the chart lattice, exactly.**  In the
chart `z = (A + B sqrt33)/12 + i(C sqrt3 + D sqrt11)/12`, write `L` for the
integer points obeying

        A = B = C = D  (mod 2)      and      A + B + C + D = 2A  (mod 4).

Then `R = L`.  Proved by: the 30 unit vectors satisfy both congruences; the
conditions are closed under addition, so `L` is a group and `R` is inside it;
`L` occupies 16 of the 256 residue classes mod 4, so has index 16; `R` occupies
the same 16; and `R` contains `4 Z^4` (checked on the four generators), so `R`
is the full preimage and equals `L`.

**6.  `p/2 in R  <=>  4 | a`.**  With `S = A^2 + 33B^2 + 3C^2 + 11D^2 = 144a` and
`144 = 16 * 9`, `4 | a` is exactly `64 | S`.  Write `(i)` for `A = B = C = D (mod 2)`
and `(ii)` for `A + B + C + D = 2A (mod 4)`, and recall that `|p|^2` is rational
exactly when `AB + CD = 0`.  Two lemmas do the work.

> **Lemma A.**  For any `(A,B,C,D)` satisfying `(i)` and `AB + CD = 0`, `16 | S`.
> Equivalently, **every rational squared norm of `R` lies in `(1/9)Z`.**

*Proof.*  For odd `x`, `x^2 = 1 + 8k_x`, and `k_x mod 2` is `0` when `x = ±1 (mod 8)`
and `1` when `x = ±3 (mod 8)`.  That map `e` is a group homomorphism
`(Z/8)^* -> Z/2` -- check it on `3*5 = 7`, `3*3 = 1`, `3*7 = 5` -- so
`e(xy) = e(x) + e(y)` and `e(-1) = 0`.

*All odd.*  `S = 48 + 8(k_A + 33k_B + 3k_C + 11k_D)`, and mod 16 every one of
`33, 3, 11` acts as an odd multiplier on `8k`, so
`S = 8(e(A) + e(B) + e(C) + e(D)) (mod 16)`.  From `AB = -CD`,

        e(A) + e(B) = e(AB) = e(-CD) = e(C) + e(D),

so the bracket is even and `16 | S`.

*All even.*  Put `A = 2A'` and so on; then `S = 4S'` with
`S' = A'^2 + 33B'^2 + 3C'^2 + 11D'^2`, and `A'B' + C'D' = 0`.  Mod 4,
`S' = [A'] + [B'] + 3[C'] + 3[D']` where `[x]` is 1 for odd `x` and 0 for even.
Condition `(ii)` gives `A' + B' + C' + D'` even, so the number of odd entries is
0, 2 or 4.  Zero and four give `S' = 0` and `S' = 8 = 0 (mod 4)`.  Of the six ways
to have two, `{A',B'}` makes `A'B'` odd and `C'D'` even, and `{C',D'}` the reverse,
so both are excluded by `A'B' + C'D' = 0`; the remaining four give
`1 + 3 = 0 (mod 4)`.  So `4 | S'` and `16 | S`. ∎

> **Lemma B.**  If `A, B, C, D` are all **odd** then `S = 16 (mod 32)`; in
> particular `32` does not divide `S`, let alone `64`.

*Proof.*  For odd `x`, `x^2 = 1 + 8*eta(x) (mod 32)` with `eta(x)` in `{0,1,2,3}`.
From `AB = -CD` we get `A^2 B^2 = C^2 D^2`, and mod 32

        A^2 B^2 = (1 + 8 eta_A)(1 + 8 eta_B) = 1 + 8(eta_A + eta_B),

because `64 = 0 (mod 32)`; likewise for `C^2 D^2`.  Equality forces
`eta_A + eta_B = eta_C + eta_D (mod 4)`.  And
`S = 48 + 8(eta_A + 33 eta_B + 3 eta_C + 11 eta_D)`, which mod 32 is
`16 + 8(eta_A + eta_B + 3eta_C + 3eta_D) = 16 + 8(eta_A + eta_B - eta_C - eta_D)`,
so `S = 16 (mod 32)`. ∎

> **Lemma C.**  For any integers `X, Y, Z, W`, if
> `4 | X^2 + 33Y^2 + 3Z^2 + 11W^2` then `X + Y + Z + W` is **even**.

*Proof.*  Mod 4 a square is 1 for an odd argument and 0 for an even one, so

        S = [X] + [Y] + 3[Z] + 3[W]   (mod 4),

with `[.]` the odd indicator.  With exactly one odd entry `S` is `1` or `3`; with
exactly three it is `1 + 1 + 3 = 5 = 1` or `1 + 3 + 3 = 7 = 3`.  Neither is `0`, so
the number of odd entries cannot be odd. ∎

*(Exhaustively: of the 16144161 tuples with `|entries| <= 40` and `4 | S`, none has
odd sum.)*

**The theorem now follows both ways.**

*If `p/2` is in `R`*, write `p = 2w` with `w` in `R`.  Then `a = |p|^2 = 4|w|^2`,
and Lemma A applied to `w` puts `|w|^2 = T/9` for an integer `T`.  So `a = 4T/9`,
and `a` being an integer forces `9 | T`, hence **`4 | a`**.

*If `4 | a`*, then `64 | S`, so certainly `32 | S`, and Lemma B rules out
`A, B, C, D` all odd.  By `(i)` they are therefore all **even**; write `A = 2A'`
and so on, so that `S = 4S'` and `16 | S'`, and `A'B' + C'D' = 0`.  It remains to
put `(A', B', C', D')` in `R`.

*They satisfy `(i)`.*  Lemma C applied to the halves gives an **even** number of
odd entries among them, so 0, 2 or 4.  Two is impossible: if `A', C'` are the odd
ones then `A'B' = -C'D'` forces `v_2(B') = v_2(D') = k`, and mod 16
`S' = A'^2 + 3C'^2` when `k >= 2`, while `k = 1` contributes `4 + 12 = 0`; either
way `S'` lands in `{4, 12}`, against `16 | S'`.  The other mixed pairs are the same
computation.  So the halves are all odd or all even.

*They satisfy `(ii)`.*  If all odd, reduce `A'B' = -C'D'` mod 4 with every entry in
`{1,3}`: when `A', B'` agree the product is `1`, forcing `C'D' = 3` and so `C', D'`
differ; when they differ the product is `3`, forcing `C', D'` to agree.  In each
case the number of entries congruent to `3` is **odd**, which is exactly `(ii)`
because `A' + B' + C' + D' = 2t` and `2A' = 2` mod 4.  If all even, write
`A' = 2A''` and so on; `(ii)` reduces to `A'' + B'' + C'' + D''` being even, and
`16 | S'` gives `4 | S''`, so Lemma C supplies it.

Hence `p/2` is in `R`. ∎

Combining 6, 4, 2 and 1 gives the theorem.

## What kind of proof this is

Step 6 **was** a finite verification over 11776 residue classes mod 32.  It is now
three lemmas with short proofs -- A from the homomorphism `(Z/8)* -> Z/2`, B from
`A^2 B^2 = C^2 D^2` read mod 32, C from a parity count mod 4 -- and no residual
check.  Steps 2 and 3 are symbolic identities in the field.  Step 5 is a finite
check plus a standard index argument.

Every lemma was also confirmed exhaustively before it was written, which is how
Lemma C was found: the branch it settles was the last thing in the chain still
carried by verification.

Reproduce: `scripts/prove_law_direction.py`.

## The converse, closed 16 Sep 2026

It used to be open: producing, for each `a` with `4` not dividing it, an explicit
homomorphism `Lambda -> G` killing no unit vector.  It is now constructed rather
than observed.  Lemma D of `results/THEOREM.md` shows no shell point is divisible
by either prime above 2 when `4` does not divide `a`, so the shell displacements
impose only diagonal conditions `(c, c)` with `c != 0`; steps 4 and 5 there show
nothing else constrains; and any pair of automorphisms whose relative permutation
is a 3-cycle -- 12 of the 36 pairs -- satisfies every such condition at once.

## What the converse needs, stated exactly

Writing `ub` for the mod-2 images of the unit vectors of `Lambda` in
`Lambda / 2 Lambda = F_2^r`, the measurements are sharp:

| | `4` does not divide `a` | `4 | a` |
|---|---|---|
| `0` in `ub` | **never** | **always** |
| `|ub|` | 9, 18, 27 | 19, 31, 37 |
| rank | 4 or 8 | 8 |

`0 in ub` says a unit vector lies in `2 Lambda`, which is the theorem above in
other words.  So the proved direction accounts for the whole first row.

A Klein certificate is a pair `l1, l2` with `ub` disjoint from
`ker l1 ∩ ker l2`.  The converse therefore reduces to:

> `0` not in `ub`  ==>  some codimension-2 subspace of `F_2^r` misses `ub`.

**Why this is not a counting argument.**  In `F_2^8` a codimension-2 subspace
has 63 non-zero elements out of 255, so a set of 27 points meets a uniformly
random one about 6.7 times over.  Almost no subspace works.  A certificate
existing at all means `ub` sits inside a union of three hyperplanes -- there is
real structure in `ub`, and identifying it is what a proof of the converse needs.

**A route tried and abandoned.**  The certificates the solver returns are
3-periodic: `phi(w(k,j))` depends only on `(k mod 3, j mod 3)`, and `phi` on the
rotated generators is the same table shifted in `j`.  Measured across ten dead
rotations, the shift takes values 0, 1 and 2 with no pattern in `a mod 3`, and
the `W`-table appears in three colour-permuted forms.  So the first certificate
the solver finds is not canonical, and reading a construction off it would need
all certificates characterised rather than one sampled.

## The dichotomy that drives everything

Reducing each shell of the Moser lattice into `R/2R` (16 classes) gives a clean
split, with no exception across every occupied shell to squared radius 36:

| shell | classes it occupies in `R/2R` |
|---|---|
| `4 | a` (4, 12, 16, 20, 28, 36) | **`{0}` alone** |
| otherwise (1, 3, 5, 7, 9, 11, 13, 15, 19, 21, 23, 25, 27, 31, 33) | **exactly `{1,2,3,5,6,8,10,14,15}`** |

Always one class or always the same nine.  The remaining six classes -- 4, 7, 9,
11, 12, 13 -- carry no shell point at all, at any radius.

The first row is the proved theorem restated: the shell lies in `2R`, so
`p/2` is a lattice point, so `4 | a`.

The second row gives the converse **for the rank-4 spindles**.  For those,
`Lambda` contains `R` with index exactly `a^2` -- measured 1, 9, 49, 361, 625,
1369 at `a` = 1, 3, 7, 19, 25, 37 -- and its unit vectors correspond precisely to
`R`'s shell-`a` points, matching in number every time (30, 42, 60, 60, 90, 120).
So a certificate for `Lambda` is a homomorphism on `R` avoiding the shell-`a`
classes; and since those classes are the same nine for every such `a`, **one
certificate serves them all**.  The pair of functionals `(l1, l2) = (2, 9)` works
for `a` = 1, 3, 7, 19, 25 alike.

At `a = 1` the shell is the unit-vector set, so this case is Ducz's theorem; the
content here is that the other rank-4 spindles reduce to the same nine classes
and therefore to the same certificate.

**The rank-8 case was the open one** on this route, where `Lambda` genuinely
leaves `R` and the classes live in `F_2^8` rather than `F_2^4`; the measured counts
are 9, 18 or 27 classes for `4` not dividing `a`, against 19, 31 or 37 when it
does.  The converse was settled a different way -- by constructing the certificate
from Lemma D rather than by collapsing the class counts -- so this route is no
longer needed, though the uniformity it asks about is still unknown.

## The rank-8 structure, and what the converse becomes there

For every rank-8 spindle measured, `Lambda` is a **direct sum**:

    Lambda = R  (+)  theta(R),      R cap theta(R) = 0,

confirmed by rank (4 + 4 = 8) in every case.  Its unit vectors split into R's own
30, theta(R)'s 30, and a set of **cross** vectors `r + t` with `r` in `R`,
`t` in `theta(R)`, both non-zero.

A homomorphism `phi : Lambda -> G` is therefore exactly a pair: `phi_1` on `R`
and `phi_2` on `theta(R)`.  Avoiding the first 30 forces `phi_1` to be a
geometric 4-colouring of `R`, of which Ducz proves there are exactly **two**;
same for `phi_2`; and the Klein group has **6** automorphisms.  So there are at
most `2 * 2 * 6 = 24` candidate colourings, whatever `a` is, and the cross
vectors are the only thing that can cut that down.

**The count confirms this exactly.**  Measured:

| a | cross unit vectors | Klein certificates |
|---|---|---|
| 2, 14, 17 | **0** | **24** |
| 6 | 36 | 24 |
| 10 | 60 | 12 |
| 5, 9, 11, 13, 15 | 30 to 144 | 4 |
| 4, 12, 16, 20, 28 (`4 | a`) | 42 to 120 | **0** |

At zero cross vectors the count is 24 on the nose -- `2 x 2 x 6` -- which is the
structural claim verified rather than assumed.

So the whole problem reduces to a statement about the cross vectors:

> **the cross unit vectors eliminate all 24 pairings exactly when `4 | a`.**

One half of that is the theorem proved above: `4 | a` produces a unit vector
inside `2 Lambda`, which every Klein homomorphism kills, so nothing survives.
The other half -- that for `4` not dividing `a` some pairing always escapes -- is
what remains, and it is now a finite question about a set of at most 24
candidates rather than a search over `2^8` functionals.

## The converse, reduced to one lemma and verified

`Lambda = R (+) theta(R)`, so every cross unit vector is `u = r + theta(s)` with
`r, s` in `R`, and a colouring `(phi_1, phi_2)` kills it exactly when
`phi_1(r) = psi(s)`, where `psi = phi_2 . theta` is again a Ducz colouring of `R`.
Fixing one Ducz colouring `gamma` and recording, over all cross unit vectors, the
pair `(gamma(r), gamma(s))` in `{0,1,2,3}^2` settles everything:

* `(0,0)` means `r` and `s` both lie in `2R`, so `u` lies in `2 Lambda`.  Then
  `phi(u) = 0 + 0` for **every** pairing -- no certificate can exist.
* `(0,c)` or `(c,0)` with `c` non-zero never kills anything: the sum is `c`.
* only pairs with **both** entries non-zero constrain the automorphisms, via
  `pi_1(c1) != pi_2(c2)`.

**Measured on 22 rank-8 spindles with `4` not dividing `a`** (a = 2, 5, 6, 9, 10,
11, 13, 14, 15, 17, 18, 21, 22, 23, 26, 27, 29, 30, 31, 33, 34, 35):

| | `(0,0)` present | both-non-zero pairs | automorphism pairs surviving |
|---|---|---|---|
| `4` does not divide `a` | **never** | **empty, or exactly the diagonal** `{(1,1),(2,2),(3,3)}` | 36 or 12, never 0 |
| `4 | a` | **always** | empty | **0** |

The diagonal is always escapable: any two automorphisms differing at every point
satisfy `pi_1(c) != pi_2(c)`, and 12 of the 36 pairs do.  So a certificate always
exists when the pairs stay within the diagonal.

**The first row's `(0,0)` column is the proved theorem**, since `(0,0)` occurring
is exactly "a cross unit vector lies in `2 Lambda`", which the congruence
argument settles.  What is left is a single lemma:

> **Lemma (open).**  For `4` not dividing `a`, the both-non-zero cross colour
> pairs lie within the diagonal.

Verified on all 22 cases and needed nowhere else.  With it, the divisibility law
is a theorem in both directions; without it, the converse is an observation on
28 spindles (22 of rank 8, 6 of rank 4) resting on an explicit finite structure
rather than on a solver's output.

Reproduce: `scripts/cross_pairs.py`.
