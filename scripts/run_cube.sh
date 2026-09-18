#!/bin/sh
cd "$(dirname "$0")/.."
P=.venv/bin/python
$P -u scripts/haugland_sets.py --sets 2 --depth 2 --radius 1.35 --cube 8 --procs 9 \
   > out/cube135.log 2>&1
$P -u scripts/haugland_sets.py --sets 2 --depth 2 --radius 1.6 --cube 8 --procs 9 \
   > out/cube160.log 2>&1
