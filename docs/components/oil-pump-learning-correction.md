# Oil-pump learning correction — candidate handoff

## Contract

Root-assigned engine#32 learning QC following frozen Ford pump topology/coverage evidence. Contributor pump_foot_resume; root owns integration. Scope: candidate text patch only for `inventory/engine/lubrication-learning.json`. No installed lesson, canonical manifest, viewer, source originals or geometry changed. Owned files have `oil-pump-learning-correction` prefix. Baseline commit, original lesson hash and six evidence-document hashes are bound in candidate/validation JSON. Units/transforms/CAD tolerances N/A for this prose task.

## Audit and correction

The installed pump lesson says its architecture follows the factory references. That is now too broad: the reviewed Ford comparison shows a raised drive neck and separate pickup flange, while visible geometry retains outboard feet and an inserted tube. Calling those merely dimensionally provisional hides a known architectural conflict. The lubrication overview and pickup steps also risk implying that displayed parts form a verified connected oil path.

The candidate changes six text fields across four existing lessons, plus three source lists:

- Lubrication overview explicitly identifies the visible old feet/tube and missing sealing/outlet interfaces. Collection step distinguishes pickup function from the unsupported modeled joint.
- Pump assembly limits and housing step identify the raised-neck/flange mismatch without claiming the industrial pickup route is truck geometry.
- Drive lesson distinguishes shaft/socket continuity from mounting or pressure-outlet correctness.
- Pan pickup step repeats the sealing limitation where the user selects the pickup.

The gerotor explanation,4/5 profile/speed ratio, provisional tooth-count/clearance warning,0.005-inch service endplay context, relief-calibration limitation and useful filter/pressure-switch content remain byte-for-byte unchanged. No new physical part or service procedure is invented. No definitive dowel lumen, outlet drilling, flange dimensions or gasket outline is claimed. The existing useful relief-to-inlet explanation already marks its full bypass passage missing and is retained.

Evidence: exact-year pump C5AZ6600A and pickup E3TZ6622F identities; new pump gasket required by service procedure; Ford industrial parts PDF8/18 and CSG649 PDF28/36 show the comparison neck/pickup flange. Industrial pickup C5TZ6622B differs from the truck. The existing `ford-industrial-parts` and `ford-industrial-csg649` source records explicitly label comparison applicability. Candidate reuses those stable IDs; hashes of both locally available PDFs match their canonical source records. No source original is included.

## Delivery and integration

- `inventory/engine/oil-pump-learning-correction-candidate.json`: nine guarded replacements with original values, proposed values and reasons. This is a patch proposal, not a learning module loaded by the viewer.
- `scripts/oil-pump-learning-correction-check.py`: applies the patch only in memory and checks exact original hash/values, stable part targets, source-ID resolution, unchanged unaffected lessons, retained rotor/service limits and source PDF hashes.
- `inventory/engine/oil-pump-learning-correction-validation.json`: hash-bound results.

Run `python3 scripts/oil-pump-learning-correction-check.py` from repository root. Python3 standard library, macOS; no CAD runtime. Checker writes only its dedicated report. Root can apply the nine guarded replacements to the installed lesson after review, then run navigation and browser review. Candidate does not patch automatically. Preserve all existing part/occurrence/source IDs. A changed original lesson hash requires rebase/review rather than blind overwrite.

## Validation and limits

Text audit/application: PASS for bounded evidence correction. Stable part targets and source links: PASS against current manifest registry; no claim of external URL availability. Primary local PDF hash matches: PASS. Profile/calibration/service limits retained: PASS. All unselected lessons unchanged: PASS. CAD/export and geometry comparison: N/A. Installed UI and browser rendering: NOT RUN; no canonical/viewer changes. Reviewer: root pending. Readiness: candidate text, not installed repair. No pump manufacturing or pressure performance claim follows from clearer prose.

Next action: root review/apply guarded text and perform its standard learning/navigation integration checks. Pump physical repair still requires measured mounting, gasket, discharge and pickup datums. No running processes. Model/effort/usage unavailable.
