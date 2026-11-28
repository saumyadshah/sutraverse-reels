# OTLO brand standard v1: "Kankotri Press" (draft for Saumya's approval, 28 Nov 2026)

Pilot: `otlo/work/2026-11-28-amul-manthan-v2/` (Manthan / Amul). Kit: `runtime/brand.css` + `runtime/brand.js`.
Status: **approved in principle by Saumya (28 Nov 16:07) with improvements; v2 delivered for final sign-off.** When she approves, create `otlo/BRAND_APPROVED`; from then on every Reel uses this standard.

## The idea
An OTLO feature looks like a beautifully printed Gujarati invitation (kankotri): ivory card stock, letterpress vermilion
and haldi rules, the toran from our logo as the signature device, photographs mounted as press plates with a printed
credit, and indigo "night cards" for chapter turns and the close. Restraint over decoration: one idea, one image and
one headline per frame. (Lesson from the @manka.daily study: a page feels branded through a consistent system of
paper, type, framing and a single recurring device, not through more graphics.)

## Elements (all in the kit)
| Element | Class | Use |
|---|---|---|
| Card stock | `.o-card` (+ `.night`) + `.o-rule` | Every scene. Ivory for story, indigo night cards for numbers/turns and the end slate. Put `night` on the `.scene` too. |
| Toran | `.o-toran` | Top of every card: a straight embroidered band with mirror-work, fabric pennants (rani/haldi, stitched edge, mirror, tassel) and mango leaves, evenly spaced. Unfurls on frame 0 (brand sting), then sways like cloth, each flag on its own phase. |
| Transitions | automatic (`otlo.js`, `body.otlo`) | Cinematic dissolve, 0.75 s: the outgoing scene drifts forward, blurs and fades; the incoming settles from a slight zoom; a warm haldi/rani light-leak glows through. Start each scene's main visual within 0.2 s so both sides of the dissolve carry content. |
| Kicker | `.o-kicker` with `<span class="g">ગુજરાતી</span> · <b>ENGLISH</b>` | Series + chapter, e.g. `OTLO CINEMA · વાર્તા ૦૧`. Never letter-space Gujarati. |
| Progress | `.o-progress` | Toran beads, one per scene, current one vermilion. |
| Headline | `.o-head` > `.gu` (Rasa 700) + `.en` (Fraunces 600) | `<em>` = vermilion emphasis in Gujarati, `<i>` = italic counterpoint in English. Gujarati animates word by word (`data-kinetic="words"`). |
| Press plate | `.o-plate` (+ `.o-tape`, `.cr` credit) | Every photograph, slightly rotated (`data-rot`), with the source printed under it. |
| Cutout | `img.o-cut` (rembg) | Isolated subjects over a vermilion disc or a plate; never an awkward hard edge. |
| Parallax | `.o-layer[data-par]` | Background layers 20–40 px, foreground 60–90 px. |
| Lower third | `.o-lower` | Names of real people: Gujarati name + role in English caps. |
| Numbers | `.o-stat` + `.o-label` | Fraunces 800; count-ups (`data-count`). |
| Kankotri card | `.o-invite` | Quotes, credits, title lines. |
| Seal | `.o-seal` | One per scene at most: a verdict, a date, a number. |
| Map | `.o-map` + `assets/gujarat.json` | Self-drawing outline, bouncing pins, ripples. |
| End slate | night card + `.o-badge-end` (Toran badge stamps in) + ask + `@OTLO.GUJARAT · ગુજરાતની વાતો, ઓટલા પર` | Every Reel. |
| Cover | `cover.html` in the work dir | Card + big Gujarati headline + one English line + 1–2 plates + seal + badge; must read in the 3:4 grid. |
| Voice | `"single_take": true` in script.json | The whole script is recorded as ONE take (one model, Sulafat), then cut at the pauses: one consistent tone and timbre. Keep the script tight enough for natural pace (speed 1.0–1.1), 30–38 s. |
| Music | `"score": "otlo"` | OTLO's original score (`bin/score.py`): tanpura, santoor motifs in Bhoopali, warm pad; a dhol/tabla groove enters at the turn and builds to the climax, then resolves. Ducked ~9 dB under the voice. |
| Sound | automatic | Soft air swell under dissolves, paper slide on plates/lower thirds/cards/logos, letterpress thump on seals, logos and the badge. |
| Official logos | `.o-logo` disc / `.o-logocard`, source `wiki_logo` | Only real logos of organisations the story is about (fetched from their Wikipedia infobox), on a white disc/card, never recoloured or distorted, credited in the caption. |

## Palette and type
Ivory `#F4EAD7` · ink indigo `#1B2A4A` · vermilion `#B8322A` · haldi `#E3A21A` · rani `#C2185B` (toran only) ·
gold `#D9A441` (night cards). Rasa (Gujarati headlines), Fraunces (English display), Fira Sans (labels, credits),
Anek Gujarati (Gujarati labels). Subtitles stay in the safe band (y 1,380–1,480).

## Images
Real first: official artwork (credited), Commons photos (licence printed on the plate), maps from open data.
Never misidentify a real person: if a photo is a group shot and you can't be certain who is who, don't crop it to
"them"; use a name lower third without a face. No AI images of real people. Crop to remove irrelevant text
(e.g. other events' banners). Images are never stretched: `object-fit:cover` with a chosen `object-position`.
