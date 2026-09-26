# Component contract and handoff: water-pump-mechanical-seal

## Contract

- Issue: #47 water-pump, engine system; integration owner: root agent.
- Baseline: d410ca6666d764b02b392e07e05befd1c4309e9c; manifest SHA-256 821f7d3bb47d49a00ffb2975fa5faffcd306fe90bea48ce7c0d6308cd636653f.
- Scope: usable six-piece illustrative seal installation candidate. Exact Gates 44009 internal construction, production dimensions, bearing internals and service procedure excluded.
- Own candidate source, dedicated seal scripts/reports and this handoff. Shared builder/manifest exclusively owned by integration owner.
- Units mm. Existing pump-local X axis, parent water-pump-assembly at (440,-32,170), no rotation. Preserve all six stable IDs and existing axial explosion offsets.
- Interfaces: carrier/housing radius 24 at X18..21; collar/shaft radius 8; stationary/rotating contact plane X13.5; bellows and spring contacts connect the stationary face to carrier.
- Available inputs: repository generated STEP assets, current manifest and reference/engine/water-pump-internal-construction-reviewed.json. No personal temporary baseline required after this change.
- Acceptance: six valid single solids; STEP symmetric difference <0.02 mm³; contacts <1e-7 mm; exact annular face area; wet/dry topology with face-gap fault; open wet passage with blocked-passage fault; current-neighbor overlaps <=0.02 mm³. Six sampled display explosions are not a removal sweep.

## Evidence ledger

| Feature | Value / datum | Evidence class | Source | Limit |
|---|---|---|---|---|
| Pump applicability | Gates 44009 | replacement comparison | reference/engine/water-pump-internal-construction-reviewed.json | Does not identify actual internal seal parts |
| Axial mechanical face-seal construction | rotating and spring-loaded stationary faces | generic manufacturer construction | same source ledger, Gates/GMB | Six-piece count is illustrative |
| Seal dimensions/materials | X11..21, face radii 18/11, carrier radius24 mm | inferred | candidate module and inherited pump interfaces | No factory drawing or measured teardown |
| Bearing internals | unknown | unknown | Schaeffler comparison in same ledger | Existing bearing cartridge retained |

## Delivery

Delivered on engine/finish-component-interfaces and provisionally installed by the integration owner. Geometry stays illustrative; combined assembly and browser acceptance belong to root. No factory-completion claim.

## Validation and review

Readiness: **provisionally installed for the explicitly illustrative educational scope**. Local installed checks pass; root combined/browser review remains a separate acceptance gate. Not factory-exact and not Done. No shape edits were necessary: the pre-existing carrier, collar, faces, bellows and spring satisfy current neighbor geometry. The readiness defect was that all checks and harnesses depended on deleted historical temporary directories and lacked bad-geometry sensitivity.

| Gate | Result | Evidence / limits |
|---|---|---|
| Application/coverage | PASS within illustrative scope | Source ledger preserves generic architecture versus Gates applicability; real seal BOM remains unknown |
| Dimensions/coordinates | PASS model interfaces | Existing X11..21 mm envelope, six rigid poses checked; dimensions inferred |
| CAD/export | PASS STEP | Six valid single solids and symmetric difference <0.02 mm³; browser GLB export remains integration-owner gate |
| Source/visual comparison | PASS illustrative structure only | Existing manufacturer construction ledger; regenerated actual CAD axial section/explosion, reference/engine/qc/water-pump-mechanical-seal.png; actual factory contours unknown |
| Installed interfaces | PASS candidate and installed harness | candidate-validation.json: 30 exact static comparisons, contacts, 637.7433 mm² annular face; installed-validation.json: six actual installed shapes/poses; harness-validation.json preserves the separate pre-integration harness |
| Passage/sealing topology | PASS ideal geometry | Wet samples share connected void; dry sample separate. Opening stationary face 0.2 mm makes wet/dry connected; transverse 0.2 mm obstruction splits wet path. No coolant film, pressure or hydraulic simulation |
| Motion/disassembly | PASS sampled display; physical removal NOT RUN | 52 exact pairs at explosion fractions .05/.1/.25/.5/.75/1; no claim of continuous full-engine removal or elastomer mechanics |
| Learning/diagnostics | PASS limited teaching scope | Existing inventory/engine/water-pump-mechanical-seal-learning.json preserves material/architecture uncertainty |
| Browser integration | NOT RUN by contributor | Root must export, select/isolate, explode/reset and inspect six parts |
| Reproduction/review | PASS local reproduction; root review pending | All input hashes repository-relative in report. Current generated STEP restored by integration owner from matching checkpoint |

Commands from repository root:

```sh
.venv-cad/bin/python scripts/check-water-pump-mechanical-seal-candidate.py
.venv-cad/bin/python scripts/prepare-water-pump-mechanical-seal-harness.py
.venv-cad/bin/python scripts/check-water-pump-mechanical-seal-candidate.py --manifest cad/engine/candidates/mechanical-seal/harness/full-assembly.json --report inventory/engine/water-pump-mechanical-seal-harness-candidate-validation.json
.venv-cad/bin/python scripts/check-water-pump-mechanical-seal-installed.py --manifest cad/engine/candidates/mechanical-seal/harness/full-assembly.json --candidate-report inventory/engine/water-pump-mechanical-seal-harness-candidate-validation.json --report inventory/engine/water-pump-mechanical-seal-harness-validation.json
MPLCONFIGDIR=/tmp/truck-matplotlib python3 scripts/render-water-pump-mechanical-seal-candidate.py
```

