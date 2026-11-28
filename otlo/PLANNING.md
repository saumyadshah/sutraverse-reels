# Otlo weekly planning

Every **Saturday** a scheduled run plans the **next Mon–Sun** (14 posts) so the content follows what is
actually happening: festivals, Friday film releases, reviews, box office, OTT drops, weather, news in Gujarat,
and what worked on @otlo.gujarat last week. It plans only; it never posts. Work unattended, ask nothing.
Same IDs as `otlo/RUNBOOK.md` (sheet `Calendar` + sheet `Idea bank` in the Otlo Content Calendar).

## Pattern (fixed)
Every day, weekends included. Days alternate **A** (Carousel slot 10:00, posted as a swipe-style Reel + Reel 19:30)
and **B** (Reel 10:00 + Reel 19:30), continuing day by day: next Monday's type is the **opposite of this
Sunday's** (Sunday has a Carousel row = A, so Monday = B). 7 days → 14 rows. This week's Saturday and Sunday were
planned last Saturday, so the plan always runs Monday to Sunday. Weekend posts lean lighter (food, family,
language, weekend watchlists) unless a festival falls on the day.

## Skills to use
`anthropic-skills:content-calendar`, `anthropic-skills:series-planner`, `anthropic-skills:content-pillar-builder`,
`anthropic-skills:trend-spotter`, `anthropic-skills:analytics-readout` / `anthropic-skills:social-analytics-report`
(look back), `anthropic-skills:content-audit` (every 4th week), `anthropic-skills:comment-mining` (ideas from
comments), `anthropic-skills:best-time-scheduler` (only to flag if 13:00/19:30 should move; never change the
pattern without Saumya), `anthropic-skills:content-research` / `anthropic-skills:competitor-teardown` /
`anthropic-skills:viral-carousel` (paid vidIQ calls: at most 15 credits a week, check `vidiq_balance` first).
Same exclusions and rule precedence as the RUNBOOK. Note in the plan which skills were used.

## Steps
1. **Repo + sheets.** Pull the repo. Read `Calendar!A1:H120` and `Idea bank!A1:F200`.
2. **Look back (last Mon–Sun).** For each posted row get the permalink from column G and, if available for free,
   reach/saves/comments from `vidiq_instagram_owner_insights` (account `29167885212872260`). Note the top 2 and the
   bottom 2 posts and why (topic, hook, format). Note skipped rows and their reasons.
3. **Look ahead (next Mon–Sun).** WebSearch, two sources each:
   - festivals/tithis and observances (Drik Panchang), Gujarat events (Gujarat Tourism, AMC, district pages);
   - Gujarati film releases this Friday and last Friday; reviews and reported box office of recent releases;
     Gujarati titles new on OTT; Hindi releases with a real Gujarati link;
   - seasonal food, weather and Gujarat culture stories people are discussing (no politics, no crime).
4. **Pick 14 posts.** Priority: (a) dated, timely topics (festival on its day or the day before; reception
   Reels 3–4 days after a release; Monday box office); (b) results/poll follow-ups owed from last week;
   (c) best-fit Idea bank rows; (d) fresh evergreen ideas. Rules:
   - balance pillars across the week: culture/festivals, food, cinema (at least 3 cinema posts), language/humour;
   - no series twice on the same day; no more than 2 of one series a week (Utsav Guide may go to 3 in a festival week);
   - each carousel complements a Reel that day or the next (cheat sheet, comparison, map, word list, results),
     never the same content restated;
   - lean towards what worked last week; drop or rework what flopped;
   - every row needs a column-G note naming the sources to check.
5. **Write the Calendar.** If next week already has rows (e.g. planned earlier in chat), do **not** append a
   second set: keep its rows and only update a row's Topic/Notes in place where you found a clearly more
   timely or better-sourced topic for the same slot and format (log what changed and why). Otherwise: Delete rows of weeks that are fully past **only after** confirming they are
   `Posted`/`Skipped` (never delete a `To make` row from the current or a future week). Append the 14 new rows
   (`Date`, `=TEXT(A<n>,"ddd")`, `10:00`/`19:30`, Format, Series, Topic, Notes, `To make`) in date and time order.
   Format and Status cells use the existing dropdown labels exactly.
6. **Update the Idea bank.** Set Status `Used <date>` on rows you used; add 5–10 new ideas you found
   (Suggested date if time-bound), Status `Unused`. Mark stale time-bound ideas `Expired`.
