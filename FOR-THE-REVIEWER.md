# What is supplied, and what is already known to be open

*Companion note to* **A divisibility obstruction for joining two Moser lattices**
*(25 pages).* Read this first if you would rather not spend the first hour
rediscovering what we already know.

## What you have

| | |
|---|---|
| the manuscript | `joining-rotations.pdf`, 25 pages; `scripts/check_paper.sh` greps the rendered text for `??` and for unfilled placeholders |
| the artifacts | <https://github.com/calinnedelcu/joining-rotations-artifacts>, public; archived at Zenodo, DOI [10.5281/zenodo.22855504](https://doi.org/10.5281/zenodo.22855504), which resolves to the deposit matching this manuscript. The paper's code and data are those of commit `cb7880173badcfd33201ba378ee1f2ffb5b991a2`; the commits after it touch documentation and the manuscript only |
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
   witnesses. Seconds. **Read its contract before you rely on it.** A witness
   names a rotation, a modulus, the rank, the residue classes of the lattice's
   unit vectors, two colourings of `Lambda/m*Lambda`, and the residue pairs that
   occur among cross pairs; the validator checks that each colouring is proper
   — no two residues a unit step apart share a colour — that they agree at the
   shared origin, and that they disagree on every listed pair.

   Until this release it did **not** check properness, and could not: the unit
   steps were not in the file. A referee corrupted a witness into a
   monochromatic unit edge and it still printed `ok`. The producer had always
   asserted properness at generation, so no shipped verdict was wrong, but the
   standalone checker was not the checker described here. The witnesses now
   carry their unit steps, the check is real, and
   `python3 scripts/check_periodic.py --selftest` corrupts a copy in front of
   you and shows it refused. It still does **not** check that the listed pairs
   are all the pairs that occur — re-deriving that needs the lattice, so it is the producer's
   enumeration, and the script's own header says so. Completeness therefore
   rests on `scripts/join_filter_residues.py`, which enumerates the occurring
   pairs exactly, with no ball and no radius, from the joint lattice's unit
   vectors. Until this release the one-command suite ran that producer for two
   of the eleven; it now runs all eleven, at `m = 8` for `a = 48` and `80`,
   about three minutes in total. Regenerating them returns the shipped JSON
   byte for byte.

   A witness that carries no unit steps is now refused rather than passed, so
   an unverifiable file cannot be mistaken for a verified one.

   The independent corroboration, if you would rather not take either script's
   word: the same two rotations were also run directly on a ball holding the
   whole shell — `theta_12`, **0** monochromatic edges out of 867054;
   `theta_20`, **0** out of 2076192. That is a different method reaching the
   same verdict, and it is in `results/BALL-FREE-TYPE-M.md`.
4. **`scripts/check_drat.sh`** — verifies all eight proof certificates. Fetch
   `drat-trim` yourself (the script deliberately does not vendor it: a checker
   you got from the people whose proof you are checking is not a check) and
   expect eight `s VERIFIED` in about ten minutes. We ran exactly this from a
   clean `git clone` of the public archive, on a bare `python3` with no `pysat`,
   with `drat-trim` built from source on the spot: eight of eight.
5. **`bash scripts/verify_all.sh`** — the whole table, run in parallel (`JOBS`,
   default 6). A little over an hour. Our last full run: **35 of 35 PASS**,
   0 FAIL, 0 TIMEOUT; the 36th entry, `check_notes`, was added after that run
   and passes on its own.

Nothing in the checking path above needs a SAT solver, `pysat`, or a
virtualenv — that is the six checks listed, and it is tested by
`check_claims.py`, which runs each of them on a bare interpreter. Regenerating the periodic pair lists is a different thing and does need
`python-sat`: `join_filter_residues.py` asks one SAT instance per rotation.
So validating the shipped witnesses is dependency-free; establishing that
their pair lists are complete is not. A
solver is needed only to *regenerate* a proof or rebuild a construction.

## What we already know is open, so you need not find it

- **The record of 509 is untouched**, and nothing here brings it closer. We say
  so in the abstract and again in Section 8.
- **The law is silent exactly where the constructions live.** It kills three
  rational `a` in four; Theorem 1's own second half proves that at `4 | a` with
  an occupied shell *no* homomorphism colouring exists, so the method has
  nothing further to say there. Section 1 states this in one paragraph rather
  than leaving it to be assembled.
- **It is silent outside the spindle family altogether.** Four of the five
  previously known working rotations have irrational cosine; neither the law nor
  the periodic refinement applies, and Section 8 says both tools are blind there.
- **`chi = 5` is not established for any full union.** What is certified is
  non-4-colourability, i.e. `chi >= 5`. Lemma 21 gives a 5-chromatic induced
  subjoin, with no size bound better than the full union. The table column says
  `chi >= 5`.
