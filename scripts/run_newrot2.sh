#!/bin/sh
cd "$(dirname "$0")/.."
.venv/bin/python -u scripts/new_rotations.py --depth 5 --radius 5.05 --fields 79,83,91 \
  > out/newrot2.log 2>&1
