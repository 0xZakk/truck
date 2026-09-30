# Component contract and handoff: timing-cover-registration-study

## Contract

Issue #32 under Engine #1. Root integration owner; air_cleaner_candidate contributor. Baseline `124aa7c345af352459a800343ffc50f1e931367c`, branch `engine/exhaust-timing-joints`. Isolated source-registration and feasibility study only; no canonical changes or new installed joint. Preserve all prior rejected artifacts and the supported 25 pan stations/count.

Owned: `scripts/check-timing-cover-registration-study.py`, `reference/engine/timing-cover-registration-review.json`, `inventory/engine/timing-cover-registration-validation.json`, this handoff and `cad/engine/generated/timing-cover-registration-study/`. Inputs: seven main-gasket hole centers and unchanged normalized contour; actual Dorman 635-109 photos 001/002/003/007/009; current pan parameters; current and alternative gear axes.

Reconcile plane homography versus physical similarity registration and image mirroring explicitly. Use aperture boundary, not guessed image center, to estimate the crank point and show uncertainty. Projective image correction may explain camera perspective; it must not projectively warp a CAD outline to force fit. All mm scales remain estimated. Acceptance is a quantified feasible parameter envelope or a clear incompatibility proof, not a manufactured dimension claim. No browser or user-facing learning completion.

## Method and evidence

Dorman photos 001, 002, 003 and 007 were inspected alongside the separate gasket photo 009. The seven holes are indexed from the long terminal around the arch to the short terminal. This indexing resolves visual rotation and reversal; photo orientation is not treated as engine orientation. Source points, actual image sizes and capture hashes are retained in the review. The source gasket image is a product photo, not a dimensioned orthographic drawing, so its metric shape also remains approximate.

A seven-point homography maps source-gasket pixels to photo 002 with residuals 0.26–2.17 pixels. A uniform similarity fit instead has RMS 28.61 pixels. The separate gasket photo 009 likewise needs perspective correction (homography RMS 1.46 versus similarity RMS 24.95 pixels). This supports using a projective transform to compare photographed points. It does not license a projective warp of the CAD contour to meet pan constraints.

The source-to-photo mapping reverses handedness: its best orthogonal mapping has determinant −1. Global study plots use +Y to the right and +Z up, with the cam on +Y. A photo taken from the opposite face reverses that display convention. Both physical Y reflection choices are tested; the mirrored-lobe choice does not fit the protected +Y cam envelope. Front/oblique photos are qualitative confirmation of the seal boss, lower bridge and opposite views; their partly obscured bosses are not fabricated into a second seven-point fit.

The crank estimate now comes from 24 boundary points of the actual white seal aperture in photo 002, not a guessed center. Points were extracted from the grayscale >160 connected region containing pixel (205,198), sampled at 24 angles; the code retains their coordinates. Thresholds 100–220 gave a bounded aperture region approximately X163–250/Y172–235. Mapping this boundary into the source-gasket view and fitting a circle gives crank point (588.537,930.475), radius 92.863 pixels, RMS deviation 3.976 pixels. The prior (595,955) point is superseded only for this study, not overwritten in old candidates.

The aperture is at a different axial depth from the flange holes. A single-plane homography cannot remove that parallax. Its circle fit is therefore an approximation, not a recovered factory crank datum. A deterministic 120-trial perturbation study uses ±3 source-hole pixels, ±5 photo-hole pixels and ±4 aperture-edge pixels. The central 95% interval is X571.904–603.484/Y921.281–939.705; it excludes unknown systematic depth parallax, lens effects and product-photo metric distortion. The current provisional seal inner radius 21 mm would imply scale 0.22614 from this aperture; this is a consistency comparison, not a source dimension or an instruction to resize the seal.

## Feasibility comparison

Only uniform scale, rigid in-plane rotation and a tested reflection change the original outline. The crank is fixed at YZ(0,0). The homography is never applied to CAD geometry. Parameters are `[mm per reference pixel, crank source x, crank source y, rotation degrees]`. The two cam axes are (90,72) and (95.109821,76.087857). A 360-point circle at radius 86.947 mm protects each source 83.947 mm tip radius plus estimated 1 mm clearance and 2 mm shell wall. The check uses the cover's outer arch, not its gasket inner edge: the gasket flange is axially behind the gears in the prior shell proposal. Crank lower-bridge containment is deliberately not claimed.

