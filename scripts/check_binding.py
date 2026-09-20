#!/usr/bin/env python3
"""Bind each shipped certificate to the graph it is supposed to be about.

`check_drat.sh` checks a stored CNF against a stored proof.  That establishes
that the CNF is unsatisfiable; it says nothing about whether the CNF encodes the
graph the paper's table names.  The two are separate obligations, and this
project has already shipped one certificate for someone else's graph, so the gap
is not theoretical.  A referee made the point three ways in one report.

This closes it without a solver.  The CNF is a deterministic function of the
coordinate file and the field: read the points, take every pair at distance
exactly 1 in exact arithmetic, encode one variable per (vertex, colour), break
the colour symmetry on the first triangle found.  Rebuilding it from the shipped
coordinates and comparing bytes decides the question.  The rebuild is done by
`certify.py --emit-only`, the same code path that produced the certificate, so
the two cannot drift apart.

    .venv/bin/python scripts/check_binding.py            # all seven
    .venv/bin/python scripts/check_binding.py theta16    # one of them

The record's certificate, `proofs/509_not4col.*`, is NOT covered: its CNF was
not produced by `certify.py` and has no target here.  Seven of the eight, and
the eighth is said so rather than implied.

The four full-ball instances rebuild to 140-170 MB and take minutes each; the
three small ones take seconds.  Nothing is written outside a temporary
directory.
"""
import gzip, hashlib, os, shutil, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
PROOFS = os.path.join(ROOT, "proofs")
PY = sys.executable

# Every target certify.py knows, in increasing cost.
NAMES = ["gadget367", "theta16", "alpha64_9",
         "theta28", "theta36", "alpha64_3", "alpha256_9"]


def digest(path):
    """sha256 of a CNF, whether it ships plain or gzipped."""
    op = gzip.open if path.endswith(".gz") else open
    h = hashlib.sha256()
    with op(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def shipped(name):
    for suffix in (".cnf", ".cnf.gz"):
        p = os.path.join(PROOFS, name + suffix)
        if os.path.exists(p):
            return p
    return None


def check(name, tmp):
    ship = shipped(name)
    if ship is None:
        return name, "MISSING", 0, "no CNF in proofs/"
    t = time.time()
    r = subprocess.run([PY, "-u", os.path.join(HERE, "certify.py"),
                        "--emit-only", "--out", tmp, name],
                       capture_output=True, text=True)
    secs = time.time() - t
    if r.returncode != 0:
        tail = (r.stdout + r.stderr).strip().splitlines()[-1:] or [""]
        return name, "ERROR", secs, f"certify.py exited {r.returncode}: {tail[0][:80]}"
    built = os.path.join(tmp, name + ".cnf")
    if not os.path.exists(built):
        return name, "ERROR", secs, "certify.py wrote no CNF"
    a, b = digest(built), digest(ship)
    os.remove(built)
    if a != b:
        return name, "MISMATCH", secs, f"rebuilt {a[:16]} vs shipped {b[:16]}"
    return name, "BOUND", secs, f"{a[:16]}  {os.path.basename(ship)}"


def main():
    names = sys.argv[1:] or NAMES
    unknown = [n for n in names if n not in NAMES]
    if unknown:
        sys.exit(f"not a target: {', '.join(unknown)}\nknown: {', '.join(NAMES)}")
    bad = 0
    with tempfile.TemporaryDirectory() as tmp:
        for n in names:
            name, verdict, secs, why = check(n, tmp)
            print(f"{name:12s} {verdict:9s} {secs:6.0f}s  {why}", flush=True)
            if verdict != "BOUND":
                bad += 1
    print(f"\n{len(names) - bad} of {len(names)} certificates bound to their graphs")
    print("proofs/509_not4col.* is out of scope: its CNF is not certify.py's")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
