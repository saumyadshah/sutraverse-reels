/* SutraVerse CAST v4: one rig per character, reused in every shot and every Reel.
 *
 * Why: a character redrawn per shot changes face, hair and proportions (Saumya, 30 Oct).
 * Rule: a character is DEFINED once (CAST.define or toolkit/cast/cast.json) and BUILT from that
 * definition; close-up / medium / wide are camera framings of the same rig (CAST.frame), never redraws.
 *
 *   CAST.load(json)                                   // registry from toolkit/cast/cast.json (build_composition injects it)
 *   const k = CAST.build("kabir", svgGroup);          // same face, hair, outfit everywhere
 *   CAST.frame(k, "CU" | "MCU" | "MS" | "WS", { x: 540, side: "center" | "left" | "right" });
 *   CAST.idle(tl, k, t0, dur);  CAST.blink(tl, k, t);  CAST.talk(tl, k, words);
 *   CAST.emote(tl, k, "worried", t);                  // neutral smile sad worried shock angry hopeful tired
 *   CAST.look(tl, k, -1 | 0 | 1, t);                  // eyes + a 3/4 head turn toward screen left/right
 *   CAST.phone(tl, k, "ear" | "hold" | "none", t);    // phone prop; "hold" lights the face with screen glow
 *
 * Mithila world (ancient scenes), same rule: CAST.build("gajendra", g) where the registry entry
 * says { rig: "m_elephant", ... }. Rigs: m_human, m_elephant, m_crocodile, m_cow, m_snake, m_bird,
 * and symbols m_sun, m_moon, m_lotus, m_chakra, m_tree, m_fish.
 *
 * Placement: gsap.set(rig.root, { x, y, scale, svgOrigin: "0 0" }) (never transformOrigin: it is bbox-relative).
 * Modern rig space: origin = base of the neck, head centre (0,-175), ~ 300 units of head,
 * torso to y = 700. Mithila rigs: origin = ground contact, facing RIGHT (flip: true faces left).
 */
