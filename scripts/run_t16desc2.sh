#!/bin/sh
cd "$(dirname "$0")/.."
P=.venv/bin/python
$P -u scripts/descend_t16.py out/t16_s0.pts --seed 5 --fracs 0.97,0.94,0.9,0.85,0.8 \
   > out/t16desc_5.log 2>&1 &
$P -u scripts/descend_t16.py out/t16_s0.pts --seed 6 --fracs 0.9,0.8,0.7,0.6 \
   > out/t16desc_6.log 2>&1 &
wait
