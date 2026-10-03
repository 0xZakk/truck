# Text-to-CAD first-run comparison

The plugin works after restart. Both approaches delivered the same accepted **isolated, estimated-section Melling MPS-59-A candidate**. This trial found no speed or total-token advantage for the plugin. It did provide integrated STEP viewing, a useful section snapshot and native STEP/GLB declarations. No installed engine component was accepted or replaced.

## Measured results

Fresh workers both used **gpt-6-astra, medium**, confirmed in their session metadata. Same frozen brief, dimensions, candidate acceptance gates and machine; concurrent execution. Start timestamps below come from session creation, correcting the approximate times in worker prompts/handoffs.

| Measure | Existing method | Text-to-CAD 0.7.10 |
|---|---:|---:|
| Start UTC | 18:21:38.032 | 18:21:51.437 |
| Worker submitted UTC | 18:27:19.161 | 18:31:15.893 |
| Dispatch to submission | 5m41s | 9m24s |
| Root acceptance UTC | 18:27:59.092 | 18:32:09.812 |
| Dispatch to reviewed candidate | **6m21s** | **10m18s** |
| Input tokens, including cached | 813,991 | 1,998,134 |
| Cached input subset | 748,288 | 1,944,448 |
| Uncached input | 65,703 | 53,686 |
| Output tokens, including reasoning | 7,026 | 10,639 |
| Total worker tokens | **821,017** | **2,008,773** |
| GLB triangles | 26,540 | 134,864 |
| GLB bytes | 531,848 | 3,257,900 |
| Mesh bounds error, mm | .005195773 | .0000008554 |

Plugin reviewed elapsed time was 1.62× baseline; total worker tokens 2.45×. Cached input is already included in input, and reasoning already included in output: never add either again. These are actual recorded token counters, not dollar costs or unique words. The plugin had fewer uncached tokens; raw totals alone do not establish a pricing comparison. Initial cache conditions differ, including a cached initial plugin prompt. Each total includes the worker's final handoff message, a few seconds after its submission timestamp.

Shared coordinator overhead through the measurement cutoff was **4,860,023 tokens**: 4,847,723 input, including 4,776,064 cached, plus 12,300 output. Both workers plus that overhead total **7,689,813 tokens**. This is substantial overhead from the long coordinator context, inspections, measurement tooling and progress reporting; it must not be omitted from an experiment budget or charged twice to the arms. Counter cutoff18:31:52.143UTC; capture18:32:10UTC. The final acceptance-record write, subsequent report/publication/PR administration and this response are outside the counter window. Earlier installation, restart, research and part selection are also excluded, not measured as zero. A fresh coordinator context would be worth testing separately.

## What was actually checked

Root reopened each saved STEP and GLB with the same independent checker: one valid positive solid, correct envelope, 640 analytic section/occupancy probes including estimated corner bands, missing-floor/blocked-opening negative controls, one watertight consistently wound mesh, converted bounds within .025mm, and mesh volume within .5% of STEP. Both PASS; STEP volumes agree at3350.599607mm³. These finite tests do not establish production fit. Root separately inspected baseline CAD/mesh opening and cutaway renders, plugin CAD opening/section/mesh snapshots and the loaded native CAD viewer screenshot. Worker manifests verified16 baseline entries and32 plugin entries. Both engine assembly manifest hashes remain unchanged.

The source supports replacement diameter and height, not original truck fit, wall thickness, corner radii or installed location. Inch/metric catalog discrepancy is retained in the brief. Factory contour comparison, installed interfaces, removal/explosion and engine-browser integration remain **NOT RUN**. Native CAD tab success is not engine-browser acceptance. Issue#24 remains open under Engine#1.

## First-run friction and confounds

- Baseline: one geometry build; one render correction to show clipped floor triangles correctly. No geometry repair.
- Plugin: three failed build attempts (cache permissions/local broker sockets), three snapshot failures (service/browser dependency), missing checker dependency and two checker repairs. All are in elapsed time and worker usage. Authorized local execution and isolated writable caches resolved them; no global configuration change or geometry redesign. The source remained unchanged.
- Root: first independent checker report serialization failed on a NumPy boolean; native-bool correction and unchanged-geometry rerun passed. This overhead belongs to the coordinator.
- Baseline kernel: build123d0.10.0/OCP7.8.1.1.post1; plugin: build123d0.11.1/OCP7.9.3.1.1. Same Python3.13.12/macOS15.6.1 arm64, different dependencies. This tests complete workflows, not a controlled kernel-only comparison.
- Plugin mesh settings generated 5.08× triangles and6.13× bytes. Both meet the same gates; denser tessellation does not prove more accurate factory geometry. Future browser export work should tune density against geometric deviation and silhouette requirements.
- One simple rotational cup cannot predict complex casting or full-truck performance. Concurrent runs share CPU, cache and I/O; no isolated repeated timing or steady-state speed claim is made.

Recommendation: retain the current modeling pipeline while using the plugin's CAD inspection and section tools where useful. Before switching wholesale, repeat on a more complex unstarted component with both environments prepared, equal artifact requirements and explicit mesh-fidelity/size targets. Keep dependency setup reported separately without erasing this first-run result. The plugin cannot supply missing Ford measurements automatically.

## Reproduction and evidence

- [Frozen brief](BRIEF.md), [baseline handoff](baseline/HANDOFF.md), [plugin handoff](plugin/HANDOFF.md).
- Root evidence: `reference/engine/text-to-cad-20261003/{measurement,usage,baseline-root-review,plugin-root-review,mesh-cost,package}.json`.
- `review.py` checks saved artifacts with `.venv-cad/bin/python`; pass STEP, GLB and report paths. `measure_usage.py` accepts a local Codex session directory and emits only this experiment's numeric counters. Raw conversation logs are not committed.
- Generated artifacts are preserved in the private release `studies-2026-10-03-cad-plugin-pilot`; verify `package.json` publication state and SHA256 before claiming availability. Download `truck-cad-plugin-pilot-20261003.tar.gz`, verify SHA256 `35d8af354768168159f36676d9ea94e8f3de09da9af01072d9c0d27837d326c9`, then extract from repository root. No source original/manual/owner photo is included. `package.py` reproduces the generated-only archive.

Root acceptance covers this experiment's isolated scope only. The broader engine goal remains unfinished; its stored goal state was paused when checked this turn. No background work is implied by this report.
