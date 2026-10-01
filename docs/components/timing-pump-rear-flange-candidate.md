# Component contract and handoff: timing-pump-rear-flange-candidate

## Contract

Issue32/47; pump_foot_resume worker, root integration owner. Baseline8c2d2d9a1400acf784e04581a61e6a6ede38d3ba, branch engine/timing-drive-fit; canonical manifest91950c89dc12c17d1169ec77eed16efa71919c6832061346582ee02b81599ad6. Root authorized the bounded inferred contour in `timing-pump-rear-flange-contract.md`. All original geometry/failures remain frozen. Owned module `cad/engine/timing_pump_rear_flange_candidate.py`, new rear-flange scripts/reports/asset folder and this handoff only. No canonical or private-stage modifications.

Scope: refine lower pump exterior lug cap and adjacent cover/main-gasket edge using declared analytic masks, preserve axes/core/2692/seven main-hole interfaces, export four separate physical parts. No block, pan, terminal sealant, rotating part or forward inlet edit. All unitsmm; exportedSTEP/GLB are world coordinates and require inverse existing occurrence frames before any future integration. Do not copy these world assets over canonical local definitions.

Evidence: applicable topology and unknown dimensions are in the bound contract source ledger. NewR8.75 exterior cap andR66.25 separation boundary are engineering estimates. They are not measured Ford contours or manufacturing clearances. Same replacement identities and existing physical ownership remain; neither gasket is duplicated or fused into a neighbor.

## Delivery

**FAIL overall; useful rear-fit candidate, not integration-ready.** Four valid one-solidSTEP and watertight one-componentGLBs saved in `cad/engine/generated/timing-pump-rear-flange-candidate/`: housing, pump-gasket, cover, main-gasket. API `timing_pump_rear_flange_candidate.build()` returns new/old shapes, analytic cutters, source paths, manifest and poses. It checks immutable input hashes. It never subtracts actual neighboring parts as cutters.

Reports:

- `inventory/engine/timing-pump-rear-flange-export.json`
- `inventory/engine/timing-pump-rear-flange-validation.json`
- `inventory/engine/timing-pump-rear-flange-access-evidence.json`
- `inventory/engine/timing-pump-rear-flange-visual-review.json`
- `inventory/engine/timing-pump-rear-flange-strip-topology.json`
- `inventory/engine/timing-pump-rear-flange-delivery.json` binds all five reports and every asset.

Actual saved-mesh rendering and rear sections: `cad/engine/generated/timing-pump-rear-flange-candidate/review.png`. Worker reviewed both views. Original source photos remain in excluded research storage; no source originals redistributed. Release packaging pending root.

```sh
.venv-cad/bin/python scripts/build-timing-pump-rear-flange-candidate.py
.venv-cad/bin/python scripts/check-timing-pump-rear-flange-candidate.py
.venv-cad/bin/python scripts/check-timing-pump-rear-flange-access-evidence.py
.venv-cad/bin/python scripts/check-timing-pump-rear-flange-strip-topology.py
.venv-cad/bin/python scripts/render-timing-pump-rear-flange-candidate.py --extract
MPLCONFIGDIR=/tmp/truck-gear-mpl python3 scripts/render-timing-pump-rear-flange-candidate.py
python3 scripts/check-timing-pump-rear-flange-delivery.py
```

macOS/Python3.13.12/build123d0.10.0/trimesh4.7.4; rendering uses systemNumPy/Matplotlib. No Shapely dependency; the strip check uses exact planar CAD offsets. Generated build/check/access logs are retained. STEP regeneration changes serialization hashes; rerun dependent checks before review. Usage/model billing unavailable.

## Results and sensitivity

Rear housing/cover overlap0; cover/pump-gasket0; main/pump-gasket0. Every planar mating face of both new gaskets is completely supported: main gasket11506.165723mm² on each owner and pump gasket2877.391093mm² on each owner, missing area0. Exact1.52mm inward planar offsets leave both gaskets connected; all7 main-gasket holes and6 pump-gasket openings remain. Connected eroded stock alone is insufficient: the stricter `timing-pump-rear-flange-strip-topology.json` proves the main gasket retains all7 independent holes after erosion, but the pump gasket merges6 openings into2 in both baseline and candidate. Therefore the3.04mm closed separation-strip gate FAILS for the inherited pump gasket. No threshold was lowered; pressure and production tolerance remain unproven.

