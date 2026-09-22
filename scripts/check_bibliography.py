#!/usr/bin/env python3
"""Check every bibliography entry against the source it names.

Three rounds of referees read this paper and none of them opened an arXiv
identifier.  Nothing here did either: `check_claims.py` compares the numbers in
the manuscript with the filesystem, `check_notes.py` resolves cross-references
and commit hashes, `check_drat.sh` and `check_binding.py` bind certificates to
graphs.  Forty-seven checks, and the bibliography was in none of their domains.

So two entries sat wrong for two days.  One named `M. Krebs` as an author of
arXiv:2406.15317, whose five authors are Engel, Hammond-Lee, Su, Varga and
Zsamboki and whose full text contains the string "krebs" zero times.  The other
gave arXiv:2410.16172 the title of a different paper.  Both identifiers were
right, and both had genuinely been fetched and read -- the commit that added
them reports full-text counts that reproduce exactly today.  What went wrong was
the part a human types next to an identifier they have already checked.

This asks arXiv.  For each \\bibitem carrying an arXiv id it compares the title
and every surname against that id's metadata, and fails on a mismatch.  It does
not judge entries without an identifier -- blog comments, wiki pages, a
ResearchGate deposit -- because there is no machine-readable source to compare
them with; it counts them and says so, rather than passing silently and letting
you believe they were checked.

    .venv/bin/python scripts/check_bibliography.py
    .venv/bin/python scripts/check_bibliography.py --selftest

The self-test corrupts a copy of a real entry the way the real defect looked --
a stranger's surname, then a transplanted title -- and shows both rejected.  A
checker nobody has watched fail is not a checker.

Needs the network.  With none, it says so and exits 0: a check that cannot run
is not a check that passed, but it must not turn an offline machine red either.
"""
import html
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
TEX = os.path.join(HERE, "..", "paper", "joining-rotations.tex")
API = "https://export.arxiv.org/api/query?id_list={}&max_results=1"
PAUSE = 3.0                      # arXiv asks for one request every three seconds


def fold(s):
    """Compare names and titles without accents, case or punctuation noise."""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]+", " ", s.lower()).strip()


def words(s):
    return [w for w in fold(s).split() if len(w) > 2]


def entries(tex):
    """Every \\bibitem as (key, body), split on the next \\bibitem or the end."""
    body = re.search(r"\\begin\{thebibliography\}(.*?)\\end\{thebibliography\}",
                     tex, re.S)
    if not body:
        return []
    chunks = re.split(r"\\bibitem\{([^}]+)\}", body.group(1))[1:]
    return list(zip(chunks[0::2], chunks[1::2]))


def cited_title(entry):
    m = re.search(r"\\emph\{(.*?)\}", entry, re.S)
    return " ".join(m.group(1).split()) if m else None


def cited_names(entry):
    """Surnames as the entry gives them, before the first \\emph."""
    head = entry.split("\\emph")[0]
    head = re.sub(r"\\['`\"^~=.]?\{?([A-Za-z])\}?", r"\1", head)   # \'a -> a
    head = head.replace("~", " ").replace("\\", "")
    out = []
    for part in re.split(r",| and ", head):
        part = part.strip(" .{}")
        if not part or "et al" in part.lower():
            continue
        toks = [t for t in part.split() if t]
        if toks:
            last = toks[-1].strip(".")
            if len(last) > 2:                      # an initial is not a surname
                out.append(last)
    return out


def fetch(arxiv_id):
    with urllib.request.urlopen(API.format(arxiv_id), timeout=40) as r:
        x = r.read().decode("utf-8", "replace")
    if "<entry>" not in x:
        return None
    t = re.search(r"<entry>.*?<title>(.*?)</title>", x, re.S)
    return {
        "title": " ".join(html.unescape(t.group(1)).split()) if t else "",
        "authors": [html.unescape(a) for a in re.findall(r"<name>(.*?)</name>", x)],
    }


