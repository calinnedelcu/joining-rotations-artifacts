# Every claim in the papers, reproduced in one pass

Run `scripts/verify_all.sh`. It executes every script `paper/README.md` names,
one log per script, and reports pass, fail or timeout. This file records the
pass of 17 September 2026 and what each script actually returned, so that a
number in the papers can be traced to a line of output rather than to a memory
of one.

## The pass of 20 September 2026, and what it deliberately skipped

A second pass after the page-by-page read-through. Everything the read-through
touched was re-run; four scripts were not, on purpose, and the reason is recorded
here rather than left to be inferred from a gap.

Run and passing: `audit_numbers.py` (69 numbers, new), `blind_spot.py`,
`finer_lattices.py`, `step5_signs.py`, `two_colourings.py`, `shells.py`,
`shell_criterion.py 400`, `hept_rank.py`, `hept_classify.py 1 2`,
`interface_bound_exact.py` at 4, 16, 28 and 36, `rank8_condition.py`,
`interface_bound.py`, `interface_matchings.py`, `build_join16.py`,
`prove_law_direction.py`, `hept_halfunit.py 1`, `voronov_rotations.py`,
`join_filter_residues.py` at 12 and 20. All eight figure scripts regenerate and
pass their assertions. All ten construction sizes match their coordinates on
disk. Both papers compile with zero errors.

Not re-run, and why:

| script | cost | changed since the 17 September pass? |
|---|---|---|
| `z4_relation.py 100` | 48 min | no -- untouched |
| `rho_unit_family.py` | 433s | no -- untouched |
| `lambda_sweep.py` | 46 min | docstring only: "step 4" to "step 2", `|v|^2` to `|v/2|^2` |
| `prove_step5.py` | 21 min | yes, the trichotomy counter -- **and it was run in full** that day: 552 cross vectors to `a = 60`, 0 counterexamples to the contrapositive and 0 to the trichotomy |

So three carry unchanged code and the fourth was measured after its change. Their
17 September results stand. Before submission they should be run once more, as a
single clean end-to-end pass -- `scripts/verify_all.sh` now covers all 30 entries
of the table, where it covered 14.

## The reproducibility table

| script | verdict | time | what it returned |
|---|---|---|---|
| `shells.py 100` | PASS | 1s | occupied and empty shells to 100; the empty multiples of 4 are 8, 24, 32, 40, 56, 68, 72, 88, 96 |
| `hept_rank.py` | PASS | 2s | Haugland's lattice rank 12 at 1, 2, 3 and 4 sets; joint rank 24 throughout; covolume **1, 1/7, 1/49, 1/343** (pivot products `7^11`, `7^10`, `7^9`), asserted |
| `finer_lattices.py` | PASS | 4s | section 10's nested family: generators **30, 42, 54, 66**, indices **1, 9, 81, 729** over the 30-vector lattice, and the unit vectors are exactly the generators at `J = 2` (30) and `J = 3` (42) |
| `blind_spot.py` | PASS | 1s | both lattices carry a unit triangle -- **60** ordered triples on the Moser lattice, **84** on Haugland's -- so Proposition 23's cyclic half holds for both at every `a = 4m^2`; `|h_g| = 1/2` exactly at `a = 4, 16, 36, 64, 100, 144` |
| `hept_classify.py 1 2` | PASS | 1s | `theta_1` dead by a Klein colouring, `theta_2` **survives**; square roots in `Q(zeta_420)` are 1, 3, 5, 7, 15, 21, 35, 105 |
| `interface_bound.py 4 --depth 4 --radius 2.53 --model shared` | PASS | 6s | 126 cross edges, 384 pairings, 235 patterns, UNSAT at 4 and SAT at 5 |
| `interface_bound_exact.py 4` (and `16`, `28`, `36`) | PASS | 1s | the same bound with no ball, from Proposition 18: `theta_4` 126 cross edges, 66 usable, 235 patterns, **5**; `theta_16` **1**; `theta_28` **180** cross edges (the depth-6 ball found only 156), 120 usable, **5**; `theta_36` **5** |
| `interface_matchings.py` | PASS | 33s | 1920 minimum interfaces, all perfect matchings, all one profile, `30 x 8 x 8` relative to the reference edge |
| `hept_halfunit.py 1` | PASS | 106s | joint rank 24, 210 unit vectors, **42 in `2*Lambda`**, one per generator |
| `voronov_rotations.py` | PASS | 5s | all five are `rho*u`, one of five fixes `R`, one of five is a spindle, criterion kills none |
| `prove_law_direction.py` | PASS | 1s | 11776 residue tuples, **0 exceptions**; `4 | a` admits no homomorphism 4-colouring |
| `step5_signs.py` | PASS | 1s | the chart congruences cut out `R` exactly (index 16, 6561 of 6561 agree); `a = 7/19` odd and rank 8 carries a cross unit vector with **lambda = +1**; neither prime divides it; the two finite checks proving `v_pi(|v|^2) = 2 v_pi(v)` (30 of 30 unit vectors, 435 of 435 polarisations; three classes, all at norm 1/9); and the identity sampled on 8198 points, **0 mismatches** |
| `prove_step5.py` | PASS | 1266s | 552 cross vectors with `lambda != -1` to `a = 60`: **0 counterexamples** to the contrapositive and **0** to the trichotomy (4 does not divide `a` => no prime divides both `r` and `s`). Each prime divides `r` or `s` in every vector except at `a = 39` and `a = 51`, the two `|d| = 2` spindles |
| `lambda_sweep.py` | PASS | 2766s | `a = 2` to `80`, 72 rows, **0 violations** of the repaired step 5 |
| `join_filter_residues.py 12` | PASS | 4s | `theta_12` DEAD, 69 occurring residue pairs at `m = 4` |
| `join_filter_residues.py 20` | PASS | 8s | `theta_20` DEAD |
| `rho_unit_family.py` | PASS | 433s | both filters kill **0 of 30**; 6 units fix `R`, 2 rotations are spindles |
| `rank8_condition.py` | PASS | 44s | 50 rotations, **0 mismatches**; rank 4 exactly at the nine excluded `a`, 8 elsewhere |
| `z4_relation.py 100` | PASS | 48min | every spindle to `a = 100` with a half-unit vector -- **16 of 16**, including 48, 64 and 80 -- carries the odd relation. The earlier row said it failed at 48, 64 and 80; that was a bug in the sweep, which discarded the zero class before testing -- and at those three every half-unit vector lies in `2*Lambda`, so discarding zero emptied the system |
| `shell_criterion.py 400` | PASS | 30s | **0 mismatches** to 400 and on 16 targeted larger values including 17^2, 17^3, 101^2, 2^8 |
| `two_colourings.py` | PASS | 3s | 9 unit-vector classes, 35 subgroups, **exactly 2** survive; `moser_is_ov.py` now proves the same two from `R/2R = F_4 x F_4` |
| `cross_kinds.py` | PASS | 153s | kinds of joining edge, from the joint lattice's unit vectors with no ball: **2, 4, 3, 2** for `theta_4/16/28/36`, **1** for each rational spindle, and **2** for each of the five rotations already known -- so 4 + 5 - 1 = **8** are type M |
| `ball_params.py` | PASS | see table | the ball behind each construction, measured from the shipped coordinates: half-size, radius and the smallest generation depth that reproduces the half exactly |

