# Revision history

*What changed in* **A divisibility obstruction for joining two Moser lattices**
*and why.* This was written as a reply to a round of referee reports, so it is
phrased as a response; it is kept here because it records the reasoning behind
each change, including three errors of ours that the reports found. A reader
coming to the paper fresh does not need it — `FOR-THE-REVIEWER.md` is the
orientation note.

Numbered references below are to the **current** paper, not to the draft each
entry was written against; where a renumbering left an object with no current
number, the object is named instead. `scripts/check_notes.py` checks them.

We are grateful for the report, and particularly for the reviewer who
reimplemented the lattice from the chart and the congruences rather than running
our code. Three of the findings were errors on our side that we had not seen,
and one of them was a mathematical overreach in the section that carries the
paper's own method. Everything below is done unless it says otherwise.

---

## The ten must-fix items

**1. The new constructions were uncertified.** Fixed, and further than asked.
The report requested DRAT proofs for the two minimised graphs, and said a
certificate for the four full-ball unions "may genuinely be impractical" with a
reported attempt sufficing. It is not impractical. **All seven constructions of
Section 6 now carry a checked DRAT proof**, as does Parts' 509-vertex record:

| instance | vertices | clauses | proof lines | solve | `drat-trim` |
|---|---:|---:|---:|---:|---|
| `theta16`, minimised | 2 901 | 87 250 | 1 575 613 | 65 s | `s VERIFIED` 45 s |
| `alpha64_9`, minimised | 1 408 | 37 911 | 1 220 482 | 43 s | `s VERIFIED` 33 s |
| `theta28`, full ball | 156 577 | 8 443 306 | 8 171 047 | 236 s | `s VERIFIED` 65 s |
| `theta36`, full ball | 175 825 | 9 533 074 | 9 172 884 | 375 s | `s VERIFIED` 160 s |
| `alpha64_3`, full ball | 187 225 | 10 140 490 | 9 659 817 | 237 s | `s VERIFIED` 74 s |
| `alpha256_9`, full ball | 158 257 | 8 536 258 | 8 157 168 | 175 s | `s VERIFIED` 47 s |
| `gadget367`, terminals split | 367 | 9 864 | 1 139 281 | 33 s | `s VERIFIED` 30 s |
| `509_not4col` | 509 | 13 331 | 3 101 213 | — | `s VERIFIED` 131 s |

`theta_4` is the record itself, so the eight rows account for all seven
rotations. About 415 MB of compressed proof; roughly ten minutes to re-check the
lot with `scripts/check_drat.sh`.

Two things made this possible, and both are stated in `proofs/README.md`. Of the
`python-sat` bindings only `lingeling` emits a proof at all, and it is far too
slow here — it ran 22 minutes on the *smallest* instance without finishing — so
`scripts/certify.py` now writes the CNF and calls the CaDiCaL binary. And every
instance fixes a triangle's three vertices to colours 0, 1, 2. That is the only
step in the encoding that is not a literal transcription, and it is sound in the
usual way: a triangle gets three distinct colours under any proper colouring, so
composing with the permutation carrying them to 0, 1, 2 satisfies the added unit
clauses; the augmented instance is satisfiable exactly when the graph is
4-colourable. It is not a nicety. Without it the 367-vertex gadget passed 580 MB
of proof without terminating; with it the whole run takes 75 seconds.

**2. Lemma 20's UNSAT was undisclosed and uncertified.** Fixed. The reviewer was
right that this was the more serious of the two certificate gaps: the entire
`a = 64n^2/9` family rests on Parts' gadget having no 4-colouring that separates
its terminals, and that instance was not even on our list of things needing a
certificate. It is now row seven above, and the paper's inventory names it.

**3. "The obstruction decides every rational `a`."** Removed. The abstract now
says it is *decidable in closed form* at every rational `a`, that it kills every
`a` with `4 | a` failing, and that it is silent otherwise. The reviewer's reading
was correct and ours was not defensible.

