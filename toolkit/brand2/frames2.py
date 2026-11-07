#!/usr/bin/env python3
"""Render the SutraVerse 2.0 brand board, cover and one style frame per series treatment (1080x1920).
python3 frames2.py --out samples/"""
import argparse, json, pathlib
HERE = pathlib.Path(__file__).resolve().parent
LOGO = '''<svg width="{s}" height="{s}" viewBox="0 0 100 100"><circle cx="50" cy="50" r="10" fill="none" stroke="#F2A93B" stroke-width="5.5"/>
<path d="M72 22 C62 12 34 12 30 30 C27 44 44 48 52 50 C64 53 72 58 70 72 C68 88 40 90 28 78" fill="none" stroke="#0F0E12" stroke-width="12" stroke-linecap="round"/>
<path d="M72 22 C62 12 34 12 30 30 C27 44 44 48 52 50 C64 53 72 58 70 72 C68 88 40 90 28 78" fill="none" stroke="#F1E8D6" stroke-width="7" stroke-linecap="round"/></svg>'''
HEAD = '''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="brand2.css"><style>
body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#0F0E12}.f{position:absolute;inset:0;overflow:hidden}canvas{position:absolute;inset:0}
.wm{position:absolute;bottom:250px;left:0;right:0;display:flex;justify-content:center}</style></head><body><div class="f sv2-vignette">
<canvas id="c" width="1080" height="1920"></canvas>'''
TAIL = '''</div><script src="cast2.js"></script><script>CAST2.load(__REG__);const g=document.getElementById('c').getContext('2d');
function glow(x,y,r,col,a){const gr=g.createRadialGradient(x,y,0,x,y,r);gr.addColorStop(0,col);gr.addColorStop(1,'rgba(0,0,0,0)');g.globalAlpha=a;g.fillStyle=gr;g.fillRect(0,0,1080,1920);g.globalAlpha=1;}
function dots(x0,y0,x1,y1,gap,r,col,a){g.fillStyle=col;g.globalAlpha=a;for(let y=y0;y<y1;y+=gap)for(let x=x0+((y/gap)%2?gap/2:0);x<x1;x+=gap){g.beginPath();g.arc(x,y,r,0,7);g.fill();}g.globalAlpha=1;}
function grain(a){let s=11;const R=()=>((s=(s*16807)%2147483647)/2147483647);g.globalAlpha=a;for(let i=0;i<9000;i++){g.fillStyle=R()<.5?'#000':'#fff';g.fillRect(R()*1080,R()*1920,1.5,1.5);}g.globalAlpha=1;}
document.fonts.load('600 20px "Plex Mono"').then(()=>document.fonts.load('600 20px "Anek Latin"')).then(()=>document.fonts.load('italic 600 20px Fraunces')).then(()=>{
__DRAW__
window.DONE=1;});</script></body></html>'''

