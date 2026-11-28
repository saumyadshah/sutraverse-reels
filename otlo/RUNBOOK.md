# Otlo runbook: one post per run

Otlo (ઓટલો, Instagram **@otlo.gujarat**) is Saumya's faceless Gujarati culture, food and cinema brand.
Posts: Reels (Gujarati voice-over, English subtitles, bilingual on-screen text) and carousel slots
(bilingual slides, posted as voiced swipe-style Reels), all in the "Kankotri Press" style. Scheduled runs follow this file **exactly**, work unattended and ask
nothing. Each run handles **one slot**: the calendar row whose Date is today (Asia/Kolkata) and whose
Time (IST) is the run's slot (`13:00` = midday run, `19:30` = evening run).


> ## ✅ OTLO BRAND STANDARD v1.1 APPROVED (Saumya, 28 Nov 2026 17:28 IST): MANDATORY FOR EVERY REEL
> Every Reel is built with the brand kit in `otlo/toolkit/BRAND.md` (`body.otlo`, `brand.css`/`brand.js`): toran,
> cinematic dissolves, `"single_take": true` voice, `"score": "otlo"` music, official logos where the story names an
> organisation, real posters/photos with cutouts, maps and infographics. The reference is
> `otlo/work/2026-11-28-amul-manthan-v2` (copy its `reel.html`, `cover.html` and `script.json` structure, never its
> content). Every Reel must look like an officially produced OTLO feature; if a build can't reach that bar, make
> the backup, don't publish a weaker look. Chat Reels and static carousels stay discontinued. Never publish
> `otlo/work/2026-11-28-1930-*` (the superseded draft).

## Schedule (Saumya, 26 Nov 2026 overhaul): prepared in advance, two posts every day

Two posts every day, weekends included: **Morning 10:00 IST** and **Evening 19:30 IST**. Days alternate
A (carousel slot in the morning, posted as a swipe-style Reel + Reel in the evening) and B (Reel + Reel), as the
calendar says. Each post is made by a **PREP run** well before its slot and published by a short **PUBLISH run**:

| Run | When (IST) | Does |
|---|---|---|
| PREP evening | 14:15 | makes, checks and readies tonight's 19:30 post; its final reply is the content email |
| PUBLISH evening | 19:25 | publishes the readied 19:30 post (and recovers any unconfirmed container) |
| PREP morning | 21:15 | makes, checks and readies tomorrow's 10:00 post; its final reply is the content email |
| PUBLISH morning | 09:55 | publishes the readied 10:00 post (and recovers any unconfirmed container) |

A PREP run follows **Steps 1–7** and **Step 8-PREP**; a PUBLISH run follows only **Step 8-PUBLISH** and **Step 9**.
The calendar holds one week at a time, planned every Saturday by `otlo/PLANNING.md` (backlog: `Idea bank`).

## Fixed IDs

| What | Value |
|---|---|
| Repo | `saumyadshah/sutraverse-reels` (public), branch `main` |
| Content calendar (Claude Sheet) | artifact `e89bed33-8969-476f-9b60-09a18065bbb3`, workbook node `3d2daa40-bf99`, sheet `Calendar` |
| Calendar columns | A Date · B Day · C Time (IST) · D Format (Reel / Carousel) · E Series · F Topic · G Notes and sources to check · H Status (Idea / To make / Ready / Posted / Skipped) |
| Strategy doc | https://claude.ai/artifact/LCvcv5vPVocJuHEjeKDrU9 |
| Instagram (vidIQ) | platformAccountId `29167885212872260` (username otlo.gujarat) |
| Voice | Otlo narrator = Gemini TTS voice `Sulafat` (warm, expressive) for every non-chat Reel; chat Reels use one voice per character (see 4B-chat). `direction` always `""` (instruction text gets read aloud) |

Sheets calls: `read`/`update` with `ref={"object":"node","id":"3d2daa40-bf99"}`,
`container={"kind":"project","id":"e89bed33-8969-476f-9b60-09a18065bbb3"}`, `engine="workbook"`.
Read `{"kind":"readCells","sheet":"Calendar","range":"A1:H120"}`. Write
`{"kind":"applyEdits","base":<revision>,"edits":[{"kind":"writeCells","sheet":"Calendar","topLeft":"G<row>","rows":[["<notes>","Posted"]]}]}`
(call the Docs `guide` with `topic.sheets` first if unsure).

