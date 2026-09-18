# Which shells exist, decided by the form rather than by a ball

A spindle `theta_a` acts only on the lattice points at squared radius `a`.  If
the lattice has none, the rotation has nothing to move and cannot join anything,
however cleanly it passes the arithmetic filter.  So shell existence is a second,
independent kill -- and it must be decided exactly, because absence from a ball
proves nothing.

In the chart `z = (a + b sqrt33)/12 + i(c sqrt3 + d sqrt11)/12`,

    |z|^2 = [ (a^2 + 33 b^2 + 3 c^2 + 11 d^2) + 2 (ab + cd) sqrt33 ] / 144

so `|z|^2 = N` is a rational integer exactly when

    ab + cd = 0    and    a^2 + 33 b^2 + 3 c^2 + 11 d^2 = 144 N.

Positive definite, so each `N` is a finite exact search.

**The chart is a superset, and reading it as the lattice overcounts.**  Integer
`(a,b,c,d)` describe a group containing `R` with index 16.  Measured: the chart
claims 28 points at squared radius 7/4 and 30 at 9/4, where the lattice has
**none** of either.  `R` is cut out by congruences, extracted from the lattice
and now enforced:

    a = b = c = d  (mod 2)      and      a + b + c + d = 2a  (mod 4)

which selects exactly the 16 residue classes mod 4 that occur, of 256.  `N = 1`
returns the 30 unit vectors and `N = 7/4` returns 0, and both are asserted in
`scripts/shells.py` so the bug cannot come back.

**Nothing downstream changed.**  Every count this repository relied on was
re-derived with the congruences in place and is identical: the occupied integer
shells, the multiples of 4 among them (4, 12, 16, 20, 28, 36, 44, 48, 52, 60),
the empty ones (8, 24, 32, 40, 56), and every rational candidate's shell.  The
bug only ever affected radii no result used.

**Occupied, N <= 60:** 1, 3, 4, 5, 7, 9, 11, 12, 13, 15, 16, 19, 20, 21, 23, 25,
27, 28, 31, 33, 35, 36, 37, 39, 43, 44, 45, 47, 48, 49, 52, 53, 55, 57, 59, 60.

**Empty, N <= 60:** 2, 6, 8, 10, 14, 17, 18, 22, 24, 26, 29, 30, 32, 34, 38, 40,
41, 42, 46, 50, 51, 54, 56, 58.

## Effect on the classification

Of the eleven rotations surviving the arithmetic filter, exactly one --
**`theta_24`** -- spins a shell that does not exist. It is eliminated
geometrically, and the genuine candidate list is **ten**:

    4, 12, 16, 20, 28, 36, 44, 48, 52, 60.

## A correction worth recording

A depth-7 ball of 168307 points contains no point at squared radius 44, 48, 52
or 60, and reading that as "those shells are empty" would have been wrong: the
form shows all four are occupied, with 84, 60, 60 and 84 points. Points at those
radii simply need more than seven unit-vector steps to express.

This is the routes 20/44/48 error in its purest form, and it was made again here
before the exact check caught it. A ball answers about a ball.

Reproduce: `scripts/shells.py 60`.
