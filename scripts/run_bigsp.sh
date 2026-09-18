#!/bin/sh
cd "$(dirname "$0")/.."
.venv/bin/python -u scripts/big_spindles.py --radius 3.8 --depth 4 --spindles 14 \
  > out/bigsp14.log 2>&1
