# Component contract and handoff: composed corrected cam drive

## Contract before modeling

Issues #32/#34, root integration owner, pan_access_resume contributor; coordinated with inclined_linkage_resume. Creation baseline26d0fdc4e7cdd3de0c621309499d1535d8c5131e on engine/timing-drive-fit. Separate candidate only. Own new cam_composed_drive_candidate module, check/export/render scripts, reports and generated/cam-composed-drive-candidate. No frozen source, asset, occurrence or shared transform edits.

Input corrected-lobe local cam SHA81933607c28c521f8f077239e16174a5d718c9aec0f1e4450ac041b1931fbc68 and corrected gear local STEP SHAa8c0288344579f739983e3b7a29858c4806f364351917be11b3cf82bf5b23b29. Local shaft Y=Z=0, millimeters, +X axis. World placement Pos(0,95.1098209901611,76.08785679212888). Existing camshaft identity, parent and explode remain integration-owned.

Analytic replacement mask is X221.584..233.584 and radius15..(18+2*18*cos45°/16), the original/corrected modeled gear tip radius. Keep R15 shaft core throughout. Subtract only that annulus; union the frozen corrected gear at X227.584. No neighbor subtraction, fullshaft mirror, lobe adjustment or extra phase. Preserve every surface outside that exact mask and original core material. All gear dimensions, lead and source approximation retain their existing estimated classification.

Acceptance: valid single solid/shaft continuity, exact outside-mask two-way difference <1e−5mm³, gear-window match <1e−5mm³, STEP roundtrip difference <0.001mm³ and actual local/world mesh bounds <0.15mm as prior cam export. Supplement fragile coincident Boolean metrics with independent actual BRep cross-sections at all12 lobe centers and shaft/gear borders, 4096-point boundary distance <0.002mm and area error <0.02mm²; retain any failures. Core-point/notch and wrong-gear controls must detect faults. Rebind prior lobe contact and corrected-pair/endplay proofs only through unchanged exact geometry/pose APIs and valid input hashes. Do not call inherited full-assembly collision, browser, manufacturing or pressure checks passed.

## Delivery

Candidate only; no canonical writes. API `cam_composed_drive_candidate.build()` returns the composed definition-local cam. Source input hashes are hard guards; world diagnostic asset is translated once by Pos(0,*AXIS). Use local STEP/GLB for the existing `camshaft` definition and retain the corrected rigid cam parent +q/2+degrees(K*x). The new endplay API remains gear-centered: its cam frame applied to a fullcam requires first Pos(−227.584,0,0), whereas the existing fullcam parent works directly. Do not apply both offsets/rotations.

Assets under `cad/engine/generated/cam-composed-drive-candidate/`:

- `camshaft-local.step`:58434e1a4a96b1cf9fef0075277ed3a114ff90ac2a5093b5956c6cb305c84c38
- `camshaft.step` (world diagnostic):87b9d4053d26af8ca663eb92fcc5960fc4d77188a384f5877bfe36993b9e3a65
- `camshaft-local.glb`:8c0b13698e6122da1d341791965427d3755866dd69776a367cd4f526cd311a77
- `cam-composed-drive-review.png`: actual exported mesh overview and old/new tooth-region comparison. Source gear lead differs, preserved shaft and lobes remain visible. Worker inspected; root review pending.

Build/export result: valid single solid, exact outside-mask symmetric difference0mm³, exact actual gear-window difference0mm³, R15 core missing0mm³, world/local STEP roundtrip difference0mm³. Protected shaft notch control detects0.523598775598mm³. Actual composed STEP has304 positive-lead helical edges, slopes .05555555101054... .05555555101064rad/mm. Mesh37,432 triangles, watertight/winding-consistent/positive volume; local/world bounds error0.00796416mm. Existing0.15mm mesh bound and strict geometric thresholds unchanged.

