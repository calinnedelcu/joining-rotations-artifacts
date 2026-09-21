# Verification transcript

Every check we ran, with its output, so you can compare your run against ours
rather than take a summary on trust. Machine: Apple M5, 32 GB, macOS, ten cores.
Reproduce any line with the command above it.

Archive: the Zenodo deposit at DOI 10.5281/zenodo.22855504, or the repository at
the release that deposit was cut from. The paper pins commit
`105e3f586d9d12d967ed769ffb31bfbd99bbacb2` for its code and data, and nothing the
suite below runs changed after it. A shallow clone is about 900 MB, most of it
proof.

The transcript was taken at an earlier commit. Five scripts and one README have
changed since, and section 1's table predates all of them: `certify.py`, which
named a build directory that is not shipped and has since gained `--emit-only`;
`check_binding.py`, which is new and rebuilds each certified CNF from the
shipped coordinates; `check_notes.py`, which learned to compare commit hashes;
`check_paper.sh`, which gained the test that compiles the shipped source against
the shipped PDF, quoted current in section 5; and `verify_all.sh`, which grew
from 35 entries to 46 — the binding check, and nine periodic regenerations that
two rows used to stand for. Each addition was run on its own and passes; what is
not here is a single transcript of all 46 together.

---

## 1. The suite as it stood at the transcript — 35 of 35

    OUT=/tmp/verify JOBS=6 bash scripts/verify_all.sh

Entries run in parallel (`JOBS`, default 6); one at a time takes about three
hours, six at a time a little over one.

Nine of the thirty-five belong to the companion paper rather than to this one —
`ib_exact_4/16/28/36`, `interface_bound`, `interface_match`, `hept_classify`,
`hept_halfunit`, `hept_rank`. They are left in because the archive serves both
papers; a referee of this manuscript can ignore their rows.

```
audit_numbers          PASS       144s
ball_params            PASS       169s
blind_spot             PASS         0s
build_join16           PASS        56s
check_drat             PASS       410s
check_emptyshell       PASS         0s
check_paper            PASS         0s
check_periodic         PASS         0s
cross_kinds            PASS       136s
empty_shell_st         PASS       885s
finer_lattices         PASS         0s
gadget_chain           PASS        32s
hept_classify          PASS         3s
hept_halfunit          PASS       167s
hept_rank              PASS         2s
ib_exact_16            PASS        11s
ib_exact_28            PASS        28s
ib_exact_36            PASS        42s
ib_exact_4             PASS         1s
interface_bound        PASS         9s
interface_match        PASS        60s
join_filter12          PASS         6s
join_filter20          PASS        13s
lambda_sweep           PASS      3409s
moser_is_ov            PASS         0s
prove_law_dir          PASS         1s
prove_step5            PASS      1776s
rank8_condition        PASS         7s
rho_unit_family        PASS       697s
shell_criterion        PASS       180s
shells                 PASS         2s
step5_signs            PASS         0s
two_colourings         PASS         1s
voronov                PASS         8s
z4_relation            PASS      1979s
```

Totals: **35 PASS, 0 FAIL, 0 TIMEOUT**.

---

## 2. The eight certificates, from a clean clone of the public archive

Not from our working tree — from `git clone` of the archive, with `drat-trim`
built from source on the spot, to check the path a referee actually takes.

    git clone --depth 1 https://github.com/calinnedelcu/joining-rotations-artifacts.git
    cd joining-rotations-artifacts && mkdir -p tools && cd tools
    curl -O https://raw.githubusercontent.com/marijnheule/drat-trim/master/drat-trim.c
    cc -O2 -o drat-trim drat-trim.c && cd ..
    bash scripts/check_drat.sh ./tools/drat-trim

```
== 509_not4col
s VERIFIED
c verification time: 67.500 seconds
OK -- 509_not4col checks
== alpha256_9
s VERIFIED
c verification time: 27.431 seconds
OK -- alpha256_9 checks
== alpha64_3
s VERIFIED
c verification time: 30.981 seconds
OK -- alpha64_3 checks
== alpha64_9
s VERIFIED
c verification time: 19.558 seconds
OK -- alpha64_9 checks
== gadget367
s VERIFIED
c verification time: 17.810 seconds
OK -- gadget367 checks
== theta16
s VERIFIED
c verification time: 25.915 seconds
OK -- theta16 checks
== theta28
s VERIFIED
c verification time: 43.809 seconds
OK -- theta28 checks
== theta36
s VERIFIED
c verification time: 81.188 seconds
OK -- theta36 checks
```

Eight of eight. The `drat-trim.c` we built has sha256
`d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee`, which the
script prints so you can compare.

---

## 3. The numbers, on a bare interpreter

No `pysat`, no virtualenv, no solver — system `python3` 3.14 from a clean clone.

    python3 scripts/audit_numbers.py

```
  ok  and excluded 27: 97 < 99                                                 True

every number checks
```

97 checks, all ok.

---

## 4. The witnesses

    python3 scripts/check_emptyshell.py
    python3 scripts/check_periodic.py

```
   a  rank  units   verdict  witness
   8     8     60    killed  Klein colouring, kernel <34,145>, avoids all 60
  24     8     72  survives  a vector of length 1/2 -> Proposition 5
  32     8     60    killed  Klein colouring, kernel <33,211>, avoids all 60
  40     8     60    killed  Klein colouring, kernel <33,195>, avoids all 60
  56     8     60    killed  Klein colouring, kernel <34,156>, avoids all 60
  68     8     60    killed  Klein colouring, kernel <34,153>, avoids all 60
  72     8     72  survives  a vector of length 1/2 -> Proposition 5
  88     8     72  survives  a vector of length 1/2 -> Proposition 5
  96     8     60    killed  Klein colouring, kernel <38,216>, avoids all 60

9 witnesses, 0 bad

theta_84      4      256     69  ok
theta_92      4      256     69  ok

11 witnesses, 0 bad
```

The three that survive carry a vector of length 1/2 rather than a search log:
by Proposition 5 that is a one-line proof that no homomorphism onto a group of
order 4 avoids the unit vectors. The checker computes those lengths itself, from
the multiquadratic field's own multiplication table, importing nothing from this
project.

---

## 5. The rendered paper

    bash scripts/check_paper.sh

```
ok   no unresolved references
ok   no placeholders
     25 pages
ok   the shipped source reproduces the shipped PDF
```

Run against the submitted manuscript, which is the copy bundled in the archive.
The fourth line is the check that a referee's compile of the shipped source
gives back the shipped PDF: it was added after that compile produced 42 pages
against a 24-page submission, and a paper missing a proof the PDF still had. An
earlier draft of this transcript quoted a bundled copy whose DOI and affiliation
were still unfilled — a contradiction with the cover note, caught in review.

This check exists because a previous draft claimed "0 unresolved references"
while containing two `??`. The claim had been made by grepping the TeX engine's
`.log` for "undefined" — and the engine writes no `.log` unless asked, so the
grep matched nothing and the absence read as success. The only honest test is on
the rendered PDF.
