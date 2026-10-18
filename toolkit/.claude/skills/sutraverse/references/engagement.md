# Engagement layer — the Ootto content skills, adapted for SutraVerse

SutraVerse vendors 23 skills from [Ootto-AI/claude-content-skills](https://github.com/Ootto-AI/claude-content-skills) (MIT) into `.claude/skills/`. They are general growth playbooks; this file says **which one to load at which step, and what changes for sacred material.** Where they conflict with `scripture-research.md`, scripture accuracy wins.

## Where each skill plugs in

| Production step | Load | Use it for | SutraVerse adaptation |
|---|---|---|---|
| Topic choice | `content-research`, `trend-spotter`, `comment-mining`, `content-pillar-builder` | what people are actually struggling with; which pillar (work, family, mind, money, mortality) | Demand picks the *modern problem*; scripture still has to genuinely address it |
| Brief | `going-viral` (Step 1) | pick ONE goal: **share** (default for teachings), **save** (frameworks/lists), **follow** (series) | Emotion = recognition + "aha", never fear or outrage at a community |
| Hook | `virality` (8-point checklist), `viral-hook-writer`, `ab-hook-tester` | write 3 hooks, describe frame 0 → 3 s for each, keep the one that passes all 8 | see "Hook rules" below |
| Script — Shorts | `reel-scripter`, `going-viral` (Step 3–3.5) | open loop → escalating beats → payoff at the end | the payoff must be the verified teaching, not a twist you invented |
| Script — long-form | `youtube-scriptwriting` (+ `references/hooks|structures|retention|editing`) | click confirmation, rehooks every 60–90 s, second-best point first, binge-loop outro | claims still carry `claim_type` + `source_ref` |
| Storyboard | `reel-builder`, `on-screen-text-writer` | a visual change on every spoken line; text = beat headline; mute pass | English only; Sanskrit only as a verified `.sv-sanskrit` block |
| CTA | `cta-writer` | one ask, with a reason line | default **share** ("send this to the friend who…") or **save**; see CTA rules |
| Packaging | `caption-and-hashtags`, `cover-thumbnail-brief`, `youtube-thumbnail`, `youtube-seo`, `cross-platform-reformatter`, `story-sequencer` | caption, hashtags, first comment, thumbnail, titles/description/chapters, per-platform cuts | titles never claim what the text doesn't say |
| Series | `series-planner`, `content-calendar`, `content-repurposer` | named recurring format, 12 episodes, 2-week calendar; long video → 5 Shorts | one shared visual bible per series |
| Post-mortem | `reel-analyzer`, `virality` ("why did it flop") | frame 0 / 0.5 / 1 / 2 / 3 s review | compare against our own QA contact sheet |

Not vendored (available upstream if wanted): comment→DM lead automation, Instagram auto-posting, Obsidian memory, the Agent-Reach scraper. They post or message on the user's behalf and need separate, explicit setup and approval.

## Hook rules (short-form, every video)
1. **Frame 0 is already moving** and shows something the viewer instantly recognises from *their* life (a slide, a phone, an email, a family chat) — not a logo, not abstract cosmic art, not a deity portrait standing still.
2. The biggest element owns ≥40% of the frame and moves from frame 1.
3. The **claim lands at ~1.2–1.6 s**, word by word, synced to the voice, big and high-contrast (Cormorant ≥100 px on 1080-wide).
4. **First spoken word within 0.5 s** (`lead_in_seconds` ≈ 0.15–0.2) and it is about the viewer: "आपका…", "आपने कभी…".
5. Works on mute (the claim + visuals tell the story without audio).
6. The brand opening is the compact `badge` — it never competes with the hook.
7. Something extraordinary happens before 3 s (a name gets struck out, a chain snaps, a counter races, a flame flares).

`qa_check.py` measures 1, 4 and the visual-change cadence automatically; you judge the rest on the contact sheet.

## Holding attention
- **Open loop, visible finish line, real payoff.** Promise the payoff in the first 10 s, keep a visible marker of it on screen (e.g. a `LINK #1: ?` chip, a numbered chain, "3 signs"), escalate, and pay it off at the end. Never resolve early; never tease what you can't deliver.
- **Re-hook at the dips** (~4 s, ~9 s, ~15 s in Shorts): a twist line ("और ट्विस्ट ये है…"), a question ("तो ग़ुस्सा आता कहाँ से है?"), a stakes beat.
- **Every spoken line changes something on screen.** Cut on the phrase: `T.lines[id].phrases[k].start` gives exact phrase starts from the real audio.
- **Reality beats expectation:** the scripture insight should be more surprising than the hook implied (the "most people get this verse wrong" beat is gold — when it's true).

## Natural Hindi for retention
Short spoken phrases with real beats ("…" becomes a timed pause), questions to the viewer, everyday Hinglish (मीटिंग, ईमेल, ईगो, रिप्ले), and one idea per line. See `hindi-narration.md`.

## CTA rules
- One ask. Default: **share** ("उस दोस्त को भेजिए जिसे आज ये सुनना है") or **save** for frameworks. The end card carries follow.
- **Comment-keyword CTAs only when a real deliverable exists and the DM is actually wired** (e.g. a verse card PDF). An unwired keyword is a broken promise — `cta-writer`'s delivery check applies.
- On-screen CTA text complements the voice, never repeats it word for word.

## Honesty guardrails specific to SutraVerse
- No fabricated stats. Dramatised counters inside a story (a "REPLAY ×47" gag, a reputation bar draining) are fine only as obvious metaphor, never presented as data.
- Curiosity is not clickbait: a hook may withhold, never misstate the scripture.
- No fear-mongering (afterlife, curses, "you will suffer"), no shaming the viewer, no communal or caste framing.
- Model a reel's *structure*, never copy another creator's words, voice or visuals.
