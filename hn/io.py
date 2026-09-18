"""Readers for the file formats used by Heule's CNP-SAT repository."""
from __future__ import annotations
import os
import re
from .field import K, Pt

_TOK = re.compile(r"(Sqrt\[)|(\d+)|([()+\-*/,\]])|(\s+)|(.)")


def _parse_expr(s):
    """Parse a Mathematica scalar such as  (1 + 3*Sqrt[33])/12  into a K.

    Strict: every character must be part of a token, and every Sqrt[...]
    argument -- an arbitrary sub-expression -- must have an exact square
    root in K.  The earlier version silently skipped anything it did not
    understand and mis-read nested radicals; now it raises.
    """
    toks, i = [], 0
    for m in _TOK.finditer(s):
        if m.group(1):
            toks.append(("sqrt", None))
        elif m.group(2):
            toks.append(("num", int(m.group(2))))
        elif m.group(3):
            toks.append(("op", m.group(3)))
        elif m.group(4):
            continue
        else:
            raise ValueError(f"unexpected character {m.group(5)!r} in {s!r}")

    def atom():
        nonlocal i
        kind, val = toks[i]
        if kind == "op" and val == "(":
            i += 1
            v = expr()
            assert toks[i] == ("op", ")"), s
            i += 1
            return v
        if kind == "op" and val == "-":
            i += 1
            return -atom()
        if kind == "sqrt":
            i += 1
            v = expr()
            assert toks[i] == ("op", "]"), s
            i += 1
            r = v.sqrt()
            if r is None:
                raise ValueError(f"radicand {v!r} has no square root in K: {s!r}")
            return r
        i += 1
        assert kind == "num", (kind, val, s)
        return K.rat(val)

    def term():
        nonlocal i
        v = atom()
        while i < len(toks) and toks[i][0] == "op" and toks[i][1] in "*/":
            op = toks[i][1]
            i += 1
            r = atom()
            v = v * r if op == "*" else v / r
        return v

    def expr():
        nonlocal i
        v = term()
        while i < len(toks) and toks[i][0] == "op" and toks[i][1] in "+-":
            op = toks[i][1]
            i += 1
            v = v + term() if op == "+" else v - term()
        return v

    v = expr()
    assert i == len(toks), f"trailing tokens in {s!r}"
    return v


def load_vtx(path):
    """Read a .vtx file: one '{x, y}' Mathematica pair per line."""
    pts = []
    for line in open(path):
        line = line.strip()
        if not line:
            continue
        assert line[0] == "{" and line[-1] == "}"
        inner, depth, cut = line[1:-1], 0, None
        for j, ch in enumerate(inner):
            if ch in "([":
                depth += 1
            elif ch in ")]":
                depth -= 1
            elif ch == "," and depth == 0:
                cut = j
                break
        pts.append(Pt(_parse_expr(inner[:cut]), _parse_expr(inner[cut + 1:])))
    return pts


def load_edges(path):
    """Read a DIMACS 'p edge' file; returns 0-indexed pairs."""
    out = []
    for line in open(path):
        if line.startswith("e"):
            _, a, b = line.split()
            out.append((int(a) - 1, int(b) - 1))
    return out


# ---- native exact format for pools built here -----------------------------
# The first line names the field.  A .pts read under the wrong triple gives
# too few unit edges and NO error -- a graph that is not 4-colourable comes
# back 4-colourable -- so the file carries its own field and the loader
# refuses to read it under another.

def _ensure_dir(path):
    """Create the parent directory.  Seven scripts write into out/, which a fresh
    extraction of the distributed archive does not have."""
    d = os.path.dirname(os.path.abspath(path))
    if d:
        os.makedirs(d, exist_ok=True)


def save_points(path, points, primes=None):
    """One point per line: 8 numerators and the denominator of x, then of y."""
    import hn.field as _f
    primes = tuple(primes) if primes is not None else _f.PRIMES
    _ensure_dir(path)
    with open(path, "w") as f:
        f.write("# primes " + " ".join(map(str, primes)) + "\n")
        for p in points:
            f.write(" ".join(map(str, p.x.n)) + f" {p.x.d} | "
                    + " ".join(map(str, p.y.n)) + f" {p.y.d}\n")


def points_field(path):
    """The triple a .pts was written under, or None for a headerless file."""
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                parts = line.split()
                if len(parts) == 5 and parts[1] == "primes":
                    return tuple(int(t) for t in parts[2:])
                continue
            return None
    return None


def load_points(path, check=True):
    """Read a .pts.  Raises if its header names a field other than the one set."""
    import hn.field as _f
    want = points_field(path)
    if check and want is not None and want != tuple(_f.PRIMES):
        raise ValueError(
            f"{path} was written over Q(sqrt{want[0]}, sqrt{want[1]}, "
            f"sqrt{want[2]}) but the current field is Q(sqrt{_f.PRIMES[0]}, "
            f"sqrt{_f.PRIMES[1]}, sqrt{_f.PRIMES[2]}).  Reading it anyway finds "
            f"too few unit edges and reports the graph 4-colourable.  Call "
            f"set_primes({want}) first.")
    pts = []
    for line in open(path):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        a, b = line.split("|")
        xa, ya = list(map(int, a.split())), list(map(int, b.split()))
        pts.append(Pt(K(xa[:8], xa[8]), K(ya[:8], ya[8])))
    return pts


def save_edges(path, n, edges):
    _ensure_dir(path)
    with open(path, "w") as f:
        f.write(f"p edge {n} {len(edges)}\n")
        for a, b in edges:
            f.write(f"e {a + 1} {b + 1}\n")
