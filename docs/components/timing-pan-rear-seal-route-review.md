# Rear gasket contact corridor: bounded research handoff

## Contract

Issues #32/#34 under Engine #1. Root requested a separate read-only investigation after the expanded-seat v2 freeze. Delivery branch `engine/timing-pan-seal-joints`; candidate baseline remains `70542fad9de467a5c03ad54a6f54def8550956eb`. Pan worker owns only this review, checker, renderer, reports and `generated/timing-pan-rear-seal-review/`. No production geometry, station, crank-clearance or drain changes. World millimeters, unchanged transforms. Inputs are frozen expanded-seat v2 pan/gasket exports and source `oil_pan_joint_v9_candidate.py`, hash-bound in the report.

## Evidence and method

The declared source architecture uses a rear curved gasket band X−380..−365, radii51.1/53.1mm, transitioning into the flat ring at Z−32/−34. Pan support uses the outer gasket radius53.1 with4mm radial backing. All radii, widths and registration are explicit estimates; the replacement photograph supports continuous gasket topology rather than these dimensions.

The prior full-downward-face test found two unsupported surfaces at X−370..−365, Y±40.787..42.375, Z−34..−32, totaling25.5355846545mm². The same surfaces occur in frozen v2 and the expanded candidate. That failure remains unchanged.

This checker constructs an independent **4mm-wide contact corridor** at X−378..−374: the outer radius53.1 surface belowZ−34, joining horizontal lands at Y±sqrt(53.1²−34²)=±40.7873755 and continuing toY±60. Each full-width join shares the same boundary coordinates; the arch plus two flat strips is a continuous positive-width route. It is not selected by subtracting failed faces or repairing the pan. Exact surface subtraction against every actual pan face and every actual gasket face finds **zero missing area over525.7857998365mm²**. A separate6×3×6mm pan-removal fault centered(−376,0,−54) interrupts the whole corridor width and produces12.0015965388mm² missing support.

## Delivery and validation

- Entry/check: `.venv-cad/bin/python scripts/check-timing-pan-rear-seal-route.py`.
- Render: `python3 scripts/render-timing-pan-rear-seal-route.py`.
- Reports: `inventory/engine/timing-pan-rear-seal-route-review.json` and `timing-pan-rear-seal-render-review.json` bind source/input/output hashes.
- Actual candidate sections at X−376 and−367.5, serialized edge samples, exported `contact-route.step`, and `rear-contact-review.png` are in the dedicated generated folder.
- macOS, Python3.13/build123d0.10 plus existing system matplotlib; no new dependencies, assets unreleased, model/usage unavailable.
- Worker inspected the actual section image. Supported arch and flat joins are visible atX−376; inboard unsupported transition is visible atX−367.5. Root review pending.

| Quality gate | Result and scope |
|---|---|
| Application/coverage | Estimated source architecture; no factory fit claim |
| Dimensions/coordinates | PASS bounded, same declared arch datum and actual frozen exports |
| CAD/export | Research surfaces only; no new component solid or installation |
| Source/visual | PASS bounded, source architecture plus actual STEP sections |
| Installed interfaces | PASS local rear contact route only; original full-face FAIL retained |
| Motion/disassembly | N/A read-only rear surface review |
| Learning/diagnostics | NOT RUN user-facing lesson; engineering diagnostic supplied |
| Browser integration | NOT RUN, no installation |
| Reproduction/review | Commands and hashes retained; root review pending |

## Verdict and restart

The missing surfaces are **inboard overhang relative to a demonstrated continuous rear arch-to-flat contact corridor**. They do not interrupt that local route. No localized rear geometry repair is indicated by this bounded result. This does not establish pressure/compression, casting strength, complete perimeter contact, block-side gasket contact, or oil containment; those remain separate unresolved gates. No front file or original failure was changed.

Next: root review of the actual rear sections and retain this evidence beside the full-face failure. No process remains running. The combined front block/pan/gasket check is separately owned and remains unresolved until its report is accepted.
