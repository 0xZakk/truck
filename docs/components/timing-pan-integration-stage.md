# Pan and fastener integration stage

## Contract before staging

Issues #32/#34 under Engine #1, root-owned eventual canonical integration. Work begins after PR102 checkpoint `dafb8175e4e7b328d2a16bdc47914307f044b0c8` on `engine/timing-motion-integration`. Own only the new staging script, staged assets, serialized patch proposal, validation report and this handoff. No canonical asset, shared manifest or builder writes.

Stage frozen pan v2 and molded gasket in their existing canonical local frames. Keep stable definition/occurrence IDs and parents. Use the actual threaded screw candidate and existing washers; move only five screw/washer occurrence pairs using attachment-v2 world datums, explicitly converted to parent-local coordinates. Preserve all other occurrence fields and all20 retained poses. Definition replacement of the shared screw affects all25 occurrences and must carry their valid evidence.

Validation: guarded manifest/source/evidence hashes; actual localized STEP roundtrip and reconstructed world bounds/shape metrics; inverse GLB coordinate mapping and full vertex reconstruction; all25 occurrence datum checks and five world fastener witnesses; reuse pose-specific pan/backing/tool evidence only when direct inputs still match. Produce a usable serialized patch with before values and staged-to-canonical asset instructions. Preserve unresolved overhang, rear-owner architecture, production dimensions, compression/containment and browser gates. No promotion or installed claim.

## Delivery

The usable proposal is `inventory/engine/timing-pan-integration-patch.json`, schema `truck-guarded-integration-proposal-v1`. It carries the manifest SHA256, exact before/after definition/occurrence objects, and staged-asset copy instructions with hashes. The canonical destination paths remain stable. Root must reject stale before values or hashes, copy the local staged assets and apply the ten poses together with the coordinated block/cover changes. This script does not apply that promotion.

Staged assets are in `cad/engine/generated/timing-pan-integration-stage/`:

- `oil-pan.step/.glb`: inverse of existing oil-pan world frame (translation0,−12,−96mm), preserving original occurrence and parent.
- `oil-pan-molded-gasket.step/.glb`: existing identity frame, original occurrence and parent preserved.
- `oil-pan-mounting-screw.step/.glb`: actual threaded source definition, shared by all25 screws. All20 retained poses remain exact; only five front poses change.
- `oil-pan-mounting-washer.step/.glb`: existing canonical washer, retained for evidence; **washer definition is not patched**. Exact two-way Boolean differences versus the frozen candidate's existing washer are zero. Canonical washer GLB has duplicated shading-seam vertices: raw mesh is not index-watertight, welded verification copy is watertight. Staged mesh preserves original face/vertex reconstruction rather than silently replacing the canonical washer with a different tessellation.

Five world datums, used for both screw and washer, converted through each actual parent transform:

| Station | World XYZ mm |
|---|---|
|20|365.5,−132,−32.1|
|10|365.5,196,−32.1|
|21|390,−110,−32.1|
|23|390,0,−67|
|22|390,180,−32.1|

Existing parents, IDs, occurrence metadata and explosion stages remain unchanged. Explosion/removal for the full assembled engine is **not revalidated** by preserving those fields. Prior nominal axial socket/path evidence retains its original limited scope.

## Validation and evidence reuse

`inventory/engine/timing-pan-integration-stage-validation.json` binds75 inputs, including the manifest, relevant source modules, reviewed STEP/GLB files and existing pan/pair/contact reports. Each directly bound report input is checked before reuse. Pan report's old aggregate FAIL is explicitly retained; the obsolete future-land collision is not relabeled. The matching block v3 paired report is separately reused. The20 retained and five revised hardware/washer seats and nominal access gates are reused only after their actual source hashes and all50 final hardware world datums match. Each revised world hardware STEP additionally matches the reconstructed staged shape bounds, face count and volume.

All four local STEP exports are valid with original solid/face counts. Restoring their source frames yields zero STEP bounds error. Pan GLB vertex reconstruction error is0.000005484mm; gasket/screw/washer errors are zero. Maximum STEP roundtrip volume difference is0.0000864334mm³ for the threaded screw; this is a serialization check, not a new acceptance of total-engine volume metrics.

`inventory/engine/timing-pan-integration-patch-replay.json` independently reloads the serialized proposal, applies it **in memory**, checks all52 pan/gasket/screw/washer world mesh-to-STEP bounds within0.025mm, and confirms every unpatched occurrence is unchanged. Three negative controls reject stale manifest binding, wrong before-pose and changed staged-asset hash. Coordinate controls detect96mm double pan placement and21.5mm use of the old station20 position.

The proposed metadata appends limitations to the existing source uncertainties; it does not claim the new contours, sealing pressure, rear cap architecture or production dimensions are verified. Original upper/lower full-face backing failures remain in their reports. All contact/containment distinctions are carried forward.

## Commands, environment and review

From repository root:

```sh
.venv-cad/bin/python scripts/stage-timing-pan-assets.py
.venv-cad/bin/python scripts/verify-timing-pan-integration-patch.py
```

Existing macOS Python3.13/build123d0.10/trimesh/numpy, no new dependencies. Reuses `assembly_math.transforms` and the front-seal staging approach. All paths are repository-relative in the proposal/report. Assets not released by this worker. Model/effort/usage unavailable.

| Gate | Result and scope |
|---|---|
| Application/coverage | Uninstalled integration stage; stable four definition IDs and52 occurrences |
| Dimensions/coordinates | PASS inverse local frames, all50 hardware world datums and52 STEP/mesh reconstructions |
| CAD/export | PASS serialized solids, faces, bounds, mesh topology with explicit washer seam qualification |
| Source/visual | Reviewed frozen pan/gasket visuals reused by unchanged geometry/input hashes; no new factory fidelity claim |
| Installed interfaces | Existing bounded hardware/contact proofs reused under valid hashes; no combined installed verdict |
| Motion/disassembly | NOT RUN whole-engine motion/explosion; existing stages retained, nominal prior access scope only |
| Learning/diagnostics | NOT RUN new user-facing lesson |
| Browser integration | NOT RUN, no canonical promotion |
| Reproduction/review | PASS guarded serialized patch replay and three rejected corruptions; root review pending |

## Stop and next action

Stage complete, no running process and no canonical writes. Root owns review, asset publication and coordinated manifest application. Apply with matching block v3,2692 cover/seal stage and other root-owned dependency changes; then perform combined assembly and browser acceptance. #32/#34 remain open. This stage is usable preparation, not installed acceptance or whole-fluid-containment proof.
