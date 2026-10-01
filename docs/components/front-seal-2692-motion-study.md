# Component handoff: 2692 seal rotation and axial sensitivity

## Contract before checking

Issue #32, root integration owner; separate follow-up to the frozen seal delivery. Current branch `engine/timing-pan-seal-joints`, baseline `a66b33c`. Own only this handoff, new `front-seal-2692-motion-*` source/report files and `scripts/check-front-seal-2692-motion-study.py`. No geometry/export/canonical changes; the frozen seal delivery binding remains authoritative. All dimensions millimeters, +X forward, crank axis Y=Z=0.

Scope: continuous nominal rotation of the actual candidate hub relative to stationary cover/case/elastomer/garter, and bounded axial sensitivity using applicable source endplay. No whole-engine/endplay acceptance and no change to timing gears. Validate the full annular hub region from actual STEP in both Boolean directions, independently probe material, prove all other hub geometry lies forward of the stationary seal envelope for every tested axial offset, then use interval bounds for continuous angle/translation coverage. Exact endpoint poses are controls, not the continuous proof. Preserve frozen source assumptions and report a material or source conflict instead of moving parts.

## Evidence and assumptions

The captured exact-year 1994 F-150 4.9 rebuilding specifications list thrust bearing clearance0.0040–0.0080in, exactly0.1016–0.2032mm. The adjacent-year Ford1996 4.9 OEM specification explicitly calls the same range crankshaft free end play. This is a specification, not a measurement of this truck. Ford's CSG649 procedure describes the dial-indicator travel between rearward and forward crank stops; its industrial applicability is a comparison only.

The absolute nominal hub registration is estimated and is not identified with either thrust stop or the midpoint. Check offsets−0.2032..+0.2032mm around that assumed nominal. This conservative sensitivity covers either possible endpoint registration of a0.2032mm total travel; it does NOT redefine factory total endplay as0.4064mm. Also report the centered±0.1016mm interpretation without adopting it as actual position.

The conceptual moving crank assembly is crankshaft, hub/damper, rigid crank bolt/washer/key, flywheel and crank-mounted timing gear; stationary cover and all three seal constituents stay fixed. Only the actual hub is moved mathematically in this isolated checker. Other crank-group members are neither moved in exported CAD nor accepted by this check. Relative crank/cam axial motion changes the helical gear engagement/phase relationship and requires a coupled gear/thrust study. Rod alignment, clutch/input shaft, rear seal, belt alignment and thrust clearances also remain outside scope.

Viewer code `atlas.js` uses increasing positive angle and +X crank rotation, with CAD→view basis(X,Z,−Y). For an observer on the front/+X side looking rearward/−X, with CAD+Z screen-up and CAD+Y screen-right, a top marker moves toward screen-left: counterclockwise. This is a source-code/matrix finding, not a browser interaction test. Timken2692 says clockwise-spiral lip design, but the reviewed2692 table/catalog does not establish viewing direction or equate groove handedness directly with shaft direction. Exact-year captured pages searched did not establish a direct crank rotation convention. Handedness compatibility remains UNKNOWN; do not silently change viewer angle, cam phasing or modeled lip texture.

## Planned commands and gates

Run `.venv-cad/bin/python scripts/check-front-seal-2692-motion-study.py` after restoring frozen seal artifacts. Gate exact hub annulus equality and positive material, local radial protection, continuous far-hub axial separation, complete lip-track support throughout the offset interval, selected endpoint/angle controls, and intentionally removed-material/off-track negative controls. Bind actual STEP/source/helper/viewer/manual hashes. No new mesh is needed because geometry is unchanged. Browser, physical force/preload/temperature/wear and whole-engine endplay are NOT RUN. Root owns final review, issue updates and any future integration. Usage/model effort unavailable.

## Delivery and validation

New report: `inventory/engine/front-seal-2692-motion-validation.json`; source ledger: `reference/engine/front-seal-2692-motion-source-review.json`. Readiness is a bounded research/checking result on an uninstalled candidate. Frozen seal geometry and delivery files are unchanged. CAD package environment and dependencies are inherited unchanged from the seal handoff; no new artifacts need export.

The actual exported hub regionX419–435.5 equals the complete annulusR21.05–23.8125 in both Boolean directions, with zero missing/excess material. Thirty strict interior witnesses independently confirm actual track material. The entire case/rubber/spring remains within the common track intervalX419.2032–435.2968 throughout the conservative offset range; therefore the stationary seal's nominal radial contact/clearance relation is invariant for all rotation angles and every offset in that interval. All remaining hub material is forward of the stationary seal envelope by at least1.8856mm; its non-axisymmetric features cannot enter this neighborhood under rotation.

The cover retains0.1875mm radial clearance to the track throughout the expanded axial domain. The full lip contact band retains8.6968mm rear and7.0968mm forward track margin at the conservative extreme. Even the complete source seal-width interval retains0.7968mm rear/1.8856mm forward margin. Full annular material probes covering the union of all axial lip positions pass. Twelve exact endpoint/angle pair controls also pass; these samples supplement the continuous annulus/interval proof and are not mislabeled as the proof itself.

A deliberately removed track patch is detected, and a10mm rearward shift fails the forward track margin. The initial0.4mm-wide diagnostic notch removed less than the predeclared0.01mm³ detection gate; it was expanded to0.8mm instead of weakening that gate. This was a negative-control size issue, not an accepted physical model failure or a geometry revision.

| Gate | Result |
|---|---|
| Application/source | Exact-year thrust-clearance range found; adjacent-year OEM endplay label corroborates. Actual truck endplay and nominal thrust position unknown. |
| Continuous rotation | PASS for the declared hub versus stationary seal/cover neighborhood, using actual exported axial/radial geometry. |
| Axial support | PASS conservative±0.2032mm sensitivity about estimated nominal; no claim of0.4064mm factory total endplay. |
| Fixed seal supports | Reused frozen case/flange/bond/spring support checks; these components do not translate in this study. |
| Direction/handedness | Viewer front-view counterclockwise established by code/matrix; exact-year operating crank direction and2692 viewing convention remain UNKNOWN. |
| Whole-engine motion | NOT RUN. Crank-mounted helical gear, cam thrust, rods, clutch, rear seal and belt coupling remain required follow-up. |
| CAD/browser | Frozen CAD unchanged; no new export needed. Browser NOT RUN. |
| Reproduction | Checker binds actual inputs and source/viewer hashes. Root review and issue/PR tracking remain integration-owner work. |

No process is intended to continue after delivery. Root may merge this scoped evidence without claiming installed endplay or rotation-handedness acceptance. Exact next integration action: resolve crank operating direction/2692 viewing convention from an applicable primary source, then coordinate the real crank/cam thrust range and helical engagement before any whole-engine axial animation.
