# The joining criterion, both directions

> **Theorem.**  Let `theta_a` be the spindle at squared radius `a`, with non-empty
> shell, and `Lambda = R + theta_a(R)` the joint lattice of the Moser lattice and
> its rotated copy.  Then `Lambda` admits a homomorphism 4-colouring **if and
> only if `4` does not divide `a`**.
>
> Equivalently: `theta_a` can join two copies into a 5-chromatic graph only when
> `4 | a`.

## The proof, in six steps

**1.  `Lambda` is a direct sum.**  `Lambda = R (+) theta(R)` with trivial
intersection -- verified by rank (4 + 4 = 8) in every case.  So a homomorphism
`phi : Lambda -> G` is a pair `(phi_1, phi_2)`, one per summand.  Avoiding the 30
unit vectors of each summand forces each to be a geometric 4-colouring of a copy
of `R`, of which Ducz proves there are exactly **two**; the Klein group has **six**
automorphisms.  At most `2 * 2 * 6 = 24` candidates, whatever `a` is.

*Verified exactly*: where the cross unit vectors number zero (`a` = 2, 14, 17)
there are precisely **24** certificates.

**2.  Every cross unit vector has its two parts parallel.**  Write
`u = r + theta(s)`, `r, s` in `R`.  Then

    |u|^2 = |r|^2 + |s|^2 + [ (2a-1) Re(r conj(s)) + sqrt(4a-1) Im(r conj(s)) ] / a.

`|u|^2 = 1` is rational and `|r|^2, |s|^2, Re, Im` all lie in `Q(sqrt3, sqrt11)`,
while `sqrt(4a-1)` does **not** -- that is exactly what makes the spindle rank 8.
So the `sqrt(4a-1)` term must vanish on its own:

        Im(r conj(s)) = 0,     i.e.  s = lambda r  for a real lambda.

*Verified*: 100% of cross unit vectors, every rotation tested.

**3.  The `lambda = -1` cross vectors are exactly the shell displacements.**  For
`lambda = -1`, `u = r - theta(r) = (1 - theta) r`, and `|1 - theta| = 1/sqrt(a)`
forces `|r|^2 = a`: `r` is a shell point.

*Verified*: their count equals the shell count exactly, in every case --
60, 54, 30, 60, 30, 42, 60, 60 at `a` = 5, 9, 11, 13, 4, 12, 20, 28.

**4.  For those, the two colours agree.**  `s = -r` and `-1 = 1` in the Klein
group, so `gamma(s) = gamma(r)`.  Both vanish exactly when `r` lies in `2R`, and

        r in 2R   <=>   4 | a

is the congruence theorem (results/LAW-PROOF.md): in the chart, `R` is cut out by
`A = B = C = D (mod 2)` and `A + B + C + D = 2A (mod 4)`; with `S = 144a`,
`4 | a` is `64 | S`; `S mod 64` depends only on the coordinates mod 32; and all
11776 qualifying residue tuples check with **zero** exceptions.

**5.  For `lambda != -1` the vector imposes nothing new.**  This step used to
rest on a claim that is **false**, and the replacement is a proof rather than a
measurement.

*The claim that failed.*  It said every rational `lambda` is a ratio of
**consecutive** integers, `|p - q| = 1`, measured across every rank-8 spindle
with `a <= 35`.  At **`a = 39`** the cross unit vectors have `lambda = -13/15`
and `-15/13`, with `|p - q| = 2`.  The measurement had simply stopped four short.

*The identity everything follows from.*  With `s = lambda r` the `sqrt(4a-1)`
term of step 2 is already gone, so

    |u|^2 = |r|^2 [ lambda^2 + ((2a-1)/a) lambda + 1 ] = 1.

Write `lambda = -p/q` in lowest terms and `d = q - p`.  Clearing denominators,

    rho = |r|^2 = a q^2 / [ a d^2 + p q ].

Since `gcd(p,q) = 1`, Bezout gives `x p + y q = 1`, and `r/q = x (p/q) r + y r`
is an integer combination of `s` and `r`, so **`r/q` lies in `R`**.  Putting
`m = |r/q|^2 = rho / q^2`,

> **`a d^2 + p q = a / m`.**

*Why `m` is rational, which is what makes this work.*  In the chart

    |z|^2 = [ (A^2 + 33B^2 + 3C^2 + 11D^2) + 2(AB + CD) sqrt33 ] / 144,

so a lattice norm is irrational in general -- the shortest vector of `R` has
`|v|^2 = (23 - 4 sqrt33)/9` -- and is **rational exactly when `AB + CD = 0`**, in
which case it lies in `(1/144)Z`.  A rational `lambda` makes the bracket above
rational, hence `rho` rational, hence `m` rational.  So `m` is a **rational**
squared norm of a nonzero lattice point, and `scripts/shells.py` decides those
exactly: the only one below `1/4` is **`1/9`**, attained by 6 points.

