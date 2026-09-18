#!/bin/sh
# Supervise a batch of long searches as children of one process.
#
# Background jobs started with nohup from a one-shot shell do not survive here:
# the process group goes away with the shell that launched it, and a search that
# needs hours dies in seconds with no traceback (its log just stops after the
# pool line).  Everything long therefore runs as a child of this script, which
# waits, so the batch lives exactly as long as the task supervising it.
cd "$(dirname "$0")/.."
P=.venv/bin/python
for s in 10 11 12 13; do
  $P -u scripts/complete_core.py out/symcore.pts 457 \
     --bound 51 --pairs 0 --search --seed $s > out/cs4_$s.log 2>&1 &
done
for s in 20 21; do
  $P -u scripts/complete_core.py out/symcore510.pts 466 \
     --bound 42 --pairs 0 --search --seed $s --start data/vtx/510.vtx > out/cs510_$s.log 2>&1 &
done
$P -u scripts/complete_core.py out/symcore517.pts 505 \
   --bound 3 --pairs 0 --search --seed 30 --start data/vtx/517.vtx > out/cs517_30.log 2>&1 &
wait
