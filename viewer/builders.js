// Detailed parametric part models. Each builder returns a THREE.Group built in
// local coordinates; the viewer positions/rotates it from the part's model{} block.
// This is the "refined" fidelity tier — real shaped geometry, not massing blocks.
import * as THREE from 'three';

const DEG = Math.PI / 180;

// ---- shared materials ----
const M = {
  steel:     () => new THREE.MeshStandardMaterial({ color: 0x9aa3ad, metalness: 0.9,  roughness: 0.34 }),
  darkSteel: () => new THREE.MeshStandardMaterial({ color: 0x565c64, metalness: 0.85, roughness: 0.45 }),
  cast:      () => new THREE.MeshStandardMaterial({ color: 0x6f757c, metalness: 0.55, roughness: 0.62 }),
  copper:    () => new THREE.MeshStandardMaterial({ color: 0xb87333, metalness: 0.95, roughness: 0.32 }),
  brass:     () => new THREE.MeshStandardMaterial({ color: 0xc9a96a, metalness: 0.9,  roughness: 0.35 }),
  lead:      () => new THREE.MeshStandardMaterial({ color: 0x8d949c, metalness: 0.6,  roughness: 0.5 }),
  blackPl:   () => new THREE.MeshStandardMaterial({ color: 0x1b1f24, metalness: 0.15, roughness: 0.7 }),
  caseDark:  () => new THREE.MeshStandardMaterial({ color: 0x23272e, metalness: 0.2,  roughness: 0.6 }),
  caseTop:   () => new THREE.MeshStandardMaterial({ color: 0x2f343c, metalness: 0.2,  roughness: 0.55 }),
  rubberRed: () => new THREE.MeshStandardMaterial({ color: 0x7a2222, metalness: 0.1,  roughness: 0.8 }),
  rubberBlk: () => new THREE.MeshStandardMaterial({ color: 0x16181c, metalness: 0.1,  roughness: 0.85 }),
};

// ---- primitive helpers (axis = orientation of a cylinder's length) ----
function cyl(r1, r2, len, mat, axis = 'y', seg = 32) {
  const g = new THREE.CylinderGeometry(r1, r2, len, seg);
  if (axis === 'x') g.rotateZ(90 * DEG);
  else if (axis === 'z') g.rotateX(90 * DEG);
  return new THREE.Mesh(g, mat);
}
function box(x, y, z, mat) { return new THREE.Mesh(new THREE.BoxGeometry(x, y, z), mat); }
function ball(r, mat) { return new THREE.Mesh(new THREE.SphereGeometry(r, 24, 16), mat); }
function at(mesh, x, y, z) { mesh.position.set(x, y, z); return mesh; }

// a simple spur gear: root cylinder + trapezoidal teeth around it (axis = x)
function gear(rootR, teeth, toothH, width, mat) {
  const grp = new THREE.Group();
  grp.add(cyl(rootR, rootR, width, mat, 'x', 28));
  const tW = (2 * Math.PI * rootR) / teeth * 0.55;
  for (let i = 0; i < teeth; i++) {
    const a = (i / teeth) * Math.PI * 2;
    const t = box(width, toothH, tW, mat);
    t.position.set(0, Math.cos(a) * (rootR + toothH / 2), Math.sin(a) * (rootR + toothH / 2));
    t.rotation.x = a;
    grp.add(t);
  }
  return grp;
}

// ============================ STARTER MOTOR ============================
// Built along +X; drive/nose at +X, commutator end at -X. ~8.5 in long.
function starterMotor() {
  const g = new THREE.Group();
  const bodyR = 2.2, bodyL = 6;

  // motor housing
  g.add(at(cyl(bodyR, bodyR, bodyL, M.steel(), 'x'), 0, 0, 0));
  // band rings near each end
  g.add(at(cyl(bodyR * 1.04, bodyR * 1.04, 0.4, M.darkSteel(), 'x'), bodyL / 2 - 0.5, 0, 0));
  g.add(at(cyl(bodyR * 1.04, bodyR * 1.04, 0.4, M.darkSteel(), 'x'), -bodyL / 2 + 0.5, 0, 0));
  // commutator end cap
  g.add(at(cyl(bodyR * 0.98, bodyR * 0.86, 1.0, M.cast(), 'x'), -bodyL / 2 - 0.5, 0, 0));
  g.add(at(ball(0.45, M.blackPl()), -bodyL / 2 - 1.0, 0, 0)); // end bushing cap

  // drive-end housing (nose, frustum) + drive gear at the tip
  const noseL = 2.4;
  g.add(at(cyl(bodyR, 1.5, noseL, M.cast(), 'x'), bodyL / 2 + noseL / 2, 0, 0));
  const drive = gear(0.9, 9, 0.35, 1.2, M.steel());
  drive.position.set(bodyL / 2 + noseL + 0.3, 0, 0);
  g.add(drive);

  // through-bolts along the body
  for (const a of [35, 145, 215, 325]) {
    const r = bodyR * 0.92, rad = a * DEG;
    g.add(at(cyl(0.12, 0.12, bodyL + 1.6, M.darkSteel(), 'x'),
      0, Math.cos(rad) * r, Math.sin(rad) * r));
  }

  // solenoid mounted parallel, above the motor toward the drive end
  const sol = new THREE.Group();
  const solR = 1.25, solL = 3.4;
  sol.add(cyl(solR, solR, solL, M.steel(), 'x'));
  sol.add(at(cyl(solR, solR * 0.8, 0.5, M.cast(), 'x'), -solL / 2 - 0.2, 0, 0)); // plunger end
  sol.add(at(ball(solR, M.blackPl()), solL / 2 + 0.1, 0, 0));                    // cap (half-ish)
  // two terminal studs (B+ and S) on the cap with nuts
  for (const z of [-0.5, 0.5]) {
    sol.add(at(cyl(0.16, 0.16, 0.9, M.brass(), 'x'), solL / 2 + 0.6, 0.0, z));
    sol.add(at(cyl(0.28, 0.28, 0.22, M.brass(), 'x'), solL / 2 + 0.95, 0.0, z)); // nut
  }
  sol.position.set(0.6, bodyR + solR - 0.2, 0);
  g.add(sol);

  // jumper strap solenoid -> motor
  g.add(at(box(0.5, 1.0, 0.18, M.copper()), bodyL / 2 - 0.2, bodyR + 0.3, 0));

  // mounting flange with two bolt bosses
  const fl = box(0.5, 3.4, 2.2, M.cast());
  fl.position.set(bodyL / 2 - 0.2, -0.2, 0);
  g.add(fl);
  for (const y of [-1.3, 1.3]) g.add(at(cyl(0.3, 0.3, 0.7, M.darkSteel(), 'x'), bodyL / 2 + 0.2, y, 0));

  return g;
}

// ============================ BATTERY ============================
// Group-24-ish case with terminals, cell caps, and a carry strap.
function battery() {
  const g = new THREE.Group();
  const w = 9, h = 7.5, d = 6.8; // x,y,z
  // tray + hold-down so it sits on the fender instead of floating
  g.add(at(box(w + 0.8, 0.5, d + 0.8, M.darkSteel()), 0, -h / 2 - 0.35, 0));   // tray
  g.add(at(box(0.4, h + 0.5, 0.4, M.darkSteel()), w / 2 + 0.2, -0.2, d / 2 + 0.2)); // hold-down rod
  g.add(at(box(w, h, d, M.caseDark()), 0, 0, 0));
  g.add(at(box(w * 0.96, 0.5, d * 0.96, M.caseTop()), 0, h / 2 + 0.2, 0)); // lid
  // cell caps (2 rows x 3)
  for (const x of [-2.6, 0, 2.6]) for (const z of [-1.4, 1.4])
    g.add(at(cyl(0.6, 0.6, 0.35, M.blackPl(), 'y', 16), x, h / 2 + 0.55, z));
  // terminals (POS outboard +Z toward the relay, NEG inboard -Z toward the engine block)
  const pos = cyl(0.65, 0.5, 1.1, M.lead(), 'y', 20); at(pos, -3.4, h / 2 + 0.8, 2.4); g.add(pos);
  const neg = cyl(0.55, 0.42, 1.0, M.lead(), 'y', 20); at(neg, -3.4, h / 2 + 0.75, -2.4); g.add(neg);
  // colored base rings, laid flat on the lid (ring around Y axis)
  const ringR = new THREE.Mesh(new THREE.TorusGeometry(0.8, 0.18, 8, 18), M.rubberRed());
  ringR.rotation.x = 90 * DEG; at(ringR, -3.4, h / 2 + 0.4, 2.4); g.add(ringR);
  const ringB = new THREE.Mesh(new THREE.TorusGeometry(0.75, 0.18, 8, 18), M.rubberBlk());
  ringB.rotation.x = 90 * DEG; at(ringB, -3.4, h / 2 + 0.4, -2.4); g.add(ringB);
  // carry strap arching over the top
  const strap = new THREE.Mesh(new THREE.TorusGeometry(1.4, 0.16, 8, 20, Math.PI), M.blackPl());
  at(strap, 2.4, h / 2 + 0.2, 0); g.add(strap);
  return g;
}

