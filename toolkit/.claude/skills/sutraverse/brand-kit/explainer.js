/* SutraVerse EXPLAINER KIT v4 (CONTENT_STANDARDS §17). Infographics that teach, on one grid.
 *
 *   const st = EX.stage(sceneEl, { theme: "paper" | "night" });
 *   const h  = EX.head(st, { kicker: "SutraVerse Explains", title: "Why friends <em>go quiet</em>" });
 *   const a  = EX.node(st, { x: 300, y: 760, label: "You", sub: "lost the job", glyph: "1", color: EX.C.sindoor });
 *   const b  = EX.node(st, { x: 780, y: 760, label: "The group", glyph: "23" });
 *   const th = EX.thread(st, a, b, { label: "0 replies" });
 *   EX.compare(st, {...}) · EX.bars(st, {...}) · EX.steps(st, {...}) · EX.stat(st, {...}) · EX.cycle(st, {...})
 *   EX.callout(st, {...}) · EX.source(st, "Source: …")
 *   Motion (deterministic, transforms/opacity only, safe for HyperFrames seeking):
 *   EX.in(tl, els, t) · EX.draw(tl, paths, t) · EX.grow(tl, bars, t) · EX.count(tl, stat, t) · EX.focus(tl, keep, all, t) · EX.out(tl, els, t)
 *
 * Layout contract: content stays in x 72-1008, y 250-1400 (EX.BOX). Text never below 30 px.
 * At most 3 nodes or 4 bars or 4 steps per screen; one idea per screen; every number carries a source.
 */
