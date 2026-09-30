# Component contract and handoff: throttle stops integration

## Contract

- Issue #43 under engine #1; contributor stop integration worker, integration owner root engine lead. Branch `engine/runner-stops-and-evr`; candidate baseline commit `74ca5288bb543871b1cc550e191e3f54ed62a8f1`.
- Frozen candidate baseline is the preserved `cad/engine/generated/throttle-cable-integration-stage/full-assembly.json`, SHA256 `0656841ba587a3f05d193aa75fb711f320ddf732cc0343c68504836c9ea7537d` (733 definitions / 1,341 occurrences). Actual installation baseline is recorded by the stage after runner and EVR integration.
- Own `cad/engine/throttle_stop_integration.py`, `scripts/install-throttle-stops.py`, `inventory/engine/throttle-stop-learning.json`, this handoff and stop-only generated stage/records. Shared builder, manifest, viewer and canonical outputs belong exclusively to the root integration owner.
- Scope: install the independently reviewed illustrative idle boss/screw/pad and WOT lug, retaining the two existing definition IDs and adding one stationary screw. No factory calibration, locking/strength/torque, airflow or hidden production geometry claims.
- Units mm; existing throttle parent/moving local frames and all prior occurrence transforms/explosion vectors are unchanged. Screw is identity-local under `throttle-assembly`, explode `(-50,40,0)` mm. Shaft origin `(394,25,490)`, axis Y; neutral cable ball `(394,95,514)` remain inherited datums.
- Housing/lever, cable/socket/guide/compression spring, shaft return spring, key/pin, bracket/shield interfaces are protected by frozen candidate proof. No modifications to candidate source or accepted candidate exports.
- Inputs: candidate exports, baseline housing/lever STEP, historical manifest, candidate report and source ledger are locally available. Generated fixtures must be included in the private CAD release. Source comparison/manual originals are restricted and must not be redistributed.
- Gates: frozen 47-pose/843-pair proof; fresh all-occurrence broadphase plus new/changed/unbound-neighbor checks at all 47 transforms; STEP target equality <0.00001 mm³; exact new overlap threshold 0.00001 mm³; GLB/CAD bounds <0.15 mm; ordinary and independent partial refresh replay; displaced-frame/geometry rejection. No threshold relaxation.

## Evidence ledger

See `docs/components/throttle-stop-proposal.md` and `reference/engine/throttle-stop-review.json`. Exact-year prose supports external screw-to-lever-pad contact and WOT stop existence. Rounded boss, helix, screw axis/size, contact lands and WOT casting lug are inferred educational constructions. The inherited 0–90° travel is not a Ford calibration. Frozen contact areas are idle 3.694166 mm² and WOT 6.946350 mm².

## Delivery

Readiness: integration-ready for bounded illustrative scope; actual integration branch HEAD before work `796b621244d8e341fe2f3c4de7af99488af01548`; final isolated stage passed against installed runner/EVR baseline. No worker canonical writes, commits or PRs.

`throttle_stop_integration.install(define, add, definitions, occurrences, assemblies, shapes)` uses existing exporter callbacks with `prepared=True`. Merge `throttle_stop_integration.source()` into manifest sources, then overlay `inventory/engine/throttle-stop-learning.json` in learning loading. Root owns shared hooks. Call after existing throttle/cable/spring adapters. No additional mesh/bounds hook is required.

Durable baseline inputs: `cad/engine/generated/throttle-stop-baseline/{throttle-housing,throttle-lever-estimated}.step`; accepted target exports remain in `cad/engine/generated/throttle-stop-candidate/`. The adapter accepts independently either baseline or installed target for both replaced IDs; it installs the frozen checked shapes without adding their features twice. Candidate parametric source remains the reproduction source for those accepted fixtures.

From repository root, after root confirms the final canonical baseline and shared hook:

```sh
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/install-throttle-stops.py --stage
# Root integration owner only, after reviewing the stage report:
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/install-throttle-stops.py --apply
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/install-throttle-stops.py --check-installed
```

Stage is `cad/engine/generated/throttle-stop-integration-stage/`; canonical records are `inventory/engine/throttle-stop-{installation,installed-validation}.json`. Promotion uses the existing rollback transaction helper and installed postcheck; stage/source/context/artifact hashes must remain unchanged. CAD release URL/hash: pending integration owner's checkpoint. Environment macOS / Python 3.13.12 / build123d 0.10.0 / trimesh 4.7.4; model effort and usage unavailable.

## Validation and review

| Gate | Status | Evidence / limits |
|---|---|---|
| Application / coverage | PASS bounded illustrative scope | Exact topology versus estimated construction separated in ledger |
| Dimensions / coordinates | PASS candidate and stage | Protected regions zero difference in frozen report; world-frame inheritance checked at all 47 poses during stage |
| CAD / export | PASS candidate and stage | Three one-solid watertight exports; stage checks installed target equality and mesh bounds |
| Source / visual comparison | Root accepted rounded candidate | Endpoint render reviewed; restricted source composite excluded from release |
| Installed interfaces | PASS staged interfaces | Frozen 843-pair candidate proof retained; current changed/new/unbound overlapping neighbors pass141 additional exact pairs |
| Motion / disassembly | PASS sampled motion and replay; browser disassembly NOT RUN | 47 angles, finite sampling; explosion browser check NOT RUN |
| Learning / diagnostics | PASS content references and explicit limits | Educational force/calibration limits explicit |
| Browser integration | NOT RUN | Root reports browser automation security block; no alternative browser surface attempted |
| Reproduction / review | PASS scoped stage; release pending | Fixture hashes bound; release and integration review pending |

