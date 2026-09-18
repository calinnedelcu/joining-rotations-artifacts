#!/bin/sh
cd "$(dirname "$0")/.."
P=.venv/bin/python
$P -u scripts/newfield_sweep.py --primes 2,3,5 --dirs 15 --depth 4 --radius 2.2 > out/nf15_d4.log 2>&1
$P -u scripts/newfield_sweep.py --primes 2,3,5 --dirs 15 --depth 5 --radius 1.8 > out/nf15_d5.log 2>&1
$P -u scripts/newfield_sweep.py --primes 3,5,11 --dirs 15 --depth 4 --radius 2.2 > out/nf15cl_d4.log 2>&1
