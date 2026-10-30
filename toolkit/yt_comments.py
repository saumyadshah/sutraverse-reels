#!/usr/bin/env python3
"""SutraVerse YouTube comment tool (free YouTube Data API, same keys as yt_upload.py).

  python3 yt_comments.py --list [--days 3]
      Prints JSON: top-level comments on the channel's videos from the last N days that the channel
      has NOT replied to yet (comment_id, video_id, video_title, author, text, likes, published).
  python3 yt_comments.py --reply COMMENT_ID --text "reply"
      Posts ONE public reply as the channel, after re-checking live that the channel hasn't already
      replied to that thread (no duplicates). Refuses links, @mentions of other channels, text over
      450 characters, and empty text.

Quota: list = 1 unit per page, reply = 50 units. Requires the youtube.force-ssl scope.
Never prints any key. Safeguards on WHAT to reply live in toolkit/COMMENT_PLAYBOOK.md.
"""
import argparse, datetime as dt, json, os, re, sys, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from yt_upload import access_token, req  # noqa: E402

API = "https://www.googleapis.com/youtube/v3"
CHANNEL = os.environ.get("YT_EXPECT_CHANNEL", "UClp0hIIwbvwByw7_UQrJmhQ")


def get(tok, path, **params):
    url = f"{API}/{path}?" + urllib.parse.urlencode(params)
    return json.load(req(url, headers={"Authorization": f"Bearer {tok}"}))


def owner_replied(thread):
    for r in (thread.get("replies") or {}).get("comments", []):
        if r["snippet"].get("authorChannelId", {}).get("value") == CHANNEL:
            return True
    return False


def list_open(tok, days):
    since = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days)
    out, page, titles = [], None, {}
    for _ in range(5):
        p = dict(part="snippet,replies", allThreadsRelatedToChannelId=CHANNEL, order="time", maxResults=100, textFormat="plainText")
        if page:
            p["pageToken"] = page
        j = get(tok, "commentThreads", **p)
        stop = False
        for th in j.get("items", []):
            top = th["snippet"]["topLevelComment"]["snippet"]
            when = dt.datetime.fromisoformat(top["publishedAt"].replace("Z", "+00:00"))
            if when < since:
                stop = True
                break
            if top.get("authorChannelId", {}).get("value") == CHANNEL or owner_replied(th):
                continue
            out.append(dict(comment_id=th["id"], video_id=th["snippet"].get("videoId"), author=top.get("authorDisplayName"),
                            text=top.get("textDisplay", "")[:1000], likes=top.get("likeCount", 0), published=top["publishedAt"]))
        page = j.get("nextPageToken")
        if stop or not page:
            break
    ids = sorted({c["video_id"] for c in out if c["video_id"]})
    for i in range(0, len(ids), 50):
        v = get(tok, "videos", part="snippet", id=",".join(ids[i:i + 50]))
        titles.update({x["id"]: x["snippet"]["title"] for x in v.get("items", [])})
    for c in out:
        c["video_title"] = titles.get(c["video_id"], "")
    return out


BAD = re.compile(r"(https?://|www\.|\.com\b|\.in\b|@\w{3,})", re.I)


def reply(tok, comment_id, text):
    text = (text or "").strip()
    if not text or len(text) > 450 or BAD.search(text):
        sys.exit("refused: reply must be 1-450 characters with no links or @mentions")
    th = get(tok, "commentThreads", part="snippet,replies", id=comment_id)
    items = th.get("items", [])
    if not items:
        sys.exit("refused: comment thread not found (deleted or held for review)")
    if owner_replied(items[0]):
        print(json.dumps({"status": "skipped", "reason": "channel already replied", "comment_id": comment_id}))
        return
    body = json.dumps({"snippet": {"parentId": comment_id, "textOriginal": text}}).encode()
    r = json.load(req(f"{API}/comments?part=snippet", data=body, method="POST",
                      headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"}))
    print(json.dumps({"status": "posted", "comment_id": comment_id, "reply_id": r.get("id")}))


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--list", action="store_true"); a.add_argument("--days", type=int, default=3)
    a.add_argument("--reply"); a.add_argument("--text")
    o = a.parse_args()
    tok, scope = access_token()
    if o.reply and "force-ssl" not in scope:
        sys.exit("refused: token lacks youtube.force-ssl scope")
    if o.list:
        print(json.dumps(list_open(tok, o.days), ensure_ascii=False, indent=1))
    elif o.reply:
        reply(tok, o.reply, o.text)
    else:
        a.print_help()


if __name__ == "__main__":
    main()
