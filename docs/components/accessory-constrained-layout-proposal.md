# Component contract and handoff: accessory-constrained-layout

## Contract

- Issues #32/#34, engine system; contributor pan_access_resume; integration/review owner root. Predeclared scope: `accessory-constrained-layout-contract.md`.
- Creation baseline e6dc8fcd68e28ff201ee2cd9b69aee0bb8a588eb; delivery branch engine/timing-drive-fit. Shared branch advanced to 6b1608257e8c2eaa12512ac0c256d882854f3996 during study. Frozen private v3 SHA f512d6024ed4d3d0d86c45c39492b4ab525e039a9c50fb71b67940633b8a2055 remains the checked assembly.
- Research/candidate pose feasibility only. Own new accessory-constrained-layout scripts/reports/docs and generated folder. No canonical, runtime, existing component or carrier edits. No manufacturing or installed acceptance.
- Units mm; engine world X shaft/front direction, Y/Z transverse coordinates. Retain each part's local origin/rotation, stable occurrence ID and parent. Proposal is world translation (0,ΔY,ΔZ) of explicitly owned rigid branches; any future serialized patch must convert through parent inverse. Two common carriers require replacements. Engine attachment hardware stays fixed, including thermactor-engine-bolt-1/2 despite their inherited moving parent.
- Actual v3 geometry, q0 adapter, mesh assets and exact relevant STEP files are hash-bound in reports. Authorized source manual/photos remain private access dependencies; no restricted images redistributed.
- Screen: 25 mm axial slabs over X250..550, actual mesh-edge intersections and conservative convex configuration obstacles; 1 mm exterior trial reserve. Tensioner reserve additional 11 mm for inferred ±5°/75 mm arm envelope. Exact q0 broadphase padded 2 mm; historical 0.1 mm³ intersection gate. Restoring old AC pose is the fault control.

## Evidence ledger

| Feature | Value/datum | Evidence class | Source / locator | Limits |
|---|---|---|---|---|
| Routing | ALT→TENS→PS→AC→WP→CS→AP; WP/TENS backside | applicable Ford diagram | 1994 manual image DM05Q313/ford10/212084317.png, SHA cb47b6d8dd2899cd32f86f62dc86d264182f417888b65ec568517bb2a1be5216 | ordering, not metric centers |
| Shared right carrier | front-head, side-head, two block-stud attachments | applicable topology | Ford TSB94-10-19 Fig4; previous block-FS10 investigation ledger | seat coordinates remain estimates |
| Diameters CS/PS/AC/TENS | 163.068/131.318/145/90 mm outside | replacement comparisons | Dorman594-152 /300-029; UACCO101220C; Gates38022, captured in frozen investigation | PS published five grooves conflicts six-rib application; identity unresolved |
| WP/ALT/AP diameters | 150/70/140 mm | illustrative estimates | current source models | no measured production pitch diameters |
| Belt | K060980/6PK2491, effective2491 mm | replacement comparison | frozen accessory source research | effective is not geometric cord length |
| Effective radius bounds | grooved outside−3.45..outside; smooth outside..outside+2.7 mm | inferred trial uncertainty | generic prior belt profile | not calibrated confidence bounds or belt manufacturing tolerance |
| Tensioner | 75 mm arm, ±5° trial movement | inferred | inherited support geometry; numerical trial | spring preload, stops and actual working range unknown |
| Broad cover shape | retained v3 source-correlated silhouette | source comparison | frozen block-FS10/Dorman independent registration reports | no narrowed compressor-shaped contour |

## Selected numerical proposal

All five weak centers move together. Fixed crank(0,0), WP(−32,170), axial belt-plane estimate X473.56 and engine anchors remain unchanged. No shaft inversion or X movement.

