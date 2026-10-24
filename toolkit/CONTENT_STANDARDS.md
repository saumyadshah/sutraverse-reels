# SutraVerse content standards v2 (Reels, carousels, Stories)

Read this before writing any SutraVerse script, carousel or plan. It works together with CAPTION_STRATEGY.md (captions, keywords, hashtags). Where an older instruction in a task prompt or the skill conflicts with this file, this file wins.

**v2, 24 Oct 2026.** Saumya rejected the Rigveda 10.191 Reel ("The Rigveda's Last Hymn") as rushed and unclear. Its faults, which v2 exists to prevent: about 19 separate ideas in 57 s (a new idea every ~3 s); a trivia detour (Agni is the first and last word) that pulled focus from the message; up to three text layers on screen at once (headline + verse card + boxed subtitles); the "assembly that won't agree" was announced but never dramatised; the verse card was not on screen long enough to read; flat cut-out characters. **Fewer ideas, more time per idea, a real story, one clear message.**

Data behind the hook rule (weekly growth review, 18–24 Oct 2026): the top 3 Reels (Ravana 4,346 plays, Dhruva 1,322, Prahlada 1,092) opened on a scripture character in conflict; the 4 that opened on a modern scene or an abstract "you" line averaged 179 plays and lost 76–88% of viewers in the first 3 s.

## 0. Publishing strategy: fewer, better
- **9 Reels a week:** 1 each weekday (Mon–Fri, 10:00) and 2 on Saturday and Sunday (10:00 and 18:00). Never make a Reel just to fill a slot: if a Reel can't meet the quality bar (§10), it waits for review rather than posting.
- Every Reel has ONE written purpose before scripting: the one sentence the viewer should be able to repeat afterwards, plus one goal (share, save, or comment).
- Rotate formats (§3) so no two Reels in a row use the same one.

## 1. Pre-production gate (before any rendering)
Write `renders/beat_sheet.md` and check it before building scenes:
1. **The one message** in one plain sentence ("Agreement isn't thinking alike; it's understanding each other").
2. **The story** in 3 sentences: who wants what, what stands in the way, what they choose.
3. **Beat table**: for every beat, its start and end time, the narration (Hinglish) with word count, what is on screen, and the single text element (if any).
4. **Cut list**: every idea considered and dropped. If a fact doesn't serve the one message, cut it, however interesting (no trivia detours).
5. **Comprehension check**: reading only the beat table, could a first-time viewer with no background say the message back? If not, simplify.

## 2. Pacing and timing (hard limits)
- **Length 60–85 s** (YouTube Shorts and Instagram both allow this). Never compress a story to fit 60 s; cut ideas instead.
- **At most 5 ideas per Reel**: hook, story turn, the verse, its meaning, the takeaway. One idea per beat.
- **Narration speed: at most 2.2 words per second** averaged over the Reel (about 130–175 Hinglish words for 60–80 s), and never above 2.6 words/s in any single beat. Count words in the beat sheet before recording.
- **Pauses are part of the script**: 0.6–1.0 s of silence after the hook, after the turn, before the verse, and after the takeaway. Write them as "…" and keep them in the edit.
- **Scene length**: no scene shorter than 4 s; average 6–8 s. Inside a scene, keep the camera moving slowly (push-in or drift of 3–8% over the scene). No cut every 2.5–4 s.
- **The verse beat gets at least 15 s in total**: recitation at a slow, reverent pace (the card on screen the whole time), then 1.5 s of quiet, then the plain translation, then the 1–2 key words. The card stays up until the explanation has finished.
- **The takeaway is held for at least 3 s** with nothing else on screen except the subtitle.
- **Sync**: every cut, camera move and text change lands on a narration phrase boundary (use the word timings from the TTS/Whisper pass). What the voice is saying is what the picture shows, at that moment.
- Gemini TTS: direct the voice as "unhurried, warm storyteller; lets each line land". If the take is faster than 2.2 words/s, shorten the script or retake; never speed up the audio.

