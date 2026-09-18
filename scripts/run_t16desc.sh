#!/bin/sh
cd "$(dirname "$0")/.."
P=.venv/bin/python
for s in 2 3 4; do
  $P -u scripts/descend_t16.py out/t16_s0.pts --seed $s > out/t16desc_$s.log 2>&1 &
done
wait
