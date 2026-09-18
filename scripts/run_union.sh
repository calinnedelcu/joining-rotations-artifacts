#!/bin/sh
# The union of every published part-graph is an accumulative graph larger than any
# one of his, and no search of his ranged over it.  L side: 613 points, answer 61%.
cd "$(dirname "$0")/.."
P=.venv/bin/python
for s in 41 42; do
  $P -u scripts/parts_side.py L --pool file:out/Lunion.pts --bound 372 --seed $s \
     --grow 2 --pairs 0 > out/uniL_$s.log 2>&1 &
done
$P -u scripts/parts_side.py L --pool file:out/Lunion.pts --bound 372 --seed 43 \
   --grow 3 --pairs 300 > out/uniL_43.log 2>&1 &
for s in 44 45; do
  $P -u scripts/parts_side.py S --pool file:out/Sunion_rot.pts --bound 134 --seed $s \
     --grow 2 --pairs 0 > out/uniS_$s.log 2>&1 &
done
wait
