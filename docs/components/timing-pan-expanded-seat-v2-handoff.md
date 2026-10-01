# Component contract and handoff: timing pan expanded seat v2

## Contract

- Issues #32/#34, Engine #1. Pan worker owns the v2 contract, source, checker, renderers, reports and generated folder; root owns integration and block worker owns the matching casting adapter.
- Baseline `70542fad9de467a5c03ad54a6f54def8550956eb`; assembly manifest hash is bound in the validation report.
- Uninstalled candidate, estimated shared X300..365 interface. Exact prebuild API and protected regions: `timing-pan-expanded-seat-v2-contract.md`, inheriting the first expanded contract. Stable pan and pan-gasket identities; no new service number or verified factory contour.
- World CAD millimeters, unchanged assembly origin/axes and transforms. Rear X≤300, 20 retained mounts, five revised axes and front arch X365+ protected.
- Inputs: frozen attachment v2, original pan fasteners, prior failed pan witness, nominal TEKTON tool ledger. Existing local CAD environment; no new dependencies or shared builder/inventory changes.
- Checks: exact Boolean material/contact checks, independent hardware/tool transforms, actual face support, fixed witness paths and independently placed breach/block controls. No neighboring solid used to carve the pan.

## Evidence ledger

| Feature | Value/datum | Class and source | Limit |
|---|---|---|---|
| Shared seat | X300..365, Z−32..−24.5 | Explicit estimate, shared API | Not measured factory geometry |
| Wall | Entry3→4mm, downstream normal4mm | Explicit estimate | No casting/strength acceptance |
| Socket flats | Radius10 at stations10/20 | Functional estimate preserving existing owner region | Threads owned by block worker |
| Nominal socket | OD17.526, length48.26mm | Manufacturer comparison, `reference/engine/tekton-shd03013-access-review.json` | No ratchet/tolerance or vehicle access claim |
| Mounts | All25 original/revised transforms | Existing source contracts and bound inputs | Factory flange contours remain estimated |

## Delivery

- Delivery branch `engine/timing-pan-seal-joints` (created on `engine/timing-interface-integration`); no separate PR or installation by worker.
- API `timing_pan_expanded_seat_v2_contract.py`: `band`, `pan_flange`, `gasket_band`, `below_mating_seat`, `upper_wall_envelope`, `transition_below_seat`, `transition_seat_support`. Block explicitly calls support height10; default8 is unused.
- Candidate entry `timing_pan_expanded_seat_v2_candidate.build()`; exports in `cad/engine/generated/timing-pan-expanded-seat-v2-candidate/`.
- STEP pan SHA256 `d7f495ec95b0cc465880c72ae38f6e873f5ee30cdbebecf4a1613a7cbe6e5b3f`; gasket `8e968afca78cf09e81e678307b24d59a78cbe251210983a4eb5f6981619d6936`.
- API SHA256 `4fa9d104606158710bb221fcfc71ca5dcddb62bf00243338920e92adb8f9839e`; remaining input/output hashes in validation and render reports.
- Reproduce: `.venv-cad/bin/python scripts/check-timing-pan-expanded-seat-v2-candidate.py`; then `python3 scripts/render-timing-pan-expanded-seat-v2-candidate.py` and `python3 scripts/render-timing-pan-expanded-seat-v2-shaded.py`.
- macOS, CAD Python3.13/build123d0.10; system Python matplotlib for rendering. Temporary font cache fallback is automatic, no persistent external evidence dependency. Model/effort/usage unavailable. Assets unreleased.

## Validation and review

| Gate | Result | Evidence and remaining scope |
|---|---|---|
| Application/coverage | Partial | Component estimate; no factory contour claim |
| Dimensions/coordinates | PASS bounded | Rear/front exact preservation; all25 mounting/seat checks;3.5mm midpoint and4mm downstream wall probes |
| CAD/export | PASS | Single valid solids, STEP roundtrip, watertight meshes, CAD/GLB bounds checks |
| Source/visual comparison | Candidate reviewed by worker | Actual `review.png` sections and `shaded-glb-review.png`; root reviewed v2 section render |
| Installed interfaces | FAIL / OPEN | Frozen future-land overlaps143.799914mm³. Coordinated block revision must remove old seat by shared contract, not pan subtraction. New transition gasket underside and all2089.9674mm² walltop fully backed |
| Full gasket contact | OPEN inherited |25.535585mm² rear selected downward surfaces unbacked in both original and candidate; exact diagnostic in first expanded folder. No threshold waiver or full contact claim |
| Motion/disassembly | PASS bounded | Five hardware/washer solids clear; nominal90mm socket approach clear, minimum1.335676mm; priorR11 failures preserved |
| Interface/flow diagnostics | PASS bounded | Dry/wet path witnesses, actual section loops, breach and blockage controls; whole oil containment NOT VERIFIED |
| Learning/diagnostics | NOT RUN | No user-facing lesson or diagnostic learning content updated |
| Browser integration | NOT RUN | Uninstalled candidate, no browser authorized after earlier rejection |
| Reproduction/review | PASS local / root section review complete | Bound source/checker/API/export/render hashes; no frozen failed files overwritten |

No complete installed or whole-fluid-containment verdict. Local topological method proposal remains in first expanded contract, with no global roof retry or geometry changes for a probe. Render shading exposes actual triangle contours; it does not smooth geometry or certify strength. Checker's overall FAIL is intentionally retained for the obsolete frozen land pair; matching block-pair evidence is a separate report.

## Tracking and restart

Issues remain open. Next: block worker checks matching v2 pan/gasket against its union-land-before-seat-cut block with protected female cavities. Preserve both failed pairs and inherited rear contact diagnostic. No running pan process. Usage figures unavailable.
