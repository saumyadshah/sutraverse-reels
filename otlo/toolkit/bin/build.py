#!/usr/bin/env python3
"""Otlo Reel builder. Run from repo root.
  python3 otlo/toolkit/bin/build.py render otlo/work/<slug>     # needs <slug>/reel.html, script.json, vo/s*.wav
  python3 otlo/toolkit/bin/build.py stills otlo/work/<slug> 1 4 9   # check stills at given seconds (original timeline)
Outputs in <slug>/: timing.json, mix.wav, subs.ass, thumb.png/thumb.jpg, reel.mp4 (thumbnail = first frame), contact.jpg, qa.json\n  python3 otlo/toolkit/bin/build.py carousel otlo/work/<slug>   # needs carousel.html -> slide_NN.jpg, contact.jpg, qa.json
  python3 otlo/toolkit/bin/build.py thumb otlo/work/<slug>      # thumbnail only
script.json: {"voice":"Kore","direction":"","lines":[{"id":"s1","gu":"<Gujarati VO>","en":["subtitle chunk 1","chunk 2"]},...]}
One line per scene, same order. Optional "thumb": {"chip_gu","chip_en","gu","en","ribbon_gu","ribbon_en","art_t":sec,"art_clip":[x,y,w,h],"gu_size","en_size"}. Subtitle chunks: short (<= ~55 chars), plain English, no trailing commas needed."""
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
    if is_slideshow(d):
        n = len(sorted(d.glob('slide_*.png'))); return [(i*4.5, (i+1)*4.5) for i in range(n)]
    html = (d/'reel.html').read_text()
    return [(float(s), float(e)) for s, e in re.findall(r'class="scene"[^>]*data-s="([\d.]+)"\s+data-e="([\d.]+)"', html)]

def is_slideshow(d):
    return (d/'carousel.html').exists() and not (d/'reel.html').exists()

def slideshow_frames(d, T):
    """Swipe-style Reel: each carousel slide (1080x1350) sits on the branded 1080x1920 stage with a slow push-in,
    a 0.3 s slide-in between slides, and the bottom kept clear for subtitles. Also writes thumb.png (slide 1 = cover)."""
    from PIL import Image, ImageDraw
    out = d/'frames'; out.mkdir(exist_ok=True)
    IV, IN, RD, HD = (243, 233, 214), (27, 42, 74), (168, 50, 42), (227, 162, 26)
    bg = Image.new('RGB', (1080, 1920), IV); dr = ImageDraw.Draw(bg)
    for y0 in (0, 1884):
        dr.rectangle([0, y0, 1080, y0+36], fill=IN)
        for x in range(0, 1080, 36):
            dr.polygon([(x+18, y0+4), (x+32, y0+18), (x+18, y0+32), (x+4, y0+18)], fill=RD)
            dr.polygon([(x+18, y0+11), (x+25, y0+18), (x+18, y0+25), (x+11, y0+18)], fill=HD)
    slides = [Image.open(p).convert('RGB') for p in sorted(d.glob('slide_*.png'))]
    W, H, X, Y = 1000, 1250, 40, 250          # slide box on the stage; subtitles live below y=1520 area (MarginV)
    base = [s.resize((W, H), Image.LANCZOS) for s in slides]
    def frame(i, local, dur):
        k = 1 + 0.025*min(1, local/max(dur, .1))       # slow push-in
        im = slides[i].resize((int(W*k), int(H*k)), Image.LANCZOS)
        cx, cy = (im.width-W)//2, (im.height-H)//2; im = im.crop((cx, cy, cx+W, cy+H))
        f = bg.copy(); f.paste(im, (X, Y))
        if i > 0 and local < 0.3:                        # previous slide slides out to the left
            t = local/0.3; e = 1-(1-t)**3; off = int(-W*1.1*e)
            f = bg.copy(); f.paste(base[i-1], (X+off, Y)); f.paste(im, (X+off+int(W*1.1), Y))
        return f
    n = int(FPS*T['ends'][-1])
    for fi in range(n):
        t = fi/FPS; i = max(k for k in range(len(T['starts'])) if t >= T['starts'][k])
        frame(min(i, len(slides)-1), t-T['starts'][i], T['ends'][i]-T['starts'][i]).save(out/f'f{fi:05d}.png', compress_level=1)
    c = bg.copy(); c.paste(base[0], (X, Y)); c.save(d/'thumb.png'); c.save(d/'thumb.jpg', quality=95, subsampling=0)

