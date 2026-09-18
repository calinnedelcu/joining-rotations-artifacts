#!/bin/sh
# Parts' own arithmetic filter on candidates: writing a vertex as
# (a + b sqrt33 + i c sqrt3 + i d sqrt11)/(4 * 3^h), he reports that every useful
# orbit satisfies abcd = 0.  It cuts 7757 lattice candidates to 1965, and it selects
# a different set from any degree heuristic.
cd "$(dirname "$0")/.."
P=.venv/bin/python
$P -u scripts/parts_side.py L --pool file:out/Labcd4.pts --bound 372 --seed 101 \
   --grow 2 --pairs 0 > out/abcd4_101.log 2>&1 &
$P -u scripts/parts_side.py L --pool file:out/Labcd3.pts --bound 372 --seed 102 \
   --grow 2 --pairs 0 > out/abcd3_102.log 2>&1 &
wait
