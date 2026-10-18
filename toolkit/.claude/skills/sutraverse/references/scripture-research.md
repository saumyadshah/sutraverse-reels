# Scripture research & accuracy protocol

The channel's trust is the product. A beautiful video with one invented verse is a failed video.

## 1. Pick sources by topic, not by habit

Choose the text(s) that actually address the topic. Do not force the Gita into every video or stack five scriptures for authority. One well-chosen passage, properly contextualised, beats a montage of quotes.

| Text | Where the passage is located | Credible references to check (use ≥2) | Watch-outs |
|---|---|---|---|
| Bhagavad Gita | chapter.verse (e.g. 2.62) | gitasupersite.iitk.ac.in (multiple classical commentaries), holy-bhagavad-gita.org (Swami Mukundananda), bhagavad-gita.us (Shankara/Ramanuja/Madhva notes), Gita Press | Translators diverge on key words (e.g. *prasāda*: "grace" vs "serenity"). Viral "Gita quotes" are often fake (e.g. "Change is the law of the universe" is not a Gita verse). |
| Mahabharata | parva, adhyaya (and verse if cited) | BORI Critical Edition / Bibek Debroy translation; K. M. Ganguli translation (sacred-texts.com, public domain) | Many famous episodes are later or regional additions (e.g. several Karna and Draupadi episodes). Say "in popular retellings" when not in the critical edition. |
| Ramayana (Valmiki) | kanda, sarga, verse | valmiki.iitk.ac.in, Gita Press | Valmiki ≠ Tulsidas *Ramcharitmanas* ≠ TV serials/folk versions (e.g. the Lakshman Rekha is not in Valmiki). Name the version. |
| Srimad Bhagavatam | canto.chapter.verse | vedabase.io (ISKCON — note its devotional lens), Gita Press | Commentary is often sectarian; separate text from purport. |
| Garuda Purana | khanda/section, adhyaya | Motilal Banarsidass translation; Wood & Subrahmanyam *Garuda Purana (Saroddhara)* 1911 (public domain) | Online "list of 28/36 punishments" is frequently embellished. Recensions differ. Present afterlife descriptions as what the text says, not as fact; handle death and grief gently. |
| Upanishads | Upanishad, chapter/section, verse | Swami Nikhilananda, Eknath Easwaran, Advaita Ashrama editions; Max Müller (public domain) | Mahāvākya interpretations differ by school (Advaita/Vishishtadvaita/Dvaita). |
| Vedas | mandala.sukta.verse (Rig) | Jamison & Brereton (Rig Veda, 2014); Griffith (public domain, dated) | Avoid treating ritual hymns as self-help aphorisms; give context. |
| Yoga Sutras | pada.sutra (e.g. 1.2) | Edwin Bryant; Swami Vivekananda *Raja Yoga*; Swami Satchidananda | Sutras are terse — commentary does most of the interpreting; say whose. |
| Vidura Niti | Mahabharata, Udyoga Parva (Prajagara sub-parva) chapters | Ganguli; Gita Press *Vidura Niti* | Chapter numbering differs between editions — give the edition. |
| Chanakya Niti | chapter.verse (*Chanakya Niti Darpana*) | Gita Press / scholarly editions; for statecraft use Kangle's *Arthashastra* | Huge volume of fake "Chanakya quotes" online. Distinguish *Niti* (aphorisms, attribution traditional) from *Arthashastra*. |

If a site above is unreachable, use another credible edition and say which. Do not cite a blog, quote-image site or AI summary as the source of a verse.

## 2. Research steps (stage `research`)

1. Identify the exact passage(s). Confirm numbering in two sources (numbering varies by edition — record the edition).
2. Read the surrounding context: who is speaking, to whom, and why. Many "lessons" invert when context is ignored.
3. Read ≥2 translations; note material differences in key terms.
4. Read at least one traditional commentary when you will say what the verse *means*; name the commentator.
5. Note popular misreadings (they make excellent "common misunderstanding" beats).
6. Decide what the video will claim and classify every claim (below).
7. Write `artifacts/sources.json` and the canonical `research_brief` (`schemas/artifacts/research_brief.schema.json`).

## 3. Claim types — every script line has one

| `claim_type` | Meaning | How it may be voiced/shown |
|---|---|---|
| `direct_quote` | Translation of the verse itself | Only after verification; reference shown on screen (e.g. "Bhagavad Gita 2.63"). Name the translation in sources. |
| `faithful_paraphrase` | Plain restatement of what the text says | "Krishna says…" is fine; keep the reference on screen. |
| `story_retelling` | Narrating an episode | Name the version (Valmiki / Critical Edition / popular retelling) when versions differ. |
| `traditional_interpretation` | What a commentator or tradition reads into it | Attribute: "Shankaracharya explains…", "traditionally understood as…". |
| `philosophical_inference` | Your reasoning from the text | Signal it: "This suggests…", "One way to read this…". |
| `modern_application` | Practical advice for today | Frame as application, never as scripture: "In today's terms…". |

Never upgrade a claim's status (an inference voiced as "the Gita says"). If sources disagree materially, say so in one line ("Some translators read this as…"). If something cannot be verified, cut it or say it is uncertain — do not soften with vague wording.

## 4. `artifacts/sources.json`

```json
{
  "passages": [
    {"ref": "Bhagavad Gita 2.62", "edition": "Gita (standard numbering)",
     "transliteration": "dhyāyato viṣayān puṁsaḥ …",
     "translation_used": "…", "translator": "…", "urls": ["…", "…"],
     "context": "Krishna to Arjuna, describing the sthita-prajña", "verified": true}
  ],
  "interpretations": [{"claim": "anger arises when desire is obstructed", "attributed_to": "Shankara; Ramanuja", "url": "…"}],
  "uncertainties": ["…"],
  "not_used": [{"claim": "…", "why": "unverifiable / later interpolation / misattributed"}]
}
```

## 5. Respect

Deities, sages and sacred stories are treated with dignity: no comedy at their expense, no sexualised depiction, no gore, no mockery of rituals or communities. Present multiple traditions without ranking them. Avoid caste, communal or political framing. Death, grief and afterlife topics (Garuda Purana, Katha Upanishad) are handled gently and without fear-mongering; add a helpline line in the description only if a video touches self-harm.
