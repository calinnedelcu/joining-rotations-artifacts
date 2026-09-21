#!/usr/bin/env python3
"""Run the paper's claims about its own tooling, instead of believing them.

Four rounds of review have now found the same species of defect: a sentence in
the manuscript or the notes says what a script does or what the archive holds,
the script or the archive later changes, and nothing compares the two.  It has
cost a checker that could not test what it advertised, a "nothing needs pysat"
that stopped being true the day a script that needs pysat joined the checking
path, an audit described as deriving everything while one block reads a stored
file, "the entry added since" that was eleven, and counts that drifted.  None of
it was a mathematical error, and all of it was visible from inside the
repository.

`check_paper.sh` tests the rendered PDF.  `check_notes.py` tests numbered
cross-references and commit hashes.  Neither can see "this script verifies
properness" or "eight certificates".  This does: where a claim states a number,
the number is read OUT of the document and compared with the filesystem, so
editing the prose without changing the fact fails; where a claim states a
behaviour, the behaviour is executed.

    python3 scripts/check_claims.py            # the fast checks
    python3 scripts/check_claims.py --slow     # and the binding rebuild

It needs no third-party package, by design: several of the claims it checks are
claims about running without one.
"""
import glob, gzip, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
TEX = os.path.join(ROOT, "paper", "joining-rotations.tex")
BARE = "/usr/bin/python3" if os.path.exists("/usr/bin/python3") else sys.executable

WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
         "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11,
         "twelve": 12, "twenty": 20, "thirty": 30}

results = []


def record(name, ok, detail):
    results.append((name, ok, detail))


def skip(name, why):
    results.append((name, None, why))


def tex():
    try:
        return open(TEX, encoding="utf-8").read()
    except OSError:
        return None


def claimed(pattern, text):
    """The number a sentence claims, read out of the document itself."""
    m = re.search(pattern, text)
    if not m:
        return None
    w = m.group(1)
    return WORDS.get(w.lower(), int(w) if w.isdigit() else None)


def run(cmd, timeout=900):
    try:
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True,
                           timeout=timeout)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except subprocess.TimeoutExpired:
        return 124, "timed out"
    except OSError as e:
        return 127, str(e)


# --- claims that state a number --------------------------------------------

def certificates_counted():
    t = tex()
    if t is None:
        return skip("eight certificates", "no manuscript source here")
    n = claimed(r"verifies the\s+(\w+)\s+DRAT certificates", t)
    if n is None:
        return skip("DRAT certificate count", "the sentence is not in the paper")
    have = len(glob.glob(os.path.join(ROOT, "proofs", "*.drat.gz")))
    record(f"the paper says {n} DRAT certificates", n == have,
           f"proofs/ holds {have}")


def witnesses_counted():
    t = tex()
    if t is None:
        return skip("twenty witnesses", "no manuscript source here")
    n = claimed(r"check the\s+(\w+)\s*\n?\s*witnesses against their JSON", t)
    if n is None:
        n = claimed(r"the\s+(\w+)\s+witnesses", t)
    if n is None:
        return skip("witness count", "the sentence is not in the paper")
    have = (len(glob.glob(os.path.join(ROOT, "results", "periodic", "*.json"))) +
            len(glob.glob(os.path.join(ROOT, "results", "emptyshell", "*.json"))))
    record(f"the paper says {n} witnesses", n == have,
           f"results/ holds {have}")


def parts_files_counted():
    t, prov = tex(), os.path.join(ROOT, "PROVENANCE.md")
    if t is None or not os.path.exists(prov):
        return skip("files from Parts", "manuscript or PROVENANCE.md not here")
    n = claimed(r"names\s*\n?\s*the\s+(\w+)\s+files taken from", t)
    if n is None:
        return skip("files from Parts", "the sentence is not in the paper")
    body = open(prov, encoding="utf-8").read()
    have = len(set(re.findall(r"`(data/[^`]+)`", body)))
    record(f"the paper says {n} files from Parts", n == have,
           f"PROVENANCE.md names {have}")


def suite_entries_counted():
    readme = os.path.join(ROOT, "README.md")
    sh = os.path.join(ROOT, "scripts", "verify_all.sh")
    if not (os.path.exists(readme) and os.path.exists(sh)):
        return skip("suite entry count", "README.md or verify_all.sh not here")
    m = re.search(r"#\s*all\s+(\d+)\s+entries", open(readme, encoding="utf-8").read())
    if not m:
        return skip("suite entry count", "README does not state a count")
    n = int(m.group(1))
    have = sum(1 for line in open(sh, encoding="utf-8")
               if re.match(r"\s*(run|sh_run)\s", line) and "()" not in line)
    record(f"README says {n} suite entries", n == have,
           f"verify_all.sh registers {have}")


# --- claims that state a behaviour -----------------------------------------

