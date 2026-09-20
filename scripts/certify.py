#!/usr/bin/env python3
"""Emit a DRAT proof that a graph is not 4-colourable, and check it.

The paper's constructions are established by running a solver again, which is
weaker than checking a proof, and a reviewer was right that the one certificate
this project had was for someone else's graph.  This produces ours.

    .venv/bin/python scripts/certify.py gadget367    # Lemma 18's premise
    .venv/bin/python scripts/certify.py theta16      # the minimised 2901
    .venv/bin/python scripts/certify.py alpha64_9    # the minimised 1408

Writes proofs/<name>.cnf, proofs/<name>.drat.gz and proofs/<name>.drat-trim.log.

Encoding: one variable per (vertex, colour); at-least-one and at-most-one per
vertex; for each edge and colour, the two ends may not share it.  For the gadget
the two terminals are additionally forced apart, which is exactly the
monochromatic-pair property Lemma 18 needs.

The solver is the CaDiCaL binary, not the python-sat binding: of the bindings
only lingeling emits a proof at all, and it is far slower here.  Emitting the CNF
first also means a failed or abandoned solve still leaves the instance behind for
someone else to attack.
"""
import gzip, os, shutil, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)
log = lambda s: print(s, flush=True)

CADICAL = os.path.join(ROOT, "tools", "cadical-rel-2.1.3", "build", "cadical")
DRATTRIM = os.path.join(ROOT, "tools", "drat-trim")

TARGETS = {
    "gadget367": dict(primes=(3, 11, 247), vtx="data/parts/v367e1822.vtx",
                      split=True,  what="Parts' 367-vertex gadget, terminals forced apart"),
    "theta16":   dict(primes=(3, 7, 11),   pts="results/theta16/t16_best.pts",
                      split=False, what="the minimised theta_16 graph"),
    "alpha64_9": dict(primes=(3, 11, 247), pts="results/alpha64_9/minimised.pts",
                      split=False, what="the minimised alpha_64/9 graph"),
    # The two largest, unminimised, attempted so the outcome can be reported
    # rather than guessed.  Give them a wall-clock cap: what a referee needs to
    # know is the instance size and whether it finishes, not a machine left on.
    "theta28":   dict(primes=(3, 11, 37),  pts="graphs/join28.pts",
                      split=False, cap=7200, what="the full-ball theta_28 union"),
    "theta36":   dict(primes=(3, 11, 13),  pts="graphs/join36.pts",
                      split=False, cap=7200, what="the full-ball theta_36 union"),
    "alpha64_3": dict(primes=(3, 11, 23),  pts="graphs/join64_3.pts",
                      split=False, cap=7200, what="the full-ball alpha_64/3 union"),
    "alpha256_9": dict(primes=(3, 11, 1015), pts="graphs/join256_9.pts",
                      split=False, cap=7200, what="the full-ball alpha_256/9 union"),
}

name = sys.argv[1] if len(sys.argv) > 1 else "gadget367"
cfg = TARGETS[name]
out = os.path.join(ROOT, "proofs")
os.makedirs(out, exist_ok=True)
cnf_path = os.path.join(out, f"{name}.cnf")
drat_path = os.path.join(out, f"{name}.drat")

from hn.field import set_primes, K, Pt
set_primes(cfg["primes"])
from hn import construct as C
C.refresh_field()
from hn.construct import edges_grid

t0 = time.time()
if "vtx" in cfg:
    from hn.io import load_vtx
    P = load_vtx(os.path.join(ROOT, cfg["vtx"]))
else:
    from hn.io import load_points
    P = load_points(os.path.join(ROOT, cfg["pts"]))
E = [tuple(sorted(e)) for e in edges_grid(P)]
log(f"{cfg['what']}: {len(P)} vertices, {len(E)} unit edges  ({time.time()-t0:.0f}s)")

extra = []
if cfg["split"]:
    key = lambda p: (str(p.x), str(p.y))
    idx = {key(p): i for i, p in enumerate(P)}
    i0 = idx[key(Pt(K.rat(-4, 3), K.rat(0)))]
    i1 = idx[key(Pt(K.rat(4, 3), K.rat(0)))]
    extra = [(i0, i1)]
    log(f"  terminals at indices {i0}, {i1} forced apart")

n, k = len(P), 4
var = lambda v, c: v * k + c + 1
cls = []
for v in range(n):
    cls.append([var(v, c) for c in range(k)])
    for c in range(k):
        for d in range(c + 1, k):
            cls.append([-var(v, c), -var(v, d)])
for a, b in E + extra:
    for c in range(k):
        cls.append([-var(a, c), -var(b, c)])

