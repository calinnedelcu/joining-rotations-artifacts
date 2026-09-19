#!/bin/bash
# Verify a proof certificate this project ships.
#
# drat-trim is Marijn Heule's checker, a single C file.  We do not vendor it --
# a checker you got from the people whose proof you are checking is not a check.
# Fetch it yourself, build it, and run this.
#
#   curl -O https://raw.githubusercontent.com/marijnheule/drat-trim/master/drat-trim.c
#   cc -O2 -o drat-trim drat-trim.c
#   bash scripts/check_drat.sh ./drat-trim              # every certificate
#   bash scripts/check_drat.sh ./drat-trim 509_not4col  # just one
#
# Expected: "s VERIFIED" for each.  The 509 instance takes about two minutes and
# 1 GB; the others are listed in proofs/README.md with their own figures.
set -e
DT=${1:-drat-trim}
cd "$(dirname "$0")/.."
command -v "$DT" >/dev/null 2>&1 || [ -x "$DT" ] || {
  echo "no drat-trim at '$DT'.  See the header of this script." >&2; exit 1; }
echo "sha256 of the checker source you should have used:"
echo "  d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee  drat-trim.c"

if [ -n "$2" ]; then
  NAMES="$2"
else
  NAMES=$(for f in proofs/*.drat.gz; do basename "$f" .drat.gz; done)
fi

T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
fail=0
for n in $NAMES; do
  # The four largest CNFs are 140-170 MB raw, so they ship gzipped like the
  # proofs.  Accept either form; drat-trim needs a real file, so unpack first.
  if   [ -f "proofs/$n.cnf" ];    then CNF="proofs/$n.cnf"
  elif [ -f "proofs/$n.cnf.gz" ]; then CNF="$T/p.cnf"; gzip -dc "proofs/$n.cnf.gz" > "$CNF"
  else CNF=""; fi
  [ -n "$CNF" ] && [ -f "proofs/$n.drat.gz" ] || {
    echo "== $n: FAILED -- no such certificate in proofs/" >&2; fail=1; continue; }
  echo "== $n"
  gzip -dc "proofs/$n.drat.gz" > "$T/p.drat"
  # drat-trim draws its progress with carriage returns, so the verdict line
  # arrives as "\rs VERIFIED" and an anchored grep misses it.  Strip the CRs.
  "$DT" "$CNF" "$T/p.drat" | tee "$T/out.txt"
  if tr '\r' '\n' < "$T/out.txt" | grep -qx 's VERIFIED'; then
    echo "OK -- $n checks"
  else
    echo "NOT VERIFIED -- drat-trim did not report success for $n" >&2; fail=1
  fi
  rm -f "$T/p.drat" "$T/p.cnf"
done
exit $fail
