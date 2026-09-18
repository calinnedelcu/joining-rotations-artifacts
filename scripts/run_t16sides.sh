#!/bin/sh
cd "$(dirname "$0")/.."
P=.venv/bin/python
$P -u scripts/t16_sides.py out/t16_d5.pts S --seed 1 > out/t16sideS_1.log 2>&1 &
$P -u scripts/t16_sides.py out/t16_d5.pts L --seed 2 > out/t16sideL_2.log 2>&1 &
wait
