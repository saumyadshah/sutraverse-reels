# Installing the SutraVerse skill into OpenMontage

## 1. Get OpenMontage
```bash
git clone https://github.com/calesthio/OpenMontage.git
cd OpenMontage
pip install -r requirements.txt
```
Node.js 22+ and FFmpeg are required for HyperFrames rendering.

## 2. Copy the SutraVerse files into the repo root
Unzip `sutraverse-skill.zip` at the OpenMontage root. It adds:

| Path | What |
|---|---|
| `.claude/skills/sutraverse/` | the Claude Code skill (SKILL.md, config, references, templates, scripts, brand kit) |
| `.claude/commands/sutraverse.md` | `/sutraverse` slash command |
| `tools/audio/sherpa_onnx_tts.py` | offline Hindi TTS provider — auto-joins `tts_selector` |
| `tools/audio/gemini_tts.py` | patched OpenMontage Gemini TTS tool: fixes a client-lifetime bug ("client has been closed"), adds a timeout, and adds the 3.1/2.5 preview TTS models via the REST endpoint (fails fast on quota 429 instead of hanging) |
| `styles/sutraverse.yaml` | SutraVerse style playbook (schema-validated) |
| `.claude/skills/<23 folders>` | engagement skills vendored from Ootto-AI/claude-content-skills (MIT, each folder has `VENDORED.md` + `LICENSE`): virality, going-viral, viral-hook-writer, reel-scripter, youtube-scriptwriting, youtube-seo, youtube-thumbnail, cta-writer, caption-and-hashtags, series-planner and more |
| `skills/INDEX.md` | index entry for the skill + playbook (replaces the stock file; only two table rows were added) |

## 3. Install the free local pieces (Hindi voices + Whisper verifier)
```bash
python .claude/skills/sutraverse/scripts/setup_check.py --install
npx hyperframes browser ensure        # headless Chrome for rendering
python .claude/skills/sutraverse/scripts/setup_check.py   # should show READY lines
```
Windows: run these in PowerShell or Git Bash from the repo root. If `browser ensure` cannot download Chrome, set `HYPERFRAMES_BROWSER_PATH` to an installed Chrome/Edge executable.

## 4. Natural Hindi voice (strongly recommended) and other upgrades (add to `.env`)
- **Gemini TTS** (most natural, directable): `GOOGLE_API_KEY=` from Google AI Studio. It is first in the voice order, so it is used as soon as the key is present.
- Other Hindi voices: `AZURE_SPEECH_KEY` (+ region) → `hi-IN-MadhurNeural`, or `ELEVENLABS_API_KEY` and put a Hindi voice id in `config/sutraverse.yaml`, or `GOOGLE_API_KEY` → Chirp3 HD Hindi.
- Painterly images / AI motion: `FAL_KEY` (unlocks FLUX images and several video models), or any other image/video provider listed by `setup_check.py`.

## 5. Use it
Open Claude Code in the OpenMontage folder and say, for example:
> Create a 60-second Reel explaining Krishna's teaching on controlling anger, with a modern workplace example.

or `/sutraverse 8-minute YouTube video on attachment and relationships through the Bhagavad Gita`.

Change brand colours, CTA, handle, voice order, durations or loudness in `.claude/skills/sutraverse/config/sutraverse.yaml`.

## Optional: the full Ootto skill set
Only the 23 skills SutraVerse uses are vendored. For the rest (lead-gen DMs, auto-posting, Obsidian memory) install the upstream plugin in Claude Code:
`/plugin marketplace add Ootto-AI/claude-content-skills` then `/plugin install claude-content-skills@ootto-content-skills`. Those post or message on your behalf — review them before enabling.
