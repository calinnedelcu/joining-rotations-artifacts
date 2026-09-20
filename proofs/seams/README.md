# Seam certificates

The UNSAT results of `results/SEAMS.md` as DRAT proofs rather than solver
verdicts. A Galois conjugation of the coordinate field preserves unit distance,
because `|p-q|^2 = 1` is rational and Galois fixes the rationals, so it carries a
5-chromatic unit-distance graph to another one. Composed with the twelve
isometries that gives 96 maps, and the *seam* is the one under which a graph
splits most unevenly: the 509-vertex record splits 494 fixed and 15 moved, which
turns "is there a smaller 5-chromatic graph sharing this core" from a 509-choice
search into a 14-choice one.

Each instance ships beside its proof and its `drat-trim` log.
`scripts/certify_seams.py` regenerates any of them.

| instance | vars | clauses | proof lines | proof | `drat-trim` |
|---|---:|---:|---:|---:|---|
| `master_ps_L_4` | 3307 | 25226 | 5,236,053 | 76.4 MB | **`s VERIFIED`**, 80.1 s |
| `master_core494` | 9570 | 28211 | 1,630,223 | 42.0 MB | **`s VERIFIED`**, 56.1 s |
| `master_core484` | 6798 | 24885 | 1,209,589 | 21.7 MB | **`s VERIFIED`**, 22.3 s |
| `master_ps_S_1` | 2789 | 6019 | 146,248 | 2.2 MB | **`s VERIFIED`**, 1.0 s |
| `master_core493` | 5048 | 15836 | 116,301 | 1.2 MB | **`s VERIFIED`**, 0.9 s |
| `master_ps_L_0` | 1801 | 4347 | 68,029 | 0.6 MB | **`s VERIFIED`**, 0.5 s |
| `master_ps_L_1` | 1792 | 4304 | 19,207 | 0.1 MB | **`s VERIFIED`**, 0.1 s |
| `master_core491` | 2353 | 6888 | 12,797 | 0.1 MB | **`s VERIFIED`**, 0.1 s |
| `master_core505` | 3078 | 5030 | 2,673 | 0.0 MB | **`s VERIFIED`**, 0.0 s |
| `master_ps_S_5` | 1062 | 1477 | 488 | 0.0 MB | **`s VERIFIED`**, 0.0 s |

Ten instances, 144 MB of compressed proof, all
verified. What each CNF encodes is documented in the script that built it
(`scripts/gal_core.py`, `scripts/part_seam.py`): a certificate settles the CNF,
and the modelling is the script's.

Three further instances in `out/` — `master_rec509_d7`, `d8`, `d9` — are from a
different line of work, not the seam programme, and are not certified here. The
first was abandoned after its proof passed 5 GB.
