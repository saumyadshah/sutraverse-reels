#!/usr/bin/env python3
"""Chat-style Reel v2 (26 Nov 2026): looks AND sounds like a real phone chat.
Usage: python3 otlo/toolkit/bin/chat_reel.py otlo/work/<slug>   # reads chat.json -> writes reel.html + script.json

chat.json
{
 "group": "ફેમિલી ગ્રુપ 🏠", "members": "Ba, Mummy, Pappa, Fai, Jay +9", "clock": "9:41",
 "caption": {"gu": "<pinned top caption, Gujarati, <= 28 chars>", "en": "<same idea in English, <= 40 chars>"},
 "cast": {"Ba": {"label": "બા", "color": "#A8322A", "voice": "Gacrux"}, "Pappa": {...}, ...},
 "beats": [                                    # one beat = one message = one voiced line (the first beat is the hook)
   {"from": "Ba", "type": "text", "gu": "...", "en": "...", "time": "9:12 PM",
    "say": "<what the voice says, Gujarati; defaults to gu>", "react": "😂 4", "reply_to": 0, "forwarded": false},
   {"from": "Ba", "type": "voice", "secs": "0:07", "gu": "<transcript>", "en": "..."},
   {"from": "Pappa", "type": "deleted"},       # "This message was deleted" (say: optional line)
   {"from": "narrator", "type": "end", "gu": "<one-line ask on screen>", "en": "...", "say": "..."}
 ],
 "narrator_voice": "Sulafat"
}
Writing rules (RUNBOOK 4B-chat): open on the most dramatic message, not a greeting; every beat must escalate,
reveal or twist; real chat texture (voice notes from elders, a forward, an emoji reaction, a deleted message,
someone replying to the wrong message); a payoff in the last two beats; 6-10 beats; 18-35 s in total.
Invented characters only; generic UI (no real app names or logos).
"""
import json, sys, pathlib, html

HERE = pathlib.Path(__file__).resolve().parent
d = pathlib.Path(sys.argv[1]); C = json.loads((d/'chat.json').read_text()); e = html.escape
CAST = C.get('cast', {}); NARR = C.get('narrator_voice', 'Sulafat')

CSS = """<style>
.cap{position:absolute;left:70px;right:70px;top:250px;text-align:center;z-index:5}
.cap .g{font:800 66px/1.05 'Anek Gujarati';color:var(--indigo)} .cap .x{font:800 44px/1 'Anek Gujarati';font-stretch:75%;text-transform:uppercase;color:var(--red);margin-top:8px}
.phone{position:absolute;left:105px;top:420px;width:870px;height:1060px;background:#0E0F12;border-radius:84px;padding:20px;box-sizing:border-box;box-shadow:0 26px 50px rgba(27,42,74,.28)}
.scr{position:relative;width:100%;height:100%;border-radius:66px;overflow:hidden;background:#EFE6D8;display:flex;flex-direction:column}
.notch{position:absolute;left:50%;top:12px;transform:translateX(-50%);width:180px;height:42px;background:#0E0F12;border-radius:26px;z-index:3}
.sb{height:70px;display:flex;align-items:flex-end;justify-content:space-between;padding:0 52px 6px;font:600 30px/1 'Anek Gujarati';color:#111;background:#F7F3EC}
.sb .ic{display:flex;gap:10px;align-items:center}
.hdr{display:flex;align-items:center;gap:18px;padding:12px 24px 14px;background:#F7F3EC;border-bottom:2px solid #E2D8C6}
.av{width:74px;height:74px;border-radius:50%;background:#E3A21A;display:flex;align-items:center;justify-content:center;font:800 40px 'Anek Gujarati';color:#1B2A4A;flex:none}
.gn{font:700 40px/1.1 'Anek Gujarati';color:#111}.gm{font:400 26px/1.2 'Rasa',serif;color:#6b6f76;margin-top:2px;white-space:nowrap;overflow:hidden;max-width:470px}
.gm.ty{color:#2E8B57;font-style:italic}
.wall{flex:1;position:relative;overflow:hidden;background-color:#EFE6D8;background-image:radial-gradient(#E2D6C2 2.5px,transparent 3px),radial-gradient(#E6DBC9 2px,transparent 2.5px);background-size:46px 46px,46px 46px;background-position:0 0,23px 23px}
.feed{position:absolute;left:0;right:0;bottom:0;display:flex;flex-direction:column;gap:14px;padding:18px 22px 22px}
.day{align-self:center;background:#FFF8E6;color:#6b6f76;font:600 24px 'Anek Gujarati';padding:6px 20px;border-radius:12px}
.m{position:relative;align-self:flex-start;max-width:640px;background:#fff;border-radius:0 24px 24px 24px;padding:10px 20px 8px;box-shadow:0 2px 0 rgba(0,0,0,.10);margin-left:12px}
.m:before{content:"";position:absolute;left:-13px;top:0;border-top:17px solid #fff;border-left:15px solid transparent}
.m .n{font:700 28px 'Anek Gujarati'} .m .t{font:600 46px/1.18 'Anek Gujarati';color:#111;margin-top:2px}
.m .tr{font:italic 400 29px/1.2 'Rasa',serif;color:#5d6470;margin-top:3px} .m .tm{font:400 22px 'Anek Gujarati';color:#8a8f98;text-align:right;margin-top:2px}
.m .fw{font:italic 400 24px 'Rasa',serif;color:#8a8f98;margin-bottom:2px}
.m .q{border-left:6px solid #2E8B57;background:#F1F6EE;border-radius:10px;padding:6px 12px;margin:4px 0 6px;font:500 28px/1.2 'Anek Gujarati';color:#4a5058}
.m .vn{display:flex;align-items:center;gap:14px;margin-top:4px}
.m .vn .pl{width:56px;height:56px;border-radius:50%;background:#2E8B57;display:flex;align-items:center;justify-content:center}
.m .vn .wv{display:flex;gap:4px;align-items:center;height:56px}
.m .vn .wv i{display:block;width:6px;border-radius:3px;background:#9fb3a5}
.m .del{font:italic 400 36px 'Rasa',serif;color:#8a8f98}
.m .rx{position:absolute;right:14px;bottom:-22px;background:#fff;border-radius:22px;padding:2px 12px;font:600 26px 'Anek Gujarati';box-shadow:0 2px 4px rgba(0,0,0,.15)}
.typ{align-self:flex-start;margin-left:12px;background:#fff;border-radius:0 22px 22px 22px;padding:16px 22px;display:flex;gap:8px}
.typ i{display:block;width:12px;height:12px;border-radius:50%;background:#9aa0a8}
.inp{display:flex;align-items:center;gap:16px;padding:14px 20px 26px;background:#F7F3EC}
.ibox{flex:1;height:76px;border-radius:40px;background:#fff;display:flex;align-items:center;padding:0 28px;font:400 30px 'Anek Gujarati';color:#9aa0a8}
.mic{width:76px;height:76px;border-radius:50%;background:#2E8B57;display:flex;align-items:center;justify-content:center}
.endq{position:absolute;left:90px;right:90px;top:540px;text-align:center}
</style>"""

