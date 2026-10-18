# Quality gates — check the real output, fix, re-render

Run `python .claude/skills/sutraverse/scripts/qa_check.py <id>` after every final render. It writes `qa/qa_report.json`, `qa/speech_check.json`, scene frames and `qa/contact_sheet.jpg`. Then **look at the frames yourself** (Read the PNG/JPG files) — automated checks do not see ugliness, clipping text or cultural missteps.

| Check | Pass | Typical fix |
|---|---|---|
| container | exact WxH and fps of the format | wrong `format` in sv_script / config |
| duration | render == timing total (±0.25 s) | rebuild composition after re-narration |
| audio | AAC stream present, tagged `hin` | finalize mux step failed — rerun `finalize.py --skip-render` |
| loudness | −14 LUFS ±1.5 (short & long) | `loudness_lufs` in config; re-mix |
| true_peak / clipping | ≤ −1 dBTP, 0 clipped samples | lower bed level; mixer limiter |
| audibility | narration ≥ 12 dB above the bed in pauses | lower `music.bed_volume_db` or `duck_to` |
| sync | rendered audio offset ≤ 40 ms vs narration | never edit audio after timing; rebuild + re-mux |
| speech_lang | Whisper detects Hindi in every window | wrong voice/tool; never ship English narration |
| meaning | Whisper EN translation shares keywords with subtitles (≥0.35) | mispronunciation (add `hi_tts`) or a subtitle that drifted from the Hindi |
| subtitles | English only, in range, no overlap, line length, ≤ ~20 cps | shorten `en`, split long lines |
| on_screen | no Devanagari outside a verified `.sv-sanskrit` block | rewrite phrase in English |
| branding | opening, watermark, end card present; end card visibly gold | don't remove brand nodes; check config |
| motion | every scene's 25% vs 75% frames differ | add drift/particles/character action |
| hook | frame 0 already moving; first spoken word ≤ 0.5 s | animate from t=0; `lead_in_seconds` 0.15–0.2 |
| cadence | every spoken line visibly changes the picture | cut/animate on `T.lines[id].phrases` |

## Human-eye review (do it on the contact sheet + key frames)
- Text never clipped, never collides with captions, readable on a phone (look at 270-px-wide thumbnails: still legible?).
- Hook frame is striking within the first second; the opening identity doesn't hide it.
- Character designs consistent across scenes; deities/sages depicted with dignity.
- Colour stays in palette; no flat yellow "gold"; ember used only for conflict.
- Transitions smooth; no blank/black frames; end card clean.
- Scripture reference chips match `sources.json` exactly.

Max two fix rounds per issue (OpenMontage reviewer protocol); then deliver with the remaining warnings stated plainly.