FRAMES = {}
# 1. Chanakya Files — Ember Engraving
FRAMES["frame_chanakya"] = ('''
<div class="sv2-bug">%s</div>
<div class="sv2-tag"><span class="n">RULE 07</span><span class="t">PLAN IN SILENCE</span></div>
<div style="position:absolute;top:300px;left:72px;color:#F2A93B"><span class="sv2-chip">Chanakya Files</span></div>
<div class="sv2-sub"><p>Jo plan karo, woh <b>batao mat</b>.<br>Result ko bolne do.</p></div>
<div style="position:absolute;left:72px;right:72px;bottom:300px;font:500 22px/1.3 var(--mono);color:#8C8478">CHANAKYA NITI 2.7 · TRADITIONAL ATTRIBUTION</div>''' % LOGO.format(s=84),
'''g.fillStyle='#0F0E12';g.fillRect(0,0,1080,1920);glow(760,560,900,'#F2A93B',.28);glow(760,560,260,'#F2A93B',.35);
// engraved plate: paper card with a plate mark
g.fillStyle='#EFE5CF';g.fillRect(150,400,780,860);g.strokeStyle='#0F0E12';g.lineWidth=3;g.strokeRect(176,426,728,808);g.strokeRect(186,436,708,788);
g.save();g.beginPath();g.rect(186,436,708,788);g.clip();
// lamp-lit hatch background (lighter near the lamp)
for(let k=0;k<4;k++){g.strokeStyle='rgba(15,14,18,'+(0.12+k*0.07)+')';g.lineWidth=1.4;g.beginPath();for(let y=466-900;y<1400;y+=9+k*3){g.moveTo(186,y+k*2);g.lineTo(894,y+700+k*2);}g.save();g.beginPath();g.rect(186+k*120,466,708,908);g.clip();g.stroke();g.restore();}
CAST2.draw(g,'chanakya',{x:560,y:1010,s:430,yaw:-0.35,mood:'smirk',style:'engrave',light:1,body:'bust'});
g.restore();
g.fillStyle='#0F0E12';g.font='italic 600 30px Fraunces';g.textAlign='center';g.fillText('Plate VII · The Strategist',540,1300);
// the lamp
g.fillStyle='#F2A93B';g.beginPath();g.ellipse(930,1540,46,16,0,0,7);g.fill();g.beginPath();g.moveTo(930,1470);g.quadraticCurveTo(948,1510,930,1528);g.quadraticCurveTo(912,1510,930,1470);g.fill();glow(930,1500,220,'#F2A93B',.5);grain(.05);''')

# 2. Mind Games — Case File
FRAMES["frame_mindgames"] = ('''
<div class="sv2-bug">%s</div>
<div class="sv2-tag conflict"><span class="n">FILE 02</span><span class="t">THE SMALL YES</span></div>
<div style="position:absolute;top:300px;left:72px;color:#E04A2F"><span class="sv2-chip">Mind Games</span></div>
<div style="position:absolute;left:72px;right:72px;top:1130px;color:#F1E8D6">
 <div style="font:600 26px/1 var(--mono);letter-spacing:.14em;color:#E04A2F">THE TRICK</div>
 <div style="margin-top:18px;font:700 92px/1 var(--display);font-variation-settings:'opsz' 144">Foot-in-the-<em style="color:#F2A93B;font-weight:600">door</em></div>
 <div style="margin-top:22px;font:500 36px/1.3 var(--ui);color:#CFC3AA">A tiny favour first. Then the big ask feels impossible to refuse.</div>
 <div style="margin-top:20px;font:500 22px/1.3 var(--mono);color:#8C8478">FREEDMAN &amp; FRASER, 1966 · J. PERS. SOC. PSYCHOL.</div></div>
<div class="sv2-sub conflict" style="bottom:330px"><p>"Bas <b>5 minute</b> ka kaam hai, Kabir…"</p></div>''' % LOGO.format(s=84),
'''g.fillStyle='#16141B';g.fillRect(0,0,1080,1920);dots(0,0,1080,1920,14,2.2,'#2C2933',1);
// dossier folder
g.fillStyle='#211E27';g.fillRect(60,380,960,700);g.fillStyle='#2C2933';g.fillRect(60,360,300,40);
// polaroid evidence
g.save();g.translate(330,720);g.rotate(-0.06);g.fillStyle='#EFE5CF';g.fillRect(-210,-290,420,520);g.fillStyle='#1B1920';g.fillRect(-185,-265,370,400);
g.beginPath();g.rect(-185,-265,370,400);g.clip();glow(0,0,1,'#000',0);CAST2.draw(g,'kabir',{x:0,y:110,s:260,yaw:0.3,mood:'worried',arms:'phone'});g.restore();
g.save();g.translate(330,720);g.rotate(-0.06);g.fillStyle='#0F0E12';g.font='600 22px Plex Mono';g.fillText('EXHIBIT A · KABIR, 29',-180,200);g.restore();
// chat card (the ask)
g.save();g.translate(770,640);g.rotate(0.04);g.fillStyle='#F1E8D6';g.beginPath();g.roundRect(-230,-120,460,240,18);g.fill();g.fillStyle='#0F0E12';g.font='600 22px Plex Mono';g.fillText('MALHOTRA · 9:47 PM',-200,-72);
g.font='600 34px Anek Latin';g.fillText('Ek chhota sa favour?',-200,-20);g.fillText('Bas 5 min. 🙂',-200,26);g.fillStyle='#8C8478';g.font='500 22px Plex Mono';g.fillText('seen ✓✓',-200,82);g.restore();
// red stamp
g.save();g.translate(800,930);g.rotate(-0.18);g.strokeStyle='#E04A2F';g.lineWidth=7;g.strokeRect(-150,-50,300,100);g.fillStyle='#E04A2F';g.font='700 66px Plex Mono';g.textAlign='center';g.fillText('TRAP',0,24);g.restore();
// red connection string
g.strokeStyle='#E04A2F';g.lineWidth=4;g.beginPath();g.moveTo(470,560);g.quadraticCurveTo(560,520,560,600);g.stroke();grain(.06);''')