// ============================ STARTER RELAY ============================
// Ford fender-mount relay: can body, two big copper studs + two small spades.
function relay() {
  const g = new THREE.Group();
  g.add(box(2.4, 2.4, 1.8, M.blackPl()));                 // body
  g.add(at(box(2.4, 0.4, 2.6, M.darkSteel()), 0, -1.0, 0)); // mounting foot
  for (const z of [-0.7, 0.7]) {                            // big battery/starter studs
    g.add(at(cyl(0.22, 0.22, 1.0, M.copper(), 'y', 16), 0.0, 1.5, z));
    g.add(at(cyl(0.34, 0.34, 0.22, M.brass(), 'y', 6), 0.0, 1.85, z));
  }
  for (const z of [-0.4, 0.4]) g.add(at(box(0.4, 0.5, 0.12, M.brass()), 0.9, 1.4, z)); // spade terminals
  return g;
}

// ============================ CABLE ============================
// Routed heavy cable as a tube along world-space waypoints (model.path).
function cable(model) {
  const g = new THREE.Group();
  const pts = (model.path || []).map(p => new THREE.Vector3(p[0], p[1], p[2]));
  if (pts.length < 2) return g;
  const curve = new THREE.CatmullRomCurve3(pts, false, 'catmullrom', 0.5);
  const r = model.cableRadius || 0.34;
  const mat = new THREE.MeshStandardMaterial({
    color: new THREE.Color(model.color || 0x14171b), metalness: 0.2, roughness: 0.75,
  });
  g.add(new THREE.Mesh(new THREE.TubeGeometry(curve, Math.max(16, pts.length * 12), r, 12, false), mat));
  // crimp lugs at each end
  for (const e of [pts[0], pts[pts.length - 1]])
    g.add(at(cyl(r * 1.5, r * 1.5, 0.5, M.lead(), 'y', 12), e.x, e.y, e.z));
  return g;
}

// ============================ IGNITION SWITCH ============================
// Column-mounted electrical switch with rotary actuator + wiring connector.
function ignitionSwitch() {
  const g = new THREE.Group();
  g.add(box(2.6, 1.8, 2.2, M.cast()));                                  // body
  g.add(at(cyl(0.5, 0.5, 1.3, M.steel(), 'x'), 1.6, 0, 0));            // actuator stub (toward lock)
  g.add(at(cyl(0.7, 0.7, 0.3, M.darkSteel(), 'x'), 2.1, 0, 0));        // collar
  const conn = box(1.0, 1.3, 1.7, M.blackPl()); at(conn, -1.6, -0.2, 0); g.add(conn); // connector
  for (const z of [-0.5, 0, 0.5]) g.add(at(cyl(0.08, 0.08, 0.6, M.brass(), 'x'), -2.2, -0.2, z)); // pins
  return g;
}

// ============================ IGNITION LOCK CYLINDER ============================
function ignitionLock() {
  const g = new THREE.Group();
  g.add(cyl(0.85, 0.85, 2.2, M.steel(), 'x'));            // barrel
  g.add(at(cyl(1.1, 1.1, 0.25, M.darkSteel(), 'x'), -0.6, 0, 0)); // mounting flange
  g.add(at(cyl(1.0, 1.0, 0.22, M.brass(), 'x'), 1.2, 0, 0));      // face
  g.add(at(box(0.06, 0.7, 0.2, M.blackPl()), 1.33, 0, 0));        // key slot
  return g;
}

// ============================ CLUTCH PEDAL POSITION SWITCH ============================
function cppSwitch() {
  const g = new THREE.Group();
  g.add(box(1.6, 1.6, 1.1, M.blackPl()));                  // body
  g.add(at(cyl(0.32, 0.32, 1.1, M.steel(), 'x'), 1.1, 0, 0)); // plunger
  g.add(at(cyl(0.45, 0.45, 0.2, M.darkSteel(), 'x'), 0.85, 0, 0)); // collar
  const conn = box(0.7, 1.0, 0.9, M.blackPl()); at(conn, -1.0, -0.1, 0); g.add(conn);
  for (const z of [-0.3, 0.3]) g.add(at(cyl(0.07, 0.07, 0.5, M.brass(), 'x'), -1.45, -0.1, z));
  return g;
}

// ============================ ENGINE — 4.9L (300) I6 ============================
// Built local: X = crankshaft axis (+X toward front of truck), longitudinal inline-six.
function engineLongBlock() {
  const g = new THREE.Group();
  g.add(at(box(30, 10.5, 11, M.cast()), 0, -2.75, 0));                // cylinder block (real ~10.3" deck height)
  g.add(at(box(30.4, 1.2, 11.4, M.cast()), 0, 3.35, 0));              // deck
  g.add(at(box(24, 5, 9.5, M.darkSteel()), -1, -10.5, 0));            // oil pan
  g.add(at(box(9, 2.5, 9, M.darkSteel()), -7, -13, 0));               // sump (deeper at rear)
  g.add(at(box(2.5, 11, 10.6, M.cast()), 15.6, -2.5, 0));             // front timing cover
  g.add(at(box(2, 14, 13, M.cast()), -15.6, -1.5, 0));                // bellhousing flange
  for (const x of [-9, -3, 3, 9]) g.add(at(cyl(1, 1, 0.4, M.steel(), 'z', 12), x, -1, -5.7)); // freeze plugs
  return g;
}
function cylinderHead() {
  const g = new THREE.Group();
  g.add(box(30, 5, 10, M.cast()));
  for (let i = 0; i < 6; i++) {                                       // intake/exhaust port stubs + plug bosses (passenger side +Z)
    const x = -12.5 + i * 5;
    g.add(at(box(2.6, 2, 2, M.cast()), x, 0.4, 5.6));
    g.add(at(cyl(0.5, 0.5, 1.3, M.steel(), 'z', 10), x, 1.7, 6.2));
  }
  return g;
}
function valveCover() {
  const g = new THREE.Group();
  const m = M.blackPl();
  g.add(box(28, 3, 7, m));
  g.add(at(box(27, 1.6, 5.5, m), 0, 2, 0));
  g.add(at(cyl(1.1, 1.1, 1.3, M.steel(), 'y', 16), -10, 3, 2));       // oil fill cap
  for (const x of [-12, -4, 4, 12]) g.add(at(cyl(0.25, 0.25, 0.7, M.steel(), 'y', 8), x, 2.3, -3));
  return g;
}
function intakeManifold() {
  const g = new THREE.Group();
  const m = M.cast();
  g.add(box(26, 4, 4, m));                                            // log
  for (let i = 0; i < 6; i++) g.add(at(box(2.6, 3, 3.5, m), -12.5 + i * 5, -1.5, -2.4)); // runners toward head
  g.add(at(cyl(1.7, 1.7, 2.2, M.steel(), 'y', 18), 6, 3, 0));         // throttle body
  return g;
}
function exhaustManifold() {
  const g = new THREE.Group();
  const m = M.darkSteel();
  g.add(box(26, 3, 3, m));
  for (let i = 0; i < 6; i++) g.add(at(box(2.2, 2.5, 2.6, m), -12.5 + i * 5, 0.4, -1.9)); // runners toward head
  g.add(at(cyl(1.4, 1.4, 3, m, 'y', 16), 8, -2.6, 0));               // collector / outlet
  return g;
}
function harmonicBalancer() {
  const g = new THREE.Group();
  g.add(cyl(3.2, 3.2, 1.6, M.darkSteel(), 'x', 28));                  // damper ring
  for (const x of [-0.5, 0.5]) g.add(at(cyl(3.5, 3.5, 0.4, M.steel(), 'x', 28), x, 0, 0)); // pulley flanges
  g.add(at(cyl(1.2, 1.2, 2.4, M.steel(), 'x', 16), 1.0, 0, 0));       // hub
  g.add(at(cyl(0.5, 0.5, 0.6, M.darkSteel(), 'x', 8), 2.1, 0, 0));    // crank bolt
  return g;
}
function oilFilter() {
  const g = new THREE.Group();
  g.add(cyl(1.7, 1.7, 4.6, M.blackPl(), 'x', 20));
  g.add(at(cyl(1.75, 1.75, 0.6, M.steel(), 'x', 20), -2.2, 0, 0));    // threaded base
  return g;
}
function motorMount() {
  const g = new THREE.Group();
  g.add(box(3, 3, 2.5, M.rubberBlk()));                              // rubber isolator
  g.add(at(box(4, 1, 3.5, M.darkSteel()), 0, -2, 0));               // frame bracket
  g.add(at(box(3.5, 1, 2.2, M.darkSteel()), 0, 2, 0));             // block bracket
  return g;
}