`check-water-pump-mechanical-seal-inlet-readiness.py` delegates to the same candidate checker with its dedicated report name; its saved report is an alias of the current candidate result, not a second independent audit. Optional `--manifest`, `--output-dir`, `--report` keep all scripts reusable. Harness output defaults to a repository-relative candidate directory and can be regenerated; STEP files follow existing artifact policy. Full manifest snapshots in the harness are generated, not new authoritative assembly manifests.

Environment: macOS, Python 3.13.12; build123d 0.10.0, cadquery-ocp 7.8.1.1.post1, NumPy 2.5.3, trimesh 4.7.4. Rendering uses system python3 with Matplotlib 3.10.9 because CAD environment does not include Matplotlib. No new package installation or pin change. Worker model/effort and detailed usage unavailable.

## Exact integration patch guidance

1. Collect existing pump output, remove definition and occurrence `water-pump-seal` only. Preserve housing, shaft, impeller, bearing, inlet, fasteners and their existing transforms.
2. After `water-pump-assembly` exists invoke `water_pump_mechanical_seal_candidate.build((define, add, group))`. API takes the existing exporter callbacks, creates child `water-pump-mechanical-seal-assembly` with zero local transform and six named occurrences; net +5 definitions and occurrences.
3. Register source ID `water-pump-internal-construction` with path `reference/engine/water-pump-internal-construction-reviewed.json`; merge existing seal learning JSON. Preserve all illustrative labels and GAPS.
4. Export using the common exporter, rerun the candidate checker against the exported installed manifest, then run the installed checker against the real manifest (omit `--manifest`) and existing candidate report. It verifies candidate input hashes before accepting geometry. If neighbors change, rerun candidate checker first. Root must perform GLB/browser review and affected combined-assembly gates.

## Tracking and restart

#47 remains open pending integrated/browser acceptance and remaining water-pump coverage. Root owns shared builder/manifest and issue tracking. Local current-manifest candidate, harness and installed checks PASS; no contributor processes running after delivery. Revalidate after later component/transform edits with the candidate checker, then `.venv-cad/bin/python scripts/check-water-pump-mechanical-seal-installed.py --candidate-report inventory/engine/water-pump-mechanical-seal-candidate-validation.json`. Candidate code may be preserved regardless of unresolved factory fidelity; exact pump construction remains explicitly unknown.

The rotating face and shaft collar are axially symmetric rings; rotation about pump-local X leaves their occupied volume invariant. This supports continuous rotational clearance of those two rigid shapes, but does not establish friction, drive torque, compression or wear performance. Spring, carrier, stationary face and bellows stay stationary. Issue number was resolved from the checked-in work breakdown; live issue body fetch was unavailable due network connection failure, so no external changes were made.

Final local rerun used the restored current CAD baseline recorded in `inventory/engine/cad-baseline-restoration.json`. Candidate and installed harness both passed again after restoration; earlier local STEP hashes are superseded. The committed manifest stayed at the contract hash during this audit. Canonical reports contain the final restored-neighbor hashes, all six contact/roundtrip results, both deliberate-fault outcomes and no collision failures.

Installed checker now requires an exact candidate/installed manifest hash match, in addition to per-input hashes. Any transform or inventory change requires a fresh candidate audit; the candidate checker handles both old-envelope and installed six-part manifests.

## Actual installed audit — 2026-09-26

Integration owner installed six seal pieces into the authoritative assembly (705 definitions / 1,310 occurrences; manifest SHA-256 `18d31887ddae03bb78c1abfe565f4cd5c3a469c81328c77c4b4f1e04860de37c`). The candidate audit was rerun against this exact installed manifest, covering current neighbor shapes and transforms; strict installed check then compared all six actual exported STEP definitions, poses and display offsets. Reports are `inventory/engine/water-pump-mechanical-seal-candidate-validation.json` and `inventory/engine/water-pump-mechanical-seal-installed-validation.json`. Previous baseline/harness results are historical bounded checks; current report hashes govern current claims.

Installed geometry remains a generic educational six-piece study. No actual Gates44009 seal supplier, dimensions, material pairing, spring preload, elastomer squeeze, bearing internals or truck identity has been verified. #47 and broader pump fidelity remain open. Browser and combined-assembly acceptance are recorded separately by the integration owner; successful local installation checks do not mark the component Done.

## Integration-owner checkpoint

Provisionally installed on manifest `f725260d8f1497a1b6f2aed9d41d01155bf2a82e7391d24ce866f352bb50cd5b`. Current installed checks and whole-static audit pass (4,944 exact pairs, zero overlaps above 0.1 mm³). Browser selection, individual explanations, assembled view, explosion/reset and applicable throttle motion were inspected; see `inventory/engine/component-interface-browser-review.json`. CAD source renders were compared with the cited reference topology. Production dimensions, identities and the other explicit gaps above remain unresolved; issue stays open. This accepts the educational addition for integration, not the complete component ticket or a factory-exact replica.
