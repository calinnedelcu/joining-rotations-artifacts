#!/bin/sh
# Many randomised trims of pools that contain the record.  Each trim lands on a
# different minimal graph; the question is whether any lands under 509.  This is how
# Heule got from 1581 to 553 -- not a better method, the same method run many times
# with the formula shuffled.
cd "$(dirname "$0")/.."
P=.venv/bin/python
for s in 11 12; do
  $P -u scripts/rand_trim.py out/recf6.pts --shuffles 6 --seed $s --rounds 40 \
     --tag rt6_$s > out/rt6_$s.log 2>&1 &
done
for s in 21 22; do
  $P -u scripts/rand_trim.py out/recf4.pts --shuffles 6 --seed $s --rounds 40 \
     --tag rt4_$s > out/rt4_$s.log 2>&1 &
done
$P -u scripts/rand_trim.py out/Lunion.pts --shuffles 6 --seed 31 --rounds 40 \
   --tag rtLu > out/rtLu.log 2>&1 &
wait
