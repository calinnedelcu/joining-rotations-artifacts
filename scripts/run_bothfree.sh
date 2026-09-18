#!/bin/sh
# The most general formulation left: BOTH parts free, over a pool that reaches
# outside Parts' region and is still dense enough to converge.  The published
# "509 is minimum with both parts free" is over his pool only.
cd "$(dirname "$0")/.."
P=.venv/bin/python
$P -u scripts/pool_attack.py out/bothfree_d5d3.pts --start data/vtx/509.vtx \
   --bound 508 --pairs 0 --seed 120 > out/bothfree_120.log 2>&1 &
wait