# 3. Office Shastra — Night City Cel
FRAMES["frame_office"] = ('''
<div class="sv2-bug">%s</div>
<div class="sv2-tag"><span class="n">EP 04</span><span class="t">CREDIT THEFT</span></div>
<div style="position:absolute;top:300px;left:72px;color:#F2A93B"><span class="sv2-chip">Office Shastra</span></div>
<div class="sv2-sub conflict"><p>"Great idea, <b>team</b>." Team? Woh <b>mera</b> slide tha.</p></div>''' % LOGO.format(s=84),
'''const gr=g.createLinearGradient(0,0,0,1920);gr.addColorStop(0,'#1C2140');gr.addColorStop(1,'#0F0E12');g.fillStyle=gr;g.fillRect(0,0,1080,1920);
// window grid (city at night)
for(let r=0;r<7;r++)for(let c=0;c<5;c++){const lit=((r*7+c*3)%5)===0;g.fillStyle=lit?'rgba(242,169,59,.55)':'rgba(61,76,145,.35)';g.fillRect(70+c*196,380+r*120,160,90);}
g.fillStyle='rgba(15,14,18,.55)';g.fillRect(0,1100,1080,820);
// meeting-room glass edge + screen glow
glow(300,900,700,'#2BA39A',.12);
// slide on a screen
g.fillStyle='#F1E8D6';g.fillRect(560,470,420,250);g.fillStyle='#2C6E6A';g.fillRect(590,500,200,22);g.fillStyle='#CFC3AA';for(let i=0;i<4;i++)g.fillRect(590,545+i*30,330-i*40,14);g.fillStyle='#F2A93B';g.fillRect(860,640,90,60);
g.fillStyle='#0F0E12';g.font='600 20px Plex Mono';g.fillText('Q3_plan_RIYA_v7.pptx',590,700);
CAST2.draw(g,'malhotra',{x:770,y:1200,s:250,yaw:-0.35,mood:'smirk',light:-1});
CAST2.draw(g,'riya',{x:290,y:1260,s:300,yaw:0.4,mood:'worried',light:-1});grain(.05);''')