7. **Plan note.** Write `otlo/plans/<monday-date>.md`: last week's top/bottom posts and lessons, the 14 rows with
   one line of reasoning each, key dates found, and anything Saumya should know (e.g. a sensitive topic skipped).
   Commit and push.
8. Finish with one line: the week planned (dates) and its three headline posts.

## Added 26 Nov (overhaul)
- **Source pre-check:** before a fact-based topic enters the calendar, confirm today that at least two usable
  sources exist (search them, note the URLs in column G). Three evening topics were skipped in the week of
  23 Nov because sources did not exist (e.g. reviews of a film released 3 days earlier). Reception Reels go in
  only once at least two named reviews exist.
- **Formats:** follow the "Creative standard v2" in RUNBOOK.md and the test plan in the audit doc
  (https://claude.ai/artifact/YMP1dotTv6rbaEGPfx5aXJ): each week include at least 2 city-rivalry posts, 2 "you've
  eaten it all your life, but…" posts, 2 Family Group Chat v2 posts, 2 save-it lists (carousel slots) and 1 Gujlish
  word; no format more than 3 times a week; no two chat Reels on the same day.
- **Weekly report (your final reply is emailed to Saumya):** start with `OTLO WEEKLY REPORT: <dates>`; then a table of
  every post of the past week (title, format, plays, skip %, watched %, shares, saves, comments, follows), the 3
  lessons, the change in followers, the week's 14 planned posts (date, time, format, topic) and the 2 formats
  being tested. Also save it as `otlo/plans/<monday>-report.md`.

## Added 28 Nov (Saumya's brief: complete content strategy overhaul). This section wins over older lines above.
**Pattern change:** no static carousel slots. Both daily slots (10:00 and 19:30) are Reels; carousel ideas become
multi-scene explainer Reels (RUNBOOK 4C). **Mix rule:** every day has ≥ 1 *timely* post (release, number,
announcement, anniversary this week, upcoming event, festival, weather); every week ≥ 4 entertainment/cinema
posts (Gujarati first, Bollywood with a Gujarat/Gujarati angle), ≥ 2 events, ≥ 2 food/discoveries, 0 chat Reels (discontinued 28 Nov), ≥ 1 business/creator feature format (see below), ≥ 1 curiosity explainer (the Pol-maze pattern).

### Daily research routine (runs inside every PREP run, ~10 minutes, before writing)
1. **Entertainment now:** WebSearch for this week's Gujarati releases and announcements ("Gujarati film
   trailer", "Gujarati film release date announced", Sacnilk Gujarati box office, the 2026 Gujarati films list
   on Wikipedia), Bollywood headlines of the day, OTT drops this Friday.
2. **Official accounts:** for any film/event chosen, find its official Instagram/X handles and official artwork
   (production house, distributor, District/BookMyShow page) and record them in the ready file.
3. **Events:** District, ahmedabad2go, eventsaroundme, AMC and Gujarat Tourism listings for the next 14 days.
4. **Food and city:** new openings, seasonal dishes (winter: undhiyu, adadiya, chikki; Uttarayan in January),
   viral food spots in Ahmedabad, Surat, Vadodara and Rajkot (two sources; never invent a review).
5. **What audiences respond to:** free vidIQ `vidiq_instagram_owner_insights` for our posts. Paid tools
   (`vidiq_instagram_tiktok_outlier_search`, `vidiq_ig_profile_reels` of Gujarati pages) only in the weekly plan,
   ≤ 15 credits a week. Take the **format** that works, never the content.
6. Log the 3 best opportunities found (with sources) in `otlo/logs/<date>.md` even if not used today; add them
   to the Idea bank.

