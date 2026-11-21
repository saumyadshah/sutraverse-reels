#!/usr/bin/env python3
"""Otlo Reel builder. Run from repo root.
  python3 otlo/toolkit/bin/build.py render otlo/work/<slug>     # needs <slug>/reel.html, script.json, vo/s*.wav
  python3 otlo/toolkit/bin/build.py stills otlo/work/<slug> 1 4 9   # check stills at given seconds (original timeline)
Outputs in <slug>/: timing.json, score.wav, mix.wav, subs.ass, reel.mp4, cover.jpg, contact.jpg, qa.json
script.json: {"voice":"Kore","direction":"","lines":[{"id":"s1","gu":"<Gujarati VO>","en":["subtitle chunk 1","chunk 2"]},...]}
One line per scene, same order. Subtitle chunks: short (<= ~55 chars), plain English, no trailing commas needed."""
import sys, json, wave, subprocess, pathlib, asyncio, numpy as np
HERE = pathlib.Path(__file__).resolve().parent
SR = 44100; FPS = 30

def rd(p):
    w = wave.open(str(p)); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    if w.getnchannels() == 2: x = x.reshape(-1, 2)
    return x, w.getframerate()

def speech_bounds(p):
    x, sr = rd(p); x = x if x.ndim == 1 else x.mean(1); fr = int(sr * 0.05)
    e = np.array([np.sqrt(np.mean(x[k:k+fr]**2)) for k in range(0, len(x)-fr, fr)]); a = np.where(e > e.max()*0.05)[0]
    return float(a[0]*0.05), float((a[-1]+1)*0.05)

def orig_scenes(d):
    import re
    html = (d/'reel.html').read_text()
    return [(float(s), float(e)) for s, e in re.findall(r'class="scene"[^>]*data-s="([\d.]+)"\s+data-e="([\d.]+)"', html)]

def timing(d, S):
    orig = orig_scenes(d); n = len(S['lines'])
    if len(orig) != n: sys.exit(f"QA FAIL: {len(orig)} scenes in reel.html but {n} voice lines")
    starts, ends, vo, t = [], [], [], 0.0
    for i, ln in enumerate(S['lines']):
        p = d/'vo'/f"{ln['id']}.wav"; on, off = speech_bounds(p); lead = 0.5 if i == 0 else 0.35
        L = float(max(orig[i][1]-orig[i][0], lead + (off-on) + (1.6 if i == n-1 else 0.7)))
        starts.append(round(t, 3)); vo.append({"file": str(p), "at": round(t+lead-on, 3), "on": on, "off": off}); t += L; ends.append(round(t, 3))
    T = {"starts": starts, "ends": ends, "vo": vo}; (d/'timing.json').write_text(json.dumps(T, indent=1)); return T

async def frames(d, T, only=None):
    from playwright.async_api import async_playwright
    out = d/'frames'; out.mkdir(exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        await pg.goto((d/'reel.html').resolve().as_uri()); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(600)
        if only:
            for s in only:
                await pg.evaluate(f"window.render({s})"); await pg.screenshot(path=str(d/f'still_{s}.jpg'), type='jpeg', quality=88)
        else:
            for i in range(int(FPS*T['ends'][-1])):
                await pg.evaluate(f"window.renderTimed({i/FPS},{T['starts']},{T['ends']})")
                await pg.screenshot(path=str(out/f'f{i:05d}.jpg'), type='jpeg', quality=90)
        await b.close()

def music(d, T):
    DUR = T['ends'][-1]; N = int(SR*DUR); t = np.arange(N)/SR; out = np.zeros(N)
    def env(n, a, dk): x = np.arange(n)/SR; return np.minimum(x/a, 1)*np.exp(-x/dk)
    def pluck(f, st, dur=2.2, amp=.2, br=1.0):
        s = int(st*SR); n = min(int(dur*SR), N-s)
        if n <= 0: return
        x = np.arange(n)/SR; out[s:s+n] += amp*sum((br**k)*np.sin(2*np.pi*f*(k+1)*x)/(k+1) for k in range(6))*env(n, .004, dur/4)
    tt = 0.0
    while tt < DUR:
        for f in [220.0, 293.66, 293.66, 146.83]: pluck(f, tt, 3.0, .11, .8); tt += .75
    out += .035*(np.sin(2*np.pi*146.83*t)+.6*np.sin(2*np.pi*220*t))*np.minimum(t/2, 1)
    notes = {'S': 293.66, 'R': 329.63, 'G': 369.99, 'P': 440.0, 'D': 493.88, "S'": 587.33, "R'": 659.26}
    phr = [("S", 0), ("G", .5), ("P", 1), ("D", 1.5), ("P", 2), ("G", 2.5), ("R", 3), ("S", 3.5)]
    for st in [T['starts'][0]+1.0]+T['starts'][1:-1]:
        for nm, off in phr: pluck(notes[nm], st+off, 1.6, .09, .55); pluck(notes[nm]*2, st+off+.02, .8, .025, .4)
    e0 = T['starts'][-1]
    for nm, off in [("P", 0), ("D", .4), ("S'", .8), ("R'", 1.4), ("S'", 2.0)]: pluck(notes[nm], e0+off, 2.0, .1, .55)
    def bell(st, amp=.12):
        s = int(st*SR); n = min(int(3*SR), N-s); x = np.arange(n)/SR
        out[s:s+n] += amp*sum(a*np.sin(2*np.pi*f*x)*np.exp(-x*k) for f, a, k in [(1240, 1, 1.2), (2980, .5, 2), (4130, .3, 3), (1870, .4, 1.6)])*np.minimum(x/.002, 1)
    for b in [0.05]+T['starts'][1:]: bell(b)
    beat = 60/84; k = 0; x0 = .6
    while x0 < DUR-1:
        s = int(x0*SR); n = min(int(.35*SR), N-s); x = np.arange(n)/SR; f = 110*np.exp(-x*8)+55
        out[s:s+n] += (.16 if k % 4 in (0, 3) else .08)*np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-x*12); x0 += beat/2 if k % 4 == 2 else beat; k += 1
    out *= np.minimum(1, np.minimum(t/.4, (DUR-t)/1.5)); out /= np.max(np.abs(out))*1.15; out *= .55
    return np.stack([out, np.roll(out, 90)], 1).astype(np.float32)

