#!/bin/sh
# The S part only meets L after the joining rotation, so the engine must be given
# it already rotated -- otherwise the working graph is simply not 5-chromatic.
cd "$(dirname "$0")/.."
P=.venv/bin/python
$P -u scripts/parts_engine.py out/S166rot.pts --companion data/parts/v374e1860.vtx \
   --companion-side L --portion 40 --seed 21 --jitter 6 --iters 200 --time 300 \
   --grow-time 240 --grow-set 6 --tag peS166 > out/peS166.log 2>&1 &
$P -u scripts/parts_engine.py out/S172rot.pts --companion data/parts/v141e594.vtx \
   --companion-side L --portion 40 --seed 22 --jitter 6 --iters 200 --time 300 \
   --grow-time 240 --grow-set 6 --tag peS172 > out/peS172.log 2>&1 &
wait
