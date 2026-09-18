#!/bin/sh
# --pairs 0: the size-2 correction-set bootstrap enumerates tens of thousands of
# pairs, each a SAT call.  It sharpens a PROOF and does nothing for a hunt, so a
# search that wants a graph should go straight to the loop.
cd "$(dirname "$0")/.."
P=.venv/bin/python
$P -u scripts/parts_side.py L --pool file:out/wideL_d5.pts --bound 372 --seed 53 \
   --grow 2 --pairs 0 > out/wideL5_53.log 2>&1 &
$P -u scripts/parts_side.py L --pool file:out/wideL_d4.pts --bound 372 --seed 64 \
   --grow 3 --pairs 0 > out/wideL4_64.log 2>&1 &
$P -u scripts/parts_side.py S --pool file:out/wideS_d2.pts --bound 134 --seed 71 \
   --grow 2 --pairs 0 > out/wideS2_71.log 2>&1 &
wait
