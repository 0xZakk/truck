# Component contract and handoff: timing-cover-attachment-v2

## Contract

Issue #32 / Engine #1. Root is integration owner. Baseline `8547c589d3c086bad91baf879219612bcd9a162f`, branch `engine/timing-support-joints`; current manifest bound by the checker. Scope is an isolated attachment revision, not installation. Freeze prior front joint, rejected attachment and accepted reusable male proofs.

Own `cad/engine/timing_cover_attachment_v2.py`, `scripts/check-timing-cover-attachment-v2.py`, corresponding renderer, review/validation JSON, this handoff and generated `timing-cover-attachment-v2/` outputs. No shared builder, canonical block, pan, seal or fastener occurrence changes.

Reuse the accepted nominal 5/16-18 × 0.87 in male at five proposed stations: IDs 20, 10, 21, 23, 22. Regenerate only local female socket interiors as estimated zero-clearance educational threads. Preserve separate existing washers. Preserve all six frozen sealing parts outside five cylindrical socket regions; main-cover hardware and unsupported uniform boss heights remain excluded.

CAD units and world frame remain millimeters; screws point +Z. Proposed transforms are inherited from the frozen joint. Audit all 25 existing canonical locations with the new reusable male and unchanged transforms; 20 of those also remain unchanged in the proposed assembly. Existing smooth sockets are not evidence of thread retention.

Checks: normalized plain solids and explicit empty-result guards; valid single casting solids and watertight export; actual flank contact area and engagement, tip clearance and wall support; matched rotation/advance and wrong-phase controls; zero unintended overlap; unchanged seal faces via bounded material differences; actual render. Existing main-cover hardware, production thread class, preload/strength, learning and installed/browser acceptance remain outside the local acceptance claim.

## Evidence ledger

| Feature | Value / evidence | Classification and limit |
|---|---|---|
| Pan screws and washers | 25 assemblies, 5/16-18 × 0.87 in; 1994 Fig. 34 / 350379654 | Exact-year nominal callout; source ledger `reference/engine/ford-oil-pan-hardware-reviewed.json` |
| Reusable male | Frozen accepted isolated candidate, nominal diameter 7.9375 mm and length 22.098 mm | Detailed root, crest, runout and head/washer dimensions remain estimates |
| Female thread | Exact conjugate of the accepted male, Z = 7.8 through 22.0 relative to its under-head plane | Ideal zero-clearance teaching form; no manufacturing thread class |
| Front socket stations | Five positions inherited from the accepted local sealing candidate | Coordinated model estimates; not factory measurements |
| Existing canonical sockets | Existing smooth bore geometry | Clearance cannot establish female-thread retention |

## Delivery

**FAIL, frozen candidate.** No installation or local attachment acceptance. APIs: `build()` returns revised parts, frozen originals, five screw/washer occurrences, reusable definitions and socket ownership. Run `.venv-cad/bin/python scripts/check-timing-cover-attachment-v2.py`, then `python3 scripts/render-timing-cover-attachment-v2.py`. Actual outputs and console log are under `cad/engine/generated/timing-cover-attachment-v2/`; report is `inventory/engine/timing-cover-attachment-v2-validation.json`. Review ledger binds hashes. No asset release published.

All five actual sockets have 402.9465 mm² positive flank contact, zero nominal male/owner overlap and contact distance, 14.2 mm engagement, complete wall/floor support and 0.502 mm clear tip reserve. Matched quarter-turn advance has zero overlap; wrong axial phase gives about 51.1884 mm³ interference. All exported solids are valid and meshes watertight. Only bounded socket material was added: cover 609.7136 mm³, future land 406.4758 mm³. Nothing was removed; all material outside socket regions and all four remaining sealing parts are unchanged.

The failure is actual interference with the frozen pan wall. Station 10 screw/washer overlaps are 27.3217 / 9.6992 mm³. Stations 21, 23 and 22 each overlap by 49.9371 / 30.9748 mm³. Their head/washer seat support passes, but nearby vertical pan walls cross their dry-side volume. The actual center section shows this at X395. Positive thread contact cannot waive these collisions.

Separately, all 25 current canonical positions accept the reusable male with zero pan/block/washer overlap and complete existing head/washer/pan support. Block distance is approximately 0.18119 mm everywhere, reflecting the smooth bore clearance. This is not female thread retention. No transform changed; 20 positions remain unchanged in the proposed joint.


## Validation and review

Predeclared tolerances are in `reference/engine/timing-cover-attachment-v2-review.json`. Numerical overlap uses the existing 0.1 mm³ convention; bounded material differences use 0.01 mm³. These are CAD audit tolerances, not manufacturing specifications. Contact requires over 1 mm² of shared flank face and distance below 0.00001 mm. Fault control advances the male 0.3 mm without rotation; the matched control rotates 90 degrees and advances one-quarter pitch.

Shared contact is measured against the actual modified casting faces. Faces with absolute Z-normal component between 0.1 and 0.99 count toward flank area, excluding cylindrical crests/roots and planar axial ends. This is a geometric contact classifier, not a load distribution calculation. A 6.2 mm outer-radius annulus checks the declared local wall envelope; it does not certify casting strength.

The accepted reusable male report independently verifies wrong-phase interference with interior-point classification. This study binds that frozen input proof and checks the five actual sockets. The Boolean wrapper rejects failed kernel operations, handles genuinely empty results explicitly, and normalizes imported shapes into plain solids without assembly child metadata.

## Tracking and restart

Issue #32 remains open. No candidate is installed. Checker finished; preserved log is `cad/engine/generated/timing-cover-attachment-v2/validation-console.txt`. No process remains running. An additional temporary point-classifier probe was stopped after the full report localized the actual collisions to the pan; it is not acceptance evidence. Model/effort and billing usage unavailable. Environment is the existing macOS CAD environment, Python 3.13.12, build123d 0.10.0 and trimesh 4.7.4. Renderer uses system Python with NumPy/Matplotlib. No dependency pins changed.


### Final gate record

| Gate | Status | Scope / remaining limit |
|---|---|---|
| Application / dimensions | PASS, bounded | Nominal source callout; explicit profile and station estimates |
| CAD / export | PASS | Valid intended solids, watertight STEP-roundtrip meshes |
| Visual fidelity | PASS for diagnostic review | Actual sections show matching threads and pan-wall collision; no factory stamping fidelity claim |
| Installed interfaces | FAIL | Four relocated heads/washers collide with pan walls |
| Motion / disassembly | PASS for thread control only; full removal NOT RUN | Matched advance and wrong-phase controls work; tool access unresolved |
| Learning / diagnostics | NOT RUN | No user-facing component lesson delivered |
| Browser integration | NOT RUN | Candidate remains uninstalled |
| Reproduction / review | PASS locally; root reviewed failure | Inputs and output hashes preserved; root requests separate dry-side recess proposal |

Root accepted this diagnosis and requested a new bounded estimated stamping study, keeping fixed stations, full seats and a continuous oil boundary. The next design must construct a coherent wall recess, not subtract neighboring solids blindly. Preserve this revision and its failures unchanged. The canonical 25-position reuse audit may be reused only with unchanged bound inputs.