## 3. Story and formats
Every Reel tells a story with a person in it: someone wants something, something stands in the way, they choose, and the verse is the answer to that choice. For hymns and teachings without a narrative (Vedas, Upanishad dialogues, Niti), build the story from the text's own setting (the rishi, the assembly, the student and teacher) or from a clearly labelled illustrative scene ("Imagine a family argument at dinner…"); never present an illustration as scripture.

Default spine (60–85 s):
1. **Hook (0–3 s):** named character + conflict + stake, shown in motion. Hold a beat of silence after it.
2. **Mirror (3–10 s):** one line linking it to the viewer's life. Say the search phrase here if it wasn't in the hook.
3. **The story (10–35 s):** 2 escalating beats, each a full scene with a character speaking one short line. Show the conflict happening; don't just announce it.
4. **The turn (35–42 s):** the decision or the surprising detail, with a pause after it.
5. **The verse (42–60 s):** recited, translated, 1–2 key words glossed, and its context (who says it, to whom, when) in one sentence (§4).
6. **Takeaway + close (60–80 s):** ONE concrete thing to try today, then one comment question, then a last line that echoes the hook. One ending only: no stacked CTAs.

Formats to rotate (one per Reel; never the same twice in a row):
- **Story drama:** the default spine above.
- **Verse explained slowly:** one famous line taken apart word by word, with what it does NOT mean ("Everyone quotes it. Almost no one knows the second half.").
- **Myth vs text:** a popular belief, then what the scripture actually says, with the reference.
- **Dilemma:** two choices, the character's choice, "What would you do?" (comments).
- **Numbered list:** "3 things Vidura said…" (saves); at most 3 items in a Reel.
- **Then and now:** the same human problem in two eras, one verse.
- **Character speaks:** one character's monologue in the first person, at a turning point.

## 4. Shloka standard (every verse shown)
Each shloka appears with Devanagari + IAST + a faithful English translation + the exact reference (text, book/chapter.verse, and the edition if numbering varies). Never show a verse without helping the viewer understand it.
- **Reel:** the card shows Devanagari, IAST, translation and reference, at most 2 lines of Sanskrit (split a long verse across two cards or show the key half). The narration covers, in plain words and in this order, each with room to breathe: (a) the recitation, slowly; (b) what it literally says, with 1–2 key words glossed ("sam = together"); (c) its context: who says it, to whom, when; (d) one practical use today. Put the fuller explanation in the caption or the pinned comment.
- **Carousel:** a dedicated explanation spread: slide A = shloka + translation; B = word by word for the 3–5 key words; C = context (speaker, situation, what happens next); D = deeper meaning in plain English; E = how to use it this week.
- **Accuracy:** verify against at least two reputable editions (e.g. Gita Press; the BORI critical edition for the Mahabharata; the Valmiki Ramayana critical edition; vedabase or holy-bhagavad-gita.org for the Gita; Sanskrit Wikisource or sanskritdocuments.org for the Vedas). If editions number differently, say so in a small note.
- **Labels:** "The text says…" (scripture), "Tradition holds…" (commentary or folk belief), "For us today…" (application). Never present folk versions, TV-serial scenes or later works as the original text (e.g. the "janami dharmam" line is from the later Pandava Gita, not the Mahabharata critical edition).
- No unsupported claims (no "science proves", no invented dates, no miracle promises). Depict deities respectfully; no gore.

## 5. Story research (planner + Reel runs)
- Prefer lesser-known incidents, sharp decisions and moral dilemmas over the most famous summaries: e.g. Hanuman forgetting his power (Kishkindha 65–66), Manthara's whisper (Ayodhya 7–9), Satyakama's honesty (Chandogya 4.4), Ashtavakra in Janaka's court (Vana Parva 132–134), Gajendra's long fight (Bhagavata 8.2–3), Savitri's argument with Yama (Vana Parva 277–283), the Yaksha's questions, Shvetaketu and the banyan seed (Chandogya 6.12), Da-Da-Da (Brihadaranyaka 5.2).
- Every story: name the exact section; note one surprising detail viewers won't know, and use it only if it serves the one message; note what is text vs tradition.
- Festival tie-ins on the day or the day before (Dussehra was our best Reel).
- Rotate sources across the week; never repeat a topic already used (check the board).

