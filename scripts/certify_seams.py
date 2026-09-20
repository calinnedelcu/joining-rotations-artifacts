#!/usr/bin/env python3
"""Certify the seam programme's UNSAT results, instead of re-running a solver.

results/SEAMS.md records twenty-one exact UNSAT results around the 509-vertex
record, reached by cutting a graph along a Galois seam: conjugating the
coordinate field preserves unit distance, because |p-q|^2 = 1 is rational and
Galois fixes the rationals, so a conjugation carries a 5-chromatic unit-distance
graph to another one.  Composed with the twelve isometries that gives 96 maps,
and the seam is the one under which a graph splits most unevenly -- the record
splits 494 fixed and 15 moved -- which turns "is there a smaller 5-chromatic
graph sharing this core" from a 509-choice search into a 14-choice one.

Those were solver verdicts.  This makes them proofs, the same upgrade the
constructions got: cadical writes a DRAT proof, drat-trim checks it, and the
compressed proof ships beside the instance.

Run: .venv/bin/python scripts/certify_seams.py [name ...]
"""
import glob, gzip, os, shutil, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
CADICAL = os.path.join(ROOT, "tools", "cadical-rel-2.1.3", "build", "cadical")
DRATTRIM = os.path.join(ROOT, "tools", "drat-trim")
OUT = os.path.join(ROOT, "proofs", "seams")
log = lambda s: print(s, flush=True)

names = sys.argv[1:]
cnfs = ([os.path.join(ROOT, "out", n + ".cnf") for n in names] if names
        else sorted(glob.glob(os.path.join(ROOT, "out", "*.cnf"))))
os.makedirs(OUT, exist_ok=True)

rows, bad = [], 0
for cnf in cnfs:
    name = os.path.basename(cnf)[:-4]
    if not os.path.exists(cnf):
        log(f"{name}: no such instance"); bad += 1; continue
    head = open(cnf).readline().split()
    nv, nc = head[2], head[3]
    drat = os.path.join(OUT, name + ".drat")

    t = time.time()
    r = subprocess.run([CADICAL, "--no-binary", cnf, drat], capture_output=True, text=True)
    solve = time.time() - t
    if r.returncode == 10:
        log(f"{name}: SATISFIABLE -- nothing to certify"); bad += 1; continue
    if r.returncode != 20:
        log(f"{name}: cadical exited {r.returncode}"); bad += 1; continue
    lines = sum(1 for _ in open(drat))

    t = time.time()
    v = subprocess.run([DRATTRIM, cnf, drat], capture_output=True, text=True)
    check = time.time() - t
    ok = any(l.strip() == "s VERIFIED" for l in v.stdout.replace("\r", "\n").splitlines())
    bad += not ok
    with open(os.path.join(OUT, name + ".drat-trim.log"), "w") as f:
        f.write("\n".join(l for l in v.stdout.replace("\r", "\n").splitlines() if l.strip()) + "\n")

    shutil.copyfile(cnf, os.path.join(OUT, name + ".cnf"))
    with open(drat, "rb") as fi, gzip.open(drat + ".gz", "wb") as fo:
        shutil.copyfileobj(fi, fo)
    os.remove(drat)
    mb = os.path.getsize(drat + ".gz") / 2**20
    rows.append((name, nv, nc, lines, solve, check, mb, ok))
    log(f"{name:<22} {nv:>6}v {nc:>7}c  UNSAT {solve:5.0f}s  "
        f"proof {lines:>9} lines  {'s VERIFIED' if ok else 'NOT VERIFIED'} {check:4.0f}s  "
        f"{mb:.0f} MB")

log(f"\n{len(rows)} certified, {bad} failed")
if rows:
    with open(os.path.join(OUT, "README.md"), "w") as f:
        f.write("# Seam certificates\n\n"
                "The UNSAT results of `results/SEAMS.md`, as DRAT proofs rather than\n"
                "solver verdicts. Each row's instance is beside its proof and its\n"
                "`drat-trim` log; `scripts/certify_seams.py` regenerates any of them.\n\n"
                "| instance | vars | clauses | proof lines | solve | `drat-trim` |\n"
                "|---|---:|---:|---:|---:|---|\n")
        for n, nv, nc, ln, s_, c_, mb, ok in rows:
            f.write(f"| `{n}` | {nv} | {nc} | {ln:,} | {s_:.0f} s | "
                    f"{'**`s VERIFIED`**' if ok else 'FAILED'}, {c_:.0f} s |\n")
        f.write("\nWhat each instance encodes is documented in the script that built it\n"
                "(`scripts/gal_core.py`, `scripts/part_seam.py`); a certificate settles\n"
                "the CNF, and the modelling is the script's.\n")
sys.exit(1 if bad else 0)