# 4. Turning Points — Archive & Timeline
FRAMES["frame_history"] = ('''
<div class="sv2-bug">%s</div>
<div class="sv2-tag" style="color:#0F0E12"><span class="n">CHAPTER 1</span><span class="t" style="color:#0F0E12">THE INSULT</span></div>
<div style="position:absolute;top:300px;left:72px;color:#3D4C91"><span class="sv2-chip">Turning Points</span></div>
<div style="position:absolute;left:72px;top:400px;font:600 210px/1 var(--mono);color:#0F0E12;letter-spacing:-.04em">c.<span style="color:#E04A2F">321</span><span style="font-size:90px"> BCE</span></div>
<div style="position:absolute;left:72px;right:72px;top:640px;font:700 64px/1.05 var(--display);color:#0F0E12">A teacher is thrown out of a king's court.</div>
<div class="sv2-sub"><p>Usne kasam khaayi: <b>shikha</b> tab bandhegi jab Nanda raaj khatam hoga.</p></div>
<div style="position:absolute;left:72px;right:72px;bottom:310px;font:500 22px/1.3 var(--mono);color:#5A5348">TRADITION HOLDS (MUDRARAKSHASA, LATER LEGEND) · DATE APPROXIMATE</div>''' % LOGO.format(s=84).replace('#F1E8D6','#0F0E12').replace('stroke="#0F0E12" stroke-width="12"','stroke="#EFE5CF" stroke-width="12"'),
'''g.fillStyle='#EFE5CF';g.fillRect(0,0,1080,1920);let s=5;const R=()=>((s=(s*16807)%2147483647)/2147483647);for(let i=0;i<300;i++){g.fillStyle='rgba(120,100,70,'+(R()*.05)+')';g.beginPath();g.arc(R()*1080,R()*1920,20+R()*120,0,7);g.fill();}
// timeline
g.strokeStyle='#0F0E12';g.lineWidth=4;g.beginPath();g.moveTo(72,860);g.lineTo(1008,860);g.stroke();
[['350',140],['330',360],['321',560],['305',800],['268',960]].forEach(([y,x])=>{g.lineWidth=3;g.beginPath();g.moveTo(x,846);g.lineTo(x,874);g.stroke();g.fillStyle=y==='321'?'#E04A2F':'#0F0E12';g.font='600 26px Plex Mono';g.textAlign='center';g.fillText(y,x,912);});
g.fillStyle='#E04A2F';g.beginPath();g.arc(560,860,14,0,7);g.fill();g.textAlign='left';
// medallion portrait (engraved)
g.save();g.beginPath();g.arc(540,1180,230,0,7);g.fillStyle='#E7DCC2';g.fill();g.clip();CAST2.draw(g,'chanakya',{x:540,y:1350,s:300,yaw:0.45,mood:'angry',style:'engrave'});g.restore();
g.strokeStyle='#0F0E12';g.lineWidth=5;g.beginPath();g.arc(540,1180,230,0,7);g.stroke();g.lineWidth=2;g.beginPath();g.arc(540,1180,244,0,7);g.stroke();''')