The optimistic current pan terminal corridor is Y−140..116.6 at Z−32 mm. All sampled low terminal-edge points must land in that corridor; corners of the actual pan can only reduce available support. Searches cover scale 0.16–0.34, rotation ±30 degrees and the pixel perturbation crank interval, with both reflections. The best found unmirrored tradeoff still has 24.057 mm maximum violation, balancing missed terminal support and inadequate gear-wall enclosure. The reflected choice gives 92.206 mm. Expanding the unknown crank registration to X450–800/Y750–1100 and scale to 0.38 still leaves 14.663 mm. These are reproducible numerical search results within stated bounds, not a global mathematical proof for every conceivable camera or casting.

The useful coordinated alternative keeps the aperture-based crank point and fits a flat terminal direction from the source edge samples: −0.03982 degrees, rather than silently assuming zero. Minimum nominal scale for both gear envelopes is 0.25585. Including an additional eight-reference-pixel trace reserve gives scale **0.262233**, with 2.09786 mm extra outer-envelope margin beyond the protected circles. This is a feasibility-selected estimate, never a manufacturer dimension. It preserves the original outline and fixed crank/seal stations.

At that estimate the terminal corridor spans **Y−141.240..204.908 mm** and **Z−26.807..−24.704 mm**. Relative to the optimistic current pan corridor, the cam-side seat must reach about **88.3 mm farther**, and terminal level is **5.2–7.3 mm higher**. The small Z spread reflects the traced edge; a future smooth/trimmed seat needs explicit review rather than treating it as a wavy production surface. A local widened/asymmetric front flange is a coordinated candidate option; this does not require widening the entire pan sump by assumption. The 25 fastener count is supported and retained. Their current coordinates are still unchanged and would need a clamp/engagement review before a proposed flange could be accepted.

Pixel-interval corner sensitivity repeats the envelope sizing at all four crank-coordinate bounds; exact ranges are in the validation report. That bounds the stated pixel perturbation effect only. Depth parallax remains an open degree of freedom. The root must choose and record an estimated design hypothesis before any new joint is built.

## Delivery and gates

Commands: `python3 scripts/check-timing-cover-registration-study.py`, then `python3 scripts/render-timing-cover-registration-study.py`. The latter is also owned by this study. They use system Python 3.13.12 with NumPy, SciPy, Matplotlib and the existing source-outline text; CAD packages are not needed. Temporary Matplotlib cache fallback is harmless. Seed 32094 governs perturbations, seed 32 governs numerical search. No original photos are required to reproduce the stored-coordinate calculations; exact hashes and URLs support renewed visual review.

Outputs: `inventory/engine/timing-cover-registration-validation.json`, `reference/engine/timing-cover-registration-review.json`, and `cad/engine/generated/timing-cover-registration-study/registration-review.png` with supporting NPZ. The four-panel figure shows camera correspondence, aperture uncertainty, both gear envelopes and the required pan corridor. No new solid or STEP is produced, so watertight export is N/A. Primary photos remain excluded from Git and releases. No release URL or PR created by this worker. Baseline manifest is not consumed or certified; model/effort and usage unavailable.

| Gate | Result | Limit |
|---|---|---|
| Source/application | PASS for comparison | Manufacturer replacement specimen; no factory metric drawing |
| Coordinates/uncertainty | Quantified estimate | Camera handedness and perspective separated; depth parallax unbounded |
| Same-outline feasibility | Current pan rejected within search | Both cam envelopes tested, no canonical transform selected |
| Source/visual | Worker inspected | Original pixels and derived figure reviewed; root final review pending |
| CAD/export | N/A | Numeric registration study only |
| Seat/contact/terminal continuity | NOT RUN | Required corridor proposed; no assembled joint yet |
| Motion/disassembly | NOT RUN | Static cam disks only; crank bridge and bolts need subsequent checks |
| Learning/diagnostics | NOT RUN | Developer plots are not complete user-facing component learning |
| Browser/installation | NOT RUN | No installation or browser acceptance |
| Reproduction | PASS within numeric scope | Deterministic scripts, source samples and input hashes |

## Root decision and restart

Root accepted the earlier terminal-gap rejection and allowed a wider/asymmetric front pan corridor to be considered. This delivery proposes that finite coordinated envelope; it does not alter the pan to make the old report pass. Review it together with the same-ray 121.8 mm timing-core hypothesis. Neighbor revisions would involve the cover lower bridge, block front land, pan front flange and front portions of its rails, continuous pan gasket, and front screw seating/engagement. The fixed crank and seal station X414 stay unchanged; no identified strip is stacked over OS34601R.

Next action is root selection of the estimated joint hypothesis and authorization of the corresponding isolated cover/block/pan candidate. That candidate must construct both main-gasket terminal T-joints, continuous upper/lower support, protected crank/gear cavities, bolt seals and a valid extraction path. It must then pass actual CAD/mesh checks and missing-seal/terminal fault controls. Issue #32 stays open. No process remains running after delivery, and all prior failed figures/candidates remain untouched.