def compare(key, entry, meta):
    """Everything wrong with one entry, as sentences."""
    why = []
    want = cited_title(entry)
    if want and meta["title"]:
        if fold(want) != fold(meta["title"]):
            shared = set(words(want)) & set(words(meta["title"]))
            if len(shared) < 0.6 * max(1, len(set(words(want)))):
                why.append(f'titled "{want}" but arXiv says "{meta["title"]}"')
    have = fold(" ".join(meta["authors"]))
    for name in cited_names(entry):
        if fold(name) not in have:
            why.append(f"names {name}, who is not an author "
                       f"({', '.join(meta['authors'])})")
    return why


def selftest(tex):
    """Corrupt a good entry the two ways the real defect looked."""
    rows = [(k, e) for k, e in entries(tex) if re.search(r"arXiv:(\d{4}\.\d{4,5})", e)]
    if not rows:
        print("selftest: no entry carries an arXiv id")
        return 1
    key, good = rows[0]
    arxiv_id = re.search(r"arXiv:(\d{4}\.\d{4,5})", good).group(1)
    try:
        meta = fetch(arxiv_id)
    except (urllib.error.URLError, OSError) as e:
        print(f"selftest: arXiv unreachable ({e}); cannot run")
        return 0
    if meta is None:
        print(f"selftest: arXiv returned no entry for {arxiv_id}")
        return 1

    ok = True
    bad_name = good.split("\\emph")[0].rstrip().rstrip(",") + ", M. Krebs,\n\\emph" \
        + good.split("\\emph", 1)[1]
    got = compare(key, bad_name, meta)
    hit = any("not an author" in w for w in got)
    print(f"selftest: added a stranger's surname to [{key}]")
    print(f"  checker says: {got[0] if got else 'ok -- NOT REJECTED'}")
    print(f"  {'PASS' if hit else 'FAIL -- it slipped through'}")
    ok &= hit

    bad_title = re.sub(r"\\emph\{.*?\}",
                       "\\\\emph{On the density of sets avoiding distance one}",
                       good, count=1, flags=re.S)
    got = compare(key, bad_title, meta)
    hit = any("arXiv says" in w for w in got)
    print(f"selftest: transplanted another paper's title onto [{key}]")
    print(f"  checker says: {got[0] if got else 'ok -- NOT REJECTED'}")
    print(f"  {'PASS' if hit else 'FAIL -- it slipped through'}")
    ok &= hit
    return 0 if ok else 1


def main():
    if not os.path.exists(TEX):
        print("no manuscript here; nothing to check")
        return 0
    tex = open(TEX, encoding="utf-8").read()
    rows = entries(tex)
    if not rows:
        print("no thebibliography in the manuscript")
        return 1

    if "--selftest" in sys.argv:
        return selftest(tex)

    checked, skipped, bad = 0, [], []
    for key, entry in rows:
        m = re.search(r"arXiv:(\d{4}\.\d{4,5})", entry)
        if not m:
            skipped.append(key)
            continue
        arxiv_id = m.group(1)
        try:
            meta = fetch(arxiv_id)
        except (urllib.error.URLError, OSError) as e:
            print(f"arXiv unreachable ({e}); checked {checked} of "
                  f"{len(rows) - len(skipped)} entries before stopping")
            return 0
        if meta is None:
            bad.append((key, [f"arXiv has no record of {arxiv_id}"]))
        else:
            why = compare(key, entry, meta)
            checked += 1
            print(f"  {key:<12} {arxiv_id}  {'ok' if not why else 'MISMATCH'}")
            if why:
                bad.append((key, why))
        time.sleep(PAUSE)

    print(f"\n{checked} entries checked against arXiv, {len(bad)} wrong")
    for key, why in bad:
        for w in why:
            print(f"  [{key}] {w}")
    if skipped:
        print(f"\n{len(skipped)} entries carry no arXiv id and were NOT checked: "
              + ", ".join(skipped))
        print("  these are blog comments, wiki pages and a preprint deposit; "
              "they have no machine-readable source to compare against.")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
