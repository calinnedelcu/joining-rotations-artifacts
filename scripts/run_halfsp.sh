#!/bin/sh
# The half-spindle generators are the principled ones -- two steps of theta_i/2
# give theta_i, so the spindle is realisable inside the lattice, which is what
# supplies the structure de Grey's argument runs on.  This sweep exists; it has
# never been run in Q(sqrt2, sqrt3), which only became readable today.
cd "$(dirname "$0")/.."
P=.venv/bin/python
HN_FIELD=2,3,5 $P -u scripts/sweep_halfspindle.py 3 2.2 > out/hs_235.log 2>&1
HN_FIELD=2,3,7 $P -u scripts/sweep_halfspindle.py 3 2.2 > out/hs_237.log 2>&1
HN_FIELD=2,5,11 $P -u scripts/sweep_halfspindle.py 3 2.2 > out/hs_2511.log 2>&1
