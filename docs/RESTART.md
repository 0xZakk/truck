---
title: "Restart plan for an evidence-backed interactive truck"
date: 2026-09-22
---

## Intended result

An explorable replica of the owner's truck, with nested exploded assemblies,
mechanical motion, system explanations, and source-linked diagnostic pathways.
The owner confirmed on 2026-09-22: white 1994 F-150 XLT SuperCab, 2WD,
4.9L inline-six, M5OD-R2 five-speed manual. No modifications or swapped
components were reported. The inventory also records a short bed; its dimensions
and component identifiers still need physical verification.

## Verified checkout audit

- 281 inventory part records; 61 GLB references, all resolving to local files.
- 44 files in models; 37 Python CAD sources and four Blender generator scripts.
- 163 source pages, 354 atomic notes, 21 maps.
- Viewer code includes system isolation, body hiding, selection and explosion;
  22 records specify explicit model.explode vectors. Other parts use radial
  displacement, which is not a validated disassembly sequence.
- Only four part records have nonempty fsm_sources. Existing part numbers,
  dimensions and explanations need a provenance audit before being called verified.
- The historical manual archive and raw knowledge captures were absent at audit.
  Restored the factory-manual ZIP from the existing project URL, verified its CRC
  and extracted it locally during this restart. Raw KB captures remain absent.
- CAD export depends on an absent .venv-cad and absent Claude plugin script.
  Blender is not on PATH or at the documented macOS application path.
- docs/NEXT-SESSION.md describes an older, removed 2D application. Current entry
  point is scripts/serve.py with viewer/. Historical progress is not runtime QA.

These are filesystem/code checks, not visual or dimensional certification.

## Modeling decision

Retain build123d/OpenCASCADE for dimensioned mechanical solids, STEP as an
editable interchange artifact, Blender for body surfaces/materials/presentation,
and Three.js with GLB assets for the browser. Replace the external-plugin export
dependency with a repository-owned, version-pinned exporter. Validate unit and
axis conversion against known dimensions before regenerating existing assets:
the current pipeline has an inch/model-unit and 1000x display-scale convention.

Geometry detail and evidence quality must be independent. For each important
dimension store value, unit, source/page/figure, applicability, uncertainty and
one of measured / published / inferred / unknown. Preserve competing claims.
A STEP solid or a detailed mesh is not inherently a faithful replica.

Build a vehicle → system → assembly → component hierarchy with stable IDs,
local coordinate frames, mating references, rotation/translation axes, motion
limits, and explicit explode stages. Keep assembled transforms authoritative;
explosion is a reversible display transform. Model housing internals separately.
Cutaways must expose actual modeled internals rather than imply absent detail.

## Research acquisition

1. Restore the exact-configuration factory manual and preserve original figures,
   page paths, retrieval time and content hashes. Reconnect inventory references.
2. Expand through Ford parts catalogs, wiring diagrams, TSBs, transmission rebuild
   literature and dimensioned component manufacturer drawings. Record application
   ranges and distinguish superseded/service part numbers from original numbers.
3. Discover relevant threads on Ford Truck Enthusiasts, FordSix and other owner
   communities. Capture complete accessible threads with pagination, post dates,
   author attribution, images and follow-up outcomes. Treat anecdotes as leads;
   verify specifications and procedures against applicable technical references.
4. Use a resumable crawl queue with URL canonicalization, content deduplication,
   per-domain rate limits, retry/backoff, robots/access checks and crawl logs.
   Record failures and access restrictions rather than claiming full coverage.
5. Ingest raw captures, create source pages with processed:false, extract distinct
   atomic notes, link them, then mark processed:true and run semantic backlinks.
   Preserve image/source usage information for eventual publication.

Measure coverage by system, component and unanswered question. A broad archive
is valuable, but page count alone does not establish useful or correct coverage.

## First deep assembly (owner selected: engine)

Keep the existing whole-truck context while rebuilding the engine around sourced
dimensions. Begin with block, head, crank, six pistons/rods and cam/valvetrain;
then timing gears, lubrication, induction, cooling and accessories. Separate
castings, covers, seals, bearings and relevant fasteners. Validate interfaces
before polishing materials. The owner selected engine first on 2026-09-22.
See [COMPONENT-MODEL.md](COMPONENT-MODEL.md) for the binding part-by-part scope,
assembly architecture and acceptance criteria.

The first reviewable milestone must provide:

- Assembled, cutaway and staged exploded views with selectable individual parts.
- A slow, scrubbable four-stroke animation with verified crank/cam relationship,
  firing sequence, piston travel and valve events; simplified events labeled.
- A part panel explaining function with direct evidence links and uncertainty.
- One sourced symptom-to-test diagnostic flow, with conditions, expected result,
  branches and hazards tied to the relevant component. Do not invent thresholds.
- Multi-angle comparison against references, dimension/fit checks, reproducible
  exports and a browser check for selection, visibility and reversible explosion.

Repeat for the M5OD-R2 with verified shafts, gear pairs, synchronizers, selector
mechanism and gear-dependent power flow. Attractive gear meshes alone are not
evidence of a mechanically valid transmission.

## Physical evidence needed

Confirm actual engine/transmission/axle identifiers, wheelbase and modifications.
Use reference/photos and docs/SHOT-LIST.md for photographs with scale references.
Prioritize mating dimensions, bolt patterns and accessible major envelopes.
Hidden casting passages and exact surface geometry may need drawings, a spare
part, measurement or scanning. Keep such gaps explicit and continue work on
documented assemblies while gathering those references.

## Checked external starting points

- [Exact vehicle manual and offline download](https://charm.li/Ford/1994/F%20150%202WD%20Pickup%20L6-300%204.9L/)
- [build123d native STEP/glTF export documentation](https://build123d.readthedocs.io/en/latest/import_export.html)
- [Blender glTF export and animation documentation](https://docs.blender.org/manual/en/3.0/addons/import_export/scene_gltf2.html)

Tool documentation establishes supported formats; it does not validate this
project's geometry or confirm compatibility with an uninstalled runtime.
