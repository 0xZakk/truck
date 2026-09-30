# Component contract and handoff: EVR vent detail

## Contract

- Issue58 / engine parent1, cross-system7. Contributor pump_seal_finish; root integration owner.
- Baseline `74ca5288bb543871b1cc550e191e3f54ed62a8f1`. Manifest and local source hashes: `reference/engine/evr-detail-review.json`.
- Research/proposal first; owned this document and `reference/engine/evr-detail-review.json`. No shared geometry, manifest, frozen IAC studies or canonical artifacts changed.
- First supported missing element: **atmospheric vent filter**. Actual truck regulator identity, filter material, dimensions, retention and hidden valve construction remain unresolved. Saved Standard VS52 manufacturer fit/specification capture is replacement evidence; its five named product photographs have not been inspected.
- Existing EVR-local axes: cylindrical body alongZ, ports point+X; assembly has explicit installed transforms. Any candidate must preserve current relevant occurrence/ancestor frames rather than assume the original hard-coded world location. CAD millimeters.

## Evidence ledger

| Claim | Evidence | Scope |
|---|---|---|
| Filter exists and vents to atmosphere | Exact1994 DN testing notes | Applicable functional topology |
| Filter can be obstructed and replaced | Exact1994 DN42 | Separately identifiable service element; does not specify material/shape |
| Electromagnetic regulator | Exact1994 description and DN10 |20–70ohm diagnostic window is not a winding-design target |
| Upper nipple to EGR, lower to vacuum source | Actual inspected image615919167 | Exterior topology, no dimensions |
| Coil controls disc | Ford1999 PCED section1, reviewed online text | Later-system mechanism comparison; no calibration transferred |
| Hollow core, disc below it, weak spring, vented cover | Archived Ford1992 F3505.8 description, reviewed text | Adjacent application only; not proof of exact1994 internals |

The exact1994 image is an external illustration, not a section. The1994PCED10A-7 scan has now been inspected: it describes coil/armature/disc/orifice operation and shows typical exteriors, not an internal section. No dimensions or2.3Ranger-specific feature is transferred. Local source hashes and external URLs are in the ledger. Restricted manual content is not redistributed.

## Proposed bounded candidate

Create a separate filter envelope only as part of a mechanically coherent, explicitly illustrative vent study. The existing body is solid; nipple bores terminate at localX8 and do not share an internal chamber. Existing cap cavityR13 spans localZ41–57 with a solid roofZ57–59 and no atmospheric opening. A disk dropped inside this shell would neither vent nor explain the regulator.

The candidate therefore needs isolated replacement body/cap geometry, a supported filter seat and a continuous atmospheric passage. Proposed decomposition is filter, vented cover and body passage; defer winding/core/disc/spring solids until the stronger section evidence is inspected. All seat, inlet and passage dimensions must be labeled model-derived educational choices. Represent filter permeability explicitly as an envelope or open illustrative lattice; never claim a solid disk passes air, nor claim its hole pattern reproduces factory media.

Required checks: exterior-to-filter-to-body continuous flow witnesses; blocked-inlet and filter-bypass controls; positive seat contact and removal access; no unintended body/cap overlap; surviving wall thickness; unchanged mounting ears, connector and nipple exterior; relevant neighboring STEP collision tests; STEP/GLB binding and actual section render. A complete valve-flow simulation, measured pressure calibration and winding physics are outside this first element.

## Delivery and validation

Readiness: **research proposal**, not geometry or installed acceptance. No CAD builder, STEP, GLB or render created. Evidence review passed within stated source scope; dimensions, CAD/export, motion, installed interfaces and browser checks are NOT RUN. Learning scope is topology and uncertainty only. No commit, PR, external post or canonical write.

Review reproduction: verify SHA256 for the local paths in `reference/engine/evr-detail-review.json`; read the listed exact-year pages and inspect image615919167. Source access requires authorized local manuals. Environment: macOS, Python3.13; CAD was not executed for this research-only proposal. Usage/billing unavailable.

## Tracking and restart

Issue58 remains open. Next action: integration-owner review of this one-element proposal, plus inspect the pending page10A-7 section and replacement photographs if accessible. Then build the isolated filter/vent candidate with explicit dimensional estimates. No process remains running. Do not substitute an inferred armature or spring construction for unresolved actual-part evidence.

## Isolated vent candidate delivery

Entry point `cad/engine/evr_detail_candidate.py:build()` returns replacement body/cap and separate illustrative filter. Checker `scripts/check-evr-detail-candidate.py`; report `inventory/engine/evr-detail-candidate-validation.json`. Isolated ignored artifacts: `cad/engine/generated/evr-detail-candidate/` with individual STEP/GLB, combinedGLB and `candidate-review.png`.

Estimated topology: two lateral cap inlets at localZ54 → chamber above filter → illustrative perforations atZ48–50 → body well → central vent bore → upper/EGR nipple. The lower/source nipple remains blind and unfinished. **This is a vent/filter subassembly study, not a functioning or integration-ready EVR.** Coil, disc, orifice calibration and magnetic assembly remain deferred. All radii, pore count, perforations, seats and capture construction are educational choices; no factory filter-media resemblance is claimed.

The body shoulder and cap retaining ring contact both filter faces. Existing ears/bolt openings, electrical connector and nipple ends are protected by exact Boolean comparison. Flow witnesses pass through actual voids and an actual filter pore. Oversized-filter collision, lifted-filter lost seating and blocked-flow witness are deliberate fault controls. Installed neighboring geometry/browser checks remain NOT RUN; no shared component is promoted.

Reproduce from repository root:

```sh
.venv-cad/bin/python scripts/check-evr-detail-candidate.py
python scripts/check-evr-detail-candidate.py --render
```

macOS/Python3.13/build123d0.10/OCP7.8; systemPython supplies matplotlib for render. Fine mesh tessellation preserves CAD; duplicate and degenerate mesh faces are removed and watertightness checked after vertex merge. No cap fastener/press-fit force or filtering efficiency certification.

Observed export issue and fix: inherited lower nipple began exactly atX12, tangent to lower bodyR12, producing one four-face mesh edge. Candidate overlaps that root inward by0.5mm and recuts the original bore. Exact protected nipple ends/barbs remain unchanged. This estimated root repair is localized and explicitly not a measured factory shape. All three final meshes are watertight; valid single-solid STEP round trips agree within5e-10mm³. Filter contacts216.769893mm² per face, interpart overlaps0, flow witness obstruction0. Blocked-path control detects0.062832mm³, oversized filter83.252205mm³ collision, lifted filter0.5mm lost contact. Cap attachment strength/sealing to outer body remains unresolved; filter capture assumes cap stays installed. No installed acceptance.
