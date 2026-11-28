# Otlo creative toolkit: what's in it and when to use it (audited and tested 28 Nov 2026)

Every tool below was cloned, its licence checked and tested in this environment before it went in.

| Tool | Licence | Installed / discoverable | Tested here (28 Nov) | Used in Otlo for |
|---|---|---|---|---|
| **GSAP 3.15** + official **gsap-skills** | GSAP free incl. plugins; skills MIT | Vendored in `runtime/vendor/`; docs in `skills-ref/gsap/` | ✅ Kinetic type, count-ups, stamps, timelines render frame-exact (Laalo, Rani ki Vav, Manthan) | All Reels: `runtime/otlo-fx.js` |
| **Three.js r186** + **threejs-skills** | MIT | Vendored; docs in `skills-ref/threejs/` | ✅ WebGL via SwiftShader in headless Chromium: 3D poster card, card flip, bokeh, confetti | `runtime/otlo-3d.js` (`poster`, `flip`, `bokeh`, `confetti`) |
| **Remotion 4.0.547** + remotion skills | Free for individuals and companies of up to 3 people (Otlo qualifies; larger needs a company licence) | `toolkit/remotion/` project; `setup_extras.sh remotion` | ✅ 1080×1920 H.264 render with the session Chromium; `Feature` template (clips + lower thirds) rendered | Structured edits of real footage: Otlo Spotlight business features, event highlights from organisers' clips |
| **Manim (ManimGL 1.7.2)** | MIT | `setup_extras.sh manim` (needs libpango1.0-dev, audioop-lts, xvfb) | ✅ after 3 fixes: rendered an animated bar chart to MP4 | Data explainers (box office, timelines, maps of numbers) rendered with `--transparent` and placed as a clip; use when the maths *is* the story |
| **AniDoodle** | Apache 2.0 | Vendored in `toolkit/anidoodle/` | ✅ rendered sample stills (koi: hand-drawn flat illustration) | Hand-drawn hero illustrations for folk stories, food origins, explainers where no photo exists |
| **Huashu Art Motion** | MIT | Reference in `skills-ref/huashu-art-motion/` | n/a (a style/grammar guide, no engine) | Visual rhythm and art-style recipes for explainer Reels |
| **Lemo Opuscar 2.0** (99 film styles) | Code MIT; style docs CC BY-NC 4.0 + permission to use them for our own (incl. commercial) films; **not redistributable**, so it is **not committed** to this public repo | `setup_extras.sh lemo` clones to `/tmp/lemo-opuscar` at run time | ✅ rendered the *Dark Documentary* demo at 1080×1920 (software WebGL, ~4 s/frame); same `window.render(t)` page contract as Otlo's engine | Visual grammar for documentary Reels: `dark-documentary`, `archive-lighttable`, `map-explainer`, `newsreel`, `news-package`, `caption-news`, `comic-history`. Read the STYLE.md, author the 9:16 page in Otlo's engine. Films we make are ours, no credit needed |
| **Claude Video Effects** | MIT | Vendored in `toolkit/video-effects/` | Scripts need real footage (face tracking); not run on Otlo's animated Reels | Partner footage features: comment-box, receipt, punch-in, grade |
| **Brag** (`/brag-slim`) | MIT | Docs read; it is a workflow skill that renders with whatever is installed | n/a as an engine; its website-to-promo workflow fits Remotion/our engine | 15–20 s promo films for a partner business made from its website (only for confirmed partnerships) |

## Image sources (img/get_images.py, runs in GitHub Actions)
Order of preference, written into `script.json` `"images"`:
1. **Official artwork** for films and events: `wiki_poster` (reads the film's Wikipedia infobox poster), `og` (the share image of an official, District or BookMyShow page), `url` (a direct official image URL). Credit goes in the caption.
2. **Licensed photos**: `commons` (CC0 / PD / CC BY / CC BY-SA only; credits written to `img/credits.json`).
3. **Generated**: `ai` (Gemini first; if its quota fails, the free Pollinations/Flux API) for illustrations and mood scenes. **Never** a fake poster, a real person, a logo or text.
4. **Drawn**: AniDoodle stills or inline SVG.

Repeat an id with a second source to make a fallback, e.g. `wiki_poster` then `og`.

## Documentary look (28 Nov, second brief)
`runtime/doc.css` + `<body class="doc">`: full-bleed real photographs (`.docbg img.kb`, Ken Burns), dark cinematic
shade, film grain, vignette, gold type. Every AI image is labelled on screen ("Illustrative reconstruction (AI)").
Examples: `otlo/work/2026-11-28-1230-rani-ki-vav-note/`, `otlo/work/2026-11-28-1930-manthan-farmers/`.