// ============================ ENGINE INTERNALS (explodable) ============================
function crankshaft() {
  const g = new THREE.Group();
  g.add(cyl(1.2, 1.2, 30, M.steel(), 'x', 16));                       // main shaft
  for (let i = 0; i < 6; i++) {
    const x = -12.5 + i * 5, a = i * Math.PI * 2 / 3;
    g.add(at(cyl(2.6, 2.6, 1.3, M.darkSteel(), 'x', 14), x, 0, 0));   // counterweight
    g.add(at(cyl(0.9, 0.9, 1.6, M.steel(), 'x', 10), x + 1.5, Math.cos(a) * 1.6, Math.sin(a) * 1.6)); // rod journal
  }
  g.add(at(cyl(1.4, 1.4, 2, M.darkSteel(), 'x', 12), 16.5, 0, 0));    // snout (front)
  g.add(at(cyl(3, 3, 1, M.darkSteel(), 'x', 18), -16.5, 0, 0));       // rear flange
  return g;
}
function pistonSet() {
  const g = new THREE.Group();
  for (let i = 0; i < 6; i++) {
    const x = -12.5 + i * 5;
    g.add(at(cyl(1.9, 1.9, 3, M.steel(), 'y', 18), x, 0, 0));         // piston
    for (const yy of [1, 0.4]) g.add(at(cyl(1.95, 1.95, 0.18, M.darkSteel(), 'y', 18), x, yy, 0)); // rings
    g.add(at(cyl(0.35, 0.35, 2.2, M.darkSteel(), 'z', 8), x, -0.6, 0)); // wrist pin
  }
  return g;
}
function conrodSet() {
  const g = new THREE.Group();
  for (let i = 0; i < 6; i++) {
    const x = -12.5 + i * 5;
    g.add(at(box(0.8, 6.5, 1.1, M.darkSteel()), x, 0, 0));            // beam
    g.add(at(cyl(1.3, 1.3, 1.4, M.steel(), 'z', 12), x, -3.3, 0));    // big end
    g.add(at(cyl(0.7, 0.7, 1, M.steel(), 'z', 10), x, 3.3, 0));       // small end
  }
  return g;
}
function camshaft() {
  const g = new THREE.Group();
  g.add(cyl(0.9, 0.9, 30, M.steel(), 'x', 14));                       // shaft
  for (let i = 0; i < 12; i++) g.add(at(cyl(1.3, 1.3, 0.9, M.darkSteel(), 'x', 8), -13.5 + i * 2.45, 0.3, 0)); // lobes
  g.add(at(gear(2.2, 18, 0.4, 1, M.steel()), 16, 0, 0));             // cam gear (front)
  return g;
}

// ============================ COOLING ============================
function radiator() {
  const g = new THREE.Group();
  g.add(box(2.5, 22, 28, M.darkSteel()));                              // core
  for (let z = -12; z <= 12; z += 2.5) g.add(at(box(2.7, 20, 0.25, M.steel()), 0, 0, z)); // fin slats
  g.add(at(box(3.2, 3, 30, M.blackPl()), 0, 12, 0));                   // top tank
  g.add(at(box(3.2, 3, 30, M.blackPl()), 0, -12, 0));                  // bottom tank
  g.add(at(cyl(1.1, 1.1, 1.4, M.brass(), 'y', 14), 0, 14, 11));        // filler neck
  g.add(at(cyl(1.3, 1.3, 0.6, M.steel(), 'y', 14), 0, 15.1, 11));      // cap
  g.add(at(cyl(1, 1, 1.6, M.blackPl(), 'x', 12), -2, 10, 10));         // upper hose outlet
  g.add(at(cyl(1.1, 1.1, 1.6, M.blackPl(), 'x', 12), -2, -10, -10));   // lower hose outlet
  return g;
}
function fanBlade() {
  const g = new THREE.Group();
  g.add(cyl(1.6, 1.6, 3, M.darkSteel(), 'x', 16));                     // fan clutch
  g.add(at(cyl(2.1, 2.1, 0.5, M.steel(), 'x', 16), 1.3, 0, 0));        // clutch face
  g.add(at(cyl(1.1, 1.1, 0.6, M.steel(), 'x', 12), -1.7, 0, 0));       // hub
  const blades = 7;
  for (let i = 0; i < blades; i++) {
    const a = (i / blades) * Math.PI * 2;
    const b = box(0.3, 7, 2.4, M.darkSteel());
    b.position.set(-1.6, Math.cos(a) * 4, Math.sin(a) * 4);
    b.rotation.x = a;
    g.add(b);
  }
  return g;
}
function waterPump() {
  const g = new THREE.Group();
  g.add(cyl(2.5, 2.5, 2.6, M.cast(), 'x', 20));                        // volute body
  g.add(at(box(3, 4.5, 4.5, M.cast()), -1.6, 0, 0));                   // flange to block
  g.add(at(cyl(2, 2, 1.5, M.steel(), 'x', 16), 2, 0, 0));             // hub
  g.add(at(cyl(2.6, 2.6, 0.4, M.darkSteel(), 'x', 16), 2.7, 0, 0));    // pulley
  g.add(at(cyl(1.2, 1.2, 2.2, M.cast(), 'y', 12), 0, -2.6, 0));        // lower inlet
  return g;
}
function thermostatHousing() {
  const g = new THREE.Group();
  g.add(cyl(1.4, 1.4, 2, M.cast(), 'y', 14));                          // housing
  g.add(at(cyl(1, 1, 2.2, M.cast(), 'x', 12), 1.3, 0.4, 0));           // outlet neck
  for (const z of [-1, 1]) g.add(at(cyl(0.2, 0.2, 1.6, M.steel(), 'y', 8), 0, -0.4, z));
  return g;
}

// ============================ INTAKE & EXHAUST ============================
// Rigid pipe routed along world waypoints (model.path), metal, no end lugs.
function pipe(model) {
  const g = new THREE.Group();
  const pts = (model.path || []).map(p => new THREE.Vector3(p[0], p[1], p[2]));
  if (pts.length < 2) return g;
  const curve = new THREE.CatmullRomCurve3(pts, false, 'catmullrom', 0.5);
  const r = model.pipeRadius || 1.1;
  g.add(new THREE.Mesh(new THREE.TubeGeometry(curve, Math.max(20, pts.length * 14), r, 14, false), M.darkSteel()));
  return g;
}
function catalyticConverter() {
  const g = new THREE.Group();
  g.add(cyl(2.2, 2.2, 11, M.steel(), 'x', 22));                       // body
  g.add(at(cyl(2.3, 2.3, 7, M.darkSteel(), 'x', 22), 0, 0.3, 0));     // heat shield
  g.add(at(cyl(1.1, 2.2, 2, M.steel(), 'x', 16), 6.5, 0, 0));         // inlet cone
  g.add(at(cyl(2.2, 1.1, 2, M.steel(), 'x', 16), -6.5, 0, 0));        // outlet cone
  return g;
}
function muffler() {
  const g = new THREE.Group();
  const body = cyl(3, 3, 16, M.darkSteel(), 'x', 24); body.scale.set(1, 0.72, 1); g.add(body); // oval
  for (const x of [-7.9, 7.9]) g.add(at(cyl(3.05, 3.05, 0.4, M.steel(), 'x', 24), x, 0, 0));    // crimp seams
  const n1 = cyl(1.1, 1.1, 2, M.steel(), 'x', 12); n1.scale.set(1, 0.72, 1); at(n1, 9, 0, 1.2); g.add(n1);
  const n2 = cyl(1.1, 1.1, 2, M.steel(), 'x', 12); n2.scale.set(1, 0.72, 1); at(n2, -9, 0, -1.2); g.add(n2);
  return g;
}
function airCleaner() {
  const g = new THREE.Group();
  g.add(box(8, 5, 7, M.blackPl()));                                   // housing
  g.add(at(box(8.2, 1, 7.2, M.blackPl()), 0, 2.8, 0));               // lid
  g.add(at(cyl(0.4, 0.4, 1, M.steel(), 'y', 8), 0, 3.6, 0));         // wing nut
  g.add(at(cyl(1.3, 1.3, 4, M.blackPl(), 'x', 12), 5.5, 0, 0));      // inlet snorkel
  g.add(at(cyl(1.6, 1.6, 2.4, M.blackPl(), 'y', 12), -2, -3, 0));    // outlet to throttle body
  return g;
}

