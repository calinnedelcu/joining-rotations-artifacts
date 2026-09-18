#!/bin/sh
# de Grey, Polymath16 thread 18, 13 Sep 2026: "using more than just two sets of 42
# vectors.  Anyone want to have a go?"  Two sets is Haugland's; three and four are
# the extension.  theta_4 needs sqrt15, hence conductor 420.
cd "$(dirname "$0")/.."
P=.venv/bin/python
$P -u scripts/haugland_sets.py --sets 2 --depth 2 --radius 2.2 > out/hg2.log 2>&1 &
$P -u scripts/haugland_sets.py --sets 3 --depth 2 --radius 2.2 > out/hg3.log 2>&1 &
$P -u scripts/haugland_sets.py --sets 4 --depth 2 --radius 2.2 > out/hg4.log 2>&1 &
$P -u scripts/haugland_sets.py --sets 3 --depth 2 --radius 1.6 > out/hg3b.log 2>&1 &
$P -u scripts/haugland_sets.py --sets 6 --depth 2 --radius 1.6 > out/hg6.log 2>&1 &
wait
