# Cover note

**A divisibility obstruction for joining two Moser lattices** — 45 pages.

Enclosed:

| | |
|---|---|
| `joining-rotations.pdf` | the manuscript, 45 pages |
| `FOR-THE-REVIEWER.md` | what is supplied, what is already known to be open, and the cheapest checks in order |
| `RESPONSE.md` | point-by-point reply to the previous round, if you want to see what changed and why |
| `VERIFICATION.md` | every check we ran, with its output, so you can compare rather than trust |
| artifacts | <https://github.com/calinnedelcu/joining-rotations-artifacts>, public, release `v1.1` |

## The short version

We prove that if the joint lattice `R + theta_a(R)` has rank 8 and `4` does not
divide `a`, it carries a 4-colouring by a group homomorphism — so no subset of
it is 5-chromatic, at any size, and no 5-chromatic `L ∪ theta_a(S)` exists. The
engine is that `3R` is the maximal order of `Q(sqrt33, i·sqrt3)`, which turns the
lattice's two integral geometric 4-colourings into reduction modulo the two
primes above 2, and shell occupancy into a relative-norm condition with a
closed-form answer. `V` is the narrow Hilbert class field of `Q(sqrt33)`.

Against the obstruction: seven joining spindles, an infinite chained family at
`a = 64n^2/9`, eleven further exclusions, and an exact interface bound at
`theta_4`.

**The record of 509 is untouched, and we say so in the abstract.** The law is
also provably silent exactly where working rotations live — Section 1 states
this in one paragraph rather than leaving it to be assembled. We think the
durable contribution is the arithmetic, not the obstruction, and the paper is
now framed that way.

## What you can check, and how long it takes

From a clean clone of the archive:

| | |
|---|---|
| `scripts/audit_numbers.py` | 97 checks, ~3 min, standard library only, shares no code with the rest |
| `scripts/check_drat.sh` | **8 DRAT certificates**, ~10 min, all `s VERIFIED` |
| `scripts/check_emptyshell.py` | 9 witnesses, seconds, imports nothing from the project |
| `scripts/check_periodic.py` | 11 witnesses, seconds, same |
| `bash scripts/verify_all.sh` | the whole table in parallel, a little over an hour. Last full run: **35 of 35 PASS**, 0 FAIL, 0 TIMEOUT |

Every construction in the paper carries a checked proof. `drat-trim` is
deliberately not vendored — fetch and build it yourself; the sha256 of the
source we used is pinned in `proofs/README.md`.

## Since the last round

Section 9's open case is closed: `theta_7` on Haugland's lattice **survives**,
and informatively — it has no half-unit vector, so Proposition 25 gives it no
free pass and the complete search that follows returns nothing. The enumeration
cost 11 522 seconds. `N = 9` remains open, and is rank 24.

## Two things are still missing, and they are ours

The archival DOI and the affiliation are the only `[TO BE SUPPLIED]` left in the
manuscript.