(function () {
  const NS = "http://www.w3.org/2000/svg";
  const C = { kajal: "#100E17", neel: "#1A1D47", chandan: "#F4EADB", chandan2: "#D9CBB4", haldi: "#F2B33D", sindoor: "#D63E2A", mor: "#137C77", palash: "#EE7A2E", kumkum: "#9E2348" };
  const BOX = { x0: 72, x1: 1008, y0: 250, y1: 1400 };
  const h = (tag, cls, parent, html) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html !== undefined) e.innerHTML = html; if (parent) parent.appendChild(e); return e; };
  const s = (tag, attrs, parent) => { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); if (parent) parent.appendChild(e); return e; };
  const at = (e, x, y) => { e.style.left = x + "px"; e.style.top = y + "px"; return e; };
  const ink = (st) => getComputedStyle(st.el).getPropertyValue("--ex-ink").trim() || C.kajal;

  const EX = { C, BOX };
  EX.col = (c, span = 1) => ({ x: BOX.x0 + c * (936 + 24) / 12, w: span * (936 + 24) / 12 - 24 }); // 12-col grid

  EX.stage = (scene, { theme = "paper" } = {}) => {
    const el = h("div", "ex-stage" + (theme === "night" ? " ex-night" : ""), scene);
    const svg = s("svg", { class: "ex-svg", viewBox: "0 0 1080 1920" }, el);
    return { el, svg, theme };
  };
  EX.head = (st, { kicker, title }) => {
    const d = h("div", "ex-head", st.el);
    if (kicker) h("div", "ex-kicker", d, kicker);
    if (title) h("div", "ex-title", d, title);
    return d;
  };
  EX.node = (st, { x, y, r = 110, label, sub, glyph = "", color }) => {
    const n = at(h("div", "ex-node", st.el), x, y);
    if (color) n.style.setProperty("--c", color);
    const disc = h("div", "ex-disc", n, glyph); disc.style.width = disc.style.height = 2 * r + "px";
    if (label || sub) { const t = h("div", "ex-text", n); if (label) h("div", "ex-label", t, label); if (sub) h("div", "ex-sub", t, sub); }
    n._c = { x, y, r: r + 10 };
    return n;
  };
  // a thread between two points or nodes; trims at node discs; optional label pill at the midpoint
  EX.thread = (st, A, B, { color, curve = 0.22, width = 8, dashed = false, label, hi = false } = {}) => {
    const pa = A._c || { x: A[0], y: A[1], r: 0 }, pb = B._c || { x: B[0], y: B[1], r: 0 };
    // node centre is the disc centre; the disc sits at the top of the node box when it has a label
    const ca = A._c ? discCentre(A) : pa, cb = B._c ? discCentre(B) : pb;
    const dx = cb.x - ca.x, dy = cb.y - ca.y, L = Math.hypot(dx, dy), ux = dx / L, uy = dy / L;
    const x1 = ca.x + ux * pa.r, y1 = ca.y + uy * pa.r, x2 = cb.x - ux * pb.r, y2 = cb.y - uy * pb.r;
    const mx = (x1 + x2) / 2 - uy * L * curve, my = (y1 + y2) / 2 + ux * L * curve;
    const col = color || ink(st);
    const g = s("g", {}, st.svg);
    const p = s("path", { d: `M${x1} ${y1} Q${mx} ${my} ${x2} ${y2}`, fill: "none", stroke: col, "stroke-width": width, "stroke-linecap": "round", pathLength: 1 }, g);
    const p2 = s("path", { d: `M${x1} ${y1} Q${mx} ${my} ${x2} ${y2}`, fill: "none", stroke: col, "stroke-width": width * 0.35, "stroke-linecap": "round", pathLength: 1, transform: `translate(${-uy * 14} ${ux * 14})`, opacity: 0.8 }, g);
    if (dashed) [p, p2].forEach((q) => q.setAttribute("stroke-dasharray", "0.02 0.03"));
    const end = s("circle", { cx: x2, cy: y2, r: width * 1.3, fill: col }, g);
    const out = { g, paths: [p, p2], end, mid: { x: (x1 + 2 * mx + x2) / 4, y: (y1 + 2 * my + y2) / 4 } };
    if (label) out.pill = EX.callout(st, { at: [out.mid.x, out.mid.y], label, hi });
    return out;
  };
  function discCentre(n) { const d = n.querySelector(".ex-disc"); const r = parseFloat(d.style.width) / 2; const box = n.getBoundingClientRect(); const stg = n.closest(".ex-stage").getBoundingClientRect(); const k = 1080 / stg.width; return { x: n._c.x, y: (box.top - stg.top) * k + r }; }

  EX.callout = (st, { at: p, label, hi = false, from }) => {
    if (from) s("path", { d: `M${from[0]} ${from[1]} L${p[0]} ${p[1]}`, stroke: ink(st), "stroke-width": 4, fill: "none", pathLength: 1 }, st.svg);
    const e = at(h("div", "ex-pill" + (hi ? " ex-hi" : ""), st.el, label), p[0], p[1]);
    return e;
  };
  EX.compare = (st, { top = 560, height, left, right }) => {
    const mk = (side, d) => { const c = h("div", "ex-card", st.el); c.style.top = top + "px"; if (height) c.style.height = height + "px"; c.style.width = "444px"; c.style.left = (side ? 564 : 72) + "px"; if (d.color) c.style.setProperty("--c", d.color);
      h("h3", "", c, d.title); const ul = h("ul", "", c); (d.items || []).forEach((it) => h("li", "", ul, it)); return c; };
    const L = mk(0, left), R = mk(1, right);
    const H = Math.max(L.offsetHeight, R.offsetHeight) || height || 600; L.style.height = R.style.height = H + "px";
    const vs = h("div", "ex-vs", st.el, "VS"); vs.style.top = top + H / 2 + "px";
    return { L, R, vs, items: [...L.querySelectorAll("li"), ...R.querySelectorAll("li")] };
  };
  EX.bars = (st, { top = 560, gap = 190, rows, max, source }) => {
    const m = max || Math.max(...rows.map((r) => r.value));
    const out = rows.map((r, i) => {
      const row = h("div", "ex-bar-row", st.el); row.style.top = top + i * gap + "px"; if (r.color) row.style.setProperty("--c", r.color);
      const tp = h("div", "ex-bar-top", row); h("div", "ex-label", tp, r.label); const v = h("div", "ex-bar-val", tp, r.display || String(r.value));
      const tr = h("div", "ex-bar-track", row); const f = h("div", "ex-bar-fill", tr); f.style.width = (100 * r.value) / m + "%";
      return { row, fill: f, val: v, value: r.value };
    });
    if (source) EX.source(st, source);
    return out;
  };
  EX.steps = (st, { top = 560, gap = 200, items, color }) => {
    const out = items.map((it, i) => {
      const r = h("div", "ex-step", st.el); r.style.top = top + i * gap + "px"; if (it.color || color) r.style.setProperty("--c", it.color || color);
      h("div", "ex-num", r, String(i + 1)); const t = h("div", "", r); h("div", "ex-label", t, it.label); if (it.sub) h("div", "ex-sub", t, it.sub);
      return r;
    });
    const line = s("path", { d: `M128 ${top + 112} L128 ${top + (items.length - 1) * gap}`, stroke: ink(st), "stroke-width": 5, "stroke-dasharray": "0.015 0.02", pathLength: 1, fill: "none" }, st.svg);
    return { steps: out, line };
  };
  EX.stat = (st, { x = 540, y = 760, value, decimals = 0, prefix = "", suffix = "", label, source }) => {
    const box = at(h("div", "ex-abs", st.el), 72, y - 120); box.style.width = "936px"; box.style.textAlign = "center";
    const num = h("div", "ex-stat", box); const frames = [];
    for (let k = 0; k <= 12; k++) { const v = (value * k) / 12; const sp = h("span", "", num, prefix + v.toLocaleString("en-IN", { maximumFractionDigits: decimals, minimumFractionDigits: decimals }) + suffix); sp.style.display = k === 12 ? "inline" : "none"; frames.push(sp); }
    if (label) { const l = h("div", "ex-label", box, label); l.style.marginTop = "18px"; }
    if (source) EX.source(st, source);
    return { box, num, frames };
  };
  EX.cycle = (st, { cx = 540, cy = 830, R = 300, items, r = 92 }) => {
    const n = items.length, nodes = [];
    items.forEach((it, i) => { const a = -Math.PI / 2 + (i * 2 * Math.PI) / n; nodes.push(EX.node(st, { x: cx + R * Math.cos(a), y: cy + R * Math.sin(a), r, label: it.label, glyph: it.glyph || String(i + 1), color: it.color })); });
    const arcs = nodes.map((nd, i) => { const a1 = -Math.PI / 2 + (i * 2 * Math.PI) / n + 0.42, a2 = -Math.PI / 2 + ((i + 1) * 2 * Math.PI) / n - 0.42;
      return s("path", { d: `M${cx + R * Math.cos(a1)} ${cy + R * Math.sin(a1)} A${R} ${R} 0 0 1 ${cx + R * Math.cos(a2)} ${cy + R * Math.sin(a2)}`, fill: "none", stroke: ink(st), "stroke-width": 7, "stroke-linecap": "round", pathLength: 1 }, st.svg); });
    return { nodes, arcs };
  };
  EX.source = (st, text) => h("div", "ex-source", st.el, text);

  // ---- motion (one vocabulary, used the same way in every explainer) ----
  const arr = (x) => (Array.isArray(x) ? x : x && x.length !== undefined && !(x instanceof Element) ? Array.from(x) : [x]);
  EX.in = (tl, els, t, { stagger = 0.12, y = 24, dur = 0.45 } = {}) => tl.fromTo(arr(els), { opacity: 0, y }, { opacity: 1, y: 0, duration: dur, stagger, ease: "power2.out" }, t);
  EX.pop = (tl, els, t, { stagger = 0.1 } = {}) => tl.fromTo(arr(els), { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.45, stagger, ease: "back.out(1.8)" }, t);
  EX.draw = (tl, paths, t, { dur = 0.8, stagger = 0.1 } = {}) => {
    const ps = arr(paths).flatMap((p) => (p && p.paths ? [...p.paths, p.end] : [p]));
    const strokes = ps.filter((p) => p && p.tagName === "path"), dots = ps.filter((p) => p && p.tagName === "circle");
    tl.fromTo(strokes, { strokeDasharray: "1 1", strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: dur, stagger, ease: "power2.inOut" }, t);
    if (dots.length) tl.fromTo(dots, { opacity: 0 }, { opacity: 1, duration: 0.15 }, t + dur * 0.9);
  };
  EX.grow = (tl, bars, t, { stagger = 0.18, dur = 0.8 } = {}) => {
    tl.fromTo(bars.map((b) => b.row), { opacity: 0 }, { opacity: 1, duration: 0.3, stagger }, t);
    tl.fromTo(bars.map((b) => b.fill), { scaleX: 0 }, { scaleX: 1, duration: dur, stagger, ease: "power3.out" }, t + 0.1);
  };
  EX.count = (tl, stat, t, { dur = 1.0 } = {}) => {
    const fr = stat.frames; fr.forEach((sp, k) => tl.set(sp, { display: "none" }, t));
    fr.forEach((sp, k) => { tl.set(sp, { display: "inline" }, t + (dur * k) / (fr.length - 1)); if (k > 0) tl.set(fr[k - 1], { display: "none" }, t + (dur * k) / (fr.length - 1)); });
    EX.in(tl, stat.box, t - 0.05, { dur: 0.3 });
  };
  EX.focus = (tl, keep, all, t, { dur = 0.35 } = {}) => { const k = new Set(arr(keep)); tl.to(arr(all).filter((e) => !k.has(e)), { opacity: 0.25, duration: dur }, t); tl.to(arr(keep), { opacity: 1, duration: dur }, t); };
  EX.out = (tl, els, t, { dur = 0.3 } = {}) => tl.to(arr(els), { opacity: 0, y: -16, duration: dur, ease: "power1.in" }, t);

  window.EX = EX;
})();
