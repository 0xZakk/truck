# Upper intake, oil filler and coordinated interface candidate

## Contract

- Dependency: engine oil-cap issue #15 and the parent engine integration task. Root owns installed assets. This worker owns this document, `cad/engine/upper_intake_clearance_candidate.py`, and `reference/engine/upper-intake-topology-review.json`.
- Baseline source checkpoint: `5567d751abcf6a9bfac84bdf87ce0d7f0d4dac5c`; exact checked manifest and all relevant asset/source hashes are recorded by the candidate command. No shared geometry or manifest edits.
- Scope: isolated source-compared upper-intake contour, coordinated cap/neck station, throttle and EGR/EVP frame changes. Preserve all six lower runner stations and seven manifold studs. The root integration owner separately coordinates fixed-end EGR tubing.
- Units and frame: millimeters, assembly CAD coordinates, Z up. All returned solids are world placed. Existing occurrence IDs describe affected interfaces; no new installed occurrences are created.
- Critical gates: valid continuous intake and cover solids; six open runner passages; unchanged lower mating interface; sealing land, retention, complete cap withdrawal and all twelve rocker phases; all affected parts against the current assembly; honest disclosure of inherited collisions and disconnected routes.
- Thresholds: 0.1 mm³ is the existing numerical overlap audit convention, not a strength or leak tolerance. Motion contact threshold is 0.002 mm. Mesh broad-phase bounds expand0.2 mm, then exact CAD decides overlap. No thresholds are lowered to accept a trial.

## Evidence ledger and chosen topology

The actual Ford intake installation drawing, Ford exploded parts drawing, used Ford upper-manifold specimen photo, a1994 owner's exposed throttle flange, the exact local1994 manual and both photographs of this truck were inspected. URLs, application limits, original-image hashes and local manual paths are in `reference/engine/upper-intake-topology-review.json`. No source images are redistributed, and no AI-generated search captions are used as evidence.

| Feature | Evidence | Classification / limit |
|---|---|---|
| Compact common plenum and six curved runners spreading toward a longer lower flange | Ford1987 installation drawing and actual specimen | Supported topology; drawings are undimensioned comparisons |
| Outward runner spread at both ends | Actual specimen photograph | Supported visible topology; perspective prevents precise metric tracing |
| Direct twin-port front flange, separate gasket and four throttle fasteners | Ford installation/parts drawings, exact1994 V5652-D and1994 exposed-flange photo | Supported; no long front feed neck is shown |
| Seven upper-to-lower studs and separate castings | Exact1994 service text | Verified application architecture |
| UpperE7TZ9424A / lowerE7TZ9424D | Exact1994 parts information | Service identity, not an engineering drawing |
| Exposed cap ahead of the plenum, close to cover front | Both owner bay photographs | Owner-specific relationship; no calibrated coordinates |
| Plenum X-200 to+200; centerY25/Z490,145×90 section | Chosen coherent trial | Inferred dimensions; front/rear and lateral/height datums remain unmeasured |
| Cap/neck X300 instead ofX240 | Owner-landmark proportion estimate | Inferred station; cap dimensions are unchanged |

The cap center now sits67 mm behind the modeled cover frontX367, approximately one69.09 mm comparison cap diameter. It sits100 mm ahead of the proposed plenum front, approximately1.45 cap diameters. Those ratios are rough consistency checks against the owner views, not measurements of the truck. Existing Y25/Z490 plenum coordinates are retained provisionally because the photographs do not uniquely resolve their lateral/height components; the audit checks their mechanical coherence.

The original trial kept rearX-367 to avoid disturbing the EGR interface. Inspection of the actual specimen showed why that was inadequate: it produced weak rear runner spread and preserved an unsupported full-length datum. The revised plenum is centered longitudinally and its terminal runner stations are `[150,90,30,-30,-90,-150]` mm. The six lower port stations and mating flange remain unchanged. No cap-shaped notch or shortened cap stem is used.

## Coordinated interfaces

