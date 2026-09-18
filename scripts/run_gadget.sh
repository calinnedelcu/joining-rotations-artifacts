#!/bin/sh
# Minimise the distance-2 forcer in Q(sqrt2, sqrt3).  Everything on this route
# depends on it: the total is forcer + killer, the classical pair is 374 + 136,
# so the forcer has to come under about 374 for the field to be worth anything.
cd "$(dirname "$0")/.."
P=.venv/bin/python
for s in 0 1; do
  $P -u scripts/shrink_gadget.py data/vtx/T721.vtx --primes 2,3,5 --pair 0,1 --seed $s \
     > out/gadgetT721_$s.log 2>&1 &
done
wait