- **The interface bound at `theta_4` is not in this paper** — it is left for a
  companion, and `scripts/interface_matchings.py` in the archive computes it.
  Its negative is weak: Parts' record carries 18 cross edges, not the minimum 5,
  and its interface is disjoint from all 1920 minimum ones. We know of no graph
  realising any of them and have run no systematic search over the halves.
- **Three of the seven constructions are not ours in substance.** Parts'
  inventory (`data/parts/graphs.txt`) lists two monochromatic-pair gadgets: 367
  vertices with terminals `8/3` apart, and 421 vertices with terminals `8/sqrt3`
  apart. Lemma 20 sends the first to `a = 64n^2/9`, giving `theta_64/9` and
  `theta_256/9` at `n = 1, 2`, and the second to `a = 64n^2/3`, giving
  `theta_64/3` at `n = 1`. All three follow without any of this paper's
  machinery. A referee objected that the manuscript named only one gadget and so
  could not reach `64/3`; the objection was right about the manuscript, which
  now names both, and we briefly made it worse by moving `theta_64/3` into our
  own column before checking `graphs.txt`. After subtracting the three and
  `theta_4` (the record), the new constructive content is `theta_16`,
  `theta_28`, `theta_36`.
- **Priority for those three is a statement about our search**, not a proof. We
  searched the obvious places to September 2026. One absence we can explain
  rather than report: the one published enumeration on this lattice clips its
  point set to radius 2, and only `theta_4` of the seven has a shell reaching so
  far — which is why `theta_4` is the one it found.
- **A referee sent us to a preprint and half of it stuck.** Two reviewers named
  Gibbs, *Elements of the Moser Spindle Ring* (May 2018), as absent from our
  bibliography and a likely antecedent for Proposition 8. We read it. Its
  Theorem 1 gives the Moser ring as `(a + ib√3 + ic√11 + d√33)/(4·3^k)` under
  `a ≡ b ≡ c ≡ d (mod 2)` and `a + b + c − d ≡ 0 (mod 4)`; at `k = 0`, scaled by
  three, that is our chart. The two second congruences differ by `2(a−d)`, which
  the parity condition kills modulo 4 — checked over the 512 quadruples mod 8
  that satisfy it, zero disagreements. (Over all 4096, without the parity
  condition, 1024 disagree; the condition is what makes them the same.) So the chart is his, it is cited now, and we no longer
  imply otherwise. Proposition 8 is not his: his ring inverts 3, so it is not a
  finitely generated `Z`-module and not an order in `V`, and nothing there
  identifies the maximal order or proves maximality. Please do check this
  yourself rather than take our reading of someone else's preprint.
- **The same criterion on Haugland's lattice** settles `theta_2` and `theta_7`
  as survivors and leaves `N = 9` open at rank 24; those computations are
  `scripts/hept_*.py` in the archive, and are described in a companion paper.

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
   (Theorem 18) are new. We have checked what can be checked: the six papers the
   manuscript lists as working in or on this lattice — Dúcz `arXiv:2606.12325`,
   Parts `arXiv:2010.12665`, Voronov et al. `arXiv:2106.11824`, Haugland
   `arXiv:2608.04542`, Engel et al. `arXiv:2406.15317`, Ruhland
   `arXiv:2410.16172`, and also `arXiv:1908.03880` — contain, in their full
   texts, **no occurrence** of "maximal order", "ring of integers", "prime
   ideal" or "number field". The classical spectrum here is the triangular
   lattice's (the Loeschian numbers); we found no closed-form spectrum for `R`,
   which is rank 4.

   One precedent we did find, and cite in the paper: David Speyer's comment of
   3 May 2018 on the Polymath16 third thread. It gives the
   Moser ring as the elements of `Q(sqrt-3, sqrt-11)` integral over `Z[1/3]`,
   names the subring `Z[(1+sqrt33)/2]` — the ring Theorem 9 works over — and
   takes the norm `N(u) = u * conj(u)` from one to the other, colouring by the
   elements of norm 1. So the field, that ring and the norm map are not ours.
   What Proposition 8 adds is that `3R` is the **maximal** order of `V` rather
   than some order inside it, and what Theorem 18 adds is the closed form for
   occupancy.

   That is still evidence and not proof: this literature is partly distributed
   across blog comments and data files — Speyer's is one — and a negative over
   it cannot be certified. If you know of another precedent we would want to
   hear it.
2. Whether the narrow-class-field framing of Sections 4 and 6 can be pushed
   further than we push it — we use it to explain, not to prove. One candidate:
   since "obstructed" is "`p` lies in the non-principal genus of discriminant
   33", Theorem 18's sufficiency might be rederivable as a statement about which
   rationals are norms from the genus field, removing the separate appeal to
   `h(V) = 1`. We have not worked it through.
3. Any 5-chromatic `L ∪ theta_4(S)` realising one of the 1920 minimum
   interfaces `scripts/interface_matchings.py` enumerates. We could not build one and do not
   know whether one exists.
