#!/bin/sh
# The record's other two distinct cuts.  Every seam of the 509 graph needs the
# same one point shaved off -- the seam only sets how big the search is -- so
# each distinct cut is an independent shot at the same prize.
cd "$(dirname "$0")/.."
P=.venv/bin/python
for s in 21 22; do
  $P -u scripts/complete_core.py out/galcore_rot180g7_509.pts 493 --bound 15 --pairs 0 --search \
     --seed $s --start data/vtx/509.vtx > out/gal509B_$s.log 2>&1 &
done
$P -u scripts/complete_core.py out/galcore_reflrot180g1_509.pts 484 --bound 24 --pairs 0 --search \
   --seed 23 --start data/vtx/509.vtx > out/gal509C_23.log 2>&1 &
wait
