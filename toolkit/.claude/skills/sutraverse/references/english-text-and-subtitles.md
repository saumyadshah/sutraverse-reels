# English on screen: subtitles, phrases, references

Everything a viewer *reads* is English. Two different text systems run in every video — keep them separate.

## A. Subtitles (the `en` field of each script line)
- Translate the **meaning and tone** of the Hindi line into natural English. Not word-for-word; not embellished. If the Hindi says "पूरा दिन खराब कर दिया", write "ruined your whole day", not "devastated your entire existence".
- Keep proper nouns consistent: Krishna, Arjuna, Bhagavad Gita, Mahabharata, Ramayana, Karna, Vidura, Chanakya, Patanjali.
- Sanskrit terms: italic-free plain text with a gloss the first time ("anger — *krodha*" is for on-screen phrases, not subtitles; in subtitles prefer the English word).
- Timing is automatic and exact at line level: `narrate.py` measures each synthesized line and cuts cues inside it (long lines split at clause boundaries, proportional to characters).
- Limits (from config): short-form 34 chars × 2 lines, long-form 48 × 2; ≤ ~20 characters per second reading speed. If a cue is too dense, shorten the English (keep meaning) or split the Hindi line.
- Style: Inter 600, cream on a translucent midnight plate with a thin gold hairline, inside the safe area (short-form bottom 420 px clear of Reels/Shorts UI).
- Deliverables: burned-in captions + sidecar `final.en.srt` (and `.vtt`).

## B. On-screen phrases (authored in `scenes.html`)
Short, memorable English that *complements* the narration — never a transcript.
- Max one phrase on screen at a time (besides subtitles); 2–7 words is ideal.
- Use them for: the hook question, the reference chip ("BHAGAVAD GITA 2.62–63"), the key idea ("Anger isn't the first link"), the chain/steps of a teaching, the closing line.
- Placement: upper-middle third (short-form: the compact badge occupies only the top ~200 px for 1.8 s, so the hook headline can sit at ~300 px from frame 0); never inside the subtitle band.
- Typography: Cormorant Garamond for display lines (italic gold `<em>` for the key word), Inter caps with tracking for kickers/labels, Cinzel only for the logotype.

## C. Sanskrit verses
Show Sanskrit only when the exact wording matters and the text is verified in `sources.json`. Render it inside an element with class `sv-sanskrit` (the only place Devanagari is allowed on screen) **and** show IAST transliteration (`sv-translit`) or English meaning beside it. Default to transliteration + meaning without Devanagari. Never display unverified Sanskrit.

## D. Guards
`build_composition.py` refuses Devanagari in captions or scene text outside `.sv-sanskrit`; `qa_check.py` re-checks the rendered HTML and the `.srt`.