Historical limitation: original candidate proof bound exact-neighbor STEP files and motion source modules, but did not hash broadphase GLBs or assembly-math/volume-helper modules. The stage binds the preserved original manifest, actual checked shapes/modules and all current broadphase GLBs. It repeats all-occurrence broadphase at 47 transforms, inherits only unchanged exact STEP-bound or source-bound dynamic neighbors, and exact-checks changed/new/unbound overlapping neighbors. These current hashes cannot retrospectively certify unrecorded historical bytes. No full candidate sweep is silently rerun or claimed.

## Tracking and restart

Issue #43 stays open. Direct GitHub issue read in this worker failed with API connectivity; issue scope is inherited from the repository handoff and integration lead, and no remote status is newly claimed. Root owns final installed/browser acceptance; candidate acceptance does not close the component. Next action: root reviews and runs the exact --apply command above, whose transaction runs installed postcheck, then performs remaining integration/browser acceptance when available. No background process is implied after worker returns. Usage unavailable.


## Final stage result

`cad/engine/generated/throttle-stop-integration-stage/validation.json` PASS, SHA256 `5fde91e792199da60fa108ca496456eee54e993baa72a5241cc8c4981548a9af`. Baseline manifest SHA256 `d748bcc9a38a592dc058bcf9c3a792a0dc59821a3bbd442cbcd73705a18569b9` (740 definitions / 1,348 occurrences). Staged manifest SHA256 `eeafadb96e186266dab83ec10b96c54fc73197d75dc615e2688f566cdffc2f69` (741 definitions / 1,349 occurrences).

Fresh all-occurrence broadphase across 47 angles identified runner and eleven EVR definitions as changed/new relative to the preserved733 baseline; 141 additional exact added-material neighbor pairs pass with zero collisions. The frozen843-pair candidate proof is retained. Unchanged exact-neighbor/source-bound dynamic work is inherited under the reported hashes and frames; historical unbound-helper limitations remain explicit.

All three staged STEP shapes have zero symmetric difference from accepted exports. All GLBs are watertight, without degenerate/duplicate faces; maximum bounds error0.001866mm. Final triangle counts: housing37,620; screw11,362; lever1,608. Ordinary replay, both-parts refresh and each individual partial refresh preserve exact metadata and accepted geometry. Shifted frame and shifted geometry are rejected. Transaction rollback controls pass injected first-write, second-write and postcheck failure. Learning links, coverage counts and current completion-plan omissions pass.

The first generic housing export exposed eight degenerate triangles. Root added housing to existing mesh cleanup and made triangle metadata count final faces. The failed log and original mesh are preserved as `cad/engine/generated/throttle-stop-integration-export-failure.log` and `cad/engine/generated/throttle-stop-integration-stage/housing-before-mesh-cleanup.glb`. A checker ShapeList-to-Compound conversion error was fixed without changing geometry/tolerances; its log is `cad/engine/generated/throttle-stop-integration-shapelist-failure.log`. Final log: `cad/engine/generated/throttle-stop-integration-stage.log`.

No canonical writes by this worker. Root promotion and installed/browser acceptance remain separate. No stop process is running at handoff. Keep installer, adapter, candidate, sources, learning, completion plan, shared builder, helper and stage files unchanged through promotion; all are bound by the installation record. This handoff is not itself a bound execution input.

## Integration-owner installation

Root applied the checked stage on September30 with `XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/install-throttle-stops.py --apply`. Transactional installed postcheck passed: three zero-difference STEP bindings, watertight exports, four replay cases, frame/geometry rejection, rollback controls and the fresh47-pose/141-pair context check. Canonical assembly now741definitions/1,349occurrences. Viewer learning is registered; navigation reaches1,349parts/1,548links. Browser acceptance remains NOT RUN because the browser tool rejected the localhost preview. This is an installed illustrative study, not accepted production geometry or a Done issue.

Report: `inventory/engine/throttle-stop-installed-validation.json`; log: `cad/engine/generated/throttle-stop-install-20260930.log`. EVR proof refresh and whole-engine checkpoint follow; their results are separate evidence.

## Integration-owner checkpoint

Root reports PR #94 merged as `124aa7c345af352459a800343ffc50f1e931367c`; the next focused branch is `engine/exhaust-timing-joints`. Canonical inventory is741 definitions /1,349 occurrences. This tracking addendum does not modify the frozen stage/check inputs or retroactively certify browser acceptance. Refer to the root-owned installed validation and current-state checkpoint for the final installed scope.
