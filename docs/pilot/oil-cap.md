---
title: "The oil filler cap uses screw retention and a separate rubber seal"
---

## Candidate and evidence

This bounded pilot replaces the two-cylinder oil-cap placeholder with an EC743-style cap body and separate seal. Ford's current product page identifies EC743/F3AZ6766B and embeds the exact 1994 F-150 4.9 Gas application. Its top and underside photographs establish the scalloped grip, closed male screw stem, underside relief, and annular seal. They do not verify the installed truck's cap identity or factory dimensions.

[MotoRad MO100](https://motorad.com/part/MO100/) cross-references this Ford number and lists a 31.24 mm neck, 69.09 mm shell, 38.10 mm height, male screw retention, nonvented construction and a preinstalled rubber seal. Those dimensions size the **replacement comparison candidate only**. [Dorman 90005](https://www.dormanproducts.com/p-84374-90005.aspx) lists a materially different 0.5-inch height, whose measurement scope is unresolved. No dimension was averaged or labeled verified Ford metrology. Source records, exact Ford application extraction and capture hashes are in `inventory/engine/pilot/oil-cap/evidence.json`.

## Interface and acceptance

The cap occurrence remains at CAD millimetres `(240,-12,419)`. Its seal rests on the frozen cover's Z413 top; its hole remains centered at `(240,-12)` with radius17. No baseline file was edited. The cap's separate gasket touches the cap boss at Z416 and the cover at Z413. Flat-face contact proves only modeled geometry; elastomer compression, sealing pressure and material performance are unvalidated.

**Retention fails against the frozen baseline.** The cover contains a smooth 34 mm hole and no female thread. The comparison male thread is 31.24 mm major diameter, leaving 1.38 mm radial clearance, with no retention load path. The source-supported screw construction must not be relabeled as a successful bayonet fit. Thread pitch, profile, engagement length, grip contours, relief and seal dimensions are explicitly assumed. A future cover-thread reconstruction needs applicable measurements before this can become a production-accurate pair.

## Reproduction and integration

Run from the repository root:

```sh
XDG_CACHE_HOME=/private/tmp/truck-cache .venv-cad/bin/python scripts/pilot/oil-cap/write_evidence.py
XDG_CACHE_HOME=/private/tmp/truck-cache .venv-cad/bin/python scripts/pilot/oil-cap/build_check.py > reference/engine/pilot/oil-cap/build-check.log 2>&1
```

`cad/engine/pilot/oil-cap/oil_cap.py` exposes `Parameters`, `POSITION`, `parts(parameters)` and `build((define, add), parameters)`. Load the module by adding its directory to the import path (module name `oil_cap`). Remove the original oil-cap `define/add` pair in an isolated integration build and call `build((define, add))` inside the same closures context. Two definitions and occurrences are emitted: `oil-filler-cap` and `oil-filler-cap-seal`. Geometry is CAD Z-up millimetres; standalone GLBs map to metres `(X,Z,-Y)` like the shared exporter. The API passes normal source/gap metadata and preserves the existing parent and datum. Merge the source records and the keyed learning JSON into the isolated viewer's standard data loader. No shared builder/viewer is modified by this pilot.

STEP and GLB outputs live beside the module. `review.png` contains top, underside and frozen-cover views. `validation.json` records STEP round trip, volume, topology, watertight meshes, bounding dimensions, exact contact/intersection checks and a 15 mm broad-phase neighborhood with exact STEP checks. Baseline, builder and checker hashes identify evidence scope. This is a candidate handoff; viewer integration/browser acceptance remains the integration owner's task.

Render after the CAD checks using the bundled image runtime:

```sh
/Users/zacharyfleischmann/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/pilot/oil-cap/render.py
```

The closest static neighbor is the cylinder 1 intake rocker, at 1.3754 mm. This is **not a dynamic rocker-clearance pass**; its full travel and real production tolerances still need validation. The upper intake is 12.9 mm away in the frozen pose. CAD validity and zero interference cannot override those unresolved functional limits. Missing markings, photo-derived grip approximation and sharper shoulders keep the visual result provisional.
