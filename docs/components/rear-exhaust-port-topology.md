# Component contract and handoff: rear exhaust port topology

## Contract

- Issue: #46, engine exhaust; research continuation of the accepted bounded collector study. Integration owner: root coordinator; researcher: `evr_install_resume`.
- Baseline: `a93b5bc1732f41651403ff15d821b52ab3d57d82`, branch `engine/exhaust-timing-joints`. Model snapshot manifest SHA-256 `ab99fff2f63ad5dfc21fde8d12a32fc2a3d65832e6c8664baefd99d94403f7bf`; 741 definitions, 1,349 occurrences. This research changes neither count.
- Own only this document, `reference/engine/rear-exhaust-port-topology.json`, and ignored `cad/engine/generated/rear-exhaust-port-topology/`. No shared, canonical, frozen candidate or integration-proof edits.
- Scope: discriminate EGR, AIR and other rear casting features; examine outlet form. No speculative CAD, port relocation, thread specification or installed identity claim.
- Preserve existing millimeter axes, frames and stable IDs. A later coordinated correction may affect `exhaust-rear`, `egr-tube-manifold-fitting`, `egr-exhaust-tube`, `egr-tube-heat-sleeve`, and only if necessary `egr-tube-valve-nut`. Head entries/bolts and pipe-flange datums remain protected until contrary applicable evidence exists.
- Inputs: retained manufacturer images, selected 1994 service archive, 1994 EVTM and current mesh, all locally available. File hashes and exact archive paths are in the companion JSON. No owner measurements required for this research.
- Acceptance: identify observed features without confusing photograph orientation with vehicle coordinates; resolve identities only through applicable labeled evidence; disclose conflicts. Geometry acceptance is N/A.

## Evidence ledger

| Claim / feature | Evidence | Applicability / uncertainty |
|---|---|---|
| Rear service part | Selected 1994 exhaust parts table lists F5TZ9431F; Dorman 674-186 cross-reference includes that number | Service/replacement linkage, not proof of the owner's installed casting |
| EGR endpoint | Exact selected 1994 exhaust and intake removal procedures separately remove the EGR-valve-to-rear-manifold tube | Establishes rear manifold endpoint, not boss position, thread or seat |
| Thermactor hardware | Same procedure removes two Thermactor tube retaining nuts and a bypass-valve bracket nut at lower intake | Distinct plumbing/support exists; attachment fasteners do not establish gas-entry location |
| AIR routing | Retained AIR description gives upstream and downstream/catalyst paths | Illustration 606914019 is explicitly typical and shows two four-port banks. It cannot locate the 4.9L receiver in the head, manifold or catalyst plumbing |
| HO2S manifold location | 1994 EVTM PDF page 341, printed 152-6, explicitly lists 4.9L HO2S in exhaust manifold, connector C1025, figure 151-1-B1 | Strong engine-specific location statement, but no boss identity |
| HO2S location illustration | EVTM PDF page 312, printed 151-1, captioned 4.9L engine | Leader enters an obscured lower engine region; does not discriminate the two replacement bosses |
| Conflicting HO2S pipe location | Selected 1994 sensor service says exhaust pipe. Ford TSB 95-2-10, dated January 30, 1995, covering 1991–94 F-Series 4.9L, uses catalyst inlet pipe | Pipe evidence is not solely generic V8 wording. TSB calibration applicability to this vehicle is unconfirmed. Conflict remains unresolved |
| Neck/flange | Actual 674-186 back and three-quarter photographs show a broad blended discharge with integral two-hole flange | Supports qualitative casting form; no calibrated length, angle or sealing-seat section |
| Tube hardware | Actual 598-105 image shows bent sleeved tube and exposed end connectors; manufacturer lists two threaded connectors, 0.74-inch OD (18.796 mm), OE F4TZ9D477C | Replacement comparison. Listed 17.9-inch length has unspecified measurement basis. No connector endpoint assignment, pitch, seat angle or bending coordinates |

