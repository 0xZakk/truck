# Project: a complete, interactive 3D 1994 Ford F-150

**Vehicle:** 1994 Ford F-150 XLT SuperCab · 2WD · 4.9L (300 cu in) inline-six ·
M5OD-R2 5-speed manual · white.

## Current scope clarification (2026-09-22)

The owner selected **engine first** and requires individually modeled physical
components assembled into nested, working mechanisms across the entire truck.
See [COMPONENT-MODEL.md](COMPONENT-MODEL.md) for the component architecture and
acceptance criteria, and [RESTART.md](RESTART.md) for the restart audit. This
supersedes older suggestions to leave the engine until last or treat detailed
exterior meshes as completed systems. Rendering fidelity and verified accuracy
are separate measures; a sourced mesh is not automatically accurate.

## The end goal
An assembled, interactive 3D model of the **entire truck**, renderable in the
browser (WebGL), built from a 3D model of **every individual part**. With it you can:
- **Highlight any part** → a page explaining where it is and what it does.
- **Isolate any system** (ignition, transmission, brakes, …) → a 3D view of just
  that system, for a walkthrough of how it works.
- Eventually **diagnose common issues** system by system.

## How we actually get there (the strategy)
Two intertwined tracks. The inventory is the spine; the 3D model hangs off it.

### Track A — the inventory (the foundation)
A comprehensive, structured catalog of **every part on the truck**, down to trim,
clips, and fasteners. Source: the factory service manual exploded views + Ford
parts catalogs (mine `manuals/`), cross-checked against the actual truck.
- One record per part in `inventory/parts.json`, following `inventory/schema.md`.
- Each record carries its function, location, Ford part number, specs, common
  issues, manual references, **and** a geometry spec + real-world coordinates.

### Track B — the 3D model (progressive fidelity)
**The viewer is generated entirely from the inventory.** Adding a part record adds
it to the 3D truck — no per-part viewer code. Every part climbs a fidelity ladder:
1. **massing** — primitives (box/cylinder/sphere) at correct size & position. The
   truck is recognizable and fully interactive from day one.
2. **refined** — hand-authored parametric mesh, better-shaped.
3. **sourced** — a real `.glb` mesh (licensed/commissioned/scanned) in `models/`.

A part is useful at every rung, so we never block the catalog on perfect geometry.

> **Honest scope note.** I can't conjure photoreal CAD of a real starter from
> nothing. The achievable, genuinely useful path is the ladder above: get the
> whole truck blocked out and interactive first, then deepen fidelity part by part
> (and bring in real meshes where they exist). The catalog work — every part,
> located, explained, with part numbers — is the long grind this goal is built for.

## Repo layout
```
inventory/
  schema.md       # part-record contract + coordinate convention (READ FIRST)
  systems.json    # system taxonomy (tags + colors used to isolate/colour parts)
  parts.json      # THE inventory — the viewer builds the truck from this
viewer/
  index.html      # WebGL explorer (Three.js via CDN)
  app.js          # builds the scene from inventory, selection + system isolation
models/           # (future) sourced/refined .glb meshes
manuals/          # factory service manual + owner's/Haynes refs (research source)
docs/
  PROJECT.md      # this file
  PROGRESS.md     # running ledger + coverage tracker (update every session)
scripts/serve.py  # static server (127.0.0.1:8080), serves repo root
```

## Run it
```
python3 scripts/serve.py            # → http://127.0.0.1:8080/  (redirects to /viewer/)
# remote (tailnet): tailscale serve --bg --https=443 http://127.0.0.1:8080
```

## How to run this as a long goal (the loop)
Each work session does one tractable bite and logs it in `docs/PROGRESS.md`:
1. Pick the next assembly/system to catalog (see the coverage tracker).
2. Mine the FSM exploded views for that assembly: enumerate parts, part numbers,
   quantities, locations.
3. Add/update records in `parts.json` (massing geometry + real coordinates).
4. Verify it renders (`scripts/serve.py`) and looks right; adjust coordinates.
5. Update `docs/PROGRESS.md` (what was added, what's next).
Repeat. The truck fills in and deepens over time.

## Open decisions to confirm with the owner
- **Fidelity target & how high to climb the ladder** (massing everywhere first, vs.
  deep-detailing hero systems early).
- **Sourcing real meshes** (commission/license vs. stay fully parametric).
- **Cataloging order** (which systems first).