(function () {
  const NS = "http://www.w3.org/2000/svg";
  const el = (tag, attrs, parent) => {
    const e = document.createElementNS(NS, tag);
    for (const k in attrs) if (attrs[k] !== undefined && attrs[k] !== null) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  };
  const g = (parent, attrs = {}) => el("g", attrs, parent);
  let uid = 0;
  const id = (p) => `cast${p}${++uid}`;

  // ---- brand palette (brand.css tokens) ----
  const C = {
    kajal: "#100E17", neel: "#1A1D47", neel2: "#2A2F6B", chandan: "#F4EADB", chandan2: "#D9CBB4",
    haldi: "#F2B33D", sindoor: "#D63E2A", mor: "#137C77", palash: "#EE7A2E", kumkum: "#9E2348",
  };
  // skin tones: [base, shadow, lip] -- Indian range, light to deep
  const SKIN = {
    1: ["#E3B48F", "#C08A66", "#A8545A"], 2: ["#D2A07A", "#AB7653", "#9A4A4E"],
    3: ["#BE875F", "#966143", "#8A3F44"], 4: ["#A26E4A", "#7C5034", "#73343A"], 5: ["#835536", "#5F3B24", "#5E2A2F"],
  };
  const HAIR = { black: ["#16121C", "#3A3350"], brown: ["#2E1E16", "#5A3C2A"], grey: ["#8E8A93", "#C9C4CC"], white: ["#D8D3CF", "#F4EFEA"] };

  const REG = {};
  const CAST = { C, REG };
  CAST.define = (name, spec) => { REG[name] = Object.assign({ name }, spec); return REG[name]; };
  CAST.load = (json) => { Object.entries(json.characters || json).forEach(([k, v]) => CAST.define(k, v)); };

  /* ======================= MODERN (Night Cinema) ======================= */
  function modern(parent, s) {
    const sk = SKIN[s.skin || 3], hr = HAIR[s.hair_color || (s.age === "elder" ? "grey" : "black")];
    const fem = s.gender === "f";
    const out = Object.assign({ style: "shirt", color: C.neel2, color2: C.chandan }, s.outfit || {});
    const root = g(parent, { class: "cast cast-" + (s.name || "modern") });
    const inner = g(root, {});
    const rig = { kind: "modern", spec: s, root, inner };
    const clip = id("face");

    // --- back hair (behind everything) ---
    const backHair = g(inner, {});
    if (["long", "braid", "bun_low"].includes(s.hair)) {
      const len = s.hair === "long" ? 300 : 120;
      el("path", { d: `M-122 -190 C-140 -320 140 -320 122 -190 C130 -60 ${110} ${len - 140} 90 ${len - 60} L-90 ${len - 60} C-110 ${len - 140} -130 -60 -122 -190 Z`, fill: hr[0] }, backHair);
    }

    // --- torso ---
    // legs / lower garment (seen in MS-WS; off frame in closer shots)
    const lower = g(inner, { class: "c-legs" });
    if (out.style === "saree") {
      el("path", { d: `M-190 760 L-250 1830 L250 1830 L190 760 Z`, fill: out.color2 }, lower);
      el("path", { d: `M-246 1790 L246 1790`, stroke: C.haldi, "stroke-width": 26 }, lower);
      [-60, 0, 60].forEach((x) => el("path", { d: `M${x} 1000 L${x * 1.3} 1780`, stroke: C.kajal, "stroke-opacity": 0.25, "stroke-width": 6 }, lower));
    } else {
      el("path", { d: `M-165 760 L-178 1815 L-28 1815 L-12 1040 L12 1040 L28 1815 L178 1815 L165 760 Z`, fill: s.bottom || "#24263F" }, lower);
      el("path", { d: `M0 1040 L0 1200`, stroke: C.kajal, "stroke-opacity": 0.4, "stroke-width": 5 }, lower);
      [-1, 1].forEach((sd) => el("path", { d: `M${sd * 30} 1815 L${sd * 30} 1790 L${sd * 180} 1790 C${sd * 215} 1795 ${sd * 222} 1840 ${sd * 190} 1845 L${sd * 30} 1845 Z`, fill: s.shoes || C.kajal }, lower));
    }
    const torso = g(inner, { class: "c-torso" });
    const shoulders = `M-236 820 L-250 250 C-250 140 -190 75 -70 40 L70 40 C190 75 250 140 250 250 L236 820 Z`;
    if (out.style === "kurta") el("path", { d: `M-200 760 L-215 1150 L215 1150 L200 760 Z`, fill: out.color }, torso);
    if (out.style === "saree") {
      el("path", { d: shoulders, fill: out.color }, torso); // blouse
      el("path", { d: `M-236 820 L-250 330 C-170 300 -40 170 70 40 L170 70 C120 220 40 500 -10 820 Z`, fill: out.color2 }, torso); // pallu
      el("path", { d: `M-250 330 C-170 300 -40 170 70 40`, stroke: C.haldi, "stroke-width": 14, fill: "none" }, torso);
      el("path", { d: `M-226 345 C-150 315 -30 190 76 62`, stroke: C.haldi, "stroke-width": 5, fill: "none" }, torso);
    } else {
      el("path", { d: shoulders, fill: out.color }, torso);
    }
    // neck + neckline
    el("path", { d: `M-46 -70 L-48 40 C-30 70 30 70 48 40 L46 -70 Z`, fill: sk[0] }, torso);
    el("path", { d: `M-46 -60 C-20 -30 30 -30 46 -60 L46 -10 C20 0 -20 0 -46 -10 Z`, fill: sk[1], opacity: 0.7 }, torso); // jaw shadow
    if (out.style === "hoodie") {
      el("path", { d: `M-150 70 C-120 -10 120 -10 150 70 C110 120 60 130 0 132 C-60 130 -110 120 -150 70 Z`, fill: out.color2 || C.neel }, torso);
      el("path", { d: `M-110 80 C-60 40 60 40 110 80 C60 100 -60 100 -110 80 Z`, fill: C.kajal, opacity: 0.55 }, torso);
      el("path", { d: `M-34 110 L-40 260 M34 110 L40 260`, stroke: C.chandan2, "stroke-width": 6, "stroke-linecap": "round" }, torso);
    } else if (out.style === "kurta") {
      el("path", { d: `M-52 34 C-30 52 30 52 52 34 L52 52 C30 70 -30 70 -52 52 Z`, fill: out.color2 }, torso);
      el("path", { d: `M0 60 L0 240`, stroke: out.color2, "stroke-width": 10 }, torso);
      [100, 150, 200].forEach((y) => el("circle", { cx: 0, cy: y, r: 6, fill: C.haldi }, torso));
    } else if (out.style === "blazer") {
      el("path", { d: `M-60 40 L0 200 L60 40 Z`, fill: out.color2 }, torso); // shirt V
      el("path", { d: `M-70 40 L-10 220 L-110 160 L-90 90 Z M70 40 L10 220 L110 160 L90 90 Z`, fill: C.kajal, opacity: 0.35 }, torso); // lapels
      el("path", { d: `M-8 70 L0 200 L8 70 Z`, fill: s.tie || C.kumkum }, torso);
    } else if (out.style === "tshirt") {
      el("path", { d: `M-56 38 C-30 72 30 72 56 38`, stroke: C.kajal, "stroke-opacity": 0.35, "stroke-width": 8, fill: "none" }, torso);
    } else if (out.style === "shirt") {
      el("path", { d: `M-62 36 L-8 130 L-40 150 L-86 60 Z M62 36 L8 130 L40 150 L86 60 Z`, fill: out.color2 }, torso); // collar
      [170, 240].forEach((y) => el("circle", { cx: 0, cy: y, r: 6, fill: out.color2 }, torso));
    } else if (out.style === "saree") {
      el("path", { d: `M-56 38 C-30 80 30 80 56 38`, stroke: C.haldi, "stroke-width": 8, fill: "none" }, torso);
    }
    if (s.lanyard) {
      el("path", { d: `M-70 50 L-30 300 M70 50 L30 300`, stroke: s.lanyard, "stroke-width": 8 }, torso);
      el("rect", { x: -48, y: 296, width: 96, height: 120, rx: 10, fill: C.chandan }, torso);
      el("rect", { x: -34, y: 314, width: 68, height: 40, rx: 4, fill: s.lanyard }, torso);
    }
    if (s.mangalsutra) el("path", { d: `M-50 40 Q0 150 50 40`, stroke: C.kajal, "stroke-width": 5, fill: "none", "stroke-dasharray": "3 7" }, torso);
    // torso shading (key light from front-left -> shadow on the right) + rim
    [-1, 1].forEach((sd) => el("path", { d: `M${sd * 172} 240 L${sd * 180} 812`, stroke: C.kajal, "stroke-opacity": 0.35, "stroke-width": 5 }, torso)); // arm edges
    if (out.style === "hoodie") el("path", { d: `M-236 800 L236 800`, stroke: C.kajal, "stroke-opacity": 0.3, "stroke-width": 26 }, torso);
    el("path", { d: `M90 50 C200 90 250 150 250 250 L236 820 L130 820 C150 500 150 250 90 50 Z`, fill: C.kajal, opacity: 0.32 }, torso);
    el("path", { d: `M70 40 C190 75 250 140 250 250 L236 820`, stroke: C.haldi, "stroke-width": 6, fill: "none", opacity: 0.85 }, torso);
    [-1, 1].forEach((sd) => el("path", { d: `M${sd * 236} 812 C${sd * 250} 850 ${sd * 238} 905 ${sd * 206} 905 C${sd * 182} 900 ${sd * 176} 850 ${sd * 182} 812 Z`, fill: sd > 0 ? sk[1] : sk[0] }, torso)); // hands

    // --- head (pivot at the neck) ---
    const head = g(inner, { class: "c-head" });
    rig.head = head; head.setAttribute("data-face", "1");
    const face = fem
      ? `M-100 -200 C-104 -285 -58 -310 0 -310 C58 -310 104 -285 100 -200 C98 -135 80 -80 44 -52 C24 -38 -24 -38 -44 -52 C-80 -80 -98 -135 -100 -200 Z`
      : `M-106 -200 C-108 -285 -60 -312 0 -312 C60 -312 108 -285 106 -200 C104 -128 88 -74 52 -46 C30 -32 -30 -32 -52 -46 C-88 -74 -104 -128 -106 -200 Z`;
    // ears
    [-1, 1].forEach((sd) => {
      el("ellipse", { cx: sd * 104, cy: -176, rx: 18, ry: 30, fill: sd > 0 ? sk[1] : sk[0] }, head);
      if (s.earrings) el(s.earrings === "jhumka" ? "path" : "circle",
        s.earrings === "jhumka" ? { d: `M${sd * 104 - 10} -138 L${sd * 104 + 10} -138 L${sd * 104 + 14} -112 L${sd * 104 - 14} -112 Z`, fill: C.haldi } : { cx: sd * 104, cy: -150, r: 7, fill: C.haldi }, head);
    });
    const fp = el("path", { d: face, fill: sk[0] }, head);
    const cp = el("clipPath", { id: clip }, head); el("path", { d: face }, cp);
    const shade = g(head, { "clip-path": `url(#${clip})` });
    el("ellipse", { cx: 120, cy: -170, rx: 95, ry: 170, fill: sk[1], opacity: 0.75 }, shade); // shadow side
    el("ellipse", { cx: -48, cy: -128, rx: 22, ry: 13, fill: sk[2], opacity: 0.18 }, shade); // cheeks
    el("ellipse", { cx: 52, cy: -128, rx: 22, ry: 13, fill: sk[2], opacity: 0.14 }, shade);
    const glow = el("rect", { x: -130, y: -330, width: 260, height: 300, fill: "#7FB7FF", opacity: 0 }, shade); // phone-screen glow
    rig.glow = glow;
    el("path", { d: face, fill: "none", stroke: C.haldi, "stroke-width": 5, "stroke-dasharray": "0 300 260 2000", opacity: 0.9 }, head); // rim, right contour
    if (s.age === "elder") {
      el("path", { d: `M-50 -262 Q0 -270 50 -262 M-40 -246 Q0 -252 40 -246`, stroke: sk[1], "stroke-width": 4, fill: "none" }, head);
      el("path", { d: `M-40 -125 Q-52 -100 -42 -80 M40 -125 Q52 -100 42 -80`, stroke: sk[1], "stroke-width": 4, fill: "none" }, head);
    }
    // nose
    el("path", { d: `M8 -186 C14 -160 22 -142 18 -128 C10 -122 -4 -122 -12 -128`, stroke: sk[1], "stroke-width": 6, fill: "none", "stroke-linecap": "round" }, head);
    // facial features group (shifts for 3/4 turns)
    const feat = g(head, { class: "c-feat" });
    rig.feat = feat;
    // eyes
    rig.eyes = []; rig.lids = []; rig.pupils = [];
    [-1, 1].forEach((sd) => {
      const ex = sd * 44, ey = -178;
      const E = g(feat, {});
      el("path", { d: `M${ex - 24} ${ey} Q${ex} ${ey - 20} ${ex + 24} ${ey} Q${ex} ${ey + 14} ${ex - 24} ${ey} Z`, fill: "#F6EEE6" }, E);
      const P = g(E, {});
      el("circle", { cx: ex, cy: ey - 2, r: 11, fill: "#2B1A12" }, P);
      el("circle", { cx: ex, cy: ey - 2, r: 5.5, fill: "#07060A" }, P);
      el("circle", { cx: ex - 4, cy: ey - 6, r: 3, fill: "#FFFFFF" }, P);
      const lid = el("path", { d: `M${ex - 27} ${ey + 2} Q${ex} ${ey - 24} ${ex + 27} ${ey + 2} L${ex + 27} ${ey - 26} L${ex - 27} ${ey - 26} Z`, fill: sd > 0 ? sk[1] : sk[0] }, E);
      gsap.set(lid, { scaleY: 0, svgOrigin: `${ex} ${ey - 26}` });
      el("path", { d: `M${ex - 26} ${ey + 1} Q${ex} ${ey - 21} ${ex + 26} ${ey + 1} ${sd < 0 ? `M${ex - 26} ${ey + 1} l-7 -6` : `M${ex + 26} ${ey + 1} l7 -6`}`, stroke: C.kajal, "stroke-width": 5, fill: "none", "stroke-linecap": "round" }, E);
      rig.eyes.push(E); rig.lids.push(lid); rig.pupils.push(P);
    });
    if (s.glasses) [-1, 1].forEach((sd) => el("rect", { x: sd * 44 - 34, y: -204, width: 68, height: 50, rx: 18, fill: "none", stroke: s.glasses === true ? C.kajal : s.glasses, "stroke-width": 6 }, feat));
    // brows
    rig.brows = [-1, 1].map((sd) => {
      const bx = sd * 44, by = -216;
      const b = el("path", { d: `M${bx - 26} ${by + 4} Q${bx} ${by - 8} ${bx + 26} ${by + 4}`, stroke: hr[0], "stroke-width": fem ? 7 : 10, fill: "none", "stroke-linecap": "round" }, feat);
      return { el: b, sd, ix: bx - sd * 26, iy: by + 4 };
    });
    if (s.bindi) el("circle", { cx: 0, cy: -232, r: 7, fill: s.bindi === true ? C.sindoor : s.bindi }, feat);
    if (s.tilak) el("path", { d: `M-6 -262 L0 -222 L6 -262 Z`, fill: s.tilak }, feat);
    // mouth set (opacity swaps; one visible at a time)
    const my = -96, M = g(feat, { class: "c-mouth" }); const lip = sk[2];
    rig.mouth = {
      neutral: el("path", { d: `M-26 ${my} Q0 ${my + 6} 26 ${my}`, stroke: lip, "stroke-width": 7, fill: "none", "stroke-linecap": "round" }, M),
      smile: el("path", { d: `M-34 ${my - 6} Q0 ${my + 22} 34 ${my - 6}`, stroke: lip, "stroke-width": 7, fill: "none", "stroke-linecap": "round", opacity: 0 }, M),
      sad: el("path", { d: `M-26 ${my + 6} Q0 ${my - 10} 26 ${my + 6}`, stroke: lip, "stroke-width": 7, fill: "none", "stroke-linecap": "round", opacity: 0 }, M),
      grim: el("path", { d: `M-28 ${my} L28 ${my}`, stroke: lip, "stroke-width": 7, fill: "none", "stroke-linecap": "round", opacity: 0 }, M),
      open: el("path", { d: `M-24 ${my - 4} Q0 ${my - 10} 24 ${my - 4} Q20 ${my + 22} 0 ${my + 24} Q-20 ${my + 22} -24 ${my - 4} Z`, fill: "#3A1418", opacity: 0 }, M),
      o: el("ellipse", { cx: 0, cy: my + 6, rx: 13, ry: 17, fill: "#3A1418", opacity: 0 }, M),
    };
    rig.mouthBase = "neutral";
    // facial hair
    if (s.stubble) el("path", { d: `M-92 -120 C-80 -60 -40 -36 0 -36 C40 -36 80 -60 92 -120 C70 -90 40 -76 0 -76 C-40 -76 -70 -90 -92 -120 Z`, fill: hr[0], opacity: 0.22 }, head);
    if (s.beard) el("path", { d: `M-100 -150 C-96 -60 -50 -20 0 -18 C50 -20 96 -60 100 -150 C80 -100 50 -84 0 -84 C-50 -84 -80 -100 -100 -150 Z`, fill: hr[0] }, head);
    if (s.mustache || s.beard) el("path", { d: `M-40 -108 Q0 -128 40 -108 Q20 -112 0 -106 Q-20 -112 -40 -108 Z`, fill: hr[0], "stroke": hr[0], "stroke-width": 8, "stroke-linejoin": "round" }, feat);
    // front hair
    const H = g(head, { class: "c-hair" });
    const hairPaths = {
      short: `M-112 -190 C-122 -300 -40 -350 20 -336 C90 -330 126 -280 112 -190 C100 -240 70 -262 30 -266 C-10 -250 -60 -262 -92 -236 C-100 -224 -106 -210 -112 -190 Z`,
      side: `M-112 -180 C-128 -300 -30 -352 40 -340 C110 -326 132 -262 112 -180 C104 -236 80 -270 10 -262 C-40 -258 -60 -232 -100 -230 C-106 -214 -110 -200 -112 -180 Z`,
      curly: `M-118 -180 C-150 -260 -100 -340 -20 -344 C60 -360 150 -300 118 -180 C108 -230 90 -246 60 -252 C40 -236 10 -250 -10 -244 C-40 -256 -70 -236 -96 -236 C-106 -222 -112 -204 -118 -180 Z`,
      long: `M-118 -150 C-130 -300 -30 -352 30 -340 C110 -330 136 -260 118 -150 C108 -230 70 -276 0 -276 C-20 -250 -70 -236 -100 -214 C-108 -194 -114 -172 -118 -150 Z`,
      bun: `M-110 -190 C-120 -300 -30 -340 20 -334 C96 -326 124 -270 110 -190 C100 -246 64 -276 0 -278 C-60 -276 -100 -246 -110 -190 Z`,
      bun_low: `M-110 -190 C-120 -300 -30 -340 20 -334 C96 -326 124 -270 110 -190 C100 -246 64 -276 0 -278 C-60 -276 -100 -246 -110 -190 Z`,
      braid: `M-110 -190 C-120 -300 -30 -340 20 -334 C96 -326 124 -270 110 -190 C100 -246 64 -276 0 -278 C-60 -276 -100 -246 -110 -190 Z`,
      bald: `M-108 -200 C-112 -230 -104 -250 -96 -256 C-90 -230 -96 -214 -108 -200 Z M108 -200 C112 -230 104 -250 96 -256 C90 -230 96 -214 108 -200 Z`,
    };
    el("path", { d: hairPaths[s.hair || "short"] || hairPaths.short, fill: hr[0] }, H);
    if (s.hair === "bun") el("ellipse", { cx: 0, cy: -350, rx: 52, ry: 40, fill: hr[0] }, H);
    if (s.hair !== "bald") el("path", { d: `M-60 -300 C-20 -326 40 -326 80 -296`, stroke: hr[1], "stroke-width": 7, fill: "none", opacity: 0.6, "stroke-linecap": "round" }, H);
    if (s.hair === "curly") [[-80, -300], [-30, -334], [30, -340], [84, -300]].forEach(([x, y]) => el("circle", { cx: x, cy: y, r: 22, fill: hr[0] }, H));
    if (s.hair === "long" || s.hair === "braid" || s.hair === "bun_low" || s.hair === "bun")
      el("path", { d: `M-4 -330 C-4 -300 -2 -290 0 -276`, stroke: hr[1], "stroke-width": 4, opacity: 0.6 }, H); // parting
    if (s.dupatta) el("path", { d: `M-250 260 C-200 120 -150 60 -70 40 L-40 80 C-120 120 -180 200 -200 330 Z`, fill: s.dupatta, opacity: 0.92 }, inner);

    // --- phone + hand (hidden until CAST.phone) ---
    const ph = el("g", { opacity: 0 }); inner.insertBefore(ph, head); rig.phoneEar = ph; // behind the head: the hand shows outside the face only
    el("rect", { x: 92, y: -250, width: 56, height: 110, rx: 12, fill: C.kajal, stroke: "#3A3550", "stroke-width": 4 }, ph);
    el("path", { d: `M250 260 C280 120 240 -20 170 -90 L110 -40 C160 30 190 140 170 280 Z`, fill: out.style === "saree" ? out.color : out.color }, ph); // forearm in sleeve
    el("path", { d: `M250 260 C280 120 240 -20 170 -90`, stroke: C.haldi, "stroke-width": 5, fill: "none", opacity: 0.8 }, ph);
    el("path", { d: `M96 -238 C120 -250 150 -236 160 -200 L176 -100 C170 -70 130 -50 104 -70 Z`, fill: sk[1] }, ph); // hand around the phone
    el("path", { d: `M112 -200 L150 -206 M110 -170 L152 -176 M108 -140 L150 -146`, stroke: sk[0], "stroke-width": 5, "stroke-linecap": "round" }, ph);
    const ph2 = g(inner, { opacity: 0 }); rig.phoneHold = ph2;
    el("path", { d: `M-80 520 C-60 430 60 430 80 520 L90 700 L-90 700 Z`, fill: sk[0] }, ph2);
    el("rect", { x: -70, y: 300, width: 140, height: 250, rx: 18, fill: C.kajal, stroke: "#3A3550", "stroke-width": 5 }, ph2);
    el("rect", { x: -60, y: 312, width: 120, height: 226, rx: 12, fill: "#22305E" }, ph2);
    el("path", { d: `M-90 520 C-80 470 -40 470 -30 500 L-40 560 Z M90 520 C80 470 40 470 30 500 L40 560 Z`, fill: sk[0] }, ph2);
    return rig;
  }

  /* ======================= MITHILA (ancient panels) ======================= */
  // Grammar: every form has the double outline (kajal line, then a gap, then a thin pigment line inside),
  // flat pigments, kachni hatching / dot bands, long "fish" eyes. Facing right by default.
  const hatch = (parent, x, y, w, h, color, step = 12, ang = 1) => {
    const G = g(parent, {});
    for (let i = 0; i < w + h; i += step) el("line", { x1: x + i, y1: y, x2: x + i - h * ang, y2: y + h, stroke: color, "stroke-width": 3 }, G);
    return G;
  };
  const fishEye = (parent, x, y, s = 1, line = C.kajal) => {
    el("path", { d: `M${x - 26 * s} ${y} Q${x} ${y - 16 * s} ${x + 30 * s} ${y + 2 * s} Q${x} ${y + 12 * s} ${x - 26 * s} ${y} Z`, fill: C.chandan, stroke: line, "stroke-width": 4 }, parent);
    el("circle", { cx: x + 4 * s, cy: y, r: 6 * s, fill: line }, parent);
  };
  const band = (parent, x1, y, x2, color, r = 5, gap = 16) => { for (let x = x1; x <= x2; x += gap) el("circle", { cx: x, cy: y, r, fill: color }, parent); };

  function mHuman(parent, s) {
    // Classic Mithila figure: profile head with a long fish eye, frontal torso, flared garment,
    // profile feet. Heads are large (about 1/5 of the height), every form outlined in kajal.
    const root = g(parent, { class: "cast cast-" + (s.name || "m_human") }); const inner = g(root, {});
    const skin = s.skin || "#E9B48A", robe = s.robe || C.mor, robe2 = s.robe2 || C.sindoor, line = C.kajal;
    const fem = s.gender === "f", sage = s.variant === "sage", gold = C.haldi;
    const ol = { stroke: line, "stroke-width": 7, "stroke-linejoin": "round" };
    // long hair behind (not for crowned men with short hair)
    const hair = sage ? C.chandan2 : line;
    el("path", { d: `M-40 -780 C-110 -760 -120 -640 -96 ${fem ? -470 : -580} C-70 ${fem ? -500 : -600} -50 -640 -20 -680 Z`, fill: hair, ...ol }, inner);
    // feet (profile, facing right)
    [-34, 30].forEach((x) => el("path", { d: `M${x - 26} -2 L${x - 22} -40 L${x + 18} -40 C${x + 40} -26 ${x + 56} -12 ${x + 54} -2 Z`, fill: skin, ...ol }, inner));
    // lower garment
    const LG = g(inner, {});
    if (fem) {
      el("path", { d: `M-170 -30 L-74 -390 L74 -390 L170 -30 Z`, fill: robe2, ...ol }, LG);
      [-300, -200, -100].forEach((y, i) => { const w = 74 + (y + 390) * 0.27; el("path", { d: `M${-w} ${y} L${w} ${y}`, stroke: line, "stroke-width": 5 }, LG); band(LG, -w + 14, y + 22, w - 14, i % 2 ? C.chandan : gold, 6, 24); });
      el("path", { d: `M-170 -30 L170 -30`, stroke: gold, "stroke-width": 14 }, LG);
    } else {
      el("path", { d: `M-96 -40 L-74 -390 L74 -390 L100 -40 Z`, fill: robe2, ...ol }, LG);
      el("path", { d: `M-14 -390 L-40 -40 L40 -40 L14 -390 Z`, fill: gold, ...ol }, LG); // front pleat
      for (let y = -350; y < -60; y += 34) el("path", { d: `M${-14 - (y + 390) * 0.075} ${y} L${14 + (y + 390) * 0.075} ${y}`, stroke: line, "stroke-width": 4 }, LG);
      band(LG, -84, -62, 84, C.chandan, 5, 20);
    }
    el("rect", { x: -82, y: -414, width: 164, height: 30, rx: 8, fill: gold, ...ol }, inner); // waistband
    band(inner, -66, -399, 66, C.sindoor, 5, 22);
    // torso
    const T = g(inner, { class: "c-torso" });
    el("path", { d: `M-74 -410 L-104 -640 C-60 -676 60 -676 104 -640 L74 -410 Z`, fill: sage ? C.palash : robe, ...ol }, T);
    if (!sage) { // uttariya sash, hatched
      const sash = g(T, {}); el("path", { d: `M-96 -650 L-60 -650 L80 -420 L44 -410 Z`, fill: C.palash, ...ol }, sash);
      for (let k = 0; k < 9; k++) { const t = k / 9; el("path", { d: `M${-90 + 140 * t} ${-640 + 220 * t} l30 0`, stroke: line, "stroke-width": 3 }, sash); }
    }
    if (s.necklace !== false) { el("path", { d: `M-56 -660 Q0 -580 56 -660`, stroke: gold, "stroke-width": 10, fill: "none" }, T); el("path", { d: `M-46 -656 Q0 -600 46 -656`, stroke: C.sindoor, "stroke-width": 6, fill: "none", "stroke-dasharray": "2 12", "stroke-linecap": "round" }, T); }
    if (sage) el("path", { d: `M-60 -662 Q0 -560 60 -662`, stroke: "#6B3A1E", "stroke-width": 12, fill: "none", "stroke-dasharray": "1 15", "stroke-linecap": "round" }, T); // rudraksha
    // arms with armlets and bracelets
    const arms = [];
    [-1, 1].forEach((sd) => {
      const A = g(inner, { class: sd < 0 ? "c-armB" : "c-armF" });
      const pose = s.pose || "rest";
      const d = pose === "namaskar" ? `M${sd * 98} -630 C${sd * 136} -540 ${sd * 70} -500 ${sd * 8} -540`
        : pose === "raise" && sd > 0 ? `M98 -630 C150 -690 168 -790 156 -880`
        : pose === "offer" && sd > 0 ? `M98 -630 C150 -580 190 -560 240 -560`
        : `M${sd * 98} -630 C${sd * 136} -540 ${sd * 136} -460 ${sd * 118} -400`;
      el("path", { d, stroke: line, "stroke-width": 40, fill: "none", "stroke-linecap": "round" }, A);
      el("path", { d, stroke: skin, "stroke-width": 27, fill: "none", "stroke-linecap": "round" }, A);
      const len = 1; const pth = el("path", { d, fill: "none", stroke: "none" }, A);
      try { const L2 = pth.getTotalLength(); [0.28, 0.9].forEach((f) => { const p = pth.getPointAtLength(L2 * f); el("circle", { cx: p.x, cy: p.y, r: 15, fill: gold, stroke: line, "stroke-width": 4 }, A); }); } catch (e) {}
      arms.push(A);
    });
    // head in profile, large, facing right
    const Hd = g(inner, { class: "c-head", "data-face": "1" });
    el("path", { d: `M-22 -660 L-20 -700 L26 -700 L28 -660 Z`, fill: skin, ...ol }, Hd);
    const head = `M-64 -790 C-72 -870 -12 -906 38 -894 C82 -884 92 -846 90 -820 L112 -794 L90 -782 C96 -756 86 -732 66 -718 C34 -694 -36 -700 -56 -732 C-72 -754 -70 -774 -64 -790 Z`;
    el("path", { d: head, fill: skin, ...ol }, Hd);
    el("ellipse", { cx: -18, cy: -790, rx: 14, ry: 20, fill: skin, ...ol }, Hd); // ear
    el("circle", { cx: -18, cy: -760, r: 10, fill: gold, stroke: line, "stroke-width": 4 }, Hd);
    if (sage) {
      el("path", { d: `M-70 -800 C-90 -910 50 -940 76 -856 C50 -878 0 -884 -36 -866 Z`, fill: C.chandan2, ...ol }, Hd);
      el("path", { d: `M-14 -900 C-30 -990 40 -1004 40 -910 Z`, fill: C.chandan2, ...ol }, Hd); // jata
      el("path", { d: `M28 -734 C56 -700 42 -610 -12 -590 C0 -640 -12 -690 0 -734 Z`, fill: C.chandan2, ...ol }, Hd); // beard
      el("path", { d: `M-30 -858 L60 -858`, stroke: C.sindoor, "stroke-width": 5 }, Hd); // tripundra hint
    } else if (s.crown) {
      el("path", { d: `M-66 -830 L-54 -940 L-18 -878 L8 -960 L34 -878 L66 -940 L80 -830 Z`, fill: gold, ...ol }, Hd);
      band(Hd, -48, -848, 64, C.sindoor, 6, 22);
      el("path", { d: `M-70 -800 C-76 -840 -40 -850 -60 -828 Z`, fill: line }, Hd);
    } else {
      el("path", { d: `M-70 -786 C-90 -886 14 -924 72 -858 C34 -870 -10 -864 -46 -824 Z`, fill: line }, Hd);
      if (fem) el("ellipse", { cx: -78, cy: -812, rx: 34, ry: 28, fill: line }, Hd); // bun
    }
    fishEye(Hd, 44, -812, 1.15);
    el("path", { d: `M24 -836 Q48 -850 76 -838`, stroke: line, "stroke-width": 5, fill: "none", "stroke-linecap": "round" }, Hd); // brow
    el("path", { d: `M62 -748 Q76 -742 84 -752`, stroke: C.sindoor, "stroke-width": 7, fill: "none", "stroke-linecap": "round" }, Hd); // lips
    if (fem) { el("circle", { cx: 70, cy: -856, r: 7, fill: C.sindoor }, Hd); el("circle", { cx: 100, cy: -780, r: 5, fill: gold, stroke: line, "stroke-width": 2 }, Hd); }
    else if (!sage) el("path", { d: `M50 -770 Q72 -764 92 -774`, stroke: line, "stroke-width": 6, fill: "none", "stroke-linecap": "round" }, Hd); // moustache
    if (s.tilak || sage) el("path", { d: `M78 -872 L82 -846`, stroke: C.sindoor, "stroke-width": 6, "stroke-linecap": "round" }, Hd);
    return { kind: "m_human", spec: s, root, inner, head: Hd, arms };
  }
  function mElephant(parent, s) {
    // Gajendra-ready: rigged trunk (3 segments), raisable front leg, ear flap, lotus in trunk optional
    const root = g(parent, { class: "cast cast-" + (s.name || "m_elephant") }); const inner = g(root, {});
    const body = s.body || C.chandan, cloth = s.cloth || C.sindoor, line = C.kajal, acc = s.accent || C.haldi;
    const legs = [];
    [[-230, 0], [-150, 1], [110, 0], [190, 1]].forEach(([x, front]) => {
      const L = g(inner, { class: "c-leg" });
      el("path", { d: `M${x - 34} -230 L${x - 34} 0 L${x + 34} 0 L${x + 34} -230 Z`, fill: front ? body : C.chandan2, stroke: line, "stroke-width": 7, "stroke-linejoin": "round" }, L);
      [-20, 0, 20].forEach((dx) => el("path", { d: `M${x + dx - 8} 0 Q${x + dx} -16 ${x + dx + 8} 0`, fill: "none", stroke: line, "stroke-width": 4 }, L));
      el("path", { d: `M${x - 34} -40 L${x + 34} -40`, stroke: acc, "stroke-width": 6 }, L);
      legs.push(L);
    });
    // body
    el("path", { d: `M-300 -220 C-320 -360 -230 -470 -60 -470 C120 -470 230 -430 270 -330 C290 -280 280 -230 250 -210 L-280 -200 Z`, fill: body, stroke: line, "stroke-width": 8, "stroke-linejoin": "round" }, inner);
    el("path", { d: `M-300 -260 C-320 -280 -340 -250 -330 -200`, stroke: line, "stroke-width": 7, fill: "none", "stroke-linecap": "round" }, inner); // tail
    // saddle cloth with kachni + dots
    const SC = g(inner, {});
    el("path", { d: `M-190 -450 L120 -456 L110 -250 C30 -230 -110 -230 -200 -250 Z`, fill: cloth, stroke: line, "stroke-width": 7, "stroke-linejoin": "round" }, SC);
    el("path", { d: `M-178 -436 L108 -442 L100 -264 C30 -246 -110 -246 -188 -264 Z`, fill: "none", stroke: acc, "stroke-width": 5 }, SC);
    [[-120, -380], [-40, -380], [40, -380], [-80, -310], [0, -310], [70, -320]].forEach(([x, y]) => el("circle", { cx: x, cy: y, r: 14, fill: acc, stroke: line, "stroke-width": 3 }, SC));
    band(SC, -190, -232, 100, acc, 5, 18);
    // head
    const Hd = g(inner, { class: "c-head", "data-face": "1" });
    el("path", { d: `M180 -470 C260 -520 360 -480 370 -380 C376 -320 350 -280 320 -260 L230 -250 C200 -300 180 -380 180 -470 Z`, fill: body, stroke: line, "stroke-width": 8, "stroke-linejoin": "round" }, Hd);
    const ear = g(Hd, { class: "c-ear" });
    el("path", { d: `M200 -450 C150 -470 120 -380 150 -300 C180 -260 230 -280 240 -320 C250 -380 240 -440 200 -450 Z`, fill: C.chandan2, stroke: line, "stroke-width": 7 }, ear);
    hatch(ear, 150, -430, 70, 120, C.kajal, 16).setAttribute("opacity", 0.45);
    fishEye(Hd, 320, -390, 1.0);
    el("path", { d: `M280 -462 C300 -500 340 -500 356 -470`, stroke: acc, "stroke-width": 10, fill: "none", "stroke-linecap": "round" }, Hd); // headpiece
    el("circle", { cx: 318, cy: -490, r: 12, fill: C.sindoor, stroke: line, "stroke-width": 3 }, Hd);
    if (s.tusk !== false) el("path", { d: `M330 -290 C360 -270 390 -270 410 -290`, stroke: C.chandan, "stroke-width": 14, fill: "none", "stroke-linecap": "round" }, Hd);
    // trunk: 3 nested segments for curling (rotate T1, T2, T3)
    const T1 = g(Hd, { class: "c-trunk1" }), T2 = g(T1, { class: "c-trunk2" }), T3 = g(T2, { class: "c-trunk3" });
    const seg = (G, x, y, len, w0, w1, tip) => {
      const d = tip
        ? `M${x - w0 / 2} ${y - 6} L${x - w1 / 2} ${y + len - 14} C${x - w1 / 2} ${y + len + 20} ${x + w1 / 2 + 24} ${y + len + 16} ${x + w1 / 2 + 18} ${y + len - 10} L${x + w0 / 2} ${y - 6} Z`
        : `M${x - w0 / 2} ${y - 6} L${x - w1 / 2} ${y + len + 6} L${x + w1 / 2} ${y + len + 6} L${x + w0 / 2} ${y - 6} Z`;
      el("path", { d, fill: body, stroke: line, "stroke-width": 7, "stroke-linejoin": "round" }, G);
      for (let i = 22; i < len - 8; i += 20) { const k = i / len, w = w0 + (w1 - w0) * k; el("path", { d: `M${x - w / 2 + 6} ${y + i} Q${x} ${y + i + 6} ${x + w / 2 - 6} ${y + i}`, stroke: line, "stroke-width": 3, fill: "none" }, G); }
    };
    const ring = (G, x, y, w) => { el("rect", { x: x - w / 2 - 4, y: y - 9, width: w + 8, height: 18, rx: 9, fill: acc, stroke: line, "stroke-width": 5 }, G); };
    seg(T1, 352, -330, 120, 74, 60); seg(T2, 352, -210, 104, 60, 46); seg(T3, 352, -106, 86, 46, 30, true);
    ring(T2, 352, -210, 60); ring(T3, 352, -106, 46);
    gsap.set(T1, { svgOrigin: "352 -330", rotation: 8 }); gsap.set(T2, { svgOrigin: "352 -210", rotation: 12 }); gsap.set(T3, { svgOrigin: "352 -106", rotation: 22 });
    const lotus = g(T3, { opacity: s.lotus ? 1 : 0 }); symLotus(lotus, 362, -2, 0.5);
    return { kind: "m_elephant", spec: s, root, inner, head: Hd, ear, trunk: [T1, T2, T3], legs, lotus };
  }

  function mCrocodile(parent, s) {
    // makara-style: long hatched body, rigged upper jaw (opens), tail sway
    const root = g(parent, { class: "cast cast-" + (s.name || "m_crocodile") }); const inner = g(root, {});
    const body = s.body || C.mor, belly = s.belly || C.haldi, line = C.kajal;
    const tail = g(inner, { class: "c-tail" });
    el("path", { d: `M-200 -60 C-300 -80 -380 -40 -460 -100 C-420 -20 -330 10 -200 0 Z`, fill: body, stroke: line, "stroke-width": 7, "stroke-linejoin": "round" }, tail);
    gsap.set(tail, { svgOrigin: "-200 -30" });
    el("path", { d: `M-220 0 C-220 -90 -100 -120 60 -110 C150 -104 200 -80 220 -50 L220 0 Z`, fill: body, stroke: line, "stroke-width": 8, "stroke-linejoin": "round" }, inner);
    el("path", { d: `M-210 -8 C-100 -30 100 -30 214 -10`, stroke: belly, "stroke-width": 16, fill: "none" }, inner);
    for (let x = -180; x < 200; x += 34) el("path", { d: `M${x} -96 l14 -26 l14 26`, fill: C.chandan, stroke: line, "stroke-width": 4, "stroke-linejoin": "round" }, inner); // ridge
    for (let x = -170; x < 200; x += 30) el("path", { d: `M${x} -70 Q${x + 15} -54 ${x + 30} -70`, fill: "none", stroke: line, "stroke-width": 3.5 }, inner); // scales
    [[-120, 0], [110, 0]].forEach(([x]) => el("path", { d: `M${x - 20} -10 L${x - 30} 30 L${x + 26} 30 L${x + 20} -10 Z`, fill: body, stroke: line, "stroke-width": 6 }, inner));
    // head with jaws
    const Hd = g(inner, { class: "c-head", "data-face": "1" });
    el("path", { d: `M200 -10 L420 -10 C440 -10 446 4 430 12 L210 20 Z`, fill: body, stroke: line, "stroke-width": 7, "stroke-linejoin": "round" }, Hd); // lower jaw
    for (let x = 230; x < 420; x += 24) el("path", { d: `M${x} -10 l8 -14 l8 14`, fill: C.chandan, stroke: line, "stroke-width": 3 }, Hd);
    const jaw = g(Hd, { class: "c-jaw" });
    el("path", { d: `M200 -100 C260 -110 300 -90 330 -70 L440 -40 C452 -30 446 -14 430 -14 L200 -14 Z`, fill: body, stroke: line, "stroke-width": 7, "stroke-linejoin": "round" }, jaw);
    for (let x = 236; x < 430; x += 24) el("path", { d: `M${x} -14 l8 14 l8 -14`, fill: C.chandan, stroke: line, "stroke-width": 3 }, jaw);
    fishEye(jaw, 286, -84, 0.75);
    gsap.set(jaw, { svgOrigin: "210 -14" });
    return { kind: "m_crocodile", spec: s, root, inner, head: Hd, jaw, tail };
  }

  function mCow(parent, s) {
    const root = g(parent, { class: "cast cast-" + (s.name || "m_cow") }); const inner = g(root, {});
    const body = s.body || C.chandan, line = C.kajal, acc = s.accent || C.sindoor;
    [[-160], [-100], [90], [150]].forEach(([x]) => el("path", { d: `M${x - 18} -170 L${x - 16} 0 L${x + 16} 0 L${x + 18} -170 Z`, fill: body, stroke: line, "stroke-width": 6 }, inner));
    el("path", { d: `M-210 -170 C-220 -300 -120 -320 0 -320 C120 -320 200 -300 210 -200 L200 -160 L-200 -150 Z`, fill: body, stroke: line, "stroke-width": 7, "stroke-linejoin": "round" }, inner);
    el("path", { d: `M-140 -300 L120 -300 L110 -190 L-130 -180 Z`, fill: acc, stroke: line, "stroke-width": 6 }, inner);
    band(inner, -120, -240, 100, C.haldi, 7, 26);
    const Hd = g(inner, { class: "c-head", "data-face": "1" });
    el("path", { d: `M180 -300 C230 -330 290 -300 300 -240 C306 -200 290 -170 260 -170 C220 -180 196 -230 180 -300 Z`, fill: body, stroke: line, "stroke-width": 7 }, Hd);
    el("path", { d: `M200 -310 C190 -350 210 -370 230 -360 M250 -310 C270 -350 290 -350 296 -330`, stroke: line, "stroke-width": 9, fill: "none", "stroke-linecap": "round" }, Hd);
    fishEye(Hd, 250, -262, 0.75);
    el("path", { d: `M210 -330 L196 -290 L226 -300 Z`, fill: C.chandan2, stroke: line, "stroke-width": 5 }, Hd);
    return { kind: "m_cow", spec: s, root, inner, head: Hd };
  }

  function mSnake(parent, s) {
    const root = g(parent, { class: "cast cast-" + (s.name || "m_snake") }); const inner = g(root, {});
    const body = s.body || C.mor, line = C.kajal, acc = s.accent || C.haldi, heads = s.heads || 1;
    el("path", { d: `M-300 0 C-200 -120 -80 80 40 -40 C120 -120 140 -260 80 -360`, stroke: line, "stroke-width": 64, fill: "none", "stroke-linecap": "round" }, inner);
    el("path", { d: `M-300 0 C-200 -120 -80 80 40 -40 C120 -120 140 -260 80 -360`, stroke: body, "stroke-width": 50, fill: "none", "stroke-linecap": "round" }, inner);
    el("path", { d: `M-300 0 C-200 -120 -80 80 40 -40 C120 -120 140 -260 80 -360`, stroke: acc, "stroke-width": 10, fill: "none", "stroke-dasharray": "4 22", "stroke-linecap": "round" }, inner);
    const Hd = g(inner, { class: "c-head", "data-face": "1" });
    const hood = heads > 1
      ? `M-40 -380 C-120 -460 -60 -560 80 -560 C220 -560 260 -460 180 -380 C140 -350 20 -350 -40 -380 Z`
      : `M30 -360 C-10 -420 20 -480 80 -480 C140 -480 170 -420 130 -360 Z`;
    el("path", { d: hood, fill: body, stroke: line, "stroke-width": 7 }, Hd);
    const n = heads, xs = n === 1 ? [80] : Array.from({ length: n }, (_, i) => -20 + i * (200 / (n - 1)));
    xs.forEach((x) => { const y = n === 1 ? -440 : -500 + Math.abs(x - 80) * 0.3; el("ellipse", { cx: x, cy: y, rx: 26, ry: 34, fill: body, stroke: line, "stroke-width": 6 }, Hd); el("circle", { cx: x - 8, cy: y - 6, r: 5, fill: line }, Hd); el("circle", { cx: x + 8, cy: y - 6, r: 5, fill: line }, Hd); });
    return { kind: "m_snake", spec: s, root, inner, head: Hd };
  }

  function mBird(parent, s) {
    const root = g(parent, { class: "cast cast-" + (s.name || "m_bird") }); const inner = g(root, {});
    const body = s.body || C.palash, line = C.kajal, acc = s.accent || C.mor;
    el("path", { d: `M-40 0 L-40 40 M20 0 L20 40`, stroke: line, "stroke-width": 10 }, inner);
    el("path", { d: `M-160 -60 C-140 -200 120 -220 160 -120 C170 -80 140 -20 60 0 L-100 0 C-140 -10 -160 -30 -160 -60 Z`, fill: body, stroke: line, "stroke-width": 7 }, inner);
    const wing = g(inner, { class: "c-wing" });
    el("path", { d: `M-80 -120 C-40 -260 120 -280 140 -180 C80 -160 0 -100 -80 -120 Z`, fill: acc, stroke: line, "stroke-width": 7 }, wing);
    hatch(wing, -60, -240, 180, 110, C.kajal, 18).setAttribute("opacity", 0.4);
    gsap.set(wing, { svgOrigin: "-60 -120" });
    el("path", { d: `M-160 -60 L-280 -120 L-260 -40 L-290 10 L-160 -20 Z`, fill: acc, stroke: line, "stroke-width": 6 }, inner);
    const Hd = g(inner, { class: "c-head", "data-face": "1" });
    el("circle", { cx: 150, cy: -170, r: 50, fill: body, stroke: line, "stroke-width": 7 }, Hd);
    el("path", { d: `M196 -180 L250 -160 L196 -150 Z`, fill: C.haldi, stroke: line, "stroke-width": 5 }, Hd);
    fishEye(Hd, 160, -176, 0.6);
    return { kind: "m_bird", spec: s, root, inner, head: Hd, wing };
  }

  // ---- symbols ----
  function symLotus(parent, x, y, s = 1) {
    const G = g(parent, { transform: `translate(${x} ${y}) scale(${s})` });
    [[-70, -20, -30], [70, -20, 30], [-36, -50, -14], [36, -50, 14], [0, -70, 0]].forEach(([px, py, r]) =>
      el("path", { d: `M0 0 C${-30} -40 ${-20} -110 0 -130 C20 -110 30 -40 0 0 Z`, fill: r === 0 ? C.sindoor : C.palash, stroke: C.kajal, "stroke-width": 6, transform: `translate(${px * 0.5} ${py * 0.2}) rotate(${r * 1.4})` }, G));
    el("path", { d: `M-90 6 C-40 30 40 30 90 6`, stroke: C.mor, "stroke-width": 14, fill: "none", "stroke-linecap": "round" }, G);
    return G;
  }
  function symSun(parent, s) { const G = g(parent, {}); const r = s.r || 90; for (let i = 0; i < 16; i++) { const a = (i / 16) * Math.PI * 2; el("path", { d: `M${Math.cos(a) * (r + 10)} ${Math.sin(a) * (r + 10)} L${Math.cos(a + 0.1) * (r + 46)} ${Math.sin(a + 0.1) * (r + 46)} L${Math.cos(a - 0.1) * (r + 46)} ${Math.sin(a - 0.1) * (r + 46)} Z`, fill: C.palash, stroke: C.kajal, "stroke-width": 4 }, G); } el("circle", { r, fill: C.haldi, stroke: C.kajal, "stroke-width": 7 }, G); el("circle", { r: r * 0.72, fill: "none", stroke: C.kajal, "stroke-width": 3, "stroke-dasharray": "3 9" }, G); return { kind: "m_sun", root: G }; }
  function symMoon(parent, s) { const G = g(parent, {}); const r = s.r || 70; el("path", { d: `M0 ${-r} A${r} ${r} 0 1 0 0 ${r} A${r * 0.7} ${r} 0 1 1 0 ${-r} Z`, fill: C.chandan, stroke: C.kajal, "stroke-width": 6 }, G); return { kind: "m_moon", root: G }; }
  function symChakra(parent, s) { const G = g(parent, {}); const r = s.r || 110; el("circle", { r, fill: C.haldi, stroke: C.kajal, "stroke-width": 8 }, G); el("circle", { r: r * 0.78, fill: "none", stroke: C.sindoor, "stroke-width": 6 }, G); for (let i = 0; i < 12; i++) { const a = (i / 12) * Math.PI * 2; el("line", { x1: Math.cos(a) * r * 0.2, y1: Math.sin(a) * r * 0.2, x2: Math.cos(a) * r * 0.78, y2: Math.sin(a) * r * 0.78, stroke: C.kajal, "stroke-width": 6 }, G); el("path", { d: `M${Math.cos(a) * r} ${Math.sin(a) * r} L${Math.cos(a + 0.13) * r * 1.22} ${Math.sin(a + 0.13) * r * 1.22} L${Math.cos(a + 0.26) * r} ${Math.sin(a + 0.26) * r} Z`, fill: C.haldi, stroke: C.kajal, "stroke-width": 4 }, G); } el("circle", { r: r * 0.2, fill: C.sindoor, stroke: C.kajal, "stroke-width": 5 }, G); return { kind: "m_chakra", root: G, spin: G }; }
  function symTree(parent, s) { const G = g(parent, {}); el("path", { d: `M-24 0 L-16 -260 L16 -260 L24 0 Z`, fill: C.palash, stroke: C.kajal, "stroke-width": 6 }, G); for (let i = 0; i < 7; i++) { const a = -Math.PI / 2 + (i - 3) * 0.42; const x = Math.cos(a) * 170, y = -300 + Math.sin(a) * 140; el("path", { d: `M0 -260 Q${x * 0.5} ${y + 40} ${x} ${y}`, stroke: C.kajal, "stroke-width": 7, fill: "none" }, G); el("ellipse", { cx: x, cy: y, rx: 46, ry: 26, fill: C.mor, stroke: C.kajal, "stroke-width": 5, transform: `rotate(${(a * 180) / Math.PI + 90} ${x} ${y})` }, G); } return { kind: "m_tree", root: G }; }
  function symFish(parent, s) { const G = g(parent, {}); const col = s.color || C.mor; el("path", { d: `M-110 0 C-60 -70 60 -70 100 0 C60 70 -60 70 -110 0 Z`, fill: col, stroke: C.kajal, "stroke-width": 6 }, G); el("path", { d: `M-110 0 L-160 -40 L-150 0 L-160 40 Z`, fill: col, stroke: C.kajal, "stroke-width": 6 }, G); hatch(G, -60, -30, 100, 60, C.kajal, 14).setAttribute("opacity", 0.4); fishEye(G, 60, -6, 0.6); return { kind: "m_fish", root: G }; }

  const RIGS = { modern, m_human: mHuman, m_elephant: mElephant, m_crocodile: mCrocodile, m_cow: mCow, m_snake: mSnake, m_bird: mBird,
    m_sun: symSun, m_moon: symMoon, m_chakra: symChakra, m_tree: symTree, m_fish: symFish,
    m_lotus: (p, s) => ({ kind: "m_lotus", root: symLotus(p, 0, 0, s.scale || 1) }) };
  CAST.rigs = Object.keys(RIGS);

  /** Build a registered character (or an inline spec object) into an SVG parent. */
  CAST.build = (nameOrSpec, parent, opts = {}) => {
    const spec = typeof nameOrSpec === "string" ? REG[nameOrSpec] : nameOrSpec;
    if (!spec) throw new Error(`CAST: "${nameOrSpec}" is not in the cast registry. Add it to toolkit/cast/cast.json (or CAST.define) first.`);
    const s = Object.assign({}, spec, opts);
    const fn = RIGS[s.rig || "modern"];
    if (!fn) throw new Error(`CAST: unknown rig "${s.rig}"`);
    const rig = fn(parent, s);
    rig.name = s.name; rig.spec = s;
    rig.root.setAttribute("data-cast", s.name || s.rig);
    if (s.flip && rig.inner) { const F = el("g", { transform: "scale(-1 1)", class: "c-flip" }); rig.root.insertBefore(F, rig.inner); F.appendChild(rig.inner); }
    if (opts.x !== undefined || opts.y !== undefined || opts.s !== undefined)
      gsap.set(rig.root, { x: opts.x || 0, y: opts.y || 0, scale: opts.s || 1, svgOrigin: "0 0" });
    return rig;
  };

  /* ---- camera framings for the modern rig: the SAME rig at every shot size ----
     Face centre lands on fixed screen lines so cuts between shots feel continuous, and the
     face never enters the subtitle zone (bottom 420 px + plate). */
  const FRAMES = { ECU: { s: 2.6, y: 1180 }, CU: { s: 1.9, y: 1150 }, MCU: { s: 1.35, y: 1000 }, MS: { s: 1.0, y: 850 }, WS: { s: 0.5, y: 570 } };
  CAST.FRAMES = FRAMES;
  CAST.frame = (rig, size = "MCU", { x, side = "center", tl, t, dur = 0 } = {}) => {
    const f = FRAMES[size]; if (!f) throw new Error("CAST.frame: size must be ECU|CU|MCU|MS|WS");
    const cx = x !== undefined ? x : side === "left" ? 340 : side === "right" ? 740 : 540;
    const props = { x: cx, y: f.y, scale: f.s, svgOrigin: "0 0" };
    rig.frameSize = size;
    if (tl) tl.to(rig.root, Object.assign({ duration: dur || 0.001, ease: "power2.inOut" }, props), t || 0);
    else gsap.set(rig.root, props);
    return props;
  };

  /* ---- acting ---- */
  const EXPR = {
    neutral: { brow: [0, 0], lid: 0, mouth: "neutral" },
    smile: { brow: [-4, 0], lid: 0.15, mouth: "smile" },
    hopeful: { brow: [-10, -10], lid: 0, mouth: "smile" },
    sad: { brow: [-6, 14], lid: 0.35, mouth: "sad" },
    worried: { brow: [-10, 18], lid: 0.1, mouth: "grim" },
    shock: { brow: [-18, -4], lid: -0.1, mouth: "o" },
    angry: { brow: [6, -18], lid: 0.25, mouth: "grim" },
    tired: { brow: [2, 6], lid: 0.55, mouth: "neutral" },
  };
  CAST.EXPRESSIONS = Object.keys(EXPR);
  const setMouth = (tl, rig, key, t) => { Object.entries(rig.mouth).forEach(([k, m]) => tl.set(m, { opacity: k === key ? 1 : 0 }, t)); };
  CAST.emote = (tl, rig, mood, t, dur = 0.3) => {
    if (rig.kind !== "modern") return;
    const e = EXPR[mood]; if (!e) throw new Error("CAST.emote: " + mood);
    rig.brows.forEach((b) => tl.to(b.el, { y: e.brow[0], rotation: b.sd * e.brow[1] * 0.6, svgOrigin: `${b.ix} ${b.iy}`, duration: dur }, t));
    rig.lids.forEach((l) => tl.to(l, { scaleY: Math.max(0, e.lid), duration: dur }, t));
    setMouth(tl, rig, e.mouth, t + dur * 0.5); rig.mouthBase = e.mouth; rig.lidBase = Math.max(0, e.lid);
  };
  CAST.blink = (tl, rig, t) => { if (!rig.lids) return; const base = rig.lidBase || 0; tl.to(rig.lids, { scaleY: 1, duration: 0.06 }, t).to(rig.lids, { scaleY: base, duration: 0.09 }, t + 0.1); };
  CAST.idle = (tl, rig, t0, dur, { seed = 7 } = {}) => {
    const breath = rig.kind === "modern" ? rig.inner : rig.inner;
    tl.fromTo(breath, { scaleY: 1 }, { scaleY: 1.012, svgOrigin: "0 700", duration: 1.6, yoyo: true, repeat: Math.max(0, Math.floor(dur / 1.6) - 1), ease: "sine.inOut" }, t0);
    if (rig.head && rig.kind === "modern") tl.fromTo(rig.head, { rotation: -0.6 }, { rotation: 0.6, svgOrigin: "0 -40", duration: 2.3, yoyo: true, repeat: Math.max(0, Math.floor(dur / 2.3) - 1), ease: "sine.inOut" }, t0);
    if (rig.trunk) tl.fromTo(rig.trunk[1], { rotation: -4 }, { rotation: 4, duration: 1.8, yoyo: true, repeat: Math.max(0, Math.floor(dur / 1.8) - 1), ease: "sine.inOut" }, t0);
    if (rig.ear) tl.fromTo(rig.ear, { scaleX: 1 }, { scaleX: 0.92, svgOrigin: "230 -360", duration: 0.9, yoyo: true, repeat: Math.max(0, Math.floor(dur / 0.9) - 1) }, t0);
    if (rig.tail) tl.fromTo(rig.tail, { rotation: -5 }, { rotation: 5, duration: 1.4, yoyo: true, repeat: Math.max(0, Math.floor(dur / 1.4) - 1), ease: "sine.inOut" }, t0);
    if (rig.lids) { let x = seed; for (let t = t0 + 0.8; t < t0 + dur - 0.3; t += 2.4 + ((x = (x * 9301 + 49297) % 233280) / 233280) * 1.8) CAST.blink(tl, rig, t); }
  };
  CAST.talk = (tl, rig, words) => {
    if (rig.kind !== "modern") return;
    (words || []).forEach((w) => { const d = Math.max(0.08, w.end - w.start); setMouth(tl, rig, "open", w.start); setMouth(tl, rig, rig.mouthBase || "neutral", w.start + d * 0.7); });
  };
  CAST.look = (tl, rig, dir, t, dur = 0.35) => {
    if (rig.kind !== "modern") return;
    tl.to(rig.pupils, { x: dir * 7, duration: dur * 0.6 }, t);
    tl.to(rig.feat, { x: dir * 12, duration: dur, ease: "power2.inOut" }, t);
    tl.to(rig.head, { rotation: dir * 2, svgOrigin: "0 -40", duration: dur }, t);
  };
  CAST.phone = (tl, rig, mode, t) => {
    if (rig.kind !== "modern") return;
    tl.to(rig.phoneEar, { opacity: mode === "ear" ? 1 : 0, duration: 0.25 }, t);
    tl.to(rig.phoneHold, { opacity: mode === "hold" ? 1 : 0, duration: 0.25 }, t);
    tl.to(rig.glow, { opacity: mode === "hold" ? 0.16 : 0, duration: 0.4 }, t);
  };
  // Mithila verbs
  CAST.trunk = (tl, rig, pose, t, dur = 0.8) => { // "down" | "raise" | "curl" (raise = offering the lotus)
    if (!rig.trunk) return; const P = { down: [8, 12, 22], raise: [-115, -35, -40], curl: [20, 40, 60] }[pose];
    rig.trunk.forEach((s, i) => tl.to(s, { rotation: P[i], duration: dur, ease: "power2.inOut" }, t));
  };
  CAST.jaw = (tl, rig, open, t, dur = 0.25) => { if (rig.jaw) tl.to(rig.jaw, { rotation: open ? -16 : 0, duration: dur }, t); };
  CAST.struggle = (tl, rig, t, dur) => tl.fromTo(rig.inner, { x: -6, rotation: -0.8 }, { x: 6, rotation: 0.8, svgOrigin: "0 0", duration: 0.18, yoyo: true, repeat: Math.max(1, Math.floor(dur / 0.18)), ease: "sine.inOut" }, t);

  window.CAST = CAST;
})();
