/* SutraVerse motion helpers — engine mechanics only (seeded randomness, word splitting,
   particles, camera drift, draw-on strokes). No frozen looks: scenes compose these freely.
   HyperFrames determinism: everything here is built synchronously at load and only
   animates allow-listed visual properties on the ONE paused timeline. */
(function () {
  function mulberry32(a) {
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  const SV = {
    rand: mulberry32(20261017),
    seed(n) { SV.rand = mulberry32(n); },

    /** Wrap each word of el in <span class="sv-w"> for staggered reveals, keeping inline
        markup such as <em>. Returns the spans in reading order. */
    splitWords(el) {
      const spans = [];
      const walk = (node) => {
        Array.from(node.childNodes).forEach((child) => {
          if (child.nodeType === 3) {
            const parts = child.textContent.split(/(\s+)/);
            const frag = document.createDocumentFragment();
            parts.forEach((p) => {
              if (!p) return;
              if (/^\s+$/.test(p)) { frag.appendChild(document.createTextNode(" ")); return; }
              const sp = document.createElement("span");
              sp.className = "sv-w";
              sp.style.display = "inline-block";
              sp.textContent = p;
              frag.appendChild(sp);
              spans.push(sp);
            });
            node.replaceChild(frag, child);
          } else if (child.nodeType === 1) {
            walk(child);
          }
        });
      };
      walk(el);
      return spans;
    },

    /** Floating motes / embers / dust. Deterministic. Returns the created nodes. */
    particles(tl, container, { count = 40, color = "#E8C979", size = [2, 6], start = 0, dur = 10,
      rise = [60, 220], drift = 60, opacity = [0.25, 0.9], blur = 0, area = null } = {}) {
      const W = area ? area.w : container.clientWidth || 1080;
      const H = area ? area.h : container.clientHeight || 1920;
      const nodes = [];
      for (let i = 0; i < count; i++) {
        const d = document.createElement("div");
        const s = size[0] + SV.rand() * (size[1] - size[0]);
        Object.assign(d.style, {
          position: "absolute", left: (SV.rand() * W) + "px", top: (SV.rand() * H) + "px",
          width: s + "px", height: s + "px", borderRadius: "50%", background: color,
          boxShadow: `0 0 ${s * 3}px ${color}`, opacity: 0, filter: blur ? `blur(${blur}px)` : "none",
        });
        container.appendChild(d);
        nodes.push(d);
        const o = opacity[0] + SV.rand() * (opacity[1] - opacity[0]);
        const delay = SV.rand() * Math.min(2.5, dur * 0.4);
        tl.to(d, { opacity: o, duration: 0.8, ease: "sine.out" }, start + delay);
        tl.to(d, { y: -(rise[0] + SV.rand() * (rise[1] - rise[0])), x: (SV.rand() - 0.5) * 2 * drift,
          duration: dur - delay, ease: "none" }, start + delay);
        tl.to(d, { opacity: 0, duration: 0.8, ease: "sine.in" }, start + dur - 0.8);
      }
      return nodes;
    },

    /** Slow "camera" move on a layer: scale/x/y over a span (parallax when layers differ). */
    drift(tl, el, start, dur, { fromScale = 1, toScale = 1.08, x = 0, y = 0, ease = "sine.inOut" } = {}) {
      tl.fromTo(el, { scale: fromScale, x: 0, y: 0 }, { scale: toScale, x, y, duration: dur, ease }, start);
    },

    /** Draw-on for SVG strokes that carry pathLength="1". */
    drawOn(tl, els, at, { dur = 1.2, stagger = 0.08, ease = "power2.inOut" } = {}) {
      tl.fromTo(els, { strokeDasharray: 1, strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: dur, stagger, ease }, at);
    },

    /** Word-by-word rise reveal. */
    revealWords(tl, el, at, { stagger = 0.07, dur = 0.55, y = 26 } = {}) {
      const ws = SV.splitWords(el);
      tl.fromTo(ws, { opacity: 0, y }, { opacity: 1, y: 0, duration: dur, stagger, ease: "power3.out" }, at);
      return ws;
    },

    /** Scene crossfade: scenes are opaque and stacked in order, so the incoming scene fades in
        over the outgoing one during the overlap that build_composition.py adds before each scene. */
    sceneFade(tl, el, start, end, { overlap = 0.45, first = false } = {}) {
      if (!first) tl.fromTo(el, { opacity: 0 }, { opacity: 1, duration: overlap, ease: "sine.inOut" }, Math.max(0, start - overlap));
    },

    /** Finite flicker for flames/lights (deterministic, no repeat:-1). */
    flicker(tl, el, start, dur, { min = 0.85, max = 1.08, step = 0.12, prop = "scaleY" } = {}) {
      for (let t = 0; t < dur; t += step) {
        tl.to(el, { [prop]: min + SV.rand() * (max - min), duration: step, ease: "sine.inOut" }, start + t);
      }
    },
  };
  /** Aligned word lookup: SV.word(T, "L04", "मारीच") / SV.word(T, "L04", 2) / SV.word(T, "L18", "कहे#2") -> {start, end} */
  SV.word = function (T, lineId, key) {
    const L = T.lines[lineId];
    if (!L) throw new Error("no line " + lineId);
    const ws = L.words || [];
    if (typeof key === "number") return ws[Math.max(0, Math.min(ws.length - 1, key))] || L;
    let n = 1;
    if (key.indexOf("#") > 0) { n = parseInt(key.split("#")[1], 10); key = key.split("#")[0]; }
    let hits = ws.filter((w) => w.w === key);
    if (!hits.length) hits = ws.filter((w) => w.w.startsWith(key) || key.startsWith(w.w));
    return hits[n - 1] || L;
  };
  /** Words of a line from token index a to b (inclusive) — e.g. the words a character "speaks". */
  SV.words = function (T, lineId, a = 0, b = 1e9) { return (T.lines[lineId].words || []).slice(a, b + 1); };
  window.SV = SV;
})();
