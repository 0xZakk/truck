# Component contract and handoff: timing-pan-access-proposal

## Contract

Issue #32 / Engine #1; root is integration owner. Baseline `8547c589d3c086bad91baf879219612bcd9a162f`, branch `engine/timing-support-joints`. Own this handoff, `scripts/render-timing-pan-access-proposal.py`, `reference/engine/timing-pan-access-proposal.json` and isolated generated `timing-pan-access-proposal/` output. This is a section proposal only: no CAD solid edits, canonical installation or revision to frozen studies.

Compare an estimated broad front-wall setback against three local inward stamped recesses at the fixed front stations X390, Y−110/0/180. Diagnose station 10 separately. Preserve all 25 station identities, 20 unchanged transforms, full washer seating area, gasket lands, at least the existing estimated 4 mm pan-wall envelope, continuous oil-volume boundary and all rear material X≤335. Tool dimensions are illustrative estimates, not a tool catalog specification.

Use the actual frozen v2 mesh as context. Explicitly label wet oil region and exterior dry access. Do not use a subtraction of the fasteners to define the pan wall. Compare cross-sections and continuity of the proposed inner/outer wall paths. Root reviews before authorizing geometry. Any proposal that cannot join the unchanged lower body without interrupting oil containment or tool access remains unresolved.

## Evidence ledger

The exact-year pan figure supports stamped-pan topology and 25 screw-and-washer stations, not these local dimensions or stamping contours. All access offsets are model-design estimates. The frozen v2 report establishes actual head/washer interference; source fidelity remains bounded. Broad versus local stamping is a plausibility comparison, not a verified production feature.

## Delivery

In progress: section proposals only. APIs, geometry/export gates and installed acceptance are N/A for unbuilt proposals; contact, wall, oil-boundary and tool-access proof remain NOT RUN until a selected candidate is built.

## Section proposal and review

Run `python3 scripts/render-timing-pan-access-proposal.py`. Output is `cad/engine/generated/timing-pan-access-proposal/section-proposal.png`; numeric assumptions and input hashes are in `reference/engine/timing-pan-access-proposal.json`. Actual mesh sections come from the frozen v2 output. Renderer needs NumPy/Matplotlib only; no CAD regeneration occurred.

The preferred hypothesis is a broad inward front wall setback: estimated outer X378 / inner X374, rather than three local dimples from X399. The full upper flange and washer pads remain above the dry pocket. At the center station the actual unchanged lower body is outer X363 / inner X360 below Z−80. A 4 mm horizontal shoulder from Z−80 to −76 can join that body to the proposed vertical 4 mm front wall. The inherited lower-body wall remains 3 mm; this proposal does not silently claim it is 4 mm. Corner blend radii and actual 3D wall thickness remain unproved.

An illustrative 22 mm OD socket about X390 occupies X379..401 and has 1 mm section clearance from the proposed outer wall. Its axial access corridor extends upward to the washer underside and downward beyond the lower shoulder. Tool specification and ratchet access are unknown; this is a clearly estimated feasibility envelope.

The broad setback has fewer local blends than three dimples and defines a simpler continuous wet/dry boundary. Local dimples might preserve more oil volume but require six lateral return transitions and independent thickness/clearance proof. Neither alternative is factory-verified. Actual pan capacity is unknown and no capacity claim is made.

Station 10 has a different conflict: the steep side transition crosses its head/washer in the actual Y196 section. It needs a separately constructed flat dry-side seating pad and transition, with oil containment and tool access proven. A broad front setback alone does not resolve that station.

## Validation and restart

| Gate | Status | Scope |
|---|---|---|
| Source/application | PASS for bounded proposal | Nominal fastener evidence inherited; stamping dimensions explicitly estimated |
| Actual section extraction / visual review | PASS locally | Frozen mesh sections inspected, proposed lines labeled unbuilt |
| Dimensions / transforms | PASS for declared assumptions | Fixed station coordinates; no actual transforms changed |
| CAD/export integrity | N/A | No new solid or mesh supplied |
| Wall / oil boundary / tool sweep | NOT RUN | Section concept only; no 3D proof |
| Installed interfaces / motion | NOT RUN | No installation or disassembly acceptance |
| Learning / browser | NOT RUN | No user-facing lesson or installed model |
| Reproduction / root review | Commands and hashes provided; root pending | No temporary input dependency |

Next action is root review of the section proposal before solid construction. No process remains running. Preserve v2 and all earlier failed studies. Usage and billing measurements unavailable; system Python/NumPy/Matplotlib produced the proposal image, with no dependency changes.