def timing(d, S):
    orig = orig_scenes(d); n = len(S['lines'])
    if len(orig) != n: sys.exit(f"QA FAIL: {len(orig)} scenes in reel.html but {n} voice lines")
    starts, ends, vo, t = [], [], [], 0.0
    for i, ln in enumerate(S['lines']):
        p = d/'vo'/f"{ln['id']}.wav"
        sp = float(S.get('speed', 1.0))
        if abs(sp - 1.0) > 0.01:   # pitch-preserving tempo change (ffmpeg atempo), cached in vo_fast/; keep 1.0-1.2
            q = d/'vo_fast'/f"{ln['id']}.wav"; q.parent.mkdir(exist_ok=True)
            if not q.exists() or q.stat().st_mtime < p.stat().st_mtime:
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(p), "-filter:a", f"atempo={sp}", str(q)], check=True)
            p = q
        on, off = speech_bounds(p); lead = 0.06 if i == 0 else float(ln.get('lead', 0.18))
        L = float(max(1.6, lead + (off-on) + (0.9 if i == n-1 else float(ln.get('tail', 0.3)))))
        starts.append(round(t, 3)); vo.append({"file": str(p), "at": round(t+lead-on, 3), "on": on, "off": off}); t += L; ends.append(round(t, 3))
    T = {"starts": starts, "ends": ends, "vo": vo}; (d/'timing.json').write_text(json.dumps(T, indent=1)); return T


# --- local http server so ES modules (Three.js) load; file:// blocks module imports (28 Nov) ---
_SRV = None
def page_url(path):
    global _SRV
    import threading, functools, http.server, socketserver
    root = pathlib.Path(__file__).resolve().parents[3]
    if _SRV is None:
        class Q(http.server.SimpleHTTPRequestHandler):
            def log_message(self, *a): pass
        h = functools.partial(Q, directory=str(root))
        _SRV = socketserver.ThreadingTCPServer(('127.0.0.1', 0), h); _SRV.daemon_threads = True
        threading.Thread(target=_SRV.serve_forever, daemon=True).start()
    return f"http://127.0.0.1:{_SRV.server_address[1]}/" + str(pathlib.Path(path).resolve().relative_to(root))
CHROME_ARGS = ['--enable-unsafe-swiftshader', '--use-angle=swiftshader', '--ignore-gpu-blocklist', '--enable-webgl']
async def wait_ready(pg):
    await pg.evaluate("document.fonts.ready")
    await pg.wait_for_timeout(600)
    if await pg.evaluate("!!document.querySelector('canvas.fx3d')"):
        await pg.wait_for_function("window.OTLO3D_READY === true", timeout=20000)
        await pg.evaluate("window.render(0)")

