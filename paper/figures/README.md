# The figures, and why they are scripts

Every figure in `joining-rotations.tex` is generated from the lattice itself.  No
coordinate in any of them was typed by hand, and each script asserts the fact its
figure claims before it draws anything -- that the spindle edge has length
exactly 1, that all 126 cross edges do, that the three verdict sets partition the
sixteen candidates, that both colourings leave zero monochromatic edges.  A
figure that stopped being true would fail rather than mislead.

Rebuild them all:

```bash
cd paper/figures && for f in fig_*.py; do ../../.venv/bin/python "$f"; done
```

Each writes `<name>.pdf` for the paper and `<name>.png` to look at.

| figure | script | what it draws |
|---|---|---|
| 1 | `fig_lattice.py` | the 30 unit vectors, and the depth-2 ball |
| 2 | `fig_spindle.py` | the spindle mechanism at `a = 4` |
| 3 | `fig_law.py` | the divisibility law as a sieve over `a <= 100` |
| 4 | `fig_colourings.py` | the two prime-reduction 4-colourings |
| 5 | `fig_orbits.py` | all 126 cross edges of the `theta_4` interface |
| 6 | `fig_shells.py` | the seven rotations, each on its shell |
| 7 | `fig_graphs.py` | the 1408-vertex `alpha_64/9` union |
| 8 | `fig_reach.py` | the shells at true scale against the searched disc |

`style.py` holds the shared register; `latticeshell.py` enumerates a shell
exactly from the chart, the same reduction `scripts/shells.py` counts with.
`crossedges.json` is a cache of the depth-4 ball's cross edges -- delete it and
`fig_orbits.py` recomputes.

## The register, and why

The subject's papers (Parts; Voronov, Neopryatnaya and Dergachev) draw the
*object*, not a diagram about it: black dots, thin black lines, no colour, no
axes, and no label a caption could carry instead.  These follow that.  Two
consequences worth keeping:

* **Computer Modern inside the figures.**  matplotlib ships `cmr10` and friends,
  so `mathtext.fontset = "cm"` makes figure text the same face as the body text
  instead of a near-miss.
* **Natural size, no scaling.**  Each figure is drawn at the size it prints at
  and included with no `width=` key, so a point in the script is a point on the
  page and the label sizes are what they were chosen to be.  `TEXTWIDTH` in
  `style.py` is the amsart 11pt text block; stay under it.

Glyphs rather than colours in Figure 4, for the same reason: it has to survive a
grey print.
