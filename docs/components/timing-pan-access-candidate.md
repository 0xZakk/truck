# Component contract and handoff: timing-pan-access-candidate

## Contract

Issue #32 / Engine #1; integration owner root. Baseline 8547c589d3c086bad91baf879219612bcd9a162f; focused branch engine/timing-support-joints. Isolated candidate only. Own `cad/engine/timing_pan_access_candidate.py`, dedicated check/render scripts, validation JSON, this handoff and `cad/engine/generated/timing-pan-access-candidate/`. No frozen v2 or shared assembly changes.

Root approved broad estimated inner X374 / outer X378 front wall and independent station-10 dry-side transition. Preserve all 25 stations, all rear X≤335, full gasket lands and washer seating, and continuous oil boundary. World CAD millimeters, identity transform, +Z screw axes. Frozen v2 STEP parts and accepted screw/washer are locally present. Access shape is constructed from explicit outer/inner profiles; no subtraction of neighboring hardware. Estimated station-10 outer side Y184 / inner Y180 leaves 1 mm to a radius-11 socket about Y196. Shoulder Z−80..−76 joins inherited lower body. No factory stamping, capacity or tool specification claim.

Planned commands: `.venv-cad/bin/python scripts/check-timing-pan-access-candidate.py`; `python3 scripts/render-timing-pan-access-candidate.py`. Existing 0.1 mm³ collision threshold; 0.01 mm³ preserved-material and seat threshold. STEP valid single solid, watertight export, bounds roundtrip, explicit oil-envelope and wall samples, bad-condition controls. Browser NOT RUN due established security rejection; no alternate browser attempted. GitHub issue read attempted but network unavailable; root holds issue context.

## Evidence ledger

Nominal 25 screw/washer stations inherit exact-year Fig. 34 / 350379654 evidence. New wall, side transition, corner and tool dimensions are inferred model-design estimates. Input sources and hashes recorded in validation report. No new manufacturing dimensions.

## Delivery

In progress; uninstalled candidate. API `build()` returns candidate pan and frozen pan. All other sealing and fastening inputs remain frozen. macOS existing Python 3.13 CAD environment, build123d 0.10.0; no dependency changes. No release yet; clean-clone inputs require frozen timing-support artifact restoration.

## Validation and review

All gates pending. Root review required; no accepted-installed claim.

## Tracking and restart

Issue remains open. Usage/model/effort unavailable. Dedicated command above is restart entry point. No shared file writes authorized.

## Submitted result and limitations

**FAIL; uninstalled candidate for root review.** Source `build()` constructs outer/inner lofts, a shoulder and preserved flange; it never subtracts a hardware solid. Actual exported sections are in `cad/engine/generated/timing-pan-access-candidate/review.png`. Frozen v2 remains unchanged.

All five screw and washer overlaps are zero, all five full washer-seat probes pass, and the entire inherited front flange is preserved. Rear X≤335 has zero added/removed material. All five other sealing parts have zero pan overlap. Sampled front/side walls and shoulder have zero missing probe material. The single pan solid is valid before/after STEP and its export mesh is watertight; roundtrip volume difference is about 0.00000064 mm³, mesh bounds difference 0.0000001 mm.

These local successes do not establish acceptance. The declared estimated radius-11 mm axial socket envelope overlaps station 10 by 0.9078 mm³. Station 20 returns an unresolved adaptive-integration measurement and is marked null in the report, with diagnostic nonadaptive volume and bounds provided separately. No tolerance was loosened. The first integration exception is preserved in `first-check-failure.txt`. Front socket-envelope stations 21/23/22 have zero solid overlap; the cylinder ends at the flange plane, so its distance includes intended terminal-plane contact and must not be read as radial clearance.

A broad proposed wet-channel witness intersects 162.3776 mm³; the checker compares it with the frozen pan to distinguish inherited boundary shape from new obstruction. This probe is not a complete oil-volume definition. Full containment, corner thickness, top closure and inlet-to-sump continuity require a proper sealed-volume contract and remain NOT RUN. A valid single pan solid and wall samples do not prove those properties. No capacity claim.

| Gate | Status | Evidence / remaining scope |
|---|---|---|
| Application/coverage | PASS bounded | Exact-year nominal screw count inherited; stamping estimates explicit |
| Dimensions/coordinates | PASS bounded | World millimeters, five frozen transforms, rear unchanged |
| CAD/export | PASS | Valid single solid, watertight mesh, STEP roundtrip; output hashes in report |
| Source/visual comparison | NOT RUN for factory fidelity | Actual sections reviewed locally against frozen failure; no new manufacturing source |
| Installed interfaces | FAIL/open | Heads, washers, flange and seal overlaps pass; full oil containment unresolved |
| Motion/disassembly | FAIL | Estimated socket access fails station 10 and is unresolved at station 20 |
| Learning/diagnostics | NOT RUN | No user-facing lesson |
| Browser integration | NOT RUN | Uninstalled; prior browser security rejection honored |
| Reproduction/review | Local commands and hashes provided; root pending | Generated assets not yet published; frozen dependencies require artifact restoration |

Next action: root review actual `review.png`, then localize the station-10 tool sliver and station-20 intersection without changing frozen gasket lands; define a complete oil-space enclosure before wall acceptance. Preserve this failed candidate if another revision is started. Run commands from Contract to reproduce; no background process is claimed after handoff. Root owns issue/PR publication and integration. Shared navigation unchanged, so navigation check is N/A for this isolated uninstalled artifact. Python syntax check passed for all three owned source/check/render files. No new model was installed.

Final diagnostics: the broad wet-channel witness has the same 162.377556923 mm³ overlap in frozen v2, so it does not demonstrate a new blockage; it is unsuitable as a whole-channel acceptance probe. Station 10's actual tool intersection bounds are X357.3715..359.0000, Y187.1259..192.1534, Z−31.0089..−30.5000, localizing the residual sliver at the inherited flange transition. Station 20's valid intersection spans X354.5..376.5, Y−143..−121, Z−80..−30.5; diagnostic nonadaptive volume is 2636.4256 mm³, but the strict adaptive result remains unresolved. The left transition must be checked explicitly before any tool-access claim. No process remains running at this handoff.

Integration-owner continuation reports current branch `engine/timing-clearance-revisions`, merged base `4e480f8`; this candidate's geometry inputs remain bound to the original frozen v2 hashes. A potential separate primary tool comparison is TEKTON SHD03013 (`https://www.tekton.com/1-4-inch-drive-x-1-2-inch-deep-6-point-socket-shd03013`, dimensional image `https://images.tekton.com/assets/SHD03013_spec.jpg`). It was supplied by root but not inspected or adopted in this delivery. Original R11 failures remain; no smaller tool or modified threshold substitutes for them. Avoid arbitrary vehicle geometry changes merely to fit that illustrative tool. Priority remains continuous wet boundary and actual fastener fit.