| Branch | Old Y,Z | Proposed Y,Z | ΔY,ΔZ mm |
|---|---|---|---|
| ALT | −325,320 | −262.012039,243.569847 | +62.987961,−76.430153 |
| AP | −280,100 | −201.832511,124.393728 | +78.167489,+24.393728 |
| PS | 280,410 | 289.501109,346.563747 | +9.501109,−63.436253 |
| AC | 280,100 | 337.435375,140 | +57.435375,+40 |
| TENS | 167,350 | 129.498190,316.277747 | −37.501810,−33.722253 |

Objective minimizes squared displacement/100 mm plus PS/AC column deviation/100 mm. Selected objective3.03687835 is a local feasible result, not a proved global optimum. All domain bounds and constraints are retained in scripts. Stronger30 mm source-order separation is an **inferred hypothesis**; it is not measured from diagram pixels. PS above TENS includes0.286 mm movement allowance. AC upperZ140 is active. Catalog interval lower reserve is active. Preserve10/20/30 mm hypotheses and all seeds.

Qualified effective proxy interval2486.000..2516.181 mm includes2491 with at least5 mm interior reserve. That reserve is numerical, not a Gates tolerance. Length depends jointly on inferred profile offsets and inferred tensioner movement; it does not establish an available belt installation. `review-route.json` gives the separate illustrative cord route2533.803979 mm; its42.803979 mm difference from2491 is not interpreted as an effective-length error. No belt solids exported.

Rejected records remain: first engine-bolt ownership error; integer truncation of the order margin; static-only result with roughly2938 mm cord loop; weak1 mm ordering solution reachingAC Z169 and catalog uncertainty endpoint. Rejected scripts/reports are preserved in generated subfolders. No silent relaxed threshold.

## Support and connection interface proposal — review before CAD

1. **PS/AC/TENS carrier.** Preserve engine-side attachment seats and axes from accessory_carrier_1994.py: block stations(X292,Z110),(X340,Z110), side-head(X340,Z310), and front-head(Y90,Z300). Existing engine-side Y coordinates/foot profiles remain estimated but frozen for this proposal. Join them to the new accessory seats through a new analytically defined carrier, not translated old webs or neighbor cuts. PS faceX432.56, ears radius62 at45/165/285° around new center. AC faceX432.56 and four new ear axes(Y267.435375 or407.435375,Z100 or180); preserve actual hole/annular seat profiles and fastener engagement. Provisional tensioner pivot(Y129.498190,Z391.277747), inherited axial frame. All seat contact, continuous support stock, fastener access/retention, stiffness and swept clearances remain unverified.
2. **ALT/AP common carrier.** Keep ALT engine feet(Y−100,Z220/310), AP feet(Y−100,Z90) and(Y−125,Z140), all original engine-side X seats/holes. ALT accessory faceX438.56; revised ear axes(Y−185.012039 and−339.012039,Z243.569847). AP faceX449.06; ears(Y−116.832511 and−286.832511,Z124.393728). Open cradles/linked spine topology must connect these actual seats with positive material contact; do not rigidly move old spine. Closest ALT/AP body clearance is only2.197902 mm: do not insert support material in that gap without a separate fit check. Protect WP rear mounting/bearing interfaces, all cover main lands, broad gasket, and fixed engine hardware.
3. **Waterpump uncertainty.** Primary checker uses actual installed v3 pump. Separate source-offset inlet WORLD STEP nominal/low/high hypotheses clear moved bodies; tightest low-offset/AP front plate1.028187 mm. They do not certify new carrier stock. Require new support to clear all three or explicitly return conflict; old low-offset/old-carrier FAIL remains. Heater tube candidate remains rejected and is not a substitute neighbor.
4. **External endpoints.** AC manifold suction/discharge seal centers retainX≈278.56 and move to(Y357.435375,Z160)/(Y375.435375,Z116). PS outlet fitting region center moves to(Y340.501109,Z356.563747), X359.167695..379.952305; this bounding region is not a derived bore datum. No complete installed AC/PS hose route exists to preserve. New matched hose/line contracts must preserve remote endpoints, port-axis seating and bend/engine-motion allowances. ALT electrical connections, AC clutch lead, thermactor plumbing and fixed endpoint wiring need explicit inventory and reconnection; rigid branch clearance does not cover them.
5. **Belt/tensioner.** Verify actual pulley identities/groove count, effective radii and tensioner stop/preload range before claiming selected catalog fit. Build belt only after those decisions, then check actual belt solids, wrap/traction, working sweep and service removal. Current ±5° proxy and source ordering are feasibility assumptions. No load/material/fatigue claim.

