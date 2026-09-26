# Upper intake exterior casting candidate

## Contract

- Parent: engine reconstruction; follow-up to the checked compact-plenum/oil-cap interface proposal. Root owns promotion, assembly hooks and browser review.
- Scope: isolated casting exterior only. Preserve all six runner bores, plenum air volume, lower flange/studs, direct throttle and EGR mating faces, vacuum opening and tested cap withdrawal clearance. No canonical edits or changes to frozen coordination files.
- Owned: `cad/engine/intake_exterior_candidate.py`, `scripts/check-intake-exterior-candidate.py`, this document, `reference/engine/intake-exterior-review.json`, and its scoped validation record.
- Baseline: compact candidate source and exact hashes recorded by the checker. Millimeters, existing world CAD frame, Z up. Numerical ornament/radius dimensions are inferred, never Ford drawing measurements.
- Planned features: soften the visible upper perimeter; reproduce two raised longitudinal border ribs and observed raised wording; widen/blend runner junction shoulders where the casting specimen shows broader roots. Do not add mounting bosses that would change a tested fastener seat. Any Ford word treatment is a font approximation, not a traced trademark outline.
- Evidence access: actual owner photograph, Ford installation/parts figures and public specimen photo previously inspected and hashed in the topology ledger. Restricted originals remain outside Git. Font files are local system dependencies, not redistributed.
- Checks: valid single casting and STEP roundtrip; unchanged protected interfaces and air volume; six open flow probes; whole-neighbor broad phase plus exact candidate intersections; continuous cap-removal envelope; bounds/watertight GLB comparison; actual CAD/mesh render beside described source landmarks. Numerical overlap0.1 mm³, bounds0.15 mm; no threshold reductions.

## Source observations

The owner photograph independently confirms the raised Ford oval/word and the two-line “ELECTRONIC / FUEL INJECTION” wording on the top face, with long raised border lines. The specimen makes the rounded cast shoulder and broad runner-to-plenum transitions clearer. Both are photographs with perspective; they provide visible topology and rough proportions, not calibrated millimeters. The Ford service figures support overall architecture but omit decorative casting detail.

The current flange studs remain fixed. Visible lower bosses in a specimen cannot be added by simply raising current fastener seats; that would require coordinated hardware/seat evidence and is excluded here. The vacuum-tree boss visible in the specimen also cannot establish a new port position relative to the current inherited vacuum interface.

## Delivery and review

Readiness: PASS isolated candidate and current722-definition/1330-occurrence stage. Root accepted the preview provisionally as a recognizable exterior improvement. Canonical promotion and final browser acceptance remain integration-owner actions. No canonical files were written by these checks.

The final generated `intake-exterior-study/mesh-comparison.png` is a depth-buffered render of the actual exported GLB triangles, with the original compact casting at left and revised casting at right. Its accompanying SVG adds labels. This replaces the preliminary painter-sorted preview, whose dark roof triangle was a renderer artifact. The final mesh has a closed roof.

### Delivered files and reproduction

Owned files additionally include `cad/engine/intake_exterior_integration.py`, `scripts/stage-intake-exterior.py`, `scripts/rebind-intake-exterior-stage.py`, `scripts/install-intake-exterior.py`, `scripts/check-intake-exterior-promotion.py`, and their exterior-prefixed validation records in `inventory/engine/`. Baseline commit was `fb2a1e756cf5e0d6ed925975312231406fce18ed`; concurrent integration changes are captured by exact input hashes rather than that commit alone.

Run from the repository root with the existing CAD environment:

```sh
.venv-cad/bin/python scripts/check-intake-exterior-candidate.py
.venv-cad/bin/python scripts/stage-intake-exterior.py
.venv-cad/bin/python scripts/check-intake-exterior-promotion.py
.venv-cad/bin/python scripts/install-intake-exterior.py
```

The candidate audit deliberately uses immutable719 coordination fixtures. All six definitions subsequently replaced by IAC/plate work have durable original STEP/GLB fixtures in `cad/engine/generated/intake-exterior-study/baseline/`: IAC armature, gasket, valve body; throttle housing, shaft and plate. `restore.json` records origin and hashes. Original STEP files were verified against the prior719-compatible audit; original GLBs against recorded Git blobs. These fixtures, the coordination stage, contract fixtures and generated candidate/stage exports must travel in the private CAD release. No temporary directory is a runtime dependency.