| Affected interface | Proposed change | Preserved relationship / remaining work |
|---|---|---|
| Throttle assembly, hardware, moving mechanism, IAC, TPS, bracket and shield | Translate **(-167,0,0) mm**, no rotation | Complete descendant set moves together; internal interfaces remain rigid |
| EGR valve, EVP sensor, intake gasket and two mount bolts | Translate **(+167,0,25) mm**, no rotation | Rear valve-to-plenum interface moves coherently |
| Cap and seal | Translate **(+60,0,0) mm**, no rotation | Pilot shape, seal and assumed4.5 mm pitch preserved |
| Cover and female neck | Regenerate oldX240 roof opening closed; cut opening and attach neck atX300 | Single continuous cover solid; no separate plug or duplicate opening |
| Regulator vacuum port | Retain `(0,-47.5,460)` | Existing opening location retained; nearby routes still audited |
| Six lower runner axes, lower mating face, seven studs | No change | Preserves current lower manifold/rail datum dependency |

Fixed-end EGR routes must be adapted; translating the valve alone does not connect them. Exhaust tube `END` moves from `(-412,25,434)` to `(-245,25,459)`, while `START=(-315.688,-180,230)` and collector face `(-285.688,-180,230)` stay fixed. Move the valve union nut with the valve; retain the manifold fitting. The vacuum hose keeps its EVR start `(-420,-41,410)` and moves its valve terminal from `(-412,85,537)` to `(-245,85,562)`.

The new EGR inlet is above the cover. Over the Z413 roof, a bare18.796 mm tube requires centerline above422.398 mm before any positive margin; a25 mm sleeve requires above425.5 mm. The original sleeve stops short of the fitting, so its actual trim must be considered. Those are geometric exclusion limits, not Ford routing dimensions. Root owns the coordinated reroute proposal in `cad/engine/intake_egr_routes_candidate.py`; its four actors are included in this audit. The inferred25 mm EGR lift places the diaphragm atZ544 above theZ535 plenum roof, consistent with the undimensioned exploded comparison, and retains the outlet within the plenum cavity. This does not establish a factory height.

## Delivery and reproduction

- API: `candidate()` returns `(intake_shape, six_runner_paths)`; `coordinated_cap_cover(cover)` returns `(new_cover, neck, cap, seal)` in world coordinates.
- Run `.venv-cad/bin/python cad/engine/upper_intake_clearance_candidate.py` from repository root.
- Ignored outputs: `cad/engine/generated/upper-intake-clearance-study/upper-intake.step`, `cover-with-relocated-neck.step`, `relocated-cap.step`, `validation.json` and `comparison.svg`.
- The report records its own input snapshot and guard. The older `oil-fill-neck-candidate-validation.json` remains a frozen historical failure against the old intake; this task does not rewrite it.
- Environment: repository CAD environment; actual versions are available from the neck study. Model/effort and token usage unavailable. No worker commit or PR.

## Validation and review

The earlier asymmetric467 mm plenum was a feasibility trial, not accepted geometry. Its stored checks do not validate this revised400 mm model. The final isolated audit passes its bounded geometry gates. It does not establish installed acceptance or factory fidelity.

| Gate | Current scope / status |
|---|---|
| Application / architecture | Source review PASS for compact plenum, direct flange, six fanned runners; precise dimensions inferred |
| Coordinates / dimensions | Explicit estimates and coordinated transforms above; no OEM metrology claim |
| CAD / export | PASS: valid STEP roundtrips; four watertight GLBs, maximum bounds error0.000027 mm |
| Visual fidelity | Actual source images inspected; actual CAD comparison and neck section inspected; casting ribs/boss details remain omitted |
| Attachment / sealing / fluid paths | PASS bounded geometry: six passages, flange, cap retention/seal and all five EGR contact pairs; nominal fits are not physical sealing proof |
| Motion / service removal | PASS:181 phases,4344 cap/neck-rocker pairs; minimum1.34751 mm. Continuous0–22.5 mm cap withdrawal enclosure clear |
| All-neighbor behavior | PASS:584 exact pairs and93,482 broad-phase exclusions across718 definitions/1322 occurrences; no introduced or inherited overlaps in this affected scope |
| Learning / diagnostics | This document explains conflict and dependencies; viewer learning UI NOT RUN |
| Browser integration | NOT RUN: isolated candidate, not installed |
| Reproduction / independent review | Commands and hashes retained; parent review pending |

## Tracking and restart

No installed acceptance is claimed. Finish the current report, inspect every introduced overlap and compare the actual CAD views against the cited primary images. Resolve coordinated EGR routes and any newly affected neighbors, then repeat affected checks against the final frozen input set. The root integration owner decides promotion and browser validation; a clearance pass alone never establishes factory fidelity.

## CAD calculation regression

