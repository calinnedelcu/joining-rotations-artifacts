#!/bin/zsh
# Decide a rotation at m=4, and fall back to m=8 when m=4 is degenerate.
cd "$(dirname $0)/.."
for A in "$@"; do
  out=$(timeout 900 .venv/bin/python -u scripts/join_filter_residues.py $A 2>&1)
  v=$(echo "$out" | grep -oE "DEAD|SURVIVES at modulus|DEGENERATE AT MODULUS|EMPTY" | head -1)
  if [[ "$v" == "DEGENERATE AT MODULUS" ]]; then
    out=$(timeout 900 .venv/bin/python -u scripts/join_filter_residues.py $A --modulus 8 2>&1)
    v8=$(echo "$out" | grep -oE "DEAD|SURVIVES at modulus|DEGENERATE AT MODULUS|EMPTY" | head -1)
    printf "%-8s m=4 degenerate -> m=8: %s\n" "$A" "$v8"
  else
    printf "%-8s %s\n" "$A" "$v"
  fi
done
