# Otlo runbook: one post per run

Otlo (ઓટલો, Instagram **@otlo.gujarat**) is Saumya's faceless Gujarati culture, food and cinema brand.
Posts: Reels (Gujarati voice-over, English subtitles, bilingual on-screen text) and carousel slots
(bilingual slides, posted as voiced swipe-style Reels), all in the "Kankotri Press" style. Scheduled runs follow this file **exactly**, work unattended and ask
nothing. Each run handles **one slot**: the calendar row whose Date is today (Asia/Kolkata) and whose
Time (IST) is the run's slot (`13:00` = midday run, `19:30` = evening run).

## Posting pattern (set by Saumya, 21 Nov 2026; weekends added the same day)

**Every day, weekends included.** Days alternate, continuing day by day without a break:
- **A day:** 1 carousel slot at 13:00 (posted as a swipe-style Reel) + 1 Reel at 19:30
- **B day:** 1 Reel at 13:00 + 1 Reel at 19:30

(Sat 21 Nov = A, Sun 22 = B, Mon 23 = A, …) The calendar holds one week at a time (next Mon–Sun); it is planned
every Saturday by `otlo/PLANNING.md` (backlog in the `Idea bank` sheet). Carousel slots complement the Reels
(a save-worthy cheat sheet, a map, a word list, poll results), never the same content restated. Weekend topics
lean lighter (food, family, language, weekend watchlists) unless a festival falls on the day.

## Fixed IDs

| What | Value |
|---|---|
| Repo | `saumyadshah/sutraverse-reels` (public), branch `main` |
| Content calendar (Claude Sheet) | artifact `e89bed33-8969-476f-9b60-09a18065bbb3`, workbook node `3d2daa40-bf99`, sheet `Calendar` |
| Calendar columns | A Date · B Day · C Time (IST) · D Format (Reel / Carousel) · E Series · F Topic · G Notes and sources to check · H Status (Idea / To make / Ready / Posted / Skipped) |
| Strategy doc | https://claude.ai/artifact/LCvcv5vPVocJuHEjeKDrU9 |
| Instagram (vidIQ) | platformAccountId `29167885212872260` (username otlo.gujarat) |
| Voice | Gemini TTS voice `Kore`, `direction` always `""` (any instruction text gets read aloud) |

Sheets calls: `read`/`update` with `ref={"object":"node","id":"3d2daa40-bf99"}`,
`container={"kind":"project","id":"e89bed33-8969-476f-9b60-09a18065bbb3"}`, `engine="workbook"`.
Read `{"kind":"readCells","sheet":"Calendar","range":"A1:H120"}`. Write
`{"kind":"applyEdits","base":<revision>,"edits":[{"kind":"writeCells","sheet":"Calendar","topLeft":"G<row>","rows":[["<notes>","Posted"]]}]}`
(call the Docs `guide` with `topic.sheets` first if unsure).

## Hard rules (never break)

1. **One post per run, only this slot's row.** If there is no row for today + this slot, or its Status is
   `Posted`/`Skipped`, or `otlo/logs/<today>.md` already records this slot as POSTED, stop and log why.
2. **Facts.** Every factual claim (dates, tithis, history, numbers, release dates, box office) needs two
   independent reliable sources found today with WebSearch/WebFetch (start from column G). Drop any claim you
   cannot confirm. If the topic's core cannot be confirmed, mark the row `Skipped` with the reason and post nothing.
   Religious practice is described as belief/tradition ("it is believed", "many families"), never as fact or advice.
3. **Cinema.** No film clips, stills, posters, trailers, logos or actors' faces, ever. *Loko Shu Kahe Chhe?*
   reports what named critics and audiences said (attributed); Otlo gives **no verdict of its own**. Box office
   numbers only with a named source, labelled "reported"/"estimated".
4. **People and communities.** No real private individuals. No caste, communal, political or religious
   ridicule; no stereotypes beyond gentle, affectionate food rivalry. *Family Group Chat* is original comedy with
   invented characters (Ba, Mummy, Pappa, Fai, the NRI cousin).
5. **Copyright.** No song lyrics, film dialogue, or third-party images/audio. All art is our own inline SVG.
6. **Images must match the subject.** Khaman must look like khaman, a kite like a kite. Draw it carefully.
7. **No sponsored content, no paid links, no replies/DMs, no deleting posts.**
8. **Mandatory for every post: highest-quality export, a designed thumbnail/cover, the full caption formula
   (with the [keywords] block and exactly 5 hashtags), and the skills listed below.** A post missing any of these is not posted.
9. **When in doubt, skip.** A skipped slot is fine; a wrong or offensive post is not. Always log the reason.

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
- Natural, warm, spoken Gujarati, 60–160 characters per line; about 35–55 s in total.
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

### 4C. Carousel slot → swipe-style Reel (`carousel.html` + `script.json`)
Saumya's choice (21 Nov): carousel slots are posted as **swipe-style Reels** (vidIQ needs a manual approval
for true carousels, so those never run unattended). Make the slides exactly as a carousel, then voice them:
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
- `qa.json`: `ok` true, no `warnings`. Reels: 1080×1920, bit_rate ≥ 10,000,000, lufs ≈ −14, 15–90 s.
- A chars/sec warning means the voice may have read something extra or cut off: delete `vo/*.wav`, fix the
  line, re-queue. Layout problems: fix the HTML, re-queue (voice is reused).
- At most 2 rebuilds. Still failing → row `Skipped`, log, stop.

### 7. Caption → `caption.txt` (≤ 2,200 characters) — the Otlo formula
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

### 8. Post
- Before posting, `vidiq_social_post_list` (today) and the log: make sure this slot was not already posted.
- If the slot time (IST) is still ahead, wait until then; if it has passed, post now.
- **Reel:** `vidiq_video_upload` with
  `url=https://raw.githubusercontent.com/saumyadshah/sutraverse-reels/main/otlo/work/<dir>/reel.mp4`, then
  `vidiq_instagram_publish_reel` (platformAccountId `29167885212872260`, that videoUrl, the caption; no trial,
  no AI label unless Saumya asks). Continue with containerId every ~10 s until `PUBLISHED`.
- **Carousel slot:** it is a swipe-style Reel, so post it exactly like a Reel (above).
- Stop on errors; never retry a failed publish. If access expired, log "RECONNECT NEEDED".

### 9. Record
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
