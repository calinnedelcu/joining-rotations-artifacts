#!/bin/sh
# Start the accumulative graph from PARTS' OWN accumulative graph, not from his
# minimal one: 412 for the L side, 166 for the S side.  Choosing 373 of his 412 is
# already proven impossible, so the only way forward is to grow the accumulative
# graph PAST where his search reached -- which is what each alternative minimal
# graph found from the wider lattice does.
cd "$(dirname "$0")/.."
P=.venv/bin/python
$P -u scripts/parts_engine.py data/parts/v412e2106.vtx --companion data/parts/v136e564.vtx \
   --portion 60 --seed 11 --jitter 5 --iters 200 --time 420 --grow-time 330 --grow-set 5 \
   --tag peL412_a > out/peL412_a.log 2>&1 &
$P -u scripts/parts_engine.py data/parts/v412e2106.vtx --companion data/parts/v136e564.vtx \
   --portion 100 --seed 12 --jitter 5 --iters 200 --time 480 --grow-time 360 --grow-set 4 \
   --tag peL412_b > out/peL412_b.log 2>&1 &
$P -u scripts/parts_engine.py data/parts/v406e2082.vtx --companion data/parts/v136e564.vtx \
   --portion 70 --seed 13 --jitter 5 --iters 200 --time 420 --grow-time 330 --grow-set 5 \
   --tag peL406_a > out/peL406_a.log 2>&1 &
$P -u scripts/parts_engine.py data/parts/v166e774.vtx --companion data/parts/v374e1860.vtx \
   --companion-side L --portion 40 --seed 14 --jitter 6 --iters 200 --time 300 \
   --grow-time 240 --grow-set 6 --tag peS166_a > out/peS166_a.log 2>&1 &
$P -u scripts/parts_engine.py data/parts/v172e804.vtx --companion data/parts/v141e594.vtx \
   --companion-side L --portion 40 --seed 15 --jitter 6 --iters 200 --time 300 \
   --grow-time 240 --grow-set 6 --tag peS172_a > out/peS172_a.log 2>&1 &
wait
