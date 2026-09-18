#!/bin/sh
cd "$(dirname "$0")/.."
for spec in "2 2.0" "3 1.6" "3 2.0" "3 2.4" "4 2.0"; do
  set -- $spec
  .venv/bin/python -u scripts/hept_t2_build.py "$1" "$2" 2>&1
  echo "---"
done
