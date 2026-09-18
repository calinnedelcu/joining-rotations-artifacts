#!/bin/sh
# The size-2 correction-set bootstrap is what made the small-part proof converge in
# the first place (route 13).  On a 380-point pool with 373 free it is cheap; turning
# it off everywhere was overcorrection from the cases where the pool was large.
cd "$(dirname "$0")/.."
P=.venv/bin/python
$P -u scripts/parts_side.py L --pool file:out/Lfreq8.pts --bound 372 --seed 61 \
   --grow 2 --pairs 400 > out/frq8p_61.log 2>&1 &
$P -u scripts/parts_side.py L --pool file:out/Lfreq6.pts --bound 372 --seed 62 \
   --grow 2 --pairs 400 > out/frq6p_62.log 2>&1 &
wait
