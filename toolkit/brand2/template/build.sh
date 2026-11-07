#!/bin/sh
# Render a SutraVerse 2.0 Reel page with Lemo-Opuscar. Needs: source ~/.opuscar_env (toolkit/opuscar_setup.sh).
set -e
HERE=$(cd "$(dirname "$0")" && pwd); NAME=${1:-reel}
[ -f "$LIB/core/render/video.mjs" ] || { echo "run toolkit/opuscar_setup.sh and source ~/.opuscar_env"; exit 1; }
B2=$(cd "$HERE/.." && pwd)
for f in brand2.css cast2.js cast2.json; do [ -f "$HERE/$f" ] || cp "$B2/$f" "$HERE/"; done
[ -d "$HERE/fonts" ] || cp -r "$B2/fonts" "$HERE/"
cd "$LIB"
node core/render/events.mjs "$HERE" --size 1080x1920
node core/render/video.mjs "$HERE" --fps 30 --size 1080x1920 --workers 4 --out "$HERE/out/video.mp4"
"$LIB/.venv/bin/python" "$HERE/mix.py"
sh core/render/mux.sh "$HERE/out/video.mp4" "$HERE/out/mix.wav" "$HERE/$NAME.mp4" 30 1
