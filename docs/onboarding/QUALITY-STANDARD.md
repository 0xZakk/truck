# Shared component quality standard

Use this rubric for every contributor and agent. It applies to newly delivered components; it does not retroactively certify the existing engine. A strong visual model can still fail installation. A geometrically valid assembly can still be historically wrong.

## Classify evidence and readiness separately

For each important dimension or feature record one of: **verified application evidence** (exact applicable source/measurement), **replacement comparison** (identified substitute, with transfer limits), **inferred** (photo/proportion/engineering estimate), or **unknown**. Record source identifier, page/figure or photo, units, datum, uncertainty and applicability. A source dimension for another engine/year is not verified for this truck.

Readiness is a separate field: **research**, **candidate**, **integration-ready**, or **accepted installed**. Integration-ready means local gates passed and the interface contract is satisfied; accepted installed requires the integration owner's combined assembly and browser review. Evidence may still contain estimates, but material deviations and limits must be visible and explicitly accepted for the agreed educational scope. Never label estimated geometry factory-exact.

## Acceptance rubric

Every applicable row must have PASS, FAIL or NOT RUN plus report paths. N/A requires a specific reason, not a missing checker. Any critical FAIL/NOT RUN keeps the relevant component scope open. Do not average strong appearance against a failed mounting interface.

| Gate | Required evidence | Reject / keep open when |
|---|---|---|
| Application and coverage | Part identity, source applicability, physical component breakdown, known internals and omissions | Wrong generation/application, invented internals, an unexplained cartridge standing in for requested pieces |
| Dimensions and coordinates | Units, origin/axes, local-to-parent transform, critical dimensions with evidence classes | Scaling by eye, undocumented axis conversion, treating a catalog package size as part geometry |
| CAD/export integrity | Valid intended solids, no unintended disconnected bodies, STEP round trip, GLB bounds against CAD, stable IDs | Export succeeds but has lost holes, invalid topology, wrong units/material grouping |
| Visual fidelity | Actual CAD/GLB renders beside cited source images, matching useful viewpoints; annotate contour/interface differences | Only a generated concept image, no source comparison, hidden backside/attachment errors |
| Installed interfaces | Named neighbors, attachment axes, seats/contact area, fastener stack/engagement, passages/seals as applicable | Avoiding penetration by separating mating surfaces, unsupported retention, hidden collisions, blocked flow |
| Motion and disassembly | Defined travel/phase, relevant neighbor sweep, endpoints and worst-case samples, connected mechanisms; staged explode/reassemble | Static clearance claimed as dynamic, impossible removal, disconnected driven parts, arbitrary phase |
| Learning and diagnostics | Function, inputs/outputs, system relationship, symptoms and grounded checks, source links and limits | Generic filler, unsourced repair specifications, misleading calibration or diagnostic certainty |
| Browser integration | Individual deep link, selection/isolation, assembled scale/pose, explosion/reset and relevant motion; error check | Orphaned parts, bad navigation, missing assets, broken camera/visibility or console errors |
| Reproduction and review | Baseline/commit, commands, environment, asset/input hashes, reports, reviewer verdict and remaining gaps | Depends on undocumented local files or stale reports; self-declared completion without integration review |

## Check design and tolerances

Choose and document tolerances before acceptance: units, why appropriate, tessellation allowance versus physical clearance, contact versus permitted interference, and sampling density. Reuse applicable existing checks/thresholds; explain any changed scope. The engine's historical 0.1 mm³ overlap threshold is a numerical audit convention, not a universal production tolerance or proof that a leak path is sealed.

For newly authored critical checks, demonstrate sensitivity to a relevant bad condition (for example a deliberately shifted mating face or blocked passage). A check that cannot detect the fault it claims to rule out does not establish acceptance. Record sampled versus continuous coverage honestly. Change to geometry, transform, neighbor, source, export settings or checker invalidates dependent results; retain valid unaffected checks by their hashes.

Use repeatable views for source comparison: full silhouette, attachment side, and an assembled context view, with close-ups where scale hides details. Inspect the actual exported mesh as well as CAD when mesh fidelity matters. Reviewers compare the same critical features, not subjective polish alone.

## Deliverable package

Use [the common handoff](../templates/COMPONENT-HANDOFF.md), stored as `docs/components/<component-id>.md` for new tasks (existing pilots retain their paths). Include parametric source, STEP/GLB locations, evidence ledger, learning content, reports and renders. Reuse the current assembly/export conventions; there is not yet one universal component plugin API. Record the exact integration call and dependency order instead of assuming every module's `build` signature is the same.

Large generated files follow [artifact restoration](../CAD-ARTIFACTS.md); record release URL and checksum. Source and reports use repository-relative paths. If a source cannot be shared, identify the access dependency without uploading restricted originals. The reviewer must have enough authorized evidence to reproduce the claimed checks.

## Review and comparable outcomes

A contributor's first small part is a calibration exercise with the designated integration owner. Agree on the evidence class and detail expected, inspect the deliverable against each gate, and record concrete changes needed. Use the same rubric across systems. A different contributor or fresh-context reviewer should check critical geometry/interfaces where available; at minimum the integration owner performs a separate recorded review of the submitted revision.

Candidate studies may be merged for preservation, clearly labeled and kept out of accepted installation. Keep the component issue open until its agreed scope is accepted; a separately scoped research-only issue can be closed for completed research. New scope or lower fidelity requires an explicit recorded decision by the system/integration lead, not a quiet redefinition of Done. No process guarantees identical outputs from different agents, but these gates make quality differences visible and actionable.
