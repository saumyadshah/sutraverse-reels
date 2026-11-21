# Otlo weekly planning

Every **Saturday** a scheduled run plans the **next Mon–Fri** (10 posts) so the content follows what is
actually happening: festivals, Friday film releases, reviews, box office, OTT drops, weather, news in Gujarat,
and what worked on @otlo.gujarat last week. It plans only; it never posts. Work unattended, ask nothing.
Same IDs as `otlo/RUNBOOK.md` (sheet `Calendar` + sheet `Idea bank` in the Otlo Content Calendar).

## Pattern (fixed)
Mon–Fri only. Days alternate **A** (Carousel 13:00 + Reel 19:30) and **B** (Reel 13:00 + Reel 19:30).
The alternation runs across weekends: next Monday's type is the **opposite of last Friday's**
(read last Friday's two rows: a Carousel there = A, so Monday = B). 5 days → 10 rows.

## Steps
1. **Repo + sheets.** Pull the repo. Read `Calendar!A1:H120` and `Idea bank!A1:F200`.
2. **Look back (last Mon–Fri).** For each posted row get the permalink from column G and, if available for free,
   reach/saves/comments from `vidiq_instagram_owner_insights` (account `29167885212872260`). Note the top 2 and the
   bottom 2 posts and why (topic, hook, format). Note skipped rows and their reasons.
3. **Look ahead (next Mon–Sun).** WebSearch, two sources each:
   - festivals/tithis and observances (Drik Panchang), Gujarat events (Gujarat Tourism, AMC, district pages);
   - Gujarati film releases this Friday and last Friday; reviews and reported box office of recent releases;
     Gujarati titles new on OTT; Hindi releases with a real Gujarati link;
   - seasonal food, weather and Gujarat culture stories people are discussing (no politics, no crime).
4. **Pick 10 posts.** Priority: (a) dated, timely topics (festival on its day or the day before; reception
   Reels 3–4 days after a release; Monday box office); (b) results/poll follow-ups owed from last week;
   (c) best-fit Idea bank rows; (d) fresh evergreen ideas. Rules:
   - balance pillars across the week: culture/festivals, food, cinema (at least 3 cinema posts), language/humour;
   - no series twice on the same day; no more than 2 of one series a week (Utsav Guide may go to 3 in a festival week);
   - each carousel complements a Reel that day or the next (cheat sheet, comparison, map, word list, results),
     never the same content restated;
   - lean towards what worked last week; drop or rework what flopped;
   - every row needs a column-G note naming the sources to check.
5. **Write the Calendar.** If next week already has rows (e.g. planned earlier in chat), do **not** append a
   second set: keep its 10 rows and only update a row's Topic/Notes in place where you found a clearly more
   timely or better-sourced topic for the same slot and format (log what changed and why). Otherwise: Delete rows of weeks that are fully past **only after** confirming they are
   `Posted`/`Skipped` (never delete a `To make` row from the current or a future week). Append the 10 new rows
   (`Date`, `=TEXT(A<n>,"ddd")`, `13:00`/`19:30`, Format, Series, Topic, Notes, `To make`) in date and time order.
   Format and Status cells use the existing dropdown labels exactly.
6. **Update the Idea bank.** Set Status `Used <date>` on rows you used; add 5–10 new ideas you found
   (Suggested date if time-bound), Status `Unused`. Mark stale time-bound ideas `Expired`.
7. **Plan note.** Write `otlo/plans/<monday-date>.md`: last week's top/bottom posts and lessons, the 10 rows with
   one line of reasoning each, key dates found, and anything Saumya should know (e.g. a sensitive topic skipped).
   Commit and push.
8. Finish with one line: the week planned (dates) and its three headline posts.
