# Response to the second-round report

The Area Chair's closing sentence was that the hard fixes were done properly and
the easy ones were agreed to and not done, and that this was the whole of what was
keeping the paper out. That was accurate, and it is the criticism we took most
seriously. This revision does the list.

We have also stopped writing "accepted without argument" and then not acting. Where
we still disagree, we say so and act anyway; where we cannot act, we say who has
to.

---

## The ten items, in the order the report put them

**1. Rewrite the abstract; add a Results block on p. 1.** Done. The abstract now
opens with the obstruction deciding every rational `a`, then `3R = O_V` as its
engine, then shell occupancy in closed form with the criterion stated, then
density zero — and only then the constructions, with Lemma 18's infinite family
named rather than left as a subordinate clause. Its last sentence is that the
record of 509 is untouched. A **What is proved here** block on p. 1 lists the six
results in order of weight, each with the section that proves it, and points at
§10 for what is not settled.

**2. Retitle.** Done: *A divisibility obstruction for joining two Moser lattices*.
The Area Chair is right that an editor cannot title a paper whose scope only we
know, and right that we had deferred a decision already made for us.

**3. Certify the gadget property and the three smallest unions; label the four
largest honestly in the table.** Half done, and the half that is done is not the
half that was asked for.

The labelling is in place: every one of the seven rows now carries **reported
UNSAT, uncertified** in the same paragraph as the table, together with the solver,
its version and the machine — CaDiCaL 1.9.5 through `python-sat` 1.9.dev15, Python
3.11.15, Apple M5, 32 GB.

The certification is not. What we found instead, and had not looked for, is that
this project has held a DRAT proof of **Parts' 509-vertex record** since 15
September with no record of it ever being checked. It checks: `drat-trim` reports
`s VERIFIED` in 126 s, 915005 of 1569693 lemmas in core, 67841290 resolution
steps. `proofs/README.md` records the instance, the checker's sha256, the verdict
and the log; `scripts/check_drat.sh` reproduces it and deliberately does not
vendor the checker, since a checker obtained from the people whose proof you are
checking is not a check. The proof is a release asset, 85 MB being past GitHub's
file-size threshold.

That does not discharge the directive — it is Parts' graph, not ours. It does mean
the infrastructure now exists and has been exercised on a real three-million-line
proof, and that "no proof certificates are shipped" was a statement about what we
had packaged rather than about what the project had.

**4. Say §8's hitting-set computation is exhaustive, not a solver call.** Done.
The proof of Theorems 21–23 now says the step is an exhaustive search over the 235
patterns, that the search space is small enough to redo directly, and that no part
of those three theorems rests on an unsatisfiability verdict needing a
certificate. The panel's reconstruction established this before we wrote it and
our own wording had obscured it.

**5. Close the `audit_numbers.py` hole.** Done. `scripts/empty_shell_status.py`
derives the homomorphism-colouring status of all nine empty-shell multiples of 4
from the definitions, running filter 1 on each joint lattice directly; the audit
reads nothing and says so as it runs. The script is in the suite.

**6. Run the §7 periodic filter on `a = 24, 68, 72, 88, 96`.** Done, and it
changed the answer. Of the nine empty-shell multiples of 4 below 100, **six die**
— `8, 32, 40, 56, 68, 96` each carry a homomorphism 4-colouring, 96 of them —
and **three survive both filters**: `a = 24, 72, 88` admit none, and the periodic
filter proves at modulus 4 that no pair of 4-periodic colourings kills them, over
the 66 residue pairs occurring in each. Those three are candidates with no
construction known.

The reason we could not see them was a refusal in our own code:
`join_filter_residues.py` exited at an empty shell saying "the rotation has
nothing to act on, and the question does not arise". That is wrong. An empty shell
means no point is paired with its own image, so the spindle mechanism is absent,
but `Λ_a` still has rank 8 and 72 unit vectors whose cross edges pair distinct
points. The filter is valid there, now runs, and produced the three.

So Reviewer 2 reached the right neighbourhood by a route we still think misreads
the sentence, and there was something in it. We record both halves of that.

**7. Name the solver, version, machine and timings.** Done, in §6 where a reader
takes the claim. Timings are in the archive's logs.

**8. State the novelty search protocol; write to Parts, de Grey and Voronov.**
The protocol is in §6: which sources, which threads, which listings, and the
September 2026 cutoff, phrased as a statement about our search rather than a
priority claim. The correspondence has not been undertaken and is the authors'
to do.

**9. DOI, affiliation, repository licence, licence status of Parts' four files.**
Not done. `[ARCHIVAL DOI TO BE SUPPLIED]` and `[AFFILIATION TO BE SUPPLIED]` are
the only two placeholders left in the manuscript. Zenodo requires authorising the
GitHub account in a browser, which is not something the revision process can do.
`PROVENANCE.md` states the licence position for Parts' four files as it currently
stands, which is that none has been chosen.

**10. The three cheapest should-fix items.** All three done, and the report was
right about each. Proposition 8's chart point is `w/3 = (2,0,4,2)`; `(6,0,12,6)`
verifies only `w ∈ R`, and the paper now says which does which. Haugland's
`0.42363201413287` is `arg ρ · 42/2π`, the argument in units of the 42-fold step,
with `arg ρ = 3.63113154971030°`; read as radians or degrees it would say §9's
rotation is the wrong one. Lemma 13's odd-denominator hypothesis holds
automatically in the only case Corollary 14 uses, so the forward reference to
Theorem 16 is no longer load-bearing.

We also removed the density comparison that put a measured density and a
truncated product bound side by side as though one computed the other.

## On Ruling 1, whether M1 was a misreading

We accept the ruling and will not relitigate it. Corollary 17 does separate "the
law admits it" from "its shell is non-empty", and our defence did not survive the
paper's own vocabulary. The Area Chair's procedural note is the more useful part
and we have taken it: a response is stronger when it separates disagreement from
repair and leads with the repair. This one does.

## What we did not change

Remarks 6 and 27 and Figure 7's caption stay in the main text. The editor reads
them as evidence for weighting uncertified computation down; that inference is
fair and we accept it, and we would still rather a reader see which of our own
assertions turned out to be artefacts of a sweep, and how.

## What remains open, stated plainly

Certificates for §6's seven unions and for the gadget property behind Lemma 18.
The DOI, the affiliation and the licence. The correspondence. Three empty-shell
rotations with no construction. And the reach: rank-4 spindles, the finer
lattices, the `{ρu}` family, and the record itself.
