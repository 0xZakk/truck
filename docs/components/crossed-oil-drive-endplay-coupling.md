# Component contract and handoff: crossed oil-drive endplay coupling

## Contract before checks

Issues #32/#34, contributor pan_access_resume, root integration owner. Baseline26d0fdc4e7cdd3de0c621309499d1535d8c5131e, branch engine/timing-drive-fit. Scope is a separate pose module and bounded actual-STEP check of frozen corrected pair, cam axial x∈[−0.1,0]mm. No gear geometry, shared transform or canonical writes. Coordinate full-cam composition with inclined_linkage_resume.

The cam rotates theta_c=q/2+K*x where K=−tan25°/81.2rad/mm from the estimated front timing helix. Corrected crossed-drive lead is k=+1/18rad/mm. At fixed world axial coordinate s, translating the cam by x changes its tooth phase to theta_c+k*(s−x). Thus its effective gear registration is theta_c−k*x. The fixed distributor's nominal phase must satisfy theta_d+theta_c−k*x=0, giving **theta_d=−q/2+(k−K)*x**. This is a nominal tooth registration relation; finite backlash admits a bounded phase range rather than unique contact at every phase. Neither parameter is a factory measurement.

Verify actual STEP separation/overlap at axial endpoints and midpoint for event q=0,11.25,22.5° (cam approximately0,5.625,11.25°), including previously aliased rest/interstitial samples. Existing frozen zero-endplay17-pose evidence remains valid. Include omission of endplay correction and ±1° excessive phase error at rear stop. The omission may remain separated inside existing backlash: report it honestly as nominal registration failure, not automatically geometric collision. Independent actual STEP helix fits will verify the phase change sign/magnitude. No continuous solid sweep or production backlash assertion.

Owned new files: cad/engine/crossed_oil_drive_endplay_candidate.py, scripts/check-crossed-oil-drive-endplay.py, inventory/engine/crossed-oil-drive-endplay-review.json, generated/crossed-oil-drive-endplay/. Dependencies are frozen corrected-pair STEP hashes and previous direction/lead/backlash reports. Units mm/degrees with explicit world frames; original IDs/parents untouched. Tolerances remain exact positive distance1e−7mm for deciding intersection, strict cad_metrics volume, lead fit1e−6rad/mm. No new physical threshold.


## Delivery and integration contract

Readiness is candidate only. API `crossed_oil_drive_endplay_candidate.angles(q,x)` returns `(cam_degrees, distributor_degrees)`; `frames(q,x)` returns gear-centered local-STEP-to-world frames. Finite inputs and the agreed axial domain are enforced. Phase law at x=−0.1mm: cam timing correction +0.032903276807°, crossed-drive axial compensation −0.318309886184°, total distributor correction −0.351213162990°. Keep q monotonic and the physical −q/2 distributor direction. Do not translate the distributor with cam endplay.

The same incremental distributor correction must propagate through the rigid distributor shaft/intermediate hex/pump inner shaft path. Under the existing 4:5 inner-to-outer pump speed model, the outer rotor receives 4/5 of that phase correction. This is a kinematic dependency, not a new pump-flow/contact verification. The original branch relocation to the corrected cam axis remains the separate fixed translation already documented in the frozen direction study.

All16-teeth/R18/12mm-face/lead and front timing25°/81.2mm parameters remain estimates; no new external factory specification is asserted. The axial travel −0.1..0mm is the agreed existing candidate envelope, not a measured factory endplay specification. No learning content or browser changes.

Environment and command: macOS, `.venv-cad` Python3.13/build123d0.10, numpy. Run `.venv-cad/bin/python scripts/check-crossed-oil-drive-endplay.py` from the repository root. Source geometry and exported pair remain frozen. Checker binds exact STEP hashes and writes separate `inventory/engine/crossed-oil-drive-endplay-review.json`; overlap witnesses and recoverable partial rows are in `cad/engine/generated/crossed-oil-drive-endplay/`. Console is `cad/engine/generated/crossed-oil-drive-endplay-console.txt`. No temporary or personal input files; artifact publication remains root-owned. Model/effort/usage unavailable.

## Results and quality gates

All nine nominal actual-STEP samples have zero overlap and0.168892510989..0.170194060642mm separation. At the rear stop and event11.25°, −1° and+1° distributor errors produce0.103388442369 and0.153957333105mm³ overlap, respectively. Exact intersection STEP witnesses are retained. The omitted endplay correction produces a0.351213162990° registration error but still clears by0.097353191965mm. Thus omission biases nominal backlash without proving a jam; it must not be reported as an interference failure.

Independent actual cam-edge fitting samples17 points on each of304 exported helical edges. Translating them by−0.1mm increases their fitted world-axial phase intercept by0.005555555101055..0.005555555101064rad (expected0.1/18rad); the distributor correction cancels this plus cam timing-phase rotation. Domain/NaN controls reject invalid inputs. `crossed-oil-drive-endplay-summary.json` validates every report input hash and the numerical conditions without another CAD run.

| Gate | Status | Evidence/limits |
|---|---|---|
| Application/coverage | NOT RUN factory identity | estimated pair and existing candidate endplay envelope only |
| Dimensions/coordinates | PASS scoped | analytic phase law plus304 actual STEP edge fits; no source dimensions changed |
| CAD/export | PASS reuse | frozen pair valid-solid/watertight evidence remains hash-bound; new overlap witnesses are diagnostic intersections |
| Source/visual comparison | NOT RUN new factory comparison | no new geometry; frozen pair render remains relevant, no new source image available |
| Installed interfaces | PASS local pair only | nine actual STEP separations; fullcam/drive stack remains integration-owned |
| Motion/disassembly | PASS sampled endplay poses; full assembly NOT RUN |9 samples and3 wrong-phase controls; no continuous collision proof or disassembly study |
| Learning/diagnostics | NOT RUN | no lesson created or changed |
| Browser integration | NOT RUN | no shared viewer/canonical updates |
| Reproduction/review | PASS local bound run; root review pending | script/module/STEP input hashes; strict volume controls; no external temporary dependency |

## Tracking and restart

No canonical manifest/occurrence/parent or frozen pair asset changed. Root owns shared JS integration; inclined_linkage_resume receives the module contract for its separately composed fullcam. Next action: root reviews this phase law and combines exact frozen asset hashes with fullcam/drive-stack motion. Distributor/intermediate/pump inner correction propagation and outer4/5 transfer require combined checks before acceptance. Issues remain open; no installed claim. No running process. Console and all partial rows preserved. Candidate code can merge for preservation separately from installation.
