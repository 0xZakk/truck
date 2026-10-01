# Component contract and handoff: engine-control electrical lessons

## Contract

Engine #32, root integration owner. Research baseline `6b1608257e8c2eaa12512ac0c256d882854f3996`; branch `engine/timing-drive-fit`. Own only engine-control-electrical-learning candidate/source/report files, this handoff and dedicated checker. No canonical manifest, existing lesson, viewer, geometry or frozen map edits. Source inputs: independently reviewed `reference/engine/engine-control-electrical-map.json` and `inventory/engine/engine-control-electrical-map-root-review.json`, plus exact canonical and privatev3 manifests bound by checker.

Scope: concise electrical learning on existing component IDs, with page-specific primary references and no guessed component cavities, routes or test thresholds. No CAD units/frames changed; physical interface and calibration acceptance remain outside scope. Main learning JSON follows existing ID-keyed summary/steps/troubleshooting/sources/limits schema. Additional electrical_contract fields retain map records for deterministic semantic checks; existing rendering need not display these fields.

## Delivery and evidence

- `inventory/engine/engine-control-electrical-learning-candidate.json`:11 lessons, one each for fuel-injector-1 through6, iac-valve-body, egr-vacuum-regulator, egr-position-sensor, throttle-sensor and engine-coolant-temperature-assembly.
- `inventory/engine/engine-control-electrical-learning-sources.json`:8 page-specific sources, exact EVTM hash, PDF/printed page pair and private local URL fragment.
- `scripts/check-engine-control-electrical-learning.py`: read-only input checking and isolated validation-report output.
- `inventory/engine/engine-control-electrical-learning-validation.json`: hashes, link checks, critical negative controls and scope limits.

**MAP, IAT and HO2S have no physical component target in the current inventory.** Their source-backed electrical relationships are included as explicit non-linked context in TPS/ECT lessons. No fictitious nodes are added. Their individual component lessons remain deferred until independently supported physical parts exist. This candidate covers11 existing physical interfaces from the14-interface source map.

The six injector lessons explain common361 supply and separate odd555/PCM58 and even556/PCM59 groups without claiming injection timing. IAC distinguishes supply from PCM control and mechanical air response. EVR and EVP are separate actuator and feedback interfaces. TPS/EVP/ECT explain359 sensor return; ECT context keeps89 oxygen ground and57 heater/chassis ground distinct. Each lesson leaves calibration, component terminal numbering and harness geometry unresolved. In particular, existing CAD terminal1/terminal2 labels do not establish connector cavity assignment.

Source conflicts remain visible:361 continuationK has inconsistentS122/S136 splice labeling; this cannot join supply to oxygen ground. PCM33 table's Input wording does not establish an EVR input waveform. Diagnostic paragraphs are explicitly circuit-based reasoning: shared paths can be relevant to correlated concerns, but do not prove a failed part or authorize a test threshold. No live test procedure, factory wiring route, sensor transfer curve or injection sequence is supplied.

Primary references are the purchased1994 EVTM pages74–78,81–82,298; printed23-1 through23-5,23-8,23-9,150-1. Source map and root review preserve independent visual verification. No page images or bulk source text are redistributed. Source URLs follow the existing local/manual page-link convention and require authorized local PDF access; public hosting of the manual is not proposed.

## Validation and integration limits

Run `python3 scripts/check-engine-control-electrical-learning.py` from repository root. It checks all11 target IDs and step links in both canonical and frozen privatev3, verifies exact electrical map records, independently asserts critical injector/ground relationships, and validates source-page/hash pairs. Five controls are rejected: wrong injector group, sensor return changed to chassis ground, oxygen-ground prose changed to sensor return, a phantom MAP link, and an incorrect injector-group sentence. These are semantic/link checks, not electrical simulation.

Application/content and reproduction gates PASS for this bounded candidate. Installed interfaces, live diagnostics and browser NOT RUN. Dimensions/CAD/export/motion N/A because no physical models change. Existing learning modules are untouched: root must review and merge selected content with existing mechanical lessons rather than silently replace their construction limitations. Sources must be registered when loading the candidate; no registration occurs here. Re-run the checker if either manifest, map, review, sources or lessons changes.

Root review pending; research candidate may be preserved without installed acceptance. Exact binding report identifies the reviewed revision. Next action: root reviews prose and integrates an explicit learning merge only if desired. Missing MAP/IAT/O2 models remain separate completion tasks. Python3 on macOS; usage unavailable. No running processes. #32 remains open.