A native translated helical cap/neck Boolean incorrectly returned zero straight-pull interference at the proposedX300 station. Exporting and reimporting the world-coordinate solids restored149.912 mm³ interference for a1.125 mm pure pull, while matching screw removal stayed below0.1 mm³. The checker now bakes every exact-audited posed solid through STEP and asserts valid solids, unchanged solid count, bounds within0.01 mm and volume within0.1 mm³. Earlier native zero-overlap results are not promoted as acceptance evidence. The oversized-bore negative control remains required.

The revised command additionally exports/reimports individual GLBs and a combined candidate mesh, compares their bounds to CAD and checks watertightness. Complete cap withdrawal uses a conservative swept enclosure against every current occurrence; the cover joint is checked by matching screw motion separately.

## Current interface limitations

The source-compared contour remains a coarse casting candidate: top ribs, local bosses, wall-thickness distribution and exact runner sections are not reconstructed. The proposed cap station and400 mm plenum are numerical estimates, while the visible compact body, direct twin-port flange and two-ended runner fan are source-supported topology. Production oil-neck construction and thread pitch remain unknown;4.5 mm is the unchanged illustrative mating assumption.

The revised tube and valve union each touch the EGR body with no volumetric interference. The controlled-vacuum hose retains the inherited2.05 mm bore over a2 mm nipple radius, initially leaving0.05 mm radial clearance. Root revised the assumed terminal bore to2.0 mm for nominal fitted contact. This represents an idealized installed surface; it does not establish hose compression or a vacuum-tight seal.

## Isolated integration staging

Additional owned files: `cad/engine/intake_cap_coordination.py` and `scripts/stage-intake-cap-coordination.py`. The adapter accepts the shared exporter API through `install(define, add, group, definitions, occurrences, assemblies, shapes, mechanism)`. Run `.venv-cad/bin/python scripts/stage-intake-cap-coordination.py` only after the candidate report has every bounded gate true and its input hashes match. This command writes only `cad/engine/generated/intake-cap-integration-stage/`; it does not install anything.

The adapter changes eight definitions, adds the separate `oil-filler-cap-seal` occurrence and preserves existing stable identities. It translates the throttle, EGR valve and EVP assembly frames rigidly, preserving their internal motion and attachments. Cap and EGR gasket/bolt occurrences receive explicit corresponding local translations. Each rebuilt world solid is converted through its final occurrence pose inverse before export, so the existing cover’s nonzero origin is preserved. The staged checker verifies all original occurrence frames, excludes unrelated inventory changes and compares exported world solids directly against the audited candidate.

The root integration owner must review/apply the staged assets, add the adapter hook after all affected base builders, then rerun installed neighborhood and browser checks. The revised adapter normalizes reviewed baseline or target frame coordinates to absolute target coordinates. It compares the incoming cover to hashed legacy and coordinated solids before modifying it; coordinated geometry is retained. Unknown frames, ancestors, cover geometry or source hashes fail closed. A separate seal is upserted exactly once.

## Final isolated results

Manifest checked: `bfab1f2596991d27fe5e52e90f02d070eb034f9de8c2cd72d3dd44666d6c8bb9`. Report SHA-256: `dff419c93d029e5c5c04b8cd42704f36d31f1dd02e9454dc48725028741167e9`. The complete report is retained as `validation_snapshot` in the tracked topology ledger as well as the ignored generated report. Before/after source, manifest and used asset hashes match.

All six bounded gate values are true. The report remains `COORDINATION_REQUIRED` because this is an isolated candidate awaiting installation and browser review. The straight-pull interference is149.912 mm³; an oversized bore removes it completely. Eight matching screw samples stay below0.000034 mm³ overlap. The lowered-cap negative produces2210.697 mm³ interference. A seated two-cylinder enclosure contains the cap and seal exactly; its axisymmetric extension proves the entire0–22.5 mm withdrawal travel, including all rotations, clears current neighbors. It does not prove hand/tool access or a later carrying path.

`comparison.svg` shows the old and proposed manifold with the same proposed cap station, avoiding a hidden coordinate change between panels. `neck-section.svg` is an actual CAD cutaway through the new axis. Source comparison supports topology but still exposes missing casting ribs/bosses and unmeasured dimensions. The exported mesh bounds/watertight checks pass; final browser inspection belongs to the integration owner.

## Staged delivery result

