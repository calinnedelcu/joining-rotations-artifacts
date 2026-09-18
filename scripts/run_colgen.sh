#!/bin/sh
# The pools the learned colourings chose for themselves.  Every other pool here is
# filtered by density against the record's own large part, so a large part that does
# not resemble L_374 has never been inside one.  These were built on 13 September and
# never searched -- the attacks were killed the same hour to free cores.
cd "$(dirname "$0")/.."
P=.venv/bin/python
for r in 1 2 3 4; do
  $P -u scripts/pool_attack.py out/colgen_r$r.pts --start data/vtx/509.vtx --bound 508 \
     --pairs 0 --seed $((120+r)) > out/cg_r$r.log 2>&1 &
done
wait
