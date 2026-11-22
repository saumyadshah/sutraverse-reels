#!/usr/bin/env python3
"""Build reel.html for a chat-style Reel (Family Group Chat etc.) that looks like a real phone chat.
Usage: python3 otlo/toolkit/bin/chat_reel.py otlo/work/<slug>     # reads chat.json, writes reel.html
chat.json:
{
 "group": "ફેમિલી ગ્રુપ", "members": "Ba, Mummy, Pappa, Fai, Jay +9", "clock": "7:20",
 "hook": {"chip": "ફેમિલી ગ્રુપ ચેટ · Family Group Chat", "gu": "...", "en": "...", "art_svg": "<svg ...>...</svg>"},
 "scenes": [                      # one per voice line between hook and end card
   {"msgs": [{"from": "બા · Ba", "color": "#A8322A", "gu": "...", "en": "...", "time": "7:02 PM"}],
    "typing": "Pappa is typing…", "seen": "Seen by 14 · no replies"}   # typing/seen optional
 ],
 "end": {"question": "તમારા ઘરે ...? · Who ...?", "next": "Dev Diwali guide · Mon 1 PM"}
}
Messages accumulate like a real chat: earlier messages stay visible above and scroll off the top; new ones pop in.
Rules: invented characters only; no real app names/logos (generic chat UI); keep each message short (<= 40 Gujarati chars).
"""
import json, sys, pathlib, html

HERE = pathlib.Path(__file__).resolve().parent
d = pathlib.Path(sys.argv[1]); C = json.loads((d/'chat.json').read_text())
e = html.escape

CSS = """<style>
.phone{position:absolute;left:90px;top:110px;width:900px;height:1610px;background:#0E0F12;border-radius:96px;padding:22px;box-sizing:border-box;box-shadow:0 30px 60px rgba(27,42,74,.28)}
.scr{position:relative;width:100%;height:100%;border-radius:76px;overflow:hidden;background:#EFE6D8;display:flex;flex-direction:column}
.notch{position:absolute;left:50%;top:14px;transform:translateX(-50%);width:200px;height:46px;background:#0E0F12;border-radius:30px;z-index:3}
.sb{height:78px;display:flex;align-items:flex-end;justify-content:space-between;padding:0 58px 8px;font:600 34px/1 'Anek Gujarati',sans-serif;color:#111;background:#F7F3EC}
.sb .ic{display:flex;gap:12px;align-items:center}
.hdr{display:flex;align-items:center;gap:20px;padding:16px 28px 18px;background:#F7F3EC;border-bottom:2px solid #E2D8C6}
.av{width:86px;height:86px;border-radius:50%;background:#E3A21A;display:flex;align-items:center;justify-content:center;font:800 48px 'Anek Gujarati';color:#1B2A4A;flex:none}
.gn{font:700 44px/1.1 'Anek Gujarati';color:#111}.gm{font:400 28px/1.2 'Rasa',serif;color:#6b6f76;margin-top:4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:520px}
.gm.ty{color:#2E8B57;font-style:italic}
.hicons{margin-left:auto;display:flex;gap:30px}
.wall{flex:1;position:relative;overflow:hidden;background-color:#EFE6D8;
 background-image:radial-gradient(#E2D6C2 2.5px,transparent 3px),radial-gradient(#E6DBC9 2px,transparent 2.5px);background-size:46px 46px,46px 46px;background-position:0 0,23px 23px}
.feed{position:absolute;left:0;right:0;bottom:0;display:flex;flex-direction:column;gap:16px;padding:20px 26px 26px}
.day{align-self:center;background:#FFF8E6;color:#6b6f76;font:600 26px 'Anek Gujarati';padding:8px 22px;border-radius:14px;box-shadow:0 1px 0 rgba(0,0,0,.08)}
.m{position:relative;align-self:flex-start;max-width:640px;background:#fff;border-radius:0 26px 26px 26px;padding:12px 22px 10px;box-shadow:0 2px 0 rgba(0,0,0,.10);margin-left:14px}
.m:before{content:"";position:absolute;left:-14px;top:0;border-top:18px solid #fff;border-left:16px solid transparent}
.m .n{font:700 30px 'Anek Gujarati'}.m .t{font:600 50px/1.18 'Anek Gujarati';color:#111;margin-top:2px}
.m .tr{font:italic 400 32px/1.2 'Rasa',serif;color:#5d6470;margin-top:4px}.m .tm{font:400 24px 'Anek Gujarati';color:#8a8f98;text-align:right;margin-top:2px}
.seen2{align-self:flex-end;font:italic 400 30px 'Rasa',serif;color:#7b8089;margin-right:10px}
.inp{display:flex;align-items:center;gap:18px;padding:16px 22px 30px;background:#F7F3EC}
.box{flex:1;height:84px;border-radius:44px;background:#fff;display:flex;align-items:center;padding:0 32px;font:400 34px 'Anek Gujarati';color:#9aa0a8;gap:18px}
.mic{width:84px;height:84px;border-radius:50%;background:#2E8B57;display:flex;align-items:center;justify-content:center}
</style>"""