async def frames(d, T, only=None):
    from playwright.async_api import async_playwright
    out = d/'frames'; out.mkdir(exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(args=CHROME_ARGS); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        await pg.goto(page_url(d/'reel.html')); await wait_ready(pg)
        if only:
            for s in only:
                await pg.evaluate(f"window.render({s})"); await pg.screenshot(path=str(d/f'still_{s}.jpg'), type='jpeg', quality=88)
        else:
            # safe-zone check: text must stay clear of Instagram's UI (bottom 440 px, right 170 px below y=1000)
            # and inside the 3:4 grid crop (y 240-1680) for anything that carries the message
            warn = []
            for k, (os_, oe) in enumerate(orig_scenes(d)):
                await pg.evaluate(f"window.render({oe-0.4})")
                bad = await pg.evaluate('''() => [...document.querySelectorAll('.scene')].filter(s => s.style.display !== 'none')
                  .flatMap(s => [...s.querySelectorAll('.gu,.en,.kick,.body,.chip,.box,.cap,.m')]).filter(e => !e.closest('.endcard'))
                  .map(e => { const r = e.getBoundingClientRect(); return {c: e.className, t: (e.innerText||'').slice(0,24), b: r.bottom, r: r.right, top: r.top}; })
                  .filter(o => o.b > 1482 || (o.r > 912 && o.b > 1000) || o.top < 236)
                  .concat([...document.querySelectorAll('.scene')].filter(s => s.style.display !== 'none')
                  .flatMap(s => [...s.querySelectorAll('.art svg, .art img, img.photo, .art canvas')]).map(e => { const r = (e.closest('.kbframe') || e).getBoundingClientRect(); return {c: 'art', t: 'art/image', b: r.bottom, r: r.right, top: r.top}; })
                  .filter(o => o.b > 1366 && o.top < 1480))''')
                for o in bad[:3]: warn.append(f"scene {k+1}: '{o['t']}' " + ('runs into the subtitle band (art must end above y 1,366)' if o['c'] == 'art' else 'outside safe zone') + f" (top {o['top']:.0f}, bottom {o['b']:.0f}, right {o['r']:.0f})")
            (d/'safezone.json').write_text(json.dumps(warn))
            for i in range(int(FPS*T['ends'][-1])):
                await pg.evaluate(f"window.renderTimed({i/FPS},{T['starts']},{T['ends']})")
                await pg.screenshot(path=str(out/f'f{i:05d}.png'), type='png')
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
    rng = np.random.default_rng(7); x0 = .3
    while x0 < DUR-.5:                                   # shaker on 8ths: drive without clutter
        s0 = int(x0*SR); n = min(int(.06*SR), N-s0)
        out[s0:s0+n] += .05*rng.standard_normal(n)*np.exp(-np.arange(n)/SR*60); x0 += 60/84/2
    out *= np.minimum(1, np.minimum(t/.15, (DUR-t)/1.0)); out /= np.max(np.abs(out))*1.15; out *= .5
    for kind, at in sfx_events(d, T):                    # sound design: whoosh on cuts, pop on reveals, ping on messages
        s0 = int(at*SR)
        if s0 >= N: continue
        if kind == 'whoosh':
            n = min(int(.32*SR), N-s0); x = np.arange(n)/SR; nz = rng.standard_normal(n)
            env_ = np.sin(np.pi*np.clip(x/.32, 0, 1))**2; nz = np.convolve(nz, np.ones(12)/12, 'same')
            out[s0:s0+n] += .55*nz*env_
        elif kind == 'pop':
            n = min(int(.09*SR), N-s0); x = np.arange(n)/SR
            out[s0:s0+n] += .35*np.sin(2*np.pi*(900-5000*x)*x)*np.exp(-x*45)
        elif kind == 'ping':
            n = min(int(.35*SR), N-s0); x = np.arange(n)/SR
            out[s0:s0+n] += .30*(np.sin(2*np.pi*1568*x)+.5*np.sin(2*np.pi*2093*x))*np.exp(-x*14)
    return np.stack([out, np.roll(out, 90)], 1).astype(np.float32)

def sfx_events(d, T):
    """Map element reveal times (data-in, original timeline) to the voiced timeline."""
    import re
    if is_slideshow(d): return [('whoosh', THUMB_LEAD*0+s) for s in T['starts'][1:]]
    html = (d/'reel.html').read_text(); orig = orig_scenes(d); ev = [('whoosh', s) for s in T['starts'][1:]]
    for i, m in enumerate(re.finditer(r'class="scene"[^>]*data-s="([\d.]+)"\s+data-e="([\d.]+)"', html)):
        if i >= len(T['starts']): break
        seg_end = html.find('class="scene"', m.end()); seg = html[m.end(): seg_end if seg_end > 0 else len(html)]
        os_, oe = orig[i]; ol = oe-os_; nl = T['ends'][i]-T['starts'][i]; k = nl/ol if nl < ol else 1.0
        for cls, tin in re.findall(r'class="([^"]*\ba\b[^"]*)"[^>]*data-in="([\d.]+)"', seg):
            at = T['starts'][i] + (float(tin)-os_)*k
            if at < T['starts'][i] + 0.12 and i > 0: continue
            ev.append(('ping' if re.search(r'\bm\b', cls) else 'pop', max(0.0, at)))
    return ev

def mix(d, T, m):
    N = len(m); v = np.zeros(N, np.float32)
    for c in T['vo']:
        x, s = rd(c['file']); x = x if x.ndim == 1 else x.mean(1)
        tt = np.arange(int(len(x)*SR/s))/SR; y = np.interp(tt, np.arange(len(x))/s, x).astype(np.float32)
        i = int(c['at']*SR)
        if i < 0: y = y[-i:]; i = 0
        n = max(0, min(len(y), N-i)); v[i:i+n] += y[:n]
    v /= np.max(np.abs(v))+1e-9
    envl = np.convolve(np.abs(v), np.ones(4410)/4410, 'same'); envl = np.clip(envl/.05, 0, 1); envl = np.convolve(envl, np.ones(8820)/8820, 'same')
    out = m*(1-.65*envl)[:, None]*.6+v[:, None]*.9; out /= np.max(np.abs(out))*1.05
    w = wave.open(str(d/'mix.wav'), 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out*32767).astype(np.int16).tobytes()); w.close()