The stage-only command passed with **719 definitions /1323 occurrences**, adding only the separate seal. It checked all1322 prior occurrence frames;67 occurrences receive the intended coordinated movement. All eight staged world solids have **zero symmetric volume difference** from the audited candidate. Maximum staged GLB bounds error is0.036466 mm. Unsmooth shared-export meshes retain coincident shading vertices; closure is checked after a0.00001 mm positional weld, with raw and welded counts disclosed and no face filling or asset rewriting.

Tracked staged report: `inventory/engine/intake-cap-coordination-stage-validation.json`, SHA-256 `d0b3f0c018d9e8c6abe310c36bb188dc6b00768bccebe9d447abff233b7e135c`. The staged manifest source ledger hash was checked against the final tracked ledger. No canonical assets, manifest, assembly builder or viewer files were changed by this worker. No commit or PR was created.

Reviewer: root integration owner; final independent installation/browser verdict pending. Running processes: none. Next action: review the eight staged definitions, three assembly-frame deltas, explicit occurrence changes and separate cap seal; apply through the root-owned guarded installer, then check installed geometry and actual browser meshes. Token usage and model effort are unavailable.

## Guarded promotion and replay follow-up

The first stage and report above are historical. The revised adapter uses `reference/engine/intake-cap-frame-contract.json` to bind three assembly frames, four explicitly moved occurrences, their ancestors and reviewed cover states. Both required reference solids are generated artifacts under `cad/engine/generated/intake-cap-contract/`; include them in the matching private CAD artifact archive. Their hashes and the geometry source hashes are in the tracked contract. They are project CAD, not purchased manual images.

Replay checks (`scripts/check-intake-cap-replay.py`) pass for a twice-applied coordinated state and for a mixed partial refresh that restores the reviewed legacy cover and capX240 while retaining coordinated neighboring groups. Metadata normalizes identically, all eight world solids match, and no second seal is added. An unreviewed cover and capX301 are rejected. This is exact state recognition, not a heuristic based only on cap station or seal presence.

Promotion sequence from repository root:

```sh
.venv-cad/bin/python scripts/check-intake-cap-replay.py
.venv-cad/bin/python scripts/stage-intake-cap-coordination.py
.venv-cad/bin/python scripts/install-intake-cap-coordination.py
# Integration owner, after reviewing the passing stage:
.venv-cad/bin/python scripts/install-intake-cap-coordination.py --apply
.venv-cad/bin/python scripts/check-intake-cap-coordination-installed.py
```

The default installer performs read-only preflight. Explicit `--apply` checks source/evidence, candidate inputs, the exact canonical baseline and all staged hashes; it then replaces the eight STEP/GLB pairs and manifest. Each file replacement is atomic; the group has rollback coverage if any write or installed validation fails, including the installation records. This is not a filesystem-wide atomic transaction. Isolated failure injection verifies restoring old bytes and deleting newly created files after both mid-write and post-check exceptions.

The installed checker binds the eight actual valid STEP solids and all67 moved-frame records to the reviewed stage, along with evidence and source hashes. It deliberately requires the exact reviewed manifest; run it immediately after promotion. Later learning/metadata edits produce a new manifest and must be recorded as a later checkpoint, not described as covered by the old manifest hash. The source `full_engine.py` is not globally bound by this candidate or stage report, so adding the adapter hook does not require pretending to refresh historical geometry evidence. Pass explicit mechanism metadata and invoke after all affected base builders. Existing geometry sources and the frame contract remain guarded.

The new installer/checker/control files are owned by this delivery; no canonical builder, assets or manifest have been edited by this worker. Relevant tracked records: `intake-cap-replay-validation.json`, `intake-cap-promotion-transaction-validation.json`, `intake-cap-promotion-controls-validation.json` and `intake-cap-coordination-promotion-stage-validation.json` under `inventory/engine/`. The old `intake-cap-coordination-stage-validation.json` remains preserved.

Final promotion freeze: staged manifest SHA-256 `36e05dfee7ea0ee12761295851c8fbe804ea0d3a516502e069f1059e77bc131b`; staged report SHA-256 `90b8fad1ef445e68d172f017a29c579c7d76a59adfa5612c4138952424fc5767`. Read-only promotion preflight, isolated installed-checker mirror, corrupted-mesh and shifted-frame controls, and rollback controls all PASS. The mirror reports are explicitly simulation evidence, not an installed acceptance claim. No running processes remain.
