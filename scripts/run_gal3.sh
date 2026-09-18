#!/bin/sh
# Same bound-14 target, denser pool: candidates ranked by how many colourings of
# the fixed core they kill.  Density is what decides convergence (route 13).
cd "$(dirname "$0")/.."
P=.venv/bin/python
$P -u scripts/complete_core.py out/galcore3_509_top250.pts 494 --bound 14 --pairs 0 --search \
   --seed 11 --start data/vtx/509.vtx > out/gal509t250_11.log 2>&1 &
$P -u scripts/complete_core.py out/galcore3_509_top120.pts 494 --bound 14 --pairs 0 --search \
   --seed 12 --start data/vtx/509.vtx > out/gal509t120_12.log 2>&1 &
$P -u scripts/complete_core.py out/galcore3_517_top250.pts 491 --bound 17 --pairs 0 --search \
   --seed 13 --start data/vtx/517.vtx > out/gal517t250_13.log 2>&1 &
wait