### Series bible (recurring, named, recognisable; each has its own chip colour and hook shape)
| Series | Pillar | Promise / format | Hook shape | Visuals |
|---|---|---|---|---|
| **Loko Shu Kahe Chhe?** (લોકો શું કહે છે?) | Cinema | What critics, filmmakers and audiences said about a film this week, attributed | a named person + a strong word | official poster (3D card), quote cards, stamps |
| **Box Office no Hisaab** (બોક્સ ઓફિસનો હિસાબ) | Cinema | One number story: budget vs collection, a record, a turnaround | "₹X → ₹Y" | count-ups, growing bars, poster |
| **Friday ni Film** (શુક્રવારની ફિલ્મ) | Cinema/OTT | What's releasing this Friday in Gujarati (+ 1 Hindi) and on OTT | "This Friday: N films, one surprise" | official posters, Ken Burns, stamps |
| **Amdavad ma Aa Weekend** (આ વીકએન્ડ ક્યાં?) | Events | 4–5 verified events this weekend/fortnight: date, venue, price | "N plans for this weekend" | official event artwork, map pins, dates |
| **Swad ni Shodh** (સ્વાદની શોધ) | Food/discoveries | A dish, street-food spot or new opening, with its story | a price, an age, a secret | licensed photos / AniDoodle food art |
| **Ae Kem?** (એ કેમ?) | Culture explainer | "That's not a mistake, it's design": why something Gujarati is the way it is | a paradox | AniDoodle illustration, 3D, maps |
| **Aapde Aavā J Chhie** (આપણે આવા જ છીએ) | Relatable observation | Narrated observational humour about Gujarati habits (no chat format) | a universal habit, named | documentary/illustration, kinetic type |
| **Gujlish Shabdkosh** | Language | One word/phrase, how people really use it, a funny example | "You say it daily, but…" | kinetic type |
| **Otlo Spotlight** | Promotional showcase | A local business, artist, creator or film team, told as a story | the founder's moment/number | their footage/photos (video-effects), credited |

### Collaboration formats (make Otlo the page businesses want to be on)
- **Otlo Spotlight** (above) is the showcase: a 25–35 s story Reel about one business/artist/project. Until
  paid deals exist, pick genuinely notable subjects (verified with two sources), label it "Not sponsored", and
  tag the business. It shows prospective partners what a feature looks like.
- **Event highlights** (Amdavad ma Aa Weekend) and **Friday ni Film** show event organisers and producers the
  promotional value without being ads.
- **Collaboration CTA** (at most once a week, at the end of a Spotlight or an events Reel, never on comedy):
  "Restaurant, event, film or brand? Feature with Otlo: DM 'FEATURE'" (EN) / "તમારો બિઝનેસ, ઇવેન્ટ કે ફિલ્મ
  ઓટલા પર લાવવી છે? 'FEATURE' DM કરો". Saumya handles DMs personally; runs never reply or DM.
- **Paid posts** follow RUNBOOK hard rule 7 (Saumya confirms; disclosed; paid-partnership label).
- The weekly plan proposes 1 potential partner a week to Saumya (a business/film/event that fits a series), with
  why it fits; it never contacts anyone.

## Added 28 Nov, second brief ("Complete Content Strategy Overhaul, Weekly Planning and Immediate Reel Production")
This section wins over everything above.
- **No chat Reels, ever.** Formats: cinematic storytelling, documentary explainers, unknown facts, movie and
  entertainment stories, historical timelines and visual breakdowns, comparisons, relatable narrated observation,
  short news and event explainers.
- **Weekly, not monthly.** Every Saturday the plan covers next Mon–Sun, 2 Reels a day (10:00, 19:30). Prepare ahead,
  keep 2 reserve concepts, and swap in breaking entertainment news or events when they are genuinely bigger.
- **Each planned Reel is a full package** in `otlo/plans/<monday>.md` (and a short form in the Calendar row): specific
  topic and creative concept; the exact hook; the complete Gujarati voice-over script with English subtitles; the
  duration; scene-by-scene visual direction (which real images/official artwork/AI reconstructions, which motion);
  research sources with URLs; editing and motion plan (GSAP/Three.js/Manim/Remotion/Lemo style); the complete caption;
  verified Instagram tags (checked with `vidiq_ig_profile` or seen tagged on the official account); [keywords];
  hashtags; CTA; publishing time. PREP runs then build exactly that package (re-verifying facts the same day).
- **Look back first:** before planning, read last week's insights (plays, skip %, watched %, shares, saves, comments,
  follows) and write what to repeat and what to drop.
- **Topic test (all six must have answers):** What is happening? Why should the audience care? What is the most
  unexpected angle? What will viewers learn that they didn't know? What is the visual storytelling opportunity?
  Why would someone share, save or comment?
- **Quality review (answer in the ready file; any "no" → improve or replace before scheduling):** interesting and
  original? Hook stops the scroll? Reveals something surprising/informative/entertaining/relatable? Script concise?
  Images realistic and relevant? Motion professional and appropriate? Voice natural and consistent? Subtitles in safe
  zones? Correct in 9:16 and 3:4? Thumbnail appealing? Caption structured? Handles verified and relevant? Facts,
  sources and copyright checked? Would someone genuinely share it?
