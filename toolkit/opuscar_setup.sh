#!/usr/bin/env bash
# Lemo-Opuscar for SutraVerse 2.0 (film-style library + frame-by-frame renderer; MIT code, CC BY 4.0 docs).
# Idempotent and quiet; safe to run at the start of every production run (~1 s when already installed).
#   bash toolkit/opuscar_setup.sh        → $HOME/lemo-opuscar ready, writes $HOME/.opuscar_env
# What it does (no system installs, no browser download):
#   - sparse, shallow clone of github.com/lemomo-ai/lemo-opuscar pinned to a tested commit (guides, core/, STYLE.md files)
#   - npm packages with PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1; renders use the Chromium we already have
#   - a Python venv with the core tier (numpy, scipy, soundfile, soxr, pillow, fonttools) + imageio-ffmpeg (ffmpeg 7+, mux.sh needs it)
set -uo pipefail
PIN="${OPUSCAR_PIN:-b2a421e55b95964b864badc94c2f35d9774ff745}"
LIB="${LEMO_OPUSCAR_HOME:-$HOME/lemo-opuscar}"
BIN="$HOME/.sv-bin"; ENVF="$HOME/.opuscar_env"; LOG="$HOME/.opuscar_setup.log"
{
echo "== opuscar setup $(date -u +%FT%TZ) pin $PIN"
if [ ! -f "$LIB/core/render/video.mjs" ]; then
  rm -rf "$LIB"
  git clone -q --filter=blob:none --sparse https://github.com/lemomo-ai/lemo-opuscar "$LIB" || { echo "clone failed"; exit 1; }
  (cd "$LIB" && git sparse-checkout set --no-cone '/*' '!/styles/*/demo/' '!/styleboard/' '!/docs/frames/' '!/docs/*.jpg' '!/styles/*/poster.jpg')
fi
(cd "$LIB" && git fetch -q --depth 1 origin "$PIN" 2>/dev/null; git checkout -q "$PIN" 2>/dev/null || true)
if [ ! -f "$LIB/node_modules/playwright-core/package.json" ]; then
  (cd "$LIB" && PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm ci --silent --no-audit --no-fund 2>&1 | tail -3)
fi
if [ ! -x "$LIB/.venv/bin/python" ]; then python3 -m venv "$LIB/.venv"; fi
"$LIB/.venv/bin/python" -c "import numpy, scipy, soundfile, soxr, PIL, imageio_ffmpeg" 2>/dev/null \
  || "$LIB/.venv/bin/pip" install -q --disable-pip-version-check -r "$LIB/requirements.txt" imageio-ffmpeg
mkdir -p "$BIN"; FF="$("$LIB/.venv/bin/python" -c 'import imageio_ffmpeg as i; print(i.get_ffmpeg_exe())')"
ln -sf "$FF" "$BIN/ffmpeg"
CHROME="${PLAYWRIGHT_CHROME:-${HYPERFRAMES_BROWSER_PATH:-}}"
[ -n "$CHROME" ] && [ -x "$CHROME" ] || CHROME="$(python3 -c 'from playwright.sync_api import sync_playwright as s; p=s().start(); print(p.chromium.executable_path); p.stop()' 2>/dev/null)"
printf 'export LEMO_OPUSCAR_HOME=%s\nexport LIB=%s\nexport PLAYWRIGHT_CHROME=%s\nexport PATH=%s:$PATH\n' "$LIB" "$LIB" "$CHROME" "$BIN" > "$ENVF"
echo "ok: LIB=$LIB chrome=$CHROME ffmpeg=$("$BIN/ffmpeg" -version | head -1 | cut -c1-40)"
} >>"$LOG" 2>&1
tail -1 "$LOG"
