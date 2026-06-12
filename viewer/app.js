import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { RGBELoader } from 'three/addons/loaders/RGBELoader.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { BUILDERS } from './builders.js';

const DEG = Math.PI / 180;
const DEFAULT_COLOR = '#7e8a98';

// ---------- scene ----------
const host = document.getElementById('scene');
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.setSize(innerWidth, innerHeight);
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.05;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
host.appendChild(renderer.domElement);

// soft vertical gradient background
function gradientTexture(top, bottom) {
  const c = document.createElement('canvas'); c.width = 2; c.height = 256;
  const g = c.getContext('2d'); const grd = g.createLinearGradient(0, 0, 0, 256);
  grd.addColorStop(0, top); grd.addColorStop(1, bottom); g.fillStyle = grd; g.fillRect(0, 0, 2, 256);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
}

const scene = new THREE.Scene();
scene.background = gradientTexture('#e9eef3', '#c2ccd6');

// image-based lighting for realistic metals — real studio HDRI (CC0, Poly Haven),
// RoomEnvironment as the synchronous fallback until/unless it loads
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
new RGBELoader().load('./assets/studio_small_08_1k.hdr', tex => {
  tex.mapping = THREE.EquirectangularReflectionMapping;
  scene.environment = pmrem.fromEquirectangular(tex).texture;
  tex.dispose();
}, undefined, () => console.warn('HDRI load failed — keeping RoomEnvironment'));

const camera = new THREE.PerspectiveCamera(42, innerWidth / innerHeight, 1, 4000);
camera.position.set(175, 120, 230);

const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 36, 0);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.maxDistance = 900;
controls.minDistance = 12;
// free movement: right-drag / two-finger pans, arrow keys walk the truck,
// double-click recenters the orbit on whatever you hit
controls.screenSpacePanning = true;
controls.keyPanSpeed = 22;
controls.keys = { LEFT: 'ArrowLeft', UP: 'ArrowUp', RIGHT: 'ArrowRight', BOTTOM: 'ArrowDown' };
controls.listenToKeyEvents(window);

// lighting — studio key + fill
scene.add(new THREE.HemisphereLight('#ffffff', '#aeb9c6', 0.6));
const key = new THREE.DirectionalLight('#ffffff', 2.0); key.position.set(140, 220, 160); scene.add(key);
key.castShadow = true;
key.shadow.mapSize.set(2048, 2048);
key.shadow.camera.left = -170; key.shadow.camera.right = 170;
key.shadow.camera.top = 170; key.shadow.camera.bottom = -170;
key.shadow.camera.near = 40; key.shadow.camera.far = 700;
key.shadow.bias = -0.0006; key.shadow.normalBias = 0.5;
const fill = new THREE.DirectionalLight('#dce8ff', 0.7); fill.position.set(-160, 90, -120); scene.add(fill);
const front = new THREE.DirectionalLight('#fff6e8', 0.55); front.position.set(240, 70, 30); scene.add(front);

// ground shadow catcher — contact shadow grounds the truck without hiding the grid
const ground = new THREE.Mesh(
  new THREE.CircleGeometry(280, 64),
  new THREE.ShadowMaterial({ color: '#1d2935', opacity: 0.32 })
);
ground.rotation.x = -90 * DEG;
ground.receiveShadow = true;
scene.add(ground);

// subtle ground grid
const grid = new THREE.GridHelper(420, 42, '#9aa7b5', '#cdd5de');
grid.material.opacity = 0.5; grid.material.transparent = true;
grid.position.y = 0;
scene.add(grid);

// ---------- data ----------
let SYSTEMS = {};            // id -> {name,color,...}
const meshes = [];           // all part meshes
let selected = null;
const activeSet = new Set(); // selected systems (empty = whole truck)
let bodyHidden = false;      // body-panels toggle (see the engine without the shell)
const BODY_SYSTEMS = new Set(['body-cab', 'body-bed', 'exterior-trim', 'glass', 'interior']);
let camPosGoal = null, camTgtGoal = null;   // camera tween targets

const colorOf = (part) =>
  part.model.color || (SYSTEMS[part.systems[0]] && SYSTEMS[part.systems[0]].color) || DEFAULT_COLOR;