def icons():
    return ('<span class="ic"><svg width="40" height="26" viewBox="0 0 40 26"><rect x="0" y="16" width="6" height="10" rx="1" fill="#111"/><rect x="10" y="11" width="6" height="15" rx="1" fill="#111"/><rect x="20" y="6" width="6" height="20" rx="1" fill="#111"/><rect x="30" y="0" width="6" height="26" rx="1" fill="#111"/></svg>'
            '<span>5G</span><svg width="56" height="28" viewBox="0 0 56 28"><rect x="1" y="1" width="48" height="26" rx="7" fill="none" stroke="#111" stroke-width="2.5"/><rect x="5" y="5" width="34" height="18" rx="4" fill="#111"/><rect x="51" y="9" width="4" height="10" rx="2" fill="#111"/></svg></span>')

HDR_ICONS = ('<span class="hicons"><svg width="54" height="40" viewBox="0 0 54 40"><rect x="1" y="6" width="36" height="28" rx="7" fill="none" stroke="#1B2A4A" stroke-width="4"/><path d="M37 15 L52 6 L52 34 L37 25 Z" fill="#1B2A4A"/></svg>'
             '<svg width="40" height="40" viewBox="0 0 40 40"><path d="M9 3 L16 3 L19 12 L14 16 Q18 25 24 26 L28 21 L37 24 L37 31 Q36 37 30 37 Q4 34 3 9 Q3 3 9 3Z" fill="#1B2A4A"/></svg>'
             '<svg width="12" height="40" viewBox="0 0 12 40"><circle cx="6" cy="6" r="4.5" fill="#1B2A4A"/><circle cx="6" cy="20" r="4.5" fill="#1B2A4A"/><circle cx="6" cy="34" r="4.5" fill="#1B2A4A"/></svg></span>')

def msg(m, t_in=None):
    a = f' a" data-in="{t_in:.2f}" data-pop="1" data-origin="left top' if t_in is not None else ''
    return (f'<div class="m{a}"><div class="n" style="color:{e(m.get("color","#A8322A"))}">{e(m["from"])}</div>'
            f'<div class="t">{e(m["gu"])}</div><div class="tr">{e(m.get("en",""))}</div><div class="tm">{e(m.get("time",""))}</div></div>')

