#!/bin/sh
cd "$(dirname "$0")/.."
P=.venv/bin/python
for s in 1 2 3; do
  $P -u scripts/exploit_83.py --bound 141 --seed $s > out/ex83_$s.log 2>&1 &
done
wait
