# Shlokwise comment & engagement playbook (2.0, 7 Nov 2026; first written v4, 30 Oct)

**Brand (13 Nov):** we are Shlokwise, "Getting wise with Shlok" (toolkit/BRAND.json); never write "SutraVerse" in a reply. **2.0 update:** the channel covers ancient strategy and modern psychology (STANDARDS_2.md). Replies may use only the facts stored on the Reel's board slot: its `sources`/verse, `named_idea`, `series`, `tag`, `topic` and `real_life_angle`. Psychology claims stay at the level of the named study/concept in that slot; never give therapy, legal, medical or money advice, and never present a 'dark psychology' trick as a how-to.

Goal: every real comment gets a warm, specific, human reply within ~12 hours, which tells the algorithms the post sparks conversation and turns viewers into followers. Never spam, never argue, never sound like a bot.

## What runs automatically

**YouTube Shorts (@sutraversehindu), fully automatic.** The "SutraVerse comment replies" scheduled task runs twice a day (11:20 and 19:20 IST). It uses `toolkit/yt_comments.py`, the free YouTube Data API and the channel's own keys:
1. `python3 toolkit/yt_comments.py --list --days 3` lists comments the channel hasn't answered yet.
2. Each comment is classified using the rules below. Replies are written fresh for each comment, and each one is posted with `--reply`. The script re-checks live first, so it never replies twice.
3. Every action is logged on the board (`comment_log`). Anything that needs a human goes to Saumya in one message.

**Instagram (@sutraverselife): Saumya turns this on once in Meta's free tools.** The vidIQ connection can publish and read insights, but Instagram doesn't let it reply to comments. That needs Meta's own comment permission. Free route, about 10 minutes in Meta Business Suite on desktop (business.facebook.com → Inbox → Automations):
- **Comment to message, one keyword per series (2.0):** RULE (Chanakya Files: "Here's the full rule, its source and the move to use tomorrow"), FILE (Mind Games: "Here's the study behind it and how to spot it"), EP (Office Shastra / Ghar Ki Baat: "Here's the Option C script for your own situation"), YEAR (Turning Points: "Here's the timeline and sources"), FABLE (Panchatantra Reloaded: "Here's the original fable and its lesson"). Each DM ends: "Reply with your own story; we read every one." A caption may then say "Comment RULE and I'll send you the full rule".
- **Custom keywords** (Instagram allows up to 5): use the five above.
- **FAQs** (Instagram app → Messages → Tools → Frequently asked questions, up to 4): "Where are these verses from?", "Is this from the original scripture?", "Which Reel should I watch first?", "Can I suggest a story?". Answers are in the FAQ section below.
- **Public comment replies on Instagram** stay with Saumya, or a Meta-approved tool if she later adds one (ManyChat's free plan is only 25 contacts a month and adds "Powered by ManyChat"). Each day the weekly review and the comment task send her 3 suggested replies to the best Instagram comments, so this takes her about 2 minutes.

## Reply rules (both platforms)

Reply automatically:
- **Personal stories** ("same happened to me at work"): empathise in one line, link it to the Reel's lesson, ask one gentle follow-up question.
- **Praise:** thank them specifically (mention what they liked), plus one line of value or a question. Never just "Thanks!".
- **Factual questions about the verse, rule, study or story:** answer only from the verified slot data on the board (sources, named idea, translation, text vs tradition, study author/year). Never invent a verse, quote, study or number; if the slot doesn't hold the answer, say you'll check and list it for Saumya.
- **Topic requests** ("make one on Karna's death"): thank them and say we've noted it. Add the idea to the board's backlog with the commenter's words.

Never reply automatically (send these to Saumya in the summary instead):
- religious or political debate, caste, communal or hateful remarks, anything about a real named person;
- complaints, accusations of error, legal or medical questions, anything about money or offers;
- spam, links or self-promotion (leave them; Saumya can hide them in Studio).

Style:
- 1–3 short sentences, under 300 characters. English or Hinglish, matching the commenter. Warm, specific, never preachy.
- Use the commenter's own words back to them once. At most one emoji (🙏 or 🪔).
- No links, no @mentions, no "follow for more", no hashtags, no copy-paste: no two replies in a run may share a sentence.
- At most 25 replies per run and 1 reply per thread. Never reply to our own comments.

## FAQ answers (Instagram FAQs, keywords and YouTube)
- **Where is this from?** "Every Reel names its source on screen and in the caption: the text with chapter and verse (checked against two editions), or the study's authors and year. Anything from later tradition is labelled 'Tradition holds…', and paraphrases say 'Paraphrase'."
- **Is this from the original scripture?** "The verse is original. The modern story is an illustrative scene, and when something comes from later tradition rather than the text, we label it 'Tradition holds…'."
- **Which Reel should I watch first?** "Start with the series that fits your life: Office Shastra (work), Mind Games (psychology), Chanakya Files (strategy), Ghar Ki Baat (family and friends), Turning Points (history) or Panchatantra Reloaded (fables for adults)."
- **Can I suggest a story?** "Please do! Comment it or DM it. The best ideas become Reels, and we credit you."
