/* SutraVerse 2.0 character rig (canvas 2D, deterministic; works inside an opuscar render(t)).
 *
 * One parametric head + bust + body per character. The face is built on a 3D-ish head
 * (elliptical cross-sections) and projected for any head turn (yaw -1..1, ~ -60..60 deg),
 * so a character looks like the SAME person in every shot size and angle.
 *
 *   CAST2.define(name, spec)            register a character (or CAST2.load(json))
 *   CAST2.draw(ctx, name|spec, pose)    draw at pose = {x, y, s, yaw, tilt, mood, blink,
 *                                        talk, lookX, lookY, body, arms, light, style}
 *     x, y   screen position of the chin-neck point; s = pixels per head-height
 *     body   "head" | "bust" (default) | "full"
 *     style  "cel" (flat colour + hard shadow) | "engrave" (paper + ink hatching)
 *     mood   neutral smile grin sad worried angry shock smirk think tired
 *     arms   rest | fold | point | chin | phone | open | raise   (bust/full)
 *   CAST2.MOODS, CAST2.ARMS, CAST2.registry
 *
 * Rules (CONTENT_STANDARDS 2.0 §C): a registered character is never redrawn by hand; shot sizes are the
 * same rig at a different s; held props come from `arms` poses so they sit in a hand.
 */
