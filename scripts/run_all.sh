#!/bin/sh
# Every point of every published 5-chromatic construction, in one pool.  Nothing in
# the literature searches across families -- each of Parts' searches sat inside one.
cd "$(dirname "$0")/.."
P=.venv/bin/python
$P -u scripts/pool_attack.py out/allparts.pts --start data/vtx/509.vtx --bound 508 \
   --pairs 0 --seed 71 > out/allp_71.log 2>&1 &
$P -u scripts/pool_attack.py out/allf2.pts --start data/vtx/509.vtx --bound 508 \
   --pairs 0 --seed 72 > out/allf2_72.log 2>&1 &
$P -u scripts/pool_attack.py out/allf3.pts --start data/vtx/509.vtx --bound 508 \
   --pairs 0 --seed 73 > out/allf3_73.log 2>&1 &
wait
