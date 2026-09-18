#!/bin/sh
# A ladder of accumulative pools by how many published L-graphs each point appears
# in: 208 of the 613 union points are in all fourteen.  Dense rungs settle fast and
# narrowly, loose ones reach further and take longer.
cd "$(dirname "$0")/.."
P=.venv/bin/python
$P -u scripts/parts_side.py L --pool file:out/Lfreq8.pts --bound 372 --seed 51 \
   --grow 2 --pairs 0 > out/frq8_51.log 2>&1 &
$P -u scripts/parts_side.py L --pool file:out/Lfreq6.pts --bound 372 --seed 52 \
   --grow 2 --pairs 0 > out/frq6_52.log 2>&1 &
$P -u scripts/parts_side.py L --pool file:out/Lfreq5.pts --bound 372 --seed 53 \
   --grow 2 --pairs 0 > out/frq5_53.log 2>&1 &
$P -u scripts/parts_side.py L --pool file:out/Lfreq4.pts --bound 372 --seed 54 \
   --grow 3 --pairs 0 > out/frq4_54.log 2>&1 &
wait
