# Shlokwise — production standards (2.0 kit, from 7 Nov 2026)

**BRAND (Saumya, 13 Nov 2026): the brand is Shlokwise, "Getting wise with Shlok".** SutraVerse is another entity's trademark, so it never appears in anything viewers see (caption, title, description, cover, frame, end card, reply, bio, hashtag, keyword). Every viewer-facing name, line, handle and hashtag comes from `toolkit/BRAND.json`: wordmark SHLOKWISE, tagline "Getting wise with Shlok", the follow line and end card with `@{ig}` = `instagram.handle` (the current handle until Saumya confirms the rename), brand hashtag #Shlokwise, brand keyword Shlokwise. Internal names (repo, env files, the `sutraverse` skill, task names) stay as they are.

**This file governs every plan, Reel and review from 9 Nov 2026.** Where it conflicts with CONTENT_STANDARDS.md, CAPTION_STRATEGY.md or the sutraverse skill, this file wins. Still in force from the older files: the AUTO-PUBLISH rule (no approvals; fix, don't hold), the shloka standard (CONTENT_STANDARDS §4) whenever a verse is shown, subtitles on the solid plate, the independent final review (§17.5), the Gemini Hinglish voice, and never printing keys.

Kit: `toolkit/brand2/` (brand2.css, fonts, cast2.js + cast2.json, TREATMENTS.md, OPUSCAR.md, template/, samples/). Strategy, audit and reasoning: the "SutraVerse 2.0" doc (internal).

## 1. Positioning
**Shlokwise — getting wise with Shlok: ancient strategy and modern psychology, for everyday Indian life.** Indian wisdom (Chanakya, Arthashastra, Panchatantra, Hitopadesha, the Gita, the epics, Indian history) is the spine; psychology and global thinkers (behavioural science, Stoics, Sun Tzu, Machiavelli, Greene) are the lens. Every Reel = one real situation + one named idea + one move the viewer can use tomorrow. Never generic motivation, never a lecture.

## 2. Series (pillars) and the weekly mix
| Series | Pillar | Treatment (TREATMENTS.md) | Chapter tag | Typical sources |
|---|---|---|---|---|
| **Chanakya Files** | Ancient strategy | Ember Engraving | `RULE NN` (numbered across episodes) | Chanakya Niti, Arthashastra, Vidura Niti, Sun Tzu/Machiavelli as "versus" |
| **Mind Games** | Psychology & behaviour | Case File | `FILE NN` | peer-reviewed studies, classic experiments, Gita on the mind |
| **Office Shastra** | Corporate & career | Night City Cel | `EP NN` (one continuing cast) | workplace research, negotiation, leadership; a scripture/strategy parallel |
| **Ghar Ki Baat** | Family, friends, money, social pressure | Warm Home Cel | `EP NN` | family psychology, money behaviour; epics and Puranas |
| **Turning Points** | History & business | Archive & Timeline | `CHAPTER N` + the year | history, business cases, rulers and strategists |
| **Panchatantra Reloaded** | Fables for adults | Lamp Theatre → cel | `FABLE NN` | Panchatantra, Hitopadesha, Jataka |

**Cadence: 1 Reel every day (Saumya, 9 Nov 2026; was 5/week).** Mon 10:00 Office Shastra · Tue 10:00 Mind Games · Wed 10:00 Ghar Ki Baat · Thu 10:00 Chanakya Files · Fri 10:00 Office Shastra or Mind Games (alternate weeks) · Sat 18:00 Panchatantra Reloaded · Sun 10:00 Turning Points. At least 4 of 7 are explainer-led (a diagram, timeline or framework carries the idea). Festivals are told through the day's series, never as a separate "festival Reel" unless the story is genuinely strong. Quality first: if a run can't finish a Reel to standard, the slot moves, it is never filled with a weaker video.
**Carousels are paused** (30-day data: 4–32 accounts reached each, all followers). Revisit at 1,000 followers. When they return: render with `brand2/carousel2.py` (same spec as v4 make_post.py + "series"/"format"). **Music on carousels:** Instagram supports it only in the app; neither the Instagram Graph API, Metricool (its audio option is Reels-only) nor vidIQ can attach music to a carousel. So either (a) Saumya adds a track from the app after it posts (Edit → Add music), or (b) the carousel is also cut as a slideshow Reel with our own original score (sampler/pluck/synth), which can publish automatically.
**Continuity:** the modern cast recurs (Riya, Kabir, Malhotra sir, Maa…); Office Shastra and Ghar Ki Baat are numbered episodes; Chanakya's rules are numbered; a Reel may call back an earlier one ("Rule 07 again"). The knowledge base (`toolkit/kb/`) tracks what was told, so nothing repeats and arcs build.

## 3. Storytelling framework (every Reel is a short film)
1. **Hook (0–2 s).** Frame 1 *shows* the conflict; the first spoken words are a line of dialogue, a number/year, or a belief the Reel will overturn. Text, voice and picture say the same thing at once.
2. **Setup (≤ 8 s).** Who, where, what's at stake, in the viewer's own world.
3. **Conflict / curiosity.** Name the open loop on screen ("Why did 3 doctors refuse to wash their hands?", "Option A or B?").
4. **Explanation.** The named idea (a Chanakya rule, a bias, a historical decision), shown with one diagram/timeline/exhibit per idea, in chapters (`FILE 01 → 02`).
5. **Payoff.** The twist or the better move (often "Option C"), ending on the principle card: one line to remember + its source.
   **A verse in every Reel (Saumya, 9 Nov 2026).** Every Reel, in every series, shows ONE verified shloka/verse card that genuinely connects to its idea: Devanagari + IAST + plain English meaning + exact reference with edition (CONTENT_STANDARDS §4), on screen ≥ 4 s, voiced in Sanskrit or Hinglish meaning. Place it at the payoff (it can be the principle card itself). For a psychology/office/history idea, choose a real parallel from the Gita, Chanakya Niti, Vidura Niti, Hitopadesha/Panchatantra, the Upanishads, the epics, Yoga Sutras or Subhashitas — and say "parallel", never claim the text "proves" a modern study. Verify the verse on two editions; never invent, paraphrase into quotation marks, or force a verse that doesn't fit (pick a different, fitting one). The caption cites the verse reference; the SEO keyword section includes it.
6. **Engagement.** One specific either/or question tied to the conflict ("Would you send the deck or say it in the meeting?"). No "follow for more", no motivational outro.

**Hook rules from our data** (skip ≤ 36% → median 2,017 views; > 36% → 183):
- Wins: an instantly legible, unfair everyday conflict (leave favouritism, "log kya kahenge", the sibling who stayed, the mom who never says proud); dialogue first.
- Banned openers: "Did you know…", "In the Bhagavad Gita…", "Have you ever…", a scripture/character name before the conflict, an unnamed stranger's backstory ("Kabir got laid off…"), abstract claims ("Death offered a boy everything").
- Write 5 hooks, score them against these rules (and the virality skill's checklist), keep 2 (A/B), store `alt_hook`.

**Length:** whatever the story needs, usually 45–75 s; Turning Points and Mind Games may run to 90 s when every beat earns it. Pace by chapter, not by a clock: the viewer must always know where they are.

## 4. Formats (rotate; no two consecutive Reels share one)
Story → Framework · Case File (one named trick) · Then & Now (history/scripture ↔ modern) · Versus (Chanakya vs Machiavelli; Gita vs Stoics; what people believe vs what the text says) · Fable Remix · Turning Point (year hook → decision → consequence → lesson) · Myth vs Text.

## 5. Research and accuracy
- Every Reel keeps `FACTS.md`: each claim, its source (book + chapter/verse + edition, or paper + year + journal, or a reputable history source), and the exact wording used on screen.
- Chanakya Niti and other niti texts: verse numbers differ by edition: cite the edition, or say "attributed to". Arthashastra: cite book.chapter (Kangle or Rangarajan). Legends (e.g. Chanakya's shikha vow) are labelled "Tradition holds".
- Psychology: name the study or the concept's source (author, year); never present pop-psych or "dark psychology" tricks as how-tos: always *recognise it → defend against it*.
- History: "c." for uncertain dates; no modern borders projected into the past; maps per OPUSCAR.md.
- A shown verse follows CONTENT_STANDARDS §4 (Devanagari + IAST + English + exact reference).
- Never invent quotes, numbers, studies or verses. A paraphrase is labelled "Paraphrase".

## 6. Characters (non-negotiable)
- Only registered characters from `brand2/cast2.json`, drawn with `cast2.js` (`CAST2.draw`) in the treatment's style (`cel` or `engrave`). Same face, proportions, hair and clothes in every angle and shot size.
- New character → add to cast2.json first (role, age, era-appropriate look), render its sheet with `brand2/sheet2.py`, check it, commit it with the Reel.
- Expressions change only when the story causes it; eyelines point at what the character reacts to; `talk` while speaking; blink occasionally.
- Arms are the rig's weakest part: prefer CU/MCU/bust framing; use `arms` poses only at MS, and never in a key close moment until the arm rig is upgraded.
- Deities appear as symbols (light, lotus, chakra), not faces.

## 7. Production workflow (each step's output is a file in the project)
Research → topic (from the weekly plan) → **FACTS.md** → script (Hinglish VO + English on-screen) → **TREATMENT.md** (Opuscar DIRECTOR.md §4: 3 candidate structures, logline, benchmark learn/don't-learn, shot list with framing/move/duration/why, beat sheet, cue map, sound design table) → **storyboard** (6–9 key shots rendered with the real code, tiled by `sheet.py`; reviewed by a separate reviewer agent before full animation) → characters (cast2; sheets for new ones) → visual development (style frames) → animation (`brand2/template` + Opuscar renderer) → edit (chapters, transitions inside the medium) → sound (Gemini VO, score from the sampler/pluck/synth, foley from `EV`, two silences, J/L cuts, −14 LUFS) → cover (`frame 0`, the series cover system) → caption & SEO → QA (§8) → scheduling (status "ready") → publishing (publisher task) → performance analysis (weekly review).

## 8. Quality assurance (before "ready")
Automated: `readcheck.mjs` passes; no black frames (`blackdetect`); loudness −14 ±1 LUFS; frame 0 is the cover; subtitles never cover a face or a key action; all text ≥ 30 px inside the content box.
Independent review (separate agent, CONTENT_STANDARDS §17.5 + `templates/review.md`) scores 1–5: character consistency, factual accuracy, storytelling & hook, continuity & transitions, infographics, layout & readability, animation, sound, overall polish. Factual accuracy must be 5 (fix by cutting/rewording). Then AUTO-PUBLISH applies: fix within 2 rounds, log what's left, post.

## 9. Captions, SEO, comments
- Line 1: the conflict in the viewer's words + the search phrase (≤ 110 chars). Then the idea and its source, the move, the either/or question.
- Weave the main search words naturally into the sentences too. 3–5 hashtags chosen for *this* Reel from the series pool; never the same set twice in a row.
- **SEO keyword section (mandatory on every Reel, Short and post; Saumya, 7 Nov 2026).** One dedicated line, after the follow line and before the hashtags, in exactly this format: `[keyword one, keyword two, keyword three]` — square brackets, comma + space between keywords, no hashtags or emojis inside. 10–15 keywords, researched for *this* piece, never a reused generic set:
  1. the search phrase first (what a real person types into Instagram search for this problem);
  2. the conflict in the viewer's own words, including the Hinglish/Hindi spellings people actually type ("boss credit le gaya", "log kya kahenge");
  3. the named idea (bias, rule, concept) and its plain-English synonym;
  4. the source / character / text (e.g. "chanakya niti", "duryodhana envy", "bhagavad gita 2.14");
  5. the situation and audience (e.g. "office politics india", "desi family", "corporate life");
  6. the series name, and "Shlokwise" last (BRAND.json brand_keyword). Never "SutraVerse".
  Research: hashtag-keyword-research skill, Instagram search autocomplete phrases visible in the week's outliers' captions, and the planner's search_phrase. Lower-case except proper nouns; each keyword 1–4 words; no duplicates or near-duplicates. Store the list on the slot as `seo_keywords`. YouTube descriptions carry the same list in the same bracket format (yt_upload.py builds it from meta "keywords").
- Pinned first comment: the either/or question restated with two numbered options.
- Comment-to-DM keyword per series (after Saumya enables Meta automations): RULE (Chanakya Files), FILE (Mind Games), EP (Office Shastra / Ghar Ki Baat), YEAR (Turning Points), FABLE (Panchatantra).

## 10. Growth: what we measure and test
Per Reel: skip rate (target ≤ 30%), average watch % (≥ 45%), shares and saves per 1,000 plays (≥ 10 and ≥ 8), comments per 1,000 (≥ 2), non-follower reach, profile visits and follows.
Account: weekly followers gained and profile visit → follow conversion (now ~0; target ≥ 10%).
One controlled experiment per week (one variable: hook type, length, treatment, cover, CTA), logged in `plan.json` "experiments" with the result. Instagram doesn't expose per-second retention through the API: the weekly review asks Saumya for retention-graph screenshots of the best and worst Reel only when a diagnosis needs them.

## 12. Lessons from the competitor study (@balakheji, 9 Nov 2026; details in kb/competitors.md)
Keep our identity (animated cast, Indian wisdom + verse, Hinglish). Adopt these mechanics:
1. **Emotional micro-conflict first.** The strongest topics are two-person moments every viewer has been on one side of (saying no to family, apologising, being left out, a friend's success, a boss's double standard). Each Reel's real_life_angle names who will SEND it to whom.
2. **Open on a quoted line or a sensory image + a name**, never on context: "“Papa, maine purse khola nahi hai.”" / "Anil ke joote mein baarish ka paani bhar raha tha." Then flash back.
3. **One source of authority per Reel**, said plainly: for us, the verse (the shloka card) plus at most one named book or study. No source lists on screen.
4. **The exact words.** Every Reel ends with the character saying the better sentence (the script viewers can copy), then the verse, then the either/or. Captions repeat the sentence.
5. **Pace and length:** calm, empathetic narration (≈ 120–135 words/min), soft score, 2–3 cuts per 10 s; 70–95 s when the story needs it. Calm is fine if every beat raises the stakes.
6. **Numbered-course covers (test from week of 16 Nov):** a series-coloured card with the series tag + number and a 3–4 word Hinglish question in the viewer's words (one amber word), the same template every time, so the grid reads like a course. A/B against the face cover; keep the winner (see §10).
7. **End card with a value promise:** BRAND.json `end_card` ("Getting wise with Shlok. Follow @{ig}") (≤ 2 s, after the either/or). No mid-video CTA.
8. **Shares and saves over comments:** a viral Reel can have almost no comments; judge Reels on skip rate, watch %, shares/1k and saves/1k.
10. **YouTube = text seasons (from Balakheji's book seasons; @BalakheJi grew to 756 subscribers in 30 days on Shorts alone, 3.5 a day).** Every Short is numbered by the source text of its verse (kb/seasons.md: Bhagavad Gita - Lesson NN, Chanakya Niti - Rule NN, Panchatantra - Fable NN, Itihaas - Chapter NN). yt_title = "<emotional Hinglish hook with an ellipsis…> | <Text> - <Lesson/Rule/Fable/Chapter> NN #Shorts", ≤ 95 characters, problem first (supersedes the "≤ 60" title limit in the Reel and publisher task prompts; Saumya, 9 Nov). yt_playlist = the season's playlist. The Reel run takes the next number and records it in kb/seasons.md in its commit.
11. **Emotional beats productivity.** On both his platforms the relationship book (Courage to Be Disliked) out-performed habits and power books 5–10×. Prefer relationship/family/self-worth angles inside every series.
9. **Volume ramps with quality:** 1 a day now; 2 a day only once three weeks in a row hit skip ≤ 33% and watch ≥ 40%.

## 13. VIRAL CUT — hard gates before "ready" (Saumya, 14 Nov 2026: "make sure it is proper, catchy, viral")

Context: Office Shastra EP 03's first cuts opened on two static faces with small UI text, held shots 5–15 s (the verse card ~15 s), carried meaning in tiny mono text and ended on a faded end card. These rules override §3/§4/§12 wherever they conflict (incl. the 45–75 s / 70–95 s lengths).

1. **0–1.5 s = the hook card.** The conflict in ≤ 8 words, ≥ 96 px, one vermilion word, over the most emotional image (a reacting face, the stamp, the screen). A hit (stamp/whoosh/impact) by 1.0 s. The first spoken words ARE the hook. No series intro, no title card, no small UI card in the first 3 s.
2. **Pattern interrupts.** A visual change (cut, push-in, whip, stamp, pop, new prop) every ≤ 2 s in the first 10 s, then every ≤ 3 s. No shot held > 4 s — the verse card included.
3. **Captions people can read at a glance.** Kinetic word-group captions, ≥ 56 px, ≤ 5 words per card, the key word highlighted. Anything that must be read is ≥ 40 px and stays ≥ 1.5 s; small mono labels are decoration only.
4. **Length 35–50 s** (Turning Points and Panchatantra Reloaded ≤ 60 s). Script ≈ 95–125 Hinglish words. Cut every line that doesn't raise the stakes or pay off.
5. **Characters act.** Expressions change on the beats (worried → stung → resolved), heads are never cropped at the top, bodies never cut awkwardly at the shoulders; every character shot moves (push-in, head turn, blink, gesture). Two characters in one shot must look clearly different (hair, outfit colour, build).
6. **Verse ≤ 8 s and inside the story:** shown over the scene it explains (e.g. the crow lands on the meeting-room table), one Devanagari line + one English line; the full reference goes in the caption.
7. **One screenshot-worthy payoff frame** (the template / line / framework), held 2 s, with a small "Save this" cue.
8. **Ending:** the either/or question as big text (1 or 2), then the BRAND.json end card at full opacity for ≥ 1.5 s.
9. **Sound:** an impact on the hook, a rise under the conflict, a drop/resolve on the payoff; voice always on top.
10. **Gate:** the final review (templates/review.md) scores Hook and Retention; both must be ≥ 4 or the run recuts (max 2 rounds). Before rendering, write the shot list with timestamps and check rules 1–8 against it.

## 11. Skills (lean set; load only these)
- Plan: content-research (outliers), trend-spotter, series-planner, hook-mining (monthly), content-pillar-builder (monthly).
- Reel: sutraverse (voice, captions, publishing), virality (hook checklist), ab-hook-tester, on-screen-text-writer, cta-writer, Lemo-Opuscar guides (DIRECTOR.md, TECHNIQUE.md, the treatment's base STYLE.md).
- Cover & title: cover-thumbnail-brief, yt-package (title.py), yt-seo.
- Caption: caption-and-hashtags, hashtag-keyword-research.
- Review: analytics-readout, reel-analyzer (week's best outlier), comment-mining, yt-retention (if a CSV exists), profile-conversion-audit (monthly).
- Retired from the pipeline (overlapping or unused; still installed, not loaded): going-viral, viral-hook-writer, reel-scripter, reel-builder, youtube-scriptwriting, yt-script, youtube-thumbnail, youtube-seo, cross-platform-reformatter, content-calendar, story-sequencer, carousel-builder, viral-carousel (carousels paused), yt-plan, yt-viral, best-time-scheduler, social-analytics-report, content-audit.
