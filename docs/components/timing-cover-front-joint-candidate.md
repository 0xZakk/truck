# Component contract and handoff: timing-cover-front-joint-candidate

## Contract

Issue #32, Engine #1. Integration owner root; contributor air_cleaner_candidate. Baseline `a93b5bc1732f41651403ff15d821b52ab3d57d82` on `engine/exhaust-timing-joints`. Root accepted the central aperture registration as an explicitly estimated feasibility hypothesis, never a measured factory transform.

Owned files: `cad/engine/timing_cover_front_joint_candidate.py`, `scripts/check-timing-cover-front-joint-candidate.py`, optional renderer, `reference/engine/timing-cover-front-joint-review.json`, `inventory/engine/timing-cover-front-joint-validation.json`, this handoff, and isolated generated `timing-cover-front-joint-candidate/`. No canonical/shared edits. Block land is future casting material, not an independent installed part.

Use scale 0.2622330227, source crank (588.5373742,930.4751088), rotation −0.03982355 degrees. Fix crank YZ(0,0), seal X414, block model plane X373 and cover rear plane X373.8. Both current and proposed cam tip envelopes remain protected at X385.259375, width14 mm. Preserve 25 pan mounting stations in total; only front stations may change with the new local flange. Preserve rear pan/body wherever geometry permits.

Source support: seven-boss cover and normalized main-gasket outline; I-223 supports limited flush trimming of gasket terminals and sealant at pan/block seams; OS34601R remains a continuous gasket. No separate loose strip is stacked on it. Local front flange, transition, sealing cross-sections and fastener coordinates are estimates. Record trims and smooth-contour displacement.

Acceptance: valid watertight exports; full-area support of the revised front gasket on both faces; both terminal contacts and connected sealing path; clear fastener paths with seating and surrounding material; no unintended overlap; both gear envelopes and cover wall reserve; fixed seal; removed-front-seal and terminal-gap negative controls. Whole-engine installation, browser and full learning remain NOT RUN.

## Evidence ledger

| Claim / feature | Value and datum | Evidence class | Source and durable ledger | Limits |
|---|---|---|---|---|
| Cover identity/topology | Seven peripheral bosses, recessed back and lower pan bridge | Replacement comparison | Dorman 635-109, published cross E5TZ 6019-H; `reference/engine/timing-cover-joint-review.json` | Replacement specimen, not this truck's measured casting |
| Main gasket | Dimensionless open-bottom outline and seven holes | Replacement comparison | Fel-Pro TCS 45829/45830 images and `cad/engine/timing_cover_joint_candidate.py` | Source holes ±3 pixels, outline ±8 pixels; no manufacturer dimensions inferred |
| Gasket set compatibility | TCS 45829/45830 used with OS 34601 R | Verified catalog application | `reference/engine/fel-pro-vin-y-gaskets-reviewed.json`; 1991–1997 VIN Y entry | 45830 includes a repair sleeve; five-hole strip not added over an intact gasket |
| Terminal service method | Limited flush main-gasket trim; replace disturbed front seal; sealant at intersections | Manufacturer procedure | Fel-Pro I-223 rev 01/04, public manufacturer PDF; hash in `reference/engine/timing-cover-pan-joint-review.json` | Service instructions support topology, not this candidate's dimensions |
| Pan gasket | One-piece molded rubber | Manufacturer procedure | Fel-Pro I-1484 rev 02/15; same ledger | Candidate omits molded ribs and compression mechanics |
| Pan stations | 25 total, two front block/cover sealant sites | Applicable manual | Exact 1994 oil pan Fig. 34, source 350379654 | Existing station coordinates are provisional; count is supported |
| Registration | Scale 0.2622330227 mm/reference pixel, rotation −0.03982355°, crank source point (588.5373742, 930.4751088) | Explicit feasibility estimate | `reference/engine/timing-cover-registration-review.json` and registration validation | Seven-hole projective image comparison reverses handedness. CAD uses one similarity transform, never a projective distortion. Perspective/depth uncertainty remains unbounded |
| Common terminal plane | Z −24.5 mm | Estimated joint datum | Current module | Raw endpoints approximately Z −26.807 to −24.704; at most 2.31 mm terminal trim, plus distinct 0.5 mm sealant pocket. No filling of the prior 13/37 mm gaps |
| Fixed model interfaces | Crank Y/Z 0; seal center X 414; block front X 373 | Inherited model datums | Current shell parameters and fixed-interface checks | X 373 is not a factory measurement |
| Gear protection | Crank tip radius 43.18 mm; cam 83.947 mm; cam centers (90,72) and (95.109821,76.087857) | Replacement OD comparison plus estimated axes | Timing gear worker reports | 121.8 mm proposed axis spacing and direction remain estimates; no cam migration in this module |

