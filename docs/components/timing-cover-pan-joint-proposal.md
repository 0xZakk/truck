# Component contract and handoff: timing-cover-pan-joint-proposal

## Contract

Issue #32 under Engine #1; worker air_cleaner_candidate, root integration owner. Baseline `124aa7c345af352459a800343ffc50f1e931367c`, branch `engine/exhaust-timing-joints`, after PR #94. Scope is source-led joint reconciliation and isolated feasibility only. No canonical geometry, source-backed pan count, crank axis or seal station changes.

Owned files: this handoff, `scripts/check-timing-cover-pan-joint-proposal.py`, `reference/engine/timing-cover-pan-joint-review.json`, `inventory/engine/timing-cover-pan-joint-validation.json`, optional `cad/engine/timing_cover_pan_joint_proposal.py`, and ignored generated directory `cad/engine/generated/timing-cover-pan-joint-proposal/`. Prior shell handoff learning gate corrected separately as explicitly requested.

Inputs: exact 1994 timing-cover and oil-pan procedures, actual Fig. 33 and Fig. 34 pixels; Fel-Pro VIN Y application review, both TCS manufacturer kit photographs, current continuous OS34601R comparison gasket, source-shaped cover candidate. Source originals stay outside Git/release. Units are model mm in world engine axes. Current block seat X373 and seal X414 are estimates. The 25 pan mounting stations remain fixed in this study.

Acceptance requires more than removing intersection: continuous support on both faces of the applicable pan gasket, explicit main-gasket terminal connection and cover/block T-joints, no leak path around bolts, retained crank seal/gear envelope and no blockage. If evidence or registration cannot establish these, deliver a measured gap and proposed datum revision rather than guessed solids. Installation, browser and user-facing learning remain NOT RUN.

## Evidence ledger

| Claim | Evidence | Classification and limit |
|---|---|---|
| Cover service disturbs front pan joint | Exact 1994 cover procedure: remove front pan screws, loosen first six per side, replace cover gasket and crank seal | Verified procedure; no joint dimensions |
| Two front cover/block seam sealant locations; 25 screws | Actual Fig. 34 pixels, `350379654.png` | Exact-year drawing; depicted multipart gasket is not the OS34601R construction |
| Both timing kits require OS34601R | Fel-Pro VIN Y catalog review | Replacement compatibility, not installed identity |
| One-piece molded gasket | Manufacturer attaches Form I-1484, revision 02/15, to OS34601R | Newly confirmed by direct installation sheet; noncoplanar rail/end architecture calls for small RTV at four block-side corners |
| Front seal replacement during cover-only repair | Manufacturer attaches Form I-223, revision 01/04, to TCS45829 | Cuts old exposed front seal flush, replaces front end seal on cover, trims gasket ends to castings if needed, adds 1/8 inch silicone bead at pan/block intersections |
| Five-hole strip role | Kit photograph plus I-223 front-end seal procedure | Consistent with replacement front-end seal, but exact five-hole part callout absent; still inferred |

Exact public PDF URLs and SHA-256 hashes are in `reference/engine/timing-cover-pan-joint-review.json`. The public Fel-Pro support page uses `pies_asset_type=INS` with its `api.catalog.productAssets` endpoint. This returned I-223 for TCS45829 and I-1484 for OS34601R; TCS45830 returned no instruction asset. Both actual PDF pages were rendered and inspected using the PDF skill. Generic diagrams must not become casting dimensions. The older factory illustration and kit photograph cannot override this distinction between complete pan-gasket replacement and a cover-only repair.

Do not add the strip over an intact OS34601R. For this reconstruction, retain the continuous gasket. I-223 describes a service cut/replacement alternative, not an extra layer. Its 1/8 inch (3.175 mm) bead specification is an application size, not permission to fill a 13 mm model gap. No chemical bead solid is added.

## Delivery

Research and rejected-registration comparison only; no new joint solid, no canonical installation, no PR created by this worker. Input geometry remains unchanged. The only prior-file change is the root-requested correction of the shell handoff learning gate to NOT RUN, plus recording root's topology-only review.

