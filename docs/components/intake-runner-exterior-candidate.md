# Component contract and handoff: upper intake runner exterior

## Contract

- Issue#36, engine parent#1; contributor cap_interface_finish, integration owner root. Root owns shared assembly and browser.
- Baseline commit/manifest: exact hashes in `reference/engine/intake-runner-exterior-review.json`; installed detailed upper intake is the geometry input. Parent distributor promotion may change unrelated manifest fields; intake asset hashes govern this first feasibility study.
- Scope: isolated source-compared runner exterior, now built and reviewed; current-context audit remains separate. No global datum, support-bracket, current air-volume or mounting-interface changes.
- Owned new files: `cad/engine/intake_runner_exterior_candidate.py`, the four `scripts/*intake-runner-exterior-*.py` check/render tools, matching reference/reports and this handoff. Prior frozen exterior and coordinated intake files remain untouched.
- Evidence: actual owner bay photos, Ford1987 installation figure and later-marked replacement specimen photos, with explicit applicability limits. Wide flattened exterior faces with rounded edges are supported; exact section/radii are inferred. Existing circular air passages are protected, not declared factory geometry.
- Units/frame: millimeters, current intake world CAD frame, Zup; preserve occurrence/group transforms. Section transverse axis projects engineX onto local runner normal plane.
- Proposed profiles: rounded rectangles tapering from within existing near-flange envelopes to estimated52–58mm broad mid-arch faces, then back into current roots. Initial depth44–46mm and edge radii are estimates; maintain all six separated arches.
- Protected interfaces: complete lower flange/seven studs, six air passages and common plenum cavity, direct throttle flange/ports, EGR flange/port, regulator vacuum seat, plenum wall and cap withdrawal envelope. No inferred PCV port is added.
- PCV coordination: pump worker confirms no accepted receiver datum; arbitrary(-100,25,445) trial rejected. Preserve actual current vacuum interface and leave central plenum wall unchanged. Any new receiver requires separate source/data coordination.
- Required inputs: current detailed intake STEP, existing parametric runner paths and air volume, local comparison evidence. Private/reference originals excluded from release.
- Planned checks: cheap single-solid loft/union feasibility; old-versus-new protected-region differences and no new air blockage; six independent runner sections; later whole-neighbor/cap/motion and actual GLB comparison. Overlap convention0.1mm³, bounds0.15mm; no threshold reductions.

## Evidence ledger

See `reference/engine/intake-runner-exterior-review.json`. The F5TE-marked seller specimen is a later-revision comparison, not exact1994 identity. Ford's earlier figure independently corroborates broad runner faces; owner photographs partly corroborate visible form but do not measure section depth.

## Delivery / validation

The initial research ledger is retained as the proposal snapshot. The implemented inferred stations are `(path fraction, width, depth, corner radius)` in millimeters: `(0.025,34,34,9)`, `(0.14,50,44,9)`, `(0.32,56,44,9)`, `(0.56,56,44,9)`, `(0.74,54,46,9)`, `(0.90,34,34,9)`. Inset end profiles lie inside the original tubes. This is an exterior silhouette study; the additional material is not a measured casting wall or production mass.

The final loft adds only metal outside a protected R21.5 runner core and the existing plenum cavity. Its 0.5mm overlap with the old R22 exterior fuses the added faces while preserving the original R16.5 bore surfaces. The resulting one-solid CAD passes all five protected-region symmetric differences at zero, adds zero air blockage, and has zero overlap with the checked cap withdrawal enclosure. Added volume is1,025,652.7199mm³. No thresholds were reduced.

Failed construction trials are retained under the ignored study directory: smooth varying-radius full shell, ruled invalid shell, and fixed-radius full shell. The full-shell approach returned apparently valid solids but inconsistent lower-flange/plenum Booleans, including null shapes. Those were failures, not accepted clearance results. STEP normalization and fuzzy diagnostics did not repair them. The protected-core skin construction resolved the checks without recutting coincident bore surfaces.

Root visually reviewed the actual exported baseline/candidate comparison and accepted the broad-face silhouette as closer to the observed casting. The fine comparison used0.035mm linear/0.045rad angular tessellation (1,541,722 candidate triangles). A subsequent0.07mm/0.08rad trial reduces the candidate to435,878 triangles/8,717,760bytes; both settings produce watertight meshes and0.0000135mm CAD bounds error. The fine reference is retained under `fine-tessellation/`. Root accepted0.07mm/0.08rad for the integration candidate, subject to browser close-up; preserve that setting and the8.72MB cost in promotion. No arbitrary mesh decimation is applied. Render files are `cad/engine/generated/intake-runner-exterior-study/mesh-comparison.{png,svg}`; the candidate is on the right. No conceptual or AI-created image is used.

Reproduce with the repository CAD environment:

```sh
.venv-cad/bin/python scripts/check-intake-runner-exterior-candidate.py
.venv-cad/bin/python scripts/render-intake-runner-exterior-candidate.py
.venv-cad/bin/python scripts/check-intake-runner-exterior-controls.py
.venv-cad/bin/python scripts/check-intake-runner-exterior-context.py
```

The first two reports are `inventory/engine/intake-runner-exterior-{candidate,render}-validation.json`. Candidate STEP SHA256 is `95fe3ffef2815fcc5e9812736cf1019e87d249c90b6bd6dce210a4ddc25ea04f`. Separate fault-control and current733 context reports must pass before promotion. The context audit binds all733 definitions/1341 occurrences and every canonical STEP/GLB with before/after hashes. It compares whole-manifold static geometry against the current scene, then checks the exact added material against actual regenerated cable and shaft-spring geometry at47 throttle poses, rigid throttle descendants, and12 rockers at181 phases. Unchanged baseline motion is inherited. This is a sampled sweep, not continuous motion proof.

