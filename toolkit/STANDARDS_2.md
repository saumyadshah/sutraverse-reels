# SutraVerse 2.0 — production standards (from 7 Nov 2026)

**This file governs every plan, Reel and review from 9 Nov 2026.** Where it conflicts with CONTENT_STANDARDS.md, CAPTION_STRATEGY.md or the sutraverse skill, this file wins. Still in force from the older files: the AUTO-PUBLISH rule (no approvals; fix, don't hold), the shloka standard (CONTENT_STANDARDS §4) whenever a verse is shown, subtitles on the solid plate, the independent final review (§17.5), the Gemini Hinglish voice, and never printing keys.

Kit: `toolkit/brand2/` (brand2.css, fonts, cast2.js + cast2.json, TREATMENTS.md, OPUSCAR.md, template/, samples/). Strategy, audit and reasoning: the "SutraVerse 2.0" doc.

## 1. Positioning
**SutraVerse: ancient strategy and modern psychology, for everyday Indian life.** Indian wisdom (Chanakya, Arthashastra, Panchatantra, Hitopadesha, the Gita, the epics, Indian history) is the spine; psychology and global thinkers (behavioural science, Stoics, Sun Tzu, Machiavelli, Greene) are the lens. Every Reel = one real situation + one named idea + one move the viewer can use tomorrow. Never generic motivation, never a lecture.

## 2. Series (pillars) and the weekly mix
| Series | Pillar | Treatment (TREATMENTS.md) | Chapter tag | Typical sources |
|---|---|---|---|---|
| **Chanakya Files** | Ancient strategy | Ember Engraving | `RULE NN` (numbered across episodes) | Chanakya Niti, Arthashastra, Vidura Niti, Sun Tzu/Machiavelli as "versus" |
| **Mind Games** | Psychology & behaviour | Case File | `FILE NN` | peer-reviewed studies, classic experiments, Gita on the mind |
| **Office Shastra** | Corporate & career | Night City Cel | `EP NN` (one continuing cast) | workplace research, negotiation, leadership; a scripture/strategy parallel |
| **Ghar Ki Baat** | Family, friends, money, social pressure | Warm Home Cel | `EP NN` | family psychology, money behaviour; epics and Puranas |
| **Turning Points** | History & business | Archive & Timeline | `CHAPTER N` + the year | history, business cases, rulers and strategists |
| **Panchatantra Reloaded** | Fables for adults | Lamp Theatre → cel | `FABLE NN` | Panchatantra, Hitopadesha, Jataka |

**Cadence: 5 Reels a week, quality first** (data: volume didn't buy reach; 17 of 24 Reels died in the test pool). Mon 10:00 Office Shastra · Wed 10:00 Mind Games · Fri 10:00 Chanakya Files · Sat 18:00 Ghar Ki Baat or Panchatantra Reloaded (alternate) · Sun 10:00 Turning Points. At least 3 of 5 are explainer-led (a diagram, timeline or framework carries the idea). Festivals are told through the week's series, never as a separate "festival Reel" unless the story is genuinely strong.
**Carousels are paused** (30-day data: 4–32 accounts reached each, all followers). Revisit at 1,000 followers.
**Continuity:** the modern cast recurs (Riya, Kabir, Malhotra sir, Maa…); Office Shastra and Ghar Ki Baat are numbered episodes; Chanakya's rules are numbered; a Reel may call back an earlier one ("Rule 07 again"). The knowledge base (`toolkit/kb/`) tracks what was told, so nothing repeats and arcs build.

## 3. Storytelling framework (every Reel is a short film)
1. **Hook (0–2 s).** Frame 1 *shows* the conflict; the first spoken words are a line of dialogue, a number/year, or a belief the Reel will overturn. Text, voice and picture say the same thing at once.
2. **Setup (≤ 8 s).** Who, where, what's at stake, in the viewer's own world.
3. **Conflict / curiosity.** Name the open loop on screen ("Why did 3 doctors refuse to wash their hands?", "Option A or B?").
4. **Explanation.** The named idea (a Chanakya rule, a bias, a historical decision), shown with one diagram/timeline/exhibit per idea, in chapters (`FILE 01 → 02`).
5. **Payoff.** The twist or the better move (often "Option C"), ending on the principle card: one line to remember + its source.
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
- 6–10 specific keywords woven into sentences (no repeated boilerplate keyword line). 3–5 hashtags chosen for *this* Reel from the series pool; never the same set twice in a row.
- Pinned first comment: the either/or question restated with two numbered options.
- Comment-to-DM keyword per series (after Saumya enables Meta automations): RULE (Chanakya Files), FILE (Mind Games), EP (Office Shastra / Ghar Ki Baat), YEAR (Turning Points), FABLE (Panchatantra).

## 10. Growth: what we measure and test
Per Reel: skip rate (target ≤ 30%), average watch % (≥ 45%), shares and saves per 1,000 plays (≥ 10 and ≥ 8), comments per 1,000 (≥ 2), non-follower reach, profile visits and follows.
Account: weekly followers gained and profile visit → follow conversion (now ~0; target ≥ 10%).
One controlled experiment per week (one variable: hook type, length, treatment, cover, CTA), logged in `plan.json` "experiments" with the result. Instagram doesn't expose per-second retention through the API: the weekly review asks Saumya for retention-graph screenshots of the best and worst Reel only when a diagnosis needs them.

## 11. Skills (lean set; load only these)
- Plan: content-research (outliers), trend-spotter, series-planner, hook-mining (monthly), content-pillar-builder (monthly).
- Reel: sutraverse (voice, captions, publishing), virality (hook checklist), ab-hook-tester, on-screen-text-writer, cta-writer, Lemo-Opuscar guides (DIRECTOR.md, TECHNIQUE.md, the treatment's base STYLE.md).
- Cover & title: cover-thumbnail-brief, yt-package (title.py), yt-seo.
- Caption: caption-and-hashtags, hashtag-keyword-research.
- Review: analytics-readout, reel-analyzer (week's best outlier), comment-mining, yt-retention (if a CSV exists), profile-conversion-audit (monthly).
- Retired from the pipeline (overlapping or unused; still installed, not loaded): going-viral, viral-hook-writer, reel-scripter, reel-builder, youtube-scriptwriting, yt-script, youtube-thumbnail, youtube-seo, cross-platform-reformatter, content-calendar, story-sequencer, carousel-builder, viral-carousel (carousels paused), yt-plan, yt-viral, best-time-scheduler, social-analytics-report, content-audit.
