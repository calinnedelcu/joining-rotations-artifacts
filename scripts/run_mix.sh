#!/bin/sh
cd "$(dirname "$0")/.."
P=.venv/bin/python
$P -u scripts/pool_attack.py out/recf4.pts --start data/vtx/509.vtx --bound 508 \
   --pairs 0 --seed 91 > out/recf4_91.log 2>&1 &
$P -u scripts/pool_attack.py out/recf3.pts --start data/vtx/509.vtx --bound 508 \
   --pairs 0 --seed 92 > out/recf3_92.log 2>&1 &
$P -u scripts/descend_t16.py results/theta16/t16_best.pts --seed 31 \
   --fracs 0.9,0.97,0.8,0.95,0.99,0.9,0.97,0.995,0.93,0.98,1.0,0.99,0.96 \
   > out/t16d31.log 2>&1 &
$P -u scripts/t16_side_descend.py results/theta16/t16_best.pts S --seed 32 \
   > out/t16sdS32.log 2>&1 &
wait
