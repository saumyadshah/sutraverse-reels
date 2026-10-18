# Hindi narration — writing and voicing

## Voice of the channel
A warm, mature storyteller talking *to one person*. Conversational modern Hindi (the Hindi of a good podcast, not of a sermon or a news bulletin). Address the viewer as **आप**. Short sentences. One idea per line.

**Do**
- Everyday words: *ग़ुस्सा* not *क्रोध* in narration (the Sanskrit term can appear once as the scripture's word: "गीता इसे 'क्रोध' कहती है").
- Natural English where Indians actually use it: ऑफिस, मीटिंग, ईमेल, बॉस, प्रमोशन, मैसेज, स्ट्रेस — written in Devanagari.
- Questions and turns: "पर रुकिए…", "ध्यान दीजिए…", "यहीं सबसे बड़ी गलती होती है।"
- Verse names spoken simply: "भगवद गीता, अध्याय दो, श्लोक बासठ".

**Avoid**
- Sanskrit-heavy register (*अतः, तत्पश्चात, विद्यमान*), long compound sentences, bullet-style lists read aloud.
- Moralising ("हमें ऐसा करना चाहिए"); prefer showing consequence and choice.
- Claims stronger than the sources (see scripture-research.md claim types).

## Length and pacing
Plan with **~2.7–2.8 Hindi words per second including pauses** for local voices at speed 1.0 (measured with hi_rohan; `narrate.py` prints actual w/s). A 60 s Short (with a 3 s end card) ≈ 150–160 words; an 8-minute video ≈ 1,250–1,300 words. Slower cloud voices need ~10% fewer. Fix length by editing lines, never by inflating pauses.

Pauses: punctuation drives TTS phrasing — use commas for breaths, "…" or a separate line for a dramatic beat, `pause_after` for scene changes (defaults in config: 0.26 s line, 0.42 s scene; "…" beats 0.3 s).

## TTS-friendly spelling
- Numbers in words: "दस मिनट", "बासठ", not "10", "62".
- Write English words in Devanagari ("मीटिंग"), never Latin script, inside `hi`.
- Brand name: **सूत्रवर्स**.
- Use nukta where meaning/pronunciation needs it (ग़ुस्सा, ज़िंदगी, फ़ैसला); local voices handle it.
- If a word is mispronounced, add `hi_tts` with a respelling (e.g. split a compound, add a comma) — `hi` stays the clean script for the deliverable.
- Proper names: श्रीकृष्ण, अर्जुन, कर्ण, युधिष्ठिर, सीता, हनुमान, विदुर, चाणक्य, पतंजलि.

## Sounding human (what made v2 better than v1)
- **Talk, don't announce.** "आपका आइडिया… और तालियाँ किसी और को?" beats "मीटिंग में किसी ने आपका काम अपने नाम कर लिया"; fragments are fine.
- **Mark beats with "…" and "—".** `narrate.py` synthesizes each beat separately and inserts a real pause (config `voice.delivery`), so pacing breathes instead of running on. Mirror the beats in the English `en` so subtitles cut on them.
- **Ask the viewer questions**, then answer: "तो ग़ुस्सा आता कहाँ से है?"
- **Hinglish where Indians use it:** मीटिंग, ईमेल, ईगो, रिप्ले, ट्विस्ट, सीन, प्रमोशन (in Devanagari).
- **Short punch lines** (≤3 words) are slowed slightly; questions slightly slower; long connective phrases slightly quicker — automatic.
- Avoid textbook connectors (अतः, तत्पश्चात), and avoid stacking three clauses in one sentence.

## Voice selection (automatic, from `config.voice.preference`)
Natural, human-sounding Hindi needs a modern neural voice — configure one of these and it is used automatically:
1. **Gemini TTS** (`gemini_tts`, Google AI Studio key in `.env` as `GEMINI_API_KEY`) — most natural and directable. `voice.style_prompt` (or a per-video `voice_style` in `sv_script.json`) tells it how to perform. `narrate.py` records the **whole script in one take** (one API call, consistent voice and flow) and cuts it into lines at the natural pauses; long internal pauses are capped (`max_internal_pause_s`) and an optional pitch-preserving `tempo` (1.03–1.07) tightens runtime. Default model `gemini-3.1-flash-tts-preview`; free-tier keys hit per-model daily quotas (HTTP 429) — switch the `model:` in config (e.g. `gemini-2.5-flash-preview-tts`) or wait for the reset.
2. **ElevenLabs** (`elevenlabs_tts`) — very expressive; put a Hindi voice id in config.
3. **Azure Speech** (`azure_tts`, free F0 tier) — `hi-IN-MadhurNeural` / `hi-IN-SwaraNeural`; clean, slightly formal.
4. **Google Cloud TTS Chirp 3 HD** (`google_tts`).
5. **Local `sherpa_onnx_tts`** (free, offline): `hi_kokoro_psi` (default local — best back-translation score), `hi_rohan`, `hi_pratham`, `hi_priyamvada`, other Kokoro Hindi voices. Intelligible but audibly synthetic; good for drafts. Piper voices use livelier `local_tuning` settings; a broadcast EQ/compression chain (`voice.polish`) is applied to every narration.
Never fall back to an English voice. If nothing Hindi is available, stop and give the fix:
`python -m tools.audio.sherpa_onnx_tts --download hi_kokoro_psi`.

Licences: Piper Hindi voices are trained on IIT Madras IndicTTS data (royalty-free EULA; keep the IITM notice in project credits); Kokoro is Apache-2.0. Record the voice and licence in `asset_manifest`.

## Checking the voice
`narrate.py` measures each line; `qa_check.py` runs Whisper on the final audio: language must be detected as Hindi and the English back-translation should match the subtitles' keywords. For a new voice or unusual vocabulary, listen to (or back-translate) the first two lines before rendering everything.