# 5. Panchatantra Reloaded — Lamp Theatre (shadow puppets)
FRAMES["frame_fable"] = ('''
<div class="sv2-bug">%s</div>
<div class="sv2-tag"><span class="n">FABLE 01</span><span class="t">THE JACKAL'S WHISPER</span></div>
<div style="position:absolute;top:300px;left:72px;color:#F2A93B"><span class="sv2-chip">Panchatantra Reloaded</span></div>
<div class="sv2-sub"><p>Damanaka ne sher se kaha: "Woh bail <b>aapki kursi</b> chahta hai."</p></div>''' % LOGO.format(s=84),
'''g.fillStyle='#120D0A';g.fillRect(0,0,1080,1920);
// cotton screen lit from behind by an oil lamp
const sc=g.createRadialGradient(540,900,40,540,900,700);sc.addColorStop(0,'#F6D9A0');sc.addColorStop(.6,'#D99A4E');sc.addColorStop(1,'#5A3418');g.fillStyle=sc;g.fillRect(60,420,960,980);
g.strokeStyle='#2A1A10';g.lineWidth=16;g.strokeRect(60,420,960,980);
function puppet(x,y,sc,flip,body,col){g.save();g.translate(x,y);g.scale(flip*sc,sc);g.globalAlpha=.88;g.fillStyle=col;g.beginPath();body();g.fill();g.globalAlpha=1;g.strokeStyle='#2A1408';g.lineWidth=4/sc;g.stroke();
 // carved holes glow
 g.fillStyle='rgba(255,236,190,.85)';for(let i=0;i<6;i++){g.beginPath();g.arc(-60+i*26,-10+(i%2)*14,5,0,7);g.fill();}g.restore();
 g.strokeStyle='rgba(60,40,30,.6)';g.lineWidth=3;g.beginPath();g.moveTo(x,y-40*sc);g.lineTo(x+flip*30,1500);g.stroke();}
// lion (Pingalaka)
puppet(720,980,1.6,-1,()=>{g.moveTo(-160,40);g.quadraticCurveTo(-170,-80,-60,-90);g.quadraticCurveTo(-10,-170,70,-120);g.quadraticCurveTo(130,-110,130,-50);g.lineTo(170,-30);g.lineTo(120,0);g.quadraticCurveTo(80,60,-20,50);g.lineTo(-40,140);g.lineTo(-70,140);g.lineTo(-80,60);g.lineTo(-130,140);g.lineTo(-160,140);g.closePath();},'#B8452A');
// jackal (Damanaka), leaning in to whisper
puppet(330,1080,1.25,1,()=>{g.moveTo(-120,20);g.quadraticCurveTo(-110,-50,-20,-50);g.lineTo(40,-110);g.lineTo(50,-60);g.lineTo(120,-40);g.lineTo(60,-10);g.quadraticCurveTo(30,40,-30,40);g.lineTo(-40,120);g.lineTo(-60,120);g.lineTo(-70,50);g.lineTo(-100,120);g.lineTo(-120,120);g.lineTo(-140,40);g.lineTo(-200,10);g.closePath();},'#6E7A2E');
// whisper line
g.strokeStyle='rgba(224,74,47,.9)';g.lineWidth=5;g.setLineDash([4,14]);g.beginPath();g.moveTo(460,1000);g.quadraticCurveTo(540,930,600,950);g.stroke();g.setLineDash([]);
glow(540,1560,300,'#F2A93B',.6);g.fillStyle='#F2A93B';g.beginPath();g.ellipse(540,1560,40,12,0,0,7);g.fill();grain(.05);''')

# 6. Explainer diagram — Folio Diagram
FRAMES["frame_explainer"] = ('''
<div class="sv2-bug">%s</div>
<div class="sv2-tag"><span class="n">STEP 2</span><span class="t">THE COMPARISON LOOP</span></div>
<div style="position:absolute;left:72px;right:72px;top:300px;color:#F1E8D6;font:700 78px/1.02 var(--display)">Why <em style="color:#F2A93B;font-weight:600">their</em> bonus ruins <em style="color:#F2A93B;font-weight:600">your</em> Diwali</div>
<div style="position:absolute;left:90px;top:760px;width:260px;text-align:center" class="sv2-label">Your bonus<div class="sv2-label small">₹40k · happy</div></div>
<div style="position:absolute;left:730px;top:760px;width:260px;text-align:center" class="sv2-label">Their story<div class="sv2-label small">₹1.2L screenshot</div></div>
<div style="position:absolute;left:390px;top:1210px;width:300px;text-align:center;color:#E04A2F" class="sv2-label">The gap<div class="sv2-label small">feels like a loss</div></div>
<div class="sv2-sub"><p>Khushi <b>number</b> se nahi, <b>comparison</b> se girti hai.</p></div>
<div style="position:absolute;left:72px;bottom:320px;font:500 22px/1.3 var(--mono);color:#8C8478">SOCIAL COMPARISON THEORY · FESTINGER, 1954 · ILLUSTRATIVE AMOUNTS</div>''' % LOGO.format(s=84),
'''g.fillStyle='#0F0E12';g.fillRect(0,0,1080,1920);g.strokeStyle='rgba(241,232,214,.05)';g.lineWidth=1;for(let x=72;x<=1008;x+=78){g.beginPath();g.moveTo(x,250);g.lineTo(x,1400);g.stroke();}
function node(x,y,r,col){g.fillStyle=col;g.beginPath();g.arc(x,y,r,0,7);g.fill();g.strokeStyle='#F1E8D6';g.lineWidth=4;g.beginPath();g.arc(x,y,r+14,0,7);g.stroke();}
node(220,640,90,'#2BA39A');node(860,640,90,'#F2A93B');node(540,1090,100,'#E04A2F');
g.strokeStyle='#F1E8D6';g.lineWidth=5;g.setLineDash([2,16]);g.lineCap='round';g.beginPath();g.moveTo(320,640);g.lineTo(760,640);g.stroke();
g.beginPath();g.moveTo(270,740);g.quadraticCurveTo(330,1000,440,1070);g.stroke();g.beginPath();g.moveTo(810,740);g.quadraticCurveTo(750,1000,640,1070);g.stroke();g.setLineDash([]);
g.fillStyle='#F1E8D6';g.font='600 30px Plex Mono';g.textAlign='center';g.fillText('vs',540,620);''')

