#!/bin/sh
# The record together with every point that appears in several published graphs:
# dense enough for the exact search, and reaching across families, which no search
# of Parts' does.
cd "$(dirname "$0")/.."
P=.venv/bin/python
$P -u scripts/pool_attack.py out/recf6.pts --start data/vtx/509.vtx --bound 508 \
   --pairs 0 --seed 81 > out/recf6_81.log 2>&1 &
$P -u scripts/pool_attack.py out/recf5.pts --start data/vtx/509.vtx --bound 508 \
   --pairs 0 --seed 82 > out/recf5_82.log 2>&1 &
$P -u scripts/pool_attack.py out/recf4.pts --start data/vtx/509.vtx --bound 508 \
   --pairs 250 --seed 83 > out/recf4_83.log 2>&1 &
wait
