# Visual direction — cinematic, animated, culturally careful

Read OpenMontage `skills/meta/taste-direction.md` and `skills/meta/bespoke-composition.md` for hero work. Playbook: `styles/sutraverse.yaml`.

## Look
Midnight-blue and indigo fields; antique gold line-work and amber light as the only "glow"; parchment warmth; soft vignette and grain (added by the brand kit). Scripture worlds feel timeless and mythic (silhouettes, dusk skies, banners, chariots, river ghats, forest ashrams). Modern worlds feel specific and Indian (open-plan office in Gurugram, a Mumbai local, a family drawing room, a phone screen at night) and share the same palette so the two worlds cut together.

## Motion (non-negotiable: nothing is a still slide)
Every scene uses at least two of: layered parallax drift, light/particle motion (embers, dust, diya flicker), character/object action (head turn, arm raise, chariot banner wave, phone buzz), gold line draw-on, kinetic typography, camera push/pull. Hold times follow the playbook (2.5–10 s). Transitions: dissolve, light-wipe, match-cut on shape (a phone glow becomes a diya flame). Keep adjacent shots continuous in direction and light.

## Character & visual bible (write before authoring scenes; reuse across a series)
For each recurring figure record: silhouette shape and proportions, age, costume and jewellery (Krishna: peacock feather, yellow *pitambara*, flute or chariot reins; Arjuna: Gandiva bow, armour, banner with Hanuman), colour keys, lighting side, and how the face is treated. Keep it identical in every scene.

**Sensitivity:** depict deities and sages with dignity — calm postures, no comedy, no caricature, no gore. Silhouettes, back-lit figures and symbolic elements (chariot wheel, feather, conch, bow, lotus) are often more powerful and safer than detailed faces. Do not depict violence graphically; imply it with light, banners, dust, sound.

## Route A — hand-authored scenes (always available, zero cost)
HyperFrames atelier composition in `composition/src/`:
- `scenes.html`: one `<section class="clip sv-scene" data-scene="S#">` per scene; layers as absolutely positioned divs/inline SVG (sky, far, mid, near, fx, text).
- `scenes.css`: art using brand tokens (`--sv-gold`, `--sv-u` px unit, safe-area vars).
- `scenes.js`: `window.SV_BUILD_SCENES = (tl, T) => {…}`; all tweens at global time using `T.scenes`/`T.lines`. Helpers in `brand-kit/sv-lib.js`: `SV.sceneFade`, `SV.drift`, `SV.particles`, `SV.drawOn` (strokes with `pathLength="1"`), `SV.revealWords`, seeded `SV.rand`.
- Determinism rules (HyperFrames): no `Math.random` (use `SV.rand`), no clocks, no `repeat:-1`, animate only transform/opacity/filter/colour/stroke props, no network assets (everything local).
- Keep the badge zone (top ~200 px, first 1.8 s in short-form) and the subtitle band clear. The hook visual itself must already be moving on frame 0.
- Time key visuals to narration: e.g. light the second chain link part-way through `T.lines.L05`.

Craft tips for SVG figures: build silhouettes from a few bezier shapes; separate head/torso/arm groups so they can rotate around joints (`transformOrigin`); give back-light with a blurred amber ellipse behind; add a thin gold rim stroke for premium feel.

## Route B — generated imagery (when `image_selector` has a configured provider)
Write prompts with the playbook prefix/negative prompt plus: subject + action, costume per bible, setting, time of day/light, camera framing and lens, composition (leave subtitle band and title area calm), aspect ratio, and "no text". Generate one hero frame, review it against the bible, then batch. Animate plates with parallax (cut foreground with `bg_remove` if available), camera moves, particles and light passes in HyperFrames — still images must never sit static.

## Route C — generated motion (when `video_selector` has a configured provider)
Use image-to-video from approved plates for hero beats (chariot moving, banners in wind, a character turning). Prompts follow OpenMontage `skills/creative/video-gen-prompting.md` (Subject / Motion / Scene / Spatial / Camera) and the provider's Layer 3 skill. Announce provider, model and cost before the first paid call; sample before batching; respect `budget` in config. Put clip files in `composition/src/assets/` and declare them in `composition/src/media.html` as `<video class="clip" muted playsinline src="assets/…" data-start data-duration data-track-index="1">` — `build_composition.py` inserts that file as direct children of the root (HyperFrames media rule: never inside a scene wrapper). Animate their transforms from `scenes.js` at global time.

## Scene-plan template per scene
`id, start–end, narration lines, purpose (hook/teaching/…), visual description, layers, motion & camera, character action/expression, light, on-screen English phrase, transition in/out, SFX, music cue, negative constraints (no distorted hands, no text in generated images, no anachronisms)`.