Run `.venv-cad/bin/python scripts/check-timing-cover-pan-joint-proposal.py`, then `python3 scripts/render-timing-cover-pan-joint-proposal.py`. The first script constructs the current seven-hole main gasket and current pan gasket and measures their separation. The second renders saved tessellation without rebuilding. Output: `cad/engine/generated/timing-cover-pan-joint-proposal/terminal-comparison.step`, `terminal-preview.npz`, `terminal-review.png`. This is a comparison compound, not a watertight assembled joint. STEP source parts and saved tessellation share the world engine frame; the graphic shows Y/Z coordinates.

Environment: macOS 15.6.1 arm64, Python 3.13.12, build123d 0.10.0, trimesh 4.7.4 in `.venv-cad`; system Python NumPy/Matplotlib for render. Model/effort and usage unavailable. Inputs are the prior normalized outline, shell parameters and pan V9 candidate; their hashes and checker hash are in `inventory/engine/timing-cover-pan-joint-validation.json`. No assembly manifest is consumed or certified. Reference PDFs/images are ignored captures and must not enter Git or releases; public URLs permit re-fetching. No release URL is created.

## Validation and review

The actual comparison render exposes two separated paths. The lowest region of the main gasket's long leg is 13.625 mm from the complete unchanged pan gasket. The short-leg region is 37.2278 mm away. The full main gasket minimum distance is 13.625 mm. These are current-model values, not factory measurements; the terminal regions conservatively include the low portions of both open legs. Both have zero contact overlap, which is a failure of contact, not a success of clearance.

| Gate | Result | Scope |
|---|---|---|
| Source/application | PASS within scope | Exact-year procedure, catalog compatibility, actual manufacturer instruction sheets |
| Dimensions/coordinates | REJECTED registration | Current main-gasket endpoints cannot meet current pan joint |
| CAD/export | Comparison only | Current gasket shapes and derived STEP/tessellation exported; no new solid acceptance or watertight-joint claim |
| Source/visual | PASS for gap review | Actual source pages and CAD overlay inspected; source drawings generic or unscaled |
| Continuous seating / terminal sealing | FAIL | No terminal contact; no leak-path proof possible from this registration |
| Installed interfaces | NOT RUN | No canonical edit; prior pan/bridge collision remains |
| Fault controls | NOT RUN | No proposed sealed joint exists to challenge; absence of contact directly rejects baseline |
| Motion/disassembly | NOT RUN | No installed joint or fastener engagement revision |
| Learning/diagnostics | NOT RUN | Developer evidence is not user-facing function/diagnostic content |
| Browser | NOT RUN | Offline graphic is not browser acceptance |
| Reproduction/review | Worker reviewed | Deterministic checker, inputs and generated artifact hashes saved; root joint review pending |

## Coherent next proposal and restart

The intended topology is the continuous OS34601R front segment seated between pan and the combined block/cover surface, with the main cover gasket ending at the same two T-joints. The cover seat must follow the complete upper front-gasket path, including curved and flat portions. Under current model parameters this means the upper radial surface at radius 59.4 mm over X365–381, joining the rail seat at Z−32 mm. These are inherited estimates, not source measurements. They are proposed targets only; no surface is built while the terminals fail.

Re-establish the in-plane cover/gasket-to-crank registration from a suitable orthogonal image or dimensional specimen, retaining the primary normalized contour. Then solve both terminal locations and gear envelopes together. Preserve crank YZ(0,0), seal X414 and the 25 pan stations during that comparison. If the provisional pan end or stations prove incompatible, return an explicit coordinated revision preserving the supported count; do not move by eye or distort the source outline. Rear cover face X373.8 and block plane X373 remain model datums only.

Any future joint must pass full-area contact on both gasket faces; both terminal connections; continuous perimeter sealing with fastener holes excluded; missing front-seal and missing terminal-sealer fault controls; fixed seal and gear checks; pan screw engagement/removal; and adjacent block oil-path review. Simply subtracting the old 1421.2092 mm³ bridge overlap would satisfy none of these terminal requirements, so it was not performed.

Issue #32 remains open. Exact next action: root review of the new instruction-sheet interpretation and rejected-registration graphic, then a source-supported in-plane datum proposal. No process is running. Logs reside in the isolated generated folder. No original source or manual pages are redistributed.
