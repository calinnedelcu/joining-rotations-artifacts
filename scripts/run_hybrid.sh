#!/bin/sh
# The record's own shape: symmetric bulk by orbit, breakers by point.
cd "$(dirname "$0")/.."
P=.venv/bin/python
$P -u scripts/hybrid_orbit.py --ring 1 --seed 1 --bound 508 > out/hyb1_1.log 2>&1 &
$P -u scripts/hybrid_orbit.py --ring 2 --seed 2 --bound 508 > out/hyb2_2.log 2>&1 &
wait
