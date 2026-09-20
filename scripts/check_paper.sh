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

PAGES=$(pdfinfo "$PDF" | awk '/^Pages/{print $2}')
echo "     $PAGES pages"

# Does the shipped source actually produce the shipped PDF?  A referee compiled
# the pinned .tex and got 42 pages against a 24-page submission, because the
# source had been left six weeks behind while the PDF was kept current -- and
# the paper it produced still contained a proof the PDF had lost.  Page count
# and placeholder checks cannot see that; compiling can.
TEX=${PDF%.pdf}.tex
if [ -f "$TEX" ] && command -v tectonic >/dev/null 2>&1; then
  B=$(mktemp -d); trap 'rm -rf "$B" "$T"' EXIT
  cp -R "$(dirname "$TEX")"/* "$B"/ 2>/dev/null
  if (cd "$B" && tectonic -X compile "$(basename "$TEX")" >/dev/null 2>&1); then
    P2=$(pdfinfo "$B/$(basename "$PDF")" | awk '/^Pages/{print $2}')
    pdftotext "$B/$(basename "$PDF")" "$B/src.txt" 2>/dev/null
    if [ "$P2" != "$PAGES" ]; then
      echo "FAIL: the source compiles to $P2 pages, the shipped PDF has $PAGES"
      fail=1
    elif ! diff -q <(tr -s '[:space:]' ' ' < "$T") <(tr -s '[:space:]' ' ' < "$B/src.txt") >/dev/null 2>&1; then
      echo "note: source and PDF agree on $PAGES pages but differ in text"
    else
      echo "ok   the shipped source reproduces the shipped PDF"
    fi
  else
    echo "note: the source did not compile here; source/PDF agreement unchecked"
  fi
else
  echo "note: no .tex beside the PDF, or no tectonic; source/PDF agreement unchecked"
fi

exit $fail
