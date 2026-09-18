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

run () {                       # run <label> <timeout> <args...>
  local label=$1; shift
  local secs=$1; shift
  local log="$OUT/$label.log"
  local t0=$SECONDS
  timeout "$secs" $PY -u "$@" > "$log" 2>&1
  local rc=$?
  printf '%-22s %-8s %5ds  %s\n' "$label" \
    "$( [ $rc -eq 0 ] && echo PASS || { [ $rc -eq 124 ] && echo TIMEOUT || echo "FAIL($rc)"; } )" \
    "$((SECONDS - t0))" "$log"
}

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
run join_filter12    1800 scripts/join_filter_residues.py 12
run join_filter20    1800 scripts/join_filter_residues.py 20
run rho_unit_family  1800 scripts/rho_unit_family.py
run prove_step5      5400 scripts/prove_step5.py
run z4_relation      4200 scripts/z4_relation.py 100
run lambda_sweep    10800 scripts/lambda_sweep.py
echo "=== done ==="
