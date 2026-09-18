#!/bin/sh
# The heptagonal lattice under the rotation no quadratic field can express.
cd "$(dirname "$0")/.."
P=.venv/bin/python
for r in 2.2 2.0 1.8; do
  $P -u scripts/cyclo_sweep.py --depth 3 --radius $r > out/cyc42_d3_r$r.log 2>&1
done
$P -u scripts/cyclo_sweep.py --conductor 84 --depth 2 --radius 2.2 > out/cyc84_d2.log 2>&1
