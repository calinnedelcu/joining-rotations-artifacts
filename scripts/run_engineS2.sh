#!/bin/sh
# Matched subtypes: m6b is 374e1864 with 141e594 (accumulative S 172e804);
# m6c is 374e1872 with 150e639 (accumulative S 167e772).
cd "$(dirname "$0")/.."
P=.venv/bin/python
$P -u scripts/parts_engine.py out/S172rot.pts --companion data/parts/v374e1864.vtx \
   --companion-side L --portion 40 --seed 23 --jitter 6 --iters 200 --time 300 \
   --grow-time 240 --grow-set 6 --tag peS172 > out/peS172.log 2>&1 &
$P -u scripts/parts_engine.py out/S167rot.pts --companion data/parts/v374e1872.vtx \
   --companion-side L --portion 40 --seed 24 --jitter 6 --iters 200 --time 300 \
   --grow-time 240 --grow-set 6 --tag peS167 > out/peS167.log 2>&1 &
wait
