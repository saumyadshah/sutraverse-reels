#!/usr/bin/env bash
# SutraVerse environment setup, meant for the claude.ai/code environment's "Setup script".
# Runs once when a session's container starts, before any scheduled run begins, so the
# runs themselves never need to download or install anything.
#
# Paste this into the Default environment's setup script:
#   git clone -q --depth 1 https://github.com/saumyadshah/sutraverse-reels "$HOME/sutraverse-reels" 2>/dev/null \
#     || git -C "$HOME/sutraverse-reels" pull -q
#   bash "$HOME/sutraverse-reels/toolkit/env_setup.sh"   (returns at once; the install continues in the background)
#
# Result: $HOME/OpenMontage ready, and $HOME/.sutraverse_env with the HYPERFRAMES_BROWSER_PATH export.
# Never prints any key.
set -uo pipefail
REPO="$HOME/sutraverse-reels"
OM="$HOME/OpenMontage"
LOG="$HOME/.sutraverse_setup.log"

# The environment's setup script has a time limit, and a full install can run past it (exit -1 kills the
# session). So by default this script only starts the install in the background and returns at once.
# Every scheduled run already waits for $HOME/.sutraverse_env before it starts work.
if [ "${1:-}" != "--foreground" ]; then
  if [ -f "$HOME/.sutraverse_env" ]; then echo "SutraVerse toolkit already ready"; exit 0; fi
  if [ -f "$HOME/.sutraverse_setup.pid" ] && kill -0 "$(cat "$HOME/.sutraverse_setup.pid")" 2>/dev/null; then
    echo "SutraVerse setup already running"; exit 0
  fi
  setsid nohup bash "$0" --foreground </dev/null >/dev/null 2>&1 &
  echo $! > "$HOME/.sutraverse_setup.pid"
  echo "SutraVerse setup started in the background (log: $LOG); runs wait for $HOME/.sutraverse_env"
  exit 0
fi

{
  echo "== SutraVerse env setup $(date -u +%FT%TZ)"
  bash "$REPO/toolkit/bootstrap.sh" "$REPO/toolkit/sutraverse-skill.zip" "$OM"
} >"$LOG" 2>&1
status=$?

# Free 3D for optional Three.js scenes: vendor three.js locally so renders never need a CDN.
# Runs copy $HOME/sv-three/node_modules/three/build/three.module.min.js into the composition.
( [ -f "$HOME/sv-three/node_modules/three/build/three.module.min.js" ] \
  || npm install -s --prefix "$HOME/sv-three" three@0.169.0 ) >>"$LOG" 2>&1 || true

LINE="$(grep '^export HYPERFRAMES_BROWSER_PATH=' "$LOG" | tail -1)"
if [ -z "$LINE" ]; then
  # bootstrap stopped before printing it: fall back to the npm Chromium if it was installed
  BIN="$(cd "$HOME/sv-chromium" 2>/dev/null && node -e "require('@sparticuz/chromium').default.executablePath().then(p=>console.log(p)).catch(()=>require('@sparticuz/chromium').executablePath().then(p=>console.log(p)))" 2>/dev/null)"
  [ -n "$BIN" ] && [ -x "$BIN" ] && LINE="export HYPERFRAMES_BROWSER_PATH=$BIN"
fi
if [ -f "$OM/.claude/skills/sutraverse/scripts/narrate.py" ] && [ -n "$LINE" ] \
   && python3 -c "from PIL import Image; Image.new('RGB',(1,1))" 2>/dev/null; then
  printf '%s\nexport SUTRAVERSE_READY=1\n' "$LINE" > "$HOME/.sutraverse_env"
  echo "SutraVerse toolkit ready ($HOME/.sutraverse_env)"
else
  echo "SutraVerse toolkit setup FAILED (status $status); see $LOG"
fi
exit 0
