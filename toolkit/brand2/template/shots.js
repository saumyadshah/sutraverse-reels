// PILOT (sample, silent): Office Shastra → Chanakya Files crossover, 20 s. Replace for each Reel.
// Every shot: t0, t1, draw(H, lt, T, t), optional html(lt, T), tag, chip. SUBS: [{t0,t1,text,kind}].
export const DUR = 20;
export const CAST = await fetch('cast2.json').then(r => r.json());
export const SUBS = [
  { t0: 0.3, t1: 2.6, text: '"Great idea, <b>team</b>." Team?', kind: 'conflict' },
  { t0: 2.6, t1: 4.6, text: 'Woh slide <b>Riya</b> ne banaya tha.', kind: 'conflict' },
  { t0: 4.8, t1: 6.8, text: 'Ladegi toh <b>drama</b>.' },
  { t0: 6.8, t1: 8.6, text: 'Chup rahegi toh <b>invisible</b>.' },
  { t0: 10.0, t1: 12.6, text: '2,300 saal pehle <b>Chanakya</b> ne likha…' },
];
export const EV = [{ t: 0.0, type: 'room' }, { t: 1.2, type: 'ping' }, { t: 4.7, type: 'freeze' }, { t: 5.2, type: 'card' }, { t: 6.9, type: 'card' }, { t: 8.6, type: 'whoosh' }, { t: 9.4, type: 'paper' }, { t: 12.7, type: 'silence' }, { t: 13.4, type: 'stamp' }, { t: 16.2, type: 'card' }, { t: 18.6, type: 'ding' }];
const office = (H, push, mood, freeze) => { const { g } = H;
  const gr = g.createLinearGradient(0, 0, 0, 1920); gr.addColorStop(0, '#1C2140'); gr.addColorStop(1, '#0F0E12'); g.fillStyle = gr; g.fillRect(0, 0, 1080, 1920);
  g.save(); g.translate(540, 960); g.scale(push, push); g.translate(-540, -960);
  for (let r = 0; r < 7; r++) for (let c = 0; c < 5; c++) { const lit = ((r * 7 + c * 3) % 5) === 0; g.fillStyle = lit ? 'rgba(242,169,59,.5)' : 'rgba(61,76,145,.33)'; g.fillRect(70 + c * 196, 380 + r * 120, 160, 90); }
  H.glow(820, 760, 520, '#2BA39A', .14);
  H.CAST2.draw(g, 'riya', { x: 520, y: 1330, s: 470, yaw: 0.25, mood, blink: false, lookX: -0.5, light: -1 });
  g.restore(); if (freeze) { g.fillStyle = 'rgba(15,14,18,.55)'; g.fillRect(0, 0, 1080, 1920); }
};
export const SHOTS = [
  { t0: 0, t1: 4.7, tag: { n: 'EP 04', t: 'CREDIT THEFT', kind: 'conflict' }, chip: { name: 'Office Shastra', col: '#F2A93B' },
    draw: (H, lt) => { office(H, 1 + 0.04 * lt / 4.7, lt < 1.3 ? 'neutral' : lt < 2.6 ? 'shock' : 'angry', false); H.grain(.04, Math.floor(lt * 12)); },
    html: (lt) => { const p = H_eo(lt - 1.2); return `<div class="card" style="left:470px;top:${520 - 40 * (1 - p)}px;width:500px;opacity:${p}"><div class="m">MALHOTRA · #Q3-PLAN · 9:47 PM</div>Great idea team 👏 Presenting this to the CXO myself.</div>`; } },
  { t0: 4.7, t1: 8.6, tag: { n: 'EP 04', t: 'TWO BAD OPTIONS', kind: 'conflict' },
    draw: (H, lt) => { office(H, 1.04, 'worried', true); },
    html: (lt) => `<div class="opt" style="top:${660 + 30 * (1 - H_eo(lt - .4))}px;color:#E04A2F;opacity:${H_eo(lt - .4)}"><span class="k">OPTION A</span>Call him out in the meeting</div>
                   <div class="opt" style="top:${900 + 30 * (1 - H_eo(lt - 2.1))}px;color:#E04A2F;opacity:${H_eo(lt - 2.1)}"><span class="k">OPTION B</span>Stay quiet. Again.</div>` },
  { t0: 8.6, t1: 15.8, tag: { n: 'RULE 07', t: 'CHANAKYA NITI 2.7' }, chip: { name: 'Chanakya Files', col: '#F2A93B' },
    draw: (H, lt, T) => { const { g } = H; g.fillStyle = '#0F0E12'; g.fillRect(0, 0, 1080, 1920); H.glow(780, 520, 900, '#F2A93B', .26);
      const z = 1 + 0.08 * H.ss(lt / T); g.save(); g.translate(540, 900); g.scale(z, z); g.translate(-540, -900);
      g.fillStyle = '#EFE5CF'; g.fillRect(150, 400, 780, 860); g.strokeStyle = '#0F0E12'; g.lineWidth = 3; g.strokeRect(176, 426, 728, 808); g.strokeRect(186, 436, 708, 788);
      g.save(); g.beginPath(); g.rect(186, 436, 708, 788); g.clip();
      H.CAST2.draw(g, 'chanakya', { x: 560, y: 1010, s: 430, yaw: H.lerp(-0.55, -0.25, H.ss(lt / T)), mood: lt > 4.2 ? 'smirk' : 'think', style: 'engrave', light: 1, blink: (lt % 3.1) < 0.1 });
      g.restore(); g.restore(); H.printWipe(H.seg(lt, 0, .9)); H.grain(.05, Math.floor(lt * 12)); },
    html: (lt) => lt > 4.0 ? `<div class="card" style="left:110px;right:110px;top:1300px;opacity:${H_eo(lt - 4.0)};font:italic 600 40px/1.25 Fraunces">Decide in silence. Keep the plan secret. Let the work speak.<div class="m" style="margin-top:14px">PARAPHRASE · CHANAKYA NITI 2.7</div></div>` : '' },
  { t0: 15.8, t1: 20, tag: { n: 'THE MOVE', t: 'OPTION C', kind: 'resolve' },
    draw: (H) => { const { g } = H; g.fillStyle = '#0F0E12'; g.fillRect(0, 0, 1080, 1920); H.glow(540, 700, 700, '#2BA39A', .12); },
    html: (lt) => `<div class="opt" style="top:420px;color:#2BA39A;opacity:${H_eo(lt - .2)}"><span class="k">OPTION C</span>Send the deck to the CXO, with your name on it, <i>before</i> the meeting.</div>
      <div class="sv2-principle" style="top:900px;opacity:${H_eo(lt - 1.2)}"><div class="k">THE IDEA</div><div class="l">Don't argue for credit. <em>Timestamp it.</em></div><div class="src">SUTRAVERSE · OFFICE SHASTRA × CHANAKYA FILES · PILOT</div></div>
      <div style="position:absolute;left:0;right:0;bottom:300px;display:flex;justify-content:center;opacity:${H_eo(lt - 2.6)}"><span class="sv2-word"><span>SUTRAVERSE</span></span></div>` },
];
function H_eo(x) { x = Math.max(0, Math.min(1, x / 0.45)); return 1 - Math.pow(1 - x, 3); }