def subs(d, T, S):
    f = lambda t: f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
    ev = []
    for c, ln in zip(T['vo'], S['lines']):
        s0 = c['at']+c['on']; s1 = c['at']+c['off']; ch = []
        for x in (ln.get('en') or []):
            w, cur = x.split(), ''
            for word in w:
                if len(cur)+len(word)+1 > 32 and cur: ch.append(cur); cur = word
                else: cur = (cur+' '+word).strip()
            if cur: ch.append(cur)
        tot = sum(len(x) for x in ch) or 1; t = s0
        for x in ch:
            dd = (s1-s0)*len(x)/tot; ev.append([t, t+dd, x.replace('\n', ' ')]); t += dd
    for a, b in zip(ev, ev[1:]): a[1] = min(a[1], b[0]-.03)
    hdr = """[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 0\n\n[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Fira Sans SemiBold,58,&H00FFFFFF,&H00FFFFFF,&H004A2A1B,&H004A2A1B,0,0,0,0,100,100,0,0,3,18,0,2,90,170,450,1\n\n[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"""
    if is_slideshow(d): hdr = hdr.replace(",2,90,170,450,1", ",2,90,170,440,1")
    (d/'subs.ass').write_text(hdr+"\n".join(f"Dialogue: 0,{f(a)},{f(b)},Sub,,0,0,0,,{x}" for a, b, x in ev)+"\n")

THUMB_LEAD = 1/30  # the designed thumbnail is the very first frame only (Instagram's API cover = first frame); the hook starts on frame 2

async def thumbnail(d, S):
    """Render thumb.png/thumb.jpg (1080x1920) from script.json "thumb" and an art crop of the Reel."""
    from playwright.async_api import async_playwright
    th = dict(S.get('thumb') or {})
    if not th.get('gu'): th['gu'] = S['lines'][0]['gu'][:24]
    t = float(th.get('art_t', 3.0)); clip = th.get('art_clip', [0, 820, 1080, 1060])
    if (d/'cover.html').exists():   # brand standard: a designed cover page (1080x1920) wins over the generic template
        async with async_playwright() as p:
            b = await p.chromium.launch(args=CHROME_ARGS); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
            await pg.goto(page_url(d/'cover.html')); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(900)
            await pg.screenshot(path=str(d/'thumb.png'), type='png'); await b.close()
        from PIL import Image
        Image.open(d/'thumb.png').convert('RGB').save(d/'thumb.jpg', quality=95, subsampling=0); return
    async with async_playwright() as p:
        b = await p.chromium.launch(args=CHROME_ARGS); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        await pg.goto(page_url(d/'reel.html')); await wait_ready(pg)
        await pg.evaluate(f"window.render({t})"); await pg.wait_for_timeout(100)
        await pg.screenshot(path=str(d/'thumb_art.png'), type='png', clip={'x': clip[0], 'y': clip[1], 'width': clip[2], 'height': clip[3]})
        await pg.goto(page_url(HERE.parent/'templates'/'thumb.html')); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(400)
        th['art'] = page_url(d/'thumb_art.png')
        await pg.evaluate("d=>window.fill(d)", th); await pg.wait_for_timeout(500)
        await pg.screenshot(path=str(d/'thumb.png'), type='png')
        await b.close()
    from PIL import Image
    Image.open(d/'thumb.png').convert('RGB').save(d/'thumb.jpg', quality=95, subsampling=0)

