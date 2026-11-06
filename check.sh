#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"

test -f README.md

fail=0

echo "== api tests (unittest)"
python3 -m unittest discover -s api -t . > /tmp/mono-api-out.txt 2>&1 || fail=1
tail -4 /tmp/mono-api-out.txt >&2
rm -f /tmp/mono-api-out.txt

echo "== web tests (node --test)"
node --test web/*.test.js > /tmp/mono-web-out.txt 2>&1 || fail=1
tail -8 /tmp/mono-web-out.txt >&2
rm -f /tmp/mono-web-out.txt

if [ "$fail" -eq 0 ]; then
  echo "checks passed"
fi
exit "$fail"
