# Component handoff: air-cleaner-body-bracket-screw

## Contract

- Issue #80 under engine #1. Contributors: original `inclined_linkage_resume`, continuation `airbox_screw_finish`; root owns integration, branch and shared files.
- Baseline `4f1fe9da2ec177e1ff61668df66ca422e37b0b7c`; branch `engine/source-host-interfaces-20261002`. Manifest SHA N/A: no manifest consumed or edited. No commit/PR submitted by worker.
- Scope: isolated replacement-envelope candidate, one reusable definition. Four future body occurrences have no accepted pose. No installation, body bracket, receiving clips, box screws or grommets modeled.
- Owned files: `cad/engine/airbox_screw_online_20261002.py`; `scripts/*airbox-screw-online-20261002*`; matching `reference/engine/` and `docs/components/` files; only `cad/engine/generated/airbox-screw-online-20261002/` generated outputs. Shared edits: none.
- Identity: Auveco 13019 cross-references Ford N610959-S2 body-bracket screw. Exact-year Ford figure identifies four; distinct N611062-S2 box-to-grommet screws are not interchangeable evidence.
- Frame: CAD mm, bearing plane Z0, tip +Z19, head −Z; exporter `(X,Y,Z) → (X,Z,−Y)/1000` gives GLB meters/Y-up. Parent/transform/explode absent, not identity-world placement.
- Future interfaces: washer bearing annulus, receiving pilot/clip axis, engaged sheet stack and hex tool envelope. Host normals/coordinates, pilot, engagement, load, torque and removal clearance remain unknown. No motion/flow interface in this isolated solid.
- Inputs available: original partial CAD/STEP/GLB/report; common `pan_fastener_thread_candidate` solid/cylinder helpers; manufacturer PDF page pixels and frozen host-source ledger. Source access requires public URL in ledger; original images are not build dependencies or redistributed.
- Predeclared checks: valid one-solid STEP roundtrip, positive watertight winding-consistent mesh, bounds <0.05 mm, 80 full-shank phase/pitch material probes and smooth control. Continuation adds taper crest/root probes and old-tip negative control after actual render exposed missing point threads. These are sampled geometry checks, not thread manufacturing standards.

## Evidence ledger

| Claim | Value / datum | Class | Source | Limit |
|---|---|---|---|---|
| Body screw identity/count | N610959-S2, four | Verified application architecture | Ford 1994 figure190226466, item9; source ledger | No four body coordinates supplied |
| Nominal thread envelope | 6.3 mm × 1.81 mm × 19 mm | Replacement comparison | Auveco13019, printed102/PDF2 | Under-head length convention adopted; no OEM tolerances |
| Head envelope | Washer OD11.5 mm; hex AF8 mm | Replacement comparison | Same catalog row | Head/flange thickness unknown |
| Hex, flange, thread, point | Visible external topology | Replacement photo comparison | Same row, actual pixels reviewed | No measurable camera fit |
| Root/head/point/profile | Root4.5; flange0.7; hex height3.4; bevel0.3; point4; tip radius0.08; crest halfwidth0.08; profile halfwidth0.65 mm | Inferred construction choices | Contract / CAD PARAMETERS | Right-handed convention and tapered radial profile estimated |
| Body registration/fit | Unknown | Unknown | Host contract | No installation allowed |

Original source hash and reusable derived source notes are in `reference/engine/airbox-host-online-20261002.json` and `kb/sources/airbox-host-online-20261002-screw.md`. Source/render inspection compares actual catalog pixels with actual exported mesh; no copyrighted image is included in the archive.

## Delivery

Readiness: **candidate**, reviewable for preservation only. Entry point: `airbox_screw_online_20261002.build(smooth=False) -> build123d.Solid`. `smooth=True` constructs the intentionally wrong smooth envelope for sensitivity checks. `PARAMETERS`, `head()` and `envelope()` expose estimates. Helpers import only `build123d` and standard Python; no prior pan geometry or generated assets are needed.

Outputs are `cad/engine/generated/airbox-screw-online-20261002/air-cleaner-body-bracket-screw.step`, matching `.glb`, `source-view-review.png`, `render.json` and `build.log`. Reports: `reference/engine/airbox-screw-online-20261002-validation.json`, `-replay.json`, and frozen `-delivery.json`. Authored archive metadata/member hashes are in `-delivery.json`; release upload remains integration-owner work.

From repository root, after restoring the authored archive if reusing frozen outputs:

```sh
.venv-cad/bin/python scripts/check-airbox-screw-online-20261002.py
.venv-cad/bin/python scripts/check-airbox-screw-online-20261002-replay.py
MPLCONFIGDIR=/private/tmp/airbox-screw-mpl python3 scripts/render-airbox-screw-online-20261002.py
python3 scripts/package-airbox-screw-online-20261002.py
```

