#!/bin/sh
cd "$(dirname "$0")/.."
for spec in "2 1.2" "2 1.35" "2 1.45"; do
  set -- $spec
  timeout 900 .venv/bin/python -u scripts/hept_t2_build.py "$1" "$2" 2 2>&1
  echo "---"
done
