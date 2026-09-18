#!/bin/sh
cd "$(dirname "$0")/.."
P=.venv/bin/python
for s in 43 46 47; do
  $P -u scripts/parts_side.py L --pool file:out/Lunion.pts --bound 372 --seed $s \
     --grow 3 --pairs 0 > out/uniL_$s.log 2>&1 &
done
wait