ICONS = ('<span class="ic"><svg width="36" height="24" viewBox="0 0 40 26"><rect x="0" y="16" width="6" height="10" rx="1" fill="#111"/><rect x="10" y="11" width="6" height="15" rx="1" fill="#111"/><rect x="20" y="6" width="6" height="20" rx="1" fill="#111"/><rect x="30" y="0" width="6" height="26" rx="1" fill="#111"/></svg>'
         '<span>5G</span><svg width="50" height="26" viewBox="0 0 56 28"><rect x="1" y="1" width="48" height="26" rx="7" fill="none" stroke="#111" stroke-width="2.5"/><rect x="5" y="5" width="30" height="18" rx="4" fill="#111"/><rect x="51" y="9" width="4" height="10" rx="2" fill="#111"/></svg></span>')
MIC = '<svg width="28" height="40" viewBox="0 0 30 44"><rect x="8" y="2" width="14" height="26" rx="7" fill="#fff"/><path d="M3 20 Q3 34 15 34 Q27 34 27 20 M15 34 L15 42" stroke="#fff" stroke-width="3.5" fill="none"/></svg>'

def who(b):
    c = CAST.get(b.get('from'), {}); return c.get('label', b.get('from', '')), c.get('color', '#A8322A'), c.get('voice', NARR)

def bubble(b, i, beats, t_in=None):
    lab, col, _ = who(b); a = f' a" data-in="{t_in:.2f}" data-pop="1" data-origin="left top' if t_in is not None else ''
    inner = f'<div class="n" style="color:{col}">{e(lab)}</div>'
    if b.get('forwarded'): inner += '<div class="fw">↪ Forwarded many times</div>'
    if b.get('reply_to') is not None:
        q = beats[b['reply_to']]; inner += f'<div class="q">{e(who(q)[0])}: {e(q.get("gu","")[:38])}</div>'
    if b.get('type') == 'deleted':
        inner += '<div class="del">🚫 This message was deleted</div>'
    elif b.get('type') == 'voice':
        bars = ''.join(f'<i style="height:{h}px"></i>' for h in [14,26,40,22,34,48,30,18,38,26,44,20,32,16,28,40,24,14,30,22])
        inner += (f'<div class="vn"><div class="pl"><svg width="22" height="26" viewBox="0 0 22 26"><path d="M2 1 L21 13 L2 25 Z" fill="#fff"/></svg></div>'
                  f'<div class="wv">{bars}</div><span style="font:500 26px Anek Gujarati;color:#6b6f76">{e(b.get("secs","0:06"))}</span></div>'
                  f'<div class="t" style="font-size:40px">“{e(b["gu"])}”</div><div class="tr">{e(b.get("en",""))}</div>')
    else:
        inner += f'<div class="t">{e(b["gu"])}</div><div class="tr">{e(b.get("en",""))}</div>'
    inner += f'<div class="tm">{e(b.get("time",""))}</div>'
    if b.get('react'): inner += f'<div class="rx">{e(b["react"])}</div>'
    return f'<div class="m{a}">{inner}</div>'