// ============================ FUEL ============================
function fuelTank() {
  const g = new THREE.Group();
  g.add(box(32, 12, 12, M.steel()));                                  // tank body (midship, fits rail-to-driveshaft)
  g.add(at(box(32.4, 1, 12.4, M.darkSteel()), 0, 0, 0));              // crimp seam
  for (const x of [-9, 9]) g.add(at(box(1.4, 13, 13, M.darkSteel()), x, 0, 0)); // mounting straps
  g.add(at(cyl(2.4, 2.4, 1.2, M.darkSteel(), 'y', 18), 6, 6.2, -6));  // sender/pump module
  g.add(at(cyl(0.45, 0.45, 1.6, M.steel(), 'y', 8), 6, 7.6, -6));     // supply fitting
  g.add(at(cyl(0.45, 0.45, 1.6, M.steel(), 'y', 8), 7.6, 7.4, -6));   // return fitting
  g.add(at(cyl(1.6, 1.6, 2, M.steel(), 'x', 12), 16, 3, 4));          // filler inlet
  return g;
}
function fuelFilter() {
  const g = new THREE.Group();
  g.add(cyl(1, 1, 4, M.steel(), 'x', 16));                            // canister
  g.add(at(cyl(0.35, 0.35, 1, M.steel(), 'x', 8), 2.4, 0, 0));        // outlet
  g.add(at(cyl(0.35, 0.35, 1, M.steel(), 'x', 8), -2.4, 0, 0));       // inlet
  return g;
}

// ============================ DRIVELINE ============================
// Built local: X = lengthwise, +X = front (toward engine). Bell face at +X13.5.
function transmission() {
  const g = new THREE.Group();
  const al = M.cast();
  g.add(at(cyl(5.5, 5, 5, al, 'x', 24), 10.5, 0, 0));                  // bellhousing
  g.add(at(cyl(6, 6, 0.9, al, 'x', 24), 13.6, 0, 0));                  // bell face flange
  g.add(box(14, 9, 8, al));                                            // main case
  for (const x of [-4, 0, 4]) g.add(at(box(0.4, 9.2, 8.2, M.darkSteel()), x, 0, 0)); // ribs
  g.add(at(cyl(3, 1.6, 9, al, 'x', 20), -11.5, 0, 0));                 // tailshaft housing
  g.add(at(cyl(1.4, 1.4, 3, M.steel(), 'x', 12), -17, 0, 0));         // output yoke
  g.add(at(box(3.5, 2.5, 3.5, al), -1, 5.6, 0));                      // shifter tower
  g.add(at(cyl(0.6, 0.6, 0.5, M.steel(), 'x', 8), 7.2, -4, 0));       // drain plug
  return g;
}
function shifter() {
  const g = new THREE.Group();
  g.add(box(3, 1.5, 3, M.cast()));                                    // base
  const lever = cyl(0.35, 0.35, 12, M.steel(), 'y', 10);
  lever.position.set(-1.5, 6, 0); lever.rotation.z = 0.22; g.add(lever);
  g.add(at(ball(0.9, M.blackPl()), -4.1, 11.6, 0));                   // knob
  return g;
}
function hydraulicCylinder() {
  const g = new THREE.Group();
  g.add(cyl(0.9, 0.9, 3, M.steel(), 'x', 14));                        // body
  g.add(at(cyl(0.4, 0.4, 2, M.steel(), 'x', 8), 2.2, 0, 0));          // pushrod
  g.add(at(cyl(0.28, 0.28, 0.9, M.blackPl(), 'y', 8), -0.8, 1, 0));   // line fitting
  return g;
}

// ============================ REAR AXLE ============================
// Built local: Z = axle axis, X = fore/aft (+X toward front / pinion), Y up.
function rearAxle() {
  const g = new THREE.Group();
  for (const z of [-17, 17]) g.add(at(cyl(1.7, 1.7, 24, M.darkSteel(), 'z', 16), 0, 0, z)); // axle tubes
  for (const z of [-28.5, 28.5]) g.add(at(cyl(2.7, 2.7, 1.2, M.darkSteel(), 'z', 16), 0, 0, z)); // wheel flanges
  g.add(ball(4.6, M.cast()));                                          // pumpkin
  g.add(box(7, 8.5, 8.5, M.cast()));                                   // carrier body
  g.add(at(cyl(2, 1.3, 5, M.cast(), 'x', 16), 5, 0.5, 0));            // pinion snout
  g.add(at(cyl(2.3, 2.3, 0.6, M.darkSteel(), 'x', 12), 7.4, 0.5, 0));  // yoke flange
  g.add(at(box(1.8, 2.6, 2.6, M.darkSteel()), 8.2, 0.5, 0));          // pinion yoke
  g.add(at(cyl(0.5, 0.5, 0.5, M.steel(), 'x', 8), 3, 2.5, 3.5));      // fill plug
  return g;
}
function diffCover() {
  const g = new THREE.Group();
  g.add(cyl(4.4, 4.4, 1.2, M.steel(), 'x', 20));                       // stamped cover
  g.add(at(cyl(4.7, 4.7, 0.4, M.darkSteel(), 'x', 20), 0.7, 0, 0));    // flange
  for (let i = 0; i < 10; i++) {                                       // cover bolts
    const a = (i / 10) * Math.PI * 2;
    g.add(at(cyl(0.18, 0.18, 0.5, M.steel(), 'x', 6), 0.9, Math.cos(a) * 4.1, Math.sin(a) * 4.1));
  }
  return g;
}
function brakeDrum() {
  const g = new THREE.Group();
  g.add(cyl(5.4, 5.4, 4, M.darkSteel(), 'z', 22));                     // drum
  g.add(at(cyl(5.6, 5.6, 0.4, M.steel(), 'z', 22), 0, 0, 1.8));        // backing plate edge
  g.add(at(cyl(2, 2, 1, M.steel(), 'z', 12), 0, 0, -2.2));            // hub
  return g;
}

// ============================ SUSPENSION ============================
function iBeam() {
  const g = new THREE.Group();
  const len = 44;                                                     // spans most of the track
  g.add(box(3, 1, len, M.cast()));                                    // web
  g.add(at(box(4, 0.7, len, M.cast()), 0, 1.1, 0));                   // top flange
  g.add(at(box(4, 0.7, len, M.cast()), 0, -1.1, 0));                  // bottom flange
  g.add(at(cyl(1.6, 1.6, 3, M.darkSteel(), 'z', 12), 0, 0, len / 2 - 1)); // pivot bushing
  g.add(at(box(3, 6, 3, M.cast()), 0, 0, -len / 2 + 1));              // spindle knuckle
  return g;
}
function coilSpring() {
  const g = new THREE.Group();
  const turns = 6, h = 11, r = 2.3, pts = [];
  for (let i = 0; i <= turns * 12; i++) {
    const t = i / (turns * 12);
    pts.push(new THREE.Vector3(Math.cos(t * turns * Math.PI * 2) * r, t * h - h / 2, Math.sin(t * turns * Math.PI * 2) * r));
  }
  g.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), turns * 22, 0.35, 8, false), M.steel()));
  return g;
}
function leafSpring() {
  const g = new THREE.Group();
  for (let i = 0; i < 5; i++) g.add(at(box(48 - i * 7, 0.45, 2.4, M.darkSteel()), 0, -i * 0.55, 0)); // stacked leaves
  g.add(at(box(1.4, 3.2, 3, M.steel()), 0, -1.1, 0));                 // center bolt clamp
  for (const x of [-24, 24]) g.add(at(cyl(0.9, 0.9, 2.6, M.darkSteel(), 'z', 10), x, 0.3, 0)); // eyes
  return g;
}
function shockAbsorber() {
  const g = new THREE.Group();
  g.add(cyl(0.95, 0.95, 7, M.darkSteel(), 'y', 14));                  // body
  g.add(at(cyl(0.35, 0.35, 5, M.steel(), 'y', 10), 0, 5, 0));         // shaft
  g.add(at(ball(0.85, M.rubberBlk()), 0, 8, 0));                      // top mount
  g.add(at(new THREE.Mesh(new THREE.TorusGeometry(0.8, 0.3, 8, 12), M.darkSteel()), 0, -4, 0)); // bottom eye
  return g;
}

// ============================ STEERING ============================
function steeringGear() {
  const g = new THREE.Group();
  g.add(box(6, 7, 6, M.cast()));                                      // recirculating-ball housing
  g.add(at(box(2.2, 2.2, 2.2, M.cast()), 3, 0, 0));                   // side adjuster cover
  g.add(at(cyl(1, 1, 3, M.steel(), 'y', 12), 0, 5, 0));             // input (worm) shaft up
  g.add(at(cyl(1.5, 1.5, 4, M.cast(), 'y', 16), 0, -4.5, 0));        // sector shaft housing down
  for (const z of [-2, 2]) g.add(at(cyl(0.3, 0.3, 1, M.steel(), 'x', 6), -3.2, 0, z)); // mount bolts
  return g;
}
function psPump() {
  const g = new THREE.Group();
  g.add(cyl(2.2, 2.2, 4, M.steel(), 'x', 18));                        // reservoir/body
  g.add(at(cyl(2.5, 2.5, 0.5, M.darkSteel(), 'x', 14), 2.3, 0, 0));   // pulley
  g.add(at(cyl(1.5, 1.5, 1.2, M.steel(), 'x', 12), 2.9, 0, 0));       // pulley hub
  g.add(at(cyl(0.7, 0.7, 0.8, M.blackPl(), 'y', 8), -1, 2, 0));       // fill cap
  return g;
}
function steeringWheel() {
  const g = new THREE.Group();
  const ring = new THREE.Mesh(new THREE.TorusGeometry(4.5, 0.5, 10, 24), M.blackPl());
  ring.rotation.y = 90 * DEG; g.add(ring);                            // wheel plane faces along X
  for (const a of [0, 2.09, 4.19]) { const s = box(0.5, 0.5, 4, M.blackPl()); s.rotation.x = a; g.add(s); } // spokes
  g.add(at(cyl(0.9, 0.9, 1.5, M.darkSteel(), 'x', 10), -0.4, 0, 0));  // hub
  return g;
}

