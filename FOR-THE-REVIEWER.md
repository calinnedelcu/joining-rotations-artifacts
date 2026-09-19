# What is supplied, and what is already known to be open

*Companion note to* **A divisibility obstruction for joining two Moser lattices**
*(46 pages).* Read this first if you would rather not spend the first hour
rediscovering what we already know.

## What you have

| | |
|---|---|
| the manuscript | `joining-rotations.pdf`, 46 pages; `scripts/check_paper.sh` greps the rendered text for `??` and for unfilled placeholders |
| the artifacts | <https://github.com/calinnedelcu/joining-rotations-artifacts>, public, release `v1.1`, commit `a40f6fdf5dac` |
| a transcript | `VERIFICATION.md` — every check we ran, with its raw output |

The repository is public; nothing else needs to be sent. Its `README.md` opens
with a coverage table saying, claim by claim, whether the archive settles it and
how. `PROVENANCE.md` names the four files that come from Parts' published work
rather than from these scripts. `LICENSES.md` gives the split: MIT for the code,
CC BY 4.0 for the paper, the certificates and the data.

## The cheapest useful checks, in order

1. **`scripts/audit_numbers.py`** — 97 checks, about three minutes, standard
   library only. Re-derives the paper's numbers from the definitions and shares
   no code with the rest of the repository.
2. **`scripts/check_emptyshell.py`** — validates the nine empty-shell verdicts of
   Section 7 from their JSON alone, computing lengths from the multiquadratic
   field's multiplication table and importing nothing from this project. Seconds.
3. **`scripts/check_periodic.py`** — the same for the eleven periodic-kill
   witnesses. Seconds.
4. **`scripts/check_drat.sh`** — verifies all eight proof certificates. Fetch
   `drat-trim` yourself (the script deliberately does not vendor it: a checker
   you got from the people whose proof you are checking is not a check) and
   expect eight `s VERIFIED` in about ten minutes. We ran exactly this from a
   clean `git clone` of the public archive, on a bare `python3` with no `pysat`,
   with `drat-trim` built from source on the spot: eight of eight.
5. **`bash scripts/verify_all.sh`** — the whole table, run in parallel (`JOBS`,
   default 6). A little over an hour. Our last full run: **35 of 35 PASS**,
   0 FAIL, 0 TIMEOUT.

Nothing in the checking path needs a SAT solver, `pysat`, or a virtualenv. A
solver is needed only to *regenerate* a proof or rebuild a construction.

## What we already know is open, so you need not find it

- **The record of 509 is untouched**, and nothing here brings it closer. We say
  so in the abstract and again in Section 10.
- **The law is silent exactly where the constructions live.** It kills three
  rational `a` in four; Theorem 1's own second half proves that at `4 | a` with
  an occupied shell *no* homomorphism colouring exists, so the method has
  nothing further to say there. Section 1 states this in one paragraph rather
  than leaving it to be assembled.
- **It is silent outside the spindle family altogether.** Four of the five
  previously known working rotations have irrational cosine; neither the law nor
  the periodic refinement applies, and Section 10 says both tools are blind there.
- **`chi = 5` is not established for any full union.** What is certified is
  non-4-colourability, i.e. `chi >= 5`. Lemma 19 gives a 5-chromatic induced
  subjoin, with no size bound better than the full union. The table column says
  `chi >= 5`.
- **The 1920 five-edge interfaces may all be unrealisable.** Parts' record
  carries 18 cross edges, not 5, and its interface is disjoint from all 1920. The
  bound is a floor for a relaxation that the one known instance exceeds. We
  looked for a realising graph on a space of exactly `30 × 8 × 8` and found none.
- **Three of the seven constructions are not ours in substance.** The rational
  spindles follow from Parts' published gadgets without any of this paper's
  machinery, and we say so. After subtracting those and `theta_4` (the record),
  the new constructive content is `theta_16`, `theta_28`, `theta_36`.
- **Priority for those three is a statement about our search**, not a proof. We
  searched the obvious places to September 2026. One absence we can explain
  rather than report: the one published enumeration on this lattice clips its
  point set to radius 2, and only `theta_4` of the seven has a shell reaching so
  far — which is why `theta_4` is the one it found.
- **Section 9 is thin relative to its billing.** `N = 7` is settled (it
  survives, with no half-unit vector, so the search deciding it is the
  informative kind); `N = 9` is open and is rank 24.

## Where we have been wrong, in case it bears on how you read the rest

The paper discloses its own corrected errors, and they share a shape worth
naming: **a check whose domain excluded the thing it was meant to find.**

- A sweep skipped rotations whose shell is empty, because the shell was the only
  known source of half-unit vectors. `Lambda_24` has twelve half-unit vectors
  and an empty shell, so the code could not see the counterexample its own
  domain excluded. This makes Theorem 1's shell hypothesis sufficient but not
  necessary, explains three survivors in Section 7, and corrected a census from
  sixteen to nineteen.
- A filter declined to run at an empty shell on the ground that the question did
  not arise. It does arise; three genuine candidates were behind the refusal.
- A draft asserted "0 unresolved references" while containing two `??`. The
  assertion had been made by grepping the TeX engine's `.log` for "undefined" —
  and the engine writes no `.log` unless asked, so the grep matched nothing and
  the absence read as success. `scripts/check_paper.sh` now tests the rendered
  PDF, which is the only honest test.
- Four of the eight certificates were unverifiable from a clean clone: the large
  CNFs had been left out as build products, and the checker needs both halves.
  Found by cloning the public archive and doing what a referee would do.

If you are hunting for what else might be wrong, that is our own best guess at
the class of defect to look for.

## What we would most value

1. Whether the identification `3R = O_V` and the shell classification
   (Theorem 16) are new. We believe so and have not found them, but this
   literature is partly distributed across blog comments and data files.
2. Whether the narrow-class-field framing of Sections 4 and 6 can be pushed
   further than we push it — we use it to explain, not to prove. One candidate:
   since "obstructed" is "`p` lies in the non-principal genus of discriminant
   33", Theorem 16's sufficiency might be rederivable as a statement about which
   rationals are norms from the genus field, removing the separate appeal to
   `h(V) = 1`. We have not worked it through.
3. Any 5-chromatic `L ∪ theta_4(S)` realising one of the 1920 interfaces. We
   could not build one and do not know whether one exists.
