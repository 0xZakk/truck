# Pan gasket upper-side owner/contact study

## Contract before checking

Issues #32/#34 under Engine #1. Read-only research baseline `9ab3c57516bbe6d5f7cdb1e947b691b5f3ba768e`, branch `engine/timing-pan-seal-joints`. Pan worker owns only this handoff, separately named upper-contact checker/report and generated folder. No frozen source/STEP or shared file changes.

Question: which actual component supports each region of the gasket upper mating face, and where are actual gaps or broken owner transitions? Inputs are frozen pan gasket v2, block v3,2692 cover, attachment v2 main gasket/terminal sealant, and manifest-placed retained rear main cap/rear seal. Do not assume the rear cap owns the rear pan arch merely from physical expectation; map actual contact and record any illustrative owner mismatch. CAD coordinates are world millimeters; manifest transforms apply only to retained local definitions.

Plan: exact common/cut of actual upward mating faces against each owner's actual faces, with localized unsupported face exports and useful sections. Check the main-gasket/terminal-sealant transitions explicitly. If a real full-width gap exists, stop with its dimensions/owners. Any selected supported-route proof must distinguish overhang from a broken seal and retain full-face failures. No pressure/compression, whole-oil-containment or installation claim. No repeat of the lower-side graph unless required by a specific physical ambiguity.

## Actual owner map and bounded result

Delivery branch is now `engine/timing-motion-integration`, following root's PR102 checkpoint `dafb8175e4e7b328d2a16bdc47914307f044b0c8`. Study baseline above is retained. Frozen STEP hashes did not change.

| Actual upper-face owner | Shared upward-facing area mm² | Physical modeled role |
|---|---:|---|
| Block v3 |12324.4706876| Retained long-rail strips/pads, rear arch extension and revised X300..365 seat |
|2692 timing cover |12221.9432622| Front pan arch and front mounting land |
| Terminal sealant |316.9360229| Two explicit0.5mm terminal pockets crossing the block/main-gasket/cover junction |
| Main cover gasket |0| Direct pan-gasket distance0.5mm; modeled terminal sealant bridges this intended pocket |
| Retained rear main cap7 |0| AtX−341.376; nearest pan-gasket distance8.124mm. It does not own this model's rear arch |
| Rear crank seal |0| Nearest distance2.1mm; adjacent shaft seal, not modeled pan-gasket backing |

Upper upward-face total34972.2861712mm². Unsupported area is **10108.9362001mm²**, preserved as a full-face failure. This includes outer portions of both retained long rails/rear corners, nine small inboard pad overhangs on the left, and two2.5535585mm² rear transition slivers. Exact individual bounds/areas are in `timing-pan-upper-contact-review.json`; all unsupported faces haveX≤300. The revised front region has no unsupported upward face in this exact owner comparison.

The initial broad unsupported-area reading suggested a full-width left-rail gap. Exact section/witness evidence **rejects that interpretation**: atX±1, the complete11mm gasket strip Y−141..−130 has22mm² area, of which6mm² is backed. The surviving strip is **3mm wide atY−133..−130**. Each of nine retained left pads independently supports a2.5mm inboard witness Y−126.6..−124.1, width0.2mm inX, completely shared by gasket and block. Thus the inboard path continues around the mounting holes. Right-rail Y106..108 witness is also fully backed. A0.1mm shifted contact-plane control loses all shared face area; it is a face-match fault, not a pressure test.

At the front, terminal sealant shares135.1465392mm² with block,208.5800727mm² with cover and63.6312717mm² with main gasket. Both terminal footprints touch the pan gasket atZ−24.5. Their X371.8..375.8 bounds, source pocket geometry and actual X373.4 section explain the direct0.5mm main-gasket separation; it is not an unfilled junction gap.

## Continuity check and limits

