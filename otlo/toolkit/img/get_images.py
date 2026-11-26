#!/usr/bin/env python3
"""Fetch or generate the images a Reel/carousel needs. Runs in GitHub Actions (full internet + GEMINI_API_KEY).
Usage: python3 otlo/toolkit/img/get_images.py otlo/work/<dir>
Reads script.json "images": [
  {"id": "father", "source": "gemini", "prompt": "<what to draw>"}                       -> img/father.png
  {"id": "mandvi", "source": "commons", "query": "Mandvi Kutch beach", "min_width": 1200} -> img/mandvi.jpg
]
Commons: only CC0 / public domain / CC BY / CC BY-SA files; writes img/credits.json (title, author, licence, url) -> the
caption must carry the credit line. Gemini: illustrations only (never real people, actors, logos, posters or text).
Existing files are kept (delete one to regenerate). Never prints the key."""
import os, sys, json, base64, pathlib, re, requests
d = pathlib.Path(sys.argv[1]); S = json.loads((d/'script.json').read_text()); out = d/'img'; out.mkdir(exist_ok=True)
key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
STYLE = ("Flat editorial illustration in a warm Indian heritage style; palette ivory #F3E9D6, indigo #1B2A4A, "
         "deep red #A8322A, turmeric #E3A21A, small touches of pink #C2185B; clean shapes, soft grain, plain ivory "
         "background, no text, no letters, no logos, no real or famous people. ")
MODELS = ["gemini-2.5-flash-image", "gemini-2.5-flash-image-preview", "gemini-3-pro-image-preview"]
credits = json.loads((out/'credits.json').read_text()) if (out/'credits.json').exists() else []
UA = {"User-Agent": "OtloBot/1.0 (https://instagram.com/otlo.gujarat; saumyadshah@users.noreply.github.com)"}
OK = re.compile(r'^(cc0|public domain|pd|cc by(-sa)? ?[0-9.]*)', re.I)
for im in S.get('images', []):
    iid = im['id']
    if list(out.glob(f'{iid}.*')): print(iid, 'exists'); continue
    if im.get('source') == 'gemini':
        if not key: print(iid, 'NO_KEY'); continue
        done = False
        for m in MODELS:
            r = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent",
                              headers={"x-goog-api-key": key},
                              json={"contents": [{"parts": [{"text": STYLE + im['prompt']}]}],
                                    "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}}, timeout=180)
            if r.status_code != 200: print(iid, m, 'HTTP', r.status_code); continue
            for part in r.json().get('candidates', [{}])[0].get('content', {}).get('parts', []):
                if 'inlineData' in part:
                    (out/f'{iid}.png').write_bytes(base64.b64decode(part['inlineData']['data'])); done = True; break
            if done: print(iid, 'ok via', m); break
        if not done: print(iid, 'GEMINI FAILED')
    elif im.get('source') == 'commons':
        q = requests.get("https://commons.wikimedia.org/w/api.php", headers=UA, timeout=60, params={
            "action": "query", "format": "json", "generator": "search", "gsrsearch": im['query'] + " filetype:bitmap",
            "gsrnamespace": 6, "gsrlimit": 15, "prop": "imageinfo", "iiprop": "url|extmetadata|size", "iiurlwidth": 1600}).json()
        pages = sorted(q.get('query', {}).get('pages', {}).values(), key=lambda p: p.get('index', 99))
        got = False
        for p in pages:
            ii = (p.get('imageinfo') or [{}])[0]; md = ii.get('extmetadata', {})
            lic = md.get('LicenseShortName', {}).get('value', '')
            if not OK.match(lic.strip()) or ii.get('width', 0) < im.get('min_width', 1000): continue
            url = ii.get('thumburl') or ii.get('url'); b = requests.get(url, headers=UA, timeout=120).content
            ext = '.png' if url.lower().endswith('.png') else '.jpg'; (out/f'{iid}{ext}').write_bytes(b)
            author = re.sub('<[^>]+>', '', md.get('Artist', {}).get('value', 'unknown')).strip()
            credits.append({"id": iid, "title": p['title'], "author": author, "licence": lic, "url": ii.get('descriptionurl')})
            print(iid, 'ok', p['title'], lic); got = True; break
        if not got: print(iid, 'COMMONS: no freely licensed match')
(out/'credits.json').write_text(json.dumps(credits, indent=1, ensure_ascii=False))
