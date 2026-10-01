# Component contract and handoff: timing valvetrain adapter candidate

## Contract

- Issue32, root integration owner. Baseline8547c589d3c086bad91baf879219612bcd9a162f, branch engine/timing-support-joints. Manifest91950c89dc12c17d1169ec77eed16efa71919c6832061346582ee02b81599ad6. Frozen timing-valvetrain-contract is unchanged.
- Scope: common estimated rocker; all12 shifted lifter/pushrod branches; local head pedestal/passage candidate. No shared/canonical writes, production timing or installation claim.
- Own new cad/engine/timing_valvetrain_adapter_candidate.py, scripts/check-timing-valvetrain-adapter-candidate.py, inventory/engine/timing-valvetrain-adapter-candidate-validation.json, this handoff, ignored generated/timing-valvetrain-adapter-candidate.
- Preserve source-sized valves and pushrods byte-for-byte, valve axes/seats/guides, spherical fulcrum and ball contacts, rigid keyed-cam transform and compensated follower phase. Common pivot choice remains geometry-derived nominal intake comparison; exhaust residual explicit, no scaling.
- Head allowed material changes declared BEFORE construction: at each valve X, union of radius12.1 mm vertical cylinders centered at old/new pedestalY, localZ48.5–140 (world304–395.5). Optional pushrod passage region centered at candidateY95.109820990, radius7 mm, worldZ304–395.5 only. No changes below the head floor, including fire deck/head-gasket face; no valve-seat/guide, head-bolt or valve-cover flange changes. Exact change-mask containment and named protected-interface checks required.
- Mount/contact gates precede neighbors. Same0.002 mm contact,0.1 mm3 collision and1e-5 mm3 protected-difference thresholds as prior audits. Smooth existing bolt shanks cannot establish true thread engagement; quantify geometric insertion and label missing thread verification.
- Known possible blocker: retained lower passageY90/R6 may foul shifted pushrod. Preserve failure and map it against gasket/block/sealing lands before proposing any lower allowed-region expansion. Root explicitly requires separate review of that coordinated interface.
- Inputs available: frozen phase-contract module/report and coupled cam STEP; canonical head/rocker hardware/lifter/pushrod/valve meshes/STEP/manifest; block worker new candidate2880d7873e14c8407d40b219d06753be554c069db51da3bdf2ef300724544cfb remains uninstalled and separately reviewed.

## Evidence and acceptance

Source sizes and hypothetical profile are inherited as described in timing-valvetrain-contract.md. All new rocker/pedestal/passage shape is estimated. Actual mounting, contact, exports and protected changes first; subsequent sweep/neighbor/piston gates remain NOT RUN until then. No browser or installation scope. Usage unavailable.

## Delivery — frozen pedestal-only V2, passage scope rejected

Root requested preservation of the failed upper-passage trial and freezing the pedestal-only candidate before any further passage revision. No canonical/shared/frozen prior-study files changed. Current scope is **candidate with an unresolved physical interface**, not integration-ready.

The first upper-only passage trial is retained at `cad/engine/generated/timing-valvetrain-adapter-candidate/rejected-upper-passage-v1/` with its source/checker/report and STEP files. Although inside the initially declared optional passage mask, its cut removed **279.105585 mm³** from the current +Y valve-cover support ledge. That violates the separate protected-interface requirement; the trial is rejected. V2 removes the optional passage region entirely and changes only the twelve pedestal neighborhoods above worldZ304. All passages and cover lands remain unchanged. Exact added/removed material outside the narrowed masks is zero. This narrowing is not a relaxed acceptance threshold.

### Delivered files and commands

