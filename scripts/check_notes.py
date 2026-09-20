#!/usr/bin/env python3
"""Check that every cross-reference in the companion notes resolves in the paper.

Three rounds running, a referee found stale references in the notes that ship
with the manuscript: a release that did not exist, then a tag pointing at the
wrong commit, then six "Theorem N"/"Lemma N"/"Section N" left over from before a
renumbering.  Each time the paper was fixed and the notes were not re-checked
against it.  `check_paper.sh` tests the rendered PDF; nothing tested the notes.

This does.  It reads the paper's own .aux for label -> number and the .tex for
label -> kind, then scans the Markdown notes for "Theorem 18", "Lemma 20",
"Section 6" and the like, and fails if the paper has no result of that kind with
that number.  A reference that resolves to the WRONG object -- "Theorem 17" when
17 is a Remark -- is exactly the case it is built to catch.

It also checks the commit hashes.  The notes tell a referee which snapshot of
the archive to check out, and after the paper's pin was moved off a commit whose
certificate script named files that are not shipped, three of them still sent
the referee back to it.  Numbered cross-references were all this checked at the
time, so the run that should have caught it passed: the check's domain excluded
the thing it was meant to find.  Any `<hex>` in a note that is not a prefix of a
hash the paper names is now a failure.

Run after every recompile:  .venv/bin/python scripts/check_notes.py [notes...]
"""
import glob, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
AUX = os.path.join(ROOT, "paper", "joining-rotations.aux")
TEX = os.path.join(ROOT, "paper", "joining-rotations.tex")
KINDS = ("Theorem", "Lemma", "Proposition", "Corollary", "Remark")

if not os.path.exists(AUX):
    sys.exit("no .aux -- compile with --keep-intermediates first")

aux = open(AUX, encoding="utf-8").read()
tex = open(TEX, encoding="utf-8").read()
num = {m.group(1): m.group(2)
       for m in re.finditer(r"\\newlabel\{([^}]*)\}\{\{(\d+)\}", aux)}
kind = {m.group(2): m.group(1).capitalize()
        for m in re.finditer(
            r"\\begin\{(theorem|lemma|proposition|corollary|remark)\}[^\n]*?\\label\{([^}]*)\}", tex)}
# what exists: the set of (kind, number) the paper actually defines
exists = {(kind[l], num[l]) for l in kind if l in num}
# every commit hash the paper itself names, so a note cannot point somewhere else
pinned = set(re.findall(r"\\texttt\{([0-9a-f]{40})\}", tex))
hashpat = re.compile(r"`([0-9a-f]{7,40})`")
by_number = {}
for k, n in exists:
    by_number.setdefault(n, set()).add(k)
nsec = len(re.findall(r"\\section\{", tex))

notes = sys.argv[1:] or sorted(glob.glob(os.path.join(ROOT, "*.md")))
pat = re.compile(r"\b(" + "|".join(KINDS) + r"|Section)\s+(\d+)\b")

bad = 0
for path in notes:
    text = open(path, encoding="utf-8").read()
    hits = []
    for m in pat.finditer(text):
        k, n = m.group(1), m.group(2)
        line = text[:m.start()].count("\n") + 1
        if k == "Section":
            if not (1 <= int(n) <= nsec):
                hits.append((line, m.group(0), f"the paper has sections 1-{nsec}"))
        elif (k, n) not in exists:
            other = by_number.get(n)
            why = (f"{n} is {'/'.join(sorted(other))} {n}" if other
                   else f"nothing is numbered {n}")
            hits.append((line, m.group(0), why))
    for m in hashpat.finditer(text):
        h = m.group(1)
        if not any(p.startswith(h) for p in pinned):
            line = text[:m.start()].count("\n") + 1
            named = ", ".join(sorted(p[:12] for p in pinned)) or "no commit at all"
            hits.append((line, h, f"the paper names {named}"))
    hits.sort()
    name = os.path.relpath(path, ROOT)
    if hits:
        bad += len(hits)
        print(f"{name}: {len(hits)} stale")
        for line, ref, why in hits:
            print(f"    line {line}: '{ref}' -- {why}")
    else:
        print(f"{name}: ok")

print(f"\n{bad} stale cross-reference(s)")
sys.exit(1 if bad else 0)
