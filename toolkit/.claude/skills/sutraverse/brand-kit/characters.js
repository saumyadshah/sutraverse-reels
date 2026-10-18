/* SutraVerse character rigs — reusable, respectful, flat-vector "virtual actors".
 *
 *   const r = SVC.make("ravana", svgGroup, { x: 540, y: 1500, s: 1.0, flip: false });
 *   SVC.idle(tl, r, t0, dur);                    // breathing + natural blinks
 *   SVC.talk(tl, r, T.lines.L05.words);          // mouth opens on every aligned WORD
 *   SVC.emote(tl, r, "angry", t);                // calm | smirk | angry | sad | shock | worried
 *   SVC.gesture(tl, r, "point", t);              // point | dismiss | plead | raise | fist | rest
 *   SVC.walkOut(tl, r, t, dx);  SVC.tremble(tl, r, t, dur);  SVC.cry(tl, r, t, dur);
 *
 * Coordinates: origin at the character's feet, ~1000 units tall at s = 1. Every part is an
 * SVG group with its own pivot so GSAP can rotate it (svgOrigin in character space).
 * Design rules (references/visual-direction.md): dignified, no gore, no mockery of sacred figures;
 * deities are not drawn as cartoon characters (Rama appears only as light / an arrow).
 */
(function () {
  const NS = "http://www.w3.org/2000/svg";
  const el = (tag, attrs, parent) => {
    const e = document.createElementNS(NS, tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  };
  const g = (parent, attrs = {}) => el("g", attrs, parent);

  const PALETTE = {
    ravana:    { skin: "#B5652F", robe: "#C21F45", robe2: "#7E1235", trim: "#FFB22E", hair: "#1A1240", crown: "#FFC94A" },
    maricha:   { skin: "#9C6B4A", robe: "#C77A2E", robe2: "#8C4F1A", trim: "#FFD36B", hair: "#5B5B6E", crown: null },
    vibhishana:{ skin: "#A86A3D", robe: "#2E8C7E", robe2: "#1D5E57", trim: "#FFD36B", hair: "#1A1240", crown: "#FFC94A" },
    malyavan:  { skin: "#A97A55", robe: "#6A3FB0", robe2: "#45267A", trim: "#FFD36B", hair: "#F2EEE6", crown: null },
    mandodari: { skin: "#C68A5E", robe: "#E8457A", robe2: "#A3245A", trim: "#FFD36B", hair: "#1A1240", crown: "#FFC94A" },
    rohan:     { skin: "#B97A4F", robe: "#2F6FE0", robe2: "#1B4AA8", trim: "#FFFFFF", hair: "#1A1240", crown: null },
  };

  function head(parent, P, o) {
    // head group pivots at the neck (0, -760)
    const H = g(parent, { class: "c-head" });
    const r = o.headR || 72;
    const cy = -800;
    if (o.longHair) el("path", { d: `M${-r * 1.05} ${cy - 10} Q${-r * 1.25} ${cy + r * 2.2} ${-r * 0.4} ${cy + r * 2.6} L${r * 0.4} ${cy + r * 2.6} Q${r * 1.25} ${cy + r * 2.2} ${r * 1.05} ${cy - 10} Z`, fill: P.hair }, H);
    el("rect", { x: -26, y: cy + r * 0.7, width: 52, height: 60, rx: 18, fill: P.skin }, H); // neck
    el("ellipse", { cx: 0, cy, rx: r * 0.92, ry: r, fill: P.skin }, H);
    const flush = el("ellipse", { cx: 0, cy: cy + r * 0.1, rx: r * 0.86, ry: r * 0.9, fill: "#FF3B3B", opacity: 0 }, H);
    el("ellipse", { cx: -r * 0.9, cy: cy + 6, rx: 12, ry: 18, fill: P.skin }, H); // ears
    el("ellipse", { cx: r * 0.9, cy: cy + 6, rx: 12, ry: 18, fill: P.skin }, H);
    if (o.earrings) { el("circle", { cx: -r * 0.92, cy: cy + 30, r: 9, fill: P.trim }, H); el("circle", { cx: r * 0.92, cy: cy + 30, r: 9, fill: P.trim }, H); }
    // hair / bun / turban
    if (o.hair === "bun") { el("path", { d: `M${-r * 0.95} ${cy - 10} Q${-r * 0.9} ${cy - r * 1.05} 0 ${cy - r * 1.05} Q${r * 0.9} ${cy - r * 1.05} ${r * 0.95} ${cy - 10} Q${r * 0.5} ${cy - r * 0.6} 0 ${cy - r * 0.62} Q${-r * 0.5} ${cy - r * 0.6} ${-r * 0.95} ${cy - 10} Z`, fill: P.hair }, H); el("ellipse", { cx: 0, cy: cy - r * 1.18, rx: r * 0.42, ry: r * 0.32, fill: P.hair }, H); }
    if (o.hair === "short") el("path", { d: `M${-r * 0.95} ${cy - 4} Q${-r} ${cy - r * 1.1} 0 ${cy - r * 1.06} Q${r} ${cy - r * 1.1} ${r * 0.95} ${cy - 4} Q${r * 0.6} ${cy - r * 0.55} ${r * 0.1} ${cy - r * 0.7} Q${-r * 0.5} ${cy - r * 0.5} ${-r * 0.95} ${cy - 4} Z`, fill: P.hair }, H);
    if (o.hair === "matted") { el("path", { d: `M${-r} ${cy} Q${-r * 1.1} ${cy - r * 1.2} 0 ${cy - r * 1.1} Q${r * 1.1} ${cy - r * 1.2} ${r} ${cy} Q${r * 0.6} ${cy - r * 0.6} 0 ${cy - r * 0.66} Q${-r * 0.6} ${cy - r * 0.6} ${-r} ${cy} Z`, fill: P.hair }, H); el("path", { d: `M${-r * 0.3} ${cy - r * 1.05} Q0 ${cy - r * 1.9} ${r * 0.3} ${cy - r * 1.05} Z`, fill: P.hair }, H); }
    if (o.hair === "white") { el("path", { d: `M${-r * 0.95} ${cy} Q${-r} ${cy - r * 0.95} 0 ${cy - r * 0.98} Q${r} ${cy - r * 0.95} ${r * 0.95} ${cy} Q${r * 0.55} ${cy - r * 0.62} 0 ${cy - r * 0.7} Q${-r * 0.55} ${cy - r * 0.62} ${-r * 0.95} ${cy} Z`, fill: P.hair }, H); }
    if (o.turban) el("path", { d: `M${-r * 1.02} ${cy - r * 0.35} Q${-r * 1.1} ${cy - r * 1.35} 0 ${cy - r * 1.4} Q${r * 1.1} ${cy - r * 1.35} ${r * 1.02} ${cy - r * 0.35} Q0 ${cy - r * 0.7} ${-r * 1.02} ${cy - r * 0.35} Z`, fill: o.turban }, H);
    if (o.crown) {
      const C = g(H, { class: "c-crown" });
      el("path", { d: `M${-r * 0.9} ${cy - r * 0.62} L${-r * 0.95} ${cy - r * 1.5} L${-r * 0.5} ${cy - r * 1.15} L${-r * 0.25} ${cy - r * 1.85} L0 ${cy - r * 1.25} L${r * 0.25} ${cy - r * 1.85} L${r * 0.5} ${cy - r * 1.15} L${r * 0.95} ${cy - r * 1.5} L${r * 0.9} ${cy - r * 0.62} Z`, fill: P.crown, stroke: "#E08A1E", "stroke-width": 4 }, C);
      el("circle", { cx: 0, cy: cy - r * 0.95, r: 11, fill: "#E8344B" }, C);
      el("circle", { cx: -r * 0.55, cy: cy - r * 0.85, r: 7, fill: "#2E8C7E" }, C);
      el("circle", { cx: r * 0.55, cy: cy - r * 0.85, r: 7, fill: "#2E8C7E" }, C);
    }
    if (o.tilak) el("path", { d: `M-5 ${cy - r * 0.55} L0 ${cy - r * 0.28} L5 ${cy - r * 0.55} Z`, fill: o.tilak }, H);
    if (o.bindi) el("circle", { cx: 0, cy: cy - r * 0.42, r: 7, fill: "#E8344B" }, H);
    // eyes (white, iris, pupil) + lids for blinks
    const eyes = [], lids = [], pupils = [];
    [-1, 1].forEach((side) => {
      const ex = side * r * 0.36, ey = cy - r * 0.08;
      el("ellipse", { cx: ex, cy: ey, rx: r * 0.17, ry: r * 0.13, fill: "#FFFFFF" }, H);
      const pu = el("circle", { cx: ex + side * 2, cy: ey + 1, r: r * 0.085, fill: "#1A1240" }, H);
      el("circle", { cx: ex + side * 2 - 3, cy: ey - 3, r: 3, fill: "#FFFFFF" }, H);
      const lid = el("rect", { x: ex - r * 0.2, y: ey - r * 0.17, width: r * 0.4, height: r * 0.34, fill: P.skin }, H);
      gsap.set(lid, { scaleY: 0, svgOrigin: `${ex} ${ey - r * 0.17}` });
      eyes.push({ ex, ey }); lids.push(lid); pupils.push(pu);
    });
    // brows (pivot at inner end)
    const brows = [-1, 1].map((side) => {
      const bx = side * r * 0.36, by = cy - r * 0.32;
      const b = el("path", { d: `M${bx - r * 0.2} ${by} Q${bx} ${by - (o.thickBrows ? 12 : 9)} ${bx + r * 0.2} ${by}`, stroke: o.browColor || P.hair, "stroke-width": o.thickBrows ? 11 : 7, fill: "none", "stroke-linecap": "round" }, H);
      return { el: b, side, x: bx - side * r * 0.2, y: by };
    });
    el("path", { d: `M-4 ${cy + r * 0.05} Q-8 ${cy + r * 0.3} 0 ${cy + r * 0.33} Q8 ${cy + r * 0.3} 4 ${cy + r * 0.05}`, stroke: "rgba(26,18,64,.35)", "stroke-width": 4, fill: "none", "stroke-linecap": "round" }, H); // nose
    if (o.mustache) el("path", { d: `M${-r * 0.42} ${cy + r * 0.5} Q${-r * 0.2} ${cy + r * 0.32} 0 ${cy + r * 0.44} Q${r * 0.2} ${cy + r * 0.32} ${r * 0.42} ${cy + r * 0.5} Q${r * 0.5} ${cy + r * 0.36} ${r * 0.58} ${cy + r * 0.3} Q${r * 0.3} ${cy + r * 0.62} 0 ${cy + r * 0.52} Q${-r * 0.3} ${cy + r * 0.62} ${-r * 0.58} ${cy + r * 0.3} Q${-r * 0.5} ${cy + r * 0.36} ${-r * 0.42} ${cy + r * 0.5} Z`, fill: o.mustacheColor || P.hair }, H);
    if (o.beard) el("path", { d: `M${-r * 0.8} ${cy + r * 0.2} Q${-r * 0.75} ${cy + r * 1.6} 0 ${cy + r * 2.1} Q${r * 0.75} ${cy + r * 1.6} ${r * 0.8} ${cy + r * 0.2} Q${r * 0.4} ${cy + r * 0.9} 0 ${cy + r * 0.85} Q${-r * 0.4} ${cy + r * 0.9} ${-r * 0.8} ${cy + r * 0.2} Z`, fill: o.beard }, H);
    // mouth: closed line + open shape (talk toggles scaleY of the open shape)
    const my = cy + r * 0.62;
    const mouthClosed = el("path", { d: `M${-r * 0.22} ${my} Q0 ${my + 8} ${r * 0.22} ${my}`, stroke: "#5A1E2E", "stroke-width": 6, fill: "none", "stroke-linecap": "round" }, H);
    const mouthOpen = el("ellipse", { cx: 0, cy: my + 6, rx: r * 0.2, ry: r * 0.15, fill: "#5A1E2E" }, H);
    gsap.set(mouthOpen, { scaleY: 0, svgOrigin: `0 ${my - 2}` });
    const tear = el("path", { d: `M${-r * 0.36} ${cy + r * 0.06} q-7 16 0 22 q7 -6 0 -22 z`, fill: "#9FD8FF", opacity: 0 }, H);
    return { H, eyes, lids, pupils, brows, mouthOpen, mouthClosed, tear, flush, cy, r };
  }

  function body(parent, P, o) {
    const B = g(parent, { class: "c-body" });
    const w = o.bodyW || 1;
    if (o.kneel) {
      el("path", { d: `M${-210 * w} 0 Q${-230 * w} -260 ${-110 * w} -460 L${110 * w} -460 Q${230 * w} -260 ${210 * w} 0 Z`, fill: P.robe }, B);
      el("path", { d: `M${-210 * w} 0 L${210 * w} 0`, stroke: P.trim, "stroke-width": 10 }, B);
    } else {
      el("path", { d: `M${-150 * w} 0 L${-120 * w} -420 L${120 * w} -420 L${150 * w} 0 Z`, fill: P.robe2 }, B); // lower garment
      el("path", { d: `M${-150 * w} -10 L${150 * w} -10`, stroke: P.trim, "stroke-width": 12 }, B);
      el("rect", { x: -70 * w, y: -40, width: 50 * w, height: 40, rx: 14, fill: "#3A2A1E" }, B);
      el("rect", { x: 20 * w, y: -40, width: 50 * w, height: 40, rx: 14, fill: "#3A2A1E" }, B);
    }
    const top = o.kneel ? -460 : -420;
    el("path", { d: `M${-125 * w} ${top + 10} Q${-140 * w} ${top - 200} ${-95 * w} -700 L${95 * w} -700 Q${140 * w} ${top - 200} ${125 * w} ${top + 10} Z`, fill: P.robe }, B); // torso
    el("path", { d: `M${-95 * w} -700 Q0 ${-640} ${95 * w} -700`, stroke: P.trim, "stroke-width": 10, fill: "none" }, B); // collar
    if (o.sash) el("path", { d: `M${-90 * w} -690 L${110 * w} ${top + 20}`, stroke: o.sash, "stroke-width": 26, "stroke-linecap": "round" }, B);
    if (o.necklace) el("path", { d: `M${-70 * w} -690 Q0 -600 ${70 * w} -690`, stroke: P.trim, "stroke-width": 9, fill: "none", "stroke-dasharray": "2 14", "stroke-linecap": "round" }, B);
    if (o.rudraksha) el("path", { d: `M${-60 * w} -695 Q0 -590 ${60 * w} -695`, stroke: "#6B3A1E", "stroke-width": 12, fill: "none", "stroke-dasharray": "1 16", "stroke-linecap": "round" }, B);
    if (o.belt) el("rect", { x: -125 * w, y: top - 20, width: 250 * w, height: 30, rx: 10, fill: P.trim }, B);
    return B;
  }

  function arm(parent, P, side, o) {
    const w = o.bodyW || 1;
    const sx = side * 110 * w, sy = -680;
    const A = g(parent, { class: side < 0 ? "c-armL" : "c-armR" });
    el("path", { d: `M${sx - 26} ${sy} L${sx - 20} ${sy + 280} L${sx + 22} ${sy + 280} L${sx + 26} ${sy} Z`, fill: P.robe }, A);
    if (o.bangles) el("rect", { x: sx - 24, y: sy + 250, width: 48, height: 14, rx: 6, fill: P.trim }, A);
    el("circle", { cx: sx, cy: sy + 300, r: 26, fill: P.skin }, A);
    if (o.prop && o.prop.side === side) {
      if (o.prop.kind === "staff") el("path", { d: `M${sx} ${sy - 120} L${sx} ${sy + 700}`, stroke: "#C77A2E", "stroke-width": 16, "stroke-linecap": "round" }, A);
      if (o.prop.kind === "sword") el("path", { d: `M${sx} ${sy + 300} L${sx + side * 20} ${sy - 140}`, stroke: "#E8E8F0", "stroke-width": 14, "stroke-linecap": "round" }, A);
      if (o.prop.kind === "phone") el("rect", { x: sx - 22, y: sy + 230, width: 44, height: 80, rx: 8, fill: "#1A1240", stroke: "#FFFFFF", "stroke-width": 3 }, A);
    }
    return { el: A, ox: sx, oy: sy };
  }

  function extraHeads(parent, P, n, r) {
    // Ravana's other nine heads, in an arc behind the main head
    const G = g(parent, { class: "c-heads" });
    const out = [];
    const order = [-4, 4, -3, 3, -2, 2, -1, 1, 0].slice(0, n);
    order.forEach((k) => {
      if (k === 0) return;
      const x = k * r * 0.95, y = -800 - Math.abs(k) * 6 + (Math.abs(k) > 2 ? 20 : 0);
      const h = g(G, { class: "c-xhead" });
      el("ellipse", { cx: x, cy: y, rx: r * 0.72, ry: r * 0.8, fill: P.skin, stroke: "#8A4421", "stroke-width": 3 }, h);
      el("path", { d: `M${x - r * 0.62} ${y - r * 0.45} L${x - r * 0.55} ${y - r * 1.25} L${x - r * 0.2} ${y - r * 0.9} L${x} ${y - r * 1.4} L${x + r * 0.2} ${y - r * 0.9} L${x + r * 0.55} ${y - r * 1.25} L${x + r * 0.62} ${y - r * 0.45} Z`, fill: P.crown, stroke: "#E08A1E", "stroke-width": 3 }, h);
      el("path", { d: `M${x - r * 0.42} ${y - r * 0.2} L${x - r * 0.14} ${y - r * 0.1} M${x + r * 0.42} ${y - r * 0.2} L${x + r * 0.14} ${y - r * 0.1}`, stroke: P.hair, "stroke-width": 6, "stroke-linecap": "round" }, h);
      el("circle", { cx: x - r * 0.26, cy: y, r: r * 0.07, fill: "#1A1240" }, h);
      el("circle", { cx: x + r * 0.26, cy: y, r: r * 0.07, fill: "#1A1240" }, h);
      el("path", { d: `M${x - r * 0.32} ${y + r * 0.42} Q${x} ${y + r * 0.26} ${x + r * 0.32} ${y + r * 0.42}`, fill: P.hair }, h);
      out.push(h);
    });
    parent.insertBefore(G, parent.firstChild);
    return out;
  }

  const SPECS = {
    ravana:     { pal: "ravana", o: { headR: 80, bodyW: 1.25, crown: true, mustache: true, thickBrows: true, earrings: true, necklace: true, belt: true, sash: "#FFB22E", hair: "short", heads: 9, prop: { kind: "sword", side: 1 } } },
    maricha:    { pal: "maricha", o: { headR: 70, hair: "matted", beard: "#5B5B6E", rudraksha: true, thickBrows: true, browColor: "#3A3A4E", tilak: "#FFFFFF" } },
    vibhishana: { pal: "vibhishana", o: { headR: 70, crown: true, tilak: "#FFFFFF", necklace: true, earrings: true, sash: "#FFD36B", hair: "short" } },
    malyavan:   { pal: "malyavan", o: { headR: 70, hair: "white", turban: "#FFF6E6", beard: "#F2EEE6", browColor: "#F2EEE6", mustache: true, mustacheColor: "#F2EEE6", prop: { kind: "staff", side: 1 } } },
    mandodari:  { pal: "mandodari", o: { headR: 68, hair: "bun", longHair: false, crown: true, bindi: true, earrings: true, necklace: true, bangles: true, sash: "#FFD36B" } },
    rohan:      { pal: "rohan", o: { headR: 70, hair: "short", bodyW: 0.95, prop: { kind: "phone", side: 1 } } },
  };

  function make(kind, parent, opts = {}) {
    const spec = SPECS[kind];
    const P = PALETTE[spec.pal];
    const o = Object.assign({}, spec.o, opts.o || {});
    if (opts.kneel) o.kneel = true;
    const root = g(parent, { class: "c-root c-" + kind });
    const inner = g(root, { class: "c-inner" });
    const shadow = el("ellipse", { cx: 0, cy: 6, rx: 190 * (o.bodyW || 1), ry: 26, fill: "rgba(10,16,60,.35)" }, inner);
    const armBack = arm(inner, P, -1, o);
    const B = body(inner, P, o);
    const hd = head(inner, P, o);
    if (o.kneel) hd.H.setAttribute("transform", "translate(0 260)");
    const armFront = arm(inner, P, 1, o);
    if (o.kneel) { armBack.el.setAttribute("transform", "translate(0 260)"); armFront.el.setAttribute("transform", "translate(0 260)"); }
    const heads = o.heads ? extraHeads(hd.H, P, o.heads + 1, o.headR) : [];
    const s = opts.s || 1, x = opts.x || 0, y = opts.y || 0, flip = opts.flip ? -1 : 1;
    root.setAttribute("transform", `translate(${x} ${y}) scale(${s * flip} ${s})`);
    const rig = { kind, root, inner, head: hd.H, body: B, armL: armBack, armR: armFront, heads, shadow,
      eyes: hd.eyes, lids: hd.lids, pupils: hd.pupils, brows: hd.brows, mouthOpen: hd.mouthOpen, mouthClosed: hd.mouthClosed,
      tear: hd.tear, flush: hd.flush, cy: hd.cy + (o.kneel ? 260 : 0), r: hd.r, kneel: !!o.kneel, flip };
    return rig;
  }

  // ---------------------------------------------------------------- animation verbs
  function blink(tl, rig, t) {
    tl.to(rig.lids, { scaleY: 1, duration: 0.06, ease: "none" }, t);
    tl.to(rig.lids, { scaleY: 0, duration: 0.08, ease: "none" }, t + 0.1);
  }
  function idle(tl, rig, t0, dur, { blinks = true, sway = 1 } = {}) {
    const neckY = rig.cy + 60;
    tl.fromTo(rig.inner, { y: 0 }, { y: -6 * sway, duration: 1.6, yoyo: true, repeat: Math.max(1, Math.floor(dur / 1.6)), ease: "sine.inOut" }, t0);
    tl.fromTo(rig.head, { rotation: -1.5 * sway, svgOrigin: `0 ${neckY}` }, { rotation: 1.5 * sway, duration: 2.1, yoyo: true, repeat: Math.max(1, Math.floor(dur / 2.1)), ease: "sine.inOut" }, t0);
    if (blinks) for (let t = t0 + 0.6 + (SV.rand() * 0.8); t < t0 + dur - 0.2; t += 2.2 + SV.rand() * 1.8) blink(tl, rig, t);
  }
  /** Lip-flap on the ALIGNED words: open on each word start, close just before the next. */
  function talk(tl, rig, words, { openness = 1, jaw = true } = {}) {
    (words || []).forEach((w, i) => {
      const nxt = words[i + 1] ? words[i + 1].start : w.end + 0.1;
      const len = Math.max(0.08, Math.min(w.end, nxt - 0.03) - w.start);
      const syl = Math.max(1, Math.round(len / 0.17));            // a few flaps per long word, not one
      for (let k = 0; k < syl; k++) {
        const t = w.start + (k * len) / syl, d = len / syl;
        tl.to(rig.mouthOpen, { scaleY: openness * (0.65 + 0.35 * ((i + k) % 2)), duration: Math.min(0.07, d * 0.4), ease: "power1.out" }, t);
        tl.to(rig.mouthOpen, { scaleY: 0.12, duration: Math.min(0.08, d * 0.5), ease: "power1.in" }, t + d * 0.55);
      }
      tl.to(rig.mouthOpen, { scaleY: 0, duration: 0.06 }, w.start + len);
    });
    if (jaw && words && words.length) {
      const t0 = words[0].start, t1 = words[words.length - 1].end;
      tl.fromTo(rig.head, { y: 0 }, { y: 4, duration: 0.18, yoyo: true, repeat: Math.max(1, Math.floor((t1 - t0) / 0.18)), ease: "sine.inOut" }, t0);
    }
  }
  const MOODS = {
    calm:    { brow: [0, 0], by: 0, flush: 0 },
    smirk:   { brow: [-8, 14], by: -2, flush: 0 },
    angry:   { brow: [22, 22], by: 6, flush: 0.28 },
    sad:     { brow: [-18, -18], by: -4, flush: 0 },
    shock:   { brow: [-6, -6], by: -14, flush: 0 },
    worried: { brow: [-14, -14], by: -6, flush: 0 },
  };
  function emote(tl, rig, mood, t, dur = 0.25) {
    const m = MOODS[mood] || MOODS.calm;
    rig.brows.forEach((b, i) => {
      // rotate around the inner end; side flips the sense so "22" means inner end down on both
      tl.to(b.el, { rotation: m.brow[i] * b.side, y: m.by, svgOrigin: `${b.x} ${b.y}`, duration: dur, ease: "power2.out" }, t);
    });
    tl.to(rig.flush, { opacity: m.flush, duration: dur }, t);
    if (mood === "shock") tl.to(rig.mouthOpen, { scaleY: 1, duration: 0.12 }, t);
    if (mood === "smirk") tl.to(rig.mouthClosed, { rotation: -8, svgOrigin: `0 ${rig.cy - 0 + rig.r * 0.62}`, duration: dur }, t);
    else tl.to(rig.mouthClosed, { rotation: 0, duration: dur }, t);
    if (mood === "angry") tl.fromTo(rig.inner, { x: 0 }, { x: 6, duration: 0.05, yoyo: true, repeat: 7 }, t + dur);
  }
  const POSES = {
    rest: { L: 0, R: 0 }, point: { L: 0, R: -78 }, dismiss: { L: 0, R: -120 }, plead: { L: -38, R: 38 },
    raise: { L: 0, R: -150 }, fist: { L: 0, R: -60 }, shrug: { L: 40, R: -40 }, wipe: { L: 0, R: -140 },
  };
  function gesture(tl, rig, pose, t, dur = 0.35) {
    const p = POSES[pose] || POSES.rest;
    tl.to(rig.armL.el, { rotation: p.L, svgOrigin: `${rig.armL.ox} ${rig.armL.oy}`, duration: dur, ease: "back.out(1.6)" }, t);
    tl.to(rig.armR.el, { rotation: p.R, svgOrigin: `${rig.armR.ox} ${rig.armR.oy}`, duration: dur, ease: "back.out(1.6)" }, t);
    if (pose === "dismiss") tl.to(rig.armR.el, { rotation: -40, duration: 0.25, ease: "power2.in" }, t + dur + 0.05);
    if (pose === "fist") tl.to(rig.armR.el, { rotation: -20, duration: 0.12, yoyo: true, repeat: 3 }, t + dur);
  }
  function lookAt(tl, rig, dir, t) { tl.to(rig.pupils, { x: dir * 4, duration: 0.2 }, t); }
  function tremble(tl, rig, t, dur) { tl.fromTo(rig.inner, { x: -3 }, { x: 3, duration: 0.05, yoyo: true, repeat: Math.floor(dur / 0.05) }, t); }
  function cry(tl, rig, t, dur) {
    for (let k = 0; k < Math.floor(dur / 0.9); k++) {
      tl.fromTo(rig.tear, { opacity: 0.95, y: 0 }, { opacity: 0, y: rig.r * 1.1, duration: 0.85, ease: "power1.in" }, t + k * 0.9);
    }
    tl.fromTo(rig.inner, { y: 0 }, { y: 6, duration: 0.45, yoyo: true, repeat: Math.floor(dur / 0.45), ease: "sine.inOut" }, t);
  }
  function walkOut(tl, rig, t, dx = 700, dur = 1.6) {
    tl.to(rig.inner, { x: dx, duration: dur, ease: "power1.in" }, t);
    tl.fromTo(rig.inner, { y: 0 }, { y: -14, duration: 0.2, yoyo: true, repeat: Math.floor(dur / 0.2), ease: "sine.inOut" }, t);
    tl.to(rig.root, { opacity: 0, duration: 0.4 }, t + dur - 0.4);
  }
  function headsNod(tl, rig, t, dur) {
    rig.heads.forEach((h, i) => tl.fromTo(h, { y: 0 }, { y: -8, duration: 0.5, yoyo: true, repeat: Math.max(1, Math.floor(dur / 0.5)), ease: "sine.inOut" }, t + i * 0.07));
  }
  window.SVC = { make, idle, blink, talk, emote, gesture, lookAt, tremble, cry, walkOut, headsNod, PALETTE };
})();
