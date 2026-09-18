#!/bin/sh
# The synthesis: Heule's randomisation supplies distinct minimal graphs, Parts'
# accumulation unions them, and the exact master searches the union.  None of the
# three alone gets under 509; the union of several independently-found minimal
# graphs is ground no single trim or proof has covered.
cd "$(dirname "$0")/.."
P=.venv/bin/python
$P -u scripts/pool_attack.py out/accA.pts --start data/vtx/509.vtx --bound 508 \
   --pairs 0 --seed 111 > out/accA_111.log 2>&1 &
$P -u scripts/pool_attack.py out/accB.pts --start data/vtx/509.vtx --bound 508 \
   --pairs 0 --seed 112 > out/accB_112.log 2>&1 &
$P -u scripts/pool_attack.py out/accC.pts --start data/vtx/509.vtx --bound 508 \
   --pairs 0 --seed 113 > out/accC_113.log 2>&1 &
wait