export const BUILDERS = {
  starterMotor, battery, relay, cable, ignitionSwitch, ignitionLock, cppSwitch,
  engineLongBlock, cylinderHead, valveCover, intakeManifold, exhaustManifold,
  harmonicBalancer, oilFilter, motorMount,
  radiator, fanBlade, waterPump, thermostatHousing,
  pipe, catalyticConverter, muffler, airCleaner,
  fuelTank, fuelFilter,
  transmission, shifter, hydraulicCylinder,
  rearAxle, diffCover, brakeDrum,
  iBeam, coilSpring, leafSpring, shockAbsorber,
  steeringGear, psPump, steeringWheel,
  masterBooster, brakeRotor, brakeCaliper,
  wheelTire, alternator,
  crankshaft, pistonSet, conrodSet, camshaft,
  distributor, distributorRotor, ignitionCoil, sparkPlugSet,
  headlamp, tailLight, instrumentCluster, horn, fuseBox, wiperMotor,
  acCompressor, acCondenser, accumulator, blowerMotor, heaterBox, finnedCore,
  frameRail, bodyMount, trailerHitch, towHook,
  doorPanel, sideMirror, tailgate, wheelWell,
  grilleAssembly, bumperBar, fender,
  cabShell, bedShell, hoodPanel,
  seat, dashPanel, pedalSet,
  inputShaft, mainshaftAssembly, countershaftCluster, shiftForks,
  ringGear, pinionGear, diffCarrier, sideGearSet, axleShaft,
  starterArmature, starterDrive, starterBrushes, starterSolenoid,
};

// ============================ STARTER INTERNALS (explodable) ============================
function starterArmature() {
  const g = new THREE.Group();
  g.add(cyl(0.5, 0.5, 8, M.steel(), 'x', 12));                        // shaft
  g.add(cyl(1.6, 1.6, 4, M.darkSteel(), 'x', 16));                    // laminated core
  for (let i = 0; i < 8; i++) { const a = (i / 8) * Math.PI * 2; g.add(at(box(4, 0.3, 0.3, M.copper()), 0, Math.cos(a) * 1.6, Math.sin(a) * 1.6)); } // windings
  g.add(at(cyl(1.2, 1.2, 1.2, M.copper(), 'x', 16), -3, 0, 0));       // commutator
  return g;
}
function starterDrive() {
  const g = new THREE.Group();
  g.add(cyl(1, 1, 2, M.darkSteel(), 'x', 12));                        // overrunning clutch
  g.add(at(gear(0.9, 9, 0.3, 1.2, M.steel()), 1.8, 0, 0));            // pinion
  g.add(at(cyl(0.4, 0.4, 2, M.steel(), 'x', 8), -1.5, 0, 0));         // shaft
  return g;
}
function starterBrushes() {
  const g = new THREE.Group();
  for (let i = 0; i < 4; i++) { const a = (i / 4) * Math.PI * 2 + 0.4; g.add(at(box(0.8, 0.8, 0.6, M.copper()), 0, Math.cos(a) * 1.3, Math.sin(a) * 1.3)); }
  return g;
}
function starterSolenoid() {
  const g = new THREE.Group();
  g.add(cyl(1.25, 1.25, 3.4, M.steel(), 'x', 16));                    // body
  g.add(at(ball(1.25, M.blackPl()), 1.8, 0, 0));                      // cap
  for (const z of [-0.5, 0.5]) g.add(at(cyl(0.16, 0.16, 0.9, M.brass(), 'x', 6), 2.2, 0, z)); // studs
  return g;
}

// ============================ REAR AXLE INTERNALS (explodable) ============================
function ringGear() {
  const g = new THREE.Group();
  const r = gear(5.5, 40, 0.5, 1.2, M.darkSteel()); r.rotation.y = 90 * DEG; g.add(r); // spins on Z axis
  g.add(cyl(2, 2, 1.4, M.steel(), 'z', 16));                          // hub
  return g;
}
function pinionGear() {
  const g = new THREE.Group();
  g.add(cyl(0.9, 0.9, 7, M.steel(), 'x', 12));                        // pinion shaft (toward yoke +X)
  g.add(at(gear(1.8, 12, 0.4, 1.5, M.darkSteel()), -3, 0, 0));        // pinion gear (meshes the ring)
  return g;
}
function diffCarrier() {
  const g = new THREE.Group();
  g.add(cyl(3, 3, 4.5, M.cast(), 'z', 18));                           // carrier body
  for (const z of [-2.3, 2.3]) g.add(at(cyl(3.2, 3.2, 0.4, M.darkSteel(), 'z', 18), 0, 0, z)); // bearing journals
  return g;
}
function sideGearSet() {
  const g = new THREE.Group();
  for (const z of [-1.5, 1.5]) { const gr = gear(1.5, 14, 0.4, 1, M.steel()); gr.rotation.y = 90 * DEG; gr.position.set(0, 0, z); g.add(gr); } // side gears
  for (const y of [-1.5, 1.5]) g.add(at(gear(1.1, 10, 0.3, 0.8, M.darkSteel()), 0, y, 0)); // spider/pinion gears
  return g;
}
function axleShaft() {
  const g = new THREE.Group();
  g.add(cyl(0.9, 0.9, 26, M.steel(), 'z', 12));                       // shaft
  g.add(at(cyl(2.6, 2.6, 0.6, M.darkSteel(), 'z', 16), 0, 0, 13));    // wheel flange (outer +Z end)
  g.add(at(box(0.3, 2, 2, M.steel()), 0, 0, -13));                    // splined inner end
  return g;
}

// ============================ TRANSMISSION INTERNALS (explodable) ============================
function inputShaft() {
  const g = new THREE.Group();
  g.add(cyl(0.85, 0.85, 6, M.steel(), 'x', 14));                      // shaft
  g.add(at(gear(2.4, 24, 0.4, 1.5, M.darkSteel()), -2, 0, 0));        // input gear (rear)
  g.add(at(cyl(0.5, 0.5, 1.5, M.steel(), 'x', 10), 3, 0, 0));         // pilot nose
  return g;
}
function mainshaftAssembly() {
  const g = new THREE.Group();
  g.add(cyl(0.9, 0.9, 22, M.steel(), 'x', 14));                       // mainshaft (along X)
  for (const [x, r, t] of [[-8, 2.6, 28], [-4, 2.9, 30], [0, 3.2, 34], [4, 2.4, 24], [8, 2.0, 20]]) {
    const gr = gear(r, t, 0.4, 1.4, M.darkSteel()); gr.position.set(x, 0, 0); g.add(gr); // 5 gears
  }
  for (const x of [-6, -2, 6]) g.add(at(cyl(1.6, 1.6, 0.8, M.brass(), 'x', 16), x, 0, 0)); // synchros
  return g;
}
function countershaftCluster() {
  const g = new THREE.Group();
  g.add(cyl(0.8, 0.8, 22, M.steel(), 'x', 14));                       // countershaft
  for (const [x, r, t] of [[-8, 2.2, 22], [-4, 2.4, 24], [0, 2.6, 26], [4, 3.0, 30], [8, 3.3, 34]]) {
    const gr = gear(r, t, 0.4, 1.4, M.cast()); gr.position.set(x, 0, 0); g.add(gr); // cluster gears
  }
  return g;
}
function shiftForks() {
  const g = new THREE.Group();
  for (const z of [-1.5, 0, 1.5]) g.add(at(cyl(0.3, 0.3, 16, M.steel(), 'x', 8), 0, 0, z)); // shift rails
  for (let i = 0; i < 3; i++) {
    const f = new THREE.Mesh(new THREE.TorusGeometry(1.4, 0.3, 8, 14, Math.PI * 1.2), M.darkSteel());
    f.rotation.y = 90 * DEG; f.position.set(-4 + i * 4, -2, -1.5 + i * 1.5); g.add(f);   // forks
  }
  return g;
}