(function (root) {
  const CAST2 = {}; const REG = {};
  CAST2.registry = REG;
  CAST2.define = (n, spec) => (REG[n] = Object.assign({ name: n }, spec));
  CAST2.load = (j) => Object.entries(j.characters || j).forEach(([k, v]) => k[0] !== "_" && CAST2.define(k, v));

  const SKIN = { // base, shadow, line
    1: ["#E9C3A0", "#C99A78", "#5A3A2A"], 2: ["#D9A87F", "#B5825C", "#4E2F22"], 3: ["#C08A60", "#996744", "#432819"],
    4: ["#A06E48", "#7C5233", "#36200F"], 5: ["#7E5236", "#5E3B25", "#2A170B"],
  };
  const INK = "#0F0E12", PAPER = "#F1E8D6", AMBER = "#F2A93B";
  CAST2.MOODS = ["neutral", "smile", "grin", "sad", "worried", "angry", "shock", "smirk", "think", "tired"];
  CAST2.ARMS = ["rest", "fold", "point", "chin", "phone", "open", "raise"];

  // ---------- head geometry (head height = 1, y down, origin = head centre) ----------
  const W = (y, sp) => { // half width of the cross-section at height y
    const jaw = sp.jaw ?? 0.27, cw = sp.headW ?? 0.4;
    if (y < 0.06) { const u = Math.min(1, (0.06 - y) / 0.62); return cw * Math.pow(Math.max(0, 1 - Math.pow(u, 2.7)), 1 / 2.7); }
    if (y < 0.38) return cw * (1 + 0.03 * Math.sin(Math.min(1, (y - 0.06) / 0.14) * Math.PI)) + (jaw - cw) * smooth((y - 0.12) / 0.26);
    if (y < 0.56) return jaw * Math.sqrt(Math.max(0, 1 - Math.pow((y - 0.38) / 0.19, 2)));
    return 0;
  };
  const D = (y, sp) => W(y, sp) * 1.18 + (y < 0 ? 0.02 : 0); // depth half
  const ZC = -0.06;                                            // cross-section centre is behind the face
  function smooth(t) { t = Math.max(0, Math.min(1, t)); return t * t * (3 - 2 * t); }
  // a point on the head surface at angle th (0 = straight ahead) and height y, rotated by yaw → screen
  function P(th, y, sp, yaw, out = 0) {
    const w = W(y, sp) + out, d = D(y, sp) + out;
    const x = w * Math.sin(th), z = d * Math.cos(th) + ZC;
    return { x: x * Math.cos(yaw) + z * Math.sin(yaw), y, z: -x * Math.sin(yaw) + z * Math.cos(yaw), vis: Math.cos(th + yaw) };
  }
  function outline(sp, yaw, out = 0) { // silhouette as a polygon (screen coords)
    const L = [], R = [];
    for (let i = 0; i <= 40; i++) {
      const y = -0.56 + (i / 40) * 1.12, w = W(y, sp) + (W(y, sp) > 0 ? out : 0), d = D(y, sp) + (W(y, sp) > 0 ? out : 0);
      const ext = Math.sqrt(Math.pow(w * Math.cos(yaw), 2) + Math.pow(d * Math.sin(yaw), 2)), c = ZC * Math.sin(yaw);
      // the chin and nose push the silhouette on the turned side
      let bump = 0; if (y > 0.4 && y < 0.56) bump = 0.035 * Math.abs(Math.sin(yaw)) * Math.sin(((y - 0.4) / 0.16) * Math.PI);
      L.push([c - ext - (yaw < 0 ? bump : 0), y]); R.push([c + ext + (yaw > 0 ? bump : 0), y]);
    }
    return L.concat(R.reverse());
  }
  function poly(ctx, pts, S, ox, oy) { ctx.beginPath(); pts.forEach((p, i) => (i ? ctx.lineTo : ctx.moveTo).call(ctx, ox + p[0] * S, oy + p[1] * S)); ctx.closePath(); }

  // ---------- drawing helpers ----------
  const PATS = {};
  function hatchPat(ctx, gap) { // a 45-degree ink line pattern (robust alternative to clip + hatch)
    const k = Math.round(gap); if (PATS[k]) return PATS[k];
    const c = (typeof document !== "undefined" ? document.createElement("canvas") : new OffscreenCanvas(k, k)); c.width = c.height = k;
    const g = c.getContext("2d"); g.strokeStyle = INK; g.lineWidth = Math.max(1, k * 0.32); g.beginPath(); g.moveTo(-1, k + 1); g.lineTo(k + 1, -1); g.moveTo(-1, 1); g.lineTo(1, -1); g.moveTo(k - 1, k + 1); g.lineTo(k + 1, k - 1); g.stroke();
    return (PATS[k] = ctx.createPattern(c, "repeat"));
  }
  function hatch(ctx, x0, y0, x1, y1, gap, ang, col, lw) { // parallel lines over a box (call inside a clip)
    ctx.save(); ctx.strokeStyle = col; ctx.lineWidth = lw; ctx.beginPath();
    const cx = (x0 + x1) / 2, cy = (y0 + y1) / 2, r = Math.hypot(x1 - x0, y1 - y0) / 2 + gap;
    const ca = Math.cos(ang), sa = Math.sin(ang);
    for (let k = -r; k <= r; k += gap) { ctx.moveTo(cx + ca * -r - sa * k, cy + sa * -r + ca * k); ctx.lineTo(cx + ca * r - sa * k, cy + sa * r + ca * k); }
    ctx.stroke(); ctx.restore();
  }
  function shade(ctx, st, S, pathFn, tone, box) { // fill a shadow region in the active style
    ctx.save(); pathFn(); ctx.clip();
    if (st.mode === "engrave") {
      hatch(ctx, box[0], box[1], box[2], box[3], Math.max(3, S * 0.022), -0.9, INK, Math.max(1, S * 0.006));
      if (tone > 1) hatch(ctx, box[0], box[1], box[2], box[3], Math.max(3, S * 0.026), 0.6, INK, Math.max(1, S * 0.005));
    } else { ctx.fillStyle = st.shadowCol; ctx.globalAlpha = tone > 1 ? 1 : 0.92; ctx.fillRect(box[0], box[1], box[2] - box[0], box[3] - box[1]); }
    ctx.restore();
  }

  // ---------- expression table ----------
  const EXP = {
    neutral: { bL: 0, bR: 0, bH: 0, eye: 1, mC: 0, mO: 0, mW: 1 },
    smile: { bL: 0.05, bR: 0.05, bH: -0.005, eye: 0.82, mC: 0.6, mO: 0, mW: 1.1 },
    grin: { bL: 0.08, bR: 0.08, bH: -0.01, eye: 0.7, mC: 0.9, mO: 0.45, mW: 1.2 },
    sad: { bL: -0.35, bR: -0.35, bH: -0.005, eye: 0.85, mC: -0.55, mO: 0, mW: 0.9 },
    worried: { bL: -0.45, bR: -0.45, bH: -0.02, eye: 1.05, mC: -0.25, mO: 0.12, mW: 0.85 },
    angry: { bL: 0.5, bR: 0.5, bH: 0.02, eye: 0.88, mC: -0.4, mO: 0.15, mW: 1.0 },
    shock: { bL: -0.15, bR: -0.15, bH: -0.05, eye: 1.25, mC: 0, mO: 0.9, mW: 0.7 },
    smirk: { bL: 0.1, bR: -0.25, bH: 0, eye: 0.78, mC: 0.35, mO: 0, mW: 1.0, asym: 0.5 },
    think: { bL: -0.1, bR: 0.3, bH: -0.01, eye: 0.85, mC: -0.1, mO: 0, mW: 0.85, look: [0.6, -0.5] },
    tired: { bL: -0.15, bR: -0.15, bH: 0.01, eye: 0.55, mC: -0.15, mO: 0, mW: 0.95 },
  };

  // ---------- the head ----------
  function head(ctx, sp, po, st, ox, oy, S) {
    const yaw = po.yaw || 0, e = Object.assign({}, EXP.neutral, EXP[po.mood || "neutral"] || {});
    const [skin, skinSh, line] = st.mode === "engrave" ? [PAPER, INK, INK] : (SKIN[sp.skin || 3]);
    const lw = Math.max(1.5, S * (st.mode === "engrave" ? 0.011 : 0.009));
    const ol = outline(sp, yaw);
    const path = () => poly(ctx, ol, S, ox, oy);
    const box = [ox - S * 0.7, oy - S * 0.7, ox + S * 0.7, oy + S * 0.7];

    // back hair (behind the head) is drawn first by CAST2.draw
    if (!po._backDone) hairBack(ctx, sp, po, st, ox, oy, S);
    // ears
    for (const side of [-1, 1]) {
      const pe = P(side * 1.52, 0.06, sp, yaw, -0.01);
      if (pe.vis > -0.45 && pe.vis < 0.55) {
        ctx.save(); ctx.fillStyle = skin; ctx.strokeStyle = line; ctx.lineWidth = lw;
        ctx.beginPath(); ctx.ellipse(ox + pe.x * S, oy + pe.y * S, S * 0.05 * (0.5 + 0.5 * Math.abs(Math.sin(side * 1.52 + yaw))), S * 0.1, 0, 0, Math.PI * 2);
        ctx.fill(); ctx.stroke(); ctx.restore();
      }
    }
    // neck is drawn by the bust; face fill
    ctx.save(); path(); ctx.fillStyle = skin; ctx.fill(); ctx.restore();
    // cel shadow: the side away from the light (light from screen-left by default)
    const ldir = po.light ?? -1; // -1 light from left, +1 from right
    const term = (y) => { const p = P(-ldir * (0.5 + 0.12 * Math.sin((y + 0.56) / 1.12 * Math.PI)), y, sp, yaw); return p.x; };
    ctx.save(); path(); ctx.clip();
    shade(ctx, { mode: st.mode, shadowCol: skinSh }, S, () => {
      ctx.beginPath();
      for (let i = 0; i <= 24; i++) { const y = -0.56 + i / 24 * 1.12; const x = term(y); (i ? ctx.lineTo : ctx.moveTo).call(ctx, ox + x * S, oy + y * S); }
      ctx.lineTo(ox - ldir * S, oy + 0.6 * S); ctx.lineTo(ox - ldir * S, oy - 0.6 * S); ctx.closePath();
    }, 1, box);
    // under-brow and under-chin shade
    shade(ctx, { mode: st.mode, shadowCol: skinSh }, S, () => { ctx.beginPath(); ctx.ellipse(ox + Math.sin(yaw) * 0.05 * S, oy + 0.62 * S, S * 0.3, S * 0.09, 0, 0, Math.PI * 2); }, 1, box);
    ctx.restore();
    // keep everything inside the head silhouette: erase outside with destination-in is not possible here, so we
    // draw the outline last and the head is filled before; shadow shapes were built to stay inside (terminator ∩ box)
    // facial hair (stubble / beard / moustache)
    facialHair(ctx, sp, po, st, ox, oy, S, line);
    // eyes
    const look = e.look || [po.lookX || 0, po.lookY || 0];
    for (const side of [-1, 1]) eye(ctx, sp, po, st, e, side, ox, oy, S, line, skin, look);
    // nose
    const tip = P(0, 0.2, sp, yaw, 0.09), base = P(0, 0.05, sp, yaw, 0.02);
    ctx.save(); ctx.strokeStyle = line; ctx.lineWidth = lw; ctx.lineCap = "round"; ctx.beginPath();
    const sideX = Math.sign(yaw || 0.001) * -1;
    ctx.moveTo(ox + base.x * S, oy + base.y * S);
    ctx.quadraticCurveTo(ox + (tip.x + sideX * 0.01) * S, oy + (tip.y - 0.02) * S, ox + tip.x * S, oy + tip.y * S);
    ctx.lineTo(ox + (tip.x + sideX * 0.05) * S, oy + (tip.y + 0.01) * S);
    ctx.stroke(); ctx.restore();
    // nostril shadow
    if (st.mode !== "engrave") { ctx.save(); ctx.fillStyle = skinSh; ctx.beginPath(); ctx.ellipse(ox + (tip.x + sideX * 0.03) * S, oy + (tip.y + 0.012) * S, S * 0.03, S * 0.012, 0, 0, 7); ctx.fill(); ctx.restore(); }
    // mouth
    mouth(ctx, sp, po, st, e, ox, oy, S, line);
    // brows
    for (const side of [-1, 1]) brow(ctx, sp, po, st, e, side, ox, oy, S, line);
    // marks: bindi, tilak, scar
    if (sp.tilak) { const t = P(0, -0.16, sp, yaw); if (t.vis > 0) { ctx.save(); ctx.strokeStyle = sp.tilak; ctx.lineWidth = S * 0.018; ctx.beginPath(); ctx.moveTo(ox + t.x * S, oy + (t.y - 0.07) * S); ctx.lineTo(ox + t.x * S, oy + (t.y + 0.04) * S); ctx.stroke(); ctx.restore(); } }
    if (sp.bindi) { const t = P(0, -0.09, sp, yaw); if (t.vis > 0) { ctx.save(); ctx.fillStyle = sp.bindi; ctx.beginPath(); ctx.arc(ox + t.x * S, oy + t.y * S, S * 0.016, 0, 7); ctx.fill(); ctx.restore(); } }
    // outline
    ctx.save(); path(); ctx.strokeStyle = line; ctx.lineWidth = lw * 1.1; ctx.stroke(); ctx.restore();
    // rim light on the lit edge (cel only)
    if (st.mode !== "engrave" && st.rim) { ctx.save(); path(); ctx.clip(); ctx.strokeStyle = st.rim; ctx.lineWidth = S * 0.02; ctx.globalAlpha = 0.85;
      ctx.beginPath(); const half = ol.length / 2; const seg = ldir < 0 ? ol.slice(4, half - 6) : ol.slice(half + 6, ol.length - 4);
      seg.forEach((p, i) => (i ? ctx.lineTo : ctx.moveTo).call(ctx, ox + (p[0] + (ldir < 0 ? 0.008 : -0.008)) * S, oy + p[1] * S)); ctx.stroke(); ctx.restore(); }
    hairFront(ctx, sp, po, st, ox, oy, S, line);
  }

  function eye(ctx, sp, po, st, e, side, ox, oy, S, line, skin, look) {
    const yaw = po.yaw || 0, th = side * 0.4, c = P(th, 0.0, sp, yaw);
    if (c.vis < 0.12) return;
    const fs = Math.min(1, c.vis * 1.15);                 // foreshortening
    const w = S * 0.085 * fs, open = (po.blink ? 0.08 : e.eye) * (sp.eyeOpen || 1);
    const h = S * 0.045 * open, cx = ox + c.x * S, cy = oy + c.y * S;
    ctx.save();
    // white (cel) / paper (engrave)
    ctx.beginPath(); ctx.moveTo(cx - w, cy); ctx.quadraticCurveTo(cx, cy - h * 1.6, cx + w, cy); ctx.quadraticCurveTo(cx, cy + h * 1.1, cx - w, cy); ctx.closePath();
    ctx.fillStyle = st.mode === "engrave" ? PAPER : "#F4EEE6"; ctx.fill();
    ctx.clip();
    const ix = cx + (look[0] * 0.45 + Math.sin(yaw) * 0.2) * w, iy = cy + look[1] * h * 0.5;
    ctx.fillStyle = st.mode === "engrave" ? INK : (sp.iris || "#2B1A12"); ctx.beginPath(); ctx.arc(ix, iy, S * 0.032, 0, 7); ctx.fill();
    if (st.mode !== "engrave") { ctx.fillStyle = INK; ctx.beginPath(); ctx.arc(ix, iy, S * 0.016, 0, 7); ctx.fill();
      ctx.fillStyle = "#FFF"; ctx.beginPath(); ctx.arc(ix - S * 0.01, iy - S * 0.012, S * 0.007, 0, 7); ctx.fill(); }
    ctx.restore();
    // upper lid line (thick), lower lid (thin)
    ctx.save(); ctx.strokeStyle = line; ctx.lineCap = "round";
    ctx.lineWidth = S * 0.016; ctx.beginPath(); ctx.moveTo(cx - w * 1.08, cy + h * 0.1); ctx.quadraticCurveTo(cx, cy - h * 1.65, cx + w * 1.1, cy - h * 0.05); ctx.stroke();
    ctx.lineWidth = S * 0.006; ctx.globalAlpha = 0.6; ctx.beginPath(); ctx.moveTo(cx - w * 0.8, cy + h * 0.55); ctx.quadraticCurveTo(cx, cy + h * 1.2, cx + w * 0.8, cy + h * 0.5); ctx.stroke();
    if (sp.age >= 45) { ctx.globalAlpha = 0.45; ctx.beginPath(); ctx.moveTo(cx - w * 0.6, cy + h * 1.6); ctx.quadraticCurveTo(cx, cy + h * 2.3, cx + w * 0.7, cy + h * 1.5); ctx.stroke(); }
    ctx.restore();
  }
  function brow(ctx, sp, po, st, e, side, ox, oy, S, line) {
    const yaw = po.yaw || 0, c = P(side * 0.4, -0.115 + (e.bH || 0), sp, yaw, 0.01);
    if (c.vis < 0.1) return;
    const fs = Math.min(1, c.vis * 1.15), w = S * 0.1 * fs;
    const tilt = (side < 0 ? e.bL : e.bR) || 0;      // + = inner end down (angry), - = inner end up (worried)
    const inner = side < 0 ? 1 : -1;                  // which end is the inner one (towards the nose)
    const x0 = ox + c.x * S - w, x1 = ox + c.x * S + w, yc = oy + c.y * S;
    const yInner = yc + tilt * S * 0.04, yOuter = yc - tilt * S * 0.015;
    ctx.save(); ctx.strokeStyle = sp.browCol || line; ctx.lineCap = "round"; ctx.lineWidth = S * (sp.browW || 0.024);
    ctx.beginPath();
    if (inner > 0) { ctx.moveTo(x0, yOuter); ctx.quadraticCurveTo((x0 + x1) / 2, yc - S * 0.02, x1, yInner); }
    else { ctx.moveTo(x0, yInner); ctx.quadraticCurveTo((x0 + x1) / 2, yc - S * 0.02, x1, yOuter); }
    ctx.stroke(); ctx.restore();
  }
  function mouth(ctx, sp, po, st, e, ox, oy, S, line) {
    const yaw = po.yaw || 0, c = P(0, 0.33, sp, yaw, 0.015);
    const talk = po.talk ? (0.15 + 0.35 * Math.abs(Math.sin(po.talk))) : 0;
    const open = Math.max(e.mO, talk), fs = Math.max(0.55, Math.cos(yaw));
    const w = S * 0.085 * e.mW * fs, cx = ox + c.x * S, cy = oy + c.y * S, curve = e.mC * S * 0.03, asym = (e.asym || 0) * S * 0.02;
    ctx.save(); ctx.strokeStyle = line; ctx.lineCap = "round"; ctx.lineWidth = S * 0.012;
    if (open > 0.08) {
      ctx.beginPath(); ctx.moveTo(cx - w, cy - curve * 0.3); ctx.quadraticCurveTo(cx, cy + S * 0.06 * open + curve, cx + w, cy - curve * 0.3 - asym);
      ctx.quadraticCurveTo(cx, cy - S * 0.012, cx - w, cy - curve * 0.3); ctx.closePath();
      ctx.fillStyle = st.mode === "engrave" ? INK : "#3A1414"; ctx.fill(); ctx.stroke();
      if (st.mode !== "engrave" && open > 0.3) { ctx.fillStyle = "#F4EEE6"; ctx.beginPath(); ctx.rect(cx - w * 0.6, cy - S * 0.006, w * 1.2, S * 0.014); ctx.fill(); }
    } else {
      ctx.beginPath(); ctx.moveTo(cx - w, cy - curve); ctx.quadraticCurveTo(cx, cy + curve, cx + w, cy - curve - asym); ctx.stroke();
    }
    // lower lip hint
    ctx.globalAlpha = 0.5; ctx.lineWidth = S * 0.007; ctx.beginPath(); ctx.moveTo(cx - w * 0.4, cy + S * 0.04 + open * S * 0.05); ctx.lineTo(cx + w * 0.4, cy + S * 0.04 + open * S * 0.05); ctx.stroke();
    ctx.restore();
  }
  function facialHair(ctx, sp, po, st, ox, oy, S, line) {
    const yaw = po.yaw || 0; if (!sp.beard && !sp.stubble && !sp.moustache) return;
    const col = st.mode === "engrave" ? INK : (sp.hairCol || "#1A1412");
    if (sp.beard) {
      ctx.save(); ctx.beginPath(); const pts = [];
      for (let i = 0; i <= 16; i++) { const p = P(-1.1 + i / 16 * 2.2, 0.24, sp, yaw); if (p.vis > -0.05) pts.push(p); }
      for (let i = 16; i >= 0; i--) { const p = P(-1.1 + i / 16 * 2.2, 0.62, sp, yaw, 0.03); if (p.vis > -0.05) pts.push(p); }
      pts.forEach((p, i) => (i ? ctx.lineTo : ctx.moveTo).call(ctx, ox + p.x * S, oy + p.y * S)); ctx.closePath();
      if (st.mode === "engrave") { ctx.clip(); hatch(ctx, ox - S, oy, ox + S, oy + S, S * 0.018, 1.3, INK, Math.max(1, S * 0.006)); } else { ctx.fillStyle = col; ctx.fill(); }
      ctx.restore();
    }
    if (sp.stubble) { // stipple along the jaw, seeded so it never flickers
      ctx.save(); ctx.fillStyle = col; ctx.globalAlpha = st.mode === "engrave" ? 0.9 : 0.35; let sd = 7;
      const rnd = () => ((sd = (sd * 16807) % 2147483647) / 2147483647);
      for (let i = 0; i < 260; i++) { const th = -1.2 + rnd() * 2.4, y = 0.24 + rnd() * 0.3; const p = P(th, y, sp, yaw, 0.002);
        if (p.vis < 0.05 || (Math.abs(th) < 0.32 && y < 0.38 && y > 0.29)) continue; ctx.fillRect(ox + p.x * S, oy + p.y * S, Math.max(1, S * 0.006), Math.max(1, S * 0.006)); }
      ctx.restore();
    }
    if (sp.moustache) {
      const c = P(0, 0.27, sp, yaw, 0.03), w = S * 0.11 * Math.max(0.5, Math.cos(yaw));
      ctx.save(); ctx.fillStyle = col; ctx.beginPath(); ctx.moveTo(ox + c.x * S - w, oy + c.y * S + S * 0.02);
      ctx.quadraticCurveTo(ox + c.x * S, oy + c.y * S - S * 0.035, ox + c.x * S + w, oy + c.y * S + S * 0.02);
      ctx.quadraticCurveTo(ox + c.x * S, oy + c.y * S + S * 0.005, ox + c.x * S - w, oy + c.y * S + S * 0.02); ctx.fill(); ctx.restore();
    }
  }

  // ---------- hair ----------
  function hairCol(sp, st) { return st.mode === "engrave" ? INK : (sp.hairCol || "#17110F"); }
  function capPath(ctx, sp, yaw, ox, oy, S, hairline, out) {
    // the hair cap: left silhouette from the hairline up over the crown and down the right side, then the hairline back
    const ol = outline(sp, yaw, out), n = ol.length / 2, L = ol.slice(0, n), R = ol.slice(n).reverse(); // both top→bottom
    const lim = hairline + 0.14;
    const pts = L.filter((p) => p[1] <= lim).reverse().concat(R.filter((p) => p[1] <= lim));
    ctx.beginPath(); pts.forEach((p, i) => (i ? ctx.lineTo : ctx.moveTo).call(ctx, ox + p[0] * S, oy + p[1] * S));
    for (let i = 12; i >= 0; i--) { const th = -1.25 + i / 12 * 2.5; const p = P(th, hairline + 0.07 * Math.pow(Math.abs(th), 2) * (sp.hairDip ?? 1), sp, yaw, out * 0.5); if (p.vis > -0.35) ctx.lineTo(ox + p.x * S, oy + p.y * S); }
    ctx.closePath();
  }
  function hairBack(ctx, sp, po, st, ox, oy, S) {
    const yaw = po.yaw || 0, h = sp.hair; if (!h) return;
    ctx.save(); ctx.fillStyle = hairCol(sp, st);
    if (h === "long" || h === "braid" || h === "bun_low") {
      const len = h === "long" ? 1.05 : 0.65, wd = 0.5 * (1 - 0.25 * Math.abs(Math.sin(yaw)));
      ctx.beginPath(); ctx.moveTo(ox + (-wd + Math.sin(yaw) * 0.1) * S, oy - 0.1 * S);
      ctx.quadraticCurveTo(ox + (-wd - 0.05) * S, oy + len * 0.6 * S, ox + (-wd + 0.08) * S, oy + len * S);
      ctx.lineTo(ox + (wd - 0.08) * S, oy + len * S); ctx.quadraticCurveTo(ox + (wd + 0.05) * S, oy + len * 0.6 * S, ox + (wd + Math.sin(yaw) * 0.1) * S, oy - 0.1 * S); ctx.closePath();
      if (st.mode === "engrave") { ctx.fillStyle = PAPER; ctx.fill(); ctx.fillStyle = hatchPat(ctx, Math.max(3, S * 0.02)); ctx.fill(); ctx.strokeStyle = INK; ctx.lineWidth = S * 0.01; ctx.stroke(); } else ctx.fill();
    }
    if (h === "shikha") { // the tuft at the crown-back; untied (sp.shikhaOpen) it falls behind the shoulders
      const c = P(Math.PI * 0.8, -0.5, sp, yaw, 0.0), back = Math.sin(yaw) >= 0 ? -1 : 1;
      ctx.beginPath(); ctx.moveTo(ox + (c.x - 0.04) * S, oy + (c.y - 0.04) * S);
      if (sp.shikhaOpen) { ctx.bezierCurveTo(ox + (c.x + back * 0.22) * S, oy + (c.y - 0.16) * S, ox + (c.x + back * 0.5) * S, oy + (c.y + 0.25) * S, ox + (c.x + back * 0.5) * S, oy + (c.y + 0.95) * S);
        ctx.quadraticCurveTo(ox + (c.x + back * 0.44) * S, oy + (c.y + 1.0) * S, ox + (c.x + back * 0.4) * S, oy + (c.y + 0.92) * S);
        ctx.bezierCurveTo(ox + (c.x + back * 0.38) * S, oy + (c.y + 0.3) * S, ox + (c.x + back * 0.16) * S, oy + (c.y + 0.0) * S, ox + (c.x + 0.04) * S, oy + (c.y + 0.06) * S); }
      else { ctx.bezierCurveTo(ox + (c.x + back * 0.14) * S, oy + (c.y - 0.16) * S, ox + (c.x + back * 0.24) * S, oy + (c.y - 0.02) * S, ox + (c.x + back * 0.12) * S, oy + (c.y + 0.1) * S); }
      ctx.closePath();
      if (st.mode === "engrave") { ctx.fillStyle = PAPER; ctx.fill(); ctx.fillStyle = hatchPat(ctx, Math.max(3, S * 0.016)); ctx.fill(); ctx.strokeStyle = INK; ctx.lineWidth = S * 0.008; ctx.stroke(); } else ctx.fill();
    }
    if (h === "bun" || h === "bun_low") { const b = P(Math.PI, h === "bun" ? -0.42 : -0.05, sp, yaw, 0.08); if (b.vis < 0.2) { ctx.beginPath(); ctx.arc(ox + b.x * S, oy + b.y * S, S * 0.13, 0, 7); ctx.fill(); } }
    ctx.restore();
  }
  function hairFront(ctx, sp, po, st, ox, oy, S, line) {
    const yaw = po.yaw || 0, h = sp.hair; if (!h) return;
    const col = hairCol(sp, st);
    ctx.save(); ctx.fillStyle = col; ctx.strokeStyle = st.mode === "engrave" ? INK : line; ctx.lineWidth = S * 0.008;
    const fill = () => { if (st.mode === "engrave") { ctx.fillStyle = PAPER; ctx.fill(); ctx.fillStyle = hatchPat(ctx, Math.max(3, S * 0.02)); ctx.fill(); ctx.stroke(); } else ctx.fill(); };
    if (h === "shaved" || h === "shikha") {
      // shaved scalp: a soft crown highlight only (cel); a few contour lines (engrave)
      const c = P(-0.3, -0.38, sp, yaw, -0.02);
      if (st.mode === "engrave") { ctx.strokeStyle = INK; ctx.lineWidth = Math.max(1, S * 0.004); for (let k = 0; k < 3; k++) { ctx.beginPath(); ctx.arc(ox + (c.x + 0.25) * S, oy + (c.y + 0.25) * S, S * (0.42 + k * 0.035), Math.PI * 1.05, Math.PI * 1.45); ctx.stroke(); } }
      else { ctx.fillStyle = "rgba(255,240,220,.16)"; ctx.beginPath(); ctx.ellipse(ox + c.x * S, oy + c.y * S, S * 0.12, S * 0.06, -0.5, 0, 7); ctx.fill(); }
    } else if (h === "short" || h === "side" || h === "receding" || h === "grey") {
      capPath(ctx, sp, yaw, ox, oy, S, h === "receding" ? -0.36 : -0.27, 0.04); fill();
      if (h === "side" && st.mode !== "engrave" && Math.abs(yaw) < 0.4) { const a = P(-0.2, -0.36, sp, yaw, 0.05); ctx.strokeStyle = "rgba(255,255,255,.12)"; ctx.lineWidth = S * 0.012; ctx.beginPath(); ctx.moveTo(ox + a.x * S, oy + a.y * S); ctx.quadraticCurveTo(ox + (a.x + 0.25) * S, oy + (a.y - 0.08) * S, ox + (a.x + 0.4) * S, oy + (a.y + 0.04) * S); ctx.stroke(); }
    } else if (h === "long" || h === "bun" || h === "bun_low" || h === "braid") {
      capPath(ctx, sp, yaw, ox, oy, S, -0.25, 0.035); fill();
      // centre parting
      const a = P(0, -0.52, sp, yaw, 0.04), b = P(0, -0.3, sp, yaw, 0.03);
      if (a.vis > 0) { ctx.strokeStyle = st.mode === "engrave" ? PAPER : "rgba(255,255,255,.14)"; ctx.lineWidth = S * 0.01; ctx.beginPath(); ctx.moveTo(ox + a.x * S, oy + a.y * S); ctx.lineTo(ox + b.x * S, oy + b.y * S); ctx.stroke(); }
      // side locks framing the face
      if (h === "long") for (const side of [-1, 1]) { const p = P(side * 1.0, -0.15, sp, yaw, 0.04); if (p.vis > -0.05 && p.vis < 0.72) { ctx.beginPath(); ctx.moveTo(ox + p.x * S, oy + p.y * S);
        ctx.quadraticCurveTo(ox + (p.x + side * 0.06) * S, oy + 0.25 * S, ox + (p.x + side * 0.02) * S, oy + 0.55 * S); ctx.lineTo(ox + (p.x + side * 0.12) * S, oy + 0.55 * S);
        ctx.quadraticCurveTo(ox + (p.x + side * 0.14) * S, oy + 0.1 * S, ox + (p.x + side * 0.06) * S, oy - 0.2 * S); ctx.closePath(); fill(); } }
    }
    if (sp.greyTemples && st.mode !== "engrave") for (const side of [-1, 1]) { const p = P(side * 1.15, -0.2, sp, yaw, 0.035); if (p.vis > 0.15) { ctx.fillStyle = "rgba(170,165,158,.75)"; ctx.beginPath(); ctx.ellipse(ox + p.x * S, oy + p.y * S, S * 0.03 * p.vis, S * 0.06, 0, 0, 7); ctx.fill(); } }
    if (sp.glasses) { for (const side of [-1, 1]) { const c = P(side * 0.4, 0.0, sp, yaw, 0.04); if (c.vis > 0.1) { ctx.strokeStyle = st.mode === "engrave" ? INK : sp.glasses; ctx.lineWidth = S * 0.012; ctx.beginPath(); ctx.ellipse(ox + c.x * S, oy + c.y * S, S * 0.1 * Math.min(1, c.vis * 1.1), S * 0.07, 0, 0, 7); ctx.stroke(); } }
      const l = P(-0.17, 0, sp, yaw, 0.05), r = P(0.17, 0, sp, yaw, 0.05); ctx.beginPath(); ctx.moveTo(ox + l.x * S, oy + l.y * S); ctx.lineTo(ox + r.x * S, oy + r.y * S); ctx.stroke(); }
    ctx.restore();
  }

  // ---------- bust and body ----------
  const OUT = { // outfit drawers: (ctx, sp, st, X, Y, S, yawB, colours)
  };
  function torso(ctx, sp, po, st, nx, ny, S) {
    const yawB = (po.yaw || 0) * 0.45, o = sp.outfit || {}, c1 = st.mode === "engrave" ? PAPER : (o.color || "#2C2933"), c2 = st.mode === "engrave" ? PAPER : (o.color2 || "#1B1920");
    const sw = S * (sp.shoulders || 0.95) * (1 - 0.18 * Math.abs(yawB)), shift = yawB * S * 0.12;
    const [skin, skinSh, line] = st.mode === "engrave" ? [PAPER, INK, INK] : SKIN[sp.skin || 3];
    const lw = Math.max(1.5, S * 0.01), full = po.body === "full", bottom = full ? ny + S * 2.3 : ny + S * 1.6;
    // neck
    ctx.save(); ctx.fillStyle = skin; ctx.strokeStyle = line; ctx.lineWidth = lw; ctx.beginPath();
    ctx.moveTo(nx - S * 0.13, ny - S * 0.1); ctx.lineTo(nx - S * 0.15, ny + S * 0.22); ctx.lineTo(nx + S * 0.15, ny + S * 0.22); ctx.lineTo(nx + S * 0.13, ny - S * 0.1); ctx.closePath(); ctx.fill();
    shade(ctx, { mode: st.mode, shadowCol: skinSh }, S, () => { ctx.beginPath(); ctx.rect(nx - S * 0.16, ny - S * 0.1, S * 0.32, S * 0.12); }, 2, [nx - S, ny - S * 0.2, nx + S, ny + S * 0.1]);
    ctx.restore();
    // body block
    const top = ny + S * 0.16;
    const body = () => { ctx.beginPath(); ctx.moveTo(nx + shift - S * 0.17, top - S * 0.02);
      ctx.bezierCurveTo(nx + shift - sw * 0.55, top + S * 0.05, nx + shift - sw * 0.92, top + S * 0.1, nx + shift - sw * 0.98, top + S * 0.32);
      ctx.bezierCurveTo(nx + shift - sw * 1.0, top + S * 0.5, nx + shift - sw * 0.9, top + S * 0.8, nx + shift - sw * 0.84, bottom);
      ctx.lineTo(nx + shift + sw * 0.84, bottom);
      ctx.bezierCurveTo(nx + shift + sw * 0.9, top + S * 0.8, nx + shift + sw * 1.0, top + S * 0.5, nx + shift + sw * 0.98, top + S * 0.32);
      ctx.bezierCurveTo(nx + shift + sw * 0.92, top + S * 0.1, nx + shift + sw * 0.55, top + S * 0.05, nx + shift + S * 0.17, top - S * 0.02); ctx.closePath(); };
    ctx.save(); body(); ctx.fillStyle = c1; ctx.fill(); ctx.save(); body(); ctx.clip();
    shade(ctx, { mode: st.mode, shadowCol: shadeCol(c1) }, S, () => { ctx.beginPath(); ctx.rect(nx + shift + (po.light ?? -1) * -1 * S * 0.15 * -1, top, (po.light ?? -1) < 0 ? sw * 1.2 : -sw * 1.2, bottom - top); }, 1, [nx - 2 * S, top, nx + 2 * S, bottom]); ctx.restore();
    // outfit details
    const style = o.style || "kurta";
    ctx.strokeStyle = st.mode === "engrave" ? INK : line; ctx.lineWidth = lw;
    if (style === "shirt" || style === "blazer") { // collar + placket
      ctx.fillStyle = st.mode === "engrave" ? PAPER : (o.collar || "#F1E8D6");
      ctx.beginPath(); ctx.moveTo(nx + shift - S * 0.17, top - S * 0.02); ctx.lineTo(nx + shift - S * 0.02, top + S * 0.2); ctx.lineTo(nx + shift - S * 0.24, top + S * 0.1); ctx.closePath(); ctx.fill(); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(nx + shift + S * 0.17, top - S * 0.02); ctx.lineTo(nx + shift + S * 0.02, top + S * 0.2); ctx.lineTo(nx + shift + S * 0.24, top + S * 0.1); ctx.closePath(); ctx.fill(); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(nx + shift, top + S * 0.2); ctx.lineTo(nx + shift, bottom); ctx.stroke();
      if (style === "blazer") { ctx.fillStyle = st.mode === "engrave" ? PAPER : (o.jacket || "#23212A");
        for (const sd of [-1, 1]) { ctx.beginPath(); ctx.moveTo(nx + shift + sd * S * 0.3, top); ctx.lineTo(nx + shift + sd * S * 0.06, top + S * 0.75); ctx.lineTo(nx + shift + sd * sw * 0.82, bottom); ctx.lineTo(nx + shift + sd * sw * 0.98, top + S * 0.5); ctx.bezierCurveTo(nx + shift + sd * sw, top + S * 0.18, nx + shift + sd * sw * 0.85, top, nx + shift + sd * S * 0.3, top); ctx.closePath(); ctx.fill(); ctx.stroke(); } }
    } else if (style === "kurta" || style === "angavastram") {
      ctx.beginPath(); ctx.moveTo(nx + shift - S * 0.12, top); ctx.quadraticCurveTo(nx + shift, top + S * 0.16, nx + shift + S * 0.12, top); ctx.stroke();
      if (style === "angavastram") { // a cloth over one shoulder + the sacred thread
        ctx.fillStyle = st.mode === "engrave" ? PAPER : (o.cloth || "#C9752F");
        ctx.beginPath(); ctx.moveTo(nx + shift - sw * 0.9, top + S * 0.08); ctx.lineTo(nx + shift - sw * 0.3, top - S * 0.01); ctx.lineTo(nx + shift + sw * 0.7, bottom); ctx.lineTo(nx + shift + sw * 0.2, bottom); ctx.closePath(); ctx.fill(); ctx.stroke();
        if (st.mode === "engrave") { ctx.save(); ctx.clip(); hatch(ctx, nx - 2 * S, top, nx + 2 * S, bottom, S * 0.03, 0.9, INK, Math.max(1, S * 0.005)); ctx.restore(); }
        if (sp.janeu) { ctx.strokeStyle = st.mode === "engrave" ? INK : "#EDE3CF"; ctx.lineWidth = S * 0.012; ctx.beginPath(); ctx.moveTo(nx + shift - sw * 0.55, top + S * 0.03); ctx.quadraticCurveTo(nx + shift + sw * 0.1, top + S * 0.7, nx + shift + sw * 0.75, top + S * 1.2); ctx.stroke(); }
      }
    } else if (style === "saree") {
      ctx.fillStyle = st.mode === "engrave" ? PAPER : (o.pallu || "#9E2348");
      ctx.beginPath(); ctx.moveTo(nx + shift + sw * 0.4, top); ctx.lineTo(nx + shift + sw * 0.98, top + S * 0.45); ctx.lineTo(nx + shift + sw * 0.8, bottom); ctx.lineTo(nx + shift - sw * 0.4, bottom); ctx.closePath(); ctx.fill(); ctx.stroke();
      if (o.border && st.mode !== "engrave") { ctx.strokeStyle = o.border; ctx.lineWidth = S * 0.04; ctx.beginPath(); ctx.moveTo(nx + shift + sw * 0.4, top); ctx.lineTo(nx + shift - sw * 0.4, bottom); ctx.stroke(); }
    } else if (style === "hoodie" || style === "tee") {
      ctx.beginPath(); ctx.moveTo(nx + shift - S * 0.16, top); ctx.quadraticCurveTo(nx + shift, top + S * 0.12, nx + shift + S * 0.16, top); ctx.stroke();
      if (style === "hoodie") { ctx.fillStyle = shadeCol(c1); ctx.beginPath(); ctx.ellipse(nx + shift, top + S * 0.02, S * 0.36, S * 0.08, 0, 0, 7); ctx.fill(); }
    }
    if (sp.lanyard && st.mode !== "engrave") { ctx.strokeStyle = sp.lanyard; ctx.lineWidth = S * 0.018; ctx.beginPath(); ctx.moveTo(nx + shift - S * 0.18, top); ctx.lineTo(nx + shift - S * 0.03, top + S * 0.55); ctx.lineTo(nx + shift + S * 0.12, top); ctx.stroke(); ctx.fillStyle = PAPER; ctx.fillRect(nx + shift - S * 0.1, top + S * 0.55, S * 0.15, S * 0.2); }
    ctx.restore();
    ctx.save(); body(); ctx.strokeStyle = st.mode === "engrave" ? INK : line; ctx.lineWidth = lw * 1.1; ctx.stroke(); ctx.restore();
    if (full) legs(ctx, sp, po, st, nx + shift, bottom, S, line);
    arms(ctx, sp, po, st, nx + shift, top, sw, S, line, skin, skinSh, c1);
  }
  function shadeCol(hex) { const n = parseInt(hex.slice(1), 16); const f = 0.68; return `rgb(${(n >> 16 & 255) * f | 0},${(n >> 8 & 255) * f | 0},${(n & 255) * f | 0})`; }
  function legs(ctx, sp, po, st, x, y, S, line) {
    const col = st.mode === "engrave" ? PAPER : ((sp.outfit || {}).pants || "#23212A");
    ctx.save(); ctx.fillStyle = col; ctx.strokeStyle = st.mode === "engrave" ? INK : line; ctx.lineWidth = S * 0.01;
    for (const sd of [-1, 1]) { ctx.beginPath(); ctx.moveTo(x + sd * S * 0.05, y - 2); ctx.lineTo(x + sd * S * 0.42, y - 2); ctx.lineTo(x + sd * S * 0.34, y + S * 2.2); ctx.lineTo(x + sd * S * 0.1, y + S * 2.2); ctx.closePath(); ctx.fill(); ctx.stroke();
      ctx.fillStyle = st.mode === "engrave" ? INK : "#0F0E12"; ctx.beginPath(); ctx.ellipse(x + sd * S * 0.25, y + S * 2.25, S * 0.2, S * 0.08, 0, 0, 7); ctx.fill(); ctx.fillStyle = col; }
    ctx.restore();
  }
  function arms(ctx, sp, po, st, x, top, sw, S, line, skin, skinSh, sleeve) {
    const pose = po.arms || "rest", L = S * 0.78;
    const seg = (sx, sy, a1, a2, sd, prop) => { // shoulder → elbow → hand, angles in radians from straight down
      const ex = sx + Math.sin(a1) * L * sd, ey = sy + Math.cos(a1) * L, hx = ex + Math.sin(a2) * L * 0.9 * sd, hy = ey + Math.cos(a2) * L * 0.9;
      ctx.save(); ctx.lineCap = "round"; ctx.lineJoin = "round";
      ctx.strokeStyle = st.mode === "engrave" ? INK : line; ctx.lineWidth = S * 0.24; ctx.beginPath(); ctx.moveTo(sx, sy); ctx.lineTo(ex, ey); ctx.lineTo(hx, hy); ctx.stroke();
      ctx.strokeStyle = sleeve; ctx.lineWidth = S * 0.21; ctx.beginPath(); ctx.moveTo(sx, sy); ctx.lineTo(ex, ey); ctx.lineTo(hx - (hx - ex) * 0.18, hy - (hy - ey) * 0.18); ctx.stroke();
      ctx.fillStyle = skin; ctx.strokeStyle = st.mode === "engrave" ? INK : line; ctx.lineWidth = S * 0.01; ctx.beginPath(); ctx.ellipse(hx, hy, S * 0.1, S * 0.12, a2 * sd, 0, 7); ctx.fill(); ctx.stroke();
      if (prop === "phone") { ctx.fillStyle = INK; ctx.strokeStyle = "#555"; ctx.beginPath(); ctx.roundRect(hx - S * 0.08, hy - S * 0.2, S * 0.16, S * 0.3, S * 0.03); ctx.fill(); ctx.stroke(); ctx.fillStyle = "#6FB7C9"; ctx.globalAlpha = 0.5; ctx.fillRect(hx - S * 0.065, hy - S * 0.18, S * 0.13, S * 0.24); }
      if (prop === "point") { ctx.strokeStyle = skin; ctx.lineWidth = S * 0.05; ctx.beginPath(); ctx.moveTo(hx, hy); ctx.lineTo(hx + Math.sin(a2) * S * 0.18 * sd, hy + Math.cos(a2) * S * 0.18); ctx.stroke(); }
      ctx.restore(); return [hx, hy];
    };
    const sy = top + S * 0.2, lx = x - sw * 0.86, rx = x + sw * 0.86;
    const P_ = { rest: [[0.12, 0.05], [0.12, 0.05]], fold: [[0.35, 2.2], [0.35, 2.2]], point: [[0.12, 0.05], [1.9, 1.75]], chin: [[0.12, 0.05], [0.4, 2.85]],
      phone: [[0.12, 0.05], [0.45, 2.6]], open: [[0.55, 1.2], [0.55, 1.2]], raise: [[0.12, 0.05], [2.7, 2.9]] }[pose] || [[0.12, 0.05], [0.12, 0.05]];
    seg(lx, sy, P_[0][0], P_[0][1], -1);
    seg(rx, sy, P_[1][0], P_[1][1], 1, pose === "phone" ? "phone" : pose === "point" ? "point" : null);
  }

  // ---------- public draw ----------
  CAST2.draw = (ctx, who, po = {}) => {
    const sp = typeof who === "string" ? REG[who] : who; if (!sp) throw new Error("CAST2: unknown character " + who);
    const S = po.s || 300, st = { mode: po.style || "cel", rim: po.rim === undefined ? AMBER : po.rim };
    const body = po.body || "bust";
    // head centre sits above the neck point
    const hx = po.x, hy = po.y - S * 0.62 + (po.tilt || 0) * S * 0.02;
    hairBack(ctx, sp, po, st, hx, hy, S); po = Object.assign({}, po, { _backDone: true });
    if (body !== "head") torso(ctx, sp, po, st, po.x, po.y, S);
    ctx.save(); if (po.tilt) { ctx.translate(hx, hy + S * 0.5); ctx.rotate(po.tilt * 0.12); ctx.translate(-hx, -(hy + S * 0.5)); }
    head(ctx, sp, po, st, hx, hy, S); ctx.restore();
  };
  root.CAST2 = CAST2;
})(typeof window !== "undefined" ? window : globalThis);
