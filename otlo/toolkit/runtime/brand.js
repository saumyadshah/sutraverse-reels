// OTLO brand kit v1 (28 Nov 2026) — motion for the "Kankotri Press" identity. Load AFTER gsap and BEFORE otlo-fx.js.
// Everything is a GSAP tween on OTLO's frame clock (window.OTLO_TWEENS), so renders are frame-exact.
// Markup hooks (see otlo/toolkit/BRAND.md):
//   .o-toran                    the toran: drawn here; flags drop in on the first scene (brand sting, <0.6 s)
//   .o-progress                 progress beads: one bead per scene, the current one lit in vermilion
//   [data-in] on .o-plate/.o-cut/.o-lower/.o-invite/.o-seal  entrance at that second (each kind has its own motion)
//   .o-layer[data-par="40"]     parallax drift (px) across its scene on a wrapper; foreground layers use larger values
//   #o-wipe                     created here: a toran band sweeps down at every cut after the first (chapter turn)
//   .o-badge-end                the Toran badge stamps in like a press seal
(function(){
  const PAL = ['#C2185B', '#E3A21A'];
  const NS = 'http://www.w3.org/2000/svg';
  function toranSVG(w, n, h){
    const step = w / n; let s = `<svg xmlns="${NS}" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">`;
    s += `<path class="tstring" d="M0,14 Q${w/2},34 ${w},14" stroke="#1B2A4A" stroke-width="3" fill="none"/>`;
    for (let i = 0; i < n; i++){
      const x = i * step + step / 2, t = (x / w), y = 14 + 20 * 4 * t * (1 - t) * 1.0;
      const leaf = i % 3 === 1;
      s += leaf
        ? `<g class="flag" transform="translate(${x},${y})"><path d="M0,0 C14,18 12,46 0,62 C-12,46 -14,18 0,0Z" fill="#3C7A3A"/><path d="M0,4 L0,58" stroke="#2C5C2B" stroke-width="2"/></g>`
        : `<g class="flag" transform="translate(${x},${y})"><polygon points="${-step*0.42},0 ${step*0.42},0 0,${h*0.56}" fill="${PAL[(i>>1)%2]}"/><circle cx="0" cy="${h*0.56+8}" r="6" fill="#E3A21A"/></g>`;
    }
    return s + '</svg>';
  }
  function build(){
    document.querySelectorAll('.o-toran').forEach(el => { if (!el.innerHTML.trim()) el.innerHTML = toranSVG(1012, 23, 120); });
    const scenes = [...document.querySelectorAll('.scene')];
    document.querySelectorAll('.o-progress').forEach(el => {
      const k = scenes.indexOf(el.closest('.scene')); const n = scenes.length;
      let s = `<svg width="260" height="44" viewBox="0 0 260 44"><path d="M4,10 Q130,30 256,10" stroke="#1B2A4A" stroke-opacity=".5" stroke-width="2" fill="none"/>`;
      for (let i = 0; i < n; i++){ const x = 12 + i * (236 / (n - 1)), t = x / 260, y = 10 + 20 * 4 * t * (1 - t) * 0.5;
        s += `<polygon class="${i === k ? 'now' : ''}" points="${x-9},${y} ${x+9},${y} ${x},${y+20}" fill="${i < k ? '#E3A21A' : i === k ? '#B8322A' : 'none'}" stroke="${i <= k ? 'none' : '#1B2A4A'}" stroke-opacity=".45" stroke-width="2"/>`; }
      el.innerHTML = s + '</svg>';
    });
    if (!document.getElementById('o-wipe')){
      const w = document.createElement('div'); w.id = 'o-wipe';
      w.style.cssText = 'position:absolute;left:0;top:-260px;width:1080px;height:240px;z-index:50;pointer-events:none;background:#B8322A;';
      w.innerHTML = `<div style="position:absolute;left:0;bottom:-118px;width:1080px">${toranSVG(1080, 24, 120)}</div>`;
      document.getElementById('stage').appendChild(w);
    }
  }
  window.OTLO_TWEENS = window.OTLO_TWEENS || [];
  window.OTLO_TWEENS.unshift((tl, g) => {
    build();
    const scenes = [...document.querySelectorAll('.scene')];
    const span = el => { const s = el.closest('.scene'); return s ? [+s.dataset.s, +s.dataset.e] : [0, 1]; };
    // brand sting: toran flags drop in on frame 0-0.5
    const first = scenes[0] && scenes[0].querySelectorAll('.o-toran .flag');
    if (first && first.length) tl.fromTo(first, {y: -70, opacity: 0}, {y: 0, opacity: 1, duration: 0.42, ease: 'back.out(2.4)', stagger: 0.012}, 0.0);
    // toran in later scenes: gentle sway (alive, not static)
    scenes.slice(1).forEach(sc => { const fl = sc.querySelectorAll('.o-toran .flag'); if (fl.length)
      tl.fromTo(fl, {rotate: -4, transformOrigin: '50% 0%'}, {rotate: 3, duration: 1.6, ease: 'sine.inOut', yoyo: true, repeat: 3, stagger: 0.02}, +sc.dataset.s); });
    // chapter wipe at each cut: a vermilion sheet with a toran hem passes top to bottom
    scenes.slice(1).forEach(sc => { const s = +sc.dataset.s;
      if (sc.dataset.wipe === 'none') return;
      tl.fromTo('#o-wipe', {y: 0}, {y: 2260, duration: 0.55, ease: 'power2.inOut'}, s - 0.28); });
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
