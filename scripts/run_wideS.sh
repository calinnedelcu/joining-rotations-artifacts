#!/bin/sh
# The dual of route 42: the small part over a wide dense pool, L_374 fixed.
# Record is 374 fixed + 135 free = 509, so the bound that beats it is 134.
cd "$(dirname "$0")/.."
P=.venv/bin/python
$P -u scripts/parts_side.py S --pool file:out/wideS_d2.pts --bound 134 --seed 71 \
   --grow 2 --pairs 300 > out/wideS2_71.log 2>&1 &
$P -u scripts/parts_side.py S --pool file:out/wideS_d3.pts --bound 134 --seed 72 \
   --grow 2 --pairs 300 > out/wideS3_72.log 2>&1 &
wait
