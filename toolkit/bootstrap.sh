#!/usr/bin/env bash
# One-command SutraVerse workspace setup for a fresh Linux session (used by scheduled runs).
#   bash bootstrap.sh /path/to/sutraverse-skill.zip [target_dir]
# Clones OpenMontage, unpacks the toolkit, installs Python/Node deps, Hindi voices, Whisper verifier
# and a headless Chromium, and writes .env from GEMINI_API_KEY / GOOGLE_API_KEY if present in the environment.
# Prints "BOOTSTRAP OK" and the env line to source at the end.
set -euo pipefail
ZIP="${1:?usage: bootstrap.sh <toolkit.zip> [target_dir]}"
ZIP="$(cd "$(dirname "$ZIP")" && pwd)/$(basename "$ZIP")"
OM="${2:-$HOME/OpenMontage}"

if [ ! -f "$OM/AGENT_GUIDE.md" ]; then
  git clone -q --depth 1 https://github.com/calesthio/OpenMontage.git "$OM"
fi
cd "$OM"
unzip -qo "$ZIP"

PIP="python3 -m pip install -q"
$PIP --break-system-packages -r requirements.txt 2>/dev/null || $PIP -r requirements.txt
$PIP --break-system-packages sherpa-onnx soundfile google-genai jsonschema numpy pillow pyyaml 2>/dev/null \
  || $PIP sherpa-onnx soundfile google-genai jsonschema numpy pillow pyyaml

python3 .claude/skills/sutraverse/scripts/setup_check.py --install >/dev/null 2>&1 || true

# headless Chromium for HyperFrames (works where Chrome downloads are blocked: comes from npm)
if [ -z "${HYPERFRAMES_BROWSER_PATH:-}" ] || [ ! -x "${HYPERFRAMES_BROWSER_PATH:-/nonexistent}" ]; then
  CH="$HOME/sv-chromium"
  mkdir -p "$CH" && cd "$CH"
  [ -f package.json ] || echo '{"name":"sv-chromium","version":"1.0.0","private":true}' > package.json
  npm i -s @sparticuz/chromium@153 >/dev/null 2>&1
  BIN="$(node -e "require('@sparticuz/chromium').default.executablePath().then(p=>console.log(p)).catch(()=>require('@sparticuz/chromium').executablePath().then(p=>console.log(p)))")"
  export HYPERFRAMES_BROWSER_PATH="$BIN"
  cd "$OM"
fi

# Gemini key from the environment (never stored anywhere else)
KEY="${GEMINI_API_KEY:-${GOOGLE_API_KEY:-}}"
if [ -n "$KEY" ] && ! grep -q "GEMINI_API_KEY=" .env 2>/dev/null; then
  printf 'GEMINI_API_KEY=%s\nGOOGLE_API_KEY=%s\n' "$KEY" "$KEY" >> .env
fi

python3 .claude/skills/sutraverse/scripts/setup_check.py | tail -25
echo "BOOTSTRAP OK"
echo "export HYPERFRAMES_BROWSER_PATH=$HYPERFRAMES_BROWSER_PATH"
[ -n "$KEY" ] && echo "VOICE: Gemini key found" || echo "VOICE: no Gemini key in this environment -> local Hindi voice only"
