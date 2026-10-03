# Piston compression-height evidence reconciliation

## Contract

Assigned engine #1 core evidence follow-up from integration owner root. Research only; worker owns `core-piston-reconciliation-20261003*` files in docs, reference and scripts. Requested baseline `5c5a11d`; observed start `0d318ea9a78bbc2b23041193c3090e7fd54343fd`, branch `engine/component-fit-followup-20261003`. Concurrent root commits may advance it. Initial first-assembly manifest SHA256 `4854f483564d736233759416e9aa877946429f54dfc57797d2d2bf3bc9b8455a`. No shared CAD, inventory, Git or KB changes.

Identity is UEM/Silv-O-Lite replacement piston 1186 or 1186H, explicitly catalogued for 1987–96 VIN Y EFI truck. Owner-installed piston identity remains unknown. Coordinate comparison uses existing crank axis Z=0, positive Z toward nominal deck Z=254 mm, and the existing idealized zero-offset slider crank. No transforms, part IDs or interfaces change. Parent owns shared integration and issue tracking.

## Recommendation and evidence ledger

**Retain 45.1104 mm (1.776 in) as the replacement-reference compression height.** Do not change it to 44.6278 mm merely to match Ford's broad family nominal table, and do not promote either value to measured owner geometry. The disagreement is an evidence-scope difference, not an arithmetic or inch-to-mm conversion error. No unsupported reason for the design difference is asserted.

| Claim | Evidence | Applicability and limits |
|---|---|---|
| 1186 and 1186H compression height 1.776 in | [UEM 2020 catalog](https://www.uempistons.com/themes/UEM/images/Silv-O-Lite%2012.20.20.pdf), PDF page 40 / printed 38, both rows | Explicit 1987–96 VIN Y EFI truck; covers 1994. Replacement comparison, not original installed identity. |
| 1186H remains an application reference | [UEM supplement](https://uempistons.com/sites/default/files/Supplement_Catalog.pdf), PDF page 13 / printed 11, row 1186H | L6, 4.9L, 1987–1996, Ford Inline 6-Cylinder, 4.000-in bore. Footer 12/1/23. No compression-height column. |
| Ford 1.757-in compression height | [Ford Basic Engine Dimensions](https://www.trackey.ford.com/download/pdfs/EngineDimensions.pdf), page 1, 300 I-6 / 1965–96 | Family nominal only; no exact 1994 piston identification or tolerances. |
| Current rod 157.7 mm versus Ford mean 157.734 mm | Inventory rod claim; Ford mean 6.210 in | Current rod remains provisional; industrial comparison is not exact truck identity. Difference is 0.034 mm. |
| Current stroke 101.092 mm equals Ford 3.980 in | Inventory and Ford table | No stroke correction follows from piston comparison. |

Complete source hashes, compact source extracts, dimensions and current input hashes are in `reference/engine/core-piston-reconciliation-20261003-report.json`. Local 2020 PDF hash matches inventory. Both UEM pages were rendered and their actual rows visually reviewed. Manufacturer source PDF/pixels are excluded from delivery. Relevant prior source pages are `kb/sources/silvolite-efi-ford-300-piston-dimensions-40-40.md` and `kb/sources/pump-deck-height-20261003-ford-nominal.md`; neither was edited.

## Consequences

At idealized zero-offset TDC, crown height is stroke/2 + rod center distance + piston compression height. Nominal below-deck distance is 254 mm minus that sum.

| Combination | Calculated crown below deck |
|---|---:|
| Current replacement piston + current 157.7-mm rod | 0.6436 mm |
| Replacement piston + Ford mean 157.734-mm rod | 0.6096 mm |
| Ford nominal piston + Ford mean rod | 1.0922 mm |
| Ford nominal piston + current rod | 1.1262 mm |

Changing only compression height to Ford's nominal would lower the crown by 0.4826 mm. Changing only the current rod to Ford's mean would raise it by 0.034 mm. Neither change is needed to reconcile the sources. In particular, do not change rod length or stroke to compensate for the piston-height difference.

Catalog specifies an offset pin but not its offset magnitude or direction; the current mechanism's zero offset is explicitly idealized. These calculations do not establish actual deck clearance, piston-to-head clearance, compression ratio, production tolerance, thermal behavior or hydraulic/mechanical acceptance. Dish depth alone does not establish dish volume. Adjacent 3171H (1996–97, 1.767-in height) and older rows are not substitutes for the explicit 1994 application row.

## Delivery and reproduction

Readiness: research complete, ready for independent integration-owner review. No installed change or CAD candidate. Submitted commit/PR: root-managed, worker makes none.

From repository root:

```sh
python3 scripts/engine/core-piston-reconciliation-20261003.py
```

Python 3.13.12 and matplotlib 3.10.9 on macOS produced the report and authored `reference/engine/core-piston-reconciliation-20261003-comparison.png`. The script checks the local 2020 PDF hash when present, validates expected input piston/stroke values, calculates four stacks and records seven input hashes. It requires no downloaded PDF or temporary file to reproduce the numeric output. Matplotlib used its automatic writable temporary cache because the home cache was unavailable; no result depends on that cache.

For independent source inspection, retrieve the public catalog URLs above, compare the report's hashes, render PDF pages 40 and 13 respectively with `pdftoppm -f <page> -singlefile -png <downloaded.pdf> <review-prefix>`, and inspect the listed rows. Raw PDFs are not repository deliverables. CAD entry point, STEP/GLB, asset release and geometry exports: N/A research-only.

## Validation and review

| Gate | Status | Method / limits |
|---|---|---|
| Application/coverage | PASS for replacement reference | Explicit 1987–96 VIN Y row; owner identity unknown. |
| Dimensions/coordinates | PASS for arithmetic | Input assertions, inch conversion and zero-offset sums; no guessed tolerance. |
| Source/visual comparison | PASS for cited rows | Actual two UEM rasters reviewed; authored comparison PNG also opened and checked. |
| Reproduction/review | PASS worker reproduction; independent review pending | Script completes; JSON contains source and input hashes. |
| Learning/diagnostics | PASS research explanation | Evidence classes and consequences separated in this handoff. |
| CAD/export, installed interfaces, motion/disassembly, browser integration | N/A | No geometry, motion, browser or installed artifacts changed. |

No existing assembly check is invalidated. This delivery supports retaining the replacement piston reference; it does not close the owner's piston-identity or pin-offset gaps. Model/effort and billing usage unavailable.

## Tracking and exact next actions

Root should independently review the primary 1186/1186H row and this arithmetic, then link this evidence from the nominal-core audit to explain why its 0.4826-mm discrepancy is not an automatic correction. Preserve `replacement-reference` status and the zero-offset mechanism limitation. If original 1994 geometry is later required, seek an exact original piston engineering drawing or specific OE dimensional source; do not infer it from the family table. Rod evidence can be strengthened separately with Ford's nominal mean, without claiming a production tolerance or automatically changing the CAD. No process remains running. Issue closure and shared audit edits are root-owned.
