#!/bin/sh
# Price the partner gadget at each distance Parts priced only one side of.
cd "$(dirname "$0")/.."
P=.venv/bin/python
$P -u scripts/pair_gadget.py --pair 8_3  --mode nonmono --bound 143 --seed 1 --exact > out/pg_8_3.log 2>&1 &
$P -u scripts/pair_gadget.py --pair 7_3  --mode mono    --bound 191 --seed 2 --exact > out/pg_7_3.log 2>&1 &
$P -u scripts/pair_gadget.py --pair 5_3  --mode mono    --bound 195 --seed 3 --exact > out/pg_5_3.log 2>&1 &
$P -u scripts/pair_gadget.py --pair r11r3 --mode mono   --bound 202 --seed 4 --exact > out/pg_r11r3.log 2>&1 &
wait
