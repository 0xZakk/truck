# Component handoff: coordinated engine rotation convention

## Contract and decision

Issue #32; root integration owner. Baseline `a66b33c`, branch `engine/timing-pan-seal-joints`. Own this new handoff, `reference/engine/engine-rotation-convention-review.json`, `scripts/diagnose-engine-rotation-convention.mjs` and its new diagnostic report. Research/numeric proposal only: no viewer, manifest, frozen seal or CAD edits. Millimeter CAD frame: +X engine front, +Z up. Preserve positive720° event time and firing order1-5-3-6-2-4.

**Decision: a coordinated physical rotation correction is justified.** The exact-year captured timing-mark image193734596 supplies a rotation arrow missed by earlier text searches. Do not implement a one-line crank sign change or reverse event time. Current positive crank motion is inherited from the original pedagogical slider-crank convention and was not a verified operating-direction choice. The new evidence supersedes the crank-direction UNKNOWN in the frozen motion study without rewriting that historical report.

## Exact source viewing convention

Actual image193734596.png, in the1994 F-1504.9 Timing Marks and Indicators entry, was inspected directly. It is an oblique view of the damper circumference and pointer: FRONT points toward the lower page, and the circumferential ROTATION arrow at the visible near surface goes toward page-right. Take page-right as u, page-up as v and outward toward the source-image observer as n, with u×v=n. Engine-front axis is−v. At the visible radial surface r=n, an angular-velocity vector along engine-front would give (−v)×n=−u, contrary to the shown arrow. The shown +u motion therefore requires angular velocity into the engine, opposite the front axis: clockwise for an observer standing at engine front looking rearward. This is an explicit spatial interpretation of the exact-year arrow, not an OCR claim that the page spells out “clockwise.” The near/top-surface identification is an explicit assumption: FRONT alone does not exclude the opposite radial surface. The clockwise interpretation is corroborated by the Ford comparison below, rather than treating an unstated exact-year viewpoint as absolute.

Ford manufacturer CSG649 PDF page19 / printed1-15, Figure28 supplies the companion front-face view: its upper-left curved arrow goes up/right, clockwise. Text advances the starter one-third turn in firing order1-5-3-6-2-4; marks A upper-right, B left and C lower-right reach the upper pointer in that clockwise sequence. The caption is a1978-and-prior valve-adjustment procedure for an industrial comparison, not an exact-year dimensional specification. This corroborates the exact-year strip interpretation without claiming the two manuals are identical.

Exact-year image191786818.png independently shows the distributor in top view with a clockwise arrow, together with the front-of-vehicle/cylinder1 reference. Preserve the existing clockwise distributor rotation viewed from its cap end. Manufacturer-authored Ford industrial CSG649 supports clockwise distributor firing order as a comparison but is not needed to override the exact-year diagrams. The source originals stay ignored and are not republished.

The viewer maps CAD(X,Y,Z) to display(X,Z,−Y), a proper rotation with determinant+1. It increases event time and rotates the crank about+X. Viewed from engine front/+X with Z-up and Y-right, a top marker moves toward screen-left: counterclockwise. The legacy `engine.js`, current `atlas.js`, CAD `assembly_math.py` and source crank throw phases share this convention. It is not caused by a reflected display axis.

## National2692 compatibility conclusion

The exact-year OEM seal number E6DZ6700A and manufacturer National cross-reference2692 support replacement application compatibility. Timken's2692 table explicitly labels the lip clockwise-spiral. [Timken2692](https://cad.timken.com/item/seals/oil-seals-inch/2692)

A separate seal manufacturer's primary technical explanation explicitly defines CW/CCW shaft selection looking at the air side and explains return pumping by helical lip ribs. This is corroborating industry usage, not permission to attribute that wording directly to National. [deVries special helix lip design](https://www.devriesintl.com/products/shaft/spechellipdgn.asp)

For the proposed front seal, the air side faces forward/+X, so that conventional CW selection agrees with the source-supported engine direction. Verdict: source-supported replacement application and consistent expected handedness, with National2692's explicit viewing-definition and exact micro-rib geometry still unverified. Do not delay the justified crank correction for an unmodeled lip texture; do not claim the candidate's smooth lip demonstrates hydrodynamic pumping. Timken's industrial technical manual and National catalog were checked; neither reviewed portion supplied a2692-specific viewing convention. No arbitrary helix is added.

## Coordinated transformations

Let q be positive cycle/event angle, increasing0..720°. Let the existing event phases be φ=[0,240,120,120,240,0] for cylinders1..6, R=stroke/2, L=rod center distance. Source firing TDCs remain q=[0,120,240,360,480,600] for1,5,3,6,2,4.

