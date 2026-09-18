#!/bin/sh
# The parts split far more tightly than the whole graph.  Fix a part's seam core
# AND the other part at its published value, then ask for one point fewer than the
# record spends.  A hit is 508 vertices.
cd "$(dirname "$0")/.."
P=.venv/bin/python
$P -u scripts/part_seam.py L v374e1868.vtx --mask 1 --bound 1  --seed 80 > out/ps_L1868.log 2>&1 &
$P -u scripts/part_seam.py L v374e1860.vtx --mask 1 --bound 5  --seed 81 > out/ps_L1860.log 2>&1 &
$P -u scripts/part_seam.py L v374e1872.vtx --mask 1 --bound 7  --seed 82 > out/ps_L1872.log 2>&1 &
$P -u scripts/part_seam.py L v374e1864.vtx --iso refl.rot300 --mask 0 --bound 13 --seed 83 > out/ps_L1864.log 2>&1 &
$P -u scripts/part_seam.py S v136e564.vtx  --mask 1 --bound 8  --seed 84 > out/ps_S136.log 2>&1 &
wait