Evidence classes: corrected cam lobes inherit the qualified source profile and existing limitations; crossed-drive16teeth/R18/12mm-face/involute approximation remain estimates. This is a functional phase/lead composition, not a new Ford production specification or factory visual-fidelity claim. All journal, lobe, keyed nose, retention and end surfaces outside the exact mask remain as supplied.

Commands from repository root, macOS Python3.13/build123d0.10 in `.venv-cad`; system Python provides matplotlib. No installs or external temporary inputs. Runtime cache warnings do not alter geometry.

```
.venv-cad/bin/python scripts/check-cam-composed-drive.py
.venv-cad/bin/python scripts/check-cam-composed-drive-sections.py
.venv-cad/bin/python scripts/check-cam-composed-drive-pair.py
python3 scripts/render-cam-composed-drive.py
python3 scripts/bind-cam-composed-drive-proof.py
```

Reports are `inventory/engine/cam-composed-drive-{build-review,section-review,pair-review,render-review,proof-binding}.json`. Artifact distribution/root release URL pending. Scripts, source/module dependencies and STEP/GLB/visual hashes are bound by these reports. Creation baseline and canonical manifest unchanged; root may publish as a separate preservation checkpoint. Model/effort/usage unavailable.

## Final validation and review

Independent actual BRep sections: all12 corrected-lobe centers have0 boundary/area difference from the frozen corrected cam. Gear sections at the center and0.001mm inside both axial boundaries agree with the frozen corrected gear within1.52e−11mm sampled boundary distance; shaft sections0.001mm outside both boundaries have0 difference. All1,008 strict inset R15 core points across the joins are inside the composed shaft. Old tooth lead fault differs0.95886443mm at the off-center section, so the section comparison detects an unchanged wrong gear.

Two new fullcam/distributor checks at event11.25° and axial0/−0.1mm give0 overlap and0.170194060643/0.169862124250mm separation. These use the entire cam, not a clipped tooth blank, and the exact frozen endplay phase API. They do not cover all engine neighbors or continuous motion.

Proof binding verifies all source-cam delivery/transitive hashes plus new build/section/pair/render reports and frozen pair/endplay reports. Previous120 localized cam/lifter checks apply to geometrically unchanged clipped lobes: every previous lobe clip is disjoint from the gear change mask. The17 corrected gear snapshots and9 endplay snapshots apply to the identical corrected gear window with unchanged pose APIs. This is narrowly scoped evidence reuse, not silently rerunning all poses or treating wholecam neighbors as checked. Previous limitations remain visible.

| Quality gate | Result | Remaining scope |
|---|---|---|
| Application/coverage | Candidate only; factory identity NOT RUN | source profile and estimated gear geometry retain original limits |
| Dimensions/coordinates | PASS | explicit definition-local and world frames; source dimensions unchanged |
| CAD/export | PASS | one valid connected solid; material/roundtrip/bounds and watertight mesh checks |
| Source/visual comparison | PASS model-source comparison; factory comparison NOT RUN | actual old/new mesh closeups; independent source sections; root review pending |
| Installed interfaces | PASS declared core/lobe preservation and two fullcam/distributor samples | other combined engine neighbors NOT RUN here |
| Motion/disassembly | PASS scoped existing proof binding and new snapshots | continuous whole-engine motion/removal NOT RUN |
| Learning/diagnostics | NOT RUN | no new lesson; CAD fault controls are interface evidence |
| Browser integration | NOT RUN | isolated assets only; root owns adoption |
| Reproduction/review | PASS local hash binding; root acceptance pending | publication/restoration and installed browser checks remain root-owned |

## Tracking and restart

Bounded composition complete; no process remains. Root next action: review `cam-composed-drive-review.png` and use exact local STEP/GLB hashes for coordinated canonical staging with corrected crank, gear pair, endplay law and inclined linkages. Preserve original `camshaft` ID and avoid double world translation. Full installed acceptance remains open on #32/#34. No earlier failure or frozen file was changed. No billing/model-effort estimates supplied.
