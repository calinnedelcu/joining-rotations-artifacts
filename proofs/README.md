# Proof certificates

## `509_not4col` — Parts' record graph, verified

| | |
|---|---|
| instance | `509_not4col.cnf`, 2036 variables, 13331 clauses |
| what it encodes | 4-colourability of Parts' 509-vertex record graph: 509 at-least-one + 509·C(4,2) at-most-one + 4·2442 edge clauses = 13331, and the graph's 2442 unit edges recompute from `data/vtx/509.vtx` |
| proof | `509_not4col.drat.gz`, 3101213 lines, 85 MB uncompressed |
| checker | `drat-trim` (Heule), commit as distributed at `raw.githubusercontent.com/marijnheule/drat-trim/master/drat-trim.c`, sha256 `d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee`, built with `cc -O2` |
| verdict | **`s VERIFIED`** |
| detail | 11396 of 13331 clauses in core; 915005 of 1569693 lemmas in core using 67841290 resolution steps; 0 RAT lemmas; 126 s backward checking |
| log | `509_not4col.drat-trim.log` |

Reproduce:

    gzip -dc proofs/509_not4col.drat.gz > /tmp/509.drat
    drat-trim proofs/509_not4col.cnf /tmp/509.drat

## What is not certified

The seven constructions of the paper's Section 6 and the monochromatic-pair
property behind Lemma 18 are established by re-running a solver, not by checking
a proof. Their sizes are 733, 5809, 29113, 156577, 158257, 175825 and 187225
vertices. Nothing in `proofs/` covers them.

Theorems 21-23 need no certificate: the hitting set over the 235 patterns is an
exhaustive search, small enough to redo directly, and the paper says so.

## Where the proof file is

`509_not4col.drat.gz` is 85 MB, past GitHub's file-size threshold, so it is not in
this repository's history. It is attached to the `v1.0` release as a downloadable
asset. The CNF, the checker log and this file are here; fetch the proof from the
release and run `scripts/check_drat.sh`.
