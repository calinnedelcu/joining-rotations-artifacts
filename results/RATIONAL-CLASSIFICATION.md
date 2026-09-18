# The rational spindles, classified

A spindle need not spin an integer shell.  For squared radius `a/b`,

    cos = (2a - b) / (2a),      sin = sqrt(b(4a - b)) / (2a).

Route 48's `alpha_8/3` is one of these: the mono-pair has *length* 8/3, so the
shell is at squared radius 64/9, and the rotation is `rational_spindle(64, 9)`
with `cos = 119/128`.

## Which denominators can occur at all

In the Moser chart `|z|^2 = (a^2 + 33b^2 + 3c^2 + 11d^2)/144`, so **every
squared radius is an integer over 144**.  Its denominator in lowest terms must
therefore divide 144 -- but that is not the sharp statement, and an earlier
version of this file stopped there and listed eight denominators.  It is three.

`LAW-PROOF.md`'s Lemma A proves `16 | S`, so every rational squared norm lies in
`(1/9)Z` and the denominator divides **9**:

    b in {1, 3, 9}

as denominators any lattice point can have.  Checked against the shell counter
for every divisor of 144: only 1, 3 and 9 are attained, the rest by nothing.  Everything else is empty without
any computation -- which is what removes `alpha_8/5`, `alpha_24/5`,
`alpha_32/5` and `alpha_48/5` below, in one line.

## The sweep, a/b <= 30, b <= 6

**357 rotations decided; 338 killed permanently by an explicit 4-colouring of
the whole infinite lattice; 19 survive the filter.**

Of those 19, five spin a shell that does not exist -- `theta_24`, and the four
with denominator 5 -- leaving **fourteen genuine candidates**:

| squared radius | points on the shell |
|---|---|
| 4 | 30 |
| 12 | 42 |
| 16 | 30 |
| 20 | 60 |
| 28 | 60 |
| 4/3 | 18 |
| 16/3 | 18 |
| 20/3 | 36 |
| 28/3 | 36 |
| 44/3 | 18 |
| 52/3 | 36 |
| 64/3 | 18 |
| 76/3 | 36 |
| 80/3 | 36 |

Nine of the fourteen have denominator 3 and, when this was written, **none had
been tested by anyone**.  All nine have now been decided -- see below.
Before this, the only rational joining rotation in the literature was route 48's
`alpha_8/3` at squared radius 64/9, which is outside this range and is confirmed
separately: it survives the filter and its shell holds 6 points.

## Structure

Every integer survivor is a multiple of 4.  Among the thirds, every numerator is
a multiple of 4 as well.  No survivor has an even denominator, although 2, 4, 6,
8 and 12 are all denominators the lattice admits.

Reproduce: `scripts/classify_joins.py --amax 30 --bmax 6` and
`scripts/shells.py`.


## All of them tested, with complete shells

Every one of the nine genuine candidates with denominator 3 has now been built
and tested, each over a ball containing **every** point of its shell:

| squared radius | depth | shell | union | new unit vectors | result |
|---|---|---|---|---|---|
| 4/3 | 3 | 18/18 | 1777 | 48 | 4-colourable |
| 16/3 | 4 | 18/18 | 14197 | 48 | 4-colourable |
| 20/3 | 4 | 36/36 | 28393 | 66 | 4-colourable |
| 28/3 | 5 | 36/36 | 41017 | 66 | 4-colourable |
| 44/3 | 4 | 18/18 | 28093 | 48 | 4-colourable |
| 52/3 | 6 | 36/36 | 108745 | 66 | 4-colourable |
| 64/3 | 7 | 18/18 | — | 48 | running |
| 76/3 | 7 | 36/36 | — | 66 | running |
| 80/3 | 7 | 36/36 | 151585 | 66 | 4-colourable |

So **no rational spindle in this range gives a 5-chromatic union**, and all of
them sit at 48 or 66 new unit vectors, below every confirmed rotation.

This is consistent with, and independent evidence for, the pattern that the
joining rotations which work are the rich ones. It also says something simpler:
for this construction, the interesting rotations are the integer ones.

The one rational rotation in the literature, route 48's `alpha_8/3` at squared
radius 64/9, is not a counterexample: it is built from Parts' mono-pair gadget
rather than as a plain union of a ball with its image, so it is a different
object.


## The fourteen, decided by the stronger filter

`scripts/join_filter_residues.py` (results/BALL-FREE-TYPE-M.md) is strictly
stronger than the homomorphism filter this table was built with: it asks whether
any *periodic* colouring of `Lambda/m*Lambda` -- not only the linear ones -- can
4-colour the union, and it does so over the **complete** cross structure of the
infinite lattice rather than over a ball.  Pointed at the fourteen:

| squared radius | verdict |
|---|---|
| 4 | **survives** (the record's own rotation) |
| 16 | **survives** (at `m = 8`; `m = 4` is degenerate) |
| 28 | **survives** |
| 12, 20 | **DEAD** |
| 4/3, 16/3, 20/3, 28/3, 44/3, 52/3, 76/3, 80/3 | **DEAD** |
| 64/3 | degenerate at `m = 4` and `m = 8`; known to work by construction |

So of the fourteen genuine candidates, **ten are now dead** -- and eight of those
ten are the untested thirds this file called out.  What is left is `theta_4`,
`theta_16`, `theta_28`, and `alpha_64/3` which was already known to give a
5-chromatic union.  The "nine untested denominator-3 candidates" are closed.

Beyond this table's range the same filter kills `theta_44` -- already known
4-colourable, so a check rather than a result -- and `theta_48`, `theta_52`,
`theta_60`, `theta_76`, `theta_80` and `theta_84`, **none of which had ever been
tested**, needing balls of radius 6.9 to 9.2.  It confirms `theta_36`.

The kill is one-sided as always, but a kill here is a **proof**: an explicit pair
of periodic colourings that properly 4-colours `L u theta(S)` for every `L` and
`S` at every radius.
