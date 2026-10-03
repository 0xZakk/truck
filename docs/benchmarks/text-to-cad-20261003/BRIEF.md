# Text-to-CAD paired candidate experiment

User-authorized comparison, 2026-10-03. Root integration owner; coordinated branch `engine/coordinated-host-candidates-20261003`, baseline `4ddb52af029062268e55d4585076a8700e7e8650`. Relevant issue is block/plugs/dowels #24 under Engine #1. Historical block closure coverage used #32, which is timing; this tracking correction does not change either arm's scope.

## Frozen scope and evidence

Create isolated replacement-envelope candidate `block-core-cup-mps59a`, not an installed truck component. No model of this ID has been started. Both arms receive identical dimensions and gates, fresh context, and run concurrently on the same machine. Do not read the other arm. Do not edit shared assembly/inventory/viewer or existing candidates. No commits by workers; root serializes integration.

Melling MPS-59-A shallow cup, catalog PDF page 8 / printed page 6, local `reference/engine/research-2026-09-23/melling-expansion-plug-guide.pdf`, URL https://melling.com/wp-content/uploads/2025/05/2026-plug-catalog.pdf . Root inspected the actual page. MPE-107R kit comparison identifies one block cup, not its location or installed fit. Catalog decimal OD 2.070 inches, minimum 2.065, maximum 2.075; height .343 inches. Listed metric 52.48 conflicts with 2.070×25.4=52.578 mm. Use inch nominal consistently for this experiment; retain conflict unresolved, do not claim corrected manufacturer data. Nominal trade size 2-1/16 inches is not free OD. Existing coverage: `docs/components/block-closures-coverage-handoff.md`. Exact MPS-59A search of step.parts returned zero results before dispatch.

Frozen candidate: OD 52.578 mm; height 8.7122 mm; uniform wall/floor 1.0 mm ESTIMATED; outer bottom edge radius 1.5 mm and inner floor/wall radius .5 mm ESTIMATED, flat lip, no branding/coating/microtexture. Functional datum: bottom z=0, opening +Z, axis x=y=0. No parent transform or host bore is known. These are source-bounded educational candidate assumptions, not factory section measurements. Material appearance plain steel; no claimed alloy. Include short function/limitations text; no invented installation torque or repair specifications.

## Equal finish line

Deliver parametric source, STEP mm, viewer-compatible GLB meters (X,Z,-Y), full logs, compact reports, saved actual CAD/mesh renders and component handoff under own arm directory. Use native plugin outputs in plugin arm; if axis/unit adaptation is necessary preserve native output and document conversion. Reuse existing exporter in baseline arm (find relevant helper without ingesting whole engine). Renders must reveal cup opening and floor/radii. No wall-clock limit; count failures and rework.

Checks against saved artifacts: valid one connected positive solid; OD/height/roundtrip bounds within .025 mm; mesh watertight/consistent winding/one component, converted bounds within .025 mm; finite probes at floor center and inner cavity plus radial wall region; controls must reject missing floor and blocked opening. Record tessellation, hashes and package versions. Dimensions supported only as replacement comparison; visual source contour remains unknown without a photograph. Installed interfaces, disassembly, browser engine integration remain NOT RUN. Candidate acceptance must not imply component Done.

Use repository quality rubric and `docs/templates/COMPONENT-HANDOFF.md`, with each gate explicit. Output locations: own `cad/engine/generated/text-to-cad-20261003/<arm>/` (generated); own `docs/benchmarks/text-to-cad-20261003/<arm>/` (source/scripts/logs/reports/handoff). Root will independently review and measure comparison. Root alone controls user-facing CAD tab after delivery.

## Arms and measurement

Baseline: existing `.venv-cad/bin/python`, build123d and existing export helpers. No cadgen. Plugin: installed text-to-cad 0.7.10 CAD skill and `/private/tmp/truck-cadgen-pilot-20261003/bin/python` (reproducible pinned setup required in handoff). Plugin must follow decorated model workflow and inspect saved result; root shows it in native plugin tab. Dependency versions may differ; record this confound.

Elapsed start is root dispatch, end root accepted isolated deliverable. Record worker submission separately. Plugin installation before restart and shared source research are excluded setup, not secretly charged to baseline. Fresh worker rollouts provide actual cumulative token counters; root overhead measured separately. Input includes cached input; reasoning is included in output. No billing estimate unless supported separately. This simple cup tests workflow overhead, not complex casting productivity. One pair is not a statistical benchmark.
