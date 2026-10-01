# Component contract and handoff: shifted oil-drive connections

## Contract before geometry

Engine #32, root integration owner; inclined-linkage worker owns new connection research/module/checker/assets only. Baseline `8c2d2d9a1400acf784e04581a61e6a6ede38d3ba`, branch `engine/timing-drive-fit`. Peer owns rigid distributor/pump/intermediate branch staging. No canonical assets or frozen files change. Preserve all local occurrence IDs and the pickup bell/screen sump datums unless a separate scoped result justifies a change.

Initial scope: bind actual canonical pickup/pump STEP and current block/pan candidates; measure the old and shifted pump inlet endpoints, local axes, overlap and passage. Audit mounting seats/shaft passage independently from fluid routing. The current pump source explicitly leaves discharge routing unresolved; a mechanical shaft bore is not an oil outlet. Source classifications remain inherited: Melling shaft length/across-flats replacement comparison, pickup identity exactyear service listing, pump/tube routing/mounting dimensions estimates. No pressure or factory-contour claim.

Proposed correction, subject to measured checks: alter only the upstream portion of the estimated pickup tube to meet the translated pump inlet, retain the downstream tube/bell/screen interface and wall dimensions, and prove actual tube clearance, uninterrupted bore and positive seat contact. Predeclare the splice interval and blend law after auditing actual geometry. Do not move the whole pickup with the pump; that would disturb the retained sump position. Do not invent an outlet or drill a block passage without an explicit route/source contract.

Owned files initially: this handoff, `scripts/check-shifted-oil-drive-connections.py`, `inventory/engine/shifted-oil-drive-connection-audit.json`. Later candidate filenames will be separately declared. Planned evidence: analytic endpoint/axis differences plus actual CAD cylindrical/circular sections, positive witnesses and a deliberately stale-endpoint control. Actual overlaps use inherited0.1 mm³ convention, not a leak/fit tolerance. Export, mesh, source visual and browser gates will be separate; browser NOT RUN. Exact current neighbor hashes and environment will be bound in reports. No installed acceptance.

## Bounded pickup candidate decision

Fresh actual probes establish the old end has no inserted tube stock beyond pump localX−34; circumferential housing material atR6.1 is incomplete atX−33.9 and complete at the sampledX−33,−32,−31. A new estimated inlet insertion toX−31 provides3 mm of engagement without a housing change. This is explicitly an educational fit estimate, not a sourced press-fit depth or production attachment claim.

Candidate owned files: `cad/engine/shifted_oil_pickup_candidate.py`, `scripts/check-shifted-oil-pickup-candidate.py`, `inventory/engine/shifted-oil-pickup-candidate-validation.json`, and `cad/engine/generated/shifted-oil-pickup-candidate/`. Preserve exact exported old tail after a section normal to the original path at its worldX60 waypoint. Only a new upstream sweep joins that section to the translated/inset inlet. Conservative permitted material-change mask worldX54..200; preserve all material outside and all bell/screen datums. Tube outer radius6/bore4.8 remain estimates. No geometry may be trimmed solely to hide a collision; any failed neighbor check remains diagnostic.

## Audit results and source limits

`reference/engine/shifted-oil-drive-connection-sources.json` binds exactyear local sources without redistributing artwork. The manual pump installation calls for a new gasket; the actual lubrication schematic354634388 was viewed and supports qualitative pump/gallery topology. It supplies neither a gasket outline nor a discharge drilling datum. The existing pump source has no completed discharge passage, pump/block gasket or gallery connection. Those are missing interfaces, not satisfied by the intermediate-shaft bore.

Rigid shift `[0,5.109820990161097,4.087856792128875]` mm moves the inlet center from `[190.084,62.33097641719087,−109.2769759179967]` to `[190.084,67.44079740735197,−105.18911912586783]`, a6.543763726 mm offset. Raw old/new overlap zeros and nearzero distances fail to reveal this disconnect. Actual strict ring probes expose it. Original tube source replay is exact0; its end at pump-localX−34 has no inserted stock atX−33.9. Full housing backing appears at sampledX−33 and inward.

The new inset endpoint is worldX193.084 (pump-localX−31). The straight lead runs5 mm outward to keep the curve outside the housing. The first immediate-bend trial overlapped housing by0.154512896 mm³; source text/hashes and failure are retained in `shifted-oil-pickup-initial-bend-diagnostic.json`. No housing was trimmed. The fixed downstream splice is the original source path near `[60.0001206025,48.0000153537,−129.9999602203]`; the slight parameter inversion residual is recorded, not represented as a new measured datum.

The actual revised single-solid STEP has zero material change outside worldX54..200. All checked static neighbor overlaps are zero: pump, inner/outer rotors, cover, bell, screen, current blockv3 and panv2. Minimum rotor distance1.7 mm, block19.1218567 mm, pan8.4855071 mm. Bell surface gap0.4161788 mm and screen gap2 mm are inherited; this task does not prove downstream seal/retention. Actual insertion has103.058686 mm² shared cylindrical face,72/72 sampled wall/backing points, clear1.8 mm bore test band, and a clear swept lumen over the revised curve and retained-tail seam. The stale tube misses61.072561 mm³ of required inserted wall stock. Nominal cylindrical contact is not a pressure-seal or mechanical-retention specification.