Note on `hept_halfunit.py`: its arguments are set counts and it defaults to
`1 2`. The paper's figure is the one-set case, which takes 106 s; two sets and
up are far more expensive and did not finish in 40 minutes. So the command to
reproduce the claim is `hept_halfunit.py 1`, and the table now says so. Called
bare it produced a TIMEOUT twice here, which measured the argument default and
not the claim.

## The kill certificates, checked on real coordinates

Section 7 says each kill is a certificate checked against the exact edge set of
a ball holding the whole shell. Both reproduce exactly:

| rotation | ball | shell held | edges recomputed | monochromatic |
|---|---|---|---|---|
| `theta_12` | 39445 points, union 78890 | 42 of 42 | **867054** | **0** |
| `theta_20` | 88489 points, union 176978 | 60 of 60 | **2076192** | **0** |

Both hold the complete shell, which is the guard that the routes 20/44/48 errors
lacked. A negative over a partial shell says nothing.

## `R = (1/3) O_V`, which proves the shell criterion

`3R` is closed under multiplication (checked on a basis and on all 900 products of
unit vectors) and contains 1, since `1/3` is in `R`. Its trace-form discriminant is
**1089 = 33^2 = disc(F)^2**, so it is the *maximal* order of `V = Q(sqrt33, i sqrt3)`.
Hence `|z|^2` is the relative norm `N_{V/F}`, and occupancy is a norm question.

The rest, from PARI: `h(F) = h(V) = 1`; `disc(V) = 1089`, so `V/F` is unramified at
every finite prime; `V` is totally imaginary, signature `(0,2)`; the fundamental
unit of `V` has `N_{V/F}(eta) = 23 - 4 sqrt33`, which is `F`'s fundamental unit and
totally positive; and the primes of `F` inert in `V` are exactly those over the
obstructed `p`, plus the one over 11 where rational valuations are even anyway.
Hasse's norm theorem then gives the criterion in both directions.

`scripts/moser_is_ov.py` checks all of it. Proposition 16 was a conjecture through
five rounds of review because this structure was missed.

## Ducz's lattice is not `R`

Checked in the chart, because the paper's attribution turned on it: the lattice
`Z<1, omega_1, omega_3, omega_1 omega_3>` has chart determinant 144 against `R`'s
16, so index **9** in `R`; it does not contain `1/3 = (4,0,0,0)`, which `R` does;
and it misses twelve of `R`'s thirty unit vectors. The two theorems are about
different groups, and the paper no longer says otherwise.

