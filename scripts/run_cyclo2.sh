#!/bin/sh
# Low Z-rank cyclotomic lattices: the classical lattice has rank 8, and rank is
# what controls how often two lattice points land at distance exactly 1.  Rank 12
# (zeta_42) is too thin at 5.1 edges per point; rank 6 reaches 5.0 at a twentieth
# of the size, and admits theta_2 (zeta_14) or theta_7 (zeta_18).
cd "$(dirname "$0")/.."
P=.venv/bin/python
for spec in "14 5" "14 6" "18 5" "18 6" "36 4" "21 5" "28 4"; do
  set -- $spec
  $P -u scripts/cyclo_sweep.py --conductor $1 --depth $2 --radius 2.2 \
     > out/cyc$1_d$2.log 2>&1
done
