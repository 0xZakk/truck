# Component contract and handoff: pan-fastener-thread-candidate

## Contract

- Issue #32 / Engine #1. Candidate worker owns this isolated revision; root is integration owner. Baseline `eb502ce755d12fe896b3ea915f3ada4361e52a9c`, branch `engine/timing-interface-reconciliation`. The validation report binds the assembly manifest SHA-256.
- Root authorized a reusable male revision after the rejected attachment study. No canonical files, sockets, stations or prior proofs change. Preserve the accepted front joint and rejected attachment evidence.
- Owned files: `cad/engine/pan_fastener_thread_candidate.py`, `scripts/check-pan-fastener-thread-candidate.py`, `scripts/render-pan-fastener-thread-candidate.py`, this handoff, `inventory/engine/pan-fastener-thread-validation.json`, `reference/engine/pan-fastener-thread-review.json` and generated `pan-fastener-thread-candidate/` directory.
- Preserve verified nominal 5/16-18 × 0.87 in: major diameter 7.9375 mm, pitch 25.4/18 mm, under-head length 22.098 mm. Existing head and washer dimensions remain explicit model estimates. Preserve reusable definition `oil-pan-mounting-screw` and all 25 occurrence IDs; the report records their unchanged transforms. No service part number established.
- Local CAD units are millimeters. Screw axis is +Z; under-head seating plane is Z = 0, head extends to −5.3, tip to 22.098. Existing washer occupies Z = 0 through 1.6. No parent transform or explode transform is installed. Display export maps CAD (X,Y,Z) to (X,Z,−Y) in meters.
- Neighbors are the existing separate washer and an isolated female test coupon. Coupon is a test fixture, not an additional physical insert. No cover, block land or oil-pan changes are authorized in this module.
- Inputs are the existing screw/washer STEP files, current assembly manifest and reviewed exact-year fastener callout. All are locally available. Source-image redistribution remains excluded.
- Acceptance requires original and STEP-roundtrip validity, single solids, watertight meshes, preserved nominal bounds, head/washer support, matched helical advance and meaningful wrong-phase faults using both Boolean volume and independent point classification. Root review precedes adoption.

## Evidence ledger

| Claim / feature | Value and datum | Evidence class | Source | Uncertainty |
|---|---|---|---|---|
| Pan fasteners | 25 screw-and-washer assemblies, 5/16-18 × 0.87 in | Exact-year nominal callout | 1994 oil pan Fig. 34, drawing 350379654; `reference/engine/ford-oil-pan-hardware-reviewed.json` | Does not dimension detailed head, washer or thread form |
| Head / washer | Head AF 12.7, height 5.3; washer OD 15, ID 8.3, thickness 1.6 mm | Preserved model convention | Existing canonical definitions and STEP inputs | Not factory measurements |
| Detailed thread | Root radius 3.2, crest width 0.2, included flank angle 60 degrees, 0.1 mm runout | Explicit educational estimates | Candidate parameters | No thread class, tolerance, preload or strength claim |
| Geometry construction | Repeated one-turn radial/axial loft | Algorithmic reference | Apache-2.0 `bd_warehouse` thread.py `_make_thread_loop`; URL in review ledger | Independently expressed 13-section loft; not vehicle evidence |

## Delivery

- Submitted as uncommitted isolated files on the named branch; root owns PR/checkpoint integration. Readiness: **candidate, local checks PASS; not installed**.
- APIs: `screw()` returns one local solid; `female(male)` returns one zero-clearance conjugate test coupon. No production female socket is supplied.
- Outputs: `cad/engine/generated/pan-fastener-thread-candidate/` contains separate STEP/GLB parts, combined `candidate.glb`, render input `preview.npz`, actual `thread-review.png` and `validation-console.txt`. Review ledger records SHA-256 hashes. No asset release was published.
- Reproduce from repository root: `.venv-cad/bin/python scripts/check-pan-fastener-thread-candidate.py`, then `python3 scripts/render-pan-fastener-thread-candidate.py`. Checker needs build123d and trimesh; renderer uses NumPy and Matplotlib. No new dependency installed.
- Environment: macOS 15.6.1 arm64, CAD Python 3.13.12, build123d 0.10.0, trimesh 4.7.4. Model effort and billing usage unavailable. Ezdxf cache-home warning is harmless to outputs; no personal cache required.

## Validation and review

| Gate | Status | Evidence and result | Limits |
|---|---|---|---|
| Application/coverage | PASS, nominal only | Exact-year 25-place callout; 25 stable IDs bound | Detailed production thread unknown |
| Dimensions/coordinates | PASS | Observed major diameter 7.937616 mm; tip error 0.0000001 mm; head/collar Boolean differences zero | Explicit estimated root, crest, runout and head/washer |
| CAD/export | PASS | All three original and roundtrip solids valid; raw, roundtrip and GLB meshes watertight; STEP volume deltas below 0.000001 mm³ | Coupon is a test fixture |
| Source/visual comparison | PASS, bounded | Worker inspected actual `thread-review.png`; nominal screw/washer topology retained | No specimen comparison establishes detailed factory geometry |
| Installed interfaces | NOT RUN | Local washer support missing volume and screw/washer overlap both zero | Five relocated sockets and all 25 installed locations require checks |
| Motion/disassembly | PASS, local coupon only | Five matched rotation/advance poses have overlap below 0.000094 mm³; axial-only ±0.3 mm faults overlap 50.46 / 51.19 mm³ | Does not validate full extraction or tool access |
| Independent negative controls | PASS | 720 samples per pose: matched 0 and 90 degrees both zero common points; faults 152 and 154 common points | Finite sampling supplements Boolean proof |
| Learning/diagnostics | NOT RUN | No component lesson supplied | Development failure notes are not learning content |
| Browser integration | NOT RUN | No installed assets | CAD render is not browser acceptance |
| Reproduction/review | PASS locally; root pending | Deterministic checker, recorded inputs and export hashes | Integration owner must review before adoption |

The nominal female coupon has no radial or axial manufacturing clearance. Its shape is exactly conjugate to the estimated male. The matched phase and wrong-phase controls demonstrate a meaningful helical interface, not a certified manufactured thread fit. Direct positive-area flank contact and production tolerance qualification are outside this isolated report.

The earlier long-sweep approach and coincident collar seam were rejected. A 0.1 mm estimated runout removes the diagnosed meshing seam without lowering the watertightness gate. The frozen attachment report remains rejected; this report does not retroactively validate its socket or collision results.

No integrated neighbor changes occurred. Root may accept these files as a bounded candidate; installed acceptance requires regenerated proposed sockets, actual engagement/support checks, all 25 station interfaces, learning content and browser review.

## Tracking and restart

Issue #32 remains open. Next action: root reviews `thread-review.png` and the validation report; if accepted, regenerate only the separately authorized five proposed female socket interfaces against this reusable male and recheck land walls, seal regions and engagement. Preserve the 20 unchanged station transforms and the frozen joint exports. Eventual reuse at all 25 screws requires root coordination.

No process remains running. Exact checker output is preserved under the generated directory. Worker/coordinator token and billing usage are unavailable.
