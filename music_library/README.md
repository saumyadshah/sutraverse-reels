# SutraVerse music library (royalty-free only)

Drop royalty-free tracks here and every Reel run can use them instead of the synthesised score
(`sound_design.py --library music_library`, or `"sound": {"music_file": "music_library/warm/x.mp3"}` in sv_script.json).

- Folders by mood: `tense/` (conflict, before the verse), `warm/` (resolution, family, after the verse), `calm/` (reflective).
- Every track needs a licence sidecar next to it, named `<file>.json`:
  `{"title": "...", "artist": "...", "source_url": "https://...", "licence": "Pixabay Content License"}`
  A track without one is refused.
- Good free sources: Pixabay Music, YouTube Audio Library (no-attribution tracks), Free Music Archive (CC0/CC-BY; credit in the caption if CC-BY).
- Instrumental only, calm, never busier than the voice. Avoid tracks with vocals or a strong beat drop.
