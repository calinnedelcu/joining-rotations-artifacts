#!/bin/sh
# Further outside Parts' region (radius 3.0), and a pool grown around a different
# minimal large part, so the dense region is a different one.
cd "$(dirname "$0")/.."
P=.venv/bin/python
$P -u scripts/parts_side.py L --pool file:out/wideL_r30d5.pts --bound 372 --seed 101 \
   --grow 2 --pairs 0 > out/wideR30_101.log 2>&1 &
$P -u scripts/parts_side.py L --pool file:out/wideL_1868d5.pts --bound 372 --seed 102 \
   --grow 2 --pairs 0 --Lfile v374e1868.vtx > out/wide1868_102.log 2>&1 &
$P -u scripts/parts_side.py L --pool file:out/wideL_d3.pts --bound 372 --seed 103 \
   --grow 3 --pairs 0 > out/wideD3_103.log 2>&1 &
wait