The two exact frozen faceted feet are fully contained in current blockv3. The shifted mechanical shaft probe clears; +2 mm X control produces464.05893 mm³ overlap. Frozen positive pump and bolt seats are reused only for the unchanged rigid parts and retained support solids. Production mounting architecture, gasket/discharge and deeper galleries remain unknown.

## Native mesh failure preserved

Valid STEP/export and contact checks do not establish mesh integrity. Native tessellation of the Boolean-spliced tube is not watertight (291118 triangles); an independently swept identical full path also fails (286126 triangles), despite zero measured geometric difference and zero outside-mask difference. The canonical pickup mesh itself also fails the same watertight check. These are preserved diagnostics. No mesh hole filling, geometry trimming or relaxed gate is used.

A separate controlled circular-ring tessellation follows the identical original/revised centerline and radii. Its explicit annular connectivity, actual exported mesh bounds and sampled distances to the actual STEP shell must pass before that alternate mesh is usable. The original native export remains unchanged. Rendering and final binding specify which mesh was reviewed.

## Delivery

Uninstalled bounded candidate on `engine/timing-drive-fit`; root owns PR/release/installation. Use `shifted_oil_pickup_candidate.build(old_world)` only with the bound canonical world tube. It returns world shape plus construction metadata. The integration replacement is local `cad/engine/generated/shifted-oil-pickup-candidate/oil-pickup-tube.step` and **`oil-pickup-tube-parametric.glb`**, preserving definition/occurrence `oil-pickup-tube` and original pickup assembly position `[210,56,−112]`. Do not substitute the rejected native `oil-pickup-tube.glb`. Pump/distributor/intermediate translations remain peer-owned in `timing-conditional-drive-integration-patch.json`; this candidate adds no assembly translation.

The alternate mesh has262400 triangles, watertight consistent winding/positive volume, bounds error0.000005861 mm,528 actual shell vertex samples (max0.000012531 mm) and512 chord midpoint samples (max0.007474331 mm). A0.2 mm radial control gives0.199999911 mm shell distance. This explicitly sampled geometric verification accompanies known circular-section construction; no continuous manufactured-tolerance claim. All native failures remain preserved.

Actual parametric mesh plus STEP insertion section is rendered in `pickup-parametric-review.png`; the prior native render remains separate. Images show the estimated tube route and nominal inserted wall, not a production contour comparison. The exactyear schematic supports topology only. Source drawings remain local restricted inputs, never copied into these deliverables.

Environment: macOS15.6.1 arm64, Python3.13.12/build123d0.10.0/OCP7.8.1.1.post1 in existing `.venv-cad`; system Python uses NumPy/Trimesh/Matplotlib for rendering. No packages installed. Model/usage unavailable. Commands from repository root:

```sh
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-shifted-oil-drive-connections.py
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/probe-shifted-oil-drive-inlet.py
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-shifted-oil-drive-mounts.py
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-shifted-oil-pickup-candidate.py
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-shifted-oil-pickup-contact.py
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/probe-shifted-oil-pickup-native-sweep.py
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/mesh-shifted-oil-pickup-parametric.py
PYTHONPATH=.venv-cad/lib/python3.13/site-packages MPLCONFIGDIR=/tmp/truck-mpl XDG_CACHE_HOME=/tmp/truck-cache python3 scripts/render-shifted-oil-pickup-candidate.py
PYTHONPATH=.venv-cad/lib/python3.13/site-packages MPLCONFIGDIR=/tmp/truck-mpl XDG_CACHE_HOME=/tmp/truck-cache python3 scripts/render-shifted-oil-pickup-parametric.py
python3 scripts/bind-shifted-oil-drive-connections.py
```

| Gate | Result and limit |
|---|---|
| Application/coverage | Scoped candidate; exactyear topology/service identity, estimated tube/mount dimensions |
| Dimensions/coordinates | PASS bounded: fixed sump, exact peerDELTA, unchanged radii, explicit3 mm insertion estimate |
| CAD/export | Valid single-solid STEP, roundtrip volume error3.47e-9 mm³; alternate mesh PASS; two native mesh FAILs preserved |
| Visual fidelity | Actual mesh/section reviewed; no production contour validation |
| Installed interfaces | Local insertion/support PASS; complete fluid circuit FAIL/incomplete: discharge/gasket/gallery and bell retention unresolved |
| Motion/disassembly | Static tube; pump rotor clearances checked at rest only, no new removal or whole-system study |
| Learning/diagnostics | Explicit stale-endpoint, absent insertion, shaft-shift and radius controls; no installed lesson migration |
| Browser | NOT RUN; no canonical installation |
| Reproduction/review | Bound inputs/artifacts and commands; root review/release pending |

Issue32 remains open. Code/candidate archival is separate from installation acceptance. Next action is root review of exact hashes and assembly composition, plus an independent source/contract task for the actual pump mounting gasket, discharge face and block gallery. No source-supported complete oil circuit is claimed. No running process after delivery.