def phone(s, beats, idx, typing_who=None):
    shown = [k for k in range(idx+1) if beats[k].get('type') != 'end'][-4:]
    feed = '<span class="day">આજે · Today</span>' if len(shown) < 4 else ''
    for k in shown:
        feed += bubble(beats[k], k, beats, (s+0.22) if k == idx else None)
    sub = f'<div class="gm ty">{e(typing_who)} is typing…</div>' if typing_who else f'<div class="gm">{e(C["members"])}</div>'
    return (f'<div class="phone"><div class="scr"><div class="notch"></div>'
            f'<div class="sb"><span>{e(C.get("clock","9:41"))}</span>{ICONS}</div>'
            f'<div class="hdr"><svg width="24" height="40" viewBox="0 0 26 44"><path d="M22 4 L4 22 L22 40" stroke="#1B2A4A" stroke-width="5" fill="none" stroke-linecap="round"/></svg>'
            f'<div class="av">{e(C["group"][:2])}</div><div><div class="gn">{e(C["group"])}</div>{sub}</div></div>'
            f'<div class="wall"><div class="feed">{feed}</div></div>'
            f'<div class="inp"><div class="ibox">Message</div><div class="mic">{MIC}</div></div></div></div>')

sk = (HERE.parent/'templates'/'reel-skeleton.html').read_text()
head = sk[:sk.index('<!-- S1: hook -->')].replace('</head>', CSS + '</head>')
beats = C['beats']; cap = C['caption']; out = []; lines = []; t = 0.0
for i, b in enumerate(beats):
    s = round(t, 2); e_ = round(t + 2.4, 2); t = e_
    if b.get('type') == 'end':
        out.append(f'<div class="scene" data-s="{s}" data-e="{e_}" style="padding:0">'
                   f'<div class="cap"><div class="g">{e(cap["gu"])}</div><div class="x">{e(cap["en"])}</div></div>'
                   f'<div class="endq"><div class="gu a" data-in="{s+0.05:.2f}" data-pop="1" data-origin="center" style="font-size:96px;color:var(--indigo)">{e(b["gu"])}</div>'
                   f'<div class="en a" data-in="{s+0.35:.2f}" style="font-size:70px;color:var(--red);margin-top:16px">{e(b.get("en",""))}</div>'
                   f'<div class="kick a" data-in="{s+0.6:.2f}" style="font-size:44px;margin-top:34px">@otlo.gujarat · ગુજરાતની વાતો, ઓટલા પર</div></div></div>')
        lines.append({"id": f"s{i+1}", "gu": b.get('say', b['gu']), "en": [b.get('en', '')], "voice": NARR, "lead": 0.12})
        continue
    nxt = beats[i+1] if i+1 < len(beats) and beats[i+1].get('type') != 'end' else None
    typing = who(nxt)[0] if nxt else None
    out.append(f'<div class="scene" data-s="{s}" data-e="{e_}" style="padding:0">'
               f'<div class="cap"><div class="g">{e(cap["gu"])}</div><div class="x">{e(cap["en"])}</div></div>'
               f'{phone(s, beats, i, typing)}</div>')
    say = b.get('say') or (b.get('gu') if b.get('type') != 'deleted' else '')
    if say:
        lines.append({"id": f"s{i+1}", "gu": say, "en": [], "voice": who(b)[2], "lead": 0.32, "tail": 0.25})
    else:   # a deleted message with nothing said still needs a short beat: a soft breath line by the narrator
        lines.append({"id": f"s{i+1}", "gu": "હમ્મ…", "en": [], "voice": NARR, "lead": 0.3})
body = '\n'.join(out)
(d/'reel.html').write_text(head.replace('<!-- S1: hook -->', '') + body + '\n</div>\n<script src="../../toolkit/runtime/otlo.js"></script>\n</body></html>')
S = {"voice": NARR, "direction": "", "lines": lines,
     "thumb": C.get('thumb', {"chip_gu": "ફેમિલી ગ્રુપ", "chip_en": "Family Group Chat", "gu": cap['gu'], "en": cap['en'],
                              "art_t": 2.0, "art_clip": [105, 420, 870, 700]})}
(d/'script.json').write_text(json.dumps(S, ensure_ascii=False, indent=1))
print("wrote reel.html + script.json:", len(out), "beats")
