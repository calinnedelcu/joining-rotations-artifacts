# What is supplied, and what is already known to be open

*Companion note to* **A divisibility obstruction for joining two Moser lattices**
*(44 pages).* Read this first if you would rather not spend the first hour
rediscovering what we already know. It is written for a fresh reader; a
point-by-point reply to the previous round is in `RESPONSE-ROUND-3.md`.

## What you have

| | |
|---|---|
| the manuscript | `joining-rotations.pdf`, 44 pages; `scripts/check_paper.sh` greps the rendered text for `??` and for unfilled placeholders |
| the artifacts | <https://github.com/calinnedelcu/joining-rotations-artifacts>, public |

The repository is public; nothing else needs to be sent. Its `README.md` opens
with a coverage table saying, claim by claim, whether the archive settles it and
how. `PROVENANCE.md` names the four files that come from Parts' published work
rather than from these scripts. `LICENSES.md` gives the licence split: MIT for
the code, CC BY 4.0 for the paper, the certificates and the data.

## The cheapest useful checks, in order

1. **`scripts/audit_numbers.py`** — standard library only, no solver, about three
   minutes. Re-derives the paper's numbers from the definitions and shares no
   code with the rest of the repository.
2. **`scripts/check_emptyshell.py`** — validates the nine empty-shell verdicts of
   Section 7 from their JSON alone, computing lengths from the multiquadratic
   field's multiplication table and importing nothing from this project. Seconds.
3. **`scripts/check_periodic.py`** — the same for the eleven periodic-kill
   witnesses. Seconds.
4. **`scripts/check_drat.sh`** — verifies all eight proof certificates. Fetch
   `drat-trim` yourself (the script deliberately does not vendor it: a checker
   you got from the people whose proof you are checking is not a check) and
   expect eight `s VERIFIED` in about ten minutes.
5. **`bash scripts/verify_all.sh`** — the whole table, run in parallel
   (`JOBS`, default 6). A little over an hour. Our last full run: **35 of 35
   PASS**, 0 FAIL, 0 TIMEOUT.

## What is proved, in one paragraph

Write `R` for the Moser lattice and `theta_a` for the rotation with
`cos = (2a-1)/(2a)`. If `R + theta_a(R)` has rank 8 and `4` does not divide `a`,
the joint lattice carries a 4-colouring by a group homomorphism, so **no** subset
of it is 5-chromatic at any size. The engine is that `3R` is the maximal order of
`V = Q(sqrt33, i·sqrt3)`; from this the lattice's two integral geometric
4-colourings are reduction modulo the two primes above 2, and shell occupancy
becomes a relative-norm condition with a closed-form answer (Theorem 16). `V` is
the narrow Hilbert class field of `Q(sqrt33)`, which makes the local behaviour
class field theory rather than case work. Against the obstruction: seven joining
spindles, each with a checked DRAT certificate; an infinite chained family at
`a = 64n^2/9`; eleven further exclusions; and an exact interface bound at
`theta_4`.

## What we already know is open, so you need not find it

- **The record of 509 is untouched**, and nothing here brings it closer. We say
  so in the abstract and again in Section 10.
- **The law is silent exactly where the constructions live.** It kills three
  rational `a` in four; Theorem 1's own second half proves that at `4 | a` with
  an occupied shell *no* homomorphism colouring exists, so the method has nothing
  further to say there. Section 1 states this in one paragraph rather than
  leaving it to be assembled.
- **It is silent outside the spindle family altogether.** The four non-spindle
  rotations of [9] have irrational cosine; neither the law nor the periodic
  refinement applies, and Section 10 says both tools are blind there.
- **`chi = 5` is not established for any full union.** What is certified is
  non-4-colourability, i.e. `chi >= 5`. Lemma 19 gives a 5-chromatic induced
  subjoin, with no size bound better than the full union. The table column says
  `chi >= 5`.
- **The 1920 five-edge interfaces may all be unrealisable.** Parts' actual
  record carries 18 cross edges, not 5, and its interface is disjoint from all
  1920. The bound is a floor for a relaxation that the one known instance exceeds.
- **Three of the seven constructions are not ours in substance.** The rational
  spindles follow from Parts' published gadgets without any of this paper's
  machinery, and we say so. After subtracting those and `theta_4`, the new
  constructive content is `theta_16`, `theta_28`, `theta_36`.
- **Priority for those three is a statement about our search**, not a proof. We
  searched the obvious places to September 2026. We can now explain one absence
  positively rather than merely report it: [9]'s first series clips its point set
  to radius 2, and only `theta_4` of the seven has a shell that reaches so far —
  which is why `theta_4` is the one it found.
- **Section 9 is thin relative to its billing.** `N = 7` is now settled — it
  survives, with no half-unit vector, so the search that decides it is the
  informative kind — but `N = 9` is still open and is rank 24.

## Where we were wrong before, in case it bears on how you read the rest

The paper discloses its own corrected errors, and the last round found two more.
The one worth your attention: Section 3 claimed the half-unit vectors of a
spindle "have a closed form", when the shell construction gives only one family
of them. `Lambda_24` has twelve half-unit vectors with an empty shell. This makes
Theorem 1's shell hypothesis sufficient rather than necessary, explains the three
survivors of Section 7, and corrects a census from sixteen to nineteen. Nothing
downstream breaks — Proposition 5 is unconditional and Theorem 1's construction
is untouched — but the cause is instructive: the sweep's domain excluded empty
shells, so the code could not see the counterexample its own domain excluded.

We mention this because it is the second time a filter in this project refused to
run where it had assumed the question did not arise, and the first time it hid
three genuine candidates. If you are looking for where else that pattern might
sit, that is our own best guess at the class of defect to hunt for.

## What we would most value

1. Whether the identification `3R = O_V` and Theorem 16 are new. We believe so
   and have not found them, but this literature is partly distributed across blog
   comments and data files.
2. Whether the narrow-class-field framing of Sections 4 and 6 can be pushed
   further than we push it — we use it to explain, not to prove.
3. Any 5-chromatic `L ∪ theta_4(S)` whose interface is one of the 1920. We could
   not build one and do not know whether one exists.

## One more thing we got wrong, since it bears on the last point

The previous round's companion note asserted "0 unresolved references" and the
manuscript contained two `??`. The assertion was not checked: it was made by
grepping the TeX engine's `.log` for "undefined", and the engine writes no `.log`
unless asked — so the grep matched nothing and we read the absence as success.
The only honest test is on the rendered PDF, and `scripts/check_paper.sh` now
does it. We mention it because the shape is the same as the two defects the paper
already discloses: a check whose domain excluded the thing it was meant to find.