The normalized gasket data remain primary. The contour uses two bounded corner subdivisions, each displacement at most 0.4 mm, within the 2.098 mm transformed outline uncertainty. It is still a polygonal approximation, not a reverse-engineered production casting.

## Delivery

Candidate only; no canonical assembly, inventory, viewer or block modifications. Integration base advanced to `705c4683c199d8c5e28addba018bc8d1bdd399b1` on `engine/timing-core-pan-joint` while these owned files remained untracked. The earlier contract baseline and rejected studies remain unchanged. Current context manifest is `ab99fff2f63ad5dfc21fde8d12a32fc2a3d65832e6c8664baefd99d94403f7bf`.

Entry point: `timing_cover_front_joint_candidate.build(pan_world=None) -> (parts, metadata)`. For the complete candidate, supply the world-coordinate v9 pan: `b.Pos(0, -12, -96) * oil_pan_joint_v9_candidate.pan_interface(None)`. Millimeter CAD axes and world frame match the existing engine. GLB converts `(X,Y,Z)` millimeters to `(X,Z,-Y)` meters. The render's exploded offsets are display-only.

The six outputs are cover, main gasket, future block land, terminal sealant, continuous pan gasket and full pan. Terminal sealant intentionally contains two distinct solids. The block land is proposed casting material for a future coordinated regeneration; it must never become a loose installed component.

The changed front region is X >335 mm. The pan retains the exact prior solid for X ≤335; its wider neck extends to X 399 and Y −149…213 mm. A 4 mm estimated shoulder at Z −80…−76 connects that neck to the unchanged body. The pan gasket is 2 mm thick vertically; local thickness in the curved region is not claimed as a manufacturer section.

Twenty stations are unchanged. Five proposed stations, listed as `(X, Y, under-head Z)` in mm, are `(365.5, −132, −32.1)`, `(365.5, 196, −32.1)`, `(390, −110, −32.1)`, `(390, 0, −67)`, and `(390, 180, −32.1)`. The first two use matching future block sockets; the other three use the cover. They are estimates. Their 14.498 mm nominal shaft/socket engagement, 0.502 mm tip reserve and 7.5 mm washer seat radius are geometric stack checks, not a thread specification or torque recommendation.

The future block proposal comprises the source-following arch X 363…373 above Z −24.5, the widened side supports beginning X 335, and the two X 365.5 socket bosses clipped to the X 373 block plane. Root must coordinate it with the separate block worker's cam tunnel/front retention changes. Preserved crank, seal, deck, cylinder, head-bolt and accessory datums must remain protected. Neighbor changes required for eventual integration are cover, main gasket, pan gasket, pan, five pan fastener transforms, block front casting land and the separately reviewed timing core. Rear pan and its other 20 stations are preserved.

Build and render from repository root:

```sh
.venv-cad/bin/python scripts/check-timing-cover-front-joint-candidate.py
python3 scripts/render-timing-cover-front-joint-candidate.py
```

Environment: macOS 15.6.1 arm64, CAD Python 3.13.12, build123d 0.10.0, trimesh 4.7.4. The renderer uses system Python with NumPy and Matplotlib. Model/effort and usage billing are unavailable. Output directory: `cad/engine/generated/timing-cover-front-joint-candidate/`; six named STEP/GLB files, combined `candidate.glb`, `preview.npz`, `candidate-review.png`, `terminal-contact-review.png`, and local `source-comparison.png`. No release has been published for this candidate. Original sources and source composites are excluded from Git and release archives.

## Validation and review

The checker uses the existing 0.1 mm³ overlap/support audit convention and a 0.01 mm³ adaptive STEP volume-difference threshold. The latter is not relaxed when default CAD volume integration drifts. Meshes are tessellated from the STEP roundtrip at 0.12 mm / 0.16 radians, welded at six decimal places and required to be watertight. A continuous pan gasket with one central opening and 25 bolt holes has Euler characteristic −50; any additional window fails the topology gate.

