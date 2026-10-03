# ACT host estimate — registration sensitivity delivery

## Contract and result

Issue82, root integration owner. Pre-CAD assumptions are frozen in `act-host-estimate-20261002-contract.md`. This revision exercises the authorized sensitivity-study fallback. **No numerical installed pose is justified by the current registration; no boss, port or sensor transform was fabricated.** Host and sensor CAD remain unchanged.

The actual exact-year736×328 illustration supplies a topological location, but its exploded placement line is not a drilling-axis drawing. Five explicit pixel landmarks were tested at all1,024 corners of an independent±4pixel picking bracket. The nominal angle between the boss→probe placement line and depicted sensor axis is13.366°, with corner cases1.612–25.100°. This bracket is an image-selection sensitivity, not a factory tolerance or a proof that the illustrator intended either direction as exact.

Under the declared consecutive-runner assumption, the boss projects1.034807 runner pitches beyond the visible terminal port, with a−0.269405 perpendicular projected offset. Corner ranges are0.857617–1.248033 and−0.465179–−0.081166 respectively. Multiplying by provisional113.792mm pitch gives illustrative117.753/−30.656 values, **not world coordinates**. A naive addition to current first-runnerX284.48 would putX402.233 beyond the host'sX367 limit, demonstrating why simply scaling the exploded drawing into the existing casting is not a defensible transform. It does not establish the real port outside the casting; perspective/cross-axis projection and nonmetric illustration are unresolved.

Even an assumed orthographic camera leaves depth and axis inclination unobserved. The reproducible abstract-camera example has five distinct unit axes from−60° to+60° out of the image plane, all with the identical normalized projected direction. The extreme pair differs120°. Likewise five arbitrary view-depth positions have identical pixel positions. These are examples of nonuniqueness, **not source-derived uncertainty bounds or proposed vehicle poses**. A10pixel image-plane shift is detected as a negative control.

## Actual host and preserved interfaces

The bound canonical lower manifold is valid, one solid, boundsX[−367,367],Y[−256,−135.5],Z[252.5,364]mm. Its source module has no ACT receiver. All existing material, flange/studs/injector sockets/rail supports are unchanged. The report binds canonical manifest plus actual privatev4 SHA9da33ca507e31cf6d906d4ee2c92b87a64ba01db7abea8f14b72f244631f9fe9; neither was used as a clearance objective. No active pump study substituted.

The source-backed topology still usefully scopes a future revision: dedicated boss at the front terminal lower runner, sensing guard exposed to that runner, outward connector, independent female-thread/gauge contract. Selecting a local runner-wall normal, outward angle and penetration is an additional design assumption. It cannot be promoted as a result of this image registration. NPTF fit, installed engagement, connector roll, pressure sealing and hidden circuit remain unknown.

## Delivery and commands

- `scripts/act-host-estimate-20261002-registration.py`: source sensitivity, actual host read-only inspection, report.
- `scripts/act-host-estimate-20261002-render.py`: authored mathematical diagram, no original source pixels.
- `reference/engine/act-host-estimate-20261002-registration.json`: source/host/context hashes and numerical results.
- `cad/engine/generated/act-host-estimate-20261002-registration/`: actual script log and authored sensitivity PNG.

```sh
.venv-cad/bin/python scripts/act-host-estimate-20261002-registration.py
MPLCONFIGDIR=/tmp/act-host-estimate-20261002-mpl python3 scripts/act-host-estimate-20261002-render.py
```

The CAD virtual environment has build123d but no Matplotlib; source/CAD inspection and plotting are deliberately separate commands. Initial combined run's plotting import failure is recorded in the owned generated folder. No geometry was built or changed by that failure. Source original remains unredistributed; its exact local hash and public/context URL chain are in the previous bound host evidence. SystemPython/NumPy/Matplotlib and projectCAD environment used.

## Gate ledger and next action

| Gate | Status | Reason |
|---|---|---|
| Topological application/location | PASS qualified | Previously reviewed exact-year/service and public comparison |
| Pixel sensitivity / ambiguity controls | PASS |1,024 deterministic corners; actual numerical nullspace and visible-shift control |
| Metric world pose | NOT VERIFIED | No calibrated second3D datum or source port normal/depth |
| CAD export / source render of new host | NOT RUN | No new material candidate selected |
| Guard exposure / wall / named contacts | NOT RUN | Requires a numeric host interface |
| Wrench/removal and actual neighbors | NOT RUN | No arbitrary located sensor to test |
| Browser installation | NOT RUN | Research only |
| Reproducibility | PASS local | Hash-bound report, commands, owned logs and authored figure |

Root review may accept a separate explicitly estimated design axis/depth tied to current runner geometry; that would be a new contract rather than silently treating the source as metric. Alternatively a second identified near-orthogonal host view with matched flange/runner features can constrain the missing registration. No owner request, commit, canonical edit or hidden background task. Issue82 stays open. Usage unavailable.
