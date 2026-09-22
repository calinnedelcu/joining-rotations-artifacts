#!/bin/bash
# Run every script the paper's reproducibility table names, in roughly
# increasing cost, log each separately, and report pass/fail.  Output goes to
# files, never through a pipe: python buffers stdout when piped and a slow run
# then looks like a hung one.
cd "$(dirname "$0")/.." || exit 1
OUT=${OUT:-/tmp/verify}
mkdir -p "$OUT"

# The venv if there is one, otherwise whatever python3 is on PATH.  A fresh
# extraction of the distributed archive has no .venv, and hardcoding it made
# every entry fail with a bare "no such file".
if   [ -n "$PY" ];                   then :
elif [ -x .venv/bin/python ];        then PY=.venv/bin/python
elif command -v python3 >/dev/null;  then PY=$(command -v python3)
else echo "no python3 found; set PY=/path/to/python" >&2; exit 1
fi
echo "python: $PY  ($("$PY" -V 2>&1))"
"$PY" -c 'import pysat' 2>/dev/null \
  || echo "  note: python-sat is absent, so the solver entries will fail" >&2
echo

# Entries are collected first and executed at the end, so that JOBS>1 can send
# them through xargs -P.  Most are single-threaded and the machine is not, so a
# sequential run wastes most of the box: about three hours becomes about one.
SPECS="$OUT/_specs"
: > "$SPECS"
run    () { echo "$1 $2 $PY -u ${*:3}" >> "$SPECS"; }
sh_run () { echo "$*" >> "$SPECS"; }

echo "=== reproducing every claim in paper/README.md ==="
# --- the fast ones first, so a broken environment shows up in seconds --------
run audit_numbers    1800 scripts/audit_numbers.py
run moser_is_ov       600 scripts/moser_is_ov.py
run blind_spot        300 scripts/blind_spot.py
run finer_lattices    300 scripts/finer_lattices.py
run step5_signs       300 scripts/step5_signs.py
run two_colourings    300 scripts/two_colourings.py
run cross_kinds       900 scripts/cross_kinds.py
run gadget_chain      600 scripts/gadget_chain.py 3
run ball_params      3600 scripts/ball_params.py
run check_periodic    120 scripts/check_periodic.py
run check_emptyshell  120 scripts/check_emptyshell.py
run empty_shell_st   1800 scripts/empty_shell_status.py
run shells            300 scripts/shells.py 100
run shell_criterion   600 scripts/shell_criterion.py 400
run hept_rank         120 scripts/hept_rank.py
run hept_classify     300 scripts/hept_classify.py 1 2
run ib_exact_4        300 scripts/interface_bound_exact.py 4
run ib_exact_16       300 scripts/interface_bound_exact.py 16
run ib_exact_28       300 scripts/interface_bound_exact.py 28
run ib_exact_36       300 scripts/interface_bound_exact.py 36
run rank8_condition   600 scripts/rank8_condition.py
run interface_bound   900 scripts/interface_bound.py 4 --depth 4 --radius 2.53 --model shared
run interface_match   900 scripts/interface_matchings.py
run build_join16      900 scripts/build_join16.py
run prove_law_dir     900 scripts/prove_law_direction.py
run hept_halfunit     600 scripts/hept_halfunit.py 1
# --- and the long ones ------------------------------------------------------
run voronov          1800 scripts/voronov_rotations.py
# All eleven periodic exclusions, not the two that used to stand for them.  Three
# referees in a row made the same point: the lightweight validator checks a
# witness against its own pair list and says so in its header, so completeness
# rests on the generator -- and the suite ran the generator twice out of eleven.
# Nine of the eleven take seconds; 48 and 80 need m = 8 and take about 80.
run join_filter12    1800 scripts/join_filter_residues.py 12
run join_filter20    1800 scripts/join_filter_residues.py 20
run join_filter44    1800 scripts/join_filter_residues.py 44
run join_filter52    1800 scripts/join_filter_residues.py 52
run join_filter60    1800 scripts/join_filter_residues.py 60
run join_filter76    1800 scripts/join_filter_residues.py 76
run join_filter84    1800 scripts/join_filter_residues.py 84
run join_filter92    1800 scripts/join_filter_residues.py 92
run join_filter100   1800 scripts/join_filter_residues.py 100
run join_filter48    1800 scripts/join_filter_residues.py 48 --modulus 8
run join_filter80    1800 scripts/join_filter_residues.py 80 --modulus 8
run rho_unit_family  1800 scripts/rho_unit_family.py
run prove_step5      5400 scripts/prove_step5.py
run z4_relation      9000 scripts/z4_relation.py 100
run lambda_sweep    10800 scripts/lambda_sweep.py

