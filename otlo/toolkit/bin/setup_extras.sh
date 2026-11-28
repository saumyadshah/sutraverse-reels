#!/bin/sh
# Install the optional engines on demand (tested in this environment on 28 Nov 2026). Each is idempotent.
#   sh otlo/toolkit/bin/setup_extras.sh manim | remotion | lemo | anidoodle | all
set -e
CHROME=$(ls -d /opt/pw-browsers/chromium-*/chrome-linux64/chrome 2>/dev/null | head -1)
case "${1:-all}" in
  manim|all)   # ManimGL (3b1b): needs Pango headers, Python 3.13 audioop shim, and a virtual display to render
    (dpkg -s libpango1.0-dev >/dev/null 2>&1 || (apt-get update -q && apt-get install -y -q libpango1.0-dev pkg-config xvfb)) >/dev/null
    pip install --break-system-packages -q manimgl audioop-lts
    echo "manim ready: xvfb-run -a -s '-screen 0 1280x1024x24' manimgl scene.py Scene -w --hd  (add --transparent for overlays)";;
esac
case "${1:-all}" in
  remotion|all) (cd otlo/toolkit/remotion && npm install --silent) && echo "remotion ready: --browser-executable=$CHROME";;
esac
case "${1:-all}" in
  lemo|all)    # Lemo Opuscar: NOT committed to this public repo (its docs are CC BY-NC with a no-redistribution clause)
    [ -d /tmp/lemo-opuscar ] || git clone -q --depth 1 https://github.com/lemomo-ai/lemo-opuscar /tmp/lemo-opuscar
    (cd /tmp/lemo-opuscar && npm install --silent) && echo "lemo ready: read /tmp/lemo-opuscar/styles/<style>/STYLE.md; demo stills: PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers node core/render/still.mjs styles/<style>/demo 5 --out /tmp/x --size 1080x1920";;
esac
case "${1:-all}" in
  anidoodle|all) (cd otlo/toolkit/anidoodle/engine && npm install --omit=optional --silent) && echo "anidoodle ready: PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers node tools/still.mjs <film> --out <png>";;
esac