## 6. Typography v2
Fonts (all free, OFL). Max 2 families per frame, plus Sanskrit when a verse is shown.
| Role | Font | Size at 1080x1920 | Where the file is |
| --- | --- | --- | --- |
| Logo | Cinzel 700, tracked +0.3em | 26 px | brand-kit/fonts |
| Titles, cover, chapter cards | **Marcellus** 400 | 72–96 px, 1–2 lines, 2–6 words | toolkit/fonts |
| Subtitles, labels, body | **Mukta** 600 (700 for the highlighted word) | 52–58 px subtitles; 26–30 px labels, tracked +0.2em, uppercase | toolkit/fonts |
| IAST transliteration | Cormorant Garamond 500 italic | 38–42 px | brand-kit/fonts |
| Sanskrit | Tiro Devanagari Sanskrit | 54–62 px | brand-kit/fonts |
Copy the woff2 files from $HOME/sutraverse-reels/toolkit/fonts/ (Marcellus, Mukta) and the skill's brand-kit/fonts (the rest) into the composition and load them with @font-face. Inter and Cormorant Garamond roman are no longer used on screen.
Rules:
- **Subtitles**: no boxes or pills. Ivory #FFF6E6 text with a soft ink shadow, centred, max 2 lines and about 30 characters a line, at the lower third (bottom edge about 300 px up, clear of Instagram's UI). Highlight at most ONE word per line, in sun #FFD36B; never highlight with a filled box.
- **At most 2 text elements on screen at once** (e.g. subtitle + one label, or the verse card + its subtitle). Never headline + card + subtitle together.
- Each piece of text stays up long enough to read twice: at least 1.2 s plus 0.25 s per word.
- Verse card: ivory card with a thin marigold inner border, Sanskrit, then IAST, a saffron hairline, the translation in Mukta 500, then the reference in Mukta 600 uppercase saffron. A sample frame is in toolkit/samples/type-v2.png.

## 7. Visual direction
- **Look:** premium illustrated storybook (2.5D), one consistent world per Reel, with cinematic compositions: a clear focal point, foreground framing, depth (4–6 layers), and light that tells the mood. Hand-authored SVG/HyperFrames only (free); optional Three.js environments for scale shots. No paid image/video generation.
- **Fewer, richer scenes:** 8–12 scenes per Reel, each a full environment, instead of 20 quick cards. Each scene earns its place by moving the story forward.
- **Characters:** shaded, not flat (form shadows, rim light, cloth folds); consistent design across scenes; they act: blink, breathe, gesture, lip-move when speaking, and react to each other. Faces show emotion clearly.
- **No generic UI or icon visuals** (phone mockups, emoji faces, floating avatars, infographic dots) unless the story is literally about that object. Show people, places and objects from the story.
- **Colour grading:** one palette per Reel moving through the story (e.g. tense dusk → firelit night → calm dawn for the resolution), inside the brand family: royal #2340B8 / royal-deep #0E1A5A fields, saffron #FF7A1A energy, marigold #FFB22E / sun #FFD36B light, ivory #FFF6E6 text, ink #1A1240, ember #FF4D2E only for conflict beats, rose #FF5C8A sparingly.
- **Motion:** slow, eased camera moves (no linear motion); parallax between layers; particles, smoke and light sparingly. No random spinning, excessive glow, stacked effects or stock-template transitions.
- **Transitions:** motivated and gentle: match-cuts, a push through a doorway, light flaring into the next scene, a slow dissolve on a pause. No wipes or zoom-blurs.
- **Music:** royalty-free only: the toolkit's pixabay_music search (record the licence), else music_bed.py tanpura drone. Calm, sustained, never busier than the voice; ducked 14–18 dB under narration; drop to near silence for the verse recitation; swell gently at the turn and resolve at the takeaway.

## 8. Cover (Reels) and slide 1 (carousels)
Consistent series look: Marcellus title (2–5 words, topic words included, honest curiosity) in the upper-middle, inside the centre 1080x1350 so it survives the grid crop; a character close-up with a clear emotion; the small SutraVerse mark. Frame 0 is the cover, with nothing covering the title.