// ============================ INTERIOR ============================
const cloth = () => new THREE.MeshStandardMaterial({ color: 0x4a4f57, metalness: 0.1, roughness: 0.88 });
function seat(model) {
  const g = new THREE.Group();
  const w = (model && model.seatW) || 60;
  g.add(box(20, 5, w, cloth()));                                      // bottom cushion
  g.add(at(box(5, 22, w, cloth()), -9, 12, 0));                       // backrest (leans back -X)
  const heads = w > 40 ? [-w / 4, w / 4] : [0];
  for (const z of heads) g.add(at(box(4, 5, 7, cloth()), -10, 24, z)); // headrests
  return g;
}
function dashPanel() {
  const g = new THREE.Group();
  const m = () => new THREE.MeshStandardMaterial({ color: 0x2a2e34, metalness: 0.2, roughness: 0.72 });
  g.add(box(6, 11, 66, m()));                                         // upper dash pad
  g.add(at(box(4, 6, 66, m()), -3, -7, 0));                           // lower/knee bolster
  g.add(at(box(3, 5, 15, m()), -2.5, 3, -18));                        // cluster hood (driver)
  g.add(at(box(3, 5, 12, m()), -2.5, -1, 18));                        // glovebox (passenger)
  for (const z of [-4, 0, 4]) g.add(at(box(1, 2.4, 3, M.blackPl()), -3.2, 2, z)); // center vents
  return g;
}
function pedalSet() {
  const g = new THREE.Group();
  for (let i = 0; i < 3; i++) {
    const z = -2.2 + i * 2.2;
    g.add(at(box(2, 0.4, 1.6, M.darkSteel()), 0, -i * 0.4, z));       // pedal pad
    g.add(at(box(0.4, 4, 0.4, M.darkSteel()), 0.2, 2 - i * 0.4, z));  // arm
  }
  return g;
}

// ============================ EXTERIOR TRIM ============================
function grilleAssembly() {
  const g = new THREE.Group();
  g.add(box(1.5, 13, 58, M.darkSteel()));                             // grille backing
  for (let y = -4.5; y <= 4.5; y += 3) g.add(at(box(2, 1, 56, M.steel()), 0.6, y, 0)); // argent crossbars
  const oval = new THREE.Mesh(new THREE.SphereGeometry(3, 18, 12), new THREE.MeshStandardMaterial({ color: 0x123f86, metalness: 0.5, roughness: 0.35 }));
  oval.scale.set(0.5, 1, 1.7); at(oval, 1.4, 0, 0); g.add(oval);      // Ford blue oval
  return g;
}
function bumperBar() {
  const g = new THREE.Group();
  g.add(box(3, 4, 74, M.steel()));                                    // chrome face bar
  g.add(at(box(2, 2, 74, M.darkSteel()), -1, -2.5, 0));              // lower roll
  for (const z of [-22, 22]) g.add(at(box(3.2, 4.4, 3, M.steel()), 0, 0, z)); // ends
  return g;
}
// Front fender as a real outer skin with a wheel-arch cutout. Local origin =
// record position [69,24,±32]; outboard side inferred from the record's Z sign.
function fender(model) {
  const g = new THREE.Group();
  const s = (model && model.position && model.position[2] < 0) ? -1 : 1;
  const skin = new THREE.Shape();                      // X-Y profile, door to grille
  skin.moveTo(-25, -5); skin.lineTo(-16.88, -5);       // bottom edge aligns with the door bottom (y≈19)
  skin.absarc(0, -9.6, 17.5, 2.875, 0.266, true);      // arch over the front tire
  skin.lineTo(30, -5); skin.lineTo(30, 22); skin.lineTo(-25, 24.2); skin.closePath();
  g.add(at(panel(skin, 1.2, paintWhite()), 0, 0, s < 0 ? -4.3 : 3.1));  // proud of the door skin
  const strip = at(box(55, 1.2, 4.5, paintWhite()), 2.5, 22.5, s * 2);   // top strip in to the hood opening
  strip.rotation.z = -2.3 * DEG;                                          // follows the hood-line slope
  g.add(strip);
  return g;
}

// ============================ BODY — BED PANELS ============================
function tailgate() {
  const g = new THREE.Group();
  g.add(box(2, 20, 62, paintWhite()));                                // tailgate panel (between the end caps)
  g.add(at(box(0.6, 7, 38, M.caseTop()), -1.1, 2, 0));                // FORD stamping recess
  g.add(at(box(1.2, 2, 6, M.darkSteel()), -1.3, 8, 0));               // latch handle
  for (const z of [-30.5, 30.5]) g.add(at(cyl(0.6, 0.6, 2, M.darkSteel(), 'z', 8), 9.5, -9, z)); // hinge pivots
  return g;
}
function wheelWell() {
  const g = new THREE.Group();
  const m = () => paintWhite();
  g.add(at(box(24, 1.5, 9, m()), 0, 5, 0));                           // arch top
  g.add(at(box(24, 7, 1.5, m()), 0, 1, -4.5));                        // inboard wall
  g.add(at(box(1.5, 11, 9, m()), -11, 0, 0));                         // front wall
  g.add(at(box(1.5, 11, 9, m()), 11, 0, 0));                          // rear wall
  return g;
}

// ============================ BODY — CAB PANELS ============================
const paintWhite = () => new THREE.MeshPhysicalMaterial({ color: 0xf0f2f4, metalness: 0.0, roughness: 0.3, clearcoat: 1.0, clearcoatRoughness: 0.12 });

// Shaped sheet-metal panel: 2D profile (with holes) extruded `depth` along +Z,
// with feature edges so the CAD line-work and ghost-cage isolation still read.
function panel(shape, depth, mat, bevel = 0.2) {
  const geo = new THREE.ExtrudeGeometry(shape, {
    depth, curveSegments: 24,
    bevelEnabled: bevel > 0, bevelThickness: bevel, bevelSize: bevel, bevelSegments: 2,
  });
  const mesh = new THREE.Mesh(geo, mat);
  mesh.add(new THREE.LineSegments(
    new THREE.EdgesGeometry(geo, 32),
    new THREE.LineBasicMaterial({ color: 0x3d4855, transparent: true, opacity: 0.35 })
  ));
  return mesh;
}

// ============================ CAB SHELL (SuperCab) ============================
// Local origin = part position [12,49,0]. Real openings: doors, quarter windows,
// windshield, back glass. Pillars/rockers/roof are part of this shell (their
// records stay in the catalog with render:false).
function cabShell() {
  const g = new THREE.Group();

  // side panels — profile in X-Y with door + rear quarter-window openings
  const prof = new THREE.Shape();
  prof.moveTo(-50, -30); prof.lineTo(50, -30); prof.lineTo(50, 1);
  prof.lineTo(41, 1.5); prof.lineTo(33, 17.5); prof.lineTo(-50, 17.5); prof.closePath();
  const door = new THREE.Path();   // full-height opening: rocker (y≈22) to roof rail
  door.moveTo(-6, -27); door.lineTo(30, -27); door.lineTo(30, 15.5); door.lineTo(-6, 15.5); door.closePath();
  const qwin = new THREE.Path();   // quarter window down to the 47.5" beltline
  qwin.moveTo(-39, -1.5); qwin.lineTo(-17, -1.5); qwin.lineTo(-17, 14.5); qwin.lineTo(-39, 14.5); qwin.closePath();
  prof.holes.push(door, qwin);
  for (const s of [-1, 1]) g.add(at(panel(prof, 1.2, paintWhite()), 0, 0, s < 0 ? -38.4 : 37.2));

  // roof (overhangs the sides slightly) + windshield header
  g.add(at(box(83, 2.5, 76.3, paintWhite()), -8.5, 18.75, 0));
  g.add(at(box(3, 2, 73, paintWhite()), 34, 16.6, 0));

  // raked A-pillars (match windshield 28° rake)
  for (const s of [-1, 1]) {
    const bar = box(2.5, 18.5, 2.5, paintWhite());
    bar.position.set(37, 9.5, s * 36.9); bar.rotation.z = 26.6 * DEG;
    g.add(bar);
  }

  // cowl + firewall
  g.add(at(box(8, 1.5, 73, paintWhite()), 45, 0.75, 0));
  g.add(at(box(2, 20, 73, paintWhite()), 49, -10, 0));

  // rear wall with back-glass opening
  g.add(at(box(1.5, 22, 74.6, paintWhite()), -49.4, -9.5, 0));   // below glass
  g.add(at(box(1.5, 3, 74.6, paintWhite()), -49.4, 16, 0));      // above glass
  for (const s of [-1, 1]) g.add(at(box(1.5, 13, 7, paintWhite()), -49.4, 8, s * 34.6));

  // floor pan
  g.add(at(box(100, 1.5, 74.8, paintWhite()), 0, -19.75, 0));
  return g;
}

// ============================ BED SHELL (6.5' short bed) ============================
// Local origin = [-72,36,0]. Outer sides carry the rear wheel-arch cutout.
function bedShell() {
  const g = new THREE.Group();
  const side = new THREE.Shape();
  side.moveTo(-39, -17); side.lineTo(-14.2, -17);
  side.absarc(2.5, -21.6, 17.5, 2.879, 0.263, true);   // wheel arch over the rear tire (axle at world x=-69.5)
  side.lineTo(39, -17); side.lineTo(39, 12); side.lineTo(-39, 12); side.closePath();
  for (const s of [-1, 1]) g.add(at(panel(side, 1.2, paintWhite()), 0, 0, s < 0 ? -36.2 : 35));
  g.add(at(box(78, 1.5, 70, paintWhite()), 0, -11.2, 0));      // bed floor
  g.add(at(box(1.5, 24, 70, paintWhite()), 38.2, 0, 0));       // headboard (front wall)
  for (const s of [-1, 1]) g.add(at(box(78, 1.8, 3, paintWhite()), 0, 12.5, s * 35.5)); // top rails
  return g;
}