**4. "Join" undefined across 57 uses.** Defined once in Section 1, before
Theorem 1, together with "spindle" and the `theta_a` / `alpha_a` convention.

**5. `chi >= 5` presented as `chi = 5`.** The table column is now "vertices
(`chi >= 5`)", the contributions list is qualified at first mention rather than
twenty pages in, and a sentence after Lemma 21 says the guaranteed 5-chromatic
subjoin carries no size bound better than the full union.

**6. The empty-shell verdicts were the least-checked claims.** Fixed, and in a
better form than requested. The report asked for "the exhaustive-search log
showing none exists". For the three survivors we can do better: each ships **a
vector of length 1/2**, which by Proposition 5 rules out every homomorphism onto
a group of order 4 — a one-line proof where a log would be only a log. The six
that die ship the explicit Klein colouring, as the two functionals cutting out
its kernel. `scripts/check_emptyshell.py` validates all nine from the JSON
alone, computing lengths from the multiquadratic field's own multiplication
table and importing nothing from this project. Nine witnesses, zero bad.

**7. "That is the only outcome consistent with their being 5-chromatic, and it
is not automatic."** Deleted. `theta_4`'s survival is forced by our own
the companion paper's unit-triangle proposition, and the text now says which of
the five are informative and
which is not.

**8. Two pages of self-errata.** Cut to the disclosures a reader needs to trust
the current text. Appendix A, which said itself that nothing depends on it, is
now `docs/odd-case.tex` in the repository.

**9. The narrow Hilbert class field.** Added, and we thank the reviewer for it —
it is the better statement and we had walked past it. One correction to the
suggested route, though, because the direction matters. Deriving
`d_{V/F} = (1)` *from* the identification would be circular, since the
identification needs unramifiedness. But there is an independent derivation:
`disc(F) = 33 = (-3)(-11)` is a product of two prime discriminants, so the
narrow genus field of `F` is `Q(sqrt-3, sqrt-11)`, and since
`sqrt-3 · sqrt-11 = -sqrt33` that field **is** `V`. So `V` is the narrow Hilbert
class field of `Q(sqrt33)` by genus theory alone, `d_{V/F} = (1)` follows a
second time, and the two routes agree. We state both. "Obstructed" is now also
given as "`p` lies in the non-principal genus of discriminant 33", and the five
residue classes mod 33 are exactly those where both genus characters are `-1` —
half of the twenty classes fail the first, half of those the second.

**10. DOI, affiliation, licence.** The repository is now licensed: MIT for the
code, CC BY 4.0 for the paper, the certificates and the data, with the split and
the exceptions in `LICENSES.md` — the four files from Parts are his and are
relicensed by nothing there, and `drat-trim` and CaDiCaL are third-party and
deliberately not vendored. **The DOI and the affiliation are still outstanding**
and are the only two `[TO BE SUPPLIED]` left in the manuscript.

---

## The should-fix list

All done. In brief: the excluded-rationals list corrected at both occurrences to
`5/9, 7/3, 13/3, 71/9, 31/3, 43/3, 137/9` with `1/3` dropped and the cause named
(only the `3k^2` branch was run at non-integer `a`); Hasse demoted out of the
abstract and the contributions list, with the proof saying in terms that the
argument does not use it; the density comparison restated as asymptotic-versus-
finite with the near-coincidence of the two sets below `10^6` made explicit;
"the 59 **positive** squared radii"; "four rational conditions where `q` is one";
the lemma naming congruence (ii) and showing the halving step; the lemma noting
that the `pi_2` case is the `sigma`-image and that every congruence used is
insensitive to the sign; the table headed "shell size" with `126` in
place of the em dash; a five-line proof skeleton opening Section 5; the
modulus-selection rule stated before the results in Section 7; the richness
comparison given its missing caveat; the three-hour `verify_all.sh` budget in
the paper.