- Adapter module: `cad/engine/timing_valvetrain_adapter_candidate.py`; APIs `rocker()`, `head_adapter(old, manifest)`, `allowed_regions(manifest)`, `poses(manifest, theta=0, axial=0)`. Generator function globals are copied; baseline module globals remain unchanged.
- Mount/contact and protected changes: `.venv-cad/bin/python scripts/check-timing-valvetrain-adapter-candidate.py`.
- Independent lower interface map: `.venv-cad/bin/python scripts/check-timing-valvetrain-passage-contract.py`.
- Sampled piston envelope: `.venv-cad/bin/python scripts/check-timing-valvetrain-piston-envelope.py`.
- Exact rocker contact neighborhoods: `.venv-cad/bin/python scripts/check-timing-valvetrain-rocker-interfaces.py`.
- Exports/render: `PYTHONPATH=.venv-cad/lib/python3.13/site-packages MPLCONFIGDIR=/tmp/truck-mpl XDG_CACHE_HOME=/tmp/truck-cache python3 scripts/render-timing-valvetrain-adapter-candidate.py`.
- Active ignored output: `cad/engine/generated/timing-valvetrain-adapter-candidate/pedestal-only-v2/`. Actual reviewed worker image: `adapter-comparison.png`; model comparison only, not a manufacturer/source-photo comparison.
- macOS / Python3.13 / build123d0.10.0 / OCP7.8.1.1.post1 / trimesh4.7.4. No new dependency installation. Model/effort and usage unavailable.

### Results

| Gate | Result | Evidence / limitation |
|---|---|---|
| CAD and protected head regions | PASS | One valid head and rocker solid; STEP roundtrip; zero changed material outside pedestal masks |
| Spherical interfaces | PASS | Zero symmetric difference in fulcrumR15.05 neighborhood, aligned socketRball+0.05 neighborhood and aligned lower pad patch |
| Actual mounting support | PASS geometric stack | Twelve guide/head, guide/fulcrum and bolt/fulcrum contacts; complete support annuli; zero bolt/head overlap |
| Thread engagement | NOT MODELED | Existing smooth shank inserts15 mm into smooth bore with0.1 mm radial clearance; cannot certify physical thread engagement/preload |
| Linkage contacts | PASS sampled |120 actual poses, twelve branches × five event-relative phases × two axial endpoints; preserved source-sized valves/pushrods |
| Export integrity | PASS | Watertight rocker3,602 triangles and head82,194; maximum bounds errors below0.000006 mm |
| Head/gasket passage | FAIL | All twelve branches have independent strict interior collision witnesses; see Boolean caveat below |
| Block deck support | FAIL proposed small-hole stack | EntireR6–R8 support annulus lies over the supplied migrated block's larger through-guide opening |
| Valve/piston | PASS sampled envelope |1,442 samples per branch: integer crank0–720, axial0/-0.1; minimum separating Z envelope6.747394868 mm; not continuous proof |
| Broader neighbor/spring/cover sweep | NOT RUN | Passage contract is physically inconsistent; root deferred unrestricted checking until coordinated scope is selected |
| Source shape / browser / installation | NOT RUN | Estimated new rocker/pedestal; no production identity or installation claim |

The common-rocker choice and explicit intake/exhaust lift residuals remain exactly those in the frozen contract. It does not scale the lift law. All lifters/pushrods retain the coupled phase argument; the gear never slips independently of the keyed cam group.

Mount sensitivity: raising each guide0.1 mm opens a0.1 mm support gap. Piston sensitivity: a further10 mm valve drop makes the sampled separating bound negative; this proves bound sensitivity, not exact fault-overlap volume. The exact rocker neighborhoods retain original local contact geometry despite changed arm spans/socket position.

### Exact reports and artifacts

