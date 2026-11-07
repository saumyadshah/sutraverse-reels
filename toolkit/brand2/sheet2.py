#!/usr/bin/env python3
"""Render a CAST2 model sheet: turnaround (5 angles), 10 expressions, 3 shot sizes, cel vs engrave.
python3 sheet2.py --names chanakya riya --out sheets/   (writes <name>.png)"""
import argparse, json, pathlib
HERE = pathlib.Path(__file__).resolve().parent
PAGE = """<!doctype html><html><head><style>@font-face{font-family:M;src:url(fonts/IBMPlexMono-SemiBold.ttf)}@font-face{font-family:F;src:url(fonts/Fraunces.ttf)}
body{margin:0;background:#0F0E12}</style></head><body><canvas id=c width=1800 height=1500></canvas>
<script src="cast2.js"></script><script>
CAST2.load(__REG__);const N=__NAME__;const c=document.getElementById('c'),g=c.getContext('2d');const sp=CAST2.registry[N];
g.fillStyle='#0F0E12';g.fillRect(0,0,1800,1500);
g.fillStyle='#F1E8D6';g.font='700 46px F';g.fillText(N.toUpperCase(),40,62);g.fillStyle='#CFC3AA';g.font='600 18px M';
const words=sp.role.split(' ');let line='',yy=96;for(const w of words){if((line+w).length>150){g.fillText(line,40,yy);yy+=24;line='';}line+=w+' ';}g.fillText(line,40,yy);
const LAB=[];function cell(x,y,w,h,label,bg){g.fillStyle=bg||'#1B1920';g.fillRect(x,y,w,h);LAB.push([label,x+8,y+h-10]);}
const yaws=[-0.95,-0.5,0,0.5,0.95];yaws.forEach((yw,i)=>{const x=40+i*230,y=150;cell(x,y,220,330,'YAW '+yw);g.save();g.beginPath();g.rect(x,y,220,330);g.clip();CAST2.draw(g,N,{x:x+110,y:y+235,s:150,yaw:yw});g.restore();});
// engrave turnaround
[-0.5,0,0.5].forEach((yw,i)=>{const x=1210+i*190,y=150;cell(x,y,180,330,'ENGRAVE','#EDE3CF');g.save();g.beginPath();g.rect(x,y,180,330);g.clip();CAST2.draw(g,N,{x:x+90,y:y+235,s:125,yaw:yw,style:'engrave'});g.restore();});
CAST2.MOODS.forEach((m,i)=>{const x=40+i*172,y=510;cell(x,y,164,210,m.toUpperCase());g.save();g.beginPath();g.rect(x,y,164,210);g.clip();CAST2.draw(g,N,{x:x+82,y:y+185,s:150,yaw:0.25,mood:m,body:'head'});g.restore();});
const shots=[['ECU',420,0.15,1.55],['CU',300,0.2,1.15],['MCU',200,0.3,0.95],['MS',130,0.35,0.7]];shots.forEach((s,i)=>{const x=40+i*240,y=750;cell(x,y,230,420,s[0]);g.save();g.beginPath();g.rect(x,y,230,420);g.clip();CAST2.draw(g,N,{x:x+115,y:y+420*s[3]-s[1]*0.05,s:s[1],yaw:s[2]});g.restore();});
['rest','fold','point','chin','phone','open'].forEach((a,i)=>{const x=1010+(i%3)*260,y=750+Math.floor(i/3)*215;cell(x,y,250,205,'ARMS '+a.toUpperCase());g.save();g.beginPath();g.rect(x,y,250,205);g.clip();CAST2.draw(g,N,{x:x+125,y:y+70,s:70,yaw:0.2,arms:a,mood:a==='point'?'angry':a==='chin'?'think':'neutral'});g.restore();});
[['NIGHT · LIGHT LEFT',-1],['NIGHT · LIGHT RIGHT',1]].forEach((l,i)=>{const x=40+i*480,y=1200;cell(x,y,470,260,l[0],'#16141C');g.save();g.beginPath();g.rect(x,y,470,260);g.clip();CAST2.draw(g,N,{x:x+235,y:y+250,s:150,yaw:i?-0.4:0.4,light:l[1]});g.restore();});
LAB.forEach(l=>{g.font='600 16px M';const w=g.measureText(l[0]).width;g.fillStyle='rgba(15,14,18,.8)';g.fillRect(l[1]-4,l[2]-15,w+8,21);g.fillStyle='#CFC3AA';g.fillText(l[0],l[1],l[2]);});window.DONE=1;</script></body></html>"""
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--names", nargs="+", required=True); ap.add_argument("--out", default=str(HERE / "sheets"))
    ap.add_argument("--registry", default=str(HERE / "cast2.json")); a = ap.parse_args()
    reg = json.load(open(a.registry)); out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1800, "height": 1500})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        for n in a.names:
            tmp = HERE / f"_sheet_{n}.html"; tmp.write_text(PAGE.replace('__REG__', json.dumps(reg)).replace('__NAME__', json.dumps(n)))
            pg.goto(tmp.as_uri()); pg.wait_for_function("window.DONE===1", timeout=15000); pg.wait_for_timeout(300)
            pg.screenshot(path=str(out / f"{n}.png")); tmp.unlink(); print("sheet:", out / f"{n}.png")
        b.close()
        if errs: raise SystemExit("page errors: " + "; ".join(errs))
if __name__ == "__main__": main()
