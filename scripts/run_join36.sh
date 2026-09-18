#!/bin/sh
cd "$(dirname "$0")/.."
.venv/bin/python -u scripts/test_join.py 36 > out/join36.log 2>&1
