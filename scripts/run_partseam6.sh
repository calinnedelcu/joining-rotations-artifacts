#!/bin/sh
# A bound-13 cardinality problem over 540 candidates leaves the master grinding at
# a hundred seconds a call.  Raise the degree floor: fewer, denser candidates.
cd "$(dirname "$0")/.."
P=.venv/bin/python
$P -u scripts/part_seam.py L v375e1920.vtx --mask 1 --bound 13 --degree 6 --seed 110 \
   > out/ps_L1920d6.log 2>&1 &
$P -u scripts/part_seam.py L v375e1916.vtx --iso refl.rot180 --mask 0 --other v141e594.vtx \
   --bound 13 --degree 6 --seed 111 > out/ps_L1916d6.log 2>&1 &
wait