The two macOS system fonts and their hashes are explicit checker dependencies: Arial Bold and Brush Script. They are approximations and are not redistributed. Another machine must supply matching font files to reproduce these exact artifacts, or regenerate and review a changed-font candidate. Restricted photographs/manuals also remain outside Git; source URLs, identities, visual observations and hashes are recorded in the ledger.

### Quality gates and limits

- CAD: valid single solid; STEP roundtrip passes; original reconstructed casting agrees with the immutable compact stage.
- Interfaces: zero symmetric difference in all four protected regions: lower flange/studs, throttle pad/ports, EGR pad/port, and the actual regulator vacuum seat/bore protected by a radius10mm disk. All six radius12mm runner probes remain open and no original air volume is blocked.
- Service: the full axisymmetric cap withdrawal envelope has zero overlap. Cap/thread/neck dimensions remain the earlier explicitly inferred educational interface; this update adds no factory-thread claim.
- Historical scene:239 exact static pairs,1083 broad-phase exclusions; no introduced conflicts. Motion:2540 rocker/throttle pairs, with minimum added-material broad-phase separation4.223158mm. The spring's conservative continuous0–90degree envelope also clears the casting.
- Current scene:246 exact static neighbor pairs,1083 exclusions; no new or worsened overlaps. Current12 rigid throttle descendants, including plate screws, pass46 poses/552 pairs. Posed actors are STEP-baked before exact Boolean checks to avoid the previously demonstrated native-placement anomaly.
- Negative controls detect a plugged runner (8553.719492mm³ obstruction), a cap-envelope intrusion (4188.707689mm³), and a deliberately shifted spring envelope. These are geometric sensitivity checks, not physical flow or fatigue tests.
- GLB: actual bounds agree with CAD within0.000014mm and the welded inspection mesh is watertight. Candidate export removed one exactly zero-area triangle with repeated vertex indices after float32 conversion; no hole filling or tolerance change. The separate staged shared-exporter mesh required no removal and contains46546 triangles.
- Appearance:6mm upper rounding,3mm border width, raised heights, root-loft radii and font outlines are inferred. Source photos establish the visible features, not these dimensions. Casting texture, exact wall distribution, mounting-boss profiles and vacuum-tree architecture remain incomplete.

Numerical overlap acceptance is0.1mm³; mesh-bounds checks are stricter than0.2mm. No gate establishes production sealing, strength, airflow performance, calibrated Ford dimensions or exact lettering.

### Source-only rebind and promotion

The first current-stage audit bound manifest `62dcb37f469b21a93a74baa1fb81e44b2c7d69c8344d1cf18c667ce72a4fdff7`. A concurrent source-summary registration changed it to `f1dc26ba64eb0ba1e8fede4ef42e23a5ae3e288dbeae3cc4b2558cf4148a4a70`. The one-time rebind script reconstructed the exact earlier manifest hash, proved every non-source field equal, restricted source changes to the registration's declared IDs, and reverified every neighbor asset hash. It archived the original stage and audit under `intake-exterior-integration-stage/historical-source-context/`. Reusing that exact geometry audit is explicit; it is not represented as a new sweep.

Promotion is explicit and belongs to the integration owner:

```sh
.venv-cad/bin/python scripts/install-intake-exterior.py --apply
.venv-cad/bin/python scripts/install-intake-exterior.py --check-installed
```

The default mode is read-only. Promotion binds candidate inputs, evidence, fonts, stage/source/neighbor hashes, the original casting bytes and exact current manifest. It replaces only the intake STEP/GLB and manifest metadata, preserving all frames/counts. The already fault-tested rollback helper includes asset, manifest, installation-record and postcheck-report writes in one rollback scope. An isolated installed mirror passes, and corrupt-mesh and shifted-frame negative controls are rejected. Run the installed check before subsequent assembly edits invalidate its exact context.

For regeneration, call `intake_exterior_integration.install(...)` after the existing compact intake/cap coordination adapter, and merge `intake_exterior_integration.sources()` into assembly sources. The adapter recognizes only the reviewed compact casting or its exact detailed successor, reconstructs the detailed solid fresh, and preserves its current transform. Unknown incoming geometry fails closed. Full-engine hook and repeated whole-engine build verification are NOT RUN here and belong to root; this delivery does not edit the shared builder.

Final acceptance still requires root's installed browser inspection and release capture. The report hashes are the authority for the frozen stage; this document does not supersede stale-input failures.