function buildGeometry(m) {
  if (m.kind === 'box') return new THREE.BoxGeometry(m.size[0], m.size[1], m.size[2]);
  if (m.kind === 'sphere') return new THREE.SphereGeometry(m.radius, 28, 18);
  if (m.kind === 'cylinder') {
    const g = new THREE.CylinderGeometry(m.radius, m.radius, m.length, 36);
    if (m.axis === 'x') g.rotateZ(90 * DEG);
    else if (m.axis === 'z') g.rotateX(90 * DEG);
    return g; // axis 'y' is native
  }
  return new THREE.BoxGeometry(4, 4, 4);
}

// Build a massing primitive (box/cyl/sphere) with a system-colored material + edges.
function buildPrimitive(prim, part) {
  const g = buildGeometry(prim);
  const isGlass = part.systems && part.systems.includes('glass');
  const baseOpacity = prim.opacity != null ? prim.opacity : (isGlass ? 0.32 : 1);
  const mat = isGlass
    ? new THREE.MeshPhysicalMaterial({          // automotive glass: smooth, faint green
        color: new THREE.Color(prim.color || '#a8c4bc'),
        metalness: 0, roughness: 0.05, clearcoat: 1, clearcoatRoughness: 0.04,
        transparent: true, opacity: baseOpacity,
        emissive: new THREE.Color('#000000'), emissiveIntensity: 0,
      })
    : new THREE.MeshStandardMaterial({
        color: new THREE.Color(prim.color || colorOf(part)),
        metalness: 0.25, roughness: 0.62,
        transparent: baseOpacity < 1, opacity: baseOpacity,
        emissive: new THREE.Color('#000000'), emissiveIntensity: 0,
      });
  const mesh = new THREE.Mesh(g, mat);
  if (prim.position) mesh.position.set(prim.position[0], prim.position[1], prim.position[2]);
  if (prim.rotation) mesh.rotation.set(prim.rotation[0] * DEG, prim.rotation[1] * DEG, prim.rotation[2] * DEG);
  mesh.add(new THREE.LineSegments(
    new THREE.EdgesGeometry(g, 25),
    new THREE.LineBasicMaterial({ color: '#3d4855', transparent: true, opacity: baseOpacity < 0.5 ? 0.7 : 0.45 })
  ));
  return mesh;
}

// Load a real mesh (.glb from AI-gen or sourced CAD) into a part's group, async.
const gltfLoader = new GLTFLoader();
let pendingGltf = 0;   // geometry dump waits for these so AABBs are real
function loadGltf(src, top, part, scale) {
  pendingGltf++;
  gltfLoader.load(src, (gltf) => {
    pendingGltf--;
    if (scale && scale !== 1) gltf.scene.scale.setScalar(scale);
    gltf.scene.traverse(o => {
      o.userData.part = part;
      if (o.isMesh) { o.userData.cast = true; o.castShadow = true; o.receiveShadow = true; }
      if (o.isMesh && o.material) {
        o.material.transparent = o.material.opacity < 1;
        (top.userData.tint = top.userData.tint || []).push({ mat: o.material, base: o.material.opacity != null ? o.material.opacity : 1, edge: false });
      }
    });
    top.add(gltf.scene);
    applyAppearance(top);
  }, undefined, err => {
    pendingGltf--;
    console.warn('glTF load failed:', src, err);
    top.add(buildPrimitive({ kind: 'box', size: [6, 6, 6] }, part));   // fallback so the part still shows
  });
}

const catalogOnly = [];   // parts catalogued but not yet rendered (internal/hidden)

