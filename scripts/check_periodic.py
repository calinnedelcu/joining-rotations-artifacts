#!/usr/bin/env python3
"""Check the periodic kill witnesses in results/periodic/, from the files alone.

A witness names a rotation, a modulus m, two colourings of Lambda/m*Lambda indexed
by residue class, and every residue pair that occurs among cross pairs.  The kill
is valid when the two colourings disagree on every one of those pairs and agree at
the shared origin.  This script checks exactly that and nothing else: it reads the
JSON and never imports hn/, so a bug in the producer cannot excuse a bad witness.

What it does NOT check is that the listed pairs are all the pairs that occur --
that is the producer's enumeration, and re-deriving it needs the lattice.

Run: python3 scripts/check_periodic.py
"""
import glob, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "..", "results", "periodic")
bad, rows = [], []
for path in sorted(glob.glob(os.path.join(D, "*.json"))):
    d = json.load(open(path))
    L, S = d["colouring_L"], d["colouring_S"]
    pairs = [tuple(p) for p in d["occurring_pairs"]]
    n = d["residue_classes"]
    why = []
    if len(L) != n or len(S) != n:
        why.append(f"colourings have {len(L)}/{len(S)} entries, not {n}")
    if not all(0 <= c < 4 for c in L + S):
        why.append("a colour is outside 0..3")
    if not (L[0] == S[0]):
        why.append(f"shared origin: {L[0]} on one side, {S[0]} on the other")
    agree = [(i, j) for i, j in pairs if L[i] == S[j]]
    if agree:
        why.append(f"agrees on {len(agree)} occurring pairs, e.g. {agree[0]}")
    rows.append((d["rotation"], d["modulus"], n, len(pairs), "ok" if not why else "BAD"))
    if why:
        bad.append((os.path.basename(path), why))

print(f"{'rotation':<12} {'m':>2} {'classes':>8} {'pairs':>6}  verdict")
for r, m, n, p, v in rows:
    print(f"{r:<12} {m:>2} {n:>8} {p:>6}  {v}")
print(f"\n{len(rows)} witnesses, {len(bad)} bad")
for f, why in bad:
    print(f"  {f}: " + "; ".join(why))
sys.exit(1 if bad or not rows else 0)
