# Cover note

**A divisibility obstruction for joining two Moser lattices** — 25 pages.

Enclosed:

| | |
|---|---|
| `joining-rotations.pdf` | the manuscript, also deposited on its own at [10.5281/zenodo.22898569](https://doi.org/10.5281/zenodo.22898569) — that DOI is the citable address of this exact 25-page version. It is v2; v1 carried two wrong bibliography entries and is superseded |
| `FOR-THE-REVIEWER.md` | what is supplied, what is already known to be open, and the cheapest checks in order |
| `VERIFICATION.md` | every check we ran, with its raw output, so you can compare a run rather than trust a summary |
| artifacts | <https://github.com/calinnedelcu/joining-rotations-artifacts>, public; archived at Zenodo, DOI [10.5281/zenodo.22855504](https://doi.org/10.5281/zenodo.22855504), which resolves to the deposit matching this manuscript. The paper's code and data are those of commit `78b7579a74373cdb9fd1391ffcd1b278a27c26c9`; the commits after it touch documentation and the manuscript only |

## The result, in one paragraph

Write `R` for the Moser lattice and `theta_a` for the rotation with
`cos = (2a-1)/(2a)`, so `a` is the squared radius at which `theta_a` pairs a
point with its own image. We prove: if the joint lattice `R + theta_a(R)` has
rank 8 and `4` does not divide `a`, it carries a 4-colouring by a group
homomorphism — so no subset of it is 5-chromatic at any size, and no 5-chromatic
`L ∪ theta_a(S)` exists for any `L, S ⊆ R`.

The engine is a structural fact: `3R` is the maximal order of
`V = Q(sqrt33, i·sqrt3)`. From it, the lattice's two integral geometric
4-colourings are reduction modulo the two primes above 2, and occupancy of the
shell at radius `sqrt a` becomes a relative-norm condition with a closed-form
answer — `R` has a point at squared radius `n/b` in lowest terms iff
`b ∈ {1,3,9}` and `v_p(n)` is even at every prime splitting in `Q(sqrt33)` and
inert in `Q(sqrt-3)`. `V` is the narrow Hilbert class field of `Q(sqrt33)`,
which makes the local behaviour class field theory rather than case work.

Against the obstruction: infinitely many spindles join, by chaining a gadget of
Parts' (Lemma 20); eleven further integer candidates die to a periodic
refinement; and seven rotations carry explicit unions, each with a checked DRAT
certificate in the archive. The constructions themselves, and the interface
bound at `theta_4`, are left for a companion paper; this one keeps the arithmetic
and the law, and depends on that paper for nothing — every computation behind
the table is in the archive at the pinned commit.

## What this does not do

**The record of 509 is untouched**, and we say so in the abstract. The law is
also provably silent exactly where working rotations live: Theorem 1's own
second half proves that at `4 | a` with an occupied shell *no* homomorphism
colouring exists, so the method has nothing further to say there. We think the
durable contribution is the arithmetic rather than the obstruction, and the
paper is framed that way. `FOR-THE-REVIEWER.md` lists the rest of what is open.

## What you can check, and how long it takes

From a clean clone of the archive:

| | |
|---|---|
| `scripts/audit_numbers.py` | 97 checks, ~3 min, standard library only, shares no code with the rest |
| `scripts/check_drat.sh` | **8 DRAT certificates**, ~10 min, all `s VERIFIED` |
| `scripts/check_emptyshell.py` | 9 witnesses, seconds, imports nothing from the project |
| `scripts/check_periodic.py` | 11 witnesses, seconds, same |
| `bash scripts/verify_all.sh` | the whole table in parallel, a little over an hour. Every entry passed on the run at the pinned commit, with no FAIL and no TIMEOUT. The script prints its own tally at the end; read that rather than a count quoted here, which is exactly the sentence that has gone stale before |

Every construction in the paper carries a checked proof. `drat-trim` is
deliberately not vendored — fetch and build it yourself; the sha256 of the
source we used is pinned in `proofs/README.md` and printed by the script.

## Nothing is left blank

The manuscript carries no placeholders: the affiliation is filled and the
archive is deposited at Zenodo under the concept DOI
[10.5281/zenodo.22855504](https://doi.org/10.5281/zenodo.22855504), which
resolves to the newest version while the commit hash beside it fixes the
snapshot these numbers came from.