function addPart(part) {
  const m = part.model || {};
  if (m.placement === 'internal' || m.render === false) { catalogOnly.push(part); return; }

  let top;
  try {
    if (m.kind === 'gltf' && m.src) {
      top = new THREE.Group();                  // real mesh (AI-generated / sourced .glb), loaded async
      loadGltf(m.src, top, part, m.glbScale);   // glbScale: cadpy GLBs are meters (inches/1000) → 1000
    } else if (m.builder && BUILDERS[m.builder]) {
      top = BUILDERS[m.builder](m, part);       // refined geometry
    } else if (m.kind === 'group') {
      top = new THREE.Group();
      (m.parts || []).forEach(prim => top.add(buildPrimitive(prim, part)));
    } else {
      top = new THREE.Group();
      // position/rotation are applied to the group below — strip them so the
      // primitive isn't offset twice (this was doubling every massing part's distance).
      top.add(buildPrimitive({ ...m, position: undefined, rotation: undefined }, part));
    }
  } catch (err) {
    console.warn('build failed for', part.id, err);
    top = new THREE.Group();
    top.add(buildPrimitive({ kind: 'box', size: [6, 6, 6] }, part)); // fallback massing
  }

  const p = m.position || [0, 0, 0];
  top.position.set(p[0], p[1], p[2]);
  if (m.rotation) top.rotation.set(m.rotation[0] * DEG, m.rotation[1] * DEG, m.rotation[2] * DEG);
  if (m.scale) top.scale.setScalar(m.scale);

  // collect every tintable material under this part for selection/dim
  const tint = [];
  top.traverse(o => {
    o.userData.part = part;
    if (o.isMesh) {
      tint.push({ mat: o.material, base: o.material.opacity != null ? o.material.opacity : 1, edge: false });
      // opaque meshes cast shadows; ghosty massing boxes don't
      o.userData.cast = !o.material.transparent || o.material.opacity >= 0.6;
      o.castShadow = o.userData.cast;
      o.receiveShadow = true;
    } else if (o.isLine) tint.push({ mat: o.material, base: o.material.opacity != null ? o.material.opacity : 1, edge: true });
  });
  top.userData.part = part;
  top.userData.top = true;
  top.userData.dim = false;
  top.userData.context = !!m.context;   // body shells kept as context during isolation
  top.userData.baseOpacity = m.opacity != null ? m.opacity : 1;
  top.userData.tint = tint;
  top.userData.basePos = top.position.clone();   // for explode/teardown
  top.userData.isRouted = m.builder === 'cable' || m.builder === 'pipe';
  scene.add(top);
  meshes.push(top);
}

// ---------- explode / teardown ----------
let explodeF = 0;
function computeExplode() {
  // group by assembly; each part's explode vector = explicit, or radial from the assembly center
  const groups = {};
  meshes.forEach(m => { const a = m.userData.part.assembly || 'misc'; (groups[a] = groups[a] || []).push(m); });
  for (const a in groups) {
    const arr = groups[a];
    const c = new THREE.Vector3();
    arr.forEach(m => c.add(m.userData.basePos)); c.divideScalar(arr.length);
    arr.forEach(m => {
      const ex = m.userData.part.model.explode;
      if (ex) { m.userData.explode = new THREE.Vector3(ex[0], ex[1], ex[2]); return; }
      if (m.userData.isRouted || m.userData.context) { m.userData.explode = new THREE.Vector3(); return; }
      const dir = m.userData.basePos.clone().sub(c);
      if (dir.lengthSq() < 0.5) dir.set(0, 1, 0);
      m.userData.explode = dir.normalize().multiplyScalar(10);
    });
  }
}
function applyExplode() {
  meshes.forEach(m => {
    if (!m.userData.basePos || !m.userData.explode) return;
    const b = m.userData.basePos, e = m.userData.explode;
    m.position.set(b.x + e.x * explodeF, b.y + e.y * explodeF, b.z + e.z * explodeF);
  });
}

function applyAppearance(top) {
  const sel = top === selected;
  const ghost = top.userData.context && activeSet.size > 0 && !partInSet(top.userData.part);
  top.traverse(o => { if (o.isMesh) o.castShadow = ghost ? false : !!o.userData.cast; });
  top.userData.tint.forEach(t => {
    if (t.edge) {
      t.mat.transparent = true;
      t.mat.opacity = ghost ? 0.22 : (sel ? 0.95 : t.base);
      return;
    }
    const op = ghost ? 0.03 : t.base;
    t.mat.opacity = op;
    t.mat.transparent = op < 1;
    t.mat.depthWrite = op >= 0.5;
    if (t.mat.emissive) t.mat.emissive.set(sel ? '#2bd4ef' : '#000000');
    if ('emissiveIntensity' in t.mat) t.mat.emissiveIntensity = sel ? 0.5 : 0;
  });
}

function refreshAll() { meshes.forEach(applyAppearance); }

// ---------- selection ----------
const ray = new THREE.Raycaster();
const ptr = new THREE.Vector2();
const clickTargets = () => meshes.filter(m => m.visible && m.userData.baseOpacity >= 0.3 && !m.userData.dim);
const resolveTop = o => { while (o && !o.userData.top) o = o.parent; return o; };

