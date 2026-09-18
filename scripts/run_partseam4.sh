#!/bin/sh
# Parts' accumulative large parts have small seam cores -- 223 of 406, 235 of 412 --
# so the search has real freedom where the minimal parts have almost none.  A high
# degree floor keeps the candidate set in the density regime that converges.
cd "$(dirname "$0")/.."
P=.venv/bin/python
$P -u scripts/part_seam.py L v406e2082.vtx --mask 4 --bound 150 --degree 6 --seed 95 \
   > out/ps_L2082.log 2>&1 &
$P -u scripts/part_seam.py L v412e2106.vtx --mask 4 --bound 138 --degree 6 --seed 96 \
   > out/ps_L2106.log 2>&1 &
wait