# 7. Cover (grid tile) — Office Shastra example
FRAMES["cover_office"] = ('''
<div style="position:absolute;top:330px;left:0;right:0;text-align:center;color:#F2A93B;z-index:5"><span class="sv2-chip">Office Shastra</span></div>
<div style="position:absolute;left:70px;right:70px;top:1130px;text-align:center;z-index:5;color:#F1E8D6;font:800 168px/.9 var(--ui);font-stretch:85%;letter-spacing:-.02em;text-transform:uppercase">Boss took<br><span style="color:#E04A2F">your credit?</span></div>
<div style="position:absolute;left:70px;right:70px;top:1480px;text-align:center;z-index:5;font:italic 600 52px/1.2 var(--display);color:#CFC3AA">Chanakya had a rule for this.</div>''',
'''const gr=g.createLinearGradient(0,0,0,1920);gr.addColorStop(0,'#1C2140');gr.addColorStop(.55,'#0F0E12');g.fillStyle=gr;g.fillRect(0,0,1080,1920);glow(540,700,700,'#F2A93B',.18);
CAST2.draw(g,'riya',{x:540,y:1180,s:560,yaw:0.2,mood:'angry',light:-1});
const fade=g.createLinearGradient(0,980,0,1920);fade.addColorStop(0,'rgba(15,14,18,0)');fade.addColorStop(.4,'rgba(15,14,18,.92)');fade.addColorStop(1,'#0F0E12');g.fillStyle=fade;g.fillRect(0,980,1080,940);''')

