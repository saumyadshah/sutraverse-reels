"""Transcribe each sN.wav in the given dirs with Gemini, as a check for leaked instructions.
Usage: python3 transcribe.py vo vo2   -> writes <dir>/transcript.txt. Never prints the key."""
import base64, os, sys, pathlib, requests, time
key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
MODELS = ["gemini-2.5-flash", "gemini-flash-latest", "gemini-2.0-flash"]
for d in sys.argv[1:]:
    d = pathlib.Path(d); lines = []
    for w in sorted(d.glob("s*.wav")):
        b64 = base64.b64encode(w.read_bytes()).decode(); txt = None
        for m in MODELS:
            body = {"contents": [{"parts": [{"text": "Transcribe this audio exactly, word for word, in the script of the language spoken (English words in Latin script). Output only the transcript."},
                                            {"inlineData": {"mimeType": "audio/wav", "data": b64}}]}]}
            r = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent",
                              headers={"x-goog-api-key": key}, json=body, timeout=90)
            if r.status_code == 200:
                try: txt = r.json()["candidates"][0]["content"]["parts"][0]["text"].strip().replace("\n", " "); break
                except Exception as e: txt = f"PARSE_ERROR {e}"
            else: txt = f"HTTP {r.status_code} via {m}"
        lines.append(f"{w.stem}: {txt}"); time.sleep(1)
    (d / "transcript.txt").write_text("\n".join(lines) + "\n"); print(d, *lines, sep="\n")
