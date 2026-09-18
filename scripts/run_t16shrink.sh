#!/bin/sh
cd "$(dirname "$0")/.."
P=.venv/bin/python
for s in 0 1; do
  $P -u scripts/shrink_t16.py --radius 4.0 --seed $s > out/t16shrink_$s.log 2>&1 &
done
wait
