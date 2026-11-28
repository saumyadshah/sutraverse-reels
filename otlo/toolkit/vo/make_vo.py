"""Make one Gujarati Gemini TTS clip per line. Usage: python3 make_vo.py tulsi_vo.json outdir
Needs GEMINI_API_KEY or GOOGLE_API_KEY. Never prints the key."""
import base64, io, json, os, sys, wave, time, pathlib, requests
MODELS = ["gemini-3.8-flash-tts", "gemini-3.1-flash-tts-preview", "gemini-2.5-flash-preview-tts"]
cfg = json.load(open(sys.argv[1])); out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not key: sys.exit("NO_KEY: GEMINI_API_KEY / GOOGLE_API_KEY not set")
log = []

def single_take(cfg, out, key):
    """Brand standard: the whole script as ONE take (one model, one voice, one performance), then cut into lines at
    the pauses nearest each line's expected position, so tone and timbre never jump between lines."""
    import numpy as np
    lines = cfg["lines"]; text = "\n\n".join(l["gu"] for l in lines)
    models = cfg.get("models") or ["gemini-2.5-pro-preview-tts", "gemini-3.8-flash-tts", "gemini-3.1-flash-tts-preview", "gemini-2.5-flash-preview-tts"]
    for rnd in range(5):
        for m in models:
            body = {"contents": [{"parts": [{"text": text}]}], "generationConfig": {"responseModalities": ["AUDIO"],
                    "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": cfg["voice"]}}}}}
            r = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent",
                              headers={"x-goog-api-key": key, "Content-Type": "application/json"}, json=body, timeout=300)
            print("take", rnd, m, r.status_code, flush=True)
            if r.status_code != 200: continue
            part = r.json()["candidates"][0]["content"]["parts"][0]["inlineData"]; raw = base64.b64decode(part["data"])
            rate = 24000
            for tok in part.get("mimeType", "").split(";"):
                if tok.strip().startswith("rate="): rate = int(tok.split("=")[1])
            pcm = np.frombuffer(raw[44:] if raw[:4] == b"RIFF" else raw, dtype=np.int16).astype(np.float32)
            with wave.open(str(out / "take.wav"), "wb") as w:
                w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate); w.writeframes(pcm.astype(np.int16).tobytes())
            # silence map (20 ms frames)
            fr = int(rate * 0.02); n = len(pcm) // fr; env = np.array([np.sqrt(np.mean(pcm[i*fr:(i+1)*fr]**2)) for i in range(n)])
            thr = max(120.0, np.percentile(env, 30) * 0.6); quiet = env < thr
            gaps = []; i = 0
            while i < n:
                if quiet[i]:
                    j = i
                    while j < n and quiet[j]: j += 1
                    if j - i >= 8: gaps.append(((i + j) / 2 * 0.02, (j - i) * 0.02))
                    i = j
                else: i += 1
            tot = len(pcm) / rate; L = [len(l["gu"]) for l in lines]; cum = np.cumsum(L)[:-1] / sum(L) * tot
            cuts = []
            for c in cum:   # nearest substantial pause to each expected boundary, weighted by its length
                cand = [g for g in gaps if all(abs(g[0] - x) > 0.3 for x in cuts)]
                if not cand: break
                best = min(cand, key=lambda g: abs(g[0] - c) / (0.5 + g[1]))
                cuts.append(best[0])
            if len(cuts) != len(lines) - 1: print("SPLIT FAILED", len(cuts)); continue
            cuts = sorted(cuts); edges = [0.0] + cuts + [tot]
            for k, l in enumerate(lines):
                a, b = int(edges[k] * rate), int(edges[k + 1] * rate)
                with wave.open(str(out / f"{l['id']}.wav"), "wb") as w:
                    w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate); w.writeframes(pcm[a:b].astype(np.int16).tobytes())
            print("SINGLE TAKE OK", m, round(tot, 1), "s, cuts", [round(c, 2) for c in cuts], flush=True); return True
        time.sleep(40)
    print("SINGLE TAKE FAILED"); return False

if cfg.get("single_take") and not all((out / f"{l['id']}.wav").exists() for l in cfg["lines"]):
    for l in cfg["lines"]:
        (out / f"{l['id']}.wav").unlink(missing_ok=True)
    single_take(cfg, out, key)

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
