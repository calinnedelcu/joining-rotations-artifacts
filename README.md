# Which rotations join two Moser lattices — computational artifacts

Everything the paper's computational claims rest on, with the command that
reproduces each and the log of the run that produced the numbers printed here.

## Coverage: what is checked here, and what is not

A reviewer's first question is which claims this archive actually settles. This
table is the honest answer, and it is deliberately the first thing in the file.

| claim | status here |
|---|---|
| every number in the paper | `scripts/audit_numbers.py`, PASS. One block is **read** from `results/JOIN-CLASSIFICATION.json`, not re-derived, and the script says so as it runs |
| `R = (1/3) O_V`, `R/2R = F_4 x F_4`, Theorems 4 and 16 | `scripts/moser_is_ov.py`, PASS. Its second half needs `cypari`; without it the script **skips** that stage |
| the seven constructions, chi >= 5 | coordinates in `graphs/`, and **all seven now ship a checked DRAT certificate** in `proofs/` -- `scripts/check_drat.sh` re-verifies the eight proofs (the seven plus Parts' 509 record) in about ten minutes, each reporting `s VERIFIED` |
| chi = 5 for a full union | **not established** for any of the seven, and the paper says so. Lemma 21 gives `chi = 5` for a minimal induced subjoin of any of them; the vertex-critical 1408 has it outright |
| the eleven periodic exclusions | **all 11** have a witness in `results/periodic/`, named for its modulus. Nine die at `m = 4`; `theta_48` and `theta_80` are degenerate at `m = 4` and `m = 6` and die at `m = 8`. `scripts/check_periodic.py` re-validates all eleven from the JSON alone, importing no project code: 11 witnesses, 0 bad |
| `a = 64` joins | `proofs/gadget367.*` certifies the premise -- Parts' gadget has no 4-colouring separating its terminals -- and `scripts/gadget_chain.py n`, PASS at n = 1, 2, 3 in 40s each. The check is structural, not a solve: the gadget's monochromatic-pair property on 367 vertices, plus all six copies present intact (1822/1822 edges) inside the union. `GADGET_CHAIN_SOLVE=1` adds the redundant direct solve, which agrees at n = 1 in 450s and does not finish at n = 3 |
| the ball behind each construction | `scripts/ball_params.py`, measured from the shipped coordinates |
| kinds of joining edge | `scripts/cross_kinds.py`, PASS |
| the 5-cross-edge bound and the 1920 sets | `scripts/interface_bound_exact.py`, `interface_matchings.py`. The 1920 solve a **restricted hitting-set problem**; no 5-chromatic graph with five cross edges is claimed |
| the whole suite from a clean extraction | run in full: **35 of 35 PASS**, no FAIL and no TIMEOUT. The suite has grown to 47 entries since that run: `check_notes`, the nine periodic regenerations that used to be represented by two, `check_binding`, and `check_claims`. Each was run on its own and passes |
| the claims this archive makes about itself | `scripts/check_claims.py` reads each number out of the manuscript and compares it with the filesystem, and executes each claimed behaviour: **14 of 14** |

This archive is deposited at Zenodo under the concept DOI
[10.5281/zenodo.22855504](https://doi.org/10.5281/zenodo.22855504),
which resolves to the newest version.

The certificate gap is closed. A reviewer asked why the only proof here was for
someone else's graph while our own claims were solver verdicts, and was right.
`proofs/` now holds eight DRAT proofs -- every construction of the paper's
Section 6, the monochromatic-pair property Lemma 20 rests on, and Parts' record
-- each with its `drat-trim` log. At 415 MB of compressed proof they are most of
this repository, and a shallow clone runs to about 900 MB; they are also the
point of it. If you would rather test the pipeline before pulling that, the
smallest is 31 MB and checks in half a minute:

    bash scripts/check_drat.sh ./tools/drat-trim gadget367

Nothing in the checking path needs a SAT solver, or `pysat`, or the `.venv`:
`check_drat.sh`, `check_emptyshell.py`, `check_periodic.py` and
`audit_numbers.py` all run on a bare `python3` plus a `drat-trim` you built
yourself. We ran exactly that from a clean clone on Python 3.14 with no `pysat`
present: 97/97 numbers, 9 empty-shell witnesses, 11 periodic witnesses, 8
certificates. A solver is needed only to *regenerate* a proof or to rebuild a
construction from scratch.

The nine empty-shell verdicts of Section 7 are certified too, differently:
`results/emptyshell/` holds a witness for each, and `scripts/check_emptyshell.py`
validates all nine from the JSON alone, computing lengths from the field's own
multiplication table and importing nothing from this project. For the six that
die the witness is an explicit homomorphism 4-colouring; for the three that
survive it is a vector of length 1/2, which by Proposition 5 settles the question
in one line rather than by a search log.

## What is new since the previous archive

* **`a = 64` is settled**, by `scripts/gadget_chain.py`: Parts' 367-vertex
  monochromatic-pair gadget lies wholly in R, chaining three copies puts its
  terminals 8 apart, and the join with the theta_64 image is not 4-colourable.
  Lemma 20 in the paper. The same lemma gives the infinite family a = 64n^2/9.
* **Periodic witnesses are written and self-checked.** `join_filter_residues.py`
  used to call `solve()` and discard the model, so the colourings the paper
  promised were never saved. Each `results/periodic/*.json` now holds both
  colourings and every occurring residue pair, and the script re-checks what it
  wrote: both proper on Lambda/mLambda, agreeing at the shared origin,
  disagreeing on every occurring pair.
* **`data/parts/`** ships the two gadgets Lemma 20 uses, so the chaining is
  checkable from this archive alone.

* **`R = (1/3) O_V`.** The Moser lattice is one third of the maximal order of
  `Q(sqrt33, i sqrt3)`. That turns the shell criterion from a conjecture into
  Theorem 18 (see *Status* below) and gives Theorem 9 a structural proof:
  `R/2R = F_4 x F_4`, a unit vector is invertible at both primes, and a plane
  missing all nine such classes is a union of two subgroups, hence is one of them.
  New script `scripts/moser_is_ov.py`.
* **Kinds of joining edge**, new script `scripts/cross_kinds.py`: the five
  rotations already known have two each, so eight rotations are type M in Parts'
  sense, not four.
* **A normalisation.** `theta_{a/(4a-1)} = -conj(theta_a)` is an involution
  exchanging `(1/4, 1/2)` with `(1/2, infinity)`, so `a >= 1/2` throughout.
* Section 5 keeps the proof and the case analysis it replaced moves to Appendix A.
* `scripts/two_colourings.py` no longer concludes the identification from
  O-stability, which does not follow: eleven of the thirty-five subspaces are
  stable. It tests divisibility directly instead.
* **Every `.pts` now names its field** on its first line, and the loader refuses
  a file whose header disagrees with the field in force. The previous archive was
  not internally consistent about this: `graphs/join16.pts` is over `(3, 11, 7)`
  and `results/theta16/t16_best.pts` over `(3, 7, 11)`, and reading either in the
  other order gives a sparser graph that is 4-colourable, silently.
* **Three things that were broken as distributed and are not now**:
  `scripts/reverify_join.py` looked only in `out/`, where this archive puts the
  coordinates in `graphs/`; `scripts/audit_numbers.py` crashed on the absent
  `data/vtx/509.vtx`, which now ships; and `verify_all.sh` hardcoded a `.venv`
  that a fresh extraction does not have.
* `scripts/ball_params.py` recovers each construction's ball -- half-size, radius
  and generation depth -- from the shipped coordinates, which is where the paper's
  new depth and radius columns come from.

## Running it

Python 3.11 with `python-sat` for anything that calls a solver; the rest is
standard library only. From this directory:

    python3 -m venv .venv && .venv/bin/pip install python-sat
    .venv/bin/python scripts/audit_numbers.py        # no solver needed
    bash scripts/verify_all.sh                       # all 48 entries

`verify_all.sh` uses `.venv/bin/python` when there is one and the `python3` on
PATH otherwise, says which it picked, and warns if `python-sat` is missing; set
`PY=` to override it, `OUT=` to choose where the per-script logs go, and `JOBS=`
to set how many entries run at once (6 by default). It was
run once, in full, from a clean extraction of this tarball -- which is how the
two broken paths below were found.

`scripts/verify_all.sh` writes one log per script and prints PASS, FAIL or
TIMEOUT for each. Most entries are single-threaded and the box is not, so the
default `JOBS=6` turns about three hours into a little over one; `JOBS=1` runs
them in sequence. `lambda_sweep`, `z4_relation`, `prove_step5` and
`rho_unit_family` are the long ones, and they set the floor whatever `JOBS` is.

## The claim-to-file map

| paper | claim | command | log |
|---|---|---|---|
| all | every number re-derived from the definitions, sharing no code with `hn/` | `scripts/audit_numbers.py` | `logs/audit_numbers.log` |
| Prop 8, Thm 9, Thm 18 | **`R = (1/3) O_V`**: the maximal order, `R/2R = F_4 x F_4`, the nine unit classes, the two planes, and every ingredient of the shell criterion | `scripts/moser_is_ov.py` | `logs/moser_is_ov.log` |
| Thm 1 | steps 4 and 5 over every rank-8 spindle to `a = 80` | `scripts/lambda_sweep.py` | run it |
| Thm 1 | 552 cross vectors to `a = 60`: the contrapositive and the trichotomy | `scripts/prove_step5.py` | `logs/prove_step5.log` |
| App A | the odd case on both signs of lambda; the valuation lemma | `scripts/step5_signs.py` | `logs/step5_signs.log` |
| Thm 1 | the congruence reduction behind step 3 | `scripts/prove_law_direction.py` | `logs/prove_law_direction.log` |
| Thm 9 | the same count by enumeration -- 35 subgroups, 2 survive -- and the two identified by testing `gamma_i(x) = 0` iff `pi_i` divides `x` on a ball | `scripts/two_colourings.py` | `logs/two_colourings.log` |
| Prop 4 | rank 4 exactly at `4a-1 = 3k^2` or `11k^2` | `scripts/rank8_condition.py` | `logs/rank8_condition.log` |
| Prop 6 | the odd relation holds at every spindle with a half-unit vector | `scripts/z4_relation.py 100` | `logs/z4_relation.log` |
| Thm 18 | the closed criterion against the form, every `a <= 400` | `scripts/shell_criterion.py 400` | `logs/shell_criterion.log` |
| §6 | which shells are non-empty | `scripts/shells.py 100` | `logs/shells.log` |
| §6 | `theta_16`'s union rebuilt from the recipe and re-verified | `scripts/build_join16.py` | `logs/build_join16.log` |
| §6 | **kinds of joining edge**: 2/4/3/2 for the integer spindles, 1 for each rational one, and 2 for each of the five rotations already known -- so eight are type M | `scripts/cross_kinds.py` | `logs/cross_kinds.log` |
| §7 | the periodic filter, every occurring residue pair | `scripts/join_filter_residues.py 12` and `20` | run it |
| companion | the five-cross-edge bound, from a ball | `scripts/interface_bound.py 4 --depth 4 --radius 2.53 --model shared` | run it |
| companion | the same bound with **no ball**, from the companion's ball-free proposition | `scripts/interface_bound_exact.py 4` (also 16, 28, 36) | `logs/interface_bound_exact_*.log` |
| companion | the 1920 minimum interfaces, their shape and factorisation | `scripts/interface_matchings.py` | `logs/interface_matchings.log` |
| §8 | `L_1` to `L_4`: rank 12, joint rank 24, covolume 1/7 each step | `scripts/hept_rank.py` | `logs/hept_rank.log` |
| §8 | `theta_1` dead and `theta_2` surviving in `L_1` | `scripts/hept_classify.py 1 2` | `logs/hept_classify.log` |
| §8 | `theta_4`'s free pass there: 210 units, 42 in `2*Lambda` | `scripts/hept_halfunit.py 1` | run it |
| companion | both lattices carry a unit triangle | `scripts/blind_spot.py` | `logs/blind_spot.log` |
| §8 | the nested family: index `9^(J-2)`, units `6(2J+1)` | `scripts/finer_lattices.py` | `logs/finer_lattices.log` |
| §8 | both filters blind to the whole family `rho*u` | `scripts/rho_unit_family.py` | run it |
| §1 | the five known rotations, and that we kill none | `scripts/voronov_rotations.py` | run it |

## The graphs

`graphs/` holds the coordinates, one point per line, in the exact field the
rotation needs — each line is a pair of algebraic numbers as integer coefficient
vectors over that field's basis with a common denominator, not floats.

| file | rotation | vertices |
|---|---|---|
| `theta4_record_509.pts` | `theta_4` | 509 (Parts' record, minimised) |
| `join16.pts` | `theta_16` | 29113 |
| `join28.pts` | `theta_28` | 156577 |
| `join36.pts` | `theta_36` | 175825 |
| `join64_3.pts` | `alpha_64/3` | 187225 |
| `join64_9.pts` | `alpha_64/9` | 5809 |
| `join256_9.pts` | `alpha_256/9` | 158257 |

Minimised graphs with their edge sets, and the vertex-criticality record, are in
`results/alpha64_9/` (1408 vertices, 7013 edges), `results/theta16/` (2901) and
`results/asym/` (889). The last is not a paper claim and does not beat anything:
it is a `theta_4` graph built from an *asymmetric* unit-vector family -- 30
vectors for the large half, 18 for the small, as the record itself uses -- in a
different basin from Parts'. `results/asym/README.md` is its own write-up,
including a reading of four agreeing greedy searches that turned out to be wrong.

Every `.pts` begins with a line naming its field, e.g. `# primes 3 11 7`, and
`hn.io.load_points` refuses to read it under any other. This matters more than it
looks: the same file read under `(3, 7, 11)` instead of `(3, 11, 7)` yields a
different, sparser graph that IS 4-colourable, with no error and no warning.

**A warning that costs real time if ignored:** a `.pts` file must be read in the
field it was written for. `hn.field.set_primes` chooses that field, and the wrong
choice silently finds too few unit edges and reports a graph 4-colourable that is
not. Each script sets its own; if you write your own reader, set it from the
rotation.

## Reading a result back

`scripts/reverify_join.py A` re-verifies `theta_A` from the coordinates in a
fresh process: field rebuilt from the rotation, points reloaded, every edge
recomputed from the coordinates and re-tested exactly, non-4-colourability
re-proved with nothing carried over.

## What the logs are

`logs/` holds the run that produced the numbers in the current PDF, including
`build.log` for both papers. They are transcripts, not certificates: the scripts
are the check, and they re-run.

## Status of each claim

Everything numbered in the paper is proved there and checked here: Theorems 1, 4,
16 and 19-21, Corollaries 2, 14 and 17, Propositions 3, 5, 8, 18, 22 and 23.
Nothing in the current draft is stated as a conjecture.

**The shell criterion changed status.** In the previous version of this archive it
was labelled a conjecture -- local conditions proved necessary, integral sufficiency
unproved, checked exhaustively only to `a <= 400`. It is now **Theorem 18**, and
proved: `3R` is the maximal order of `V = Q(sqrt33, i sqrt3)` (Proposition 8), so
`|z|^2` is the relative norm `N_{V/F}`, `h(F) = h(V) = 1`, and `F`'s totally
positive fundamental unit is a relative norm -- `eta = i(2 sqrt3 - sqrt11)` has
`N(eta) = 23 - 4 sqrt33`. Hasse's norm theorem then upgrades the local conditions
to global, with no gap. The `a <= 400` sweep is corroboration now, not the
evidence. `scripts/moser_is_ov.py` checks every ingredient; its PARI half needs
`cypari`, the rest is standard library.
