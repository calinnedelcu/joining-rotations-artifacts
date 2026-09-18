#!/usr/bin/env python3
"""Verify every published record graph: exact geometry, then chromatic number."""
import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hn import load_vtx, load_edges, is_unit, verify, find_triangle

D = os.path.join(os.path.dirname(__file__), "..", "data")
for g in ["510", "517", "529", "553", "610", "633", "803", "826", "874"]:
    P = load_vtx(f"{D}/vtx/{g}.vtx")
    E = load_edges(f"{D}/edge/{g}.edge")
    bad = sum(1 for i, j in E if not is_unit(P[i], P[j]))
    tri = find_triangle(len(P), E)
    t = time.time()
    five = verify(P, E, triangle=tri)
    print(f"{g:>4}: {len(P):4d} vertices, {len(E):5d} edges, "
          f"non-unit edges {bad}, chi>=5 {five}  ({time.time()-t:.1f}s)")
