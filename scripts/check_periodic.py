#!/usr/bin/env python3
"""Check the periodic kill witnesses in results/periodic/, from the files alone.

A witness names a rotation, a modulus m, the rank r, the residue classes of the
lattice's unit vectors, two colourings of Lambda/m*Lambda indexed by residue
class, and every residue pair that occurs among cross pairs.  The kill is valid
when each colouring is PROPER -- no two residues a unit step apart share a
colour -- when the two agree at the shared origin, and when they disagree on
every occurring pair.  This checks all three and nothing else: it reads the JSON
and never imports hn/, so a bug in the producer cannot excuse a bad witness.

Earlier this script checked only the last two.  A referee copied a witness,
forced a monochromatic unit edge into one half, and it still printed "ok" --
because properness is a statement about unit edges, and the unit edges were not
in the file.  The producer now writes them and this checks against them.  Run
with --selftest to see a deliberately corrupted witness rejected; a checker
nobody has watched fail is not a checker.

What it still does NOT check is that the listed pairs are all the pairs that
occur -- re-deriving that needs the lattice, so it is the producer's
enumeration, and `scripts/join_filter_residues.py` does it exactly, with no ball
and no radius, from the joint lattice's unit vectors.  `verify_all.sh` runs that
producer for all eleven.

Run: python3 scripts/check_periodic.py [--selftest]
"""
import copy, glob, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "..", "results", "periodic")


def faults(d):
    """Everything wrong with one witness, as a list of sentences."""
    why = []
    n, m = d["residue_classes"], d["modulus"]
    L, S = d["colouring_L"], d["colouring_S"]
    pairs = [tuple(p) for p in d["occurring_pairs"]]

    if len(L) != n or len(S) != n:
        why.append(f"colourings have {len(L)}/{len(S)} entries, not {n}")
        return why                       # nothing else can be read safely
    if not all(0 <= c < 4 for c in L + S):
        why.append("a colour is outside 0..3")
    if L[0] != S[0]:
        why.append(f"shared origin: {L[0]} on one side, {S[0]} on the other")

    # properness, the check that used to be missing
    steps = d.get("unit_steps")
    if steps is None:
        why.append("no unit_steps in the file, so properness cannot be checked")
    else:
        r = d.get("rank")
        if r is None or m ** r != n:
            why.append(f"rank {r} and modulus {m} do not give {n} classes")
        else:
            dec = lambda i: [(i // m ** k) % m for k in range(r)]
            enc = lambda v: sum((c % m) * m ** k for k, c in enumerate(v))
            for side, tab in (("L", L), ("S", S)):
                for v in range(n):
                    dv = dec(v)
                    for st in steps:
                        w = enc([a + b for a, b in zip(dv, dec(st))])
                        if tab[v] == tab[w]:
                            why.append(f"colouring_{side} is not proper: "
                                       f"residues {v} and {w} are a unit step "
                                       f"apart and share colour {tab[v]}")
                            break
                    else:
                        continue
                    break

    agree = [(i, j) for i, j in pairs if L[i] == S[j]]
    if agree:
        why.append(f"agrees on {len(agree)} occurring pairs, e.g. {agree[0]}")
    return why


def selftest(paths):
    """Corrupt a copy into a monochromatic unit edge; the checker must reject it."""
    if not paths:
        print("selftest: no witness to corrupt"); return 1
    d = json.load(open(paths[0]))
    steps = d.get("unit_steps")
    if not steps:
        print(f"selftest: {os.path.basename(paths[0])} has no unit_steps"); return 1
    n, m, r = d["residue_classes"], d["modulus"], d["rank"]
    dec = lambda i: [(i // m ** k) % m for k in range(r)]
    enc = lambda v: sum((c % m) * m ** k for k, c in enumerate(v))
    w = enc([a + b for a, b in zip(dec(1), dec(steps[0]))])
    bad = copy.deepcopy(d)
    bad["colouring_L"][w] = bad["colouring_L"][1]          # one monochromatic unit edge
    got = faults(bad)
    ok = any("not proper" in s for s in got)
    print(f"selftest: forced residues 1 and {w} to share a colour in "
          f"{os.path.basename(paths[0])}")
    print(f"  checker says: {got[0] if got else 'ok -- NOT REJECTED'}")
    print(f"  {'PASS -- the corruption is caught' if ok else 'FAIL -- it slipped through'}")
    return 0 if ok else 1


def main():
    paths = sorted(glob.glob(os.path.join(D, "*.json")))
    if "--selftest" in sys.argv:
        return selftest(paths)
    bad, rows = [], []
    for path in paths:
        d = json.load(open(path))
        why = faults(d)
        rows.append((d["rotation"], d["modulus"], d["residue_classes"],
                     len(d["occurring_pairs"]), "ok" if not why else "BAD"))
        if why:
            bad.append((os.path.basename(path), why))
    print(f"{'rotation':<12} {'m':>2} {'classes':>8} {'pairs':>6}  verdict")
    for r, m, n, p, v in rows:
        print(f"{r:<12} {m:>2} {n:>8} {p:>6}  {v}")
    print(f"\n{len(rows)} witnesses, {len(bad)} bad")
    for f, why in bad:
        print(f"  {f}: " + "; ".join(why))
    return 1 if bad or not rows else 0


if __name__ == "__main__":
    raise SystemExit(main())
