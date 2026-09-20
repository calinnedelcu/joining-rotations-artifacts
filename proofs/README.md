# Proof certificates

Eight DRAT proofs, every one checked with Marijn Heule's `drat-trim`. They cover
**all seven constructions of the paper's Section 6**, the monochromatic-pair
property Lemma 18 rests on, and Parts' 509-vertex record.

Until this revision the only certificate here was the last row — a proof of
someone else's theorem, while our own claims were solver verdicts. A referee
pointed that out, and was right.

| instance | what it decides | vertices | CNF clauses | proof lines | solve | `drat-trim` |
|---|---|---:|---:|---:|---:|---|
| `theta16` | minimised `theta_16` not 4-colourable | 2 901 | 87 250 | 1 575 613 | 65 s | **`s VERIFIED`** 45 s |
| `alpha64_9` | minimised `alpha_64/9` not 4-colourable | 1 408 | 37 911 | 1 220 482 | 43 s | **`s VERIFIED`** 33 s |
| `theta28` | full-ball `theta_28` not 4-colourable | 156 577 | 8 443 306 | 8 171 047 | 236 s | **`s VERIFIED`** 65 s |
| `theta36` | full-ball `theta_36` not 4-colourable | 175 825 | 9 533 074 | 9 172 884 | 375 s | **`s VERIFIED`** 160 s |
| `alpha64_3` | full-ball `alpha_64/3` not 4-colourable | 187 225 | 10 140 490 | 9 659 817 | 237 s | **`s VERIFIED`** 74 s |
| `alpha256_9` | full-ball `alpha_256/9` not 4-colourable | 158 257 | 8 536 258 | 8 157 168 | 175 s | **`s VERIFIED`** 47 s |
| `gadget367` | Parts' gadget has no 4-colouring separating its terminals — Lemma 18's premise, and so the whole `a = 64n^2/9` family | 367 | 9 864 | 1 139 281 | 33 s | **`s VERIFIED`** 30 s |
| `509_not4col` | Parts' 509-vertex record not 4-colourable | 509 | 13 331 | 3 101 213 | — | **`s VERIFIED`** 131 s |

`theta_4` is the record itself, so the eight rows account for all seven
rotations. The two minimised graphs are themselves unions `L u theta(S)`, so
each settles its rotation on its own; the four largest are whole balls, left
unminimised.

Total: about 415 MB of compressed proof, and roughly ten minutes to re-check the
lot. A shallow clone of this repository is therefore around 900 MB; if you only
want to sanity-check the pipeline first, `gadget367` is 31 MB and verifies in
half a minute:

    bash scripts/check_drat.sh ./tools/drat-trim gadget367

Timings are on an Apple M5 with 32 GB.

Nothing here needs a SAT solver installed: `check_drat.sh` reads the shipped
proofs and calls `drat-trim`. Only `certify.py`, which *regenerates* a proof,
needs CaDiCaL.

Checker: `drat-trim` as distributed at
`raw.githubusercontent.com/marijnheule/drat-trim/master/drat-trim.c`, sha256
`d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee`, built with
`cc -O2`. Per-run detail is in each `*.drat-trim.log`.

Re-check everything:

    bash scripts/check_drat.sh ./tools/drat-trim

Regenerate one from the coordinates, solver and all:

    .venv/bin/python scripts/certify.py theta36

The four largest CNFs are 140-170 MB raw and ship gzipped, as `.cnf.gz`
beside their proofs; `check_drat.sh` unpacks either form.

## The encoding, and the one reduction in it

One variable per (vertex, colour); an at-least-one clause per vertex; an
at-most-one pair per vertex and colour pair; and for each unit edge and colour, a
clause forbidding both ends that colour. For `gadget367` the two terminals are
additionally forced apart, which is exactly the monochromatic-pair property
Lemma 18 needs.

Every instance except `509_not4col` also **fixes a triangle's three vertices to
colours 0, 1 and 2**, and this is the only step that is not a literal
transcription of the question. It is sound in the usual way: a triangle gets
three distinct colours under any proper colouring, so composing that colouring
with the permutation carrying those three to 0, 1, 2 gives a proper colouring
satisfying the added unit clauses. The augmented instance is therefore
satisfiable exactly when the graph is 4-colourable, and UNSAT for it is UNSAT for
the plain encoding. The triangle used is named in each run log.

It is not a nicety. Without it the 367-vertex gadget — the smallest instance
here — passed 580 MB of proof without terminating; with it the whole run, solve
and proof and check, takes 75 seconds.

## What is still not certified

Nothing in Section 6. Theorems 21-23 need no certificate: the hitting set over
the 235 patterns is an exhaustive search, small enough to redo directly, and the
paper says so.

The nine empty-shell verdicts of Section 7 are certified too, but not here and
not by SAT: see `results/emptyshell/` and `scripts/check_emptyshell.py`.

## Building the two tools

Neither is vendored: a checker you got from the people whose proof you are
checking is not a check, and the same goes for the solver that wrote it.
`scripts/certify.py` looks for both under `tools/`.

    mkdir -p tools && cd tools
    curl -O https://raw.githubusercontent.com/marijnheule/drat-trim/master/drat-trim.c
    cc -O2 -o drat-trim drat-trim.c
    curl -sSL -o cadical.tar.gz https://github.com/arminbiere/cadical/archive/refs/tags/rel-2.1.3.tar.gz
    tar xzf cadical.tar.gz && cd cadical-rel-2.1.3 && ./configure && make

Of the `python-sat` bindings only `lingeling` emits a proof at all, and it is far
too slow here — it ran 22 minutes on the 367-vertex gadget without finishing.
Hence the binary.