def phone(s, history, new, typing=None, seen=None):
    feed = '<span class="day">આજે · Today</span>' + ''.join(msg(m) for m in history)
    t = s + 0.45
    for m in new: feed += msg(m, t); t += 1.25
    if seen: feed += f'<div class="seen2 a" data-in="{t:.2f}">{e(seen)}</div>'
    sub = f'<div class="gm ty">{e(typing)}</div>' if typing else f'<div class="gm">{e(C["members"])}</div>'
    return (f'<div class="phone"><div class="scr"><div class="notch"></div>'
            f'<div class="sb"><span>{e(C.get("clock","7:20"))}</span>{icons()}</div>'
            f'<div class="hdr"><svg width="26" height="44" viewBox="0 0 26 44"><path d="M22 4 L4 22 L22 40" stroke="#1B2A4A" stroke-width="5" fill="none" stroke-linecap="round"/></svg>'
            f'<div class="av">{e(C["group"][:2])}</div><div><div class="gn">{e(C["group"])}</div>{sub}</div>{HDR_ICONS}</div>'
            f'<div class="wall"><div class="feed">{feed}</div></div>'
            f'<div class="inp"><div class="box"><svg width="40" height="40" viewBox="0 0 40 40"><circle cx="20" cy="20" r="17" fill="none" stroke="#9aa0a8" stroke-width="3"/><circle cx="14" cy="16" r="2.5" fill="#9aa0a8"/><circle cx="26" cy="16" r="2.5" fill="#9aa0a8"/><path d="M12 25 Q20 32 28 25" stroke="#9aa0a8" stroke-width="3" fill="none"/></svg>Message</div>'
            f'<div class="mic"><svg width="30" height="44" viewBox="0 0 30 44"><rect x="8" y="2" width="14" height="26" rx="7" fill="#fff"/><path d="M3 20 Q3 34 15 34 Q27 34 27 20 M15 34 L15 42" stroke="#fff" stroke-width="3.5" fill="none"/></svg></div></div>'
            f'</div></div>')

sk = (HERE.parent/'templates'/'reel-skeleton.html').read_text()
head = sk[:sk.index('<!-- S1: hook -->')].replace('</head>', CSS + '</head>')
end = sk[sk.index('<!-- END CARD (keep) -->'):sk.index('</div>\n<script src=')]
H = C['hook']; n = len(C['scenes']); t0 = 5.0
out = [f'''<!-- S1: hook -->
<div class="scene" data-s="0" data-e="5">
  <span class="chip a" data-in="0.1">{e(H["chip"])}</span>
  <div class="gu a" data-in="0.35" data-pop="1" style="font-size:140px;margin-top:10px;white-space:nowrap">{e(H["gu"])}</div>
  <div class="en a" data-in="0.9" style="font-size:100px">{e(H["en"])}</div>
  <div class="art a" data-in="1.0" data-rise="300" style="bottom:260px">{H.get("art_svg","")}</div>
</div>''']
history = []
for i, sc in enumerate(C['scenes']):
    s = t0 + i*5.5; e_ = s + 5.5
    out.append(f'<div class="scene" data-s="{s}" data-e="{e_}" style="padding:0">{phone(s, history[-4:], sc["msgs"], sc.get("typing"), sc.get("seen"))}</div>')
    history += sc['msgs']
es = t0 + n*5.5
for a, b in [('20.0', f'{es:.1f}'), ('23.5', f'{es+3.5:.1f}'), ('20.1', f'{es+0.1:.1f}'), ('20.5', f'{es+0.5:.1f}'), ('20.8', f'{es+0.8:.1f}'), ('21.1', f'{es+1.1:.1f}')]:
    end = end.replace(f'"{a}"', f'"{b}"')
end = end.replace('Next: {{NEXT}}', 'Next: ' + e(C['end']['next']))
end = end.replace(f'<div class="en a" data-in="{es+0.5:.1f}"', f'<div class="kick a" data-in="{es+0.3:.1f}" style="font-size:46px;color:var(--indigo)">{e(C["end"]["question"])}</div>\n  <div class="en a" data-in="{es+0.5:.1f}"', 1)
(d/'reel.html').write_text(head + '\n'.join(out) + '\n' + end + '</div>\n<script src="../../toolkit/runtime/otlo.js"></script>\n</body></html>')
print("wrote", d/'reel.html', "scenes:", 1+n+1)
