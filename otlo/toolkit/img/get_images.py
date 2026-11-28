#!/usr/bin/env python3
"""Fetch or generate the images a Reel/carousel needs. Runs in GitHub Actions (full internet + GEMINI_API_KEY).
Usage: python3 otlo/toolkit/img/get_images.py otlo/work/<dir>
Reads script.json "images": [
  {"id": "father", "source": "gemini", "prompt": "<what to draw>"}                       -> img/father.png
  {"id": "mandvi", "source": "commons", "query": "Mandvi Kutch beach", "min_width": 1200} -> img/mandvi.jpg
  {"id": "poster", "source": "wiki_poster", "page": "Laalo – Krishna Sada Sahaayate", "credit": "Poster: <studio>"} -> img/poster.jpg
        official film poster from the film's Wikipedia infobox (the studio's artwork, used for news/commentary with credit)
  {"id": "poster", "source": "og", "url": "https://<official or ticketing page>", "credit": "..."} -> the page's og:image
  {"id": "still", "source": "url", "url": "https://<direct official image URL>", "credit": "..."}     -> downloaded as is
  {"id": "scene", "source": "ai", "prompt": "..."}  -> Gemini first, then the free Pollinations (Flux) API if Gemini fails
]
Movies/events: ALWAYS official artwork first (wiki_poster / og / url); "ai" is for illustrations and mood scenes only,
never a fake poster, a real person, a logo or text.
Commons: only CC0 / public domain / CC BY / CC BY-SA files; writes img/credits.json (title, author, licence, url) -> the
caption must carry the credit line. Gemini: illustrations only (never real people, actors, logos, posters or text).
Existing files are kept (delete one to regenerate). Repeat an id with another source as a FALLBACK: the second entry
only runs if the first produced nothing (e.g. wiki_poster first, then og from the District/BookMyShow page). Never prints the key."""
import os, sys, json, base64, pathlib, re, requests
d = pathlib.Path(sys.argv[1]); S = json.loads((d/'script.json').read_text()); out = d/'img'; out.mkdir(exist_ok=True)
key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
STYLE = ("Flat editorial illustration in a warm Indian heritage style; palette ivory #F3E9D6, indigo #1B2A4A, "
         "deep red #A8322A, turmeric #E3A21A, small touches of pink #C2185B; clean shapes, soft grain, plain ivory "
         "background, no text, no letters, no logos, no real or famous people. ")
PHOTO = ("Photorealistic cinematic documentary photograph, natural light, shallow depth of field, rich but true colours, "
         "35mm film look, high detail, no text, no letters, no logos, no watermark, no famous or identifiable real people. ")
