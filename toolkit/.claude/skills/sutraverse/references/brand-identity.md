# SutraVerse brand system

**Name:** SutraVerse · **Tagline:** Ancient Wisdom. Modern Life. · Values in `config/sutraverse.yaml` (edit there).

## Mark
`brand-kit/logo.svg` — one unbroken gold thread (the *sutra*) forming a circle and ending in a small knot, holding a three-petal lotus line drawing and an amber *bindu*. Strokes carry `pathLength="1"` so the mark draws itself on.

## Palette ("Bright", v2 — brighter, festive, still premium)
| Token | Hex | Use |
|---|---|---|
| royal / royal-deep | #2340B8 / #0E1A5A | fields (bright royal indigo with a saffron sunrise glow) |
| saffron | #FF7A1A | chips, caption edge, end-card sunrise, energy |
| marigold / sun | #FFB22E / #FFD36B | logo, light, emphasis words |
| ivory | #FFF6E6 | text on dark, caption cards |
| ink | #1A1240 | text on bright surfaces (captions, end card) |
| rose | #FF5C8A | bindu accent, sparingly |
| ember | #FF4D2E | conflict beats only |

The old midnight/antique-gold token names still exist in `brand.css` (mapped to the bright values) so earlier compositions keep working.

## Type (vendored, SIL OFL — renders offline)
Cinzel 700 (logotype only) · Cormorant Garamond 500/600 + italics (display, verse transliteration) · Inter 500–700 (subtitles, labels, kickers) · Tiro Devanagari Sanskrit (verified Sanskrit only).

## Recurring elements (built automatically by `build_composition.py`)
| Element | Short-form | Long-form |
|---|---|---|
| Opening identity | `badge` (default): compact mark + wordmark + tagline at the very top, already visible on frame 0 and gone by 1.8 s, so the hook owns the frame (never open on a logo). `overlay`: a larger 1.9 s flourish | `badge` as well; after the 30–45 s cold open, author a 2–3 s brand sting as its own scene (the `sting` mode, which plays before the hook, is not recommended) |
| Watermark | top-right mark + wordmark at 55% opacity from 1.6 s to the end card | same |
| End card | 3 s on a saffron→marigold sunrise: ink mark draws on, SUTRAVERSE, rule, tagline, CTA (+ handle if set) | 6 s, room for YouTube end-screen elements |
| Captions | English, Inter 700 ink on an ivory card with a saffron edge, bottom safe area | same, slightly smaller |

The brand never covers subtitles or the focal action. Change colours/fonts/CTA/handle in config — every future render picks them up.