**(a) `|d| <= 2`.**  `p q >= 1`, so `a d^2 < a/m <= a/(1/9)`, giving `d^2 < 9`.
And `d = 0` is `lambda = -1`.  So `|d|` is 1 or 2, and `|d| = 3` is impossible --
not unobserved, impossible.

**(b) `|d| = 1` behaves as before.**  Exactly one of `p`, `q` is even, so exactly
one of `r`, `s` lies in `2R = ker gamma`, so `phi(u) = 0 + c = c != 0` whatever
the automorphisms.  No condition.

**(c) `|d| = 2` is a second case, and it is harmless.**  Then `p` and `q` differ
by 2 and are coprime, so **both are odd**.  From the identity, `4a + pq = a/m`
needs `m < 1/4`, so `m = 1/9` exactly and `p q = 5a`.  Writing `v = r/q`, we get
`r = q v` and `s = -p v` with `|v|^2 = 1/9`.  The colour group has exponent 2 and
`p`, `q` are odd, so

        gamma(r) = gamma(s) = gamma(v).

And `v` is **not** in `2R`: a point `2w` has `|2w|^2 = 4|w|^2`, so `|v|^2 = 1/9`
would need `|w|^2 = 1/36`, and the lattice attains no such rational norm (0
points).  So `gamma(v) != 0`, and the vector imposes exactly the **diagonal**
condition `(c, c)` that the shell displacements of step 4 already impose -- the
same 12 of 36 automorphism pairs satisfy it.  Nothing new.

*Verified*: `scripts/lambda_sweep.py` checks (a), (b) and (c) against the actual
cross unit vectors of every rank-8 spindle.  At `a = 39`: `m = 1/9` exactly,
`pq = 195 = 5 * 39`, and `gamma(r) = gamma(s) != 0` for both Ducz colourings, in
all 12 vectors.

*The frame the general case needs.*  The argument above settles **rational**
`lambda` directly.  Irrational ones occur at `a = 4, 10, 16, 28` -- the file
previously said `a = 10` alone -- and there `rho` is irrational, so the appeal to
a smallest rational norm does not reach them.

Two facts set up the general case, both checked:

* **`R` is not a lattice.**  It has rank 4 inside `R^2`, so it is *dense*; its
  shortest vector is as short as one likes, and the one a depth-4 ball finds has
  `|v|^2 = (23 - 4 sqrt33)/9 = 0.0024...`.  There is no minimum norm to lean on.
  The rational argument works precisely because it never needs one: rational
  norms lie in `(1/144)Z`.
* **`R` is a module over `O = Z[(1+sqrt33)/2]`**, the ring of integers of
  `Q(sqrt33)`: multiplication by `sqrt33` and by `(1+sqrt33)/2` both carry `R`
  into `R`, and the Galois conjugation `sqrt33 -> -sqrt33` maps `R` onto itself.
  Since `rank_Z R = 4` and `rank_Z O = 2`, `R` is an `O`-module of rank 2.

That is the right language for the whole step.  Coordinates lie in `Q(sqrt33)`
(the chart is `z = (A + B sqrt33)/12 + i(C sqrt3 + D sqrt11)/12`), so
`lambda = s.x / r.x` lies in `Q(sqrt33) = Frac(O)`.  Write `lambda = alpha/beta`
with `alpha, beta` coprime in `O`.  Bezout **in `O`** gives `v = r/beta` in `R`,
because `R` is an `O`-module, and then `r = beta v`, `s = alpha v` and the
identity above becomes

> **`|v|^2 * [ a (alpha - beta)^2 + (4a-1) alpha beta ] = a`.**

The rational case is the specialisation `alpha = -p`, `beta = q`, where it reads
`a d^2 + p q = a/m`.

Taking field norms and using that every `|v|^2` lies in `(1/144)Z[sqrt33]`, so
that `N(|v|^2) >= 1/144^2`:

    | N( a (alpha - beta)^2 + (4a-1) alpha beta ) |  <=  20736 a^2.

So the algebraic integer in the bracket has bounded norm -- which in a real
quadratic field pins it down up to units.  Turning that into the finitely many
cases the measurement sees is the work left, and it is the last gap in the
theorem.

**5b.  What the colours actually are, and why there are two.**  The analysis
above reads `gamma(x) = 0` as "`x` lies in `2R`".  For a **single** colouring
that is wrong, and correcting it makes the whole step transparent.  (`2R` is
right for step 4, which needs *both* colourings killed at once -- and
`pi_1 R inter pi_2 R = pi_1 pi_2 R = 2R`.)