def mix(d, T, m):
    N = len(m); v = np.zeros(N, np.float32)
    for c in T['vo']:
        x, s = rd(c['file']); x = x if x.ndim == 1 else x.mean(1)
        tt = np.arange(int(len(x)*SR/s))/SR; y = np.interp(tt, np.arange(len(x))/s, x).astype(np.float32)
        i = int(c['at']*SR); v[i:i+len(y)] += y[:max(0, N-i)]
    v /= np.max(np.abs(v))+1e-9
    envl = np.convolve(np.abs(v), np.ones(4410)/4410, 'same'); envl = np.clip(envl/.05, 0, 1); envl = np.convolve(envl, np.ones(8820)/8820, 'same')
    out = m*(1-.65*envl)[:, None]*.6+v[:, None]*.9; out /= np.max(np.abs(out))*1.05
    w = wave.open(str(d/'mix.wav'), 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out*32767).astype(np.int16).tobytes()); w.close()

def subs(d, T, S):
    f = lambda t: f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
    ev = []
    for c, ln in zip(T['vo'], S['lines']):
        s0 = c['at']+c['on']; s1 = c['at']+c['off']; ch = ln.get('en') or []; tot = sum(len(x) for x in ch) or 1; t = s0
        for x in ch:
            dd = (s1-s0)*len(x)/tot; ev.append([t, t+dd, x.replace('\n', ' ')]); t += dd
    for a, b in zip(ev, ev[1:]): a[1] = min(a[1], b[0]-.03)
    hdr = """[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 0\n\n[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Fira Sans SemiBold,46,&H00D6E9F3,&H00D6E9F3,&H004A2A1B,&H004A2A1B,0,0,0,0,100,100,0,0,3,16,0,2,110,110,40,1\n\n[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"""
    (d/'subs.ass').write_text(hdr+"\n".join(f"Dialogue: 0,{f(a)},{f(b)},Sub,,0,0,0,,{x}" for a, b, x in ev)+"\n")

def encode(d):
    fontsdir = HERE.parent/'fonts'
    vf = f"ass={d/'subs.ass'}:fontsdir={fontsdir}"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(d/'frames/f%05d.jpg'), "-i", str(d/'mix.wav'),
                    "-vf", vf, "-filter:a", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-shortest", "-movflags", "+faststart", str(d/'reel.mp4')], check=True)

def qa(d, T, S):
    from PIL import Image
    mids = [(s+e)/2 for s, e in zip(T['starts'], T['ends'])]
    ims = []
    for i, m in enumerate(mids):
        p = d/f'qa_{i+1}.jpg'; subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{m:.2f}", "-i", str(d/'reel.mp4'), "-frames:v", "1", "-vf", "scale=270:480", str(p)], check=True); ims.append(Image.open(p))
    c = Image.new('RGB', (270*len(ims), 480)); [c.paste(im, (i*270, 0)) for i, im in enumerate(ims)]; c.save(d/'contact.jpg')
    for p in d.glob('qa_*.jpg'): p.unlink()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{mids[0]:.2f}", "-i", str(d/'reel.mp4'), "-frames:v", "1", str(d/'cover.jpg')], check=True)
    lufs = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(d/'reel.mp4'), "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    import re; I = re.findall(r"I:\s+(-?[\d.]+) LUFS", lufs)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(d/'reel.mp4')], capture_output=True, text=True).stdout)
    chars = [len(l['gu']) for l in S['lines']]; speech = [c['off']-c['on'] for c in T['vo']]
    rate = [round(c/s, 1) for c, s in zip(chars, speech)]
    warn = [f"{l['id']}: {r} chars/s (normal 10-14) - possible leaked instruction or truncation, LISTEN" for l, r in zip(S['lines'], rate) if r < 8.5 or r > 17]
    rep = {"duration": round(dur, 1), "lufs": float(I[-1]) if I else None, "chars_per_sec": rate, "warnings": warn, "ok": not warn and 15 <= dur <= 90}
    (d/'qa.json').write_text(json.dumps(rep, indent=1)); print(json.dumps(rep, indent=1)); return rep

if __name__ == "__main__":
    cmd, d = sys.argv[1], pathlib.Path(sys.argv[2]).resolve()
    if cmd == "stills": asyncio.run(frames(d, None, [float(x) for x in sys.argv[3:]])); sys.exit()
    S = json.loads((d/'script.json').read_text())
    T = timing(d, S); print("scenes", T['starts'], T['ends'])
    import shutil; shutil.rmtree(d/'frames', ignore_errors=True)
    asyncio.run(frames(d, T)); mix(d, T, music(d, T)); subs(d, T, S); encode(d); qa(d, T, S)