// ============================ HOOD ============================
// Local origin = [80,48.5,0]. Slopes toward the nose, rolls down to the grille.
function hoodPanel() {
  const g = new THREE.Group();
  const p = new THREE.Shape();
  p.moveTo(-19, 1.7); p.lineTo(15, -0.2);
  p.quadraticCurveTo(19, -0.7, 19, -3);     // nose rolls down toward the grille
  p.lineTo(17.8, -3);
  p.quadraticCurveTo(17.8, -1.6, 15, -1.4);
  p.lineTo(-19, 0.5); p.closePath();
  g.add(at(panel(p, 68, paintWhite(), 0.15), 0, 0, -34));
  return g;
}
function doorPanel(model) {
  const g = new THREE.Group();
  const w = (model && model.doorW) || 34;
  // full-height door: skin from the rocker (world ~22) to the 47.5" beltline,
  // window frame up to the 64.5" roof rail. Record origin sits at y=42.
  g.add(at(box(w, 25.5, 1, paintWhite()), 0, -7.25, 0));              // outer skin
  g.add(at(box(w - 2, 1, 1, paintWhite()), 0, 5.8, 0));               // beltline trim
  g.add(at(box(1.2, 17, 1, paintWhite()), w / 2 - 0.6, 14, 0));       // front window frame
  g.add(at(box(1.2, 17, 1, paintWhite()), -w / 2 + 0.6, 14, 0));      // rear window frame
  g.add(at(box(w - 2, 1.2, 1, paintWhite()), 0, 22.4, 0));            // top frame
  g.add(at(box(3, 0.8, 0.7, M.darkSteel()), w / 4, 3, 0.8));          // handle (~45" real height)
  return g;
}
function sideMirror() {
  const g = new THREE.Group();
  g.add(box(0.7, 3.4, 4.4, M.blackPl()));                             // mirror head
  g.add(at(box(0.3, 2.8, 3.6, M.caseTop()), 0.5, 0, 0));              // mirror glass
  g.add(at(box(3, 1, 0.8, M.blackPl()), -1.7, -0.6, 0));             // stalk
  return g;
}

// ============================ FRAME & CHASSIS ============================
function frameRail() {
  const g = new THREE.Group();
  const L = 210;
  g.add(box(L, 6, 2.2, M.darkSteel()));                               // web
  g.add(at(box(L, 1, 3.4, M.darkSteel()), 0, 2.6, 0));                // top flange (C-channel)
  g.add(at(box(L, 1, 3.4, M.darkSteel()), 0, -2.6, 0));               // bottom flange
  for (let x = -95; x <= 95; x += 18) g.add(at(cyl(0.28, 0.28, 2.4, M.steel(), 'z', 6), x, 0, 0)); // rivets
  return g;
}
function bodyMount() {
  const g = new THREE.Group();
  g.add(cyl(1.4, 1.4, 2, M.rubberBlk(), 'y', 14));                    // rubber isolator
  g.add(at(cyl(0.4, 0.4, 3.2, M.steel(), 'y', 8), 0, 0, 0));          // through bolt
  g.add(at(cyl(1.6, 1.6, 0.3, M.steel(), 'y', 14), 0, -1.1, 0));      // washer
  return g;
}
function trailerHitch() {
  const g = new THREE.Group();
  g.add(box(2.5, 3, 42, M.darkSteel()));                              // cross tube
  g.add(at(box(9, 2.6, 2.6, M.darkSteel()), -3, -1, 0));             // receiver tube (rearward -X)
  g.add(at(box(0.6, 2, 2, M.blackPl()), -7.5, -1, 0));               // receiver opening
  g.add(at(cyl(0.5, 0.5, 3, M.steel(), 'y', 8), -3, 0.5, 0));        // hitch pin hole boss
  for (const z of [-17, 17]) g.add(at(box(3, 3, 2, M.darkSteel()), 4, 0, z)); // frame mount plates
  return g;
}
function towHook() {
  const g = new THREE.Group();
  g.add(box(1, 4, 1.2, M.steel()));                                   // shank
  g.add(at(new THREE.Mesh(new THREE.TorusGeometry(1.3, 0.45, 8, 14, Math.PI * 1.4), M.steel()), 0, -2.4, 0)); // hook
  g.add(at(box(2.5, 1, 2.5, M.darkSteel()), 0, 2, 0));               // bolt plate
  return g;
}

// ============================ HVAC ============================
function acCompressor() {
  const g = new THREE.Group();
  g.add(cyl(2.4, 2.4, 5, M.steel(), 'x', 18));                        // compressor body
  g.add(at(cyl(2.6, 2.6, 1, M.darkSteel(), 'x', 16), 2.8, 0, 0));     // clutch
  g.add(at(cyl(2.7, 2.7, 0.4, M.darkSteel(), 'x', 16), 3.4, 0, 0));   // pulley
  g.add(at(box(1, 3, 3, M.cast()), -2.5, -1, 0));                     // mount ear
  for (const y of [2.2, 1]) g.add(at(cyl(0.5, 0.5, 1.2, M.brass(), 'y', 8), -1, y, 0)); // ports
  return g;
}
function acCondenser() {
  const g = new THREE.Group();
  g.add(box(1.5, 22, 28, M.darkSteel()));                            // core
  for (let z = -12; z <= 12; z += 2.5) g.add(at(box(1.6, 20, 0.2, M.steel()), 0, 0, z)); // fins
  g.add(at(box(2, 2, 29, M.blackPl()), 0, 11, 0));                    // top tank
  g.add(at(box(2, 2, 29, M.blackPl()), 0, -11, 0));                   // bottom tank
  return g;
}
function accumulator() {
  const g = new THREE.Group();
  g.add(cyl(1.6, 1.6, 7, M.steel(), 'y', 16));                        // canister
  for (const y of [2.5, 1]) g.add(at(cyl(0.5, 0.5, 1.5, M.brass(), 'x', 8), 1.5, y, 0)); // ports
  return g;
}
function blowerMotor() {
  const g = new THREE.Group();
  g.add(cyl(1.8, 1.8, 2.5, M.darkSteel(), 'y', 16));                  // motor
  g.add(at(cyl(2.6, 2.6, 3, M.blackPl(), 'y', 20), 0, 2.6, 0));       // squirrel-cage housing
  return g;
}
function heaterBox() {
  const g = new THREE.Group();
  g.add(box(7, 7, 8, M.blackPl()));                                   // plenum case
  g.add(at(box(3, 3, 2, M.blackPl()), 0, 4, 2));                      // defrost duct
  g.add(at(box(2.5, 4, 2, M.blackPl()), -4, -2, 0));                  // floor duct
  return g;
}
function finnedCore() {                                               // heater core / evaporator
  const g = new THREE.Group();
  g.add(box(1, 4, 5, M.copper()));                                    // core
  for (let z = -2; z <= 2; z += 1) g.add(at(box(1.1, 3.6, 0.15, M.steel()), 0, 0, z)); // fins
  for (const z of [-2.2, 2.2]) g.add(at(cyl(0.4, 0.4, 1, M.brass(), 'x', 8), 0.9, 1.5, z)); // pipes
  return g;
}