## 9. Carousels and Stories
Carousels (goal: saves and shares), only formats with clear value:
- "Shloka explained" (§4): cover → verse → word by word → context → deeper meaning → use it today → CTA.
- Numbered list from a text: "Vidura's 6 habits that shorten life", "Patanjali's 5 rules before any pose".
- Story in 6 frames: setup → conflict → decision → verse → lesson → CTA.
Rules: one idea per slide; each slide gives a reason to swipe; same grid, type scale (§6) and palette on every slide; body max about 25 words; last slide = save/share CTA.

Stories (manual-assist): Instagram's publishing APIs can't add interactive stickers (polls, quizzes, questions), so Stories are planned automatically and finished by Saumya in the app when she wants: (1) a teaser of the Reel's hook frame; (2) a poll or quiz about the story ("Would you have forgiven Kaikeyi? Yes / No"); (3) a share of the Reel after it posts. Plan them with the story-sequencer skill; never post Stories automatically.

## 10. Quality bar before publishing
All must be true, or the Reel goes to "needs_review" instead of posting:
- the beat sheet exists, has one message, and passes the comprehension check;
- length 60–85 s; narration ≤ 2.2 words/s overall and ≤ 2.6 in any beat (from the Whisper word timings); the four pauses are present;
- no scene under 4 s; the verse beat ≥ 15 s with the card up throughout; the takeaway held ≥ 3 s;
- never more than 2 text elements on screen; subtitles follow §6;
- hook = named character + conflict in the first 3 s; one concrete takeaway; one ending;
- every verse verified on two editions; text vs tradition vs application labelled; nothing claimed that the text doesn't say;
- narration natural (Whisper check); music royalty-free with its licence recorded;
- QA has no FAIL; the cover is readable at grid size; the caption follows CAPTION_STRATEGY.md.
- Final self-review: watch the whole render once at normal speed, as a first-time viewer, and write down anything that felt rushed, unclear or disconnected. Fix it before publishing.

## 11. Learning loop
The weekly growth review compares each Reel's 3-second hold, average watch time and watch percentage, completion, shares and saves per 1,000 reached, comments and follows, against the format, hook type, length and words-per-second recorded on its slot. Repeat what beats the median; change one variable at a time.

