# cad/ — build123d part sources (text-to-cad skill pipeline)

Parametric CAD sources for high-fidelity parts, replacing hand-built Blender meshes
part by part. Authored with the **text-to-cad** Claude skill (`cad@text-to-cad` plugin):
build123d on the OpenCASCADE kernel — real BREP solids with proper fillets, chamfers,
counterbores, and boolean-clean geometry. STEP is the primary artifact; the viewer GLB
is a derived export.

## Pipeline

```
cad/<part-id>.py  ──scripts/cad_export.sh──►  cad/<part-id>.step  +  models/<part-id>.glb
```

```bash
scripts/cad_export.sh cad/<part-id>.py        # generate/regenerate STEP + viewer GLB
```

The venv is `.venv-cad/` (Python 3.11: build123d, cadquery-ocp, cadpy, playwright).
The skill's own tools (run from repo root, targets cwd-relative):

```bash
SKILL=~/.claude/plugins/cache/text-to-cad/cad/0.3.0/skills/cad
.venv-cad/bin/python $SKILL/scripts/inspect refs cad/<part>.step --facts --planes   # measurements
.venv-cad/bin/python $SKILL/scripts/snapshot --input cad/<part>.step --output /tmp/snap.png
```

## Conventions (must match inventory/schema.md + viewer)

- **1 build123d unit = 1 INCH** — sources read like the FSM dimensions. (The skill's
  docs assume mm; ignore that. Inspect/snapshot numbers are therefore inches.)
- **Axes:** +X forward, +Z up, +Y LEFT. Origin = the part record's `position`.
  cadpy's GLB export bakes the Z-up→Y-up swap into vertices ((x,y,z)→(x,z,−y)),
  which lands exactly in viewer part-local axes (+X fwd, +Y up, +Z right).
- **Scale:** cadpy GLB export divides by 1000 (mm→meters), so every record using one
  of these meshes needs `"model": { "kind": "gltf", "src": "../models/<id>.glb",
  "glbScale": 1000 }`. (Blender-era glbs stay scale 1 / no glbScale.)
- One part per file; filename = part id from `inventory/parts.json`. Define
  `def gen_step():` returning the labeled solid/compound. Name every dimension as a
  parameter; label parts verbosely.
- `cad/<part>.step` and the hidden `.<part>.step.glb` topology sidecars are
  generated (gitignored); the `.py` is the source of truth. `models/*.glb` get
  force-added (load-bearing for the viewer, see .gitignore).

## Verify loop (every part, every change)

1. `scripts/cad_export.sh cad/<part>.py`
2. Snapshot the STEP and **Read the PNG** — never ship blind.
3. Reload viewer / `python3 scripts/check_geometry.py` for placement vs neighbors.
