"""Make one Gujarati Gemini TTS clip per line. Usage: python3 make_vo.py tulsi_vo.json outdir
Needs GEMINI_API_KEY or GOOGLE_API_KEY. Never prints the key."""
import base64, io, json, os, sys, wave, time, pathlib, requests
MODELS = ["gemini-3.8-flash-tts", "gemini-3.1-flash-tts-preview", "gemini-2.5-flash-preview-tts"]
cfg = json.load(open(sys.argv[1])); out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not key: sys.exit("NO_KEY: GEMINI_API_KEY / GOOGLE_API_KEY not set")
log = []
for ln in cfg["lines"]:
    if (out / f"{ln['id']}.wav").exists(): print(ln["id"], "kept (existing clip)", flush=True); continue
    ok = False
    for rnd in range(4):                     # rate limits (429) clear within a minute: retry patiently before giving up
      if ok: break
      if rnd: time.sleep(35)
      for m in MODELS:
          body = {"contents": [{"parts": [{"text": ((cfg.get("direction") or "") + "\n\n" if cfg.get("direction") else "") + ln["gu"]}]}],
                  "generationConfig": {"responseModalities": ["AUDIO"],
                      "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": (ln.get("voice") or cfg["voice"])}}}}}
          r = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent",
                            headers={"x-goog-api-key": key, "Content-Type": "application/json"}, json=body, timeout=180)
          if r.status_code != 200:
              log.append(f"{ln['id']} {m} HTTP {r.status_code}"); continue
          part = r.json()["candidates"][0]["content"]["parts"][0]["inlineData"]
          raw = base64.b64decode(part["data"]); p = out / f"{ln['id']}.wav"
          if raw[:4] == b"RIFF": p.write_bytes(raw)
          else:
              rate = 24000
              for tok in part.get("mimeType", "").split(";"):
                  if tok.strip().startswith("rate="): rate = int(tok.split("=")[1])
              with wave.open(str(p), "wb") as w:
                  w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate); w.writeframes(raw)
          log.append(f"{ln['id']} ok via {m}"); ok = True; break
    if not ok: log.append(f"{ln['id']} FAILED")
    time.sleep(2)
(out / "log.txt").write_text("\n".join(log) + "\n"); print("\n".join(log))