`33 = 1 mod 8`, so **2 splits** in `Q(sqrt33)`:

    2 = -pi_1 pi_2,    pi_1 = (5 + sqrt33)/2,    pi_2 = (5 - sqrt33)/2,
    N(pi_i) = -2.

`R` is a module over `O = Z[(1+sqrt33)/2]` (see above), so `pi_i R` is a
subgroup, and `[R : pi_i R] = N(pi_i)^2 = 4` -- exactly the index a 4-colouring
needs, where `[R : 2R] = 16` is four times too big.

> **The two Ducz colourings are the reductions modulo the two primes above 2:**
> `ker gamma_1 = pi_1 R` and `ker gamma_2 = pi_2 R`.

*Verified*: on 2263 lattice points, `gamma_i(x) = 0` and `pi_i | x` agree in
every case, for both colourings, and neither kernel is `2R`.

So **there are exactly two because 2 splits into exactly two primes**, and the
colour condition is divisibility in `O`:

        gamma_i(x) = 0   <=>   pi_i divides x.

**5c.  The lemma that closes the step, for rational and irrational alike.**

> **Lemma.**  Let `pi` be a prime of `O` above 2, and `u = r + theta(s)` a cross
> unit vector with `s = lambda r`, `lambda != -1`, written `lambda = alpha/beta`
> with `alpha, beta` coprime in `O` and `v = r/beta`.  If `pi` divides none of
> `v`, `alpha`, `beta`, then **`a` is odd**.

*Proof.*  The residue field `O/pi` is `F_2`, so `alpha = beta = 1` in it, hence
`alpha - beta = 0` and `alpha beta = 1`, and

        W = a (alpha - beta)^2 + (4a - 1) alpha beta  =  4a - 1  =  1   (mod pi),

since `4a - 1` is odd.  So `pi` does not divide `W`.  From `|v|^2 W = a`,
`v_pi(|v|^2) = v_pi(a) = v_2(a)`, and `pi` not dividing `v` makes the left side
zero.  So `v_2(a) = 0`. ∎

**Contrapositive, which is the step.**  If `a` is **even** then `pi` divides one
of `v`, `alpha`, `beta`, hence divides `r = beta v` or `s = alpha v`, hence by 5b

        gamma_pi(r) = 0   or   gamma_pi(s) = 0,

so `phi(u) = 0 + c = c != 0` and the vector imposes no condition.  This holds for
**both** primes, for **any** `lambda`, rational or not.

*Verified*: `scripts/prove_step5.py` examines all **444** cross vectors with
`lambda != -1` over every rank-8 spindle to `a = 40`.  For every even `a`, each
prime divides `r` or `s` in **100%** of them.  **Zero counterexamples.**

**The odd case, and the one exception.**  For odd `a` the lemma says nothing, and
the run shows why it does not need to: at `a` = 9, 15, 21 every cross vector is
still covered (those are the `|d| = 1` ones, where one of `p`, `q` is even and so
divisible by both primes), and the only `a` where coverage fails is **`a = 39`,
0 of 12** -- which is exactly the `|d| = 2` case of 5(c).

There the two colours are **equal**, and 5b says why in one line: `p` and `q` are
both odd, so `pi` divides neither, so multiplication by them is invertible mod
`pi` and

        gamma_pi(r) = 0   <=>   pi | v   <=>   gamma_pi(s) = 0.

Both vanish or neither does, so the vector imposes the same **diagonal**
condition `(c, c)` that the shell displacements of step 4 impose, which the same
12 of 36 automorphism pairs satisfy.  Measured, neither vanishes.

**And that last statement is a congruence, not a measurement.**

> **Lemma.**  In the `|d| = 2` case, `pi` divides `v` for neither prime.

*Proof.*  Suppose `v = pi w` with `w` in `R`.  `pi = (5 +- sqrt33)/2` is **real**,
so `conj(pi) = pi` and `|v|^2 = pi conj(pi) |w|^2 = pi^2 |w|^2`.  With
`|v|^2 = 1/9` from 5(c),

        |w|^2  =  1 / (9 pi^2)  =  (29 -+ 5 sqrt33) / 72  =  (58 -+ 10 sqrt33) / 144.

In the chart `|z|^2 = [(A^2 + 33B^2 + 3C^2 + 11D^2) + 2(AB + CD) sqrt33]/144`,
so `A^2 + 33B^2 + 3C^2 + 11D^2 = 58`.  The lattice forces
`A = B = C = D (mod 2)`:

* all **even** makes the form `= 0 (mod 4)`, and `58 = 2 (mod 4)`;
* all **odd** makes every square `= 1 (mod 8)`, so the form
  `= 1 + 33 + 3 + 11 = 48 = 0 (mod 8)`, and `58 = 2 (mod 8)`.