## Delivery

Research proposal, ready for integration-owner support-contract review; not integration-ready assets. Entry points are scripts/accessory-constrained-layout-{envelopes,solve,catalog-solve,order-sensitivity,step-check,waterpump-sensitivity,render}.py. No new production STEP/GLB or canonical patch. Reports use same prefix under inventory/engine; generated obstacles, rejected trials and review.png are under cad/engine/generated/accessory-constrained-layout. Final file hashes: inventory/engine/accessory-constrained-layout-delivery.json.

Reproduction from repository root, with available authorized frozen CAD assets:

```sh
.venv-cad/bin/python scripts/accessory-constrained-layout-envelopes.py
.venv-cad/bin/python scripts/accessory-constrained-layout-solve.py
.venv-cad/bin/python scripts/accessory-constrained-layout-catalog-solve.py
.venv-cad/bin/python scripts/accessory-constrained-layout-order-sensitivity.py
.venv-cad/bin/python scripts/accessory-constrained-layout-step-check.py
.venv-cad/bin/python scripts/accessory-constrained-layout-waterpump-sensitivity.py
.venv-cad/bin/python scripts/accessory-constrained-layout-render.py --extract
python3 scripts/accessory-constrained-layout-render.py
python3 scripts/accessory-constrained-layout-freeze.py
```

macOS, Python3.13/build123d0.10 locked CAD environment, NumPy/SciPy/trimesh; system Python matplotlib renders. Cache-directory warnings are environmental; render succeeds. No installation performed. Model/effort/usage unavailable. No published artifact URL yet; root owns packaging.

## Validation and review

| Gate | Result | Evidence | Limitation |
|---|---|---|---|
| Application/coverage | PARTIAL | frozen Ford/source comparison ledger | actual pulley identities/range unknown |
| Dimensions/coordinates | PASS bounded numerical contract | envelopes/selection input hashes | centers explicitly inferred |
| CAD/export | N/A new assets | existing actual STEP/GLB reused | no new carrier/belt CAD |
| Source/visual comparison | PARTIAL | retained source topology; actual review.png | no measured production silhouette match |
| Installed interfaces | NOT ACCEPTED |47 changed q0 STEP pairs clear, no errors; smallest2.197902 mm | replacement carriers, hoses, belt absent |
| Motion/disassembly | NOT RUN full system | inferred tensioner screen reserve only | real range/loads unknown |
| Learning/diagnostics | NOT RUN | no user-facing lesson changes | numeric bad-pose control is checker evidence only |
| Browser integration | NOT RUN | canonical unchanged | no installed candidate |
| Reproduction/review | hash-bound; root review pending | delivery manifest, saved scripts/rejections | private source/artifact access required |

Wrong old AC pose detects17596.474199 mm³ cover intersection. Same-branch rigid relationships are unchanged and not re-certified. Broadphase separated pairs rely on padded actual mesh bounds; all47 remaining pairs checked actual STEP. The separate pump sensitivity is conditional and includes no replacement support. No full assembly, working belt, source dimensions, stress, fluid containment or installed acceptance follows.

## Tracking and restart

Issues remain open for support review and unresolved physical interfaces. Next action: root reviews this shared support/connection contract and actual mesh render before authorizing carrier construction. No process remains running at handoff. No shared files changed; root alone may create future guarded pose/asset patches. Prior defects and source investigations remain frozen.