def periodic_checker_rejects_a_bad_witness():
    """'re-checked to be proper' -- so a witness that is not must be refused."""
    code, out = run([BARE, "scripts/check_periodic.py", "--selftest"], timeout=600)
    ok = code == 0 and "PASS" in out
    line = next((l.strip() for l in out.splitlines() if "PASS" in l or "FAIL" in l),
                out.strip().splitlines()[-1] if out.strip() else "no output")
    record("check_periodic refuses an improper witness", ok, line)


def checking_path_runs_bare():
    """'Nothing in the checking path needs a SAT solver, pysat, or a virtualenv.'"""
    for s in ("check_periodic.py", "check_emptyshell.py", "check_notes.py",
              "check_claims.py"):
        p = os.path.join(ROOT, "scripts", s)
        if not os.path.exists(p):
            skip(f"{s} on a bare interpreter", "not here")
            continue
        if s == "check_claims.py":                 # do not recurse
            code, out = run([BARE, "-c",
                             "import ast,sys;ast.parse(open('scripts/check_claims.py').read())"])
        else:
            code, out = run([BARE, os.path.join("scripts", s)], timeout=900)
        bad = "ModuleNotFoundError" in out
        record(f"{s} runs without pysat", code == 0 and not bad,
               "ModuleNotFoundError" if bad else f"exit {code}")


def binding_runs_bare(slow):
    """The binding check is in the checking path, so it must run bare too."""
    p = os.path.join(ROOT, "scripts", "check_binding.py")
    if not os.path.exists(p):
        return skip("check_binding on a bare interpreter", "not here")
    targets = ["gadget367", "theta16", "alpha64_9"] if not slow else []
    code, out = run([BARE, "scripts/check_binding.py"] + targets, timeout=3600)
    bad = "ModuleNotFoundError" in out
    n_bound = out.count("BOUND")
    record("check_binding runs without pysat", code == 0 and not bad,
           "ModuleNotFoundError" if bad else f"exit {code}, {n_bound} bound")


def audit_is_independent():
    """'sharing no code with the rest' -- so it must not import the project."""
    p = os.path.join(ROOT, "scripts", "audit_numbers.py")
    if not os.path.exists(p):
        return skip("audit_numbers independence", "not here")
    body = open(p, encoding="utf-8").read()
    imports = re.findall(r"^\s*(?:from|import)\s+(hn[\w.]*)", body, re.M)
    reads = re.findall(r"results/[\w./-]+\.json", body)
    record("audit_numbers imports nothing from hn", not imports,
           ", ".join(imports) if imports else "no hn import")
    # it reads one stored file and says so in its own output; the paper must too
    t = tex()
    if t is None:
        return skip("the audit's stored-file exception", "no manuscript source")
    disclosed = "empty\\_shell\\_status" in t or "empty_shell_status" in t
    record("the paper discloses the audit's one stored read",
           (not reads) or disclosed,
           f"reads {reads[0]}" if reads and not disclosed else
           ("no stored read" if not reads else "disclosed"))


def certificates_are_verified():
    """'all reporting s VERIFIED' -- the logs must say so, for every proof."""
    logs = sorted(glob.glob(os.path.join(ROOT, "proofs", "*.drat-trim.log")))
    if not logs:
        return skip("s VERIFIED on every certificate", "no drat-trim logs here")
    bad = [os.path.basename(l) for l in logs
           if "s VERIFIED" not in open(l, encoding="utf-8", errors="replace").read()]
    record(f"all {len(logs)} drat-trim logs say s VERIFIED", not bad,
           ", ".join(bad) if bad else "every one")


def witnesses_are_checkable():
    """A periodic witness without its unit steps cannot be checked for properness."""
    files = sorted(glob.glob(os.path.join(ROOT, "results", "periodic", "*.json")))
    if not files:
        return skip("witnesses carry their unit steps", "no witnesses here")
    missing = [os.path.basename(f) for f in files
               if "unit_steps" not in json.load(open(f))]
    record(f"all {len(files)} periodic witnesses carry unit_steps", not missing,
           ", ".join(missing[:3]) if missing else "every one")


def main():
    slow = "--slow" in sys.argv
    certificates_counted()
    witnesses_counted()
    parts_files_counted()
    suite_entries_counted()
    certificates_are_verified()
    witnesses_are_checkable()
    audit_is_independent()
    periodic_checker_rejects_a_bad_witness()
    checking_path_runs_bare()
    binding_runs_bare(slow)

    width = max(len(n) for n, _, _ in results)
    bad = 0
    for name, ok, detail in results:
        verdict = "SKIP" if ok is None else ("ok" if ok else "FAIL")
        print(f"{name:<{width}}  {verdict:<4}  {detail}")
        if ok is False:
            bad += 1
    n_skip = sum(1 for _, ok, _ in results if ok is None)
    print(f"\n{len(results) - n_skip - bad} of {len(results) - n_skip} claims hold"
          + (f", {n_skip} skipped" if n_skip else ""))
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
