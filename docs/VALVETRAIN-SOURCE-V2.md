# Source-sized valvetrain candidate

This candidate replaces the earlier undersized valve/pushrod envelopes with a coordinated all12-station layout. It is a teaching assembly constrained by catalog replacement dimensions, **not a scan, verified casting, installed-part identification, or exact factory cam profile**. Do not install until its all12 candidate audit and the integrated engine audit pass.

## Evidence and dimensions

- Melling V1505 intake: length120.6246mm, head45.2882mm, stem8.6868mm; V1504 exhaust: length120.65mm, head39.5986mm, stem8.6868mm. See `kb/sources/melling-valve-progressive-size-chart-2025.md` and frozen PDF in `reference/engine/valve-layout/`.
- Application-confirmed MPR-306 pushrod: overall257.556mm, diameter7.9248mm. The modeled drilled spherical ends require250.00335443437204mm ball-center separation to preserve the actual STEP end-to-end extent. End radius and oil bore remain assumptions. Earlier first-stage nominal234.2mm envelope was23.356mm shorter than the catalog constraint.
- JB-900 lifter: primary manufacturer2.000in/50.80mm body length and.874in diameter; SYB-38 cam/lifter kit lists12JB-900. Manufacturer response does not specify socket height. Crower1.715in and Howards2.018in seat heights remain unresolved comparisons and are not used to choose this CAD datum.
- Factory1994 spring data: intake41.656mm and exhaust37.338mm closed load-test heights; guide bore midpoint8.73252mm. Six turns,2mm wire radius,13mm helix radius and end form remain illustrative. Clipped ground faces provide actual head/retainer contact; this is not a calibrated spring force model.
- SYB-38 catalog scalar cam lift/net lift constraints remain in use, but the smooth cam law is an explicit teaching approximation; installed cam identity is unknown.

The source-sized solver preserves the previous valve-seat/deck/cam datums, moves the rocker cup/fulcrum and associated head pedestals coherently, and derives the rocker angle from constant pushrod ball-center distance. Intake and exhaust share a single rocker solid; their slightly different valve lengths produce slightly different rest angles. Lifter internal offsets, absolute cam/deck/station coordinates, head castings, guide/retainer profiles and rocker construction remain assumptions. Shortening the body changes the inherited illustrative lower floor thickness from5mm to3.8mm. No manufacturer hydraulic seat-height convention is claimed.

## Owned files and composable hooks

`cad/engine/valve_source_layout.py` is the geometry/kinematic authority; `valve_dimensions_candidate.py` supplies source-sized valve and drilled pushrod geometry. `valve_source_integration.py` exposes:

1. `replacements(current_shapes, manifest)`: takes **current accepted first-stage** head/lifter/valve solids and returns11 changed definition solids. Head adaptations preserve unrelated current geometry; cam/rear-journal/gasket corrections remain inherited. Valve extension is deliberately not idempotent: do not pass already source-v2 valve solids.
2. `annotate_manifest(manifest)`: idempotently sets all12 rest datums/roles and separate intake/exhaust spring definition IDs. Register those two definitions, regenerate actual bounds/volumes/STEP/GLB, and retain source/evidence qualifiers.
3. `apply_valve_transforms(manifest, poses, crank_degrees)`: dispatch once from the shared transform authority when `valvetrain_model == 'source-sized-v2'`; it never calls that authority recursively. Do not also run first-stage valve transforms. This applies the same source-v2 roles used in browser motion.
4. `occurrence_shape(occurrence, definition_shape, crank_degrees)`: generates the correct compressed spring before the shared placement transform. All other definitions pass through. Use this in assembled STEP export and exact-check placed shapes, including at crank0 because other cylinders are lifted then.
5. `candidate_transforms` is isolated-check convenience only: strips motion metadata before calling a frozen base authority, then applies source-v2 once. It is not the live integration path.

`viewer/engine-valve-source.js` exports `sourceValveState`, `sourceOccurrencePose`, and `sourceSpringMeshData`. Reset each object to its manifest rest pose every frame. The returned `translationEngineCad` is a global engine-axis offset in millimetres: map CAD(X,Y,Z) to display(X,Z,-Y), divide by1000, and add it without rotating by the object's rest quaternion. Apply `rotationXDeltaRad` after its rest quaternion. Springs use `springHeightMm` and the ground-ended tube mesh; do not scale wire thickness. Tube meshes are display-space metres/Y-up. Do not substitute this helper for first-stage geometry without regenerating corresponding source-v2 solids and rest transforms.

