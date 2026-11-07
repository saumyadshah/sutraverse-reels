# Lemo-Opuscar in the SutraVerse 2.0 pipeline

[Lemo-Opuscar](https://github.com/lemomo-ai/lemo-opuscar) (MIT code, CC BY 4.0 docs) is a library of 66 film styles plus a frame-by-frame renderer: every frame is a web page drawn by `render(t)` and captured by headless Chrome, with a shared toolkit for sampled music, procedural foley, subtitles, reading-time checks and a −14 LUFS master. Tested here on 7 Nov 2026 (pinned commit `b2a421e`): a 20 s 1080x1920 30 fps Reel renders in ~46 s (600 frames, 4 workers), muxes at −14.6 LUFS.

## What we use it for
- **Directing method**: `DIRECTOR.md` (benchmark first, treatment with three candidate structures, shot list, beat sheet, cue map, sound design table, model sheet + style frames before animating, two silences, J/L cuts, ≥4 camera moves, one native move at the peak, one fix round). Every 2.0 Reel follows it.
- **Rendering**: `core/render/video.mjs` + our template (`brand2/template/`), `still.mjs` + `sheet.py` for contact sheets, `readcheck.mjs` for reading time, `mux.sh` for loudness.
- **Sound**: `core/audio/sampler.py` (CC0/CC BY sample libraries: flute, strings, frame drum, harp…), `pluck.py` (sitar/veena-like plucked strings with bends), `sfx.py` (foley from `window.EV`).
- **Style techniques**: the library styles named as the base of each treatment in `TREATMENTS.md` (engraving, woodcut, halftone-dossier, briefing-board, midcentury-toon, dark-keynote, archive-lighttable, transit-map, shadow-puppet, paper-lantern, dataviz, iso-infographic, whiteboard). Read a style's `STYLE.md` for grammar; the demo sources are not in our sparse clone (and are never rebuilt).

## What we don't use
- Kokoro / edge-tts voices: SutraVerse keeps its Gemini Hinglish narration (sutraverse skill `narrate.py`); Opuscar's `asr_check.py` can still verify it (faster-whisper, needs `setup.sh deps voice`).
- Its map rule §13 (written for China's standard map). **SutraVerse map rule:** draw coastlines, rivers and terrain without political borders unless the story is about them; when India's borders are shown, follow the Survey of India depiction; frame disputed areas out otherwise; credit the map data in `CREDITS`.
- LemoLab credit/sign-off: films outside the library carry no LemoLab credit (their AGENTS.md says so); we keep a `CREDITS` file for samples, fonts and data.

## Setup (every production run)
```sh
bash $HOME/sutraverse-reels/toolkit/opuscar_setup.sh && . $HOME/.opuscar_env   # ~16 s first time, ~1 s after
```
It clones the library sparsely at the pinned commit, installs its npm and Python core tiers without downloading a browser, points `PLAYWRIGHT_CHROME` at the Chromium we already have, and puts an ffmpeg 7+ (imageio-ffmpeg) first on `PATH` (Opuscar's `mux.sh` needs ffmpeg ≥ 7). Instruments: `sh $LIB/tools/fetch.sh instruments vsco2ce` (≈ 400 MB, from GitHub Releases) only when a score needs sampled instruments; otherwise synthesize.

## Making a Reel with the template
1. `cp -r $HOME/sutraverse-reels/toolkit/brand2/template $HOME/films/<slot-id>` (build.sh copies brand2.css, cast2.js, cast2.json and fonts in).
2. Write `shots.js` from the shot list: `DUR`, `SHOTS` (t0, t1, draw(H, lt, T, t), html(lt, T), tag, chip), `SUBS` (from the voice timing), `EV` (sound events).
   - Characters only via `H.CAST2.draw(g, '<name>', {x, y, s, yaw, mood, talk, blink, lookX, arms, style})`; `talk` = phase in radians while the character speaks.
   - Treatment helpers: `H.printWipe(p)` (Chanakya Files plate print), `H.glow`, `H.grain`; add helpers to the template when a treatment needs one, then commit them back.
3. Voice: render the Gemini narration with the sutraverse skill, place it in `out/vo.wav`, and add it to `mix.py` (compress, then sit the music ~10 dB under the voice).
4. `. ~/.opuscar_env && sh build.sh <slot-id>` → `<slot-id>.mp4` (1080x1920, 30 fps, −14 LUFS).
5. Checks: `node $LIB/core/render/readcheck.mjs <dir> --size 1080x1920`, a contact sheet every second (`still.mjs --range 0:DUR:1` + `sheet.py`), 0.2 s strips of key actions, then the independent review.

## Performance notes
- 2D canvas is fast (≈ 13 frames/s/worker). WebGL / three.js runs on SwiftShader (no GPU) and is slow: keep 3D to one short shot or pre-render it once and reuse it (the Paper Portal frames in `brand-v4/assets/portal/`).
- Grain belongs in `mux.sh` (argument 6), not drawn per frame, except a light per-frame grain for texture.
