#!/bin/sh
# Parts' loop with this repository's exact reduction: expand the accumulative graph
# by a random portion of the degree-ordered reserve, then prove or beat the bound on
# that dense window.  Different portions and seeds see different windows.
cd "$(dirname "$0")/.."
P=.venv/bin/python
$P -u scripts/parts_engine.py data/vtx/509.vtx --portion 60  --seed 1 --jitter 4 \
   --iters 400 --time 420 --tag pe509_a > out/pe509_a.log 2>&1 &
$P -u scripts/parts_engine.py data/vtx/509.vtx --portion 90  --seed 2 --jitter 4 \
   --iters 400 --time 420 --tag pe509_b > out/pe509_b.log 2>&1 &
$P -u scripts/parts_engine.py data/vtx/509.vtx --portion 120 --seed 3 --jitter 5 \
   --iters 400 --time 480 --tag pe509_c > out/pe509_c.log 2>&1 &
$P -u scripts/parts_engine.py data/vtx/509.vtx --portion 45  --seed 4 --jitter 6 \
   --iters 400 --time 360 --tag pe509_d > out/pe509_d.log 2>&1 &
$P -u scripts/parts_engine.py data/vtx/510.vtx --portion 90  --seed 5 --jitter 4 \
   --iters 400 --time 420 --tag pe510_a > out/pe510_a.log 2>&1 &
$P -u scripts/parts_engine.py results/theta16/t16_best.pts --field 3,7,11 --rot i:16 \
   --radius 4.0 --portion 80 --seed 6 --jitter 3 --iters 200 --time 600 --tag pet16 \
   > out/pet16.log 2>&1 &
wait