Primary manufacturer pages: [674-186 manifold](https://www.dormanproducts.com/p-26852-674-186.aspx), [598-105 tube](https://www.dormanproducts.com/p-32641-598-105.aspx). Existing captured fitment reviews remain historical inputs; this study did not repeat live vehicle selectors.

### What the pixels establish

Use **photo-relative**, nonfunctional labels in `reference/engine/dorman-674186-back.jpg`: A is the image-left lateral hex-plugged boss; B is the image-upper-right oblique hex-plugged boss; C is the smaller circular recess above the flange. A and B are visibly separate plugged features. C is not proven to be a gas passage rather than a blind or mounting recess. None receives an EGR, AIR or HO2S ID from this study.

Two supplied plugs do not establish two plugs installed on the running truck. EGR plus an HO2S/alternate-application provision is a hypothesis, not a conclusion. An AIR assignment is equally unsupported. The 598-105 photo does not label which photographed connector mates to the manifold; visible thread/recess appearance alone does not resolve its sealing seat.

The current actual mesh was rendered in two views and inspected against the retained source pixels. It retains an end EGR patch and a long straight cylindrical outlet neck, whereas the replacement has bosses around the central discharge and a broader neck blend. This confirms a visible discrepancy, not a measured correction vector. Photograph perspective is insufficient to shorten the neck or change the outlet axis confidently.

The 1988 EFI exploded intake comparison does not show an applicable rear casting map. Mixed-year catalog results, generic V8 AIR drawings and unverified forum descriptions of head injection rails are excluded from endpoint assignments. No thread sizes from mixed-application catalogs were transferred.

## Next correction contract

**Port relocation remains evidence-gated.** Obtain an applicable oriented Ford service/parts figure or manufacturer technical port map connecting tube 9D477 to A/B, identifying the other provision or unused plug, and tying the drawing to F5TZ9431F or an established 1994 4.9L emissions variant. Independently trace the 4.9L Thermactor outlet to its physical receiver. The EVTM/TSB HO2S conflict must be reconciled by variant or a matched figure before assigning an oxygen-sensor port. No outgoing manufacturer inquiry was sent.

After that gate, prepare one isolated joint candidate spanning the casting and existing EGR line IDs above. Preserve head/bolt and outlet mating datums; prove the full original/replacement interface comparison, connection alignment, continuous unobstructed gas path, wall thickness, current-neighbor clearance, valid CAD and watertight mesh. Show actual source comparisons from multiple views. Any fitting/thread/seat approximation must remain explicitly provisional until dimensional evidence supports it.

A neck-exterior-only study could explore the broader blend while retaining the current bore and flange datums. It would still be an estimated exterior study; these sources do **not** authorize a factory neck length, axis change, new seat or downstream pipe relocation. It should not substitute for resolving the more consequential port topology.

The neck/flange are integral features of `exhaust-rear`, not additional parts. Keep the separate fitting/tube/sleeve IDs. Do not create AIR, HO2S or plug occurrences from replacement packout alone. Current proposed part-count delta: zero; no canonical promotion proposed.

## Delivery

- Readiness: research complete with unresolved variant/port evidence; not geometry-ready or installed acceptance.
- Deliverables: this document and companion hash ledger. Local evidence views: `cad/engine/generated/rear-exhaust-port-topology/evtm-p341.png`, `evtm-p312.png`, `current-model.png`, `model-binding.json`.
- Current rendered GLB SHA-256: `6cdd2b125029740e6a9d3b4edd3969941bedb5c3c155948c398547ee0d716a79`; STEP: `680cf58c458970dfacd5d15f8da3533fe12fc47058de2d68f3709b35aa47bc48`. These bind the visual snapshot only, not a new integration proof.
- Rendering: local Python/matplotlib, with the existing CAD virtualenv's trimesh dependency. Existing mesh inspected in CAD millimeters after reversing viewer axes. No STEP regenerated.
- Source originals, purchased manual pages and source composites remain ignored; no release is produced. Required authoritative source paths/hashes are preserved in JSON for licensed local reproduction; render is supplemental and not required to interpret the written findings.

## Validation and review

| Gate | Result | Scope / limits |
|---|---|---|
| Application/coverage | PARTIAL | Exact service-number link; owner casting and emissions variant unknown |
| Dimensions/coordinates | NOT RUN | No dimensioned port map; no coordinates changed |
| CAD/export | N/A | Research only; canonical files unchanged |
| Source/visual comparison | PASS, bounded | Actual manufacturer pixels and hash-bound model viewed; no metric fit claimed |
| Installed interfaces | NOT RUN | New interface positions not proposed |
| Motion/disassembly | N/A | No mechanism changed |
| Learning/diagnostics | N/A | No learning edits; no repair specification proposed |
| Browser integration | N/A | No viewer/asset edits |
| Reproduction/review | PASS, bounded | Source hash ledger and page identities recorded; ignored captures are not distributable deliverables |

Reviewer: researcher; coordinator review pending. No earlier proof is invalidated by these new research files. #46 remains open for production port topology, neck/seal dimensions and remaining casting fidelity. Next action: obtain the matched oriented port/receiver evidence specified above, then revise this research contract before CAD. No process remains running. Model usage/effort and billing unavailable.
