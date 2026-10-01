# Component contract and handoff: corrected assembly motion adapter

## Contract

Root integration owner, issue #32 under Engine #1; baseline PR104 `8c2d2d9a1400acf784e04581a61e6a6ede38d3ba`. Candidate runtime only, no installed acceptance. Owned `cad/engine/assembly_clockwise_candidate.py`, dedicated checker/report and this handoff. Preserve shared legacy helpers and their frozen evidence. Manifest must explicitly opt in via `motion_revision: clockwise-inclined-v1`; compatible physical assets remain a caller requirement.

Rod/piston groups retain event phases and declare separate physical rest phases. Crank rotates −q, cam +q/2 with helix/endplay correction, distributor −q/2 with crossed-drive endplay correction. Existing oil-pump ratios retain their signed relationship; independent throttle/compressor controls are not reversed. All valve occurrence metadata must use the same revision. Neutral rest poses come from the guarded linkage patch, not already-lifted q=0 frames.

Units: engine CAD millimeters, input event degrees and axial millimeters. Only declared axial range −0.1..0 mm. Transforms do not mutate shapes. The separate `occurrence_shape` API returns the actual compressed spring CAD for this revision. Source dimensions/estimates remain classified in corrected crank/cam, inclined-linkage and crossed-drive handoffs.

## Delivery and validation

`transforms(manifest,degrees=0,axial_mm=0,throttle_degrees=0,compressor_degrees=0,compressor_engaged=True)` produces world occurrence frames from a copied manifest. It rewrites motion instructions only in that private copy before calling existing hierarchy/control logic; original manifest untouched. Positive event time is preserved in all valve state calculations.

Reproduce from repo root: `XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-assembly-clockwise-candidate.py`. Uses existing CAD lock. 3,696 independent crank/cam/slider/linkage frame comparisons pass over six event angles and both axial endpoints, maximum residual5.685e-14. Legacy manifest, missing physical phase, mixed valve revision and unsupported axial travel are rejected. Exact bindings in `inventory/engine/assembly-clockwise-candidate-validation.json`.

Initial checker rejected a null motion field; corrected fixture handling. Initial adapter guarded all valve occurrence axes too broadly, rejecting internally rotated translating lifter parts; restriction now applies only to rotating rocker/pushrod roles. Lifter/valve internals preserve their orientations while translating. Neither change adjusts geometric acceptance tolerances.

| Gate | Status and scope |
|---|---|
| Application/coordinates | PASS numeric convention against independent candidate helpers; not factory certification |
| CAD/export/source visual | N/A for numeric module; assets covered by separate candidate deliveries |
| Motion | PASS above frame subset; staged distributor/pump branch matrices still need audit |
| Installed interfaces | NOT RUN; fixture uses declared axis/phase contract, not complete installed geometry |
| Springs | PASS runtime rest/peak CAD against frozen qualified springs; separate JS topology checks exist; full neighbor acceptance separate |
| Browser | NOT RUN; adapter not yet connected to viewer |
| Reproduction | PASS local, source hashes bound; root authored/reviewed |

Next: compose actual serialized core/front/valve patches, verify adapter against their world frames and branch phase law, then coordinate browser runtime/assets. The known inherited rod-bolt/block conflict and missing oil-pump fluid joint remain unresolved and are not waived by numeric results. Per-task usage/model effort unavailable. No background process from this checker remains running.

The explicit `occurrence_shape(occurrence,shape,degrees=0,axial_mm=0)` avoids routing new metadata into the legacy shape dispatcher. Its spring construction is unchanged; only the previously qualified maximum-lift guard extension is applied. Four actual runtime rest/peak CAD shapes compare with frozen qualified assets within0.01mm³ volume and1e-5mm bounds, and ground-end heights agree. Reproduce with `scripts/check-clockwise-spring-shapes.py` under CADPython; report `inventory/engine/clockwise-spring-shape-validation.json`. Shape construction is cached without changing inputs. Frame checks rerun after this adapter addition.
