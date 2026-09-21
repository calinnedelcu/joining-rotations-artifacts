# Licensing

Two licences, split the usual way for a paper's artifacts.

| what | licence | SPDX |
|---|---|---|
| `scripts/`, `hn/` — the code | MIT, in [`LICENSE`](LICENSE) | `MIT` |
| `paper/`, `proofs/`, `results/`, `data/`, `docs/` and this file — the text, the certificates and the data | Creative Commons Attribution 4.0 International, in [`LICENSE-CC-BY-4.0.txt`](LICENSE-CC-BY-4.0.txt) | `CC-BY-4.0` |

Copyright (c) 2026 Andrei-Calin Nedelcu.

If you use the constructions, the certificates or the shell classification,
please cite the paper. If you use the code, MIT asks only that the notice
travel with it.

## What is not ours to license

`data/parts/` holds four files taken from Jaan Parts' published record
(arXiv:2010.12665); `PROVENANCE.md` names them and says where each came from.
They are his work, included so that the claims resting on them can be checked,
and nothing here relicenses them.

The two tools the certificates depend on are third-party and are not vendored
at all: `drat-trim` is Marijn Heule's, CaDiCaL is Armin Biere's, and
`proofs/README.md` says how to fetch and build each.
