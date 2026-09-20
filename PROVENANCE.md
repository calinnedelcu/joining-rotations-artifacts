# Provenance of the data in this archive

Everything here was produced by the scripts in `scripts/`, from the definitions,
except the files listed below, which come from published work by other authors.
They are included because the claims that use them cannot be checked without
them, and they are unmodified.

| file | source | what it is |
|---|---|---|
| `data/vtx/509.vtx` | J. Parts, *Graph minimization…*, Geombinatorics **29** (2020) 137–166, arXiv:2010.12665 | the 509-vertex 5-chromatic record graph, coordinates as published |
| `data/parts/v367e1822.vtx` | the same | his minimal monochromatic-pair gadget at distance 8/3, terminals (±4/3, 0) |
| `data/parts/v421e2094.vtx` | the same | the second gadget, at distance 8/√3, terminals (0, ±4/√3) |
| `data/parts/graphs.txt` | the same | his inventory table, transcribed, listing each gadget's distance and terminals |

Those four were transcribed from the published coordinates into this archive's
own exact format, not regenerated: `scripts/gadget_chain.py` recomputes the
367-vertex gadget's edge set from the coordinates and gets 1822, the number his
filename records, which is the check that the transcription is faithful.

The five rotations of Voronov, Neopryatnaya and Dergachev (*Constructing
5-chromatic unit distance graphs…*, Discrete Math. **345** (2022) 113106,
arXiv:2106.11824, Table 5) are used only through the numerical imaginary parts
quoted in `scripts/voronov_rotations.py`; no graph data of theirs is included.

Nothing in this archive is derived from Haugland's or Dúcz's coordinate files.

**Licence.** MIT for the code, CC BY 4.0 for the paper, the certificates and the
data; `LICENSES.md` gives the split. The four files above remain subject to
whatever terms their original publication carries and are relicensed by nothing
here.
