# SutraVerse content standards v4 + v5 craft (Reels, carousels, Stories)

Read this before writing any SutraVerse script, carousel or plan. It works together with CAPTION_STRATEGY.md (captions, keywords, hashtags). Where an older instruction in a task prompt or the skill conflicts with this file, this file wins.

**v4, 30 Oct 2026: BRAND & PRODUCTION REVAMP (Saumya's brief; overrides everything below that conflicts).** New identity "Mithila Night" (brand kit in `toolkit/brand-v4/`, sample frames in `toolkit/brand-v4/samples/`), shorter and tighter Reels, a style chosen by subject, recurring named series, and explainers. v3's real-life-first direction stays.

**What the data says (owner insights, 22–29 Oct, 12 Reels):** the two v3 real-life Reels averaged 32.9% skip and 24.9 s average watch, against 46–51% skip and 13–18 s for the scripture-first Reels. Karwa Chauth (family, Aman fasting) reached 3,173 plays and 14.5 shares per 1,000 plays, our best. The interview Reel (a specific modern moment) had the best share rate of all (18.3 per 1,000). But every Reel loses most viewers around 20–27 s, whatever its length (average watched 14–34%), and that is where our scripture "turn" and long verse card used to begin. So: **keep the real-life hooks; bring the scripture parallel in by second 8–12 and intercut it with the modern story; keep the modern stake unresolved until the last 5 seconds; shorten to 35–55 s.**

**v4 rules (summary; details in §2, §3, §6–8, §15–16):**
- **Length 35–55 s** (explainers up to 60 s). One message, at most 4 ideas.
- **Rhythm:** shots 2–5 s, with a meaningful visual change at least every 2–3 s (cut, camera move, a character's reaction, text reveal, thread draw), but narration stays ≤ 2.4 words/s, so it never feels rushed. The verse card is on screen ≥ 7 s (recite the key half-line, show the translation), not 15–24 s; the full verse goes in the caption and the comment-to-DM.
- **Structure ("braided" spine):** 0–3 s modern hook with a stake → 3–8 s escalation + open loop → 8–12 s the first cut to the ancient parallel (via the thread or portal transition) → 12–35 s intercut: modern beat / ancient beat answering it → 35–45 s the verse (≥ 7 s) → 45–55 s back to the modern character acting on it (the loop closes) + comment question. Each modern beat ends on a question the next ancient beat answers.
- **Visual mode chosen by subject** (§7): Night Cinema (modern scenes), Mithila Panel (ancient scenes), Paper Diorama 3D (Blender, for hero/portal shots), Chandan Explainer (diagrams). Never one template for everything.
- **Series** (one per Reel, shown as the chip at the top): Office ka Mahabharat (work, haldi), Ghar ki Ramayan (family, palash), Dosti & Dharma (friends & relationships, mor), Log Kya Kahenge (social pressure, kumkum), SutraVerse Explains (explainers, chandan). Recurring series build return viewers and profile follows.
- **Explainers** ("SutraVerse Explains"): at least 2 of the 9 weekly Reels. A real phenomenon ("why your manager listens to the loudest person", "why family WhatsApp fights escalate") explained with an animated thread diagram + one scripture parallel + one takeaway.
- **Sound (v5, Saumya 30 Oct: "change the background sound and music"):** a clear voice first (-14 LUFS master, ≤ -1 dBTP; speech ≥ 12 dB, aim 15 dB, above the bed in pauses). The background is designed per Reel with `scripts/sound_design.py`, never one drone under everything:
  - **Music follows the story:** soft modern "warm keys" (chords + a muted pluck pulse) under modern scenes, minor/tense before the verse, major/warm after it; tanpura + bansuri-style flute under ancient scenes in the same key; a riser and a gentle swell into the turn; near-silence under the shloka; a held chord that resolves under the end card.
  - **Ambience per scene:** room, dinner, office, street, night, fire, air, temple, river or rain, chosen in the shot list for every scene, about 25 dB under the voice.
  - **Story SFX, 2–5 per Reel:** an automatic whoosh at every modern↔ancient change, plus a few cues on story moments (a spoon clink, a phone notification, a door, a temple bell, paper for a manuscript). Never on every cut.
  - **Sources:** original synthesis by default (royalty-free, no licence needed). A royalty-free track Saumya drops in the repo's `music_library/<mood>/` (tense, warm, calm), each with a `.json` licence sidecar (title, artist, source_url, licence), may replace the score. Never paid music generation; never a track without its licence recorded. Record `artifacts/sound_plan.json` on the slot's log line.

**v2, 24 Oct 2026.** Saumya rejected the Rigveda 10.191 Reel ("The Rigveda's Last Hymn") as rushed and unclear. Its faults, which v2 exists to prevent: about 19 separate ideas in 57 s (a new idea every ~3 s); a trivia detour (Agni is the first and last word) that pulled focus from the message; up to three text layers on screen at once (headline + verse card + boxed subtitles); the "assembly that won't agree" was announced but never dramatised; the verse card was not on screen long enough to read; flat cut-out characters. **Fewer ideas, more time per idea, a real story, one clear message.**

**v3, 28 Oct 2026: REAL-LIFE FIRST (Saumya's direction, overrides anything below that conflicts).** Every Reel now starts from a real-life situation people genuinely live through, and SutraVerse's scripture lens is the twist and the answer, not the starting point. The viewer must think "this happens in my life too!" in the first 3 seconds, then "I never thought of it that way" at the verse. Topic territory (rotate across the week; never two from the same territory in a row):
- **Corporate life & office politics:** the colleague who takes credit, the boss who praises you in private and blames you in public, the appraisal that went to the loudest person, the 9 p.m. "quick call", the team-lunch you weren't invited to, quitting vs staying, the friend who became your manager.
- **Workplace struggles:** burnout, comparison with a batchmate's salary, imposter feeling in a new job, layoffs, the side-hustle guilt.
- **Family dynamics:** "log kya kahenge", parents comparing you with cousins, the sibling who gets away with everything, marriage pressure at 27, the joint-family kitchen politics, the parent who never says "proud of you".
- **Relationships & friendships:** the friend who only calls when they need something, the group chat that went quiet, ghosting, jealousy when a friend succeeds, the partner who never apologises, the ex who comes back.
- **Social expectations & everyday problems:** the wedding-season questions, Instagram comparison, saying no to relatives, money borrowed and never returned, the neighbour, the auto-wala, the landlord.
- **Real incidents:** a specific, believable moment (a WhatsApp message, a meeting, a dinner-table line) rather than a vague feeling. Never use a real private person; composites only.

**How the scripture fits (brand promise kept):** the modern scene is the story; at the turn, a scripture character who faced the SAME problem appears (e.g. credit-stealing colleague → Karna denied credit at the tournament; family comparison → Dhruva and his stepmother; friend who only calls in need → Sudama and Krishna; boss who manipulates → Manthara and Kaikeyi), and one verified verse lands as the answer. Every verse still follows §4 exactly. The modern characters are named composites (Riya, Kabir, Neha, Arjun-from-accounts), shown as an illustrative scene, never as scripture.

**Why this is not the old "modern mirror" opener that failed:** the 4 Reels that opened on an abstract "you" line ("your stress, your scrolling", "the strongest one in the room") averaged 179 plays. What worked (Ravana 19x, Dhruva 5.8x, Prahlada 4.8x) was a NAMED person in a CONCRETE conflict with a stake. v3 keeps that rule and applies it to modern people: "Riya's manager presented her slides in the CEO meeting… and didn't say her name." is a story hook; "Ever felt unappreciated at work?" is not, and is banned.

**Quality targets (watch until the end, share, comment):** a pattern-interrupt first frame (a face mid-reaction or an object that matters, never a title card); the stake clear by second 3; an open loop by second 8 that is only closed at the verse; one "send this to…" share moment that names a specific person ("the colleague who…"); a comment question with a side to pick. Retention is the scoreboard: the weekly review reports 3-second hold, average watch % and completion per Reel, and the next week changes one variable to beat the median.

(v2 data, kept for reference) Data behind the hook rule (weekly growth review, 18–24 Oct 2026): the top 3 Reels (Ravana 4,346 plays, Dhruva 1,322, Prahlada 1,092) opened on a scripture character in conflict; the 4 that opened on a modern scene or an abstract "you" line averaged 179 plays and lost 76–88% of viewers in the first 3 s.

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

## 2. Pacing and timing (hard limits, v4)
- **Length 35–55 s** (explainers up to 60 s). Cut ideas rather than speeding up.
- **At most 4 ideas per Reel:** the modern problem, the ancient parallel, the verse, the action.
- **Narration ≤ 2.4 words per second** overall (about 85–130 Hinglish words), never above 2.8 in a beat. Pauses of 0.4–0.8 s after the hook, before the verse and after the action. Never speed up audio.
- **Shots 2–5 s; a visual change at least every 2–3 s** (camera move, cut, reaction, text reveal, thread draw). No static frame longer than 3 s.
- **Verse card ≥ 7 s** with the key half-line recited, translation shown, reference visible. The full verse goes in the caption and the comment-to-DM.
- **The action (what the modern character does) is held ≥ 2.5 s.** The comment question is the last line.
- **Sync:** every cut and text change lands on a narration phrase boundary (word timings).
- **First frame = the cover** (frame 0), and the first 1.5 s already contains motion and the stake.

## 3. Story and formats
Every Reel tells a story with a person in it: someone wants something, something stands in the way, they choose, and the verse is the answer to that choice. For hymns and teachings without a narrative (Vedas, Upanishad dialogues, Niti), build the story from the text's own setting (the rishi, the assembly, the student and teacher) or from a clearly labelled illustrative scene ("Imagine a family argument at dinner…"); never present an illustration as scripture.

Default spine v3 (superseded on timing by the v4 braided spine at the top: 35–55 s, ancient parallel by 8–12 s, intercut, modern loop closes at the end). The beat ORDER below still applies to drama formats:
1. **Hook (0–3 s):** a named modern character in a specific, recognisable moment + the stake, shown in motion (Riya's slides on the CEO's screen, her name missing). Hold a beat of silence after it. The search phrase is spoken here or by second 5.
2. **Escalation (3–15 s):** it gets worse in one more concrete beat (the manager's "great teamwork, everyone"), with one line of real dialogue. Open the loop: "Riya had two choices…"
3. **The parallel (15–35 s):** the turn to the scripture character who faced the same thing ("Karna stood in that arena, and no one would even say his name…"), 2 short scenes, the conflict shown, not announced.
4. **The verse (35–55 s):** recited, translated, 1–2 key words glossed, context in one sentence (§4), the card up throughout.
5. **Back to the modern character (55–70 s):** what she does now, ONE concrete action the viewer can copy tomorrow at work/at home.
6. **Close (70–85 s):** a comment question with a side to pick ("Speak up in the meeting or talk to the boss after? 👇") and a share line naming a person ("Send this to the colleague who…"). One ending only.

Formats to rotate (one per Reel; never the same twice in a row):
- **Office/family drama → scripture answer:** the default spine above.
- **"POV" scene:** first-person modern moment ("POV: your mom compares you with Sharma ji's son… again"), then the scripture answer.
- **Dilemma:** a real two-way choice (quit or stay; tell your friend or not), the scripture character's choice, "What would you do?" (comments).
- **Numbered list from life:** "3 types of colleagues the Mahabharata warned you about" (saves); at most 3 items, each a recognisable person with a scripture match.
- **Then and now:** the same human problem in two eras side by side (Manthara whispering to Kaikeyi / the office gossip on Slack), one verse.
- **Myth vs text:** a common saying people use in family arguments ("Karma will get them"), then what the text actually says.
- **Character speaks:** a scripture character talks directly to the modern viewer about the exact situation ("Dear Riya, from Karna").
- **SutraVerse Explains (v4):** a real-life phenomenon explained with an animated thread diagram (Chandan Explainer mode), one scripture parallel, one takeaway; ≤ 60 s; at least 2 a week.

## 4. Shloka standard (every verse shown)
Each shloka appears with Devanagari + IAST + a faithful English translation + the exact reference (text, book/chapter.verse, and the edition if numbering varies). Never show a verse without helping the viewer understand it.
- **Reel:** the card shows Devanagari, IAST, translation and reference, at most 2 lines of Sanskrit (split a long verse across two cards or show the key half). The narration covers, in plain words and in this order, each with room to breathe: (a) the recitation, slowly; (b) what it literally says, with 1–2 key words glossed ("sam = together"); (c) its context: who says it, to whom, when; (d) one practical use today. Put the fuller explanation in the caption or the pinned comment.
- **Carousel:** a dedicated explanation spread: slide A = shloka + translation; B = word by word for the 3–5 key words; C = context (speaker, situation, what happens next); D = deeper meaning in plain English; E = how to use it this week.
- **Accuracy:** verify against at least two reputable editions (e.g. Gita Press; the BORI critical edition for the Mahabharata; the Valmiki Ramayana critical edition; vedabase or holy-bhagavad-gita.org for the Gita; Sanskrit Wikisource or sanskritdocuments.org for the Vedas). If editions number differently, say so in a small note.
- **Labels:** "The text says…" (scripture), "Tradition holds…" (commentary or folk belief), "For us today…" (application). Never present folk versions, TV-serial scenes or later works as the original text (e.g. the "janami dharmam" line is from the later Pandava Gita, not the Mahabharata critical edition).
- No unsupported claims (no "science proves", no invented dates, no miracle promises). Depict deities respectfully; no gore.

## 5. Story research (planner + Reel runs)
- **Start from the real-life moment, then find the scripture match.** For each Reel write: the modern incident (who, where, the exact line someone says), why it's universal (who will tag whom), and the scripture character who lived the same problem (exact section). Use comment-mining, trend-spotter and content-research to find the situations people are actually talking about this week (comments, trending Reels in corporate-life, family-humour and relationship niches); prefer a fresh, specific angle over a generic one ("boss takes credit" → "boss takes credit in the meeting YOU prepared at 2 a.m.").
- Good scripture matches: Karna (credit and respect denied), Ekalavya (talent ignored by the system), Manthara/Kaikeyi (office or family gossip), Dhruva (comparison, stepmother's words), Sudama (the friend you hesitate to ask), Vidura (the honest employee no one listens to), Yudhishthira's dice (one bad decision under peer pressure), Draupadi (being humiliated in front of everyone), Kumbhakarna (burnout and sleep), Hanuman forgetting his strength (imposter feeling), Arjuna on the battlefield (quitting vs staying), Savitri (standing firm against family pressure), Satyakama (honesty about your background).
- Every story: name the exact section; note one surprising detail viewers won't know, and use it only if it serves the one message; note what is text vs tradition.
- Festival tie-ins on the day or the day before, told through a modern family moment (Karwa Chauth → the husband who also fasts; Diwali → the relative's salary question at the party).
- Rotate topic territories (v3 list above) and sources across the week; never repeat a modern situation or a scripture story already used (check the board).

## 6. Typography v4 ("Mithila Night")
Fonts in `toolkit/brand-v4/fonts/` (all SIL OFL, free). Tokens in `toolkit/brand-v4/brand.css`.
- **Display / hooks / covers / chips:** Anek Latin, width 75%, weight 800, UPPERCASE, tight leading (0.9). Designed by Ek Type in India; condensed, so 3–5 big words fit a phone screen.
- **Subtitles (burned in), updated 30 Oct per Saumya ("clearly visible, with a background"):** ALWAYS on a solid plate: kajal at 88% opacity (rgba(16,14,23,.88)), radius 14 px, a 3 px haldi rule along the bottom edge, soft drop shadow. Text Anek Latin 700, 46–50 px (42 px for long lines), chandan #F4EADB (contrast ≈ 15:1 on the plate), max 2 lines, about 32 characters per line, bottom of the safe area (420 px clear of the Instagram/Shorts UI). ONE word per line may light up kajal-on-haldi as it is spoken. This is built into the pipeline's brand-kit/brand.css (.sv-cap) and build_composition.py, so use the standard captions; never draw subtitles without the plate, and never lower its opacity. QA: check one frame over the brightest scene and one over the darkest.
- **The ancient voice** (translations, quotes, the scripture character's lines): Fraunces Italic (SOFT 100), 56–64 px.
- **Sanskrit:** Tiro Devanagari Sanskrit. **IAST:** Fraunces Italic (it has every diacritic). **Hindi titles / graphics:** Anek Devanagari.
- **Wordmark:** "sutraverse" in lowercase Anek 85% / 700, with the double-line haldi underline (the Mithila double outline). It sits at the bottom of the cover and the end card only.
- Max 2 text elements on screen at once (subtitle + one label/chip). On-screen text stays up ≥ 1.2 s per line.

## 7. Visual direction v4: choose the mode by subject
Palette (brand.css): kajal #100E17 (ink), neel #1A1D47 (night), chandan #F4EADB (paper/text), haldi #F2B33D (highlight, hope), sindoor #D63E2A (conflict), mor #137C77 (wisdom/verse), palash #EE7A2E (festival/energy), kumkum #9E2348 (family/love). One dominant accent per Reel, chosen by series.
- **Night Cinema (modern scenes):** cinematic 2.5D illustration in neel/kajal with motivated warm light (laptop glow, tube light, diya), rim light on characters, shallow depth of field, film grain 12–18%, vignette. Believable Indian settings (open-plan office, glass meeting room, metro, 2BHK kitchen, wedding hall, chai tapri). Characters are shaded, expressive and act (blink, breathe, glance, lip-move).
- **Mithila Panel (ancient scenes):** an original Madhubani/Mithila-inspired look, never copying a specific artwork. Every form has the double outline; fills are flat natural pigments (haldi, sindoor, mor, palash, chandan on kajal line); hatched (kachni) and dotted bands; long "fish" eyes; motifs where they fit the story (sun and moon, fish, peacock, lotus, tree of life). Motion stays gentle (sway, blink, parallax between pattern layers). Motif library: `toolkit/brand-v4/motifs.py`.
- **Paper Diorama 3D (Blender):** layered paper cut-outs with real light and soft shadows for hero shots: the world-change portal (`toolkit/brand-v4/blender/portal_sting.py`, pre-rendered frames in `toolkit/brand-v4/assets/portal/`), 3D type for big hooks, or a key ancient tableau as a lit diorama. Rendered with Blender's Cycles on CPU (bpy, free); see §16 for budgets.
- **Chandan Explainer (diagrams):** a chandan paper background, kajal lines, animated "thread" connectors that draw themselves (the sutra), circles with the double outline, at most 3 nodes on screen, and labels in Anek. The thread is the brand's visual metaphor: every idea is connected by a thread.
- **Signature transitions** (use one per world change, never stock wipes):
  1. **Thread draw:** a haldi double line draws across the frame and the next world fills in behind it (frame_transition sample).
  2. **Paper Portal:** dolly through the 3D paper rings (pre-rendered asset), crossfading at the bright core.
  3. **Outline bloom:** the modern character's outline doubles and its fill turns to Mithila pigment (a match-cut between worlds).
  Within a world, use push-ins, rack focus and match-cuts. No zoom-blurs, spins, glitch or template transitions.
- **Never:** emoji faces, stock UI mockups, floating avatars, infographic dots, real logos, real people, gore. Deities are always respectful and recognisable.

## 8. Covers & thumbnails v4 (one system, every Reel and Short)
Template: `toolkit/brand-v4/cover.py` (samples: `samples/cover_office.png`, `samples/cover_family.png`).
- 1080×1920, all key content inside the centre 1080×1350 (grid crop). Top: the **series chip** in its accent colour. Middle: the **modern character's face**, large, with one clear emotion, lit with rim light; optional small Mithila inset of the ancient parallel (the double-outline panel). Bottom on ink gradient: the **headline**, 2–5 words in Anek 75%/800 UPPERCASE, the last 1–2 words in the accent colour, phrased as the viewer's own problem ("BOSS TOOK YOUR CREDIT?"); under it one Fraunces italic line naming the parallel ("Karna knew this feeling."). Wordmark at the bottom.
- Readable at 200 px wide (check by downscaling). No clickbait: the headline must be what the Reel is about. Never more than 7 words in total on the cover.
- YouTube Shorts use the same frame (frame 0); the title (§12) carries the search words.

## 9. Carousels and Stories

**v4 (30 Oct):** carousels render in Mithila Night automatically: make_post.py draws the night base with the Mithila double outline, Anek display, Fraunces italic, the chandan verse card and the double-rule wordmark. Put "series": "office|family|friends|social|explains" at the top of the spec for the series chip and accent. Save the spec as posts/<slot id>/spec.json next to the slides so a post can be re-rendered later. Lead with a real-life moment where the format allows (cover sub-line or slide 2).
Carousels (goal: saves and shares), only formats with clear value:
- "Shloka explained" (§4): cover → verse → word by word → context → deeper meaning → use it today → CTA.
- Numbered list from a text: "Vidura's 6 habits that shorten life", "Patanjali's 5 rules before any pose".
- Story in 6 frames: setup → conflict → decision → verse → lesson → CTA.
Rules: one idea per slide; each slide gives a reason to swipe; same grid, type scale (§6) and palette on every slide; body max about 25 words; last slide = save/share CTA.

Stories (manual-assist): Instagram's publishing APIs can't add interactive stickers (polls, quizzes, questions), so Stories are planned automatically and finished by Saumya in the app when she wants: (1) a teaser of the Reel's hook frame; (2) a poll or quiz about the story ("Would you have forgiven Kaikeyi? Yes / No"); (3) a share of the Reel after it posts. Plan them with the story-sequencer skill; never post Stories automatically.

## 10. Quality bar before publishing
All must be true, or the Reel goes to "needs_review" instead of posting:
- the beat sheet exists, has one message, and passes the comprehension check;
- length 35–55 s (explainers ≤ 60 s); narration ≤ 2.4 words/s overall and ≤ 2.8 in any beat (Whisper word timings); a visual change at least every 3 s; the ancient parallel appears by 12 s;
- the verse card ≥ 7 s; the modern loop closes in the last 10 s; the action held ≥ 2.5 s; audio -14 LUFS with clear voice;
- never more than 2 text elements on screen; typography, palette, series chip, transitions and cover follow v4 (§6–8);
- hook = a named (modern or scripture) character in a specific conflict with a stake in the first 3 s, no abstract "you" question; an open loop closed at the verse; one concrete takeaway; a share line naming a person; one ending;
- every verse verified on two editions; text vs tradition vs application labelled; nothing claimed that the text doesn't say;
- narration natural (Whisper check); music royalty-free with its licence recorded; sound designed per scene (sound_design.py: music changes between modern and ancient worlds, an ambience per scene, 2–5 story SFX, near-silence under the shloka);
- QA has no FAIL; the cover is readable at grid size; the caption follows CAPTION_STRATEGY.md.
- Final self-review: watch the whole render once at normal speed, as a first-time viewer, and write down anything that felt rushed, unclear or disconnected. Fix it before publishing.
- v5 (§17): shotlist_lint has no FAIL; layout_check has no FAIL; the model sheets were checked; the independent review passed (accuracy 5, every other category ≥ 4).

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

## 14. Schedule discipline (Saumya, 28 Oct)
- Every Reel is made the day BEFORE it posts (Reel runs claim the next open slot at least 3 hours ahead), posted at its planned time (10:00, plus 18:00 at weekends), with the YouTube Short straight after.
- If a production run fails, the next run picks the slot up; the publisher's 12:55 and 20:55 runs check that tomorrow's 10:00 Reel is being made and start a Reel run if it isn't (see the publisher prompt). Late is better than missing, but on time is the standard: a Reel that misses its slot by more than 3 hours moves to the next open slot rather than posting in a batch.
- Quality still gates publishing (§10); a weak Reel goes to needs_review, and Saumya is told the same day.

## 15. Production workflow v4 (every Reel)
1. **Research (planner):** trend scan, comment mining and the insights; pick the real-life moment, the series and the scripture match (§5).
2. **Brief + beat sheet:** one message, the braided spine (§2–3), word counts, the shot list with the visual mode per shot (§7), transitions, the cover line.
3. **Script + voice:** Hinglish script ≤ 2.4 w/s; Gemini TTS single take; Whisper listen-check.
4. **Cast + shot list + storyboard (§17):** registry entries for every character and model sheets checked; `artifacts/shotlist.json` passes shotlist_lint; then render one still per shot and check them as a contact sheet BEFORE animating (composition, readability, palette, continuity, the key visual of each shot).
5. **Assets:** Night Cinema / Mithila SVG scenes, Chandan diagrams, the Blender portal or one 3D hero plate (§16), and sound (voice, then `sound_design.py`: scored music per world, ambience per scene, story SFX and transition whooshes).
6. **Animate + edit:** HyperFrames composition; camera moves, character acting, signature transitions, subtitles v4.
7. **QA:** layout_check.py (before the high-quality render), then qa_check.py + linecheck.py + the §10 bar, then review_sheet.py and the independent review (§17.5).
8. **Package:** cover (§8, cover.py), caption + keywords + 5 hashtags + comment-to-DM line (CAPTION_STRATEGY v4), YouTube title/description (§12).
9. **Publish:** the publisher posts on time (Instagram, then YouTube); the comment task replies (COMMENT_PLAYBOOK.md).
10. **Learn:** the weekly review reads the owner insights (skip rate, average watch seconds and %, shares and saves per 1,000) and the YouTube retention, and changes one variable a week.

## 16. Blender (3D) in the pipeline
- Installed on demand by the Reel run that needs it: `[ -x $HOME/sv-bpy/bin/python ] || (python3 -m venv $HOME/sv-bpy && $HOME/sv-bpy/bin/pip install -q bpy==5.2.3)` in one Bash call with timeout 900000 (about 3–5 minutes, once per workspace). Cycles on CPU works headless here; EEVEE needs a GPU and is slower.
- **Budgets on this workspace (2 CPUs):** about 30 s per frame at 540×960 and 32 samples with denoising; about 50 s per frame at 720×1280 and 16 samples. So: never render a whole Reel in 3D. Use (a) the pre-rendered portal transition, (b) ONE 3D still plate per Reel at full resolution, animated with 2.5D camera moves, or (c) at most a 2 s 3D hero move at 720×1280 (≤ 60 frames, ≈ 50 minutes; only if the run has time).
- Look: paper layers in brand pigments, a warm key light from the upper left, a cool rim, f/2–2.8 depth of field, AgX view transform. Scripts live in `toolkit/brand-v4/blender/`.

## 17. Craft standard v5: characters, story flow, explainers, final review (Saumya, 30 Oct)
Saumya's review of the v4 Gajendra Reel: the look and direction are right, but faces and characters changed between shots, scenes didn't always follow from each other, and the layout and transitions felt random. From the next Reel on, every Reel meets this section. The Gajendra Reel itself stays as it is. If this section and an earlier one disagree, this section wins.

**17.1 Cast: one design per character, reused everywhere.**
- Every character comes from the cast registry `toolkit/cast/cast.json`, built with `CAST.build(name, svg)` from `brand-kit/cast.js`. Modern series leads (Kabir, Riya, Meera, Maa, Papa, Dev, Tara…) use the Night Cinema rig; scripture figures and animals (Gajendra, the crocodile, Karna, Draupadi, rishis…) use the Mithila rigs. Deities appear as symbols (chakra, lotus, light) unless the scene truly needs a form.
- Never redraw a character for one shot. Close-up, medium and wide are the SAME rig framed with `CAST.frame(rig, "ECU|CU|MCU|MS|WS")`. Faces always sit above the subtitle plate.
- A new character gets a registry entry FIRST (in `artifacts/cast_local.json` for the Reel, then copied into `toolkit/cast/cast.json` in the same commit), so they look identical if they return. A returning character is reused exactly: same face, skin, hair, outfit and colours.
- Before animating, render the model sheets (`scripts/model_sheet.py --names … --extra artifacts/cast_local.json --out qa/cast`) and look at them: same face, hair and proportions in every cell; expressions fit the story.
- Acting: `CAST.emote` with the beat's emotion (neutral, smile, hopeful, sad, worried, shock, angry, tired), blinks and breathing (`CAST.idle`), lip movement on the words (`CAST.talk`), and eyelines toward who or what they react to (`CAST.look`). The emotion changes only when something in the story causes it.

**17.2 Shot list: every scene earns its place.**
Write `artifacts/shotlist.json` (template `templates/shotlist.example.json`) after timing and before building any scene, then run `scripts/shotlist_lint.py <id>` until it shows no FAIL. For every shot record: the narration lines it covers; its **purpose** (what it tells the viewer); the **key visual** (the one thing they must see); world, location, framing size and the transition in; and each character's expression, action, screen side and facing direction.
- **Story elements** (the crocodile, the phone, the lotus…) are visible in the shot where the narration names them. If the voice says it, the picture shows it.
- **Cause, then effect:** the shot order follows the story logic: setup → problem → escalation → parallel → verse → choice → result. No shot exists just to fill time.
- **Continuity:** describe each location once, then keep it (light direction, props, palette). Keep screen direction within a location; a deliberate reversal is marked `"reverse": true`. Use one Mithila panel style (framed or full) per location. Avoid jump cuts (same size, same subjects); vary the framing.
- **Transitions:** within a world, use cut, match, push, rack focus or dissolve. Between the modern and ancient worlds, ALWAYS use a signature transition (thread, portal, bloom), placed on a phrase boundary.

**17.3 Explainers and infographics (the priority format).**
Build every diagram with the explainer kit (`brand-kit/explainer.js` + `explainer.css`), not ad-hoc shapes:
- Use the kit's components: head (kicker + title), node, thread, compare, steps, bars, stat, cycle and callout. Its motion vocabulary (`EX.in / pop / draw / grow / count / focus / out`) reveals the idea in the order it is spoken.
- **Grid and hierarchy:** content stays inside x 72–1008 and y 250–1400 on the 12-column grid. Type scale: kicker 30, label 40, body 42, title 88, stat 150. Nothing is smaller than 30 px. One accent colour per screen; palette tokens only.
- **One idea per screen:** at most 3 nodes, 4 bars or 4 steps. Each explainer shot in the shot list states what it `teaches` and the `diagram` it uses. Labels name things in the viewer's words.
- **Accuracy:** every number, chart and claim cites its source on screen (`EX.source`) and is backed by `sources.json`. Verse references are exact. Never invent data. A labelled illustration ("Illustrative") is fine; a fake statistic is not.
- **Animation explains:** each reveal lands on the word that names it, and `EX.focus` dims what isn't being discussed. No decorative motion that competes with the idea.

**17.4 Layout gate (automatic).**
After `build_composition.py`, run `scripts/layout_check.py <id>`. It seeks the real timeline every 0.5 s and fails on:
- text smaller than 30 px;
- text outside the frame or its margins;
- story text in the platform UI zones;
- overlapping text;
- contrast below WCAG (4.5, or 3 for large text);
- a subtitle covering a face.

It warns on crowding. Fix every FAIL before rendering high quality; it writes red-boxed frames to `qa/layout_*.png`.

**17.5 Final review by an independent reviewer (every Reel, before it can be "ready").**
After the high-quality render, `qa_check.py` and `linecheck.py`:
1. Run `scripts/review_sheet.py <id>`. It writes `qa/review_shots.jpg` (start, middle and end of every shot, with its purpose), `qa/review_cast.jpg` (each character across all their shots, next to their model sheet) and `qa/review_strip.jpg` (one frame per second).
2. Start a **separate reviewer agent** (Agent tool, general-purpose) that did not make the Reel. Give it ONLY the file paths listed in `templates/review.md` and that template. It reads every sheet, judges as a first-time viewer, and writes `qa/review.md` with scores 1–5 for:
   - character consistency
   - factual accuracy
   - storytelling
   - continuity and transitions
   - infographics
   - layout and readability
   - animation
   - overall polish

   Each score cites evidence by shot id. If the Agent tool isn't available, do the review yourself in a fresh pass using only those files, and say so in the log.
3. **Pass:** factual accuracy = 5 and every other category ≥ 4. Otherwise fix the listed issues (by shot id), re-render, and review again. Allow at most 2 rounds; if it still fails, set the slot to "needs_review" with `qa/review.md` attached, and tell Saumya the same day.
4. Record the scores on the slot as "review" and in the log line, so the weekly review can link craft scores to retention.