The first context attempt stopped on nonconvergent adaptive mass integration for the unrelated fuel-return-coupling spring; code/log are retained under `failed-context-adaptive-neighbor`. The final audit binds the current733 static report (5,249 exact scene pairs, no collisions), verifies zero removed material, and permits an inherited static result only where the exact added-material bounds are disjoint from that actor. The spring lies more than50mm beyond the added material in X, so this says the revision cannot add interference; it is not a rerun whole-manifold spring result. Intermediate distance versions were interrupted because full-casting/helix solves were expensive; their code/logs remain archived. A separate enclosing-box diagnostic was empty but is not used as the acceptance proof. Nonconvergence, invalid geometry, and null Boolean failures are never reported as zero overlap.

Current733 context and independent fault-control reports PASS. Static broadphase covers1,340 other occurrences:248 exact rerun pairs,1 explicitly inherited unchanged coupling spring, and1,091 enclosure exclusions. All2172 rocker,517 rigid-throttle,235 regenerated cable-shape and47 regenerated shaft-spring pose pairs exclude against the exact added-material bound. The complete baseline-minus-candidate removed volume is zero. All bound inputs were unchanged before/after. This is a new-material motion check, not a fresh whole-engine motion acceptance.

The scoped adapter, installer and learning supplement are `cad/engine/intake_runner_exterior_integration.py`, `scripts/install-intake-runner-exterior.py`, and `inventory/engine/intake-runner-exterior-learning.json`. The adapter requires the durable checked baseline/candidate STEP fixtures in the ignored study directory, verifies their hashes, rebuilds the skins parametrically, and compares that result with the accepted candidate. Include those fixtures and frozen reports in the CAD release; no temporary path is required. It accepts only the reviewed detailed baseline or its exact runner-exterior successor, with the current identity world/local frame.

Stage/replay/promotion validation PASS. Parametric, accepted-versus-staged, repeat and partial-refresh symmetric differences are all zero. Changed frame/geometry, corrupt staged mesh and corrupt staged frame are rejected. Transaction failures at writes1/2 and during postcheck restore both existing and previously absent files. All1501 stage-check input hashes remain unchanged. The final rebuilt/exported stage has435,346 triangles/8,707,120bytes, is watertight, and has0.0000135mm bounds error. This small tessellation-count difference from the initial mesh occurs after exact-zero-difference parametric replay; the actual staged GLB was separately rendered and inspected. Installed and current viewer/browser checks are NOT RUN. No canonical writes or completion claim. Root owns any later promotion and must preserve the existing stable ID, occurrence transform, original flange/air geometry and export settings. Unknown exact1994 section dimensions, wall thickness, and PCV receiver remain explicit limits. Original photos/manuals are excluded from shared artifacts. Usage unavailable.


## Integration sequence (integration owner only)

1. Finish `scripts/install-intake-runner-exterior.py --stage` and `--test-promotion`, then review the frozen stage and all reports.
2. Add the runner adapter immediately after the existing intake exterior adapter in `full_engine.py`, and merge its `sources()` plus learning supplement. This builder file is not a candidate/context input; the hook does not require rewriting historical audit hashes. Preserve the preceding compact and detailed-baseline construction.
3. Run the installer without arguments for read-only preflight, then use `--apply` only after integration review. `--check-installed` binds the exact installed asset/manifest scope and the preserved historical static proof. Shared scene changes before application require a new current-context audit/stage.
4. Inspect the actual installed manifold at close range in the browser, including broad elbows, both end transitions, cap removal and surrounding runners. Existing unresolved support/PCV evidence remains open. Do not mark installed completion from the isolated report alone.

The installer uses the existing reviewed per-file atomic replacement/full-rollback transaction helper. Passed negative controls cover failed writes/postchecks, corrupted staged mesh/frame, unreviewed incoming geometry, and changed local placement. It stages only the single existing intake definition/occurrence plus source metadata: no new physical parts or group frames.


Frozen handoff commands:

```sh
.venv-cad/bin/python scripts/install-intake-runner-exterior.py
.venv-cad/bin/python scripts/install-intake-runner-exterior.py --apply
.venv-cad/bin/python scripts/install-intake-runner-exterior.py --check-installed
```

The first command is read-only preflight; only the integration owner runs apply. Actual staged mesh comparison: `cad/engine/generated/intake-runner-exterior-integration-stage/actual-stage-comparison.png` (baseline left, staged candidate right), with hashes in `render-binding.json`. The installer postcheck can take several minutes because it repeats exact geometry/rebuild checks; a passed check does not imply browser acceptance.

Frozen report SHA256:

- `cad/engine/generated/intake-runner-exterior-integration-stage/validation.json`: `1e48750d2d289ae004b2b486fe5e972eec193b78feca0d361f0f2c6ab9faae6c`
- `cad/engine/generated/intake-runner-exterior-integration-stage/installation.json`: `12a60b4772920e81282fe739ac72100352ac050985404fbeec31b19fe7590017`
- `inventory/engine/intake-runner-exterior-promotion-validation.json`: `a02b11c74c5236e05f5e43f5190a8c08ede4132da4ece0be7279c85a385eb3a6`
- `inventory/engine/intake-runner-exterior-context-validation.json`: `ccd9e009bc7356d43a44d52ffb22bb4fa86fec3f1bea3b34c355a40a3f75ef74`