## Reproduction and checks

`build-valve-source-all12.py --baseline PATH --expected-manifest SHA` freezes the accepted baseline and builds only the owned `cad/engine/candidates/valve-source-all12/` directory. Baseline manifest6b11c0f874bb53638b0e7fd0f477f6b7d5fca4df928bcbc918b37c98cb01d94f; its697STEP files include the three supplemental acceptedV8pan definitions. Candidate GLB paths are intentionally not regenerated by this CAD-only builder and must not be served as an installed site manifest.

`check-valve-source-all12.py` audits changed occurrences against every frozen engine occurrence. Unchanged pairs inherit the accepted static baseline; this is a delta audit, not a claim of continuous whole-engine clearance. `--angles` controls sampled phases. The separate representative two-station report is PASS at18poses:1407 exact intersections,288 contacts,0failures, including negative tangent-probe controls. Actual representative STEP section render is `cad/engine/candidates/valve-source-layout/qc-render.png`; visually inspected at rest/peak.

`export-valve-source-api-fixtures.py` and `check-valve-source-api.mjs` test216phase/cylinder/kind combinations,19,224 comparisons including actual transformed local basis points against Python CAD placement (max error1.14e-13), and24,564 browser spring triangles with closed manifold edges, consistent winding, positive volume and exact ground bounds. These tests establish cross-language agreement, not new factory evidence.

## Browser spring performance

Use `viewer/engine-valve-source-spring-cache.js` for animation. `sourceSpringMeshDataFast(height, N, R)` caches at most32 side-connectivity templates and evaluates positions/normals at the exact requested height. It re-triangulates the two small ground caps each update: keeping old cap diagonals can invert triangles as their concavity changes, so that attempted shortcut was rejected. There is no height quantization, wire scaling or stale ground plane.

`prewarmSourceSpringCache(96,12)` optionally fills common templates while yielding between batches. Recommended whole-engine resolution is96×12; isolated detail can use192×16. In a local Node benchmark regenerating all12 springs at arbitrary crank phases, warmed CPU geometry time averaged0.87ms/frame (p951.36ms) at96×12 and2.14ms/frame (p957.22ms) at192×16. These figures exclude THREE allocations and GPU upload. Reuse existing BufferGeometry attributes when their lengths match; recreate only when clipped triangle count/index mode changes. Both canonical and accelerated source-v2 meshes are non-indexed: use `geometry.setIndex(null)`, not a BufferAttribute wrapping null.

Accelerated output matched the canonical meshes across578height/resolution combinations within5.4e-17m positions and6.2e-15 normals. Canonical sweep separately checked290meshes/1,228,876 triangles for manifold closure, consistent outward winding and ground bounds. Hashes and code snapshots were refreshed after adding optional recipe capture to the canonical helper; the existing216phase CAD/JS fixtures still pass unchanged.

## Current candidate validation

All12 source-v2 manifest SHA-256: `8ba89d0295ee040ab0709dff89794c361519c803016cbebd767a0dceba6dd630`.

- Static delta:242changed occurrences,1,078exact intersections and84contacts,0failures. Every changed occurrence was checked against every frozen engine occurrence after conservative bounds filtering.
- All12 positive motion contacts:18crank poses,1,728contacts,864negative tangent-witness controls,0failures.
- Pedestal/shim/fulcrum supports:24contacts,0failures.
- Saved-STEP valve/pushrod/lifter dimensions and both ground spring envelopes:PASS.
- Additional whole-engine collision poses are recorded separately in `motion-validation.json` when that run completes; contact tests alone do not establish collision clearance.

`valve_source_evidence.annotate_evidence` updates public source links/constraints and removes superseded first-stage pushrod-length warnings. It is separate from the geometric candidate manifest so ongoing audits remain bound to an immutable manifest hash. Call it during the real regeneration and perform the integrated audit on that resulting manifest.
