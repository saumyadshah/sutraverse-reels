# SutraVerse content standards (Reels, carousels, Stories)

Read this before writing any SutraVerse script, carousel or plan. It works together with CAPTION_STRATEGY.md (captions, keywords, hashtags). Where an older instruction in a task prompt or the skill conflicts with this file, this file wins.

Built from our own results (weekly growth review, 18–24 Oct 2026): the top 3 Reels (Ravana 4,346 plays, Dhruva 1,322, Prahlada 1,092) all opened on a scripture character in conflict; the 4 Reels that opened on a modern scene or an abstract line ("your stress, your scrolling") averaged 179 plays and lost 76–88% of viewers in the first 3 seconds. Carousels reached 3–144 accounts with 0 saves.

## 1. Hooks (first 1.5 s) — DATA RULE
- Open on the STORY, not on the viewer: a named character, a conflict, a stake. Examples that work for us:
  - Wound-first: "Told 'you don't deserve this' at age five…" (Dhruva, 5.8x median)
  - Number reveal tied to a moment: "4 warnings Ravana ignored" (Dussehra, 19x median)
  - Child vs power: "A boy refused to fear the king who wanted him dead." (Prahlada)
  - Character contradiction: "The strongest one in the Ramayana thought he was weak." (Hanuman remake)
- The modern-life mirror comes at BEAT 2 (3–8 s), never as the opener: "Aur sach kahun? Hum sab ke saath yahi hota hai…"
- Avoid: abstract "you" openers, vague superlatives ("the strongest one in the room") with no conflict, logo or title-card openings, slow pans with no action.
- Frame 0 is the designed cover (see 6); the hook's motion starts on frame 1.

## 2. Story structure (45–58 s)
Default spine (story-first):
1. Hook (0–2 s): character + conflict + stake.
2. Mirror (2–8 s): one line connecting it to the viewer's life. Say the search phrase here if not already said.
3. Rising tension (8–25 s): 2–3 escalating beats, each a new visual; a character speaks 1 short line.
4. Turn / twist (25–32 s): the surprising decision, detail or reversal — the lesser-known part people don't expect.
5. The verse (32–45 s): the shloka as the "answer", explained (see 3).
6. Takeaway + CTA (45–55 s): ONE concrete action for today, then a comment question tied to their life; last line echoes the hook (loop).
Other structures to rotate (one per Reel, vary through the week):
- "Everyone knows X. Almost no one knows Y." (lesser-known incident).
- Dilemma / debate: two choices, the character's choice, "What would you do?" (comments).
- Numbered reveal: "3 things Vidura said…" (saves).
- Then vs now: same problem, two eras, one verse.

## 3. Shloka standard (every verse shown)
Each shloka appears with: Devanagari + IAST + exact reference (text, book/chapter.verse, edition if numbering varies), and the explanation below. Never show a verse without helping the viewer understand it.
- Reel (time-limited): on-screen card = Devanagari, IAST, faithful English translation, reference. Narration covers in plain words: (a) what it literally says, with the 1–2 key words glossed ("karma = action, phala = result"); (b) what it means in its context (who says it, to whom, when); (c) one practical use today. Put the fuller explanation in the caption's first lines or the pinned comment.
- Carousel: a dedicated explanation spread: slide A = shloka + translation; slide B = word-by-word for the 3–5 key words; slide C = context (speaker, situation, what happens next); slide D = deeper meaning (the philosophical point, in plain English); slide E = how to use it this week.
- Accuracy: verify against at least two reputable editions (e.g. Gita Press, BORI critical edition for the Mahabharata, Valmiki Ramayana critical edition, vedabase/holy-bhagavad-gita.org for the Gita, sanskritdocuments.org). If editions number differently, say so in a small note.
- Label clearly: "The text says…" (scripture), "Tradition holds…" (commentary/folk belief), "For us today…" (application). Never present folk versions, TV-serial scenes or later works as the original text (e.g. the "janami dharmam" line is from the later Pandava Gita, not the Mahabharata critical edition).
- No unsupported claims (no "science proves", no invented dates, no miracle promises). Depict deities respectfully; no gore.

