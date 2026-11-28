// Otlo FX layer v1 (28 Nov 2026). Motion graphics on top of otlo.js, frame-accurate.
// otlo.js calls OTLOFX.update(t) on every frame with the scene-time t, so every effect here is a pure function of t:
// no requestAnimationFrame and no wall-clock time. A paused GSAP timeline is seeked to t; Three.js renders once per call.
//
// Include after otlo.js:
//   <script src="../../toolkit/runtime/vendor/gsap.min.js"></script>
//   <script src="../../toolkit/runtime/vendor/SplitText.min.js"></script>
//   <script src="../../toolkit/runtime/otlo-fx.js"></script>
//   <script type="module" src="../../toolkit/runtime/otlo-3d.js"></script>   (only when a .fx3d canvas is used)
//
// 1. Ken Burns on photos: every <img class="photo"> slowly pushes in and drifts across its scene.
//    data-kb="in" (default) | "out" | "left" | "right" | "none"; data-kb-amt="0.10" (scale change).
// 2. Kinetic type: data-kinetic="words" (use for Gujarati: never split Gujarati into characters, it breaks
//    the conjuncts) or "chars" (English only), plus data-at="<seconds>". Words or characters rise and fade in on a stagger.
//    Do NOT also give these elements class "a" (otlo.js reveal); the FX layer owns them.
// 3. Count-up numbers: <span data-count="120" data-at="3.2" data-dur="1.2" data-prefix="₹" data-suffix=" Cr">0</span>
// 4. Stamp / punch-in: data-stamp="<seconds>" scales the element down from 1.6 with a slight rotation (a verdict stamp).
// 5. Custom tweens: in the Reel, push functions into window.OTLO_TWEENS: (tl, gsap) => tl.to('#x', {...}, 4.2).
//    The positions are absolute Reel seconds (the same clock as data-s, data-e and data-in).
// 6. Highlight sweep: data-sweep="<seconds>" draws a turmeric highlighter under the text.
(function(){
  const G = window.gsap; if (!G) { console.warn('otlo-fx: gsap missing'); return; }
  if (window.SplitText) G.registerPlugin(window.SplitText);
  const tl = G.timeline({paused: true});
  const sceneOf = el => el.closest('.scene');
  const span = el => { const s = sceneOf(el); return s ? [+s.dataset.s, +s.dataset.e] : [0, 1]; };
  function build(){
    // kinetic type
    document.querySelectorAll('[data-kinetic]').forEach(el => {
      const at = +(el.dataset.at ?? span(el)[0] + 0.15);
      const mode = el.dataset.kinetic === 'chars' ? 'chars' : 'words';
      let parts;
      if (mode === 'chars' && window.SplitText) { parts = new SplitText(el, {type: 'words,chars'}).chars; }
      else { // split into words but keep inline markup (<em>, <i>, <b>) around the words it wrapped
        const words = [];
        const walk = (node, wrap) => { node.childNodes.forEach(c => {
          if (c.nodeType === 3) c.textContent.split(/\s+/).filter(Boolean).forEach(w => words.push({w, wrap}));
          else if (c.nodeType === 1) walk(c, c.tagName.toLowerCase()); }); };
        walk(el, null);
        el.innerHTML = words.map((o, i) => { const inner = o.wrap ? `<${o.wrap}>${o.w}</${o.wrap}>` : o.w;
          return `<span style="display:inline-block;margin-right:${i < words.length - 1 ? '0.26em' : '0'}">${inner}</span>`; }).join('');
        parts = el.querySelectorAll(':scope > span'); }
      G.set(parts, {display: 'inline-block'});
      tl.fromTo(parts, {y: 70, opacity: 0, rotate: 4}, {y: 0, opacity: 1, rotate: 0, duration: 0.45, ease: 'back.out(2)',
        stagger: mode === 'chars' ? 0.018 : 0.07}, at);
    });
    // count-up
    document.querySelectorAll('[data-count]').forEach(el => {
      const o = {v: +(el.dataset.from || 0)}; const to = +el.dataset.count; const dec = +(el.dataset.dec || 0);
      const fmt = v => (el.dataset.prefix || '') + v.toLocaleString('en-IN', {minimumFractionDigits: dec, maximumFractionDigits: dec}) + (el.dataset.suffix || '');
      el.textContent = fmt(o.v);
      tl.to(o, {v: to, duration: +(el.dataset.dur || 1.2), ease: 'power2.out', onUpdate: () => el.textContent = fmt(o.v)}, +(el.dataset.at || span(el)[0] + 0.3));
    });
    // stamps
    document.querySelectorAll('[data-stamp]').forEach(el => {
      tl.fromTo(el, {scale: 1.7, opacity: 0, rotate: -14}, {scale: 1, opacity: 1, rotate: -6, duration: 0.32, ease: 'power4.in'}, +el.dataset.stamp);
    });
    // highlighter sweep
    document.querySelectorAll('[data-sweep]').forEach(el => {
      el.style.backgroundImage = 'linear-gradient(transparent 58%, rgba(227,162,26,.75) 58%, rgba(227,162,26,.75) 92%, transparent 92%)';
      el.style.backgroundRepeat = 'no-repeat';
      tl.fromTo(el, {backgroundSize: '0% 100%'}, {backgroundSize: '100% 100%', duration: 0.5, ease: 'power2.inOut'}, +el.dataset.sweep);
    });
    (window.OTLO_TWEENS || []).forEach(f => { try { f(tl, G); } catch (e) { console.error('otlo-fx tween', e); } });
  }
  function kenburns(t){
    document.querySelectorAll('img.photo, .kb').forEach(el => {
      const mode = el.dataset.kb || 'in'; if (mode === 'none') return;
      const [s, e] = span(el); const p = Math.max(0, Math.min(1, (t - s) / Math.max(0.1, e - s)));
      const a = +(el.dataset.kbAmt || 0.10); const ease = p * p * (3 - 2 * p);
      let sc = 1 + a * ease, x = 0;
      if (mode === 'out') sc = 1 + a * (1 - ease);
      if (mode === 'left') x = -30 * ease; if (mode === 'right') x = 30 * ease;
      // the transform goes on the image itself; its frame/wrapper clips (wrap photos in .kbframe for a clean crop)
      el.style.transform = `translateX(${x}px) scale(${sc.toFixed(4)})`;
      el.style.transformOrigin = el.dataset.kbOrigin || '50% 40%';
    });
  }
  let built = false;
  window.OTLOFX = {
    update(t){
      if (!built) { built = true; build(); }
      tl.seek(Math.max(0, t), false);
      kenburns(t);
      if (window.OTLO3D) window.OTLO3D(t);
    },
    timeline: tl
  };
})();