All7 actual main screws remain clear of cover/block/pump at their installed positions. Complete estimatedR8.75 headseats andR9 rear lands remain unchanged. All4 pump screws remain physically clear; required head-bearing faces are fully supported. The raw whole-headface check initially reports7.822566mm² missing on every pump screw. The supplemental report proves this is the unchangedR4shaft-toR4.3clearance annulus, not lost bearing stock. Excluding only that declared hole leaves88.270245mm² actual bearing contact, missing0 on old and new housing. The raw diagnostic remains preserved.

The geometric margin0.155634mm protects the whole main3R9 land against theR66.25 boundary. It does not establish robust production fit. Increasing the boundary radius by0.16mm removes0.009189mm³ from theR9 guard. Increasing it0.5mm removes6.409674mm³ from that guard and0.003037mm³ from the actual required headseat witness. The headseat has a larger nominal radial margin0.405634mm, but neither margin survives all plausible unmeasured-source variations. The fixed-mask candidate passes only at its explicitly estimated parameters.

Exact signed differences show no added material and no removed material outside the declared masks. New collision cannot be introduced by these subtractive edits at unchanged poses, but retention/support still needs its separate guards. Cover changes areZ≥90, disjoint from pan/terminal/2692 geometry; fitted core axes and all source thread cavities remain unchanged. No complete coolant-jacket or strength inference is made.

## Access failures and service ordering

The complete declared main3R10.5 tool cylinder still intersects the lower pump boss by61.107063mm³. Its actual screw is clear, and a conservativeR8.75 axial cylinder enclosing continuous screw withdrawal toX455 has zero pump overlap. Thus the physical screw corridor passes while the larger declared tool corridor fails. No tool radius was reduced.

Exact1994 front-cover service steps remove shroud/radiator, drive belt andPS/ACassembly, damper, then front screws/cover. They do not state a water-pump-removal prerequisite. The separate1994 pump service removes its fan/pulley/hoses and bolts. Historical1986 FordPDF70/printed21-11-17 similarly separates procedures and does not establish cover-before-pump removal. These sources do not justify treating the pump as absent to waive the blocked tool. They also do not specify a socket outside diameter. An independently source-supported tool or revised authorized interface is needed; no silent access exemption is applied.

Pump stations2/3 also fail the declaredR10.5 forward tool cylinders against their own housing:7604.417151 and504.587271mm³. The supplemental old/new comparison proves both are inherited unchanged failures. Stations1/4 tool corridors are clear. These tool cylinders are explicit envelopes, not proof no possible wrench can reach the bolts.

Forward inlet remains physically incompatible with the cover and with main4 access. Main4R10.5 tool intersection1454.951595mm³ is retained. Actual screw4 withdrawal samples are clear at0/10/20mm but collide by358.306800mm³ at+30mm and162.654452mm³ at+40mm. This is a real sampled removal obstruction, separate from the rear-flange repair. The bounding-cylinder positive overlap alone was not used to infer an actual screw collision.

## Quality gates and review

|Gate|Status|Scope and limit|
|---|---|---|
|Application/coverage|PASS limited candidate|Four original physical owners, source topology retained; dimensions inferred|
|Dimensions/coordinates|PASS nominal / robustness open|All axes fixed; sensitivity explicitly fails slightly larger boundary|
|CAD/export|PASS|Valid connected solids, watertightGLBs, bounds<0.025mm|
|Source/visual comparison|PASS limited|Source ledger and actual mesh/section review; no factory contour claim|
|Installed interfaces|PASS rearfit/contact; FAIL overall|Main3 tool, inherited pump tools and pump3.04mm separation topology fail; forward inlet remains|
|Motion/disassembly|FAIL incomplete|Main3 continuous screw corridor passes; main4 sampled withdrawal fails; no wholeengine claim|
|Learning/diagnostics|N/A geometry trial|Existing proposed screw/seal lessons retained; future accepted geometry requires new input binding|
|Browser integration|NOT RUN|No canonical installation; existing browser restriction remains|
|Reproduction/review|PASS local; root review pending|All input/report hashes current; direct exports and logs retained|

Next action: root review exact local results and remaining access/inlet constraints. Candidate must not be promoted solely because rear overlap is zero. Keep issue32/47 open. No processes running; no further geometry edits scheduled or implied.
