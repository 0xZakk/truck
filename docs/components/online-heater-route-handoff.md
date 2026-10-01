# Component handoff: online heater-return axial route

## Contract and evidence

Engine #47/#32 under engine #1; root integration owner. Baseline `dbe1e3c435c137fe2d30f6420db28476127c0f55`. Scope is an isolated candidate following newly authorized online source research. Original contract remains `online-heater-research.md`, recorded before CAD. No canonical, private-stage, pump-housing or frozen failed-route changes.

New evidence: four actual GMB125-1810 manufacturer product views, GMB bearing bulletin014, GMB pump manual and Carter hub-height datum sheet. See `reference/engine/online-heater-research.json` for exact URLs, capture hashes and limits. Four source pages and four atomic notes use `online-heater-*`. Direct public retrieval succeeded after web cache/DNS failures. PDF text/OCR was ingested; the transcript attempt failed because yt-dlp is absent. No purchases, messages, owner-photo request or installation. Root owns semantic backlinks; the earlier failed embedding attempt wrote no shared outputs.

GMB is a replacement comparison. Its side view supports a short forward crest followed by a shallower rearward tube run; it does not identify the owner's part or provide measured millimeters. Carter separates the pulley seating plane from a protruding hub pilot. The98.552mm conversion of a secondary3.88in field is not adopted; manufacturer GMB dimensions available online are package fields. Bearing row identity/element count/size remain unknown.

## Geometry and construction

API `cad/engine/online_heater_route_candidate.py:tube(variant='nominal')` returns WORLD-CAD-mm stock. Root(410,−80,230.3), radial endpoint(−171,415), OD16/bore13,12mm insertion and beadR8.5 are inherited estimates. Pump housing is byte-identical to `waterpump-heater-source-candidate/housing.step`.

The source-derived nominal terminalX348.0333 replaces old236 only in this isolated study. Source pixel perturbations give candidateX340.125 and355.597826; they are sensitivity alternatives, not proven physical uncertainty bounds. See the prior contract for arithmetic and approximate pixels. New tangent-continuous cubic spans pass a forward crest atX425. The first quintic outer/inner sweeps were individually valid, but hollow subtraction split material; rejected code and both build failures remain. Cubic spans retain root/end constraints but their intermediate radial interpolation is also estimated, not literally the old cubic. No neighbor Boolean or clearance-fitting changed the route.

The retained radial root-tip span is205.901mm, whereas178pixels at143/180mm-per-pixel project to141.411mm. An orthographic explanation would require approximately0.687 radial projection factor; camera azimuth is unregistered. **This is an axial-only hypothesis, not a full3D source-shape match.** Four-view camera/landmark registration remains the next source-fidelity gate.

## Delivery and reproduction

Run, from repository root:

```
.venv-cad/bin/python scripts/build-online-heater-route.py
.venv-cad/bin/python scripts/check-online-heater-route.py
```

The renderer consumes the preserved `review-data.npz` extracted from actual exported meshes; run `python3 scripts/render-online-heater-route.py`. macOS, existing Python3.13/build123d0.10; matplotlib renderer uses system Python. No dependencies installed. Public original images/PDFs are local source evidence, not approved redistribution; publish authored notes, URLs and hashes under repository artifact policy.

Assets are `cad/engine/generated/online-heater-route-candidate/{nominal,rear-limit,front-limit}-tube.{step,glb}`. Nominal STEP SHA `5c2f41fab9c9024b457b173c2f76f7a3b240d34c63a6bb7c07bd4cbfef52f967`; nominal GLB SHA `beaef3d34b8f8284d267807b97dc12a8c83193a80eba5e47a3bf081dbb5991c5`. Actual render `review.png` was inspected. Root review pending.

## Validation

| Gate | Result | Scope and limits |
|---|---|---|
|Application/coverage|PASS new source capture; Ford identity partial|New primary replacement views and generic bearing references; no internal Ford bearing identification|
|Dimensions/coordinates|PASS explicit estimated frame|WORLD mm; root retained; axial interpretation inferred; radial registration NOT RUN|
|CAD/export|PASS scoped|Three valid single connected tubes; watertight/winding-consistent meshes; maximum bounds error0.001216mm|
|Source/visual comparison|PARTIAL|All four manufacturer images and actual CAD render inspected; only axial interpretation proposed|
|Interfaces|PASS conditional static|62 exact whole-stage broadphase pairs across three variants, zero overlap>0.1mm³/errors;2mm padded actual STEP bounds|
|Root/passages/wall|PASS scoped|603.185789mm² socket side area fully present in housing and tube; zero housing overlap/lumen obstruction/wall-witness loss; blocked-lumen control5.964909mm³|
|Motion/disassembly|NOT RUN|Neutralq0 only; tool envelopes/service sequence not rerun; source root retention and hose/clamps remain unknown|
|Learning/diagnostics|PASS KB scope only|Four source pages and four atomic notes; user-facing engine lessons unchanged|
|Browser|NOT RUN|No installation and existing browser restriction|
|Reproduction/review|PASS local reproduction; root pending|Reports bind inputs; syntax/KB link checks and current hashes pass|

Report `inventory/engine/online-heater-route-check.json` binds756 inputs. This run tests actual v4 stage plus explicit conditional world-STEP substitutions: frozen coordinated heater housing, rear cover, main gasket and pump gasket. It is **not** a pure installed-v4 audit or a new global housing acceptance. Replaced original heater elbow is excluded; tube-to-housing is explicitly tested. Old deep-rear route and its five conflicts remain untouched. No complete heater hose is present to certify connectivity. Unrelated engine failures remain.

## Tracking and next action

Candidate ready for root review, not installation. Root should inspect the manufacturer side view and actual render, then decide whether to pursue joint four-view registration and source-compatible hose terminal placement. No clearance-driven iteration is pending. Build3465, checker98126 and renderer4852 completed exit0; no process running. Usage/model effort unavailable.
