#!/bin/sh
# Matching interface subtypes: m6a pairs 374e1860/1868 with 136e564, m6b pairs
# 374e1864 with 141e594, m6c pairs 374e1872 with 150e639.  The m6b pair has a
# baseline of 514, so beating 509 needs |L| <= 368 against S=141 (core 360, bound
# 8) or |S| <= 135 against L=374 (core 133, bound 2).
cd "$(dirname "$0")/.."
P=.venv/bin/python
$P -u scripts/part_seam.py S v141e594.vtx --iso refl.rot120 --mask 5 --other v374e1864.vtx \
   --bound 2 --degree 3 --seed 85 > out/ps_S141.log 2>&1 &
$P -u scripts/part_seam.py L v374e1864.vtx --iso refl.rot300 --mask 0 --other v141e594.vtx \
   --bound 8 --seed 86 > out/ps_L1864b.log 2>&1 &
$P -u scripts/part_seam.py S v136e564.vtx --mask 1 --bound 8 --degree 2 --seed 87 \
   > out/ps_S136w.log 2>&1 &
wait
