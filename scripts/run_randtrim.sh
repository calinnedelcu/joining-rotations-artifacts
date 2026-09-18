#!/bin/sh
cd "$(dirname "$0")/.."
P=.venv/bin/python
$P -u scripts/rand_trim.py results/theta16/t16_best.pts --field 3,7,11 --shuffles 6 \
   --seed 1 --tag rt16_a > out/rt16_a.log 2>&1 &
$P -u scripts/rand_trim.py results/theta16/t16_best.pts --field 3,7,11 --shuffles 8 \
   --seed 2 --tag rt16_b > out/rt16_b.log 2>&1 &
$P -u scripts/rand_trim.py out/allparts.pts --field 3,5,11 --shuffles 8 \
   --seed 3 --tag rtall > out/rtall.log 2>&1 &
wait
