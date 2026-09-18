# What is supplied, and what is already known to be open

*Companion note to* **Which rotations join two Moser lattices?** *(38 pages).*
Read this first if you would rather not spend the first hour rediscovering things
we already know.

## What you have

| | |
|---|---|
| the manuscript | `joining-rotations.pdf`, 38 pages, 0 unresolved references |
| the artifacts | <https://github.com/calinnedelcu/joining-rotations-artifacts>, tag `v1.0`, public — also attached as a tarball |

The archive's `README.md` opens with a coverage table: for each claim, whether
this archive settles it, and how. `PROVENANCE.md` names the four files that come
from Parts' published work rather than from these scripts.

The cheapest useful check is `scripts/audit_numbers.py` — standard library only,
no solver, about three minutes, 97 checks. `bash scripts/verify_all.sh` runs the
whole table; budget three hours and expect two entries to take an hour each.

## What we already know is open, so you need not find it

- **No proof certificates.** Non-4-colourability is re-established by re-running a
  solver, not by checking a DRAT/LRAT proof. For the four largest unions
  (156577–187225 vertices) that is a real weakness and we state it as one.
- **χ = 5 is not established for any full union.** The scripts prove χ ≥ 5.
  Lemma 19 gives χ = 5 for a minimal induced subjoin of any of them, and the
  1408-vertex graph is vertex-critical, so it has χ = 5 outright. The full unions
  do not.
- **h(V) = 1** is a computation, not an argument in the paper. It is checked
  through PARI in `scripts/moser_is_ov.py`, and it enters at exactly one step: from
  an ideal to a generator. h(F) = 1 *is* proved, by Minkowski, in two lines.
- **The 1920 five-edge sets** solve a restricted hitting-set problem — they defeat
  every pairing of homomorphism colourings. Whether any is the interface of an
  actual 5-chromatic graph is open, and the abstract says so.
- **No archival DOI yet.** Zenodo has not been linked to the repository.
- **No licence yet**, so the default applies. This is an oversight we intend to
  fix, not a position.
- **The title promises more than the paper delivers.** What is proved is a
  divisibility obstruction plus an occupancy criterion, not a classification of
  joining rotations; Section 10 says so explicitly, and a previous reviewer
  suggested retitling. We have not decided.
- **Rank-4 spindles, empty-shell survivors, and non-spindle rotations** are
  untouched. Section 10 lists them.

## Errors earlier reviewers found, and where the fix landed

Not a defence — a map, so you can check the repairs rather than the originals.

| found | where it is now |
|---|---|
| Theorem 1 was stated without the rank-8 hypothesis | Theorem 1, Corollary 2, the abstract, and Section 10 all carry it |
| the shell criterion was a conjecture | Theorem 16, proved via Hasse's norm theorem once `3R = O_V` was noticed |
| `a = 64` was called open | Lemma 18: chaining Parts' gadget builds it, on at most 2197 vertices |
| "1408 is the smallest known" | withdrawn; doubling Parts' 367-vertex gadget gives 733 at the same rotation |
| six new rotations claimed | three are new; all three rational ones follow from Parts' gadgets |
| the eleven exclusions had no witnesses | all eleven in `results/periodic/`, with their moduli, plus an independent checker |
| Proposition 8 was "a finite check on a basis" | the basis, the trace matrix and a non-circular discriminant argument |
| Step 3 hid five cases under "the same computation" | one uniform argument: the coefficient pairs are all 4 mod 8 |

## The three questions we expect and cannot fully answer

1. *Can I check the four largest graphs without spending a day?* No — not without
   certificates. That is the gap.
2. *What is genuinely new?* The arithmetic: `3R = O_V`, the two colourings as prime
   reductions, shell occupancy as a norm condition, and the divisibility law. Among
   the constructions, three integer spindles, on the search Section 6 describes.
3. *Is the framing right?* Probably not yet. See the title point above.
