#!/bin/bash
# Verify the one proof certificate this project ships.
#
# drat-trim is Marijn Heule's checker, a single C file.  We do not vendor it --
# a checker you got from the people whose proof you are checking is not a check.
# Fetch it yourself, build it, and run this.
#
#   curl -O https://raw.githubusercontent.com/marijnheule/drat-trim/master/drat-trim.c
#   cc -O2 -o drat-trim drat-trim.c
#   bash scripts/check_drat.sh ./drat-trim
#
# Expected: "s VERIFIED".  Takes about two minutes and 1 GB.
set -e
DT=${1:-drat-trim}
cd "$(dirname "$0")/.."
command -v "$DT" >/dev/null 2>&1 || [ -x "$DT" ] || {
  echo "no drat-trim at '$DT'.  See the header of this script." >&2; exit 1; }
echo "sha256 of the checker source you should have used:"
echo "  d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee  drat-trim.c"
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
gzip -dc proofs/509_not4col.drat.gz > "$T/509.drat"
# drat-trim draws its progress with carriage returns, so the verdict line
# arrives as "\rs VERIFIED" and an anchored grep misses it.  Strip the CRs.
"$DT" proofs/509_not4col.cnf "$T/509.drat" | tee "$T/out.txt"
if tr '\r' '\n' < "$T/out.txt" | grep -qx 's VERIFIED'; then
  echo "OK -- the certificate checks"
else
  echo "NOT VERIFIED -- drat-trim did not report success" >&2; exit 1
fi
