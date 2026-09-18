#!/usr/bin/env python3
"""Shrink a graph and report the result.  Usage: shrink.py 874 [seed]"""
import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn import load_vtx, load_edges, shrink, verify
from hn.sat import find_triangle
from hn.graph import induced

D = os.path.join(os.path.dirname(__file__), "..", "data")
name = sys.argv[1] if len(sys.argv) > 1 else "874"
seed = int(sys.argv[2]) if len(sys.argv) > 2 else 0
P = load_vtx(f"{D}/vtx/{name}.vtx")
E = load_edges(f"{D}/edge/{name}.edge")
print(f"start: {len(P)} vertices")
t = time.time()
keep = shrink(P, E, seed=seed)
P2, E2 = induced(P, E, keep)
print(f"result: {len(P2)} vertices, {len(E2)} edges  ({time.time()-t:.0f}s)")
print("final independent check (no symmetry breaking):",
      verify(P2, E2, triangle=None))
print("record to beat: 509 vertices / 2442 edges (Parts, 2020)")
