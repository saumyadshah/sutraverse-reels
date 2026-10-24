#!/usr/bin/env python3
"""Upload a SutraVerse video to YouTube as a Short (YouTube Data API v3, free).

Credentials come only from the environment and are never printed:
  YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN

Usage:
  python yt_upload.py --check
      Exchange the refresh token for an access token; prints "auth ok" and the granted scope.
  python yt_upload.py --url <public mp4 url> | --file <path>  --meta meta.json [--privacy public|private|unlisted]
      meta.json (structured; the script builds the description from Saumya's template):
        {"title", "hook", "story", "shloka_devanagari", "shloka_iast", "meaning", "reference",
         "text_says", "tradition" (optional), "for_today", "chapters" (optional, long-form),
         "sources", "keywords": [...], "hashtags": ["#Topic", "#Scripture"], "tags": [...],
         "hi_title", "hi_description" (optional Hindi translations)}
      A legacy {"title", "description", "tags"} meta still works: the fixed brand block,
      links and #SutraVerse are added if missing.
  python yt_upload.py --meta meta.json --dry-run
      Print the final title, description and tags without uploading (no keys needed).
      Prints JSON: {"id": ..., "url": "https://youtube.com/shorts/<id>", "privacy": ...}

Notes:
  - Category 27 (Education), not made for kids, Hindi audio, English metadata.
  - Until Google approves the project's API audit, YouTube locks API uploads to private.
    The upload still succeeds; the result's "privacy" shows what YouTube actually set.
"""
import argparse
import json
import os
import ssl
import sys
import tempfile
import urllib.parse
import urllib.request

TOKEN_URL = "https://oauth2.googleapis.com/token"
UPLOAD_URL = ("https://www.googleapis.com/upload/youtube/v3/videos"
              "?uploadType=resumable&part=snippet,status,localizations")

# Fixed parts of Saumya's upload template (YouTube channel setup doc, 24 Oct 2026).
# Studio "upload defaults" don't apply to API uploads, so the script adds them itself.
BRAND = ("SutraVerse brings ancient Indian wisdom into modern life: real stories and shlokas from the "
         "Bhagavad Gita, Ramayana, Mahabharata, Vedas, Upanishads and Puranas, explained simply, "
         "with exact references.")
LINKS = ("Subscribe for daily life lessons from ancient wisdom: "
         "https://www.youtube.com/@sutraversehindu?sub_confirmation=1\n"
         "Instagram: https://www.instagram.com/sutraverselife")
DEFAULT_TAGS = ["SutraVerse", "Sutraverse Hindu", "ancient wisdom", "life lessons", "Hindu scriptures",
                "shloka meaning", "Sanatan Dharma", "spiritual stories"]
BRAND_KEYWORDS = ["SutraVerse", "Ancient Wisdom", "Life Lessons"]


def build_description(m):
    """Saumya's template, with the per-video fields filled from meta."""
    if m.get("description") and not m.get("hook"):
        d = m["description"].rstrip()
        if "sutraverselife" not in d:
            d += "\n\n" + BRAND + "\n\n" + LINKS
        if "#sutraverse" not in d.lower():
            d += "\n\n#SutraVerse"
        return d
    parts = [m["hook"].strip() + "\n" + m.get("story", "").strip()]
    if m.get("shloka_devanagari"):
        block = "Shloka: " + m["shloka_devanagari"].strip()
        if m.get("shloka_iast"):
            block += "\n" + m["shloka_iast"].strip()
        block += "\nMeaning: " + m.get("meaning", "").strip()
        if m.get("reference"):
            block += " (" + m["reference"].strip() + ")"
        parts.append(block)
    lines = []
    if m.get("text_says"):
        lines.append("The text says: " + m["text_says"].strip())
    if m.get("tradition"):
        lines.append("Tradition holds: " + m["tradition"].strip())
    if m.get("for_today"):
        lines.append("For us today: " + m["for_today"].strip())
    if lines:
        parts.append("\n".join(lines))
    if m.get("chapters"):
        parts.append(m["chapters"].strip())
    parts += [BRAND, LINKS]
    if m.get("sources"):
        parts.append("Sources: " + m["sources"].strip())
    kws = BRAND_KEYWORDS + [k for k in m.get("keywords", []) if k.lower() not in {b.lower() for b in BRAND_KEYWORDS}]
    parts.append(" \u00b7 ".join(kws[:15]))
    tags = ["#SutraVerse"] + [h if h.startswith("#") else "#" + h for h in m.get("hashtags", [])
                              if h.lstrip("#").lower() != "sutraverse"][:2]
    parts.append(" ".join(tags))
    return "\n\n".join(p for p in parts if p.strip())