- Adapter report SHA-256: **4e62912eec25b0f79e725a97c21bd403afaea3cd606938effe73e1b04c7e644b** (`inventory/engine/timing-valvetrain-adapter-candidate-validation.json`). Its overall FAIL is retained; zero exhaust Boolean volumes are not clearance evidence.
- Passage map SHA-256: **82196d978c10ccbf4bfbf18775e0cf4852618b1862f0f38253d9c5e4ccbbf5f6** (`inventory/engine/timing-valvetrain-passage-contract-validation.json`). This adds independent strict interior witnesses and rejected cover-land loss.
- Sampled piston report SHA-256: **cbac8fc9c205b10e0a3087aaec76c20844d2e0aa6b1bec3a841779231897a339** (`inventory/engine/timing-valvetrain-piston-envelope-validation.json`).
- Additional reports: `inventory/engine/timing-valvetrain-rocker-interfaces-validation.json`, `inventory/engine/timing-valvetrain-adapter-export-validation.json`; each binds its actual STEP inputs.
- Rocker STEP **0458f167570e4393153828f5e00e8ea98f17e1a4cc4869618a27421fa4df4a2b**; GLB **bb9740c62aff8c362864718df7b3cba14a560408fae0f7febe38cf82e5ccb58e**.
- Head STEP **d5776d25ecd3ce4b3ad413b8e876af54e7f71b9f2bfdca44663458e8b7799f6e**; GLB **cc40acd93092c5025cbd2d3e8d32cb757f71ec22173156eea88794662dcb101a**.
- Actual render **10a19a1ba061c5ace329af1f87e60fa9b27177934b2db832cb82389e3a9cc2a5**.

### Boolean false negative and physical failure

At a rest event, six intake rods overlap the unchanged lower head by1,526.886681 mm³ each and the head gasket by31.415839 mm³ each. The exhaust rod has a tiny modeled tilt; OCC `intersect` unexpectedly returnsNone despite points strictly inside both solids. For every station, `(stationX+2,98,254.75)` lies inside both pushrod and gasket; `(stationX+2,98,280)` lies inside both pushrod and head. These are away from their boundaries, not tangent tests. The map records all twelve witnesses and explicitly flags the false negatives. Do not inherit a zero-volume exhaust clearance result. Future nearly parallel rod passage checks need independent support/section or interior-witness controls.

V2 changes nothing below worldZ304; those lower-head witnesses therefore apply unchanged to the candidate. The initial restricted upper trial reduced intake head overlap to1,015.778803 mm³ but could not remove the lower collision and damaged cover support; it is not a viable partial fix.

## Coordinated physical interface proposal — no cuts authorized here

A simple vertical drilling cannot solve this stack while retaining all present interfaces. At the candidate rest axisY95.109821, a radius6 geometric study aperture would be40.840623 mm from the nearest modeled combustion aperture,29.514902 mm from the nearest head-bolt aperture and7.890179 mm from the +Y gasket outer edge. These distances describe the current model only. The head/gasket have no traced coolant network; no production coolant separation can be asserted.

The smallest coherent **scope for review**, before choosing dimensions, must include:

1. All twelve lower head passages and matching head-gasket apertures, with protected combustion/valve-seat/guide/head-bolt lands and an explicit minimum remaining sealing/support region.
2. The block deck termination of the lifter guide. The supplied migrated guide radius11.124565 continues to the deck. A smallR6 gasket opening bridges that larger void; exactR6–R8 deck probes have all0.879645943 mm³ missing. Either the deck needs a separately modeled smaller pushrod transition above the lifter guide, or the head/gasket interface must acknowledge the larger opening and its narrow outer land. That choice requires coordinated block ownership and source review, not hidden infill by this worker.
3. Upper head exit and +Y valve-cover gasket/cover base. Existing gasket land isY98–104; the shifted rod reachesY99.0722 at rest and the candidateR6 clearance envelope reachesY101.1098. A new hole intrudes into that land. Moving/widening that local cover interface or revising the motion/shape assumptions needs a separately declared scope; simply narrowing the gasket without evidence is not accepted.
4. Fresh swept envelopes through the approved interface, independent checks sensitive to the observed Boolean failure, and contact/support continuity at both gasket faces. Retain existing source-sized rods, valve axes and accepted spherical contacts unless a new source-backed contract explicitly changes them.

The reviewed ledger `reference/engine/fel-pro-vin-y-gaskets-reviewed.json` identifies Fel-Pro8168 PT /525 SD as alternative replacement head gaskets for the applicable1991–1997 VIN-Y4.9L application. It supplies no passage dimensions and does not authorize transferring an unregistered photograph's holes by eye. Root is reviewing source gasket shape before selecting the next scope.

No further passage cutting or broad sweep execution is running. Root review of the physical interface map is the next action. This candidate can be preserved as evidence; it is not ready to install or mark Done.
