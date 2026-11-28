// OTLO brand kit v1 (28 Nov 2026) — motion for the "Kankotri Press" identity. Load AFTER gsap and BEFORE otlo-fx.js.
// Everything is a GSAP tween on OTLO's frame clock (window.OTLO_TWEENS), so renders are frame-exact.
// Markup hooks (see otlo/toolkit/BRAND.md):
//   .o-toran                    the toran: drawn here; flags drop in on the first scene (brand sting, <0.6 s)
//   .o-progress                 progress beads: one bead per scene, the current one lit in vermilion
//   [data-in] on .o-plate/.o-cut/.o-lower/.o-invite/.o-seal  entrance at that second (each kind has its own motion)
//   .o-layer[data-par="40"]     parallax drift (px) across its scene on a wrapper; foreground layers use larger values
//   cuts                        cinematic dissolve + light leak, done in otlo.js when <body class="otlo">
//   .o-badge-end                the Toran badge stamps in like a press seal
(function(){
  const PAL = ['#C2185B', '#E3A21A'];
  const NS = 'http://www.w3.org/2000/svg';
  function toranSVG(w, n, h){
    // A Gujarati toran: a straight embroidered band (vermilion, haldi borders, zigzag stitch, mirror-work) with
    // evenly spaced hangings alternating fabric pennants (rani / haldi, embroidered edge, mirror, tassel bead) and
    // mango leaves (ashopallav). Each hanging pivots at the band, so the sway looks physical. Shadow falls on the card.
    const uid = 't' + Math.random().toString(36).slice(2, 7);
    const step = w / n, bandH = 30, hang = h - bandH - 6;
    let s = `<svg xmlns="${NS}" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" style="overflow:visible">
<defs>
 <filter id="${uid}sh" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="6" stdDeviation="4" flood-color="#3A2410" flood-opacity=".35"/></filter>
 <linearGradient id="${uid}band" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C8443A"/><stop offset=".55" stop-color="#A8322A"/><stop offset="1" stop-color="#7E221C"/></linearGradient>
 <linearGradient id="${uid}rani" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#E0457F"/><stop offset=".6" stop-color="#C2185B"/><stop offset="1" stop-color="#8E1043"/></linearGradient>
 <linearGradient id="${uid}haldi" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F6C24A"/><stop offset=".6" stop-color="#E3A21A"/><stop offset="1" stop-color="#B57A0C"/></linearGradient>
 <linearGradient id="${uid}leaf" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4F8F3A"/><stop offset=".5" stop-color="#3C7A2E"/><stop offset="1" stop-color="#2B5E22"/></linearGradient>
 <radialGradient id="${uid}mir" cx=".35" cy=".35" r=".7"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".45" stop-color="#DCE3EA"/><stop offset="1" stop-color="#8C98A6"/></radialGradient>
</defs><g filter="url(#${uid}sh)">`;
    // hangings first (behind the band)
    for (let i = 0; i < n; i++){
      const x = i * step + step / 2;
      if (i % 3 === 2){
        const L = hang * 0.92, W = step * 0.36;
        s += `<g class="flag" transform="translate(${x},${bandH - 4})"><path d="M0,0 C${W},${L*0.25} ${W*0.9},${L*0.7} 0,${L} C${-W*0.9},${L*0.7} ${-W},${L*0.25} 0,0Z" fill="url(#${uid}leaf)"/>
          <path d="M0,4 L0,${L-6}" stroke="#25501D" stroke-width="2"/>${[0.3,0.5,0.7].map(t=>`<path d="M0,${L*t} L${W*0.55},${L*t-10} M0,${L*t} L${-W*0.55},${L*t-10}" stroke="#2B5E22" stroke-width="1.4" opacity=".7"/>`).join('')}</g>`;
      } else {
        const col = (i % 3 === 0) ? 'rani' : 'haldi', Wd = step * 0.84, L = hang;
        s += `<g class="flag" transform="translate(${x},${bandH - 4})"><path d="M${-Wd/2},0 L${Wd/2},0 L0,${L*0.86}Z" fill="url(#${uid}${col})"/>
          <path d="M${-Wd/2+7},5 L${Wd/2-7},5 L0,${L*0.86-12}Z" fill="none" stroke="${col === 'rani' ? '#F6C24A' : '#A8322A'}" stroke-width="2" stroke-dasharray="5 4"/>
          <circle cx="0" cy="${L*0.3}" r="${Math.min(9, Wd*0.16)}" fill="url(#${uid}mir)" stroke="${col === 'rani' ? '#F6C24A' : '#7E221C'}" stroke-width="2.5"/>
          <path d="M0,${L*0.86} L0,${L*0.86+8}" stroke="#7E221C" stroke-width="2"/><circle cx="0" cy="${L*0.86+13}" r="6" fill="${col === 'rani' ? '#E3A21A' : '#C2185B'}"/>
          <path d="M-3,${L*0.86+18} L-5,${L} M0,${L*0.86+18} L0,${L+2} M3,${L*0.86+18} L5,${L}" stroke="${col === 'rani' ? '#E3A21A' : '#C2185B'}" stroke-width="2"/></g>`;
      }
    }
    // the band
    s += `<rect x="0" y="0" width="${w}" height="${bandH}" fill="url(#${uid}band)"/>
      <rect x="0" y="2" width="${w}" height="4" fill="#E3A21A"/><rect x="0" y="${bandH-6}" width="${w}" height="4" fill="#E3A21A"/>
      <path d="${Array.from({length: Math.ceil(w/18)}, (_, k) => `${k?'L':'M'}${k*18},${k%2?11:21}`).join(' ')}" fill="none" stroke="#F4EAD7" stroke-width="2" stroke-dasharray="3 3" opacity=".8"/>`;
    for (let x = step / 2; x < w; x += step) s += `<circle cx="${x}" cy="${bandH/2}" r="5" fill="url(#${uid}mir)" stroke="#E3A21A" stroke-width="1.5"/>`;
    return s + '</g></svg>';
  }
  function build(){
    document.querySelectorAll('.o-toran').forEach(el => { if (!el.innerHTML.trim()) el.innerHTML = toranSVG(1012, 23, 120); });
    const scenes = [...document.querySelectorAll('.scene')];
    document.querySelectorAll('.o-progress').forEach(el => {
      const k = scenes.indexOf(el.closest('.scene')); const n = scenes.length;
      let s = `<svg width="260" height="44" viewBox="0 0 260 44"><rect x="2" y="6" width="256" height="5" rx="2" fill="#A8322A" opacity=".85"/>`;
      for (let i = 0; i < n; i++){ const x = 14 + i * (232 / (n - 1));
        s += `<polygon class="${i === k ? 'now' : ''}" points="${x-11},11 ${x+11},11 ${x},33" fill="${i < k ? '#E3A21A' : i === k ? '#C2185B' : '#F4EAD7'}" stroke="${i <= k ? 'none' : '#A8322A'}" stroke-opacity=".6" stroke-width="1.5"/>`; }
      el.innerHTML = s + '</svg>';
    });
  }
  window.OTLO_TWEENS = window.OTLO_TWEENS || [];
  window.OTLO_TWEENS.unshift((tl, g) => {
    build();
    const scenes = [...document.querySelectorAll('.scene')];
    const span = el => { const s = el.closest('.scene'); return s ? [+s.dataset.s, +s.dataset.e] : [0, 1]; };
    // brand sting: toran flags drop in on frame 0-0.5
    const first = scenes[0] && scenes[0].querySelectorAll('.o-toran .flag');
    if (first && first.length) tl.fromTo(first, {scaleY: 0.05, transformOrigin: '50% 0%'}, {scaleY: 1, duration: 0.55, ease: 'elastic.out(1, 0.55)', stagger: {each: 0.012, from: 'center'}}, 0.0);
    // toran in later scenes: gentle sway (alive, not static)
    scenes.forEach(sc => { sc.querySelectorAll('.o-toran .flag').forEach((f, i) => {   // cloth sway, each flag its own phase
      const amp = 1.6 + (i % 4) * 0.5, per = 1.7 + (i % 5) * 0.23, len = (+sc.dataset.e) - (+sc.dataset.s) + 0.6;
      tl.fromTo(f, {rotate: -amp, transformOrigin: '50% 0%'}, {rotate: amp, duration: per, ease: 'sine.inOut', yoyo: true, repeat: Math.ceil(len / per)}, +sc.dataset.s + (i % 7) * 0.09); }); });
    // progress: current bead pops
    document.querySelectorAll('.o-progress polygon.now').forEach(p => { const [s] = span(p);
      tl.fromTo(p, {scale: 0.2, transformOrigin: '50% 0%'}, {scale: 1, duration: 0.35, ease: 'back.out(3)'}, s + 0.25); });
    // entrances by kind
    const ent = (sel, from, to) => document.querySelectorAll(sel).forEach(el => { if (el.dataset.in === undefined) return;
      tl.fromTo(el, from(el), Object.assign({duration: 0.6, ease: 'power3.out'}, to(el)), +el.dataset.in); });
    ent('.o-plate', el => ({y: 90, opacity: 0, rotate: (+el.dataset.rot || 0) - 6}), el => ({y: 0, opacity: 1, rotate: +el.dataset.rot || 0, ease: 'back.out(1.6)'}));
    ent('.o-cut', el => ({y: 140, opacity: 0, scale: 0.92}), el => ({y: 0, opacity: 1, scale: 1, duration: 0.7}));
    ent('.o-lower', el => ({x: -720, opacity: 1}), el => ({x: 0, duration: 0.55, ease: 'power4.out'}));
    ent('.o-invite', el => ({scale: 0.86, opacity: 0, rotate: -2}), el => ({scale: 1, opacity: 1, rotate: 0, ease: 'back.out(1.8)'}));
    ent('.o-seal', el => ({scale: 1.8, opacity: 0, rotate: -24}), el => ({scale: 1, opacity: 1, rotate: -10, duration: 0.32, ease: 'power4.in'}));
    ent('.o-fade', el => ({opacity: 0, y: 24}), el => ({opacity: 1, y: 0, duration: 0.5}));
    ent('.o-badge-end', el => ({scale: 2.2, opacity: 0, rotate: -30}), el => ({scale: 1, opacity: 1, rotate: 0, duration: 0.4, ease: 'power4.in'}));
    // parallax: layers drift at different speeds across their scene
    document.querySelectorAll('[data-par]').forEach(el => { const [s, e] = span(el); const a = +el.dataset.par;
      tl.fromTo(el, {y: a / 2}, {y: -a / 2, duration: Math.max(0.5, e - s), ease: 'none'}, s); });   // put data-par on a WRAPPER (.o-layer), entrances on the child
    // map: stroke draws itself, pins drop
    document.querySelectorAll('.o-map .outline').forEach(p => { const L = p.getTotalLength ? p.getTotalLength() : 4000; const [s] = span(p);
      p.style.strokeDasharray = L; tl.fromTo(p, {strokeDashoffset: L}, {strokeDashoffset: 0, duration: 1.3, ease: 'power2.inOut'}, +(p.dataset.at || s + 0.2));
      const fill = p.parentNode.querySelector('.fill'); if (fill) tl.fromTo(fill, {opacity: 0}, {opacity: 1, duration: 0.6}, +(p.dataset.at || s + 0.2) + 0.9); });
    document.querySelectorAll('.o-map .pin').forEach(p => tl.fromTo(p, {y: -60, opacity: 0}, {y: 0, opacity: 1, duration: 0.45, ease: 'bounce.out'}, +p.dataset.at));
    document.querySelectorAll('.o-map .ripple').forEach(p => tl.fromTo(p, {attr: {r: 8}, opacity: 0.9}, {attr: {r: 70}, opacity: 0, duration: 1.2, repeat: 2, ease: 'power1.out'}, +p.dataset.at));
  });
})();