One was declined in the form suggested and answered differently. The report
asked us to *either* minimise all six unions to a common protocol *or* drop the
richness paragraph. We have done neither: the paragraph now states plainly that
the unit-vector counts are lattice invariants while the vertex counts are
outputs of the ball rule, that part of the spread from 5 809 to 187 225 is the
rule and not the rotation, and that the comparison therefore supports only the
negative claim actually made — richness does not force smallness — and cannot
rank the seven. We think that is the honest reading, and minimising six graphs to
compare numbers we would still not trust seemed the wrong use of the effort.

---

## The two new findings, and the one that was an error of ours

**The literature check on [9].** The report asked whether Voronov–Neopryatnaya–
Dergachev's enumeration reaches squared radii 16, 28, 36, and noted that an
answer with an explanation would be worth more than a bare absence. It is
answerable from their paper. Their first series takes `M_1` to be the origin
with the 30 unit vectors, sets `M_2 = clip(M_1 + M_1; 1)` and then
`M_3 = M_2 + M_1` unclipped — so **every vertex it considers lies within radius
2**: 1 939 points, and `2·1939 − 1 = 3877` in the union, which is exactly what
their Table 4 reports. Every construction of our Section 6 uses a shell pair at
radius `sqrt a`, and of the seven only `theta_4` has `sqrt a <= 2`. So `theta_4`
is the only spindle that search could have succeeded at, and it is the one it
found: their `psi_* = 7/8 + (sqrt15/8)i` **is** `theta_4`. Whether the other
three occurred among their 31 375 enumerated rotations cannot be read off a table
that lists only the five successes — but none could have worked there, because
the pair that makes them work is outside the set being coloured. That is our own
Figure 8 argument met in the literature rather than supposed, and it is now in
Section 6.

**`Lambda_24` holds twelve half-unit vectors, and this was our error.** The
reviewer is right, and the consequence is larger than flagged. Section 3 said
that for a spindle the half-unit vectors "have a closed form". They do not; the
shell gives *one family* of them. At `a = 24` the shell is empty, so that family
is empty — and `Lambda_24` has twelve vectors of length 1/2 regardless. One is
hand-checkable: `R ∩ Q = (1/3)Z`, so `r = -5/3` and `s = 2` both lie in `R`, and

    r + theta_24(s) = -5/3 + 2(47/48 + i·sqrt95/48) = (7 + i·sqrt95)/24,

whose squared length is `(49 + 95)/576 = 1/4`. In the Step 1 parametrisation this
is `lambda = -6/5`; the shell is `lambda = -1`, and it is not the only value that
reaches length 1/2.

Three things follow, all now in the paper. **Theorem 1's shell hypothesis is
sufficient and not necessary** — what the second half needs is a half-unit
vector, which an occupied shell always supplies and an empty one sometimes
supplies anyway. **Section 7's three survivors are explained**: `a = 24`, `72`
and `88` each carry exactly twelve, which is why no homomorphism colouring
exists there, and it is our own half-unit proposition doing the work rather than
anything in that section. And **the census in the closed-form section was
wrong**: nineteen integer
spindles below 100 have a half-unit vector, not sixteen. We confirm the
reviewer's diagnosis of the cause, and it is worth stating because it is the same
species of blind spot the paper already confesses to elsewhere — the sweep's
domain was `if a % 4 or not shell_count(a)`, so it skipped empty shells, which
is precisely where the three missing rotations live. The code could not see the
counterexample its own domain excluded. `scripts/z4_relation.py` now covers every
multiple of 4, and where `4` does not divide `a` there is none by Theorem 1 with
Proposition 5 — a proof rather than a search.

We note for completeness that the reviewer's suspicion about the sweep
enumerating half-unit vectors *through* the shell construction was not the case:
it searched the lattice directly, which is why the published verdicts were all
correct. The defect was the domain, not the method.

---

## Two items still open

- **The DOI and the affiliation.** Ours to supply, not yet supplied.
- **Haugland's lattice at `N = 7`.** The report objected, fairly, that ninety
  minutes is
  not a budget that justifies stopping. It is now running on a ten-hour budget;
  whatever it returns, the paper will report a threshold worth the name rather
  than the one it had.