def encode(d):
    """Highest-quality master for Instagram: 1080x1920, 30 fps, H.264 High@4.2 at ~12 Mb/s (Instagram re-encodes, so a rich master keeps its copy crisp),
    BT.709 colour, AAC 256 kb/s 48 kHz, -14 LUFS. Thumbnail held for THUMB_LEAD s as the cover frame."""
    fontsdir = HERE.parent/'fonts'; ms = int(THUMB_LEAD*1000)
    fc = (f"[0:v]ass={d/'subs.ass'}:fontsdir={fontsdir}[main];"
          f"[1:v]fps={FPS},trim=end_frame=1,setpts=PTS-STARTPTS[th];"
          f"[th][main]concat=n=2:v=1:a=0,scale=1080:1920:flags=lanczos+accurate_rnd+full_chroma_int:out_color_matrix=bt709:out_range=tv,format=yuv420p[v];"
          f"[2:a]adelay={ms}|{ms},loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]")
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(d/'frames/f%05d.png'),
                    "-loop", "1", "-framerate", str(FPS), "-i", str(d/'thumb.png'), "-i", str(d/'mix.wav'),
                    "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-r", str(FPS),
                    "-c:v", "libx264", "-profile:v", "high", "-level:v", "4.2", "-preset", "slow", "-tune", "animation",
                    "-b:v", "12M", "-minrate", "12M", "-maxrate", "12M", "-bufsize", "12M", "-x264-params", "nal-hrd=cbr:force-cfr=1", "-g", "60", "-bf", "2",
                    "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
                    "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-shortest", "-movflags", "+faststart", str(d/'reel.mp4')], check=True)

def qa(d, T, S):
    from PIL import Image
    mids = [THUMB_LEAD+(s+e)/2 for s, e in zip(T['starts'], T['ends'])]
    ims = []
    for i, m in enumerate(mids):
        p = d/f'qa_{i+1}.jpg'; subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-ss", f"{m:.2f}", "-i", str(d/'reel.mp4'), "-frames:v", "1", "-vf", "scale=270:480", str(p)], check=True); ims.append(Image.open(p))
    c = Image.new('RGB', (270*len(ims), 480)); [c.paste(im, (i*270, 0)) for i, im in enumerate(ims)]; c.save(d/'contact.jpg')
    # review aids: the same frames with Instagram's UI zones shaded, and the 3:4 profile-grid crop
    from PIL import ImageDraw
    ov = c.convert('RGBA'); lay = Image.new('RGBA', ov.size, (0, 0, 0, 0)); dr = ImageDraw.Draw(lay); f = 270/1080
    for i in range(len(ims)):
        x0 = i*270; dr.rectangle([x0, int(1480*f), x0+270, 480], fill=(255, 0, 0, 70)); dr.rectangle([x0+int(912*f), int(1000*f), x0+270, 480], fill=(255, 0, 0, 70))
        dr.rectangle([x0, int(240*f), x0+269, int(1680*f)], outline=(0, 120, 255, 255), width=2)
    Image.alpha_composite(ov, lay).convert('RGB').save(d/'contact_safezones.jpg')
    for p in d.glob('qa_*.jpg'): p.unlink()
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-i", str(d/'reel.mp4'), "-frames:v", "1", "-q:v", "2", str(d/'first_frame.jpg')], check=True)
    lufs = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", str(d/'reel.mp4'), "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    import re; I = re.findall(r"I:\s+(-?[\d.]+) LUFS", lufs)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(d/'reel.mp4')], capture_output=True, text=True).stdout)
    chars = [len(l['gu']) for l in S['lines']]; speech = [c['off']-c['on'] for c in T['vo']]
    rate = [round(c/s, 1) for c, s in zip(chars, speech)]
    warn = [f"{l['id']}: {r} chars/s (normal 10-14) - possible leaked instruction or truncation, LISTEN" for l, r in zip(S['lines'], rate) if (r < 8.5 or r > 17) and len(l['gu']) >= 25]   # very short chat lines ("હું તો આવું જ!") naturally run fast/slow
    vs = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,codec_name,profile,bit_rate,r_frame_rate,pix_fmt", "-of", "json", str(d/'reel.mp4')], capture_output=True, text=True).stdout)["streams"][0]
    if (vs.get("width"), vs.get("height")) != (1080, 1920): warn.append(f"resolution {vs.get('width')}x{vs.get('height')}, expected 1080x1920")
    if dur > 40: warn.append(f"duration {dur:.0f}s: over the 40 s ceiling (target 18-35 s)")
    sz = d/'safezone.json'
    if sz.exists(): warn += json.loads(sz.read_text())
    rep = {"video": vs, "duration": round(dur, 1), "lufs": float(I[-1]) if I else None, "chars_per_sec": rate, "warnings": warn, "ok": not warn and 15 <= dur <= 90}
    (d/'qa.json').write_text(json.dumps(rep, indent=1)); print(json.dumps(rep, indent=1)); return rep