// ============================ BODY ELECTRICAL & LIGHTING ============================
function headlamp() {
  const g = new THREE.Group();
  g.add(box(2, 5, 8, M.darkSteel()));                                 // reflector bucket
  g.add(at(box(0.6, 4.6, 7.6, M.caseTop()), 1.1, 0, 0));              // lens (faces +X front)
  for (const z of [-2.5, 0, 2.5]) g.add(at(box(0.7, 4.4, 0.12, M.steel()), 1.2, 0, z)); // lens ribs
  return g;
}
function tailLight() {
  // OBS taillight: VERTICAL rectangle in the bedside end cap (~8" tall x 5.5" wide)
  const g = new THREE.Group();
  g.add(box(2, 8, 5.5, M.darkSteel()));                               // housing
  g.add(at(box(0.5, 7.4, 4.9, M.rubberRed()), -1.1, 0, 0));           // red lens (faces -X rear)
  const backup = new THREE.Mesh(new THREE.BoxGeometry(0.4, 2.2, 2.2),
    new THREE.MeshStandardMaterial({ color: 0xe8e8e8, metalness: 0.1, roughness: 0.4 }));
  g.add(at(backup, -1.3, -2.2, 0));                                   // backup lens, lower section
  return g;
}
function instrumentCluster() {
  const g = new THREE.Group();
  g.add(box(2, 5, 10, M.blackPl()));                                  // cluster housing
  for (const z of [-3, -1, 1, 3]) {                                   // round gauges (face -X toward driver)
    g.add(at(cyl(1.4, 1.4, 0.3, M.darkSteel(), 'x', 16), -1, 0, z));
    g.add(at(cyl(1.2, 1.2, 0.2, M.caseTop(), 'x', 16), -1.25, 0, z));
  }
  return g;
}
function horn() {
  const g = new THREE.Group();
  g.add(cyl(2.2, 2.2, 1.5, M.blackPl(), 'x', 20));                    // horn body
  g.add(at(cyl(2.4, 2.4, 0.3, M.darkSteel(), 'x', 20), 0.9, 0, 0));   // front grille
  g.add(at(box(1.6, 1, 0.6, M.darkSteel()), -1, -2, 0));             // bracket
  return g;
}
function fuseBox() {
  const g = new THREE.Group();
  g.add(box(3, 5, 4, M.blackPl()));                                   // box
  for (let i = 0; i < 3; i++) for (const y of [-1.2, 0.6]) g.add(at(box(0.7, 0.9, 1.2, M.caseTop()), 1.4, y, -1.2 + i * 1.2)); // relays
  return g;
}
function wiperMotor() {
  const g = new THREE.Group();
  g.add(cyl(1.6, 1.6, 3, M.darkSteel(), 'x', 16));                    // motor
  g.add(at(box(2.6, 2.6, 1.6, M.cast()), 1.9, 0, 0));                 // gearbox
  g.add(at(cyl(0.4, 0.4, 1.2, M.steel(), 'y', 8), 1.9, 1.6, 0));      // output crank
  return g;
}

// ============================ IGNITION ============================
function distributor() {
  const g = new THREE.Group();
  g.add(cyl(2, 2, 4, M.cast(), 'y', 18));                             // body
  g.add(at(cyl(2.2, 2.2, 0.5, M.darkSteel(), 'y', 18), 0, -2.1, 0));  // base hold-down
  g.add(at(cyl(2.3, 2.3, 1.6, M.blackPl(), 'y', 20), 0, 3, 0));       // cap
  for (let i = 0; i < 6; i++) { const a = (i / 6) * Math.PI * 2; g.add(at(cyl(0.35, 0.35, 1, M.blackPl(), 'y', 8), Math.cos(a) * 1.7, 4, Math.sin(a) * 1.7)); } // plug towers
  g.add(at(cyl(0.4, 0.4, 1.2, M.blackPl(), 'y', 8), 0, 4.1, 0));      // center coil tower
  g.add(at(cyl(1, 1, 0.5, M.darkSteel(), 'x', 12), 2.4, 1, 0));       // vacuum advance
  return g;
}
function distributorRotor() {
  const g = new THREE.Group();
  g.add(cyl(1.4, 1.4, 0.4, M.blackPl(), 'y', 16));                    // rotor disc
  g.add(at(box(0.3, 0.3, 1.4, M.copper()), 0, 0.2, 0.6));             // contact arm
  return g;
}
function ignitionCoil() {
  const g = new THREE.Group();
  g.add(cyl(1.4, 1.4, 4, M.darkSteel(), 'y', 16));                    // oil-filled can
  g.add(at(cyl(1.5, 1.5, 0.5, M.steel(), 'y', 16), 0, 2, 0));         // top plate
  g.add(at(cyl(0.5, 0.5, 1, M.blackPl(), 'y', 8), 0, 2.6, 0));        // HT tower
  for (const x of [-0.6, 0.6]) g.add(at(cyl(0.15, 0.15, 0.4, M.brass(), 'y', 6), x, 2.3, 0)); // + / - terminals
  return g;
}
function sparkPlugSet() {
  const g = new THREE.Group();
  for (let i = 0; i < 6; i++) {
    const x = -12.5 + i * 5;
    g.add(at(cyl(0.5, 0.5, 1.2, M.steel(), 'y', 8), x, 0, 0));        // hex base
    g.add(at(cyl(0.4, 0.4, 1.4, M.caseTop(), 'y', 8), x, 1.3, 0));    // ceramic insulator
    g.add(at(cyl(0.25, 0.25, 0.5, M.darkSteel(), 'y', 6), x, 2.2, 0)); // terminal
  }
  return g;
}

// ============================ CHARGING ============================
function alternator() {
  const g = new THREE.Group();
  g.add(cyl(2.6, 2.6, 3.5, M.steel(), 'x', 20));                      // stator body
  g.add(at(cyl(2.7, 2.4, 1.5, M.cast(), 'x', 18), 2.2, 0, 0));        // drive-end housing
  g.add(at(cyl(2.7, 2.4, 1.5, M.cast(), 'x', 18), -2.2, 0, 0));       // rear housing
  g.add(at(cyl(1.7, 1.7, 0.6, M.darkSteel(), 'x', 16), 3.4, 0, 0));   // pulley
  g.add(at(cyl(0.8, 0.8, 1, M.steel(), 'x', 10), 3.9, 0, 0));         // shaft nut
  g.add(at(box(1, 3, 1.4, M.cast()), -1, -2.6, 1.4));                 // lower mount ear
  g.add(at(box(1.6, 1, 1, M.cast()), 1, 2.7, 0));                     // top adjuster ear
  g.add(at(cyl(0.3, 0.3, 0.9, M.brass(), 'x', 6), -3.1, 1, 0));       // B+ terminal
  return g;
}

// ============================ WHEELS & TIRES ============================
// Built along Z; styled (outboard) face at +Z. Left-side wheels get rotation [0,180,0].
function wheelTire() {
  const g = new THREE.Group();
  const W = 9.3, R = 14.4, rim = 7.6;
  // tire = torus (so the rim face actually shows) + flat tread band
  const tire = new THREE.Mesh(new THREE.TorusGeometry((R + rim) / 2, (R - rim) / 2 + 0.4, 18, 48), M.rubberBlk());
  g.add(tire);                                                        // torus axis is already +Z
  g.add(cyl(R, R, W * 0.55, M.rubberBlk(), 'z', 48));                 // tread band
  g.add(at(cyl(rim, rim, W - 1.4, M.steel(), 'z', 30), 0, 0, 0));     // rim barrel
  g.add(at(cyl(rim + 0.15, rim + 0.15, 0.7, M.steel(), 'z', 30), 0, 0, W / 2 - 1.3)); // outboard lip
  g.add(at(cyl(rim - 0.6, rim - 0.6, 0.6, M.steel(), 'z', 26), 0, 0, W / 2 - 1.7));    // wheel face
  for (let i = 0; i < 6; i++) {                                       // styled slots
    const a = (i / 6) * Math.PI * 2;
    g.add(at(cyl(1.4, 1.4, 0.8, M.rubberBlk(), 'z', 12), Math.cos(a) * 4.6, Math.sin(a) * 4.6, W / 2 - 1.5));
  }
  g.add(at(cyl(2.1, 2.1, 1, M.darkSteel(), 'z', 18), 0, 0, W / 2 - 1.1)); // center cap
  for (let i = 0; i < 5; i++) {                                       // lug nuts
    const a = (i / 5) * Math.PI * 2 + 0.3;
    g.add(at(cyl(0.45, 0.45, 0.7, M.steel(), 'z', 6), Math.cos(a) * 2.5, Math.sin(a) * 2.5, W / 2 - 0.9));
  }
  return g;
}

// ============================ BRAKES ============================
function masterBooster() {
  const g = new THREE.Group();
  g.add(cyl(4, 4, 7, M.darkSteel(), 'x', 22));                        // vacuum booster
  g.add(at(cyl(4.2, 4.2, 0.5, M.steel(), 'x', 14), 3.4, 0, 0));       // booster front shell
  g.add(at(box(3, 3.4, 3.4, M.steel()), 5.8, 0, 0));                  // master cylinder body
  g.add(at(box(3.6, 2.4, 3, M.blackPl()), 5.8, 2.4, 0));             // fluid reservoir
  return g;
}
function brakeRotor() {
  const g = new THREE.Group();
  g.add(cyl(6.5, 6.5, 1.2, M.steel(), 'z', 28));                      // disc
  g.add(at(cyl(3, 3, 2.6, M.darkSteel(), 'z', 16), 0, 0, -1.2));      // hat
  for (let i = 0; i < 5; i++) { const a = (i / 5) * Math.PI * 2; g.add(at(cyl(0.25, 0.25, 1, M.steel(), 'z', 6), Math.cos(a) * 2, Math.sin(a) * 2, 0.8)); } // studs
  return g;
}
function brakeCaliper() {
  const g = new THREE.Group();
  g.add(box(3.6, 4.2, 3.2, M.cast()));                                // caliper body
  g.add(at(box(1, 3.6, 3.6, M.cast()), 0, 0, 0));                     // bridge over rotor
  g.add(at(cyl(0.4, 0.4, 1, M.steel(), 'y', 6), 1.2, -2.4, 0));       // bleeder
  return g;
}