Full-area front support uses 0.02 mm witness layers on both gasket faces. Main-gasket face witnesses cover both X-facing seats. Separate controls remove the front gasket and both terminal sealant patches. These are geometric gap/contact tests, not a fluid simulation or rubber-compression model. Gear checks include both cam hypotheses and the proposed cam axial travel −0.1…0 mm. The current oil pump and pickup are proven outside the changed front X region by their bound input geometry; whole-engine interference remains untested.

Visual review must use the actual exports. The source comparison mirrors the Dorman back photograph solely to match the displayed CAD rear-view convention; the model is not mirrored or projectively warped. The candidate captures the open arch, seven bosses, recessed cavity and lower bridge. Its front face lacks the specimen's cast reinforcement ribs, lettering and detailed blends. The broad asymmetric front pan transition is a coordinated estimate. Those differences prevent a production-fidelity claim.

Rejected results remain in `rejected-first-joint/` and `rejected-pad-windows/` beneath the generated directory. The first render revealed an open shoulder despite valid solid meshes; the shoulder was corrected. A later valid gasket contained two extra windows around flat pads on the sloping transition; relocating the two estimated side stations removed those windows. A disconnected support witness returned a shape list, so the checker now normalizes it before Boolean subtraction. These are engineering review notes, not user-facing learning content.

| Gate | Status and method | Remaining limits |
|---|---|---|
| Application/coverage | PASS for bounded replacement topology; source ledger above | Production dimensions, casting ribs/lettering and exact molded sections unknown or omitted |
| Dimensions/coordinates | PASS for explicit model contract | Estimated registration, pan corridor and five station positions; no factory-coordinate claim |
| CAD/export | PASS; bound validation JSON | STEP-normalized mesh and adaptive volume checks; no general clean-clone whole-engine rebuild claim |
| Source/visual comparison | Worker inspected actual section and source comparison; root review pending | Broad front surface and estimated asymmetric pan transition remain visibly unlike a fully detailed casting |
| Installed interfaces | NOT RUN for installed engine; isolated contact checks in validation JSON | Future block casting patch and five fastener transforms require coordinated integration |
| Motion/disassembly | PASS only for both prescribed gear tip envelopes and proposed axial travel | No full removal sequence or engine motion sweep |
| Learning/diagnostics | NOT RUN | Review notes about failed CAD are not a user-facing component lesson |
| Browser integration | NOT RUN | Offline renders cannot establish browser selection, explosion or reset |
| Reproduction/review | Reproducible isolated commands and bound hashes; root review pending | Candidate artifacts not yet released; current local exports required for visual review |

The unrelated rear-exhaust-neck installation advanced the global manifest from `ab99fff2f63ad5dfc21fde8d12a32fc2a3d65832e6c8664baefd99d94403f7bf` to `91950c89dc12c17d1169ec77eed16efa71919c6832061346582ee02b81599ad6`. Root reported that other 740 STEP files and every assembly frame/mechanism were unchanged. The current checker binds the exact manifest it reads and both imported pump/pickup STEP files; this note does not rewrite historical report hashes or waive a dependency.

## Tracking and restart

Issue #32 remains open. Root owns shared integration and any issue/PR updates. This delivery is an isolated candidate for review, not an installed acceptance request. Next action: inspect `candidate-review.png`, `terminal-contact-review.png`, `source-comparison.png` and the bound validation report, then coordinate the proposed future land with the block migration worker. No canonical hook should be added until that review passes. Usage metrics are unavailable.

Final local result: **PASS**, report `inventory/engine/timing-cover-front-joint-validation.json`, SHA-256 `6a4490ed3d50956e9fd0db1297fa17a217c363e15d1b453bd64b2a8c94d11116`. Export and render hashes are in `reference/engine/timing-cover-front-joint-review.json`. All six outputs are valid and watertight. Maximum adaptive STEP volume difference is 0.00012787827290594578 mm³. Both front faces and both main-gasket faces have zero missing support; all 15 pair overlaps are zero. Minimum checked cover clearance is 0.22 mm for the crank envelope and 0.15 mm for the proposed cam axial travel. These small model clearances are not production tolerances. Two terminal contacts pass, removed-front witnesses expose approximately 267.741 mm³ gaps, and removing sealant loses 6.339 mm³ support. Python syntax checks pass. Root visual review remains pending. No process remains running.
