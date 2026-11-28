# Otlo creative toolkit: what's in it and when to use it (evaluated 28 Nov 2026)

Every tool below was cloned, its licence checked and tested in this environment before it went in.

| Tool | Licence | Verdict | How Otlo uses it |
|---|---|---|---|
| **GSAP 3.15** (+ SplitText, CustomEase, MotionPath, DrawSVG) and the official **gsap-skills** | GSAP: free incl. all plugins (Webflow); skills MIT | **Integrated** | `runtime/vendor/gsap*.js` + `runtime/otlo-fx.js`: kinetic type, count-ups, stamps, highlighter sweeps, Ken Burns, custom tweens (`window.OTLO_TWEENS`). A paused timeline is seeked per frame, so renders are frame-exact. Docs: `skills-ref/gsap/`. |
| **Three.js r186** and **threejs-skills** | MIT | **Integrated** | `runtime/otlo-3d.js`: `canvas.fx3d` with `data-fx="poster"` (3D poster card swing-in with a moving glint), `"bokeh"` (brand-colour depth background), `"confetti"` (petals for payoffs). Rendered per frame through SwiftShader WebGL in headless Chromium. Docs: `skills-ref/threejs/`. |
| **AniDoodle** | Apache 2.0 | **Integrated for illustrations** | `anidoodle/` (skill + engine). Code-drawn illustrations in 32 styles (woodcut, risograph, sumi-e, paper craft, flat vector…). Use for hero illustrations of food, places, folk stories: author a film per `anidoodle/SKILL.md`, render a still with `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers node tools/still.mjs <film> --out <work>/img/<id>.png` (run `npm install --omit=optional` in `anidoodle/engine` first), then place it as `<img class="photo">`. |
| **Huashu Art Motion** | MIT | **Reference** | `skills-ref/huashu-art-motion/`: art-style recipes and the "explainer grammar" (beats, rhythm, voice-driven art films). Read when designing an explainer Reel's visual rhythm. |
| **Claude Video Effects** | MIT | **Kept for real footage** | `video-effects/`: ffmpeg/OpenCV effects (comment-box, the-bill receipt, lean-in punch, moody grade, swipe before/after). These need real footage, so they're for partner features (restaurant or event clips supplied by the business), not for Otlo's animated Reels. |
| **Manim** (3b1b) | MIT | **Not integrated** | Needs OpenGL + LaTeX + Pango, a heavy install. Otlo's numbers and charts (count-ups, growing bars) are done in GSAP inside the same page, which keeps one engine and one visual style. Revisit only for a genuinely mathematical explainer. |
| **Remotion skills** | Remotion licence (free for individuals; companies of 4+ need a licence) | **Not integrated** | A second React video engine would duplicate ours (HTML + GSAP + Three.js + ffmpeg already renders frame-exact at 12 Mb/s). Its best ideas (timeline-driven scenes, audio-led timing) are already in `build.py`. |
| **Brag** | MIT | **Not used** | Makes launch videos for software projects; nothing in it fits a Gujarati culture page. |

## Image sources (img/get_images.py, runs in GitHub Actions)
Order of preference, written into `script.json` `"images"`:
1. **Official artwork** for films and events: `wiki_poster` (reads the film's Wikipedia infobox poster), `og` (the share image of an official, District or BookMyShow page), `url` (a direct official image URL). Credit goes in the caption.
2. **Licensed photos**: `commons` (CC0 / PD / CC BY / CC BY-SA only; credits written to `img/credits.json`).
3. **Generated**: `ai` (Gemini first; if its quota fails, the free Pollinations/Flux API) for illustrations and mood scenes. **Never** a fake poster, a real person, a logo or text.
4. **Drawn**: AniDoodle stills or inline SVG.

Repeat an id with a second source to make a fallback, e.g. `wiki_poster` then `og`.