## The eight homomorphism colourings of `R`

`hn.algcolour` on the 30 unit vectors, in a fresh process: **2** Klein colourings
(up to colour permutation -- Theorem 4's two) and **6** `Z/4` colourings (up to
negation, the only automorphism of `Z/4`). Eight in all, giving the `8^2 * 6 = 384`
admissible pairings of section 8. The six cyclic ones had never been counted in
the paper, only in the code.

## Interface richness of the seven

Unit vectors of the joint lattice, counted directly from `Lattice.unit_vectors()`
in a fresh process, against the `units` field the classification JSONs already
record:

| | joint lattice | new (minus `R`'s own 30) | genuinely cross (minus 60) |
|---|---|---|---|
| `theta_4` | 126 | 96 | 66 |
| `theta_16` | 126 | 96 | 66 |
| `theta_28` | 180 | 150 | 120 |
| `theta_36` | 150 | 120 | 90 |
| `alpha_64/3` | 78 | 48 | 18 |
| `alpha_64/9` | 66 | 36 | **6** |
| `alpha_256/9` | 66 | 36 | **6** |

The two 6s are the shells themselves: `alpha_64/9` and `alpha_256/9` each hold six
shell points and acquire no other joining vector, so the smallest union of the
seven comes from the poorest interface.

## The seven constructions

Every size the paper prints matches the coordinates on disk, to the vertex:

| | paper | file |
|---|---|---|
| `theta_4` | 509 | `out/driven_rec509_17.pts` |
| `theta_16` | 29113 | `out/join16.pts` |
| `theta_28` | 156577 | `out/join28.pts` |
| `theta_36` | 175825 | `out/join36.pts` |
| `alpha_64/3` | 187225 | `out/join64_3.pts` |
| `alpha_64/9` | 5809 | `out/join64_9.pts` |
| `alpha_256/9` | 158257 | `out/join256_9.pts` |
| `theta_16` minimised | 2901 | `results/theta16/t16_best.pts` |
| `alpha_64/9` minimised | 1408 | `results/alpha64_9/minimised.pts` |
| asymmetric basin | 889 | `results/asym/minimised889.pts` |

`theta_16`'s union had never been kept: the paper printed 29113 and
`docs/ATTEMPTS.md` recorded the check, but only the minimised 2901 was on disk, so
"every size matches the coordinates" was not literally true. `build_join16.py`
rebuilds it from the recipe in 36 s -- ball of depth 4 and radius 4.0 in
`Q(sqrt3, sqrt7, sqrt11)`, 14557 points, 30 of them on the shell at squared radius
exactly 16, union **29113**, **285294** edges recomputed from the coordinates with
0 wrong among 4076 sampled, minimum degree 4, and **not 4-colourable** in a fresh
solver -- and writes `out/join16.pts`.

`alpha_64/9`, the paper's headline exhibit, was additionally rebuilt end to end
in a fresh process: rotation modulus exactly 1, all 30 lattice vectors exactly
unit, 5809 points loaded, **12** on the shell at `|z|^2 = 64/9` exactly -- the shell
itself holds **6** lattice points, as Figure 6 says, and the union carries their six images
too -- **41982**
edges recomputed from the coordinates, **0** wrong among 800 re-tested exactly in
`K`, minimum degree 5, and **not 4-colourable** in a fresh solver in 5 s.

## `v5-at-least-29.tex`

No scripts: both inputs are quotations and the argument is arithmetic. Both
quotations were read from the source PDFs, not from notes here:

* de Grey and Parts, verbatim: *"we get the bounds: e5 >= 99, v5 >= 28,
  e6 >= 182, v6 >= 42"*.
* Alexeev, Mixon and Parshall, Theorem 1(b): `u(28) <= 96`, `u(29) <= 103`, with
  lower bounds 89 and 93.

The arithmetic checks: `u` non-decreasing; `96 < 99` kills every `n <= 28`;
`103 >= 99` stops the route at 29 exactly; the thresholds for 30 and 31 are
`e5 >= 104` and `e5 >= 111`; `1/104 = 0.0096154`; the drop needed below `1/99` is
**4.81%**, which the paper calls "about 5%"; and the target `u <= 98` lies inside
both open intervals `[89, 103]` and `[93, 110]`.

## What the pass changed

One thing, and it made a claim stronger rather than weaker. The paper said the
corollary was checked on **444** cross vectors to `a = 40`. `prove_step5.py`
sweeps to 60 by default and returns **552**, still with zero counterexamples;
restricted to `a <= 40` it returns exactly 444, so the old figure was right but
narrower than what the code proves. The paper now states the wider one.

Two entries of the table were not literally runnable and are now: 
`join_filter_residues.py` takes a rotation, and two budgets in
`verify_all.sh` were below what their scripts need.
