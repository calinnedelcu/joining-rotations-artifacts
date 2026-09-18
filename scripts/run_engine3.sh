#!/bin/sh
# GRAPH is the accumulative pool, --minimal sets the bound.  Choosing 373 of his 412
# is already proven impossible, so every iteration that grows the accumulative graph
# past 412 is ground his own search never covered.
cd "$(dirname "$0")/.."
P=.venv/bin/python
$P -u scripts/parts_engine.py data/parts/v412e2106.vtx --minimal data/parts/v374e1860.vtx \
   --companion data/parts/v136e564.vtx --portion 60 --seed 31 --jitter 5 --iters 200 \
   --time 420 --grow-time 330 --grow-set 5 --tag peL_a > out/peL_a.log 2>&1 &
$P -u scripts/parts_engine.py data/parts/v412e2106.vtx --minimal data/parts/v374e1868.vtx \
   --companion data/parts/v136e564.vtx --portion 100 --seed 32 --jitter 5 --iters 200 \
   --time 480 --grow-time 360 --grow-set 4 --tag peL_b > out/peL_b.log 2>&1 &
$P -u scripts/parts_engine.py data/parts/v406e2082.vtx --minimal data/parts/v374e1860.vtx \
   --companion data/parts/v136e564.vtx --portion 70 --seed 33 --jitter 5 --iters 200 \
   --time 420 --grow-time 330 --grow-set 5 --tag peL_c > out/peL_c.log 2>&1 &
$P -u scripts/parts_engine.py out/S166rot.pts --minimal data/parts/v136e564.vtx \
   --companion data/parts/v374e1860.vtx --companion-side L --portion 40 --seed 34 \
   --jitter 6 --iters 200 --time 300 --grow-time 240 --grow-set 6 --tag peS_a \
   > out/peS_a.log 2>&1 &
$P -u scripts/parts_engine.py out/S172rot.pts --minimal data/parts/v141e594.vtx \
   --companion data/parts/v374e1864.vtx --companion-side L --portion 40 --seed 35 \
   --jitter 6 --iters 200 --time 300 --grow-time 240 --grow-set 6 --tag peS_b \
   > out/peS_b.log 2>&1 &
wait
