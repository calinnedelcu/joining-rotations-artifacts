#!/bin/sh
cd "$(dirname "$0")/.."
.venv/bin/python -u scripts/test_join.py 28 > out/join28.log 2>&1 &
wait
