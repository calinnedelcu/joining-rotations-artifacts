#!/bin/sh
cd "$(dirname "$0")/.."
P=.venv/bin/python
$P -u scripts/t16_side_descend.py results/theta16/t16_best.pts S --seed 1 > out/t16sd_S1.log 2>&1 &
$P -u scripts/t16_side_descend.py results/theta16/t16_best.pts L --seed 2 > out/t16sd_L2.log 2>&1 &
wait
