#!/bin/sh
# The UNSAT at bound 14 is only as strong as the candidate set it ranged over:
# 685 lattice points with 4 or more neighbours in the core.  A completion of 14
# points can give a new point up to 13 of its neighbours from among the other new
# points, so the degree-4 floor is not forced -- widen it and ask again.
cd "$(dirname "$0")/.."
P=.venv/bin/python
for s in 31 32; do
  $P -u scripts/complete_core.py out/galcore3_509_d3.pts 494 --bound 14 --pairs 0 --search \
     --seed $s --start data/vtx/509.vtx > out/gal509d3_$s.log 2>&1 &
done
$P -u scripts/complete_core.py out/galcore3_509_d2.pts 494 --bound 14 --pairs 0 --search \
   --seed 33 --start data/vtx/509.vtx > out/gal509d2_33.log 2>&1 &
wait