| Item | Proposed physical rule | Required geometry/data work |
|---|---|---|
| Crank/damper/flywheel rigid rotation | αcrank=−q about+X | Rephase actual crank throws to γ=−φ modulo360=[0,120,240,240,120,0]. Rebuild bounded pins/cheeks/counterweights while protecting nose/flange/key interfaces; a whole-engine mirror is not authorized. |
| Rod/piston solver | Evaluate existing slider-crank at t=−q+γ=−(q+φ). CAD journalY=+R sin(q+φ), Z=R cos(q+φ); rod angle=asin(journalY/L). | Match actual rephased CAD journals. Piston height Rcos(q+φ)+sqrt(L²−R²sin²(q+φ)) is unchanged. Keep stroke, lengths and cylinder stations. |
| Event scheduling | valveState(q,cylinder,kind) unchanged | Preserve positive event time, firing order and intake/exhaust event centers; no blanket q→−q. |
| Cam rigid rotation | αcam=+q/2 at nominal axial datum | External timing gears still rotate oppositely. Reverse each local lobe phase from +(firingTDC+eventCenter)/2 to its negative. Keep shaft/journal/station datums. |
| Cam lobe geometry/contact | For arbitrary profiles, reflect each local lobe's angular law about its lift-center plane as well as reversing its placed phase. Current symmetric profile needs only phase reversal. | New lift support remains identical at every q; tangent contact shifts to the opposite side of the centered flat lifter. Recheck actual lobe/footprint CAD and neighboring lobes. |
| Lifters, rods, rockers, valves, springs | Keep existing lift-driven transforms as functions of positive q | Their lift/closure curves remain unchanged if the corrected physical lobes implement that same law. Do not negate rocker or pushrod rotations. |
| Distributor rotor | Retain−q/2 about its own positive shaft axis (clockwise from cap end), including established phase/terminal layout | The revised cam rotation reverses the former cam-to-distributor input direction. Re-derive crossed-helical gear hand/contact arrangement; existing drive geometry must not be assumed valid. |
| Pump/accessory driven groups | Preserve separately sourced required physical direction and derive new signed ratios from crank/cam coupling | Do not bulk-negate every `rotary` ratio. Oil-pump rotor pair, belt drive and starter/flywheel engagement require focused review. |

The existing current-phase interpretation mixes event phase and physical rest phase. An implementation must either store these separately or consistently migrate all physical `phase_deg` values to γ with signed crank angle−q. Updating only a motion field leaves exported crank geometry wrong. Piston TDCs alone cannot prove rod/crank closure.

For the existing helical candidate relation αcam=−αcrank/2+K·x, retain the geometry-derived K sign when changing αcrank to−q: αcam=+q/2+K·x. Rephased lobes then see event argument q+2·degrees(Kx), replacing the old q−2·degrees(Kx). This algebra is a dependency warning, not an accepted endplay/gear-contact result; any hand or contact-side change requires re-deriving K from the new gear geometry.

## Acceptance scope

The separate diagnostic imports the actual viewer numeric functions and checks a full720° cycle at1° increments, all six slider-cranks, all twelve cam event phases, and all six firing TDCs. It proves analytic closure/reflection relationships and detects naive-sign/time-reversal failures. It does not rebuild CAD or validate new collisions. Reproduction command: `node scripts/diagnose-engine-rotation-convention.mjs`. Root owns the shared implementation, regeneration, source/render comparison, full gear-drive checks and browser acceptance. Readiness: research/proposal; installed correction NOT DONE. Usage/model effort unavailable.

## Diagnostic results and integration handoff

`inventory/engine/engine-rotation-convention-diagnostic.json`: PASS for the bounded numeric proposal. Across 721 sampled poses, piston height difference is exactly zero; rod length error is below 5.7e-14 mm; rephased journal closure is below 1.9e-13 mm. All six firing TDCs remain exact. Cam support height difference is zero, with contact reflection and event-lift residuals below 8e-15 mm. Continuous claims come from the listed trigonometric and profile-symmetry identities, not from sample count.

The intentionally incomplete crank-only sign change separates journals by up to 101.092 mm. Reversing physical motion while retaining old rest throw phases puts four firing pistons 82.016 mm below TDC. Blanket event-time reversal changes scheduled lift by up to 6.2738 mm and reverses the already-correct distributor direction. These controls must remain failing alternatives.

Integration sequence: first declare separate signed physical phases and unchanged positive event time; regenerate rephased crank throws and cam lobes; verify actual exported journal closure and cam/lifter contact through motion; then resolve timing/distributor/oil-drive gear handedness and related accessory directions before changing installed animation. Preserve all prior source and candidate failures. The present report authorizes neither a whole-engine mirror nor an isolated visual sign patch. Browser verification and actual corrected CAD motion remain NOT RUN.
