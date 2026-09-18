#!/bin/sh
cd "$(dirname "$0")/.."
.venv/bin/python -u scripts/rational_spindles.py --depth 4 --radius 5.05 \
  --only 5/9,7/3,13/3,31/3,71/9,11/9,4/3,13/9,5/3,16/9 > out/ratsp.log 2>&1