## Creative standard v3 (Saumya's 28 Nov brief: "a professionally managed Gujarati entertainment and lifestyle media brand")

**What the data says (28 Nov audit, last 12 Reels):** the two posts on real, timely subjects with real visuals won by
about 10×. *Ruff & Tuff Kanya* (official poster, a named filmmaker's quote, posted the week of release) got 1,473 plays,
6 shares and 3 comments. *Pol maze* (a "that's not a mistake, it's design" reveal) got 1,145 plays and the best skip rate (57%).
Everything generic or evergreen stalled at about 120 plays, and chat Reels skipped 72–89%. So:
- **Timely beats evergreen.** At least 1 of the 2 daily posts is tied to something happening now: a release, a
  box-office number, an announcement, an anniversary this week, an upcoming event, a festival, the weather.
- **Real visuals beat drawings for real subjects.** Films → the official poster/artwork; events → official event
  artwork; places/food → licensed photos or AniDoodle illustrations; stories → illustration and motion.
- **Named people and numbers travel.** "₹50 lakh → ₹100 crore", "Hansal Mehta said…" beat abstract claims.
- **Every Reel has a reason to exist**: write it in one line in the ready file ("why would someone send this?").
  If the answer is weak, change the angle or replace the idea. Never post filler to fill a slot (a stronger
  backup from the Idea bank beats a weak planned post).

**Motion standard (FX layer v1, see `otlo/toolkit/TOOLS.md`).** Every Reel uses at least two of: kinetic type
(`data-kinetic`), a count-up (`data-count`), a stamp (`data-stamp`), a highlighter sweep (`data-sweep`), Ken Burns on
photos (automatic on `img.photo`, wrap in `.kbframe`), a 3D poster card or a bokeh/confetti layer (`canvas.fx3d`),
custom GSAP tweens (`window.OTLO_TWEENS`). Include the FX scripts (see the Laalo example
`otlo/work/2026-11-28-1930-laalo-one-year/reel.html`). Motion must serve the story (reveal, emphasise, pay off),
never decorate it.

Every post must also meet all of these; the review in Step 6 checks each one.
1. **Hook in frame one.** The first spoken line (≤ 60 Gujarati characters) and its on-screen text start at once:
   no title card, no greeting, no "today we'll see". Open on a surprise, a rivalry, a number, a feeling or the most
   dramatic message. Write 3 hooks (viral-hook-writer), pick one (ab-hook-tester), log the other two.
2. **18–35 seconds** (hard ceiling 40). 5–7 lines, each ≤ 90 Gujarati characters; one idea per line; cut every line
   that does not move the story. End on the payoff + one short ask. **Never tease or announce another Reel.**
3. **Something changes every 1.5–2.5 s**: a new scene, a pop-in element, a bubble, a number. The engine adds the
   slide-in cuts, the push-in, whooshes, pops and message pings; you supply enough elements (2–4 per scene,
   staggered `data-in`).
4. **Voice**: the narrator `Sulafat`, written to be spoken: short sentences, contractions, "!" and "?" where a person
   would use them. Chat Reels: character voices, no narrator except the final ask.
5. **Subtitles and safe zones**: subtitles are automatic (large, white on indigo, about y 1,380–1,480). All other
   text stays between **y 240 and 1,480**, and **left of x 912 below y 1,000** (Instagram's buttons). The 3:4
   profile grid shows y 240–1,680: the hook must read there too. The builder fails any text outside these zones.
6. **Visuals must show the real subject** and fill their space. Pick per topic (Saumya, 28 Nov): films → the
   official poster/promotional artwork (`wiki_poster` / `og` / `url` sources in `script.json` `images`, credit in
   the caption); events → official event artwork; food/places → Commons photos (licensed) or AniDoodle/AI
   illustrations; stories/explainers → illustration, motion graphics, 3D. Never a fake AI poster when the real
   one exists, never AI images of real people, no clip art. Art and images end above y 1,366.
7. **Cover**: the designed thumbnail is frame one only (Instagram uses it as the cover); frame two is the hook.
8. **Shareability test** before building: would a Gujarati viewer send this to their family group, save it, or
   comment? If none, change the angle (rivalry, surprise, nostalgia, a "that's my Ba" moment, a useful list).

## Hard rules (never break)

1. **One post per run, only this slot's row.** If there is no row for today + this slot, or its Status is
   `Posted`/`Skipped`, or `otlo/logs/<today>.md` already records this slot as POSTED, stop and log why.
2. **Facts.** Every factual claim (dates, tithis, history, numbers, release dates, box office) needs two
   independent reliable sources found today with WebSearch/WebFetch (start from column G). Drop any claim you
   cannot confirm. If the topic's core cannot be confirmed, mark the row `Skipped` with the reason and post nothing.
   Religious practice is described as belief/tradition ("it is believed", "many families"), never as fact or advice.
3. **Cinema (updated 28 Nov).** Official posters, promotional artwork and official stills from the production
   house, distributor or the film's official listings ARE allowed, credited in the caption ("Poster: <studio>,
   official"), used to report on the film. Still no film/trailer video clips, no song audio, no film dialogue, no
   fan edits. *Loko Shu Kahe Chhe?* reports what named critics and audiences said (attributed); Otlo gives **no
   verdict on a film it has not watched**. Box office numbers only with a named source, labelled
   "reported"/"estimated". Tag the official accounts (studio, production house, director, cast) when posting.
4. **People and communities.** No real private individuals. No caste, communal, political or religious
   ridicule; no stereotypes beyond gentle, affectionate food rivalry. *Family Group Chat* is original comedy with
   invented characters (Ba, Mummy, Pappa, Fai, the NRI cousin).
5. **Copyright.** No song lyrics, film dialogue or third-party audio. Third-party images only as rule 3/6 allow
   (official promotional artwork with credit; Commons with an open licence and credit). Everything else is ours:
   SVG, AniDoodle, AI-generated illustration, GSAP/Three.js motion. Never copy another creator's post; take the
   format or idea and make an original Otlo version.
6. **Images must match the subject.** Khaman must look like khaman, a kite like a kite. Draw it carefully.
7. **Partnerships (28 Nov).** Otlo invites collaborations (see `otlo/PLANNING.md` → *Collaboration formats*), but
   no paid or sponsored post is ever made without Saumya confirming the deal in chat. A paid post is labelled
   in the first caption line ("Paid partnership with …" / #ad) and uses Instagram's paid-partnership label.
   Editorial posts never take money and say so when the subject could look promotional ("Not sponsored").
   Still no automated replies/DMs and no deleting posts.
8. **Mandatory for every post: highest-quality export, a designed thumbnail/cover, the full caption formula
   (with the [keywords] block and exactly 5 hashtags), and the skills listed below.** A post missing any of these is not posted.
9. **When in doubt, skip the topic, not the slot** (Saumya, 22 Nov), **but never post weak content** (28 Nov). If this
   slot's topic fails rule 2, 3 or 4, mark its row `Skipped` with the reason and make a **backup** from the weekly
   plan's reserve list or the `Idea bank`: a fact-based documentary Reel whose sources you CAN confirm today. Add it
   as a new calendar row (same date and time) and post it, even up to 60 minutes late. **Never use a chat Reel as a
   backup (chat Reels are discontinued).** If no backup meets the quality review, leave the slot empty and say why.
10. **Language posts (Gujlish Shabdkosh, Shabdkosh Cards):** the two sources may be one Gujarati dictionary
   (GujaratiLexicon, Bhagavadgomandal, Rekhta Gujarati) plus one published usage example from a reputable
   Gujarati outlet or book; say "commonly used to mean" rather than claiming a dictionary definition you could
   not read.

## Skills to use (Saumya: "take into account all the skills we have")
Load each with the Skill tool at the step it belongs to and follow it, inside Otlo's rules (these hard rules win
if a skill says otherwise). If a skill is not available in the run, apply its idea from this table and note it in the log.

| Step | Skills |
|---|---|
| Video craft (always, before a Reel) | `anthropic-skills:video-making`, `anthropic-skills:virality`, `anthropic-skills:going-viral` |
| Hook (4A line 1) | `anthropic-skills:viral-hook-writer` (write 3), `anthropic-skills:ab-hook-tester` (pick the stronger); `anthropic-skills:hook-mining` only if a hooks CSV exists in `otlo/data/` |
| Script + scenes (4A/4B) | `anthropic-skills:reel-scripter`, `anthropic-skills:reel-builder`, `anthropic-skills:on-screen-text-writer`, `anthropic-skills:frontend-design` (layout/typography of the HTML) |
| Ending ask | `anthropic-skills:cta-writer` |
| Thumbnail | `anthropic-skills:cover-thumbnail-brief` |
| Carousel (4C) | `anthropic-skills:carousel-builder`, `anthropic-skills:frontend-design`; `anthropic-skills:viral-carousel` only in the weekly plan (it spends vidIQ credits) |
| Caption (7) | `anthropic-skills:caption-and-hashtags`, `anthropic-skills:hashtag-keyword-research` (keywords block + the 5 hashtags) |
| Research (3) | `anthropic-skills:content-research` / `anthropic-skills:trend-spotter` for angles (free tools only in daily runs) |
| Motion and visuals (4B) | `otlo/toolkit/TOOLS.md` (read it): GSAP docs `otlo/toolkit/skills-ref/gsap/`, Three.js docs `otlo/toolkit/skills-ref/threejs/`, art-motion grammar `otlo/toolkit/skills-ref/huashu-art-motion/`, illustrations `otlo/toolkit/anidoodle/SKILL.md` |
| Series and formats | `anthropic-skills:series-planner` (weekly plan), the series bible in `otlo/PLANNING.md` |
| Quality review (6) | Saumya's 13 questions (PLANNING.md → Quality review), answered in the ready file |

Not used, because they break Otlo rules: `comment-responder`, `dm-script-writer`, `content-factory` (auto-DMs and
3 posts a day), `collab-outreach` / `creator-outreach` / `influencer-partnerships` / `ugc-creator-brief` (no
outreach or sponsorship without Saumya), `sutraverse` (the old brand). vidIQ credits are limited (150/month):
daily runs use only free vidIQ tools (upload, publish, post list); paid research belongs to the weekly plan,
at most 15 credits a week.

## Steps

### 1. Set up
```
cd $HOME && (test -d sutraverse-reels/.git && git -C sutraverse-reels pull -q || git clone -q https://github.com/saumyadshah/sutraverse-reels)
```
(If clone or push is refused, use add_repo with owner `saumyadshah`, repo `sutraverse-reels`, access `push`.)
Work dir: `otlo/work/<YYYY-MM-DD>-<HHMM>-<short-slug>/`.

### 2. Read the calendar
Read `A1:H120`. Find this slot's row, and the next row (for the "Next:" line on the end card / last slide).

### 3. Research
Follow hard rule 2. Keep a source list (outlet + URL). Note 8–12 search phrases people would type for this topic
(English and Gujarati) for the keyword block.

### 4A. Reel: script → `script.json`
```json
{"voice":"Kore","direction":"",
 "thumb":{"chip_gu":"…","chip_en":"…","gu":"<2–3 word Gujarati title>","en":"<promise, ≤ 32 chars>",
          "ribbon_gu":"…","ribbon_en":"…","art_t":<sec in the original timeline where the best art is on screen>,
          "art_clip":[x,y,w,h]},
 "lines":[
  {"id":"s1","gu":"<hook, ≤ 90 chars>","en":["subtitle chunk","subtitle chunk"]},
  … 5–7 lines in total; the last is always:
  {"id":"sN","gu":"ગુજરાતની વાતો, ઓટલા પર. ઓટલોને ફોલો કરો.","en":["Stories of Gujarat, on the otlo.","Follow Otlo."]}
]}
```
- Natural, warm, spoken Gujarati, ≤ 90 characters per line (hook ≤ 60); 18–35 s in total; voice `Sulafat`.
- Line 1 is the hook: a paradox, a felt question or a reveal (see the reference patterns below).
- `en`: faithful plain-English subtitle chunks of ≤ 55 characters each, covering the whole line.
- **Thumbnail (mandatory):** the cover must say the subject in 2–3 big Gujarati words plus a short English
  promise, and show the subject's art. `art_clip` is the region of the Reel frame at `art_t` that holds the art
  (usually around `[40, 1000, 1000, 800]`). It is rendered by `templates/thumb.html` and becomes the Reel's first
  frame, which Instagram uses as the cover.

### 4B. Reel: scenes → `reel.html`
Copy `otlo/toolkit/templates/reel-skeleton.html`. One `.scene` per script line, same order. Keep the END CARD
and set its "Next:" text. Brand classes (`.chip .gu .en .kick .body .box .art`) and colours (ivory #F3E9D6,
indigo #1B2A4A, red #A8322A, haldi #E3A21A, rani #C2185B sparingly, leaf #3C7A3A for art only). Each scene:
Gujarati headline + English headline + optional short body + SVG art of the real subject. Keep the bottom 260 px
free (subtitles). Quality bar: `otlo/toolkit/examples/2026-11-21-tulsi-vivah/`.

### 4B-chat. DISCONTINUED (Saumya, 28 Nov 2026)
**No chat-style Reels, WhatsApp/message-exchange formats or artificial conversations, in any slot, as a backup or
in the weekly plan.** `bin/chat_reel.py` stays in the repo only so old work dirs can be rebuilt. Relatable humour is
done as narrated observational Reels instead.

### 4B-doc. Documentary look (default for facts, history, cinema, food origins, places)
`<body class="doc">` + `runtime/doc.css`: real photographs full-bleed (`<div class="docbg"><img class="kb" src="img/<id>.jpg"></div>`,
`.shade`, `.grain`), gold kicker, white Gujarati headline, gold English line, GSAP motion (kinetic words, count-ups,
timelines, stamps) and Three.js where it earns it (3D poster card, card flip). Images from `script.json` `images`:
official artwork first, then Commons photos, then photoreal AI (`"source":"ai","style":"photo"`) only for scenes no
photograph shows, **always labelled on screen** ("Illustrative reconstruction (AI)") and in the caption. Lemo
Opuscar styles (`setup_extras.sh lemo`; dark-documentary, archive-lighttable, map-explainer, newsreel) are the
visual-grammar reference. Examples: `otlo/work/2026-11-28-1230-rani-ki-vav-note/`, `otlo/work/2026-11-28-1930-manthan-farmers/`.
Fast path: queue `"<dir> assets"` (cloud fetches images + voice), pull, then render in the session with
`python3 otlo/toolkit/bin/build.py render <dir>` and commit the outputs.

### 4C. Carousel ideas → multi-scene explainer Reels (Saumya, 28 Nov: no static carousels)
Carousel concepts (lists, comparisons, cheat sheets, rankings, watchlists) are now built as **animated
explainer Reels with 4A/4B** (`reel.html`), not as slides: one scene per item, each with a strong visual (poster,
photo, illustration), kinetic type, a count/number or stamp, and a transition. Keep the carousel's save-value:
the second-to-last scene is the summary people screenshot; the last is one ask. 25–40 s; if a list has more
than 6 items, cut it to the best 5 or split it into two Reels on different days. The old swipe-style path below
stays only for emergencies (a build failure an hour before the slot).

(Old path, emergencies only.) Carousel slot → swipe-style Reel (`carousel.html` + `script.json`):
- `carousel.html` from `otlo/toolkit/templates/carousel-skeleton.html`: 6–9 slides, 1080×1350:
  cover (hook + big bilingual title + subject art; it is also the Reel's cover, so design it as the thumbnail)
  → one idea per slide (number, Gujarati + English headline, 1–2 short lines, art) → second-to-last: the summary
  people screenshot → last: one ask + follow. Every slide bilingual. Save-worthy: cheat sheet, comparison, map,
  word list, checklist or results.
- `script.json`: **one voice line per slide**, same order (same format as 4A, no `thumb` needed), 40–110
  Gujarati characters each, the last line ending "ઓટલોને ફોલો કરો." Subtitles `en` as in 4A.
- The builder shows each slide on the branded stage with a slow push-in and a slide-in between slides,
  timed to the voice, with subtitles under the slide.

### 5. Build (GitHub Actions does voice + render + export)
```
echo "otlo/work/<dir>" > otlo/toolkit/queue.txt
git add -A otlo && git commit -m "Otlo: <date> <slot> <slug>" && git pull --rebase && git push
```
Poll every 30 s (`git pull`) for up to 25 min until `otlo/work/<dir>/build.log` has `BUILD OK` or
`BUILD FAILED` / `NO_KEY` / `VOICE FAILED`. (If the push did not change queue.txt, start the run with
`gh api -X POST repos/saumyadshah/sutraverse-reels/actions/workflows/otlo-build.yml/dispatches -f ref=main`.)

Export settings are fixed in `bin/build.py` (do not lower them): Reels 1080×1920, 30 fps, H.264 High 4.2,
12 Mb/s CBR, BT.709, AAC 256 kb/s 48 kHz, −14 LUFS, lossless PNG frames, thumbnail as first frame.
Swipe-style Reels: same video settings; slides rendered 1080×1350 lossless.

### 6. Review (must pass all)
- Read `contact.jpg` (and for Reels `thumb.jpg`) with the Read tool: text fits, nothing overlaps, Gujarati
  renders, art matches the subject, subtitles sit under the art, the thumbnail reads at a glance.
- `qa.json`: `ok` true, no `warnings` (this includes the safe-zone and length checks). Reels: 1080×1920,
  bit_rate ≥ 10,000,000, lufs ≈ −14, 15–40 s.
- Read `contact_safezones.jpg`: nothing important under the red (Instagram UI) zones; the hook readable inside the
  blue 3:4 frame. Read `thumb.jpg`: subject + 2–3 big words readable at phone-grid size.
- Watch the hook: frame two must already show the hook text; the voice starts within 0.2 s.
- A chars/sec warning means the voice may have read something extra or cut off: delete `vo/*.wav`, fix the
  line, re-queue. Layout problems: fix the HTML, re-queue (voice is reused).
- At most 2 rebuilds. Still failing → row `Skipped`, log, stop.

### 7. Caption → `caption.txt` (≤ 2,200 characters) — the Otlo formula v3 (28 Nov)
- **Line 1 is a second hook**, not a summary: a number, a contradiction or a question the video raises but the
  first line doesn't answer. It must make "…more" worth tapping.
- **Context, not a transcript**: 2–3 lines that add what the Reel couldn't (a date, a name, a "why"), never a
  retelling of every scene.
- **One specific, natural ask** that fits this post (vary them: a one-word answer, "tag the friend who…",
  "send it to your family group", "save it for Sunday"), never the same CTA two posts in a row, never "like and
  share", never desperate.
- **Credits**: sources; official artwork credit; "Not sponsored" when the subject could look promotional; the
  paid-partnership line first when it is one.
- **Tags**: first check `otlo/handles.md` (handles Saumya supplied; treat as verified, never guess one). For films/events/businesses, list the official handles to tag in the ready file (verified with
  `vidiq_ig_profile`, or seen tagged on the official account's own posts) and @mention one or two in the caption
  where natural (the studio, the director).
- `[keywords]`: 8–12 real search phrases, English + Gujarati script, comma-separated, in square brackets.
- **Exactly 5 hashtags**, all about this subject.
Built from the reference accounts (Dukaan Didi, Balakheji, Manka Daily): a one-line hook above the fold, a
two-to-three-line mini story with the "why", one takeaway, one specific ask, sources inline.
```
<Gujarati hook, ≤ 70 chars, the same idea as the video's first line> <one emoji at most>
<English hook, ≤ 90 chars: a paradox, felt question or reveal>

<2–3 short English lines: what happened / why it matters, with one concrete detail (date, place, number)>
<1 Gujarati line summing it up>

<Specific ask in Gujarati + English: comment a word / "save it for <day>" / "send it to <who>">

Sources: <outlets>. <any "check locally" caveat>
Illustration and voice: Otlo.            (same for swipe-style Reels)
Follow @otlo.gujarat · ગુજરાતની વાતો, ઓટલા પર

[<8–12 SEO keywords and phrases, comma-separated: topic + year, English and Gujarati spellings, related searches>]

#<EXACTLY 5 hashtags: 2 topic (one may be Gujarati script), 1 niche (#GujaratiCulture / #GujaratiFood / #GujaratiCinema / #GujaratiFestivals), 1 audience/reach (e.g. #Gujarati, #Gujarat, #Amdavad), and always #Otlo>
```
**Exactly 5 hashtags on every post (Saumya's rule), never more, never fewer.** No walls of text, no more than two emojis, no unrelated trending tags. Carousels: the ask
is usually "Save it" or "Send it to the family group".

### 8-PREP. Ready it and send the content email (PREP runs)
- **Already readied in advance** (the slot's row is `Ready` and `otlo/ready/<date>-<HHMM>.json` exists, e.g. made
  in chat): don't make a new post. Pull, open the files, re-check QA, `thumb.jpg` and `contact_safezones.jpg`, and that
  the topic is still current, then send the email package below for it.
- Write `otlo/ready/<YYYY-MM-DD>-<HHMM>.json`: `{"dir": "otlo/work/<dir>", "time": "<YYYY-MM-DD>T<HH:MM>+05:30",
  "caption_file": "otlo/work/<dir>/caption.txt", "row": <calendar row>}`; set the calendar Status to `Ready`;
  commit and push.
- If QA failed after 2 rebuilds: make the backup (rule 9) instead; if that also fails, write no ready file and say so.
- **Your final reply is emailed to Saumya.** Make it exactly this package (plain text, no tool chatter):
  `OTLO READY: <title> · <date> <time> IST`
  1. Final Reel: https://raw.githubusercontent.com/saumyadshah/sutraverse-reels/main/otlo/work/<dir>/reel.mp4
  2. Thumbnail / cover: https://raw.githubusercontent.com/saumyadshah/sutraverse-reels/main/otlo/work/<dir>/thumb.jpg
  3. Caption: the full caption text, including the [keywords] block and the 5 hashtags
  4. Scheduled: <date>, <time> IST, Instagram @otlo.gujarat
  5. Concept and objective: 2–3 lines (the idea, the hook, the action it aims for: share / save / comment)
  6. Quality check: hook, voice, subtitles, safe zones (9:16 and 3:4), thumbnail, caption, export: passed (list
     anything not perfect)

### 8-PUBLISH. Publish the readied post (PUBLISH runs)
- First, recovery: for any `otlo/ready/*.json` of the last 2 days with a `container` but no `permalink`, call
  `vidiq_instagram_publish_reel` with that `containerId` and account until `PUBLISHED` (this continues the same
  post; it is not a retry), then record it.
- Then this slot: read `otlo/ready/<today>-<HHMM>.json`. Missing → log "NOT READY", set the row `Skipped`, stop.
  Already has a `permalink` → stop.
- Wait until the slot time, then `vidiq_video_upload` with the raw URL of `reel.mp4`, then
  `vidiq_instagram_publish_reel` (account `29167885212872260`, that videoUrl, the caption from `caption_file`).
  **Write the returned `containerId` into the ready file and push before continuing.** Continue with the
  containerId every ~10 s until `PUBLISHED`; write `permalink` into the ready file. Stop on errors; never start a
  second container for the same post. If access expired, log "RECONNECT NEEDED".

### 9. Record (PUBLISH runs; PREP runs record Ready)
- Calendar: Status → `Posted` (or `Skipped`), and append the permalink (or the reason) to column G.
- Append to `otlo/logs/<YYYY-MM-DD>.md`: slot, row, POSTED/SKIPPED, permalink, sources, QA numbers, anything odd.
- Empty `otlo/toolkit/queue.txt`; commit and push (`git pull --rebase` first).
- Finish with one line: what was posted (with link) or why not.

## Reference patterns (studied 21 Nov 2026)
- **Dukaan Didi** (143K): caption opens with a paradox question ("Bestseller pe zero profit?"), then a named
  person + the money detail, then the named concept, then "Follow @…". Brand hashtag first.
- **Balakheji** (172K): opens with a felt question the viewer has lived ("Kabhi yeh kehte-kehte…?"), then the
  small family moment in two lines, then one gentle truth.
- **Manka Daily** (85.5K): opens with a challenge or exact promise ("Your whole Lakshmi Puja, in 12 steps. Save
  it for Sunday evening."), gives exact dates/times and named sources in the caption, ends with
  "comment your question" or "send this to…". Its save-worthy step-by-step posts get the most comments.

## Feedback loop (every PREP run)
Before writing, read the last 3 published posts' insights (`vidiq_instagram_owner_insights` with their media ids:
free): skip rate, average watched %, watch time, shares, saves, comments. Append one line per post to
`otlo/insights.md` (date, title, format, hook type, length, skip %, watched %, shares/saves/comments) and one
lesson. Apply it: repeat hook types and formats that beat the running average; drop ones that trail it.
