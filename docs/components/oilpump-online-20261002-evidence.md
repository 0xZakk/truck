# Component handoff: identified oil-pump exploded-view evidence

## Contract

Issue73 under Engine1; root contributor/integration owner. Baseline917af4ffa75f07aa0511c163068e36056efb1e3d, branch engine/source-driven-refinement-20261002. Research and cross-source topology reconciliation only. Own this handoff, reference/engine/oilpump-online-20261002-evidence.json and prefixed KB source/notes. No pump, drive, block or shared manifest changes. Existing raised-neck/side-inlet distinction and protected drive axis remain intact.

## New source and interpretation

Army TM10-3930-633-24P (May1993), PDF36 Fig13 and PDF37 printed13-1, explicitly identifies C5AZ-6600-A. This is a Clark/MHE-228 industrial application, not the owner's1994 truck. Actual exploded figure and its table were rendered and visually reviewed. The table distinguishes two pump mounting bolts/lockwashers, four cover screws/lockwashers and two inlet screws/lockwashers; it identifies C5AZ6626B as the inlet gasket and378644S as the pump-body pin. The figure depicts that pin as an annular piece, separate from the long intermediate shaft and its retainer. This is now a source-supported shape comparison, not a measured bore or proof of a hydraulic path.

Comparing the Army figure with the prior RONYU/LIZHONG identified replacement row supports this bounded face-assignment hypothesis: the three-aperture gasket belongs to the two-fastener inlet interface, with one larger fluid opening; the four-aperture template belongs to the raised mount, with two attachment openings and two distinct interior openings. The sources do not register these patterns in a common measured frame. Which interior opening corresponds to the shaft versus the pin/pressure-side feature remains unresolved, as do handedness, thickness and absolute coordinates. Do not construct a blocked or connected oil gallery from this hypothesis alone.

The Army listing's MS90728-61, MS90725-5 and MS90725-31 references create exact fastener research targets. Secondary dimension listings were not adopted. An attempted DLA MS90725 PDF fetch failed (connection reset); no standard dimensional acceptance is claimed. The strainer and gasket revision differ from the1994 truck listing and may not be transferred. OCR reads several part-number characters ambiguously (e.g. cover58A versus B8A); retain printed string and comparison separately.

## Reproduction and evidence

Public PDF URL and SHA256 are in the evidence JSON. Originals and derived source renders are excluded from Git. Commands: download to the capture path in the ledger, then `pdftoppm -f 36 -l 37 -scale-to 1800 -png SOURCE OUTPUT_PREFIX` and `pdftotext -layout SOURCE OUTPUT.txt`. Existing system Poppler used; no packages installed. Because the normal PDF ingester dependency was unavailable, selected Poppler pages passed through `tools/ingest.py --type local`; the KB source accurately retains PDF origin. No original-image redistribution is required.

## Validation and next work

Application PASS for the explicitly identified industrial C5AZ assembly, not exact truck variant. Source/visual PASS actual figure/table and prior gasket-detail comparison. Dimensions NOT VERIFIED; CAD/export N/A research only; installed interfaces, flow, motion and browser NOT RUN. KB structural review/semantic index performed by root with the batch. No count or installed-acceptance change. Model/token accounting unavailable.

Next: obtain an identified pump mounting-face photograph or dimensioned drawing that registers the two interior apertures, pin and drive shaft; retain independent pickup and block flange templates. An annular pin illustration must not silently become a proven pressure conduit. The evidence changes the next search from an unspecified pump underside to these named hardware and interface targets. No source access depends on personal credentials.