function pick(ev) {
  const r = renderer.domElement.getBoundingClientRect();
  ptr.x = ((ev.clientX - r.left) / r.width) * 2 - 1;
  ptr.y = -((ev.clientY - r.top) / r.height) * 2 + 1;
  ray.setFromCamera(ptr, camera);
  const hits = ray.intersectObjects(clickTargets(), true);
  for (const h of hits) { const t = resolveTop(h.object); if (t) return { top: t, point: h.point.clone() }; }
  return null;
}

let downXY = null;
renderer.domElement.addEventListener('pointerdown', e => downXY = [e.clientX, e.clientY]);
renderer.domElement.addEventListener('pointerup', e => {
  if (!downXY) return;
  const moved = Math.hypot(e.clientX - downXY[0], e.clientY - downXY[1]);
  downXY = null;
  if (moved > 5) return;               // was a drag, not a click
  const h = pick(e);
  select(h && h.top);
});
renderer.domElement.addEventListener('pointermove', e => {
  renderer.domElement.style.cursor = pick(e) ? 'pointer' : 'grab';
});
// double-click: recenter the orbit on whatever was hit and ease partway toward it
renderer.domElement.addEventListener('dblclick', e => {
  const h = pick(e);
  if (!h) return;
  const delta = h.point.clone().sub(controls.target);
  camTgtGoal = h.point;
  camPosGoal = camera.position.clone().add(delta.multiplyScalar(0.55));
});

function select(mesh) {
  selected = mesh;
  refreshAll();
  if (mesh) showInfo(mesh.userData.part); else hideInfo();
}

