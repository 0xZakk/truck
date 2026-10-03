# HO2S isolated exterior candidate — handoff

## Contract and ownership

Issue #82 under engine #1; contributor `airbox_screw_finish`; root is integration owner. Baseline `4f2760612a18e597da5e6df15e27b6b9ae69ac6c`; working shared branch is root-controlled. No Git/issue/shared manifest/builder/viewer changes made by this worker. Manifest hash N/A: no installed assembly is a build dependency. See frozen `ho2s-specimen-20261003-contract.md` and pre-CAD hash ledger; the two explicit implementation clarifications are in `ho2s-specimen-20261003-contract-amendment.json`.

Root approved the prior bounded dimension table and this isolated exterior scope. Identity: Bosch15718/0258005718 replacement comparison with qualified Ford F4UZ-9F472-C chain from earlier evidence. Only22 mm hex AF is a primary metric dimension. Other exterior dimensions, M18×1.5 visual thread choice, hidden dimensions, materials/colors and region splits are inferred estimates. Region IDs in the validation report are stable within this candidate; they are not installed occurrence IDs or a verified service BOM.

Units/frame: CAD mm, sensor nominal ring plane Z0, +Z toward exhaust tip; connector independent rear Z0/mouth Z44. No connector-to-sensor transform, parent, installed lead route, pipe/bung, harness mate or explode convention is accepted. Full lead length is deliberately not represented by the short cut stubs. Do not treat their colors/order as pin assignments or continuity.

## Evidence ledger

| Feature | Evidence | Source and limit |
|---|---|---|
| 22mm AF hex; heated narrow-band/four contacts | Primary target catalog attributes | `ho2s-online-20261003-evidence.json`; Bosch15718 product record |
| Stepped shell/metal exit, pale insert and colored exit collars; long slotted nose | Actual manufacturer photo pixels reviewed | Front/right/rear URLs and hashes in prior evidence ledger; no source originals distributed |
| Body/probe/connector dimensions | Inferred photo scale | `ho2s-dimensions-20261003-landmarks.json` and projection report; conditional camera/hex-roll sensitivity, not tolerance |
| Thread M18×1.5, profile and handedness | Inferred modeling choice | Two observed intervals cannot discriminate1.25 vs1.5; no manufacturing fit claim |
| Four cap slots; .8mm wall; empty shell; connector walls/face/pins/latch/insert | Educational geometry estimates | Named pre-CAD values; exact hidden shape/count/production construction unknown |
| NTK22503 interchange | Replacement comparison only | Manufacturer guide-only cross-reference; its different body and558mm lead not transferred |
| Heater/ceramic/electrodes/potting/crimps/hidden seals | Unknown target geometry, omitted | Bosch family thimble illustration is not target-exact BOM |

## Delivery

Readiness: **candidate, isolated exterior only**.27 individually exported regions: main shell, mounting shell, ring, hollow slotted cap, rear closure, pale exit insert, four exit collars, four sensor lead stubs; connector housing/latch, support face, colored seal, central divider, rear insert, four contacts and four connector lead stubs. No complete internal cartridge, cable route or installed host geometry is claimed.

API: import `cad/engine/ho2s_specimen_20261003.py`; call `build()` with no arguments. Returns dictionary keyed by stable region ID, each containing `shape` (one build123d solid), `frame`, `color`, `meaning`. It uses existing `pan_fastener_thread_candidate.solid/cz`; no assembly builder is called. Controls: `threaded_mount(smooth=True)`, `protective_cap(blocked=True)`, `connector_housing(blocked=True)`. Export mapping follows existing screw/ACT conventions: mmXYZ→meter(X,Z,−Y).

Outputs: `cad/engine/generated/ho2s-specimen-20261003/` contains27 STEP/GLB pairs, three saved bad-condition STEPs, actual GLB renders, renderer metadata, logs and preserved failed attempts. Validation/replay/contract/package ledgers are `reference/engine/ho2s-specimen-20261003-*`. Archive and exact dependency allowlist are in the delivery ledger; release URL remains null until root publishes. No generated predecessor needed. Original photographs/PDFs/HTML are excluded; URL/hash-based source access is separate from deterministic geometry reproduction.

From repository root, with the project CAD lock:

```sh
.venv-cad/bin/python scripts/check-ho2s-specimen-20261003.py
.venv-cad/bin/python scripts/replay-ho2s-specimen-20261003.py
MPLCONFIGDIR=/private/tmp/ho2s-specimen-mpl python3 scripts/render-ho2s-specimen-20261003.py
python3 scripts/package-ho2s-specimen-20261003.py
```

The optional temporary matplotlib cache is not an input. Build environment: macOS15.6.1arm64, Python3.13.12, build123d0.10.0, cadquery-ocp7.8.1.1.post1, trimesh4.7.4, NumPy2.5.3. Renderer uses systemPython/NumPy/Matplotlib, with recorded versions in render metadata. No installation or pin changes. Model/effort/usage measurements unavailable.

## Validation and review

