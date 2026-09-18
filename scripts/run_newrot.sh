#!/bin/sh
cd "$(dirname "$0")/.."
.venv/bin/python -u scripts/new_rotations.py --radius 4.0 --depth 4 \
  --fields 19,17,43,47,59,35 > out/newrot.log 2>&1
