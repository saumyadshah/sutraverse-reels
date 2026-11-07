# SutraVerse 2.0 — one identity, six cinematic treatments

The identity is fixed: the thread-and-ring mark, the colour-means-something palette, Fraunces / Anek / Plex Mono, the ink subtitle plate, the chapter tag, the series chip and the principle card (`brand2.css`). Each series then gets its own way of filming, so the feed never looks like one template repeated. Samples: `samples/` (frame_*.png, cover_office.png, brand_board.png).

Every treatment is written as a Lemo-Opuscar "my style" (essence → look → motion → camera → sound → native move → pitfalls) and is built on a library style as its technique base. Read `OPUSCAR.md` for how to render with it.

**Shared rules (all treatments)**
- 1080x1920, 30 fps. Content box x 72–1008, y 250–1400. Nothing important below y 1520 (Instagram UI). Subtitle plate bottom 430 px.
- Colour has one job each: **amber = insight** (the idea, the key word, the lamp), **vermilion = conflict** (the trap, the villain's move, warnings), **teal = resolution** (the better move), **indigo = the past**. Never use them as decoration.
- Chapter tag (`.sv2-tag`) on every section change: `RULE 07`, `FILE 02`, `EP 04`, `CHAPTER 1`, `FABLE 01`, `STEP 2`. It is how the viewer feels progress.
- The principle card (`.sv2-principle`) is the payoff: one line to remember, in Fraunces, with its source in Plex Mono.
- Characters come only from `cast2.json` via `cast2.js` (CAST2.draw), in the treatment's render style (`cel` or `engrave`). Same face, every angle, every shot size.
- Facts on screen carry a source line in Plex Mono (`.sv2-source`). Tradition and legend are labelled as such.

---

## 1. Chanakya Files — "Ember Engraving"
*Strategy, power, money, discipline, leadership. Chanakya Niti, Arthashastra.*
- **Essence:** a lamp-lit study at night; Chanakya appears as a living copperplate engraving on a paper plate, the world around him is ink-black, lit by one oil lamp. The modern protagonist's problem is shown in cel (Office Shastra look) and *crosses into* the engraving when the rule arrives.
- **Look:** ink background with an amber lamp glow (radial, top-right); engraving plates in paper with a double plate mark; hatching follows form, never grey fills (`style: "engrave"`). Amber only on the rule and the lamp.
- **Motion:** the burin "cuts" lines in (stroke draw-on), the plate prints (a flash of paper), slow push-ins. Rules appear as engraved roman lettering.
- **Camera:** slow push-ins, one lateral lamp-light sweep across the plate, macro on the eyes for the rule.
- **Sound:** low tanpura drone + single sitar/pluck phrases (`pluck.py`), lamp flicker, paper and burin foley; silence before the rule.
- **Native move:** *the plate prints itself*: hatching sweeps across the frame to reveal the scene.
- **Library base:** `engraving` (line engine, plate grammar) + `woodcut` (carved light).
- **Pitfalls:** grey fills (break the medium), more than one amber thing, Chanakya speaking modern slang, inventing quotes (Chanakya Niti verse numbers vary by edition: cite the edition).

## 2. Mind Games — "Case File"
*Psychology: biases, manipulation, ego, influence, persuasion, why people repeat mistakes.*
- **Essence:** every Reel opens a case file on one named trick (foot-in-the-door, sunk cost, reciprocity…). Evidence (chat cards, polaroids of the cast, receipts) is pinned to a dark dossier; the trick is stamped in vermilion; the defence is in teal.
- **Look:** graphite dossier with a halftone dot field, cream evidence cards, vermilion rubber stamps and red string, one big Fraunces concept title with an amber italic word; study citation in Plex Mono.
- **Motion:** cards slap down with weight, stamps slam (2-frame shake), red string draws between exhibits, the file tab changes `FILE 01 → 02 → 03`.
- **Camera:** top-down desk with parallax between paper layers; snap zooms into an exhibit; one pull-back to show the whole board.
- **Sound:** paper slaps, stamp thuds, typewriter ticks, a low pulse; the reveal lands on a stamp.
- **Native move:** *the stamp*: the trick's name is stamped onto the evidence at the payoff.
- **Library base:** `halftone-dossier` (dots, stamps, exhibits) adapted to a dark sheet; `briefing-board` (pinned evidence grammar).
- **Pitfalls:** pop-psychology claims without a study, "dark psychology" manipulation how-tos (always frame as *recognise and defend*), clutter (max 3 exhibits on screen).

## 3. Office Shastra — "Night City Cel"
*Office politics, bosses, credit theft, appraisals, negotiation, boundaries, careers.*
- **Essence:** an Indian office after hours: glass meeting rooms, laptop glow, a city window grid. Recurring cast (Riya, Kabir, Malhotra sir) in flat cel with hard shadow shapes and an amber rim light. UI cards (chat, email, calendar, slides) are part of the scene and colour-coded by meaning.
- **Look:** indigo-to-ink gradient, warm lit windows, cel characters (`style: "cel"`), UI cards in paper with Plex Mono timestamps.
- **Motion:** story first, framework second: the scene plays, then freezes; option cards (A / B / "+ what else is possible?") slide in; the better move turns teal.
- **Camera:** two-shots for conflict, close-ups for reactions (eyebrows matter), over-the-shoulder on screens, a whip-pan between the boss and the victim.
- **Sound:** office room tone, keyboard, AC hum, notification pings as punctuation; a warm pad under the resolution.
- **Native move:** *the freeze-frame breakdown*: the scene freezes and the UI cards dissect the moment.
- **Library base:** `midcentury-toon` (limited animation, one sentence per picture) for acting economy; `dark-keynote` for UI-card precision.
- **Pitfalls:** a generic "corporate" look, villain caricatures, advice that would get someone fired (always give a professional, safe move).

## 4. Ghar Ki Baat — "Warm Home Cel"
*Family, generations, friendship, money and status, social pressure, "log kya kahenge".*
- **Essence:** the same cel system as Office Shastra, but in warm tungsten home light: kitchens, dining tables, WhatsApp family groups, weddings. Dialogue opens the Reel.
- **Look:** warm bone-and-amber interiors, teal for the healthy move, vermilion for the remark that hurts; the family WhatsApp card is a recurring device.
- **Motion / camera:** dinner-table two-shots, a slow push on the person who is hurt, the WhatsApp thread scrolling as a split screen.
- **Sound:** pressure cooker, TV in another room, steel plates, a single tabla phrase on the turn.
- **Native move:** *the message that gets typed and deleted* (the honest reply vs the safe reply).
- **Library base:** `midcentury-toon` + `isometric-picture-book` (rooms as stages).

## 5. Turning Points — "Archive & Timeline"
*History: rulers, strategists, decisions, business failures and comebacks, lesser-known stories.*
- **Essence:** a paper archive: a giant year in Plex Mono (vermilion digits), a timeline that the camera rides, engraved medallion portraits (engrave style) and maps drawn as coastlines and terrain only.
- **Look:** warm aged paper, ink type, indigo for the past, vermilion for the decisive moment; documents and quotes highlighted on the page they come from.
- **Motion:** the year counts to the event; the timeline scrolls; a medallion turns (yaw) to face the viewer when the person speaks.
- **Camera:** rides along the timeline, a push into the medallion, a map zoom from region to place.
- **Sound:** paper, a clock tick that stops at the turning point, a low brass/drone swell.
- **Native move:** *the year snaps*: digits roll and lock on the turning point.
- **Library base:** `archive-lighttable` + `engraving` (medallions) + `transit-map` (route lines). Maps: **India-appropriate rule** (see OPUSCAR.md: no political borders unless the story needs them; when shown, follow the Survey of India depiction; never use the library's China-view map rule for South Asia).
- **Pitfalls:** dates without "c." where uncertain, legend told as fact (label "Tradition holds"), modern borders projected into the past.

## 6. Panchatantra Reloaded — "Lamp Theatre"
*Fables retold for adult life: the jackal advisers, the monkey and the crocodile, the blue jackal, the talkative tortoise.*
- **Essence:** Indian leather shadow puppetry (the tholu bommalata / tholpavakoothu tradition as grammar): translucent dyed-hide puppets with carved holes, pressed to a cotton screen, lit by an oil lamp; rods visible. Then a cut to the modern cast living the same fable.
- **Look:** warm screen gradient (amber core → burnt edges), puppets in translucent pigment colours, carved holes glowing, the lamp in frame at the bottom.
- **Motion:** profile acting, jointed limbs on rods, puppets press closer to the screen to get sharper (focus = closeness).
- **Camera:** locked wide like a stage, then a push to two puppets in conversation; the cut to the modern cast is a match on silhouette.
- **Sound:** a small ensemble feel (mridangam-like frame drum, flute), voices close-miked, the lamp crackle.
- **Native move:** *the silhouette match*: a puppet's silhouette becomes a modern character's silhouette.
- **Library base:** `shadow-puppet` (adapt to Indian puppet design, never Chinese motifs) + `paper-lantern`.
- **Pitfalls:** copying any real puppet design or troupe; cartoon animals; using Chinese shadow-theatre ornament.

## Explainer layer (all series) — "Folio Diagram"
The diagrams that explain the idea, in every series: ink ground with a faint 12-column grid, nodes as filled circles with a paper ring, dotted connections drawn on as they are spoken, labels in Anek 40 / 32, numbers in Plex Mono, the source line at the bottom. One idea per screen (max 3 nodes, 4 bars, 4 steps). The explainer kit in the sutraverse skill (`brand-kit/explainer.js`) supplies the components; restyle with `brand2.css` tokens. Library references: `dataviz` (one idea at a time, real data only), `iso-infographic` (system cutaways), `whiteboard` (step reveals).