async def carousel(d):
    """Render each <section class="slide"> of carousel.html to slide_NN.png + slide_NN.jpg (1080x1350, JPEG q95 4:4:4)."""
    from playwright.async_api import async_playwright
    from PIL import Image
    for old in d.glob('slide_*'): old.unlink()
    async with async_playwright() as p:
        b = await p.chromium.launch(args=CHROME_ARGS); pg = await b.new_page(viewport={'width': 1080, 'height': 1350})
        await pg.goto(page_url(d/'carousel.html')); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(700)
        els = await pg.query_selector_all('section.slide')
        for i, el in enumerate(els, 1):
            await el.screenshot(path=str(d/f'slide_{i:02d}.png'), type='png')
        await b.close()
    paths = sorted(d.glob('slide_*.png')); warn = []
    for q in paths:
        im = Image.open(q).convert('RGB')
        if im.size != (1080, 1350): warn.append(f"{q.name} is {im.size}, expected 1080x1350")
        im.save(q.with_suffix('.jpg'), quality=95, subsampling=0)
    if not 2 <= len(paths) <= 10: warn.append(f"{len(paths)} slides (need 2-10)")
    cols = 5; rows = (len(paths)+cols-1)//cols; c = Image.new('RGB', (216*cols, 270*rows), 'white')
    for i, q in enumerate(paths): c.paste(Image.open(q).convert('RGB').resize((216, 270)), ((i % cols)*216, (i//cols)*270))
    c.save(d/'contact.jpg')
    rep = {"slides": len(paths), "warnings": warn, "ok": not warn}; (d/'qa.json').write_text(json.dumps(rep, indent=1)); print(json.dumps(rep, indent=1))

if __name__ == "__main__":
    cmd, d = sys.argv[1], pathlib.Path(sys.argv[2]).resolve()
    if cmd == "carousel": asyncio.run(carousel(d)); sys.exit()
    if cmd == "thumb": asyncio.run(thumbnail(d, json.loads((d/'script.json').read_text()))); sys.exit()
    if cmd == "stills": asyncio.run(frames(d, None, [float(x) for x in sys.argv[3:]])); sys.exit()
    S = json.loads((d/'script.json').read_text())
    if is_slideshow(d): asyncio.run(carousel(d))
    T = timing(d, S); print("scenes", T['starts'], T['ends'])
    import shutil; shutil.rmtree(d/'frames', ignore_errors=True)
    if is_slideshow(d): slideshow_frames(d, T)
    else: asyncio.run(frames(d, T)); asyncio.run(thumbnail(d, S))
    mix(d, T, music(d, T)); subs(d, T, S); encode(d); qa(d, T, S)