# Colour symmetry.  Any proper 4-colouring can be composed with a permutation of
# the four colours, so we may fix a triangle's three vertices to colours 0, 1, 2
# without changing satisfiability: given a proper colouring c, its values on a
# triangle are distinct, and the permutation carrying them to 0, 1, 2 turns c
# into a colouring satisfying the three unit clauses.  UNSAT for the augmented
# instance therefore means UNSAT for the plain one.  Unit-distance graphs in
# this lattice are full of triangles, and without this the proof runs to
# gigabytes; proofs/README.md states the reduction alongside the certificate.
adj = [set() for _ in range(n)]
for a, b in E:
    adj[a].add(b); adj[b].add(a)
banned = {i for pair in extra for i in pair}
tri = next((sorted((v, u, w))
            for v in range(n) if v not in banned
            for u in adj[v] if u > v and u not in banned
            for w in adj[v] & adj[u] if w > u and w not in banned), None)
if tri is None:
    log("  no triangle avoiding the terminals: no symmetry breaking applied")
else:
    for c, v in enumerate(tri):
        cls.append([var(v, c)])
    log(f"  colour symmetry broken on the triangle {tuple(tri)} -> colours 0,1,2")
body = f"p cnf {n*k} {len(cls)}\n" + "".join(
    " ".join(map(str, c)) + " 0\n" for c in cls)
# The full-ball instances run to 140-170 MB.  Ship those gzipped, as the proofs
# are: check_drat.sh unpacks either form, and an unverifiable certificate is no
# certificate -- leaving the CNF out entirely made four of the eight fail on a
# clean clone, which is how this was found.
with open(cnf_path, "w") as f:                 # plain for now: both tools need a path
    f.write(body)
big_cnf = len(body) > 8 << 20
log(f"CNF: {n*k} variables, {len(cls)} clauses -> proofs/{name}.cnf"
    + ("  (will be gzipped once checked)" if big_cnf else ""))

t = time.time()
cmd = [CADICAL, "--no-binary", cnf_path, drat_path]
if cfg.get("cap"):
    cmd += [f"-t", str(cfg["cap"])]
    log(f"  wall-clock cap {cfg['cap']}s")
r = subprocess.run(cmd, capture_output=True, text=True)
solve_s = time.time() - t
# CaDiCaL exits 20 for UNSAT, 10 for SAT, 0 when it gives up on a limit.
if r.returncode == 0:
    sz = os.path.getsize(drat_path) / 2**20 if os.path.exists(drat_path) else 0
    log(f"UNDECIDED after {solve_s:.0f}s -- cadical hit its limit; "
        f"partial proof {sz:.0f} MB, discarded")
    if os.path.exists(drat_path):
        os.remove(drat_path)
    raise SystemExit(4)
# CaDiCaL exits 20 for UNSAT, 10 for SAT.
if r.returncode == 10:
    log(f"SATISFIABLE after {solve_s:.0f}s -- there is nothing to certify")
    raise SystemExit(1)
if r.returncode != 20:
    log(f"cadical exited {r.returncode}\n{r.stdout[-2000:]}\n{r.stderr[-2000:]}")
    raise SystemExit(2)
lines = sum(1 for _ in open(drat_path))
log(f"UNSAT in {solve_s:.0f}s; proof {lines} lines, "
    f"{os.path.getsize(drat_path)/2**20:.0f} MB")

t = time.time()
v = subprocess.run([DRATTRIM, cnf_path, drat_path], capture_output=True, text=True)
verdict = v.stdout.replace("\r", "\n")
ok = any(l.strip() == "s VERIFIED" for l in verdict.splitlines())
log(f"drat-trim: {'s VERIFIED' if ok else 'NOT VERIFIED'}  ({time.time()-t:.0f}s)")
with open(os.path.join(out, f"{name}.drat-trim.log"), "w") as f:
    f.write("\n".join(l for l in verdict.splitlines() if l.strip()) + "\n")

with open(drat_path, "rb") as fi, gzip.open(drat_path + ".gz", "wb") as fo:
    shutil.copyfileobj(fi, fo)
os.remove(drat_path)
# The full-ball instances run to 140-170 MB.  Ship those gzipped, as the proofs
# are; check_drat.sh unpacks either form.  Leaving the CNF out of the repository
# entirely made four of the eight certificates fail on a clean clone, and an
# unverifiable certificate is not a certificate.
if big_cnf:
    with open(cnf_path, "rb") as fi, gzip.open(cnf_path + ".gz", "wb") as fo:
        shutil.copyfileobj(fi, fo)
    os.remove(cnf_path)
    log(f"gzipped the CNF to proofs/{name}.cnf.gz "
        f"({os.path.getsize(cnf_path + '.gz')/2**20:.0f} MB)")
log(f"wrote proofs/{name}.drat.gz "
    f"({os.path.getsize(drat_path + '.gz')/2**20:.0f} MB)   total {time.time()-t0:.0f}s")
raise SystemExit(0 if ok else 3)