MODELS = ["gemini-2.5-flash-image", "gemini-2.5-flash-image-preview", "gemini-3-pro-image-preview"]
credits = json.loads((out/'credits.json').read_text()) if (out/'credits.json').exists() else []
UA = {"User-Agent": "OtloBot/1.0 (https://instagram.com/otlo.gujarat; saumyadshah@users.noreply.github.com)"}
OK = re.compile(r'^(cc0|public domain|pd|cc by(-sa)? ?[0-9.]*)', re.I)
for im in S.get('images', []):
    iid = im['id']
    if list(out.glob(f'{iid}.*')): print(iid, 'exists'); continue
    src = im.get('source')
    if src in ('gemini', 'ai'):
        if not key: print(iid, 'NO_KEY'); continue
        done = False
        for m in MODELS:
            r = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent",
                              headers={"x-goog-api-key": key},
                              json={"contents": [{"parts": [{"text": (PHOTO if im.get('style') == 'photo' else STYLE) + im['prompt']}]}],
                                    "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}}, timeout=180)
            if r.status_code != 200: print(iid, m, 'HTTP', r.status_code); continue
            for part in r.json().get('candidates', [{}])[0].get('content', {}).get('parts', []):
                if 'inlineData' in part:
                    (out/f'{iid}.png').write_bytes(base64.b64decode(part['inlineData']['data'])); done = True; break
            if done: print(iid, 'ok via', m); break
        if not done:
            # free fallback: Pollinations (Flux), no key; 1080x1350 portrait unless told otherwise
            import urllib.parse
            w, h = im.get('size', [1080, 1350])
            u = ("https://image.pollinations.ai/prompt/" + urllib.parse.quote((PHOTO if im.get('style') == 'photo' else STYLE) + im['prompt'])
                 + f"?width={w}&height={h}&nologo=true&model=flux&seed={im.get('seed', 7)}")
            try:
                r = requests.get(u, timeout=240, headers=UA)
                if r.status_code == 200 and r.headers.get('content-type', '').startswith('image'):
                    (out/f'{iid}.jpg').write_bytes(r.content); done = True; print(iid, 'ok via pollinations')
                    credits.append({"id": iid, "title": "AI illustration", "author": "Otlo (generated)", "licence": "generated", "url": ""})
                else: print(iid, 'POLLINATIONS HTTP', r.status_code)
            except Exception as e: print(iid, 'POLLINATIONS', type(e).__name__)
        if not done: print(iid, 'AI IMAGE FAILED')
    elif src in ('wiki_poster', 'wiki_logo', 'og', 'url'):
        url = None
        try:
            if src in ('wiki_poster', 'wiki_logo'):
                # posters are non-free files, which the pageimages API ignores: read the infobox "image =" field instead
                API = "https://en.wikipedia.org/w/api.php"
                sr = requests.get(API, headers=UA, timeout=60, params={"action": "query", "format": "json", "list": "search",
                                  "srsearch": im['page'], "srlimit": 1}).json().get('query', {}).get('search', [])
                title = sr[0]['title'] if sr else im['page']
                wt = requests.get(API, headers=UA, timeout=60, params={"action": "parse", "format": "json", "page": title,
                                  "prop": "wikitext", "redirects": 1}).json().get('parse', {}).get('wikitext', {}).get('*', '')
                fld = 'logo' if src == 'wiki_logo' else 'image'
                m = re.search(r'\|\s*' + fld + r'\s*=\s*(?:\[\[)?(?:File:|Image:)?([^\n|\]]+\.(?:jpe?g|png|webp|svg))', wt, re.I)
                ref = "https://en.wikipedia.org/wiki/" + title.replace(' ', '_')
                if m:
                    fq = requests.get(API, headers=UA, timeout=60, params={"action": "query", "format": "json", "prop": "imageinfo",
                                      "titles": "File:" + m.group(1).strip(), "iiprop": "url"}).json()
                    url = next(iter(fq.get('query', {}).get('pages', {}).values()), {}).get('imageinfo', [{}])[0].get('url')
                print(iid, 'wiki page:', title, '| infobox image:', m.group(1) if m else None)
            elif src == 'og':
                html = requests.get(im['url'], headers={**UA, "User-Agent": "Mozilla/5.0 (OtloBot)"}, timeout=60).text
                m = re.search(r'<meta[^>]+property=["\']og:image(?::secure_url)?["\'][^>]+content=["\']([^"\']+)', html) or \
                    re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image', html)
                url = m and m.group(1); ref = im['url']
            else:
                url = im['url']; ref = im.get('page', url)
            if url:
                r = requests.get(url, headers=UA, timeout=120)
                if r.status_code == 200 and len(r.content) > 5000:
                    from PIL import Image; import io
                    if url.lower().endswith('.svg'):
                        (out/f'{iid}.svg').write_bytes(r.content)
                        try:
                            import cairosvg; cairosvg.svg2png(bytestring=r.content, write_to=str(out/f'{iid}.png'), output_width=1200)
                        except Exception as e: print(iid, 'svg->png', e)
                    elif src == 'wiki_logo':
                        Image.open(io.BytesIO(r.content)).convert('RGBA').save(out/f'{iid}.png')
                    else:
                        Image.open(io.BytesIO(r.content)).convert('RGB').save(out/f'{iid}.jpg', quality=95)
                    credits.append({"id": iid, "title": im.get('credit', 'Official artwork'), "author": im.get('credit', ''), "licence": "official promotional artwork, used with credit for news/commentary", "url": ref})
                    print(iid, 'ok', src, url[:90])
                else: print(iid, src, 'HTTP', r.status_code)
            else: print(iid, src, 'NO IMAGE FOUND')
        except Exception as e: print(iid, src, 'ERROR', type(e).__name__, str(e)[:120])
    elif src == 'commons':
        q = requests.get("https://commons.wikimedia.org/w/api.php", headers=UA, timeout=60, params={
            "action": "query", "format": "json", "generator": "search", "gsrsearch": im['query'] + " filetype:bitmap",
            "gsrnamespace": 6, "gsrlimit": 40, "prop": "imageinfo", "iiprop": "url|extmetadata|size", "iiurlwidth": 1600}).json()
        pages = sorted(q.get('query', {}).get('pages', {}).values(), key=lambda p: p.get('index', 99))
        used = {c.get('title') for c in credits}
        pages = [p for p in pages if p['title'] not in used]
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