# --- the claims the paper makes about this repository -----------------------
# Four review rounds found the same species of defect: a sentence saying what a
# script does or what the archive holds, overtaken by a change to the script or
# the archive, with nothing comparing the two.  check_paper.sh tests the PDF and
# check_notes.py tests cross-references; neither can see "this checker verifies
# properness" or "eight certificates".  This runs them.
run check_claims      1800 scripts/check_claims.py

# --- the bibliography, against the sources it names -------------------------
# Two entries were wrong for two days: one named a person who is not an author
# of the paper it cited, the other carried a different paper's title.  Every
# check above reads this repository; none of them opens an arXiv identifier, and
# neither did three rounds of referees.  This asks arXiv about each one and
# compares title and surnames.  Needs the network; with none it says so and
# passes, which is why it prints what it could not check rather than a count.
run check_bibliography 600 scripts/check_bibliography.py

# --- the certificates' graphs, before the certificates ----------------------
# check_drat.sh checks a stored CNF against a stored proof and never looks at
# the coordinates, so it cannot tell a proof about our graph from a proof about
# someone else's -- which this project has shipped once already.  This rebuilds
# each CNF from the shipped points through certify.py's own code path and
# compares bytes.  No solver.  The four full-ball instances are 140-170 MB and
# take minutes; the three small ones take seconds.
run check_binding    5400 scripts/check_binding.py

# --- the proof certificates -------------------------------------------------
# drat-trim is deliberately not vendored, so this entry reports SKIP rather
# than FAIL when it is absent: see proofs/README.md for the two build lines.
if [ -x ./tools/drat-trim ] || command -v drat-trim >/dev/null 2>&1; then
  DT=$( [ -x ./tools/drat-trim ] && echo ./tools/drat-trim || command -v drat-trim )
  sh_run check_drat     1800 bash scripts/check_drat.sh "$DT"
else
  printf '%-22s %-8s %5ds  %s\n' check_drat SKIP 0 "no drat-trim; see proofs/README.md"
fi

# --- the rendered paper -----------------------------------------------------
if command -v pdftotext >/dev/null 2>&1 && [ -f paper/joining-rotations.pdf ]; then
  sh_run check_paper      60 bash scripts/check_paper.sh
else
  printf '%-22s %-8s %5ds  %s\n' check_paper SKIP 0 "needs pdftotext and a built PDF"
fi

# --- the notes that ship with the manuscript --------------------------------
# Three rounds running, a referee found stale cross-references in these: a
# release that did not exist, a tag at the wrong commit, then six "Theorem N"
# left over from a renumbering.  The paper was fixed each time and the notes
# were not re-checked against it.  check_paper.sh tests the PDF; this tests
# the prose that ships beside it.
if [ -f paper/joining-rotations.aux ]; then
  run check_notes        60 scripts/check_notes.py COVER.md FOR-THE-REVIEWER.md VERIFICATION.md
else
  printf '%-22s %-8s %5ds  %s\n' check_notes SKIP 0 "needs the .aux; compile with --keep-intermediates"
fi

# --- execute -----------------------------------------------------------------
JOBS=${JOBS:-6}
RUNNER="$OUT/_run_one.sh"
cat > "$RUNNER" <<'EOS'
#!/bin/bash
label=$1; secs=$2; shift 2
log="$OUT/$label.log"
t0=$SECONDS
timeout "$secs" "$@" > "$log" 2>&1
rc=$?
printf '%-22s %-8s %5ds  %s\n' "$label" \
  "$( [ $rc -eq 0 ] && echo PASS || { [ $rc -eq 124 ] && echo TIMEOUT || echo "FAIL($rc)"; } )" \
  "$((SECONDS - t0))" "$log"
EOS
chmod +x "$RUNNER"
export OUT
echo "running $(wc -l < "$SPECS" | tr -d ' ') entries, $JOBS at a time"
echo
< "$SPECS" xargs -P "$JOBS" -L1 "$RUNNER"

echo
echo "=== done ==="
