#!/bin/sh
# The one thing route 2 leaves open: a large-part pool outside Parts' region that
# is still dense enough to converge.  S_136 fixed, bound 373, so a hit is 508.
cd "$(dirname "$0")/.."
P=.venv/bin/python
$P -u scripts/parts_side.py L --pool file:out/wideL_d6.pts --bound 372 --seed 51 \
   --grow 2 --pairs 0 > out/wideL6_51.log 2>&1 &
$P -u scripts/parts_side.py L --pool file:out/wideL_d5.pts --bound 372 --seed 52 \
   --grow 2 --pairs 0 > out/wideL5_52.log 2>&1 &
$P -u scripts/parts_side.py L --pool file:out/wideL_d5.pts --bound 372 --seed 53 \
   --grow 2 --pairs 250 > out/wideL5_53.log 2>&1 &
$P -u scripts/parts_side.py L --pool file:out/wideL_d4.pts --bound 372 --seed 54 \
   --grow 2 --pairs 0 > out/wideL4_54.log 2>&1 &
wait
