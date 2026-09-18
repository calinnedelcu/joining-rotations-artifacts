#!/bin/sh
# Galois symmetry imposed on the search.  Unlike a rotation it is not an isometry,
# so a symmetric graph pays no geometric price -- and the record is only 15 points
# away from having it, against 52 for the rotation.
cd "$(dirname "$0")/.."
P=.venv/bin/python
for s in 41 42; do
  $P -u scripts/gal_symmetric.py --mask 3 --bound 508 --seed $s > out/galsym509_$s.log 2>&1 &
done
$P -u scripts/gal_symmetric.py --graph data/vtx/517.vtx --mask 3 --bound 508 --seed 43 \
   > out/galsym517_43.log 2>&1 &
wait
