#!/bin/sh
# The heptagonal union flips from instant to intractable between 2857 and 3193
# points.  In colouring, the hardest instances sit at the chromatic threshold, so
# that is where the 4/5 boundary should be.  Long runs, to decide it.
cd "$(dirname "$0")/.."
P=.venv/bin/python
$P -u scripts/haugland_sets.py --sets 2 --depth 2 --radius 1.25 > out/bs125.log 2>&1 &
$P -u scripts/haugland_sets.py --sets 2 --depth 2 --radius 1.30 > out/bs130.log 2>&1 &
$P -u scripts/haugland_sets.py --sets 2 --depth 2 --radius 1.35 > out/bs135.log 2>&1 &
$P -u scripts/haugland_sets.py --sets 3 --depth 2 --radius 1.25 > out/bs3_125.log 2>&1 &
wait
