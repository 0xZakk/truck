# FS10 axial datum and common-interface hypotheses

## Contract

Research continuation under #32/#34, baseline8c2d2d9a1400acf784e04581a61e6a6ede38d3ba / engine/timing-drive-fit. Root owns integration. Owned files: this handoff, `scripts/check-fs10-axial-mount-datums.py`, `inventory/engine/fs10-axial-mount-datums.json` and preserved initial failure. Frozen onset study is unchanged. No candidate or canonical geometry writes. Question: is the compressor reversed or axially misplaced, and which coherent interface revision is worth building?

Inputs: actual canonical FS10, shared carrier and canonical q0 poses; source `ac_compressor.py`, `accessory_carrier_1994.py`, Ford94-10-19 Fig4, two owner engine photos, UAC CO101220C row, existing timing registration ledgers. Millimeter world frame. Check physical material on both sides of four mounting seats; demonstrate a wrong axial pose loses those seats. Exact-case checks are static; no production dimensions are inferred from oblique images.

## Evidence and results

The actual front cylinder occupies X373.66..443.36, rear cylinder303.76..373.46, front head446.56..484.66, rear head278.56..300.56 and pulley461.56..485.56. Local compressor +Z was correctly rotated to world +X. The shaft nose, pulley and clutch are forward; the rear head is rearward. Thus neither an accidental front/rear inversion nor an untransformed local axial datum explains these conflicts.

Four ear seats at Y210/350, Z60/140 terminate at X432.56. Sixteen R8 annular samples at each ear lie in compressor material at X432.55 and carrier material at X432.57:64/64 on each side. This is positive local material support, not a whole-face or load-capacity proof. Moving the compressor +25 mm removes all64 material witnesses. Source model pulley center is X473.56; moving the entire compressor also displaces every groove plane. There is **no canonical belt occurrence**. The uninstalled common-profile belt study declares X473.56; its3.56mm rib pitch differs from the old compressor's4mm illustrative groove pitch. Existing accessory fit therefore already requires a coordinated profile/belt revision; it is not a validated reason to relocate a compressor axially.

The actual Ford Fig4 shows the compressor clutch forward and cylindrical body extending rearward, low on the shared carrier. It does not dimension the axial ear station or barrel-to-clutch distance. Its perspective cannot validate the modeled100mm center-to-pulley distance. The two owner photos confirm front belt/accessory arrangement but obscure the compressor rear and mounting interfaces; neither permits a calibrated axial barrel length or hidden ear coordinate. UAC's93mm tangent mount width remains undatumed. A rearward body at the current pulley plane is qualitatively supported; its exact length and center are not established.

## Coherent alternatives and screening

| Hypothesis | Preserved interfaces | Required coordinated changes | Current finding |
|---|---|---|---|
| Reverse whole compressor | None reliably | Clutch, rear ports, carrier, belt and internal direction | Rejected: contradicts actual/source clutch-forward topology |
| Rigid +25/+50mm axial branch shift | Internal compressor geometry only | Carrier ear seats plus every belt-driven accessory plane or a new compressor nose | Rejected as isolated repair: actual ear and groove errors equal shift; no source supports new common belt plane |
| Compact compressor axially while fixing pulley and ear seats | Existing external datum candidates | Both case halves, swash chamber, pistons, heads, shaft/nose and ports must be reconstructed coherently | Unproven; no source dimension fixes shorter package, and cannot trim internals to escape timing cover |
| Keep accessory axes; revise main right contour | Current compressor/carrier axial seats and belt center candidate; crank/cam axes | Common main gasket, block rail, cover wall and affected main screw axes | Recommended bounded feasibility study; source topology retained, numerical contour explicitly revised estimate |
| Keep registered main contour; revise accessory YZ layout | Current front seal/gear geometry | Compressor and PS/AC carrier webs/ears, belt routing/tensioner travel, hose endpoints | Viable alternative only as a complete accessory-layout candidate; +40mm cannot be chosen solely from collision clearance |

For the fourth option, the explicit analytic cam-pocket/barrel envelopes give a zero-margin station6-axis interval Y194.042825..211.627108 at Z74.423690, using existing estimated R84.947 cam-pocket,6mm wall, R8 support and R65 compressor barrel. This is only a feasibility illustration. It cannot pick a production hole coordinate, certify the whole source silhouette, or replace a full gasket corridor test. A proposed route must be generated from declared common planar curves and radial/axial clearance allowances, never from subtraction of compressor neighbors. Original five rail intersections as well as new station6 stock must disappear together. Root reports the newly staged main gasket also intersects FS10; it belongs to this same common-interface contract.

The next useful physical check is a bounded section sweep of that common contour corridor against the full cam gear envelope, crank seal region, front pan terminals and source hole ordering. Compare its shape to the manufacturer seven-hole open-bottom topology before selecting any new contour. If the corridor fails, move to the complete accessory-layout hypothesis rather than nibbling isolated clearances. All dimensional revisions remain estimates and require root selection. The adjacent water-pump repair retains all7axes and is spatially separate; coordinate any eventual main contour revision with that owner.

## Delivery and quality gates

Reproduce `.venv-cad/bin/python scripts/check-fs10-axial-mount-datums.py`. macOS, Python3.13/build123d0.10, existing environment; no install. No new STEP/GLB is needed for read-only datum checks. Input hashes and actual bounds in JSON. Initial nonexistent belt-ID lookup failure preserved separately; it was corrected by inspecting canonical occurrences, not by inventing an installed belt.

| Gate | Result / limit |
|---|---|
| Application/coverage | PARTIAL: replacement and Ford topology apply, installed compressor identity unknown |
| Dimensions/coordinates | PASS for actual model interpretation; factory dimensions remain unknown |
| CAD/export | N/A new geometry; actual imported STEP bounds/material checked |
| Source/visual comparison | PARTIAL: local images inspected; orientation supported, axial dimensions unverified |
| Installed interfaces | FAIL overall; four local ear material witnesses pass, timing conflicts retained |
| Motion/disassembly | NOT RUN |
| Learning/diagnostics | NOT RUN; no user-facing content changes |
| Browser integration | NOT RUN; no installed changes |
| Reproduction/review | Input-bound report; root review pending |

No current stage acceptance or factory-fidelity claim. Next action: root reviews the shared contour feasibility scope. No running process; no shared file mutation. Model/effort/usage unavailable.
