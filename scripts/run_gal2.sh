#!/bin/sh
# The second bound-14 target: 510 cut along rot60 o galois7, a different core
# from the 509 seam, so a different search with the same prize.
cd "$(dirname "$0")/.."
P=.venv/bin/python
for s in 7 8; do
  $P -u scripts/complete_core.py out/galcore_rot60g7_510.pts 494 --bound 14 --pairs 0 --search \
     --seed $s --start data/vtx/510.vtx > out/gal510b_$s.log 2>&1 &
done
wait
