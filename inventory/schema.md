# Inventory schema & coordinate convention

This is the contract every part record follows. The 3D viewer is generated
**entirely** from `parts.json` — adding a part to the data adds it to the truck.
Keep this stable; if it changes, update the viewer (`viewer/app.js`) to match.

## Coordinate convention (read this before placing any part)

Units: **inches**. Right-handed, Y-up (matches Three.js directly — no remap).

- **Origin:** center of the wheelbase, on the ground, on the vehicle centerline.
- **+X = forward** (toward the front bumper). Front axle ≈ +69, rear axle ≈ −69.
- **+Y = up** (Y = 0 is the ground).
- **+Z = right** (passenger side, US-spec). Driver side is −Z.

Reference numbers for a 1994 F-150 SuperCab, 2WD, 4.9L I6 (approximate — refine
as we measure the actual truck):
- Wheelbase ≈ 138.8 in · overall length ≈ 213 in · width ≈ 79 in · height ≈ 73 in
- Track ≈ 65 in (wheel centers at Z ≈ ±33) · frame rails at Z ≈ ±17
- Tire (P235/75R15) ≈ 28.8 in dia → radius ≈ 14.4, width ≈ 9.3
- Frame top ≈ Y 22–28 · cab roof ≈ Y 73

## Part record

```jsonc
{
  "id": "starter-motor",            // stable kebab-case slug, unique
  "name": "Starter motor",          // display name
  "systems": ["electrical-starting"], // 1+ system ids from systems.json
  "assembly": "Starting system",    // human-readable parent grouping
  "qty": 1,                          // how many on the truck
  "function": "Spins the flywheel ring gear to crank the engine.",
  "location": "Low on the rear passenger side of the engine block.",
  "ford_part_number": "F2TZ-11002-A",   // optional, "" if unknown
  "specs": ["~150–220 A under load", "permanent-magnet gear reduction"], // optional
  "fsm_sources": [                   // optional, links into the factory manual
    { "label": "Starter Motor: Description and Operation",
      "path": "Repair%20and%20Diagnosis/.../index.html" }
  ],
  "issues": ["No crank", "Slow crank", "Spins but engine won't turn"], // optional
  "model": {                         // how to draw it (see below)
    "kind": "cylinder",
    "radius": 3, "length": 9, "axis": "x",
    "position": [62, 20, 8],
    "rotation": [0, 0, 0],           // degrees, optional
    "color": "#9aa6b2",              // optional; defaults to the system color
    "opacity": 1                     // optional; <1 ghosts the part (body panels)
  },
  "fidelity": "massing",             // massing | refined | sourced
  "status": "todo"                   // todo | placed | documented | done
}
```

### `model` shapes (lowest → highest fidelity)
- **Single primitive** — `kind: "box" | "cylinder" | "sphere"`:
  - `box` → `size: [x, y, z]`
  - `cylinder` → `radius`, `length`, `axis: "x"|"y"|"z"` (length runs along that axis)
  - `sphere` → `radius`
- **`kind: "group"`** — `parts: [ <primitive>, … ]`, each child primitive with its own
  `position`/`rotation` *relative to the group origin*. Selects/highlights as ONE part.
- **`builder: "<name>"`** — a hand-authored detailed mesh from `viewer/builders.js`
  (e.g. `starterMotor`, `battery`, `relay`, `cable`). This is the **refined** tier.
  Builder-specific fields pass through (e.g. `cable` takes `path: [[x,y,z],…]` in
  **world** coords + `color`). The group is positioned by the record's `position`/`rotation`.
- **`gltf`** — `src: "models/<file>.glb"` (the **sourced** tier; real CAD/scanned mesh).

`position`/`rotation`/`scale` on the top-level `model` place the whole part.
`opacity < 1` ghosts it (used for body shells). `placement: "internal"` (or
`render: false`) catalogs the part but doesn't draw it at truck scale yet — for
parts that live inside an assembly (starter armature, brushes, …), to be shown in an
exploded view later.

`position` is the part **center** in the world frame above. `rotation` is degrees
(XYZ Euler), optional. Mirror-image left/right parts share geometry with flipped Z.

## Fidelity ladder (how a part matures)
1. **massing** — primitive(s) at correct size/position. Recognizable silhouette,
   fully interactive. This is the default for a newly catalogued part.
2. **refined** — hand-authored parametric mesh (still code/primitives, but shaped).
3. **sourced** — a real glTF/`.glb` mesh dropped into `models/` (commissioned,
   licensed CAD, or scanned). Highest fidelity.

A part is useful at every rung — we never block the catalog on having a perfect mesh.
