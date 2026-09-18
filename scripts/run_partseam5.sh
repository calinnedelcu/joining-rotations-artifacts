#!/bin/sh
cd "$(dirname "$0")/.."
P=.venv/bin/python
$P -u scripts/part_seam.py L v403e2112.vtx --mask 4 --bound 138 --degree 6 --seed 97 \
   > out/ps_L2112.log 2>&1 &
$P -u scripts/part_seam.py L v451e2400.vtx --mask 4 --bound 102 --degree 6 --seed 98 \
   > out/ps_L2400.log 2>&1 &
$P -u scripts/part_seam.py L v400e2034.vtx --mask 4 --other v150e639.vtx --bound 124 \
   --degree 6 --seed 99 > out/ps_L2034.log 2>&1 &
wait