def build_tags(m):
    out, seen, total = [], set(), 0
    for t in DEFAULT_TAGS + list(m.get("tags", [])):
        t = t.strip().replace("<", "").replace(">", "")
        if t and t.lower() not in seen and total + len(t) + 1 <= 480:
            out.append(t)
            seen.add(t.lower())
            total += len(t) + 1
    return out


def ctx():
    c = ssl.create_default_context()
    for p in (os.environ.get("SSL_CERT_FILE"), "/root/.ccr/ca-bundle.crt"):
        if p and os.path.exists(p):
            try:
                c.load_verify_locations(p)
            except Exception:
                pass
    return c


def req(url, data=None, headers=None, method=None):
    r = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    try:
        return urllib.request.urlopen(r, context=ctx(), timeout=600)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")[:800]
        sys.exit(f"HTTP {e.code} from {url.split('?')[0]}: {body}")


def access_token():
    need = ["YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN"]
    missing = [k for k in need if not os.environ.get(k)]
    if missing:
        sys.exit("missing environment variables: " + ", ".join(missing))
    data = urllib.parse.urlencode({
        "client_id": os.environ["YT_CLIENT_ID"],
        "client_secret": os.environ["YT_CLIENT_SECRET"],
        "refresh_token": os.environ["YT_REFRESH_TOKEN"],
        "grant_type": "refresh_token",
    }).encode()
    j = json.load(req(TOKEN_URL, data=data))
    return j["access_token"], j.get("scope", "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--url")
    ap.add_argument("--file")
    ap.add_argument("--meta")
    ap.add_argument("--privacy", default="public", choices=["public", "private", "unlisted"])
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if a.dry_run:
        meta = json.load(open(a.meta, encoding="utf-8"))
        print(json.dumps({"title": meta["title"].strip(), "description": build_description(meta),
                          "tags": build_tags(meta), "hi_title": meta.get("hi_title")},
                         ensure_ascii=False, indent=1))
        return

    tok, scope = access_token()
    channel = None
    if "youtube.readonly" in scope or "auth/youtube " in scope + " ":
        r = json.load(req("https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true",
                          headers={"Authorization": f"Bearer {tok}"}))
        items = r.get("items", [])
        if items:
            channel = {"id": items[0]["id"], "title": items[0]["snippet"]["title"],
                       "handle": items[0]["snippet"].get("customUrl", "")}
    if a.check:
        print("auth ok; scope:", scope)
        print("channel:", json.dumps(channel))
        return
    want = os.environ.get("YT_EXPECT_CHANNEL", "UClp0hIIwbvwByw7_UQrJmhQ")
    if channel and channel["id"] != want:
        sys.exit(f"refusing to upload: token belongs to channel {channel['title']} ({channel['id']}), expected {want}")

    meta = json.load(open(a.meta, encoding="utf-8"))
    title = meta["title"].strip()
    if len(title) > 100:
        sys.exit("title over 100 characters")
    description = build_description(meta)
    tags = build_tags(meta)

    path = a.file
    if a.url:
        fd, path = tempfile.mkstemp(suffix=".mp4")
        with os.fdopen(fd, "wb") as f, req(a.url) as r:
            f.write(r.read())
    size = os.path.getsize(path)

    payload = {
        "snippet": {"title": title, "description": description[:4900],
                    "tags": tags, "categoryId": "27",
                    "defaultLanguage": "en", "defaultAudioLanguage": "hi"},
        "status": {"privacyStatus": a.privacy, "selfDeclaredMadeForKids": False,
                   "embeddable": True, "license": "youtube"},
    }
    if meta.get("hi_title"):
        payload["localizations"] = {"hi": {"title": meta["hi_title"].strip()[:100],
                                           "description": meta.get("hi_description", "").strip()[:4900]}}
    body = json.dumps(payload).encode("utf-8")
    init = req(UPLOAD_URL, data=body, method="POST", headers={
        "Authorization": f"Bearer {tok}",
        "Content-Type": "application/json; charset=UTF-8",
        "X-Upload-Content-Type": "video/mp4",
        "X-Upload-Content-Length": str(size),
    })
    loc = init.headers["Location"]
    with open(path, "rb") as f:
        res = json.load(req(loc, data=f.read(), method="PUT", headers={
            "Authorization": f"Bearer {tok}", "Content-Type": "video/mp4",
            "Content-Length": str(size)}))
    print(json.dumps({"id": res["id"], "url": f"https://youtube.com/shorts/{res['id']}",
                      "privacy": res.get("status", {}).get("privacyStatus"),
                      "upload_status": res.get("status", {}).get("uploadStatus")}))


if __name__ == "__main__":
    main()
