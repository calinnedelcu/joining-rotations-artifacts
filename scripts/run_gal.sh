#!/bin/sh
# The Galois seam: 494 points of the record survive conjugating two radicals,
# 15 do not.  Free those 15 and ask for 14.  Smallest record attempt posable here.
cd "$(dirname "$0")/.."
P=.venv/bin/python
for s in 1 2 3; do
  $P -u scripts/complete_core.py out/galcore3_509.pts 494 --bound 14 --pairs 0 --search \
     --seed $s --start data/vtx/509.vtx > out/gal509_$s.log 2>&1 &
done
for s in 4 5; do
  $P -u scripts/complete_core.py out/galcore3_517.pts 491 --bound 17 --pairs 0 --search \
     --seed $s --start data/vtx/517.vtx > out/gal517_$s.log 2>&1 &
done
$P -u scripts/complete_core.py out/galcore3_510.pts 478 --bound 30 --pairs 0 --search \
   --seed 6 --start data/vtx/510.vtx > out/gal510_6.log 2>&1 &
wait
