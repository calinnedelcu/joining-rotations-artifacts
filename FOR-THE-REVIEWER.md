# What is supplied, and what is already known to be open

*Companion note to* **Which rotations join two Moser lattices?** *(39 pages).*
Read this first if you would rather not spend the first hour rediscovering what we
already know.

## What you have

| | |
|---|---|
| the manuscript | `joining-rotations.pdf`, 39 pages, 0 unresolved references |
| the artifacts | <https://github.com/calinnedelcu/joining-rotations-artifacts>, tag `v1.0` |

The repository is public; nothing else needs to be sent. Its `README.md` opens
with a coverage table saying, claim by claim, whether the archive settles it and
how. `PROVENANCE.md` names the four files that come from Parts' published work
rather than from these scripts.

Cheapest useful check: `scripts/audit_numbers.py` — standard library only, no
solver, about three minutes, 97 checks, re-derives the paper's numbers from the
definitions. Then `scripts/check_periodic.py`, which validates the eleven
periodic-kill witnesses from their JSON alone, importing no project code.
`bash scripts/verify_all.sh` runs the whole table; budget three hours.

## What we already know is open, so you need not find it

- **No proof certificates.** Non-4-colourability is re-established by re-running a
  solver, not by checking a DRAT/LRAT proof. For the four largest unions
  (156577–187225 vertices) that is a real weakness and the paper says so. It is
  the one thing a referee cannot check in an afternoon.
- **χ = 5 is not established for any full union.** The scripts prove χ ≥ 5.
  Lemma 19 gives χ = 5 for a minimal induced subjoin of any of them, and the
  1408-vertex graph is vertex-critical, so it has χ = 5 outright. The full unions
  do not.
- **The 1920 five-edge sets** solve a restricted hitting-set problem: they defeat
  every pairing of homomorphism colourings. Whether any is the interface of an
  actual 5-chromatic graph is open, and the abstract says so.
- **No archival DOI, no licence yet.** Zenodo has not been linked to the
  repository. Both are oversights we intend to fix, not positions.
- **The title is wider than the result.** What is proved is a divisibility
  obstruction plus an occupancy criterion, not a classification of joining
  rotations. Section 10 says so; a previous reviewer suggested retitling and we
  have not decided.
- **Rank-4 spindles, empty-shell survivors, and non-spindle rotations** are
  untouched. Section 10 lists them.
- **Suite status:** 29 of 30 entries pass from a clean extraction of the archive.
  The last, `lambda_sweep`, is a rerun in progress under a larger cap; it passed
  in earlier full runs and its script has not changed.

## Errors earlier reviewers found, and where the fix landed

Not a defence — a map, so you can check the repairs rather than the originals.

| found | where it is now |
|---|---|
| Theorem 1 stated without the rank-8 hypothesis | Theorem 1, Corollary 2, the abstract and Section 10 all carry it |
| the shell criterion was a conjecture | Theorem 16, proved via Hasse's norm theorem once `3R = O_V` was noticed |
| `h(F) = h(V) = 1` asserted | both proved by Minkowski; `h(V) = 1` needs the generator `w = (1 + i(2√3+√11))/2` of the prime above 3 |
| `a = 64` called open | Lemma 18: chaining Parts' gadget builds it, on at most 2197 vertices |
| "1408 is the smallest known" | withdrawn; doubling Parts' 367-vertex gadget gives 733 at the same rotation |
| six new rotations claimed | three are new; all three rational ones follow from Parts' gadgets |
| the eleven exclusions had no witnesses | all eleven in `results/periodic/`, with their moduli, plus an independent checker |
| Proposition 8 was "a finite check on a basis" | the basis, the trace matrix, and a non-circular discriminant argument |
| Step 3 hid five cases under "the same computation" | one uniform argument: the coefficient pairs are all 4 mod 8 |
| the six cyclic colourings were unreported | all twelve tuples printed, and re-derived by the audit |
| "exactly 5-chromatic" was asserted | Lemma 19, stated once and covering every construction |
| "no search went into them" was ambiguous | now says what it means, and where the depth and radius come from |

## The three questions we expect, and our answers

1. *Can I check the four largest graphs without spending a day?* No — not without
   certificates. That is the gap, and we are not hiding it.
2. *What is genuinely new?* The arithmetic: `3R = O_V`, the two colourings as
   prime reductions, shell occupancy as a norm condition, and the divisibility
   law. Among the constructions, three integer spindles, on the search Section 6
   describes.
3. *Is the framing right?* Probably not yet. See the title point above.

---

*Archive pinned at commit `5057ce45ba1e`. A tag can be moved; a commit cannot.*