## 4. Story research (planner + Reel runs)
- Prefer lesser-known incidents, sharp decisions and moral dilemmas over the most famous summaries: e.g. Hanuman forgetting his power (Kishkindha 65–66), Manthara's whisper (Ayodhya 7–9), Satyakama's honesty (Chandogya 4.4), Ashtavakra in Janaka's court (Vana Parva 132–134), Gajendra's long fight (Bhagavata 8.2–3), Savitri's argument with Yama (Vana Parva 277–283), the Yaksha's questions, Shvetaketu and the banyan seed (Chandogya 6.12), Da-Da-Da (Brihadaranyaka 5.2).
- Every story: name the exact section; note one surprising detail viewers won't know; note what is text vs tradition.
- Festival tie-ins on the day or the day before (Dussehra was our best Reel).
- Rotate sources across the week; never repeat a topic already used (check the board).

## 5. Visual direction
- Look: premium illustrated storybook (2.5D), one consistent world. Hand-authored SVG/HyperFrames only (free); optional Three.js environments for scale shots. No paid image/video generation.
- Palette (brand-identity.md, "Bright v2"): royal #2340B8 / royal-deep #0E1A5A fields, saffron #FF7A1A energy, marigold #FFB22E / sun #FFD36B light, ivory #FFF6E6 text, ink #1A1240 text on bright, rose #FF5C8A sparingly, ember #FF4D2E only for conflict beats. Per-scene mood grades stay inside this family.
- Type (vendored, OFL): Cinzel 700 = logotype only; Cormorant Garamond 500/600 (+ italic) = display titles and IAST; Inter 600/700 = subtitles, labels, carousel body; Tiro Devanagari Sanskrit = verified Sanskrit only. Max 2 families per frame. Titles 3–7 words.
- Motion: every scene moves (multi-plane parallax, light, particles, cloth/hair); camera move or cut every 2.5–4 s on phrase timings; eased (no linear) motion; characters blink, breathe, gesture and lip-move when speaking. Avoid: random spinning, excessive glow, stock-template transitions, more than one effect per beat.
- Transitions: match-cuts and motivated moves (push through a doorway, light flare to a new scene, dissolve on a sound). No generic wipes/zoom-blurs.
- Music: royalty-free only. Order: the toolkit's pixabay_music search (record the licence) → music_bed.py tanpura drone. Never paid music generation. Music sits under the voice (ducked), rises at the turn, resolves at the verse.
- Voice: Gemini TTS, one continuous natural Hinglish take (see task prompt).

## 6. Cover (Reels) and slide 1 (carousels)
Consistent series look: same title placement (upper-middle, inside the centre 1080x1350), Cormorant Garamond 600 title with ink outline, character close-up with strong emotion, small SutraVerse mark. 2–5 words, topic words included, honest curiosity. Frame 0 shows the cover without the opening badge on top of the title.

## 7. Carousels
Goal: saves and shares. Only formats with clear value:
- "Shloka explained" (see 3): cover → verse → word-by-word → context → deeper meaning → use it today → CTA.
- Numbered list from a text: "Vidura's 6 habits that shorten life", "Patanjali's 5 rules before any pose".
- Story in 6 frames: setup → conflict → decision → verse → lesson → CTA.
Rules: one idea per slide; each slide ends with a reason to swipe ("The 3rd one surprised me →"); consistent grid (same margins, type scale, palette); body max ~25 words; last slide = save/share CTA. Prefer festival or list topics (our two non-festival carousels reached 3 and 5 accounts).

## 8. Stories (manual-assist)
Instagram's publishing API (vidIQ, Metricool) cannot add interactive stickers (polls, quizzes, questions), so Stories are prepared automatically but finished by Saumya in the app when she wants them:
- Daily pattern (optional, 3 frames): (1) a teaser of today's Reel's hook frame + "New Reel at 6 pm"; (2) a poll/quiz about the story ("Would you have forgiven Kaikeyi? Yes / No"); (3) share the Reel to Story after it posts.
- Use the story-sequencer skill to plan; never post Stories automatically through Metricool without stickers unless Saumya asks (they count toward Metricool's ~20 posts/month).

## 9. Quality bar before publishing
QA no FAIL; every verse verified; narration natural (Whisper check); hook = character + conflict in first 1.5 s; one concrete takeaway; cover readable at grid size; captions follow CAPTION_STRATEGY.md; nothing claimed that the text doesn't say.