Environment: macOS15.6.1 arm64; CAD Python3.13.12/build123d0.10.0/trimesh4.7.4 with repository `cad/requirements-engine-lock.txt`. Renderer uses system Python with matplotlib3.10.9 and reads the CAD environment's trimesh/numpy. Renderer script discovers the repository-relative environment; the temporary cache directory is disposable, not an input. Model/effort/token/cost data unavailable. Render anti-aliasing/font bytes can vary by environment; STEP headers may vary on rebuild, so regenerated hashes require fresh reports rather than assuming frozen equivalence.

## Validation and review

| Gate | Status | Evidence and limit |
|---|---|---|
| Application/coverage | PASS scoped candidate | Source ledger distinguishes body screws from two isolated box screws; one integral screw solid, no invented separate washer |
| Dimensions/coordinates | PASS declared envelope; installed coordinates NOT RUN | Five catalog dimensions encoded; remaining values explicit estimates |
| CAD/export | PASS local | Validation binds actual STEP/GLB and checker hashes; valid single solid, positive watertight mesh and <0.05 mm bounds |
| Source/visual | PASS bounded topology comparison | Actual side/oblique/head render and catalog page reviewed; shape estimate discrepancies retained below |
| Installed interfaces | NOT RUN | No metric body bracket, receiving pilot, seat stack or world pose |
| Motion/disassembly | NOT RUN | No installation or tool/withdrawal neighborhood |
| Learning/diagnostics | PASS bounded content | Function/failure explanation below; no repair torque or fit assertion |
| Browser integration | NOT RUN | Uninstalled specimen, no deep link or runtime occurrence |
| Reproduction/review | PASS worker package; root review pending | Frozen ledger/archive exact members, source/dependency hashes, preserved failed attempts; independent saved-STEP profile replay |

Final results: CAD volume601.4400977mm³; mesh volume601.3612174mm³; maximum mesh-bounds difference0.00113677mm. All80 body and20 point material probes pass;936 probes at0.03mm outside the estimated cone remain empty. Smooth envelope and original smooth-tip controls both rejected. Targeted Python compilation and navigation (1,349 occurrences/1,548 links) pass; navigation is not specimen browser acceptance.

Actual source/render comparison: source has short external hex, round washer head, coarse thread and pointed nose. The model reproduces these features in actual mesh. Source round-over/fillets, precise chamfer and crest/root forms are absent or simplified; flange flatness, head height and point profile are not source dimensions. Taper correction is a geometric estimate, not new manufacturer evidence.

Attempts retained in generated folder: attempt1 has a constant root cylinder and clipped ridge, leaving a smooth conical point despite passing body-thread probes; attempt2 tapers the core but still loses constant-radius ridge at the end; attempt3 introduces scaled taper profiles but fails the one-solid guard because above-tip excess creates a detached body. Attempt4 then failed on an empty above-tip intersection returning None; it is retained as source/log. Attempts5–7 passed the body/export checks but failed the same three terminal crest probes. Smooth versus ruled interpolation and conical versus axial clipping did not repair the oversized end profiles. An isolated raw last turn contained a failed crest probe, while its clipped result did not; this localized the loss without proving one kernel mechanism. Final construction scales both radial and axial profile coordinates toward the nose and terminates the last turn before the endpoint, then clips axially. Taper turns use24 ruled segments/revolution, an estimated0.6mm base radial overlap and slope-based crest inset (crest halfwidth × cone slope); these are construction estimates, not catalog data. The tiny terminal end remains the tapered core. The original20 tip probes and0.03mm outside-envelope allowance were not relaxed. Do not use earlier PASS body reports as point acceptance. No historical attempts were silently overwritten.

No neighbors/manifests changed and no prior assembly checks invalidated. Worker verdict: mergeable candidate documentation/code subject to root review; **not integration-ready or accepted installed**. #80 remains open. Acquire actual bracket/body hole planes, receiving pilot/clip and stack evidence before arranging the four occurrences.

## Function and failure explanation

The four body screws retain the air-cleaner support bracket to the body. Their hex accepts a tool; the integral washer head spreads bearing load on the bracket; the coarse tapping thread engages a compatible receiving feature. Which exact pilot/clip construction is present is unresolved. The two box-to-bracket screws and isolators form a separate support path and use different hardware.

A missing screw, damaged receiving thread, loose bearing stack, corrosion or distorted bracket can reduce retention and allow movement/rattle. Inspect the actual screw identity, seat contact and receiving feature before attributing a symptom to this one part. This model cannot predict clamp load, pull-out strength, correct torque, reuse suitability or a replacement pilot size. These are mechanical failure possibilities, not diagnosed faults on the owner's truck.

## Tracking and restart

Root manages issue/PR/board; no board write made. Exact next action: independently inspect frozen source/render and validation hashes, publish authored archive, then retain #80 open for host evidence. No active CAD process remains at handoff. Initial issue fetch failed network access and process listing was sandbox denied; scope was supplied by root and the existing contract. No continuing background-work claim. No usage/billing measurements available.
