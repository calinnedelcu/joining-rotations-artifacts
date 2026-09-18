# Response to the review

We are grateful for a report of this quality, and in particular for the
independent recomputation in Appendix V. Being told that an outside pass over the
arithmetic found no numerical error is worth more than any assurance we could
offer ourselves.

Below: one finding we believe rests on a misreading, one place where the panel
found a real error we had missed, and the remaining items with what we did about
each. Section and page numbers refer to the revised manuscript, 40 pages.

---

## 1. The `a = 24` accounting (R2's M1) — we believe this is a misreading, and we
## have rewritten the sentence so that it cannot recur

R2 reads §7's

> For the sixteen integer spindles **it admits** to `a = 100` the account is now
> complete

as claiming that every multiple of 4 below 100 is settled, and concludes that
`a = 24, 68, 72, 88, 96` are undetermined inside a range the paper claims to have
closed.

The antecedent of *it* is the divisibility law, and §6 opens by defining what the
law admits:

> The law leaves `4 | a` with a non-empty shell as the candidates.

So "the sixteen it admits" is exactly the sixteen occupied-shell multiples of 4,
and the empty-shell values are not in that set. The manuscript states twice that
an empty shell decides nothing either way, and §5 says in terms that at `a = 24`
no homomorphism colouring exists. Nothing was claimed about those five and
nothing was silently dropped.

That said, R2 is a careful reader who reached the other reading, which means the
sentence was doing too much work. We have not defended it; we have replaced it:

- §7 now names its scope in place — "the sixteen occupied-shell integer spindles
  that Theorem 1 admits to `a = 100`, the candidates as §6 defines them".
- It then settles the empty-shell cases rather than leaving them implicit. Both
  filters have now been run on all nine below 100. **Six die** — `8, 32, 40, 56,
  68, 96` each carry a homomorphism 4-colouring, 96 of them. **Three survive
  both** — `24, 72, 88` admit none, and the periodic filter proves at modulus 4
  that no pair of 4-periodic colourings kills them, over the 66 residue pairs
  occurring in each. Those three are candidates on the same footing as the
  sixteen, and are not counted among them because the law never admitted them.

  We owe R2 more than the sentence, then. The reason we could not see those three
  was a refusal in our own code: `join_filter_residues.py` exited at an empty
  shell saying "the question does not arise". It does arise — an empty shell means
  no point is paired with its own image, so the spindle mechanism is absent, but
  `Λ_a` still has rank 8 and 72 unit vectors whose cross edges pair distinct
  points. The filter is valid there, now runs, and produced the three. R2 reached
  the right neighbourhood by the wrong route, and there was something in it.
- Figure 3's caption now labels the bottom row as the sixteen with an *occupied*
  shell, and says the nine gaps lie outside the accounting because the law is
  silent at an empty shell.

So the substance R2 was reaching for — that a reader cannot tell from the text
what happens at `a = 24` — is now answered in the text, and the sentence that
invited the misreading is gone. We would rather lose the elegance than the
sentence's meaning.

We accept the related point (R2's weakness 2) that `audit_numbers.py` declines to
re-derive exactly the lines that decide this, and that the hole in the
verification design fell on the same spot. Closing it is on the list below.

## 2. The one real error the panel found, which was not on our own list

§5, p. 14, previously said that avoiding the 30 unit vectors of each summand
"forces each to be a geometric 4-colouring". **That does not follow, and the
manuscript refutes it three sections earlier**, where §4 counts six cyclic
colourings that avoid every unit vector and are not geometric. We are grateful
this was caught; it had survived several rounds.

The conclusion is unaffected but the reason was wrong, and is now given properly:

- the Klein group has exponent 2, so `2R ⊆ ker φ_i` with no geometric hypothesis
  at all — and none is available;
- Theorem 4's enumeration then leaves `π₁R` and `π₂R`;
- the image cannot have order 2, by `1 + ω + ω² = 2ω`, and independently because a
  hyperplane of `R/2R` holds seven non-zero classes while only six are free;
- the cyclic target is disposed of by Proposition 5, as before.

That the two reductions *are* geometric is now a conclusion of Theorem 4 in that
paragraph, not an assumption feeding it. Both exclusions of the order-2 image are
checked in `scripts/moser_is_ov.py`.

## 3. Theorems 21–23 had no proof paragraph — added

The panel is right that the three interface theorems were stated and then
explained, with nothing saying what is computed or where. They now carry a joint
proof that names the objects (126 unit vectors, 60 at the shared origin and 66
not, 8 colourings, 384 pairings, 235 patterns), says which theorem is which
statement about them, points at the two scripts, and notes that both print every
intermediate count so a reader can check them singly rather than trusting one
verdict. The proof also states inside itself what the theorems do not say: the
1920 defeat every pairing of homomorphism colourings, which is necessary and not
known to be sufficient.

## 4. UNSAT certificates

We accept this as the weakest part of the paper and have said so in the text
rather than only in correspondence. We think the panel's framing — that without
DRAT/LRAT the results are not *established* — is stronger than the field applies
uniformly, given that instances, versions, coordinates and an independent
re-derivation are supplied. But the asymmetry the panel points at is real: a
referee can check the arithmetic in an afternoon and cannot check the four largest
graphs at all.

We would rather state the position than argue it. The paper says non-4-colourability
is re-established by re-running a solver, names the four unions for which that is
the only evidence, and does not claim more. Whether to add proof logging is a
decision we will take with the editor once a venue is fixed, since the cost is
concentrated in exactly the instances where it is largest.

## 5. Administrative items

The panel is right that these make the document look unfinished, and right that
they are cheap. `[ARCHIVAL DOI]` and `[AFFILIATION]` remain the two placeholders;
the archive has no licence yet. The 30-entry suite now passes **30 of 30** from a
clean extraction — the entry the cover note reported as still running,
`lambda_sweep`, completed in 2819s, and the two earlier failures were a path that
breaks only in a clean extraction and two timeout caps we had set below the
scripts' own runtimes. All three are fixed and rerun.

## 6. Editorial points accepted without argument

- The title promises a classification the paper does not deliver. We have not yet
  settled on a replacement and would welcome the editor's view.
- The strongest result is the arithmetic obstruction together with density zero,
  not the table of seven constructions, and the front matter should lead with it.
- Novelty for `θ₁₆, θ₂₈, θ₃₆` is stated as a search, not a priority claim: "we
  have found no prior construction", with the sources and cutoff named.
- Figures 4 and 7 are dense at print size; we will supply them at larger scale or
  move the data into tables.

## What we did not change

We have left the record of retracted earlier claims — Remark 6, Remark 27,
Figure 7's caption — in the main text. The editor reads these as evidence that
uncertified computational claims should be weighted down, and that inference is
fair. We would still rather a reader see which of our own assertions turned out to
be artefacts of a sweep, and how, than have that history tidied away.