// ---------- info panel ----------
const info = document.getElementById('info');
const infocard = document.getElementById('infocard');
const esc = s => (s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;');

function sysChip(id) {
  const s = SYSTEMS[id]; if (!s) return '';
  return `<span class="chip"><span class="sw" style="background:${s.color}"></span>${esc(s.name)}</span>`;
}
function kv(k, v) { return v ? `<div class="kv"><div class="k">${k}</div><div class="v">${v}</div></div>` : ''; }

function showInfo(part) {
  const specs = part.specs && part.specs.length
    ? `<ul class="tl">${part.specs.map(s => `<li>${esc(s)}</li>`).join('')}</ul>` : '';
  const issues = part.issues && part.issues.length
    ? `<ul class="tl">${part.issues.map(s => `<li>${esc(s)}</li>`).join('')}</ul>` : '';
  const fsm = part.fsm_sources && part.fsm_sources.length
    ? `<ul class="tl">${part.fsm_sources.map(s => `<li class="fade">${esc(s.label)}</li>`).join('')}</ul>` : '';
  infocard.innerHTML = `
    <button class="closex" id="closeinfo">✕</button>
    <h2>${esc(part.name)}</h2>
    <div class="chips">${part.systems.map(sysChip).join('')}</div>
    ${kv('What it does', esc(part.function))}
    ${kv('Where it is', esc(part.location))}
    ${kv('Assembly', esc(part.assembly))}
    ${kv('Part number', part.ford_part_number ? esc(part.ford_part_number) : '<span class="fade">not yet catalogued</span>')}
    ${specs ? kv('Specs', specs) : ''}
    ${issues ? kv('Common issues', issues) : ''}
    ${fsm ? kv('Factory manual', fsm) : ''}
    <div class="kv"><div class="fade">${esc(part.fidelity)} model · id ${esc(part.id)}</div></div>`;
  info.classList.add('show');
  document.getElementById('closeinfo').onclick = () => select(null);
}
function hideInfo() { info.classList.remove('show'); }

// ---------- system rail ----------
const _box = new THREE.Box3(), _sz = new THREE.Vector3();
function frameActive() {
  scene.updateMatrixWorld(true);
  _box.makeEmpty();
  meshes.forEach(m => {
    if (!m.visible) return;
    if (activeSet.size && m.userData.context && !partInSet(m.userData.part)) return;  // frame the selection, not the ghost cage
    _box.expandByObject(m);
  });
  if (_box.isEmpty()) return;
  const center = _box.getCenter(new THREE.Vector3());
  const maxDim = Math.max(..._box.getSize(_sz).toArray());
  const dist = (maxDim * (activeSet.size ? 1.05 : 1.3)) / (2 * Math.tan((camera.fov * DEG) / 2)) + maxDim * 0.15;
  let dir = camera.position.clone().sub(controls.target);
  if (dir.lengthSq() < 1) dir.set(1.4, 0.9, 1.4);
  dir.normalize();
  camPosGoal = center.clone().add(dir.multiplyScalar(Math.max(dist, 26)));
  camTgtGoal = center;
}

const partInSet = part => part.systems.some(s => activeSet.has(s));
const isBodyPart = part => part.systems.some(s => BODY_SYSTEMS.has(s));

function applyVisibility() {
  meshes.forEach(m => {
    const part = m.userData.part;
    let vis;
    if (activeSet.size) {
      // explicitly selected systems always show (even body ones);
      // the body shell stays as a ghost cage unless it's toggled off
      vis = partInSet(part) || (m.userData.context && !bodyHidden);
    } else {
      vis = !(bodyHidden && (m.userData.context || isBodyPart(part)));
    }
    m.visible = vis;
    m.userData.dim = false;
  });
  if (selected && !selected.visible) { selected = null; hideInfo(); }
  refreshAll();
  document.querySelectorAll('.sysbtn[data-sys]').forEach(b =>
    b.classList.toggle('active', b.dataset.sys === '__all' ? activeSet.size === 0 : activeSet.has(b.dataset.sys)));
  const bb = document.getElementById('bodybtn');
  if (bb) {
    bb.classList.toggle('active', !bodyHidden);
    bb.textContent = bodyHidden ? '🫥 Body panels hidden' : '🚚 Body panels shown';
  }
}

// click a system to ADD it to the view; click again to REMOVE it. Empty = whole truck.
function toggleSystem(id) {
  if (!id) activeSet.clear();
  else if (activeSet.has(id)) activeSet.delete(id);
  else activeSet.add(id);
  applyVisibility();
  frameActive();   // fly the camera to the visible selection (or whole truck)
}

function toggleBody() {
  bodyHidden = !bodyHidden;
  applyVisibility();
}

function buildRail() {
  const counts = {};
  meshes.forEach(m => m.userData.part.systems.forEach(s => counts[s] = (counts[s] || 0) + 1));
  const list = document.getElementById('syslist');
  list.innerHTML = Object.keys(SYSTEMS)
    .filter(id => counts[id])
    .map(id => `<button class="sysbtn" data-sys="${id}">
        <span class="sw" style="background:${SYSTEMS[id].color}"></span>${esc(SYSTEMS[id].name)}
        <span class="ct">${counts[id]}</span></button>`).join('');
  document.getElementById('allbtn').dataset.sys = '__all';
  document.getElementById('allbtn').onclick = () => toggleSystem(null);
  list.querySelectorAll('.sysbtn').forEach(b => b.onclick = () => toggleSystem(b.dataset.sys));
  const bb = document.getElementById('bodybtn');
  if (bb) bb.onclick = toggleBody;
}

// ---------- diagnostic views (URL params: ?iso=<sys>&view=side|side2|top|front|iso&snap&axes&explode=0..1) ----------
function setView(name, only) {
  scene.updateMatrixWorld(true);
  _box.makeEmpty();
  meshes.forEach(m => {
    if (!m.visible) return;
    if (only && m !== only) return;
    if (!only && activeSet.size && m.userData.context && !partInSet(m.userData.part)) return;  // frame the selection, not the cage
    _box.expandByObject(m);
  });
  if (_box.isEmpty()) return;
  const c = _box.getCenter(new THREE.Vector3());
  const d = Math.max(..._box.getSize(_sz).toArray()) * (activeSet.size ? 1.15 : 1.5) + 14;
  let pos, up = new THREE.Vector3(0, 1, 0);
  if (name === 'side') pos = c.clone().add(new THREE.Vector3(0, 0, d));        // passenger side
  else if (name === 'side2') pos = c.clone().add(new THREE.Vector3(0, 0, -d)); // driver side
  else if (name === 'top') { pos = c.clone().add(new THREE.Vector3(0, d, 0)); up.set(1, 0, 0); }
  else if (name === 'front') pos = c.clone().add(new THREE.Vector3(d, 0, 0));  // looking rearward from the front
  else pos = c.clone().add(new THREE.Vector3(d * 0.8, d * 0.6, d * 0.8));      // iso
  camera.up.copy(up);
  camPosGoal = pos; camTgtGoal = c;
}

function applyDebug() {
  const q = new URLSearchParams(location.search);
  if (q.has('axes')) scene.add(new THREE.AxesHelper(80));   // red=+X(fwd) green=+Y(up) blue=+Z(right)
  if (q.has('hidebody')) bodyHidden = true;
  const iso = q.get('iso');                                  // comma list, e.g. ?iso=engine,cooling
  if (iso) iso.split(',').forEach(s => activeSet.add(s.trim()));
  if (iso || q.has('hidebody')) { applyVisibility(); frameActive(); }
  const sel = q.get('sel'); let selMesh = null;
  if (sel) { selMesh = meshes.find(x => x.userData.part.id === sel); if (selMesh) select(selMesh); }
  const view = q.get('view'); if (view) setView(view, q.has('zoom') ? selMesh : null);
  if (q.has('snap') && camPosGoal) {                         // jump instantly (deterministic screenshots)
    camera.position.copy(camPosGoal); controls.target.copy(camTgtGoal);
    camPosGoal = null; camera.updateProjectionMatrix();
  }
  if (q.has('dump')) {
    const wait = setInterval(() => {            // let async .glb parts finish loading first
      if (pendingGltf > 0) return;
      clearInterval(wait);
      dumpGeometry();
    }, 120);
  }
  controls.update();
}

// Export every rendered part's true world AABB (+ cable centerlines) for the
// automated geometry checker. Read via headless Chrome --dump-dom.
function dumpGeometry() {
  scene.updateMatrixWorld(true);
  const r3 = v => v.toArray().map(n => +n.toFixed(2));
  const tops = [];
  const out = meshes.map(m => {
    const b = new THREE.Box3().expandByObject(m);
    const p = m.userData.part, mo = p.model || {};
    const rec = {
      id: p.id, systems: p.systems, assembly: p.assembly || '',
      kind: mo.builder || mo.kind || 'box', context: !!mo.context,
      min: r3(b.min), max: r3(b.max),
      size: r3(b.getSize(new THREE.Vector3())), center: r3(b.getCenter(new THREE.Vector3())),
    };
    if ((mo.builder === 'cable' || mo.builder === 'pipe') && Array.isArray(mo.path) && mo.path.length >= 2) {
      const curve = new THREE.CatmullRomCurve3(mo.path.map(a => new THREE.Vector3(a[0], a[1], a[2])), false, 'catmullrom', 0.5);
      rec.samples = curve.getPoints(34).map(r3);
      rec.connects = mo.connects || [];
    }
    rec.penChecked = !mo.context && !rec.samples;   // tells the checker exact tests ran
    tops.push({ rec, m, box: new THREE.Box3().expandByObject(m) });
    return rec;
  });

  // Exact cable-through containment: AABBs false-positive on concave parts (swept
  // bumpers, shells, .glb meshes), so test sample points against REAL geometry via
  // raycast parity. Backfaces must count, so flip materials double-sided briefly.
  const flipped = [];
  meshes.forEach(m => m.traverse(o => {
    if (o.isMesh && o.material.side !== THREE.DoubleSide) {
      flipped.push([o.material, o.material.side]);
      o.material.side = THREE.DoubleSide;
    }
  }));
  const rayc = new THREE.Raycaster();
  const UP = new THREE.Vector3(0, 1, 0);
  const inPart = (pt, top) => {
    rayc.set(pt, UP);
    let n = 0;
    top.traverse(o => { if (o.isMesh) n += rayc.intersectObject(o, false).length; });
    return n % 2 === 1;
  };
  // Exact solid-solid penetration: raycast sampled mesh EDGES of part A against
  // part B's surface — an edge crossing a surface means the parts truly intersect.
  // (Vertex-in-volume misses thin panels: a part poking through 1/8" sheet metal has
  // no vertices inside the sheet itself.) Skips context shells (wrap everything by
  // design), same-assembly pairs (internals nest; explode view pulls them apart),
  // and routed parts (covered by the cable check above).
  const edgesOf = (top, max = 90) => {
    const segs = [];
    top.traverse(o => {
      if (!o.isMesh || segs.length >= max) return;
      const pos = o.geometry.attributes.position;
      const idx = o.geometry.index;
      const triCount = (idx ? idx.count : pos.count) / 3;
      const step = Math.max(1, Math.floor(triCount / 30));
      for (let t = 0; t < triCount && segs.length < max; t += step) {
        const i0 = idx ? idx.getX(t * 3) : t * 3, i1 = idx ? idx.getX(t * 3 + 1) : t * 3 + 1;
        segs.push([new THREE.Vector3().fromBufferAttribute(pos, i0).applyMatrix4(o.matrixWorld),
                   new THREE.Vector3().fromBufferAttribute(pos, i1).applyMatrix4(o.matrixWorld)]);
      }
    });
    return segs;
  };
  const _dir = new THREE.Vector3();
  const crossings = (segs, top, box) => {
    let n = 0;
    for (const [a, b] of segs) {
      if (!box.containsPoint(a) && !box.containsPoint(b)) continue;
      _dir.subVectors(b, a);
      const len = _dir.length();
      if (len < 1e-4) continue;
      rayc.set(a, _dir.divideScalar(len));
      rayc.far = len;
      let hit = false;
      top.traverse(o => { if (!hit && o.isMesh && rayc.intersectObject(o, false).length) hit = true; });
      if (hit) n++;
    }
    rayc.far = Infinity;
    return n;
  };
  const _sz2 = new THREE.Vector3();
  const vol = b => { b.getSize(_sz2); return _sz2.x * _sz2.y * _sz2.z; };
  for (let i = 0; i < tops.length; i++) {
    const A = tops[i];
    if (A.rec.context || A.rec.samples) continue;
    for (let j = i + 1; j < tops.length; j++) {
      const B = tops[j];
      if (B.rec.context || B.rec.samples) continue;
      if (A.rec.assembly && A.rec.assembly === B.rec.assembly) continue;
      const ov = A.box.clone().intersect(B.box);
      if (ov.isEmpty()) continue;
      ov.getSize(_sz2);
      if (_sz2.x * _sz2.y * _sz2.z < 8) continue;
      let n = crossings(edgesOf(A.m), B.m, B.box) + crossings(edgesOf(B.m), A.m, A.box);
      if (n < 3) {
        // no surface crossings — catch full containment (small part swallowed whole)
        const small = vol(A.box) < vol(B.box) ? A : B, big = small === A ? B : A;
        const vs = edgesOf(small.m, 8).map(s => s[0]);
        if (vs.length && vs.every(p => big.box.containsPoint(p) && inPart(p, big.m))) n = 99;
      }
      if (n >= 3) (A.rec.pen = A.rec.pen || {})[B.rec.id] = n;
    }
  }

  const _p = new THREE.Vector3();
  tops.forEach(({ rec }) => {
    if (!rec.samples) return;
    const through = {};
    const pts = rec.samples.slice(4, -4);
    tops.forEach(other => {
      if (other.rec === rec || other.rec.samples) return;   // skip self + other routed parts
      let hits = 0;
      for (const s of pts) {
        _p.set(s[0], s[1], s[2]);
        if (other.box.containsPoint(_p) && inPart(_p, other.m)) hits++;
      }
      if (hits) through[other.rec.id] = hits;
    });
    rec.through = through;
  });
  flipped.forEach(([mat, side]) => mat.side = side);
  const pre = document.createElement('pre');
  pre.id = 'geomdump'; pre.style.display = 'none';
  pre.textContent = JSON.stringify(out);
  document.body.appendChild(pre);
}

// ---------- boot ----------
async function boot() {
  const bust = '?t=' + Date.now();   // cache-bust so a refresh always loads the latest model
  const [sysRes, partRes] = await Promise.all([
    fetch('/inventory/systems.json' + bust, { cache: 'no-store' }),
    fetch('/inventory/parts.json' + bust, { cache: 'no-store' }),
  ]);
  const sysData = await sysRes.json();
  const partData = await partRes.json();
  sysData.systems.forEach(s => SYSTEMS[s.id] = s);
  partData.parts.forEach(addPart);
  refreshAll();
  buildRail();
  document.getElementById('subtitle').textContent =
    `${partData.parts.length} parts catalogued · ${partData.vehicle}`;
  applyDebug();
  const q = new URLSearchParams(location.search);
  if (!q.get('view') && !q.get('iso')) frameActive();   // frame the whole truck on load
  window.__ready = true;   // signal for headless screenshots
  animate();
}

function animate() {
  requestAnimationFrame(animate);
  if (camPosGoal) {
    camera.position.lerp(camPosGoal, 0.14);
    controls.target.lerp(camTgtGoal, 0.14);
    if (camera.position.distanceTo(camPosGoal) < 0.6) camPosGoal = null;
  }
  controls.update();
  renderer.render(scene, camera);
}

addEventListener('resize', () => {
  camera.aspect = innerWidth / innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(innerWidth, innerHeight);
});

boot().catch(err => {
  document.getElementById('subtitle').textContent = 'Error loading inventory: ' + err.message;
  console.error(err);
});
