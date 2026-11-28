// Otlo 3D layer v1 (28 Nov 2026): Three.js r186 scenes that render frame by frame from the Reel clock (no rAF).
// Use one canvas per effect inside a scene:
//   <canvas class="fx3d" data-fx="bokeh"></canvas>                          full-frame drifting brand-colour bokeh
//   <canvas class="fx3d inbox" data-fx="poster" data-img="#posterImg" width="620" height="820"></canvas>
//        a 3D poster card: swings in from the side, tilts, catches a moving light, then settles into a slow float.
//        data-img points at an <img> in the page (hidden is fine) so the texture is ready before the first frame.
//   <canvas class="fx3d" data-fx="confetti"></canvas>                       falling marigold/turmeric petals for payoffs
// Effects start at their scene's data-s; add data-at="<seconds>" to start later.
import * as THREE from './vendor/three.module.js';

const PAL = [0xE3A21A, 0xA8322A, 0xC2185B, 0x1B2A4A, 0xF7EFE0];
const rng = seed => () => (seed = (seed * 16807) % 2147483647) / 2147483647;
const sceneSpan = el => { const s = el.closest('.scene'); return s ? [+s.dataset.s, +s.dataset.e] : [0, 999]; };
const ease = x => { x = Math.max(0, Math.min(1, x)); return 1 - Math.pow(1 - x, 3); };
const fx = [];

function mkRenderer(cv){
  const full = !cv.hasAttribute('width');
  const w = full ? 1080 : cv.width, h = full ? 1920 : cv.height;
  const r = new THREE.WebGLRenderer({canvas: cv, antialias: true, alpha: true, preserveDrawingBuffer: true});
  r.setPixelRatio(1); r.setSize(w, h, false); r.outputColorSpace = THREE.SRGBColorSpace;
  return [r, w, h];
}

function bokeh(cv, petals){
  const [r, w, h] = mkRenderer(cv); const sc = new THREE.Scene();
  const cam = new THREE.OrthographicCamera(-w/2, w/2, h/2, -h/2, -10, 10);
  const R = rng(petals ? 7 : 42), N = petals ? 70 : 34, items = [];
  const disc = (() => { const c = document.createElement('canvas'); c.width = c.height = 128; const g = c.getContext('2d');
    const gr = g.createRadialGradient(64, 64, 0, 64, 64, 64); gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(.55, 'rgba(255,255,255,.55)'); gr.addColorStop(1, 'rgba(255,255,255,0)');
    g.fillStyle = gr; g.fillRect(0, 0, 128, 128); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; })();
  for (let i = 0; i < N; i++) {
    const size = petals ? 16 + R() * 20 : 40 + R() * 120;
    const geo = petals ? new THREE.CircleGeometry(size / 2, 5) : new THREE.PlaneGeometry(size, size);
    const mat = petals ? new THREE.MeshBasicMaterial({color: PAL[i % 3], transparent: true, opacity: 0.9})
                       : new THREE.MeshBasicMaterial({map: disc, color: PAL[i % 4], transparent: true, opacity: 0.06 + R() * 0.10, depthWrite: false});
    const m = new THREE.Mesh(geo, mat); sc.add(m);
    items.push({m, x: (R() - .5) * w, y: (R() - .5) * h, vx: (R() - .5) * 40, vy: petals ? -(160 + R() * 220) : (R() - .5) * 30, spin: (R() - .5) * 4, ph: R() * 6.28});
  }
  return t => { for (const it of items) {
      let y = it.y + it.vy * t; if (petals) { y = h/2 + 60 - ((h/2 + 60 - y) % (h + 120)); }
      it.m.position.set(it.x + it.vx * t + Math.sin(t * 0.9 + it.ph) * 18, y, 0); it.m.rotation.z = it.spin * t; }
    r.render(sc, cam); };
}

function poster(cv){
  const img = document.querySelector(cv.dataset.img); if (!img) { console.warn('otlo-3d: poster img missing'); return () => {}; }
  const [r, w, h] = mkRenderer(cv); const sc = new THREE.Scene();
  const cam = new THREE.PerspectiveCamera(32, w / h, 1, 100); cam.position.set(0, 0, 12);
  const tex = new THREE.Texture(img); tex.needsUpdate = true; tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 8;
  const aspect = (img.naturalWidth || 3) / (img.naturalHeight || 4);
  const vh = 2 * Math.tan(THREE.MathUtils.degToRad(16)) * 12, vw = vh * (w / h);
  let ph = vh * 0.9, pw = ph * aspect; if (pw > vw * 0.9) { pw = vw * 0.9; ph = pw / aspect; }
  const card = new THREE.Mesh(new THREE.BoxGeometry(pw, ph, 0.06), [
    new THREE.MeshStandardMaterial({color: 0xF7EFE0}), new THREE.MeshStandardMaterial({color: 0xF7EFE0}),
    new THREE.MeshStandardMaterial({color: 0xF7EFE0}), new THREE.MeshStandardMaterial({color: 0xF7EFE0}),
    new THREE.MeshStandardMaterial({map: tex, roughness: 0.38, metalness: 0.0}), new THREE.MeshStandardMaterial({color: 0x1B2A4A})]);
  sc.add(card);
  sc.add(new THREE.AmbientLight(0xffffff, 1.6));
  const key = new THREE.PointLight(0xfff1d6, 90, 40); sc.add(key);
  const [s0] = sceneSpan(cv); const at = +(cv.dataset.at ?? s0);
  return t => { const u = t - at; const p = ease(u / 0.9);
    card.rotation.y = (1 - p) * -1.25 + Math.sin(u * 0.9) * 0.07 * p;
    card.rotation.x = Math.sin(u * 0.7) * 0.04 * p - (1 - p) * 0.15;
    card.position.set((1 - p) * -3.5, Math.sin(u * 1.1) * 0.08 * p, (1 - p) * -4);
    key.position.set(-6 + Math.min(u, 4) * 3, 3, 6);   // the light sweeps across the card, a glossy glint
    r.render(sc, cam); };
}

document.querySelectorAll('canvas.fx3d').forEach(cv => {
  const k = cv.dataset.fx; let f = null;
  try { f = k === 'poster' ? poster(cv) : bokeh(cv, k === 'confetti'); } catch (e) { console.error('otlo-3d', k, e); }
  if (f) fx.push([cv, f]);
});
window.OTLO3D = t => { for (const [cv, f] of fx) { const [s, e] = sceneSpan(cv); if (t >= s - 0.05 && t < e + 0.05) f(t); } };
window.OTLO3D_READY = true;
if (window.render) window.render(0);