Neither is possible, so no such `w` exists. ∎

*Checked exhaustively*: **0** lattice points at either norm.  And the chart alone
has **4** solutions, so it is the congruences -- the actual lattice against its
index-16 superset -- that rule it out, not the quadratic form.

So `gamma_pi(v) != 0`, both colours of the diagonal pair are non-zero, and the
vector imposes exactly the condition step 4 already imposes.

**Step 5 is proved.**

*A claim withdrawn in passing.*  An earlier draft of this section said every
irrational `lambda` factors as `unit * (pi_2/pi_1)^j`.  That is **false**: at
`a = 16`, `lambda = (-77 - 3 sqrt33)/64` has `N(lambda) = 11/8`, not a power of
two.  It happened to hold at `a` = 4 and 10.  The lemma above replaces it and
needs no factorisation at all.

**5d.  The choice of colouring is free.**  Step 6 needs `c != 0` uniformly over the
shell, not merely "not both colours vanish".  That follows from:

> **Lemma D.**  For a shell point `r`, either both primes above 2 divide `r` --
> which happens exactly when `4 | a` -- or neither does.

*Proof.*  Both divide iff `r` lies in `pi_1 R inter pi_2 R = 2R`, which step 4
makes `4 | a`.  Suppose exactly one does, `r = pi_1 w`.  Then
`|w|^2 = a/pi_1^2 = a(29 - 5 sqrt33)/8`, so in the chart `X = 522a`, `Y = -90a`.
If `a` is odd then `X = 2 (mod 4)`, and `X = [A]+[B]+3[C]+3[D] (mod 4)` reaches 2
only on the patterns `ooee` and `eeoo`, both of which break the first congruence.
If `a = 2 (mod 4)`, write `a = 2a'` with `a'` odd: `X = 4 (mod 8)`, which all-odd
coordinates cannot give (they force `X = 0 (mod 8)`), so all are even and
`AB + CD = 4(A'B' + C'D')` -- against `Y/2 = -90a'`, which is `2 (mod 4)`. ∎

*Verified*: over every shell to `a = 49`, a prime divides a shell point only when
`4 | a`, and then both do, on every point.  No exception.

**6.  Conclusion.**

* `4 | a`:  by 3 and 4 there is a cross unit vector with **both** colours zero, so
  `phi(u) = 0` for every one of the 24 candidates.  No certificate exists.
* `4` does not divide `a`:  by 4 the shell displacements give only **diagonal**
  pairs `(c, c)`, and by 5 nothing else constrains.  Two automorphisms differing
  at every point satisfy `pi_1(c) != pi_2(c)` -- 12 of the 36 pairs do -- so a
  certificate exists.

## Status of each step

| step | status |
|---|---|
| 1, direct sum and the bound of 24 | a **hypothesis** of the theorem (rank 8), checkable per rotation; the count is exact at 24 |
| 2, parallelism | **proved** -- the irrationality of `sqrt(4a-1)` |
| 3, `lambda = -1` are the shell points | **proved** -- `\|1 - theta\| = 1/sqrt a` |
| 4, `r in 2R <=> 4 \| a` | **proved** -- Lemmas A, B, C of `results/LAW-PROOF.md`; no residual check |
| 5, `lambda != -1` imposes nothing new | **proved**, rational and irrational alike, once the colourings are read as reduction mod the two primes above 2 |
| 6, conclusion | follows |

**Nothing in the chain is carried by verification.**

Step 5's old argument was **wrong**: it claimed `\|p - q\| = 1`, measured to
`a <= 35`, and `a = 39` breaks it with `lambda = -13/15`.  It also had the colour
kernel wrong -- `ker gamma` is `pi_i R`, not `2R`.  Step 4 was an exhaustive sweep
of 11776 residue tuples mod 32; it is now three short lemmas.  Every one of those
repairs was found by checking a claim before writing it down, and each replaced a
verification with an argument.

**The conclusion was re-derived with both Ducz colourings**, not one.  Ranging
over `2 x 2` colourings and `6 x 6` automorphisms -- 144 pairings in all -- gives

    4 does not divide a:  24, 144, 24, 72, 24, 24 valid pairings (a = 5, 6, 9, 10, 11, 13)
    4 | a:                0 in every case          (a = 4, 12, 20, 28)

so the theorem does not depend on which Ducz colouring is chosen.  An earlier
pass used a single one and reached the same conclusion, but only this version
establishes it.

Reproduce: `scripts/prove_law_direction.py` (step 4), `scripts/cross_pairs.py`
(steps 1, 2, 3, 5).
