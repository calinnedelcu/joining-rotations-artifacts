# Haugland's lattice: rank 12, and de Grey's extension does enlarge it

de Grey asked publicly (Polymath16 thread 18, 13 Sep 2026) for someone to explore
Haugland's Moser-spindle-free construction as a route past 509, "using more than
just two sets of 42 vectors".  Two measurements decide whether that is worth
pursuing and whether our machinery can reach it.

## It has rank 12, not 96

The construction lives in `Q(zeta_420)`, which has degree 96, and that looked
prohibitive: the trace-form ellipsoid enumeration behind our joining criterion
would have to run in 96 dimensions.

It does not.  The 42 unit vectors span a **12-dimensional** `Q`-subspace, and
adding more sets does not raise it -- 1, 2 and 3 sets all give `Q`-rank 12.  A
12-dimensional Fincke-Pohst enumeration is entirely tractable, so **the criterion
ports**.

## More sets DO enlarge the lattice

Rank staying at 12 does not mean nothing changes: the `Z`-module can get finer
inside the same `Q`-span.  It does.  Reducing the integer coefficient matrix:

| sets of 42 | `Z`-rank | pivot product | over |
|---|---|---|---|
| 1 | 12 | 1 | 1 |
| 2 | 12 | `7^11` | `7^12` |
| 3 | 12 | `7^10` | `7^12` |
| 4 | 12 | `7^9` | `7^12` |

Each extra set multiplies the covolume by `1/7`: the lattice becomes **seven
times finer** every time.  So de Grey's suggestion is not cosmetic -- it produces
a genuinely richer lattice, which is exactly what a construction needs.

## What this makes possible

With rank 12 the joining criterion can be asked here rather than guessed at:
which rotations can join two copies of *this* lattice.  That replaces the current
approach -- build sets, run SAT for hours, mostly time out -- with a decision
procedure, which is what worked on the Moser lattice.

The remaining work is porting the trace form from the multiquadratic field to
`Q(zeta_420)`: the principle is identical, since `Tr(z conj(z))` is positive
definite over any number field, but the implementation in `hn/lattice.py` is
written for eight basis elements and two real coordinates.
