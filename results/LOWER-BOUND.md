# v5 >= 29, from two published results nobody has combined

> **BOTH INPUTS VERIFIED VERBATIM FROM THE SOURCE PAPERS, 14 Sep 2026.**
>
> * de Grey & Parts, arXiv:2303.14714, "On lower bounds of the order of
>   k-chromatic unit distance graphs", final line of the Improvements section:
>   *"As a result, we get the bounds: e5 >= 99, v5 >= 28, e6 >= 182, v6 >= 42."*
>   Their edge->vertex conversion uses Agoston-Palvolgyi, whose table gives
>   e <= 97 at v = 27 and e <= 102 at v = 28 -- which is exactly why 27 was
>   excluded and 28 survived for them.
> * Alexeev, Mixon & Parshall, arXiv:2412.11914v2, part (b) of their theorem:
>
>       n        22  23  24  25  26  27  28  29  30
>       u(n) >=  60  64  68  72  76  81  85  89  93
>       u(n) <=  61  66  72  78  84  90  96  103 110
>
> so u(28) <= 96 < 99. A literature search on 14 Sep 2026 found no publication
> stating v5 >= 29; MathWorld's Hadwiger-Nelson page, updated August 2026, does
> not mention it.

The published lower bound on the number of vertices of a 5-chromatic
unit-distance graph in the plane is **v5 >= 28**, due to de Grey and Parts,
Geombinatorics 32(2) 2022, arXiv:2303.14714. It improves to **29** immediately,
with no new computation, by combining that paper's edge bound with a later
result on the Erdos unit-distance problem for small point sets.

## The argument

Write u(n) for the maximum number of unit distances among n points in the plane,
and e5 for the minimum number of edges of a 5-chromatic unit-distance graph.

1. **e5 >= 99.** de Grey and Parts, Geombinatorics 32(2) 2022, obtained by their
   refinement of the Pritikin uncovered-density scheme and the Gwyn-Stavrianos
   badness argument. Their own vertex bound in the same paper is v5 >= 28.
2. **u(28) <= 96.** Alexeev, Mixon and Parshall, "The Erdos unit distance
   problem for small point sets", arXiv:2412.11914v2, February 2025. They
   determine u(16..21) exactly as 41, 43, 46, 50, 54, 57 and give upper bounds
   for n = 22..30 of 61, 66, 72, 78, 84, 90, 96, 103, 110.
3. **u is non-decreasing**, since adding a point never removes a unit distance.

A 5-chromatic unit-distance graph on n <= 28 vertices would have at most
u(n) <= u(28) <= 96 edges, and 96 < 99. So no such graph exists and v5 >= 29.

The bound is exactly 29 by this route and no further: u(29) <= 103, which does
not contradict e5 >= 99.

## Why it was missed

de Grey and Parts' paper is from March 2023 and predates Alexeev-Mixon-Parshall
by two years. For the conversion they used the older Agoston-Palvolgyi values,
which give 97 edges at 27 vertices and 102 at 28, so 28 survived. The 2025
values are strictly better at every n in the relevant range, and 28 no longer
does.

## What it would take to go further, quantified

With e5 >= 99 held fixed, the arithmetic needs:

| target | requires |
|---|---|
| v5 >= 30 | u(29) <= 98, i.e. 5 better than the current 103 |
| v5 >= 31 | u(30) <= 98, i.e. 12 better than the current 110 |

Two independent levers, both engineering rather than new theory:

**Tighten u(29) and u(30).** No colouring work at all, purely the Erdos
unit-distance problem for 29 and 30 points. Alexeev-Mixon-Parshall's own lower
bounds leave room: they do not exclude u(29) = 89 or u(30) = 93, both under 99.
Pinning either near its lower bound gives v5 >= 31 at once. Their pipeline is
nauty enumeration of graphs free of Globus-Parshall's 74 minimal forbidden
subgraphs on at most 9 vertices, Schade's dense-subgraph recursion, a totally
unfaithful filter, and a custom embedder.

**Lower p4 by about 5 percent.** e5 >= 104 needs p4 < 1/104 = 0.0096154 against
the current value near 1/99. de Grey and Parts name their own bottleneck: they
write that they "encountered some problems with the numerical integration
function NIntegrate in the general case, and were forced to limit ourselves to
relatively simple tilings", and they nominate tilings with wavy borders as the
promising family. For a polygonal tiling the integrand of

    p_k = (1/(2 pi S)) integral_S d sigma integral_0^{2 pi} d phi M_k(sigma, phi)

is piecewise constant, so p4 is an exact finite sum of cell measures and can be
computed by planar arrangement rather than quadrature, which removes the
obstacle they hit.


## The strongest lever, restated after verifying the sources

Raising e5 moves v5 directly against the AMP table, with no new unit-distance
work at all:

    e5 >= 104  =>  u(29) <= 103 < 104  =>  v5 >= 30
    e5 >= 111  =>  u(30) <= 110 < 111  =>  v5 >= 31

and e5 >= 99 is itself a published number, so this moves TWO at once.

de Grey and Parts state their own bottleneck in print: they compute
p_k by numerical integration and *"encountered some problems with the numerical
integration function NIntegrate in the general case, and were forced to limit
ourselves to relatively simple tilings"*.  For a POLYGONAL tiling M_k(sigma, phi)
is piecewise constant, so p_k is an exact finite sum of cell measures and can be
evaluated by planar arrangement rather than quadrature.  That removes the
obstacle they name, and opens the richer tilings they could not reach.
