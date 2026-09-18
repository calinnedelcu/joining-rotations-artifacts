# v5 -> 30: the evaluator built, the construction reproduced, two families ruled out

`v_5 >= 30` follows from `e_5 >= 104`, since Alexeev-Mixon-Parshall give
`u(29) <= 103`.  And `e_5 >= ceil(1 / p_4)`, so the whole thing reduces to
pushing `p_4` below `1/104 = 0.0096154`.  The published value is `1/99`.

## The evaluator, and why it is trustworthy

`tiling/p4.py` computes

    p_k = (1 / (2 pi |S|)) int_S dsigma int_0^{2pi} dphi M_k(sigma, phi)

by sampling the outer integral over a fundamental domain and the inner one in
`phi`.  de Grey and Parts report being blocked here -- they "encountered some
problems with the numerical integration function NIntegrate in the general case,
and were forced to limit ourselves to relatively simple tilings".

**Validated against a closed form.**  For two colours in straight stripes of
width `h`, Heinasmaki gives `p_s(h)` exactly.  Against it:

| h | closed form | evaluator | relative error |
|---|---|---|---|
| 0.5 | 0.598743 | 0.598775 | 5.4e-05 |
| 0.75 | 0.353852 | 0.353767 | 2.4e-04 |
| sqrt3/2 | 0.333333 | 0.333367 | 1.0e-04 |
| 1.2 | 0.469484 | 0.469475 | 1.8e-05 |

It also reproduces the known optimum: straight stripes are best at `h = sqrt3/2`
with `p = 1/3` exactly.

## The published construction, reproduced

de Grey and Parts describe Gwyn-Stavrianos' tiling as "regular hexagons of four
colours with a diameter of about 1.1335".  Which four-colouring is not stated.
Searching **all seven index-4 sublattices** of the hexagonal index lattice
settles it -- one beats the rest by a factor of five:

| sublattice | 1/p_4 |
|---|---|
| `2Z x 2Z`, i.e. colour `(i mod 2, j mod 2)` | **96.4** |
| `(2,1),(0,2)` | 19.5 |
| the five others | 3.4 |

Sweeping the spacing then puts the optimum at centre distance `s = 0.980`,
**diameter 1.1316** -- against the 1.1335 they quote -- with `1/p_4 = 97.1`
against their 99.  The construction is reproduced; the remaining gap is sampling
resolution and a finer spacing search.

## Two ways to beat it, both ruled out

Their note ends: "there is still some hope of beating the latter one by using
tiles with curved borders (the so-called 'wavy edges')".  Two natural families:

**Wavy borders by a perturbed metric.**  Assign each point to the centre
minimising `|x - c| + eps cos(k arg(x - c))`, which still tiles exactly.  With
`k = 6` **nothing moves at all**, and the reason is worth recording: at every
point of the boundary between two cells the perturbation adds the same amount to
both, because the six neighbour directions are all multiples of 60 degrees.  Odd
harmonics do break that symmetry, and they make things worse:

| k | eps = 0.01 | 0.02 | 0.04 |
|---|---|---|---|
| 3 | 96.0 | 89.5 | 73.4 |
| 5 | 95.1 | 85.6 | 68.6 |
| 9 | 92.9 | 75.0 | 54.0 |

**Per-colour offsets**, making one colour class larger: 95.8, 80.5, 66.0 at
offsets 0.01, 0.02, 0.04, and worse still for negative ones.

So the straight hexagon is a **local optimum** in both directions, and beating
97 needs a genuinely different family rather than a perturbation of this one.

## Honest status

The estimate of 45% for `v_5 >= 30` was too high.  What the session produced:

* a validated `p_4` evaluator, which is the tool de Grey and Parts say they
  lacked, and which is reusable for any colouring given as a rule;
* the published construction identified exactly, including the colouring they
  do not state;
* two perturbation families ruled out with numbers.

What it did not produce is a better tiling.  Reaching 104 from 97 is a 7%
improvement on a local optimum, and the other lever -- tightening `u(29)` from
103 to 98 -- is a problem in the Erdos unit-distance literature rather than this
one.