## 12. YouTube agent pack (yt-* skills)
Vendored in toolkit/.claude/skills/yt-* (MIT; see YT-AGENT-PACK.md) and installed to ~/.claude/skills by env_setup.sh, with the voice profile at ~/.claude/youtube/voice.md. Run the scripts from the repo so they work in any workspace: `python3 $HOME/sutraverse-reels/toolkit/.claude/skills/<skill>/<script>.py` (read the skill's SKILL.md from the same folder). These standards win where the pack disagrees (e.g. its "3 uploads a week" and "presenter on camera" assumptions don't apply to us). Use them like this:
- **yt-script / hookscore.py (Reel runs):** score the 3 story-first hooks with hookscore.py as a SECOND opinion next to the virality checklist. It is tuned for English talking-head hooks and rated our Dhruva-style wound-first opener "WEAK" although it earned 5.8x our median, so never drop a story-first hook on its score alone; use its "weakest" line to sharpen wording.
- **yt-package / title.py (Reel runs + publisher):** write 5 YouTube Short titles, lint them with title.py together with the cover's 2–5 words (`--thumb`), keep the best (no truncation at 60, cover words not repeating the title), and store it on the slot as "yt_title". The publisher uses "yt_title" for the Short.
- **yt-seo (Reel runs + publisher):** for the Short's description apply its "query test": name the 3 searches the Short should win and make sure the title and first two description lines contain those words. Tags only for spellings and names (≤ 15).
- **yt-viral / swipe.py (weekly plan, when YouTube is reachable):** collect ≥ 4 recent videos per channel for 3–5 similar scripture/mythology channels (public listings only, via web fetch or the vidIQ tools; never a logged-in session), rank with swipe.py, and use the top multiples as topic or format ideas. Skip quietly if listings can't be fetched.
- **yt-retention / retention.py (weekly review):** if Saumya has dropped a YouTube Studio retention export into the repo under analytics/retention/*.csv, run it and report the hook leak and biggest cliff for that Short.
- **yt-audit (weekly review, first Saturday of each month):** run it on the YouTube channel and report its ONE fix.
- **yt-comment:** only when comments are pasted in or a tool can read them; replies are drafts for Saumya, never posted automatically.
- **yt-plan, yt-shorts, yt-edit, yt-chapters:** available on request; they target long videos and on-camera creators, so the scheduled tasks don't use them.
- **Captions + playlists (Reel runs + publisher):** every Reel run copies renders/final.en.srt to reels/<slot id>-<topic>.en.srt in the commit, and stores "caption_url" (its raw GitHub URL) and "yt_playlist" on the slot. Playlist by source: Bhagavad Gita → "Bhagavad Gita Explained"; Ramayana → "Ramayana Stories"; Mahabharata → "Mahabharata Lessons"; Vedas or Upanishads → "Vedas & Upanishads"; Puranas / Bhagavatam / Devi Mahatmya → "Puranas & Bhagavatam"; Niti, Yoga Sutras or other single-verse explainers → "Shlokas Explained"; a festival Reel → "Festival Stories". The publisher passes `--playlist "<yt_playlist>" --captions <caption_url>` to yt_upload.py.
- Every yt-* skill ends with "ship it, or change it?". In unattended runs, treat that as a self-check, not a question to wait on; nothing in the pack publishes.

## 13. Skill pipeline (mandatory, Saumya 24 Oct)
Every plan, Reel, title, cover/thumbnail, caption, carousel and review uses ALL the skills listed for its stage. Load each with the Skill tool (account skills, e.g. `going-viral`), or read its SKILL.md from $HOME/sutraverse-reels/toolkit/.claude/skills/<name>/ when it isn't listed. Apply each one briefly (a few lines of output each, not a full essay) to save Claude usage. These standards and CAPTION_STRATEGY.md win when a skill disagrees. Record the skills actually used as "skills_used" on the slot (or in the review's insights) and in the log line; if a skill can't be loaded, say which and why.

| Stage | Skills (all of them, every time) |
| --- | --- |
| Weekly plan | trend-spotter, yt-viral (skip only if YouTube listings can't be fetched), series-planner, content-calendar, going-viral, viral-hook-writer, yt-plan (as a capacity/structure check; our 9-Reel cadence wins), story-sequencer, hashtag-keyword-research; content-pillar-builder on the first Saturday of the month |
| Reel: idea, hook, script | sutraverse, virality, going-viral, viral-hook-writer, ab-hook-tester (two genuinely different hooks; keep the runner-up on the slot as "alt_hook"), yt-script (hookscore.py as a second opinion only, §12), reel-scripter, reel-builder, youtube-scriptwriting (the retention-beat checks), on-screen-text-writer, cta-writer |
| Title, cover, thumbnail | cover-thumbnail-brief, yt-package (title.py on 5 titles with the cover words), youtube-thumbnail (use its high-CTR principles for frame 0 ONLY; never its image-generation step, which needs paid Gemini image models), youtube-seo, yt-seo (the query test) |
| Caption, keywords, first comment | CAPTION_STRATEGY.md, hashtag-keyword-research, caption-and-hashtags (structure check only), cta-writer |
| YouTube Short version | cross-platform-reformatter (title/description adaptation; the video stays the same), yt-package, yt-seo |
| Carousel | carousel-builder, viral-carousel, cover-thumbnail-brief, on-screen-text-writer, cta-writer, hashtag-keyword-research |
| Stories (plan only) | story-sequencer |
| Weekly review | analytics-readout, content-audit, social-analytics-report, best-time-scheduler, hashtag-keyword-research, trend-spotter, competitor-teardown (if credits allow), reel-analyzer or content-research on the week's best outlier in our niche, comment-mining (if comments are readable), yt-retention (if a CSV exists), yt-audit (first Saturday of the month) |

Not used, on purpose: comment-responder (Saumya declined auto-replies), content-factory (duplicates this pipeline), outreach/collab/influencer/UGC/paid/UTM/LinkedIn/X skills and office-file skills (no role in an organic Instagram + Shorts channel), yt-edit/yt-chapters/yt-shorts (long-form only; available on request).
