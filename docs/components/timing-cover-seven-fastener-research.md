# Component contract and handoff: seven timing-cover fasteners

## Contract

Issue #32 under engine #1; root owns integration. Research on `engine/timing-interface-integration`, baseline `70542fad9de467a5c03ad54a6f54def8550956eb`. Owned files: this handoff and `reference/engine/timing-cover-seven-fastener-research.json`. No geometry, canonical inventory or frozen inputs changed. Scope: identify evidence for seven main-cover screws and recessed seats, distinct from the five relocated pan screws and the front-seal work. Millimeter assembly axes and seven registered axes remain fixed. Cover attachment-v2, future block land, main gasket, front seal and pan are coordinated interfaces.

## Evidence ledger

Detailed source paths, hashes and limitations are in the research JSON. The exact-year service procedure identifies cover attaching screws but supplies no size, count or recess depth. Its torque table separately lists Front Cover at 12–18 ft lb and Timing Cover Attaching Bolts at 15–22 ft lb. This ambiguity is preserved; no torque is adopted. Older Ford industrial PDF page7 calls out382781-S near cover6019; page9 lists cover D2AZ-6019-A and gasket C8AZ-6020-A but no cover-bolt dimensions/count. It is comparison evidence only. Dorman635-109 manufacturer images support recessed perimeter pads, without calibrated seat depths. Existing model radius9 lands, radius4.2 holes and radius3.3 blind pockets are estimates, not verified thread specifications.

## Delivery

Research checkpoint only; no hardware BOM or CAD candidate accepted. The ledger supplies a parameterized seat/length/engagement contract and explicit unknowns. Existing seat X415 is unverified. For rearward bolt length L and seat Xs, tip= Xs−L and engagement=373−tip. Current blind pocket ends X366, so engagement must be below7mm less declared bottom clearance. An unverified7/8in comparison length at X415 does not reach the block; at the bare rear flange X377.8 it extends beyond the modeled floor. Neither seat can be justified simply by that catalog lead.

Station-specific seat, head/washer geometry, thread, length, engagement, pointer/bracket ownership and tool access remain unknown. A subsequent estimated candidate must declare these together and verify annular contact, cover continuity, gasket support, actual thread envelope and tip clearance. Root coordinates composition with the seal worker; its radial24..43/X406..434.4112 cover mask must remain separate from the seven mounting lands.

## Validation and review

Application/coverage: PARTIAL, exact-year procedure plus qualified comparisons. Dimensions/coordinates: existing dimensions recorded only; factory verification NOT RUN. Source/visual: manufacturer oblique cover and industrial pages7–11 reviewed; low-resolution EFI exploded image not transcribed. CAD/export, installed interfaces, motion and browser: NOT RUN, research has no geometry. Learning: N/A. Reproduction: input hashes and source URLs in JSON; no source originals added for distribution. PDF text extraction returned no useful text, so industrial transcription is visual. Renderer: local Poppler; no dependency changes. Model/effort/usage unavailable.

## Tracking and restart

Issue remains open. Hardware work paused for the coordinated pan/block transition. Next action: obtain an applicable bolt/station drawing or explicitly approve a joint estimated seat/fastener contract, then test in new candidate files. No processes remain from this research. Parent owns review, publication and issue updates.