To resolve the remaining physical ambiguity without repeating route optimization, join the actual owner contact surfaces, including290.6278699mm² of block-side vertical step contact and14.1501634mm² of cover-side vertical step contact. The sewed0.025mm tessellated surface has one connected face component, no nonmanifold edges,27 closed degree-two boundary loops and Euler−25. Twenty-five individual loops match all mounting axes within0.001mm; the other two surround the wet origin. This is an intact annular contact band with individually isolated fastener holes. A full-width transverse support-loss fixture across the left rail removes the enclosing boundary topology, yielding Euler−24 and zero enclosing boundary loops. It does not merely test surface connectivity, which stays one component after that fault.

This proves bounded upper-contact continuity in the modeled geometry; it does **not** specify a global minimum sealing width. The3mm/2.5mm widths above are exact local witnesses. No optimized lower-route result was reused as upper-side acceptance. Gasket compression, pressure distribution, material strength, factory dimensions and whole fluid containment remain unverified.

## Remaining defects / repair decision

1. Full upward-face support fails by10108.9362001mm²; those modeled overhangs remain explicit. They do not interrupt every continuous inboard contact route. No block-flange repair is justified by this study.
2. Rear-owner architecture is illustrative: `oil_pan_joint_v9_candidate.block_interface()` adds the rear pan arch to the block, while the retained generic rear cap is remote from that interface. This is an unresolved factory/component-ownership fidelity gap, not a hidden contact pass for the cap. Correcting it would need a separately sourced rear cap/block contract.
3. Whole engine installation, gasket compression/pressure and fluid containment remain open. No CAD, cap, seal, drain, station or source dimension was edited. Original lower full-face failure and all prior candidates remain frozen.

## Delivery and reproduction

Research-only. Actual exact contacts, unsupported surfaces, local witness STEPs and section edge samples are in `cad/engine/generated/timing-pan-upper-contact/`. Reports:

- `inventory/engine/timing-pan-upper-contact-review.json`: complete owner mapping and unsupported-face bounds.
- `inventory/engine/timing-pan-upper-contact-diagnostic.json`: exact local witnesses and terminal transitions.
- `inventory/engine/timing-pan-upper-contact-topology.json`: minimal continuity/fault audit and25 mounting-hole matches.
- `inventory/engine/timing-pan-upper-contact-render-review.json`: actual section/owner render bindings.

Run from repository root:

```sh
.venv-cad/bin/python scripts/check-timing-pan-upper-contact.py
.venv-cad/bin/python scripts/diagnose-timing-pan-upper-contact.py
.venv-cad/bin/python scripts/check-timing-pan-upper-contact-topology.py
python3 scripts/render-timing-pan-upper-contact.py
```

Existing macOS CAD Python3.13/build123d0.10/trimesh/numpy and system matplotlib. No dependencies installed, no credentials or external private files needed beyond repository/restored CAD assets. Model/effort/usage unavailable. Assets not published by worker. Worker inspected actual `upper-contact-review.png` including owner map, retained left rail, rear arch and terminal pocket; root review pending.

| Gate | Result and scope |
|---|---|
| Application/coverage | Research scope; rear cap ownership fidelity unresolved |
| Dimensions/coordinates | PASS original world-mm transforms, manifest placement for retained cap/seal |
| CAD/export | Frozen solids unchanged; exact surface common/cut, sewed contact topology and localized exports |
| Source/visual | Actual source-code architecture and STEP sections inspected; no factory geometry claim |
| Installed interfaces | PASS bounded continuous upper contact; FAIL full-face backing, inherited overhang retained |
| Motion/disassembly | N/A stationary read-only contact study |
| Learning/diagnostics | NOT RUN user-facing lesson; engineering diagnostic only |
| Browser | NOT RUN, no installation |
| Reproduction/review | Hash-bound inputs/reports/render; root review pending |

## Stop point

Bounded study complete. No geometry repair contract proposed because the alleged full-width rail interruption was disproved. Root should review/preserve the exact overhang and rear-owner fidelity findings. No background process or further checker expansion remains. Issues #32/#34 remain open for their other gates; no installed/Done claim.
