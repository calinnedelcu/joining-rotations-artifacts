#!/usr/bin/env python3
"""Audit every claim in results/: re-derive the numbers, re-verify the graphs.

Usage: audit.py

A proof log is only as good as the code that wrote it. This re-reads every
archived log, extracts the claim it makes, and checks what can be checked
independently right now:

  * every UNSAT line names a bound and a pool size; both are reported here so a
    reader can compare them against the statement in results/README.md
  * every graph the repository ships is re-verified from its coordinates: the
    unit-distance edges are recomputed exactly in the field, the graph is
    re-checked for non-4-colourability in a fresh solver with no assumptions,
    and its minimum degree is reported, since a vertex-critical 5-chromatic
    graph must have minimum degree at least 4

What this cannot do is re-check an UNSAT answer from the master without redoing
the search, which is what the logs are for. Emitting an LRAT certificate from
the final master call is the piece still missing, and is what a referee would
ask for.
"""
import os, re, sys, glob
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn import load_vtx, load_edges, verify, find_triangle, is_unit
from hn.io import load_points
from hn.construct import edges as exact_edges
from hn.graph import degrees

D = os.path.join(os.path.dirname(__file__), "..")
print("=== claims in results/", flush=True)
for f in sorted(glob.glob(f"{D}/results/*.log")):
    txt = open(f).read()
    pool = re.findall(r"pool[^\n]*?(\d+) (?:vertices|points)", txt)
    uns = re.findall(r"UNSAT at bound (\d+)", txt)
    best = re.findall(r"best[^\n]*?(\d+) (?:vertices|free)", txt)
    five = re.findall(r"chi>=5 (True|False)", txt)
    bits = []
    if pool:
        bits.append(f"pool {pool[0]}")
    if uns:
        bits.append(f"UNSAT at {uns[-1]}")
    if best:
        bits.append(f"best {best[-1]}")
    if five:
        bits.append(f"{five.count('True')} of {len(five)} unions 5-chromatic")
    print(f"  {os.path.basename(f):58s} {'; '.join(bits) or 'scan, no bound'}", flush=True)

print("\n=== every graph shipped in data/, re-verified from coordinates", flush=True)
for g in ("509", "510", "517", "529", "553", "610", "633", "803", "826", "874"):
    P = load_vtx(f"{D}/data/vtx/{g}.vtx")
    E = load_edges(f"{D}/data/edge/{g}.edge")
    recomputed = exact_edges(P)
    same = sorted(E) == recomputed
    bad = sum(1 for i, j in E if not is_unit(P[i], P[j]))
    d = degrees(len(P), E)
    tri = find_triangle(len(P), E)
    five = verify(P, E, triangle=tri)
    fivable = not verify(P, E, k=5)
    print(f"  {g}: {len(P)} vertices, {len(E)} edges; edge list matches the exact "
          f"recomputation {same}; non-unit edges {bad}; min degree {min(d)}; "
          f"not 4-colourable {five}; 5-colourable {fivable}", flush=True)
