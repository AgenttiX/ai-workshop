#!/usr/bin/env bash
# Render an SVG (default: all poster*.svg) to build/<name>.png with headless (snap) Firefox.
# The snap cannot read /tmp, hence everything stays inside this folder.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p build/ffprofile
for svg in "${@:-poster*.svg}"; do
  for f in $svg; do
    timeout -k 5 60 firefox --headless --no-remote --profile "$PWD/build/ffprofile" \
      --screenshot "$PWD/build/${f%.svg}.png" --window-size=1123,1588 "file://$PWD/$f" >/dev/null 2>&1
  done
done
