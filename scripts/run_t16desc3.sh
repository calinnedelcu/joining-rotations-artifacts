#!/bin/sh
# sample_descend only ever advances through its schedule, so a short aggressive
# list exhausts itself and stops early.  A long mixed schedule lets it come back to
# gentler slices after an aggressive one fails, which is what keeps it moving on a
# pool still far above minimal.
cd "$(dirname "$0")/.."
P=.venv/bin/python
$P -u scripts/descend_t16.py out/t16_d5.pts --seed 11 \
   --fracs 0.9,0.97,0.8,0.95,0.99,0.9,0.97,0.995,0.93,0.98,1.0,0.99,0.96,0.9,0.995 \
   > out/t16desc_11.log 2>&1 &
$P -u scripts/descend_t16.py out/t16_d5.pts --seed 12 \
   --fracs 0.8,0.9,0.95,0.7,0.9,0.98,0.85,0.95,0.99,0.9,0.995,0.97,1.0,0.99,0.96 \
   > out/t16desc_12.log 2>&1 &
$P -u scripts/descend_t16.py out/t16_d5.pts --seed 13 \
   --fracs 0.95,0.99,0.9,0.98,0.995,0.93,0.97,1.0,0.99,0.95,0.9,0.98,0.995,0.97,0.99 \
   > out/t16desc_13.log 2>&1 &
wait
