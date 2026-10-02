# Component handoff: oil-pump dowel hardware evidence

## Contract

- Issue #73 / engine lubrication; worker pump_foot_resume, integration owner root.
- Research only, baseline `1163acf633ddab3a5bed0cd126a6becca8ddd741`. No assembly manifest altered; no CAD or installed pose proposed.
- Owned files: this handoff, `reference/engine/oilpump-dowel-20261002-evidence.json`, `kb/sources/oilpump-dowel-20261002-ford-hardware.md`, `kb/notes/oilpump-dowel-20261002-nominal-dimensions.md`.
- Resolve the hardware identity independently of vehicle applicability; no shared source/map/metadata writes.
- Public Ford catalog retrieved from its actual independent DTNA index link. Earlier Squarebirds403 and OneDrive safety rejection were not bypassed.

## Evidence ledger

| Claim | Result | Evidence and limits |
|---|---|---|
| Hardware identity | 378644-S, locator NN-61-B, Type1 | Ford FPS3733 hardware catalog, PDF216 / printed205, H143; actual pixels inspected |
| Nominal diameter | 1/2 in = 12.7 mm | Verified table heading and row; no fit tolerance |
| Nominal length | 13/32 in = 10.31875 mm | Verified table heading and row; conversion is not precision claim |
| Form | Generic unstepped Type1 icon | Not a section or part-specific solid/hollow determination |
| Annular topology | Separate Army figure identifies same part | Root evidence retained; this catalog adds nominal exterior envelope, not bore |
| Split form | Unresolved | Blocked engine-catalog snippet not accepted as verified |
| 1994 truck applicability | Unresolved | General hardware catalog has no vehicle-specific application row |

## Delivery

Research ready for preservation, not installed acceptance. Four authored files; no original PDF, scan or screenshot distributed. Public source URL, full PDF hash/size, render hash, page, reproduction commands and root prerequisite hashes are in the evidence JSON. Retrieval used public curl, Poppler text/render and existing `.venv-cad` ingestion. No CAD package needed. No temporary path is a restore prerequisite: reacquire the URL, verify hash, render page216. Source-host disappearance remains an external reproduction limit.

The local visual-review convenience is `/tmp/oilpump-dowel-20261002-page216.png`; it is deliberately excluded. OCR suffix8 was corrected to S using the actual image. The page footer has February1996 and copyright1998; record both rather than silently normalizing the scan date.

## Validation and review

| Gate | Status | Scope |
|---|---|---|
| Hardware identity/dimensions | PASS | Actual table row and column headings visually checked |
| Application/coverage | NOT VERIFIED | Same number bridges industrial hardware; exact1994 truck still open |
| Source/visual comparison | PASS | Actual PDF page216 inspected, not search snippet |
| Learning/diagnostics | PASS locally | Source→atomic note, prefixed links, no H1; root owns semantic backlinks |
| Reproduction | PASS locally | Public PDF retrieved, hash recorded, page ingestion and render complete |
| CAD/export/interfaces/motion/browser | N/A | Research-only delivery, no model mutation |

Useful next action: incorporate nominal external envelope into the existing same-part topology contract, retaining unknown internal bore/split and application. Do not build a guessed hydraulic sleeve or install it against the old illustrative pump feet. A part-specific section/drawing or identified end view is still needed for internal geometry. No further search loop is running.

## Tracking and restart

Issue remains open for pump interface/application evidence. Root reviews the source page and merges evidence as appropriate; no worker commit or publication. KB pages frozen for root semantic processing. Usage/effort billing unavailable. No active process.
