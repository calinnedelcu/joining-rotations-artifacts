#!/bin/bash
# Check the built PDF for the defects a compile does not fail on.
#
# A referee found two "??" in a draft whose companion note claimed "0 unresolved
# references".  The claim was made by grepping tectonic's .log for "undefined" --
# and tectonic writes no .log unless asked, so the grep matched nothing and the
# absence was read as success.  The only honest test is on the PDF itself.
#
#   bash scripts/check_paper.sh [paper/joining-rotations.pdf]
set -e
cd "$(dirname "$0")/.."
PDF=${1:-paper/joining-rotations.pdf}
[ -f "$PDF" ] || { echo "no PDF at $PDF -- compile first" >&2; exit 1; }
command -v pdftotext >/dev/null || { echo "needs pdftotext (poppler)" >&2; exit 1; }

T=$(mktemp); trap 'rm -f "$T"' EXIT
pdftotext "$PDF" "$T"
fail=0

n=$(grep -c '??' "$T" || true)
if [ "$n" -gt 0 ]; then
  echo "FAIL: $n unresolved reference(s) -- '??' in the rendered text:"
  grep -n '??' "$T" | sed 's/^/    /'
  fail=1
else
  echo "ok   no unresolved references"
fi

n=$(grep -c 'TO BE SUPPLIED' "$T" || true)
if [ "$n" -gt 0 ]; then
  echo "note: $n placeholder(s) still to fill:"
  grep -n 'TO BE SUPPLIED' "$T" | sed 's/^/    /'
else
  echo "ok   no placeholders"
fi

echo "     $(pdfinfo "$PDF" | awk '/^Pages/{print $2}') pages"
exit $fail
