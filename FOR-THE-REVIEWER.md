# What is supplied, and what is already known to be open

*Companion note to* **A divisibility obstruction for joining two Moser lattices**
*(42 pages).* Read this first if you would rather not spend the first hour
rediscovering what we already know.

## What you have

| | |
|---|---|
| the manuscript | `joining-rotations.pdf`, 42 pages, 0 unresolved references |
| the artifacts | <https://github.com/calinnedelcu/joining-rotations-artifacts>, release `v1.0`, public |

The repository is public; nothing else needs to be sent. Its `README.md` opens
with a coverage table saying, claim by claim, whether the archive settles it and
how. `PROVENANCE.md` names the four files that come from Parts' published work
rather than from these scripts.

**The cheapest useful checks, in order.**

1. `scripts/audit_numbers.py` — standard library only, no solver, about three
   minutes, 97 checks, re-derives the paper's numbers from the definitions.
2. `scripts/check_periodic.py` — validates the eleven periodic-kill witnesses
   from their JSON alone, importing no project code. Seconds.
3. `scripts/check_drat.sh` — verifies the one proof certificate we have. Fetch
   `drat-trim` yourself (the script deliberately does not vendor it) and expect
   `s VERIFIED` in about two minutes.
4. `bash scripts/verify_all.sh` — the whole table, 33 entries. Budget three hours.

## What we already know is open, so you need not find it

- **The seven constructions of §6 are reported UNSAT, uncertified.** We say this
  in the same paragraph as the table, not only in a later section.
  Non-4-colourability is re-established by running CaDiCaL again, not by checking
  a proof. For the four largest unions (156577–187225 vertices) that is a real
  weakness and it is the one thing a referee cannot check in an afternoon.
  We do ship one certificate, and it is **not** for our constructions: a DRAT
  proof of Parts' 509-vertex record, 3101213 lines, which `drat-trim` verifies —
  `s VERIFIED`, 126 s, 67841290 resolution steps. Theorems 21–23 need no
  certificate at all; their hitting-set step is an exhaustive search over 235
  patterns and the paper says so.
- **χ = 5 is not established for any full union.** The scripts prove χ ≥ 5.
  Lemma 19 gives χ = 5 for a minimal induced subjoin of any of them, and the
  1408-vertex graph is vertex-critical, so it has χ = 5 outright. The full unions
  do not.
- **The 1920 five-edge sets** solve a restricted hitting-set problem: they defeat
  every pairing of homomorphism colourings. Whether any is the interface of an
  actual 5-chromatic graph is open, and the abstract says so.
- **Three empty-shell rotations are open.** Of the nine multiples of 4 below 100
  with an empty shell, six carry a homomorphism 4-colouring and are dead; `a = 24,
  72, 88` carry none and survive the periodic filter at modulus 4, proved. They
  are candidates with no construction known, and they are not counted among the
  sixteen because the law never admitted them.
- **No archival DOI, no licence yet.** Zenodo has not been linked to the
  repository. Both are oversights we intend to fix, not positions.
- **Rank-4 spindles, the finer lattices, and non-spindle rotations** are
  untouched. §10 lists them. The record of 509 is not improved.

## Errors earlier rounds found, and where the fix landed

Not a defence — a map, so you can check the repairs rather than the originals.

| found | where it is now |
|---|---|
| Theorem 1 stated without the rank-8 hypothesis | Theorem 1, Corollary 2, the abstract and §10 all carry it |
| the shell criterion was a conjecture | Theorem 16, proved via Hasse's norm theorem once `3R = O_V` was noticed |
| `h(F) = h(V) = 1` asserted | both proved by Minkowski; `h(V) = 1` needs the generator `w = (1 + i(2√3+√11))/2` of the prime above 3 |
| `a = 64` called open | Lemma 18: chaining Parts' gadget builds it, on at most 2197 vertices |
| "1408 is the smallest known" | withdrawn; doubling Parts' 367-vertex gadget gives 733 at the same rotation |
| six new rotations claimed | three are new; all three rational ones follow from Parts' gadgets |
| the eleven exclusions had no witnesses | all eleven in `results/periodic/`, with their moduli, plus an independent checker |
| Proposition 8 was "a finite check on a basis" | the basis, the trace matrix, and a non-circular discriminant argument |
| Step 3 hid five cases under "the same computation" | one uniform argument: the coefficient pairs are all 4 mod 8 |
| the six cyclic colourings were unreported | all twelve tuples printed, and re-derived by the audit |
| §5 imported a "geometric" hypothesis it could not justify | the Klein group's exponent gives `2R ⊆ ker` with no geometry; both exclusions of an order-2 image written out |
| Theorems 21–23 had no proof paragraph | a joint proof naming the objects, the scripts, and the limit of the claim |
| the empty-shell multiples of 4 were unaccounted | all nine settled; three are open and named |
| the audit read one block instead of deriving it | `empty_shell_status.py` derives all nine from the definitions |
| "no search went into them" was ambiguous | says what it means, and where the depth and radius come from |
| the title promised a classification | retitled to the obstruction |

## The three questions we expect, and our answers

1. *Can I check the four largest graphs without spending a day?* No — not without
   certificates for them. That is the gap and we are not hiding it.
2. *What is genuinely new?* The arithmetic: `3R = O_V`, the two colourings as
   prime reductions, shell occupancy as a norm condition in closed form, and the
   divisibility law. Among the constructions, three integer spindles, on the
   search §6 describes.
3. *Is the framing right now?* The title and the front matter were rewritten to
   lead with the obstruction rather than the table of seven. If it is still wrong
   we would rather be told than guess again.

---

*The archive's `v1.0` release is the snapshot this note describes.*
