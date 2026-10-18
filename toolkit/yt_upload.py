#!/usr/bin/env python3
"""Upload a SutraVerse video to YouTube as a Short (YouTube Data API v3, free).

Credentials come only from the environment and are never printed:
  YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN

Usage:
  python yt_upload.py --check
      Exchange the refresh token for an access token; prints "auth ok" and the granted scope.
  python yt_upload.py --url <public mp4 url> | --file <path>  --meta meta.json [--privacy public|private|unlisted]
      meta.json: {"title": "...", "description": "...", "tags": ["..."]}
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
              "?uploadType=resumable&part=snippet,status")


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
    a = ap.parse_args()

    tok, scope = access_token()
    if a.check:
        print("auth ok; scope:", scope)
        return

    meta = json.load(open(a.meta, encoding="utf-8"))
    title = meta["title"].strip()
    if "#shorts" not in title.lower() and "#shorts" not in meta.get("description", "").lower():
        meta["description"] = meta.get("description", "").rstrip() + "\n\n#Shorts"
    if len(title) > 100:
        sys.exit("title over 100 characters")
    tags, total = [], 0
    for t in meta.get("tags", []):
        t = t.strip().replace("<", "").replace(">", "")
        if t and total + len(t) + 1 <= 480:
            tags.append(t)
            total += len(t) + 1

    path = a.file
    if a.url:
        fd, path = tempfile.mkstemp(suffix=".mp4")
        with os.fdopen(fd, "wb") as f, req(a.url) as r:
            f.write(r.read())
    size = os.path.getsize(path)

    body = json.dumps({
        "snippet": {"title": title, "description": meta.get("description", "")[:4900],
                    "tags": tags, "categoryId": "27",
                    "defaultLanguage": "en", "defaultAudioLanguage": "hi"},
        "status": {"privacyStatus": a.privacy, "selfDeclaredMadeForKids": False,
                   "embeddable": True},
    }).encode("utf-8")
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
