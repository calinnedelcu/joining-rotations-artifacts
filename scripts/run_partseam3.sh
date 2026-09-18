#!/bin/sh
# The remaining part variants, each against its matched interface subtype.
cd "$(dirname "$0")/.."
P=.venv/bin/python
$P -u scripts/part_seam.py L v375e1920.vtx --mask 1 --bound 13 --seed 90 \
   > out/ps_L1920.log 2>&1 &
$P -u scripts/part_seam.py L v376e1890.vtx --iso refl.rot180 --mask 0 --bound 15 --seed 91 \
   > out/ps_L1890.log 2>&1 &
$P -u scripts/part_seam.py L v375e1916.vtx --iso refl.rot180 --mask 0 --other v141e594.vtx \
   --bound 13 --seed 92 > out/ps_L1916.log 2>&1 &
wait