| Gate | Result | Evidence | Remaining limit |
|---|---|---|---|
| Application/coverage | PASS scoped replacement exterior | Prior primary source ledger;27 named modeled regions | Not exact production BOM; target internals omitted |
| Dimensions/coordinates | PASS declared estimates | Pre-CAD table and validation parameters; independent frames | AF22 is sole primary metric; no factory tolerances/pose |
| CAD/export | PASS local |27 valid positive single-solid STEP roundtrips;27 watertight, winding-consistent positive GLBs; maxbounds error0.002125mm <0.05mm | Mesh integrity does not establish fit |
| Source/visual comparison | PASS scoped worker comparison; root review pending | `sensor-review.png`, `connector-review.png`, `thread-cap-review.png`; actual source pixels reviewed | Stylized contours, unmeasured hidden slot count/connector dimensions |
| Local material/void | PASS sampled |48 crest/root probes;36 slot void probes plus12 between-slot material samples; smooth/closed controls rejected. Independent savedSTEP and GLB solid-angle replay48+36 | Not continuous thread gauge/flow simulation |
| Local region interfaces | PASS overlap audit |169 same-frame pairs, no overlap >0.1mm³; ring/wire-hole/hollow-body/AF probes | Ring compression/axial clamp stack and production joins unverified;0.1 is audit convention |
| Installed interfaces | NOT RUN | No actual exhaust-pipe/bung, probe intrusion, lead route or mate | No installation authorized |
| Motion/disassembly | NOT RUN | No installed neighbors, tool sweep or latch flexure | Static local geometry does not establish serviceability |
| Learning/diagnostics | PASS scoped explanation below | Primary source functions; explicit omitted internals | No calibration, DTC diagnosis, pinout or repair specification |
| Browser integration | NOT RUN | Candidate assets are not installed | No deep link/selection/reset or browser acceptance |
| Reproduction/review | PASS worker hash/replay/package; root review pending | Exact source, report, asset and archive hashes | Original source access separate; preserve newer dependencies before extraction |

### Actual source versus actual export

Manufacturer right view and exported side both show the long main cylinder, distinct22mm hex, annular seat feature, short visible coarse thread, rounded slotted cap and three-step metal rear closure. Front/rear comparisons retain four colored wire exits, pale connector with circular mouth/open latch, colored internal ring/divider and four round contact tips. Render views use a per-pixel depth buffer over actual GLB triangles, not generated concept art.

Differences remain explicit: shell stamping/rolled seams, fine edge rounding and surface finish are omitted; nose hemisphere and four equally spaced capsule slots simplify the photo's formed tip; the annular ring is a simple uncompressed envelope, not the photographed bowed section or an accepted clamp stack. Rear shoulders are estimated conical steps. Connector rear section/rail latch/pin positions are educational estimates; complex keying, internal carrier holes visible in the photo, terminal crimp form and retention are not reconstructed. The straight cut stubs omit bundled cable/jacket/wrap and do not assert any installed route. These limits keep this a candidate exterior study.

### Function and failure interpretation

The threaded/hex region locates the sensor in a future exhaust-pipe host and gives a tool interface; the cap shields the sensing region while its openings permit exhaust access. The heated narrow-band sensing function and zirconia switching-family principle are supported by the Bosch product/architecture sources. The exact ceramic/heater stack is absent here, so the hollow educational shell is not a proposed real internal flow path. Four conductors and mating contacts provide electrical paths in the real product; the modeled cut stubs do not complete that circuit.

The model exposes inspection regions for damaged threads, obstructed cap slots, damaged lead insulation and connector contact/latch damage. These are qualitative failure possibilities, not diagnosis of this truck or proof that any one symptom identifies this sensor. The blocked-cap/mouth and smooth-thread controls test geometric detection only. Signal behavior, heater circuit and any fault diagnosis require applicable electrical/service evidence and actual measurements; no numeric repair specification is inferred from the mesh.

### Preserved failure and correction

Attempt1 passed valid CAD/STEP but failed cap mesh watertightness. The mesh had two zero-area triangles at the outer/inner sphere poles, producing four non-two-use edges. Preserve `attempt1-source.py`, `attempt1-checker.py`, `attempt1-slotted-cap.step/.ply` and `attempt1-check.log`. Existing project exporter cleanup removes only degenerate/duplicate faces, not holes; two faces removed, volume delta2.84e−13mm³. Final cap remains the same CAD geometry, and all original gates pass. No bounds or topology threshold was relaxed.

Early renderer attempts exposed depth-sort artifacts on hollow connector walls. Their authored renderer/images are retained. Final rendering interpolates triangle depth per pixel; geometry and validation hashes remain unchanged. This was a display correction, not mesh repair.

## Tracking and next action

Worker verdict: ready for root's separate preservation review, **not integration-ready or accepted installed**. #82 stays open for pipe/bung/pose, thermal/probe clearance, wiring/route/mate, service/browser and exact source gaps. Root may preserve this bounded candidate without promoting installation. No shared checks were invalidated because no shared geometry/transform changed. No running worker process at handoff. Next action: root verifies frozen delivery members and compares the three actual renders with the hash-identified source photos; any correction invalidates only dependent reports. No owner request required.
