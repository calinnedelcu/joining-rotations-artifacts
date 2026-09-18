#!/bin/sh
cd "$(dirname "$0")/.."
.venv/bin/python -u scripts/classify_joins.py --amax 60 --bmax 12 --time 5400 \
  > out/classify_joins.log 2>&1 &
wait