# 8. Brand board
FRAMES["brand_board"] = ('''
<div style="position:absolute;left:72px;top:150px;display:flex;align-items:center;gap:26px;color:#F1E8D6">%s<span style="font:700 76px/1 var(--display);font-variation-settings:'opsz' 144;letter-spacing:.14em">SUTRAVERSE</span></div>
<div style="position:absolute;left:72px;top:330px;font:italic 500 44px/1.2 var(--display);color:#CFC3AA">Ancient strategy. Modern psychology.<br>Everyday India.</div>
<div style="position:absolute;left:72px;top:520px;font:600 24px/1 var(--mono);letter-spacing:.14em;color:#8C8478">COLOUR = MEANING</div>
<div style="position:absolute;left:72px;top:570px;display:grid;grid-template-columns:repeat(4,222px);gap:14px">
 <div style="height:150px;background:#F2A93B;padding:14px;font:600 22px/1.2 var(--mono);color:#0F0E12">AMBER<br>insight<br>#F2A93B</div>
 <div style="height:150px;background:#E04A2F;padding:14px;font:600 22px/1.2 var(--mono);color:#F1E8D6">VERMILION<br>conflict<br>#E04A2F</div>
 <div style="height:150px;background:#2BA39A;padding:14px;font:600 22px/1.2 var(--mono);color:#0F0E12">TEAL<br>resolution<br>#2BA39A</div>
 <div style="height:150px;background:#3D4C91;padding:14px;font:600 22px/1.2 var(--mono);color:#F1E8D6">INDIGO<br>the past<br>#3D4C91</div>
 <div style="height:110px;background:#0F0E12;outline:2px solid #2C2933;padding:14px;font:600 22px/1.2 var(--mono);color:#CFC3AA">INK #0F0E12</div>
 <div style="height:110px;background:#2C2933;padding:14px;font:600 22px/1.2 var(--mono);color:#CFC3AA">GRAPHITE</div>
 <div style="height:110px;background:#F1E8D6;padding:14px;font:600 22px/1.2 var(--mono);color:#0F0E12">PAPER</div>
 <div style="height:110px;background:#CFC3AA;padding:14px;font:600 22px/1.2 var(--mono);color:#0F0E12">BONE</div></div>
<div style="position:absolute;left:72px;top:900px;font:600 24px/1 var(--mono);letter-spacing:.14em;color:#8C8478">TYPE</div>
<div style="position:absolute;left:72px;top:950px;color:#F1E8D6;font:700 96px/1 var(--display);font-variation-settings:'opsz' 144">Fraunces <em style="color:#F2A93B;font-weight:500">titles</em></div>
<div style="position:absolute;left:72px;top:1070px;color:#F1E8D6;font:700 54px/1 var(--ui)">Anek — subtitles &amp; labels · अनेक</div>
<div style="position:absolute;left:72px;top:1150px;color:#F2A93B;font:600 40px/1 var(--mono)">PLEX MONO · FILE 02 · 321 BCE</div>
<div class="sv2-tag" style="top:1240px"><span class="n">FILE 02</span><span class="t">THE SMALL YES</span></div>
<div style="position:absolute;left:72px;top:1320px;display:flex;gap:16px;flex-wrap:wrap;width:940px">
 <span class="sv2-chip" style="color:#F2A93B">Chanakya Files</span><span class="sv2-chip" style="color:#E04A2F">Mind Games</span><span class="sv2-chip" style="color:#F2A93B">Office Shastra</span>
 <span class="sv2-chip" style="color:#2BA39A">Ghar Ki Baat</span><span class="sv2-chip" style="color:#7F8FD6">Turning Points</span><span class="sv2-chip" style="color:#E4B15A">Panchatantra Reloaded</span></div>
<div class="sv2-sub" style="bottom:300px"><p>Subtitles always sit on the <b>ink plate</b>.</p></div>''' % LOGO.format(s=120),
'''g.fillStyle='#0F0E12';g.fillRect(0,0,1080,1920);''')


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", default=str(HERE / "samples")); ap.add_argument("--only", nargs="*"); a = ap.parse_args()
    out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True); reg = (HERE / "cast2.json").read_text()
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920}); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        for name, (html, draw) in FRAMES.items():
            if a.only and name not in a.only: continue
            tmp = HERE / f"_f_{name}.html"; tmp.write_text(HEAD + html + TAIL.replace("__REG__", reg).replace("__DRAW__", draw))
            pg.goto(tmp.as_uri()); pg.wait_for_function("window.DONE===1", timeout=20000); pg.wait_for_timeout(400)
            pg.screenshot(path=str(out / f"{name}.png")); tmp.unlink(); print("frame:", name)
        b.close()
    if errs: raise SystemExit("page errors: " + " | ".join(errs))
    from PIL import Image  # contact sheet
    names = [n for n in FRAMES if not a.only or n in a.only]; ims = [Image.open(out / f"{n}.png").resize((360, 640)) for n in names]
    cols = 4; rows = (len(ims) + cols - 1) // cols; sheet = Image.new("RGB", (cols * 370 + 10, rows * 650 + 10), (15, 14, 18))
    for i, im in enumerate(ims): sheet.paste(im, (10 + (i % cols) * 370, 10 + (i // cols) * 650))
    sheet.save(out / "contact.jpg", quality=88); print("contact:", out / "contact.jpg")


if __name__ == "__main__":
    main()
