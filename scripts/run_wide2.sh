#!/bin/sh
# More density, and a second seed on the densest pools.
cd "$(dirname "$0")/.."
P=.venv/bin/python
$P -u scripts/parts_side.py L --pool file:out/wideL_d7.pts --bound 372 --seed 61 \
   --grow 2 --pairs 0 > out/wideL7_61.log 2>&1 &
$P -u scripts/parts_side.py L --pool file:out/wideL_d6.pts --bound 372 --seed 62 \
   --grow 2 --pairs 300 > out/wideL6_62.log 2>&1 &
$P -u scripts/parts_side.py L --pool file:out/wideL_d7.pts --bound 372 --seed 63 \
   --grow 3 --pairs 300 > out/wideL7_63.log 2>&1 &
wait
