# Component contract and handoff: timing valvetrain contract

## Contract

- Issue32; root integration owner. Baseline3079300, engine/timing-coupled-fit; canonical manifest91950c89dc12c17d1169ec77eed16efa71919c6832061346582ee02b81599ad6 unchanged.
- Scope: isolated phase/contact audit and coordinated estimated adapter proposal for all twelve source-sized valve linkages at the new cam axis. No production timing identification, canonical geometry, shared motion edits or installation.
- Own only new timing_valvetrain_* module/check/report and this handoff; ignored generated/timing-valvetrain-contract outputs.
- Millimeters, shaft X; migrate lifter axis fromYZ90,72 to95.1098209901611,76.08785679212888. Preserve valves/head guide axes, source-comparison valve/pushrod lengths, full rigid keyed cam group and revised helical phase compensation. Do not tune peak by scaling lift.
- Inputs: current manifest and actual cam/head/valve/rocker/lifter/pushrod STEP bytes; source-sized-v2 dispatcher/layout; frozen coupled-core and prior numerical feasibility. Sources remain replacement comparisons and inherited exact-year service dimensions with stated assumptions.
- Planned checks: verify twelve IDs/roles against actual dispatcher; numerical phase law and endpoint closure; inherited versus shifted contact witnesses on actual STEP surfaces; installed guide/stem datum checks; quantify omitted-migration and omitted-compensation faults. Propose minimal adapters before constructing any new geometry. Contact tolerance0.002 mm inherited from source-sized contact audit; numeric closure1e-8 mm; exact support material1e-5 mm3.

## Evidence ledger

- Replacement cam envelope uses assumed18 mm base circle, catalog0.247 in lobe lift and nominal0.395 in valve lift. Profile shape/intermediate timing is hypothetical; no owner/Ford calibration claim.
- Melling comparison valves4.749/4.750 in and pushrod10.14 in retained. Ball geometry/oil bore and resulting250.003354434 mm ball-center length are modeled assumptions.
- Actual source-sized-v2 uses spherical rocker pad/socket and zero-lash geometric closure; hydraulic preload and tappet crown/taper unknown.

## Delivery / tracking

Contract audit completed below. No geometry constructed. Root review will determine next bounded adapter scope. Browser/installation NOT RUN. Usage unavailable.

## Completed contract audit

Report `inventory/engine/timing-valvetrain-contract-validation.json` SHA-256 **51b5b3a67f60d7921a54619ee9ab5c5cd20260dc68a661a0fa0b3dd1b05e2aad**. New code is `cad/engine/timing_valvetrain_contract.py`; checker is `scripts/check-timing-valvetrain-contract.py`. Run from root with `XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-timing-valvetrain-contract.py`. macOS / Python3.13 / build123d0.10.0 / OCP7.8.1.1.post1. No geometry generation or installation. Input hashes are checked before and after execution; prior reports remain frozen.

The actual dispatcher selects `source-sized-v2`, with numeric equations from `valve_source_layout`, not the earlier shorter-pushrod `valve_layout_candidate.solve`. All twelve manifest valve axes and roles agree with that source-sized model. The new isolated baseline solver exactly reproduces it at721 crank samples per linkage. At rest and peak, all24 installed linkage poses retain actual STEP pad/valve, rocker/pushrod, pushrod/lifter-cup and rocker/fulcrum contact within **1.30e-11 mm** maximum measured gap. This establishes the supplied baseline contact contract, not full motion/collision or factory calibration.

### Phase and lift contract

The rigid keyed cam group retains `cam angle = -crank/2 + degrees(K*axial)`, with K=-tan(25degrees)/81.2. A stationary follower therefore sees the existing lobe law at **effective crank = crank - 2*degrees(K*axial)**. At axial=-0.1 mm, the argument shift is **-0.0658065536 degrees**. It is a consequence of the actual rotated cam, not a discretionary timing adjustment. Omitting it causes up to **0.0059386084 mm** lifter-height error on the sampled slopes, exceeding the inherited0.002 mm contact tolerance.

The supplied lobe envelope retains18 mm assumed base radius,0.247 in catalog maximum lift and existing hypothetical intermediate profile/events. No nominal lift multiplier or arbitrary phase offset is introduced. The frozen cam STEP, actual body STEP and shifted lifter branch pass **120 surface-witness checks**: all twelve stations, relative event offsets[-150,-96,0,96,150] crank degrees, axial0 and-0.1 mm. Maximum gap is **8.55e-10 mm**. The witness follows the cam's axial translation while remaining within the stationary follower footprint. A+0.1 mm normal displacement is rejected at each witness. Using an unshifted body leaves0.287857–3.816907 mm witness mismatch; this is a diagnostic mismatch, not an assertion of whole-body collision.

No separate gear rotation is allowed: camshaft, key, spacer and gear remain the frozen rigid group. Lifters translate vertically at fixed X/Y; they do not rotate with that group or follow its0.1 mm axial travel. Tappet crown, taper, wear and hydraulic preload remain unknown.

### Existing guide and rocker datums

All twelve valve axes remain worldY=-12 mm and baseZ261 mm. Actual head probes over worldZ280–300 mm have an empty radius4.36626 mm bore and complete surrounding annular support to radius4.9 mm. Actual valve stem sections lie inside radius4.3434 mm: **0.04572 mm diametral modeled clearance**. No guide/stem adaptation is proposed. This central20 mm probe does not certify full production bore straightness or all guide ends.

| Datum | Installed model | Proposed common-rocker hypothesis | Meaning |
|---|---:|---:|---|
| Lifter axisY | 90 | 95.109820990 | Same migrated cam ray; estimated spacing |
| Lifter body datumZ | 114.8 | 118.887856792 | Entire internal branch translates together |
| Flat-foot baseZ | 90 | 94.087856792 |18 mm assumed base circle preserved |
| Lower pushrod ballZ | 139.7 | 143.787856792 | Internal seat convention retained, not measured |
| Rocker pivotY | 51.071840250 | 54.008533957 | Derived from nominal intake peak and actual closure |
| Rocker socket localZ | -5.421245566 | -1.333388773 | Retains catalog pushrod length at rest |
| Pushrod ball centers | 250.003354434 | unchanged | Derived from replacement overall length and assumed ball/oil bore |

The intake pivotZ remains395.1246 mm within numerical precision. The exhaust rest solution changes pivotZ by0.000052960 mm and rest angle by0.000680736degrees; these are explicitly retained outcomes of its0.0254 mm longer valve, not quietly rounded to the intake placement.

Keeping the old pivot after moving the lower socket gives only **8.950611486 mm intake /8.950728822 mm exhaust peak**. The common-rocker proposal gives10.033 mm intake and **10.033134436 mm exhaust**. The exhaust0.000134436 mm nominal residual and maximum intermediate lift-curve changes0.0218101/0.0219481 mm remain unresolved comparisons, not waived factory tolerances. Moving the lower ball while retaining the old rocker top misses fixed pushrod length by at least4.03194 mm. Candidate numerical closure remains below1.14e-13 mm; pad slide remains below1 mm across the sampled cycle.

## Minimal coordinated adapter proposal — not built

1. Translate every lifter internal occurrence by the sameY/Z delta(+5.109820990,+4.087856792), preserve all local anatomy and X stations, and drive it using the compensated effective phase. The block worker confirms matching guide axes, radius11.124565 mm, fixed X stations and vertical cutters centeredZ154.087856792; their material/oil-feed clearance report remains a separate dependency.
2. Preserve valve, guide, seat, stem and spring-seat datums. Keep the sourced comparison valve and pushrod solids unchanged. Recompute only pushrod rigid placement from solved top/bottom centers.
3. Build one common estimated rocker using the existing source-sized generator in isolated copied function globals: proposed pivotY and socketZ above, same pad radius/shape, spherical fulcrum interface, ball radius and bore. This changes the estimated arm spans and socket end, not the lift law. Compare old/new solids and preserve source-labeled limits.
4. Move the twelve fulcrum, guide and rocker-bolt axes with their derived pivots. Adapt only their head pedestal support and bolt engagement neighborhood; keep valves/guides/seats and head attachment interfaces protected. Enlarge/reposition the head pushrod passage only to a checked swept-envelope requirement. Do not assume a global head translation or move the valve axes to hide a mismatch.
5. Apply the candidate state consistently to valve/retainer/keepers, pushrod, rocker, lifter stack and spring shape. Use actual solved exhaust lift rather than clipping it to10.033 mm. Retain the existing spring source envelope and wire geometry; no thickness scaling.

Required next acceptance: new rocker STEP/GLB validity and protected spherical interfaces; all12 actual contact witnesses across event centers/slopes and axial endpoints; positive fulcrum/guide/pedestal support and bolt engagement; spring seats/coil clearance, seals, valve guide/stem and valve seats; pushrod/head passages, valve cover and neighboring rocker/valve parts; actual migrated block/lifter/oil-feed interfaces; valve/piston clearance under coupled crank/cam phase. Add omitted-phase, unshifted-seat and unchanged-head-pedestal faults. Preserve source comparisons and dimensional uncertainty. Those checks are **NOT RUN** here; no automatic acceptance follows from numerical closure.

## Validation and review

| Gate | Result | Scope / limit |
|---|---|---|
| Application / coverage | PASS scoped contract | All twelve actual source-sized-v2 linkages; identity/calibration unknown |
| Dimensions / coordinates | PASS audit | Installed datums, compensated phase and proposed numeric closure |
| CAD/export | N/A new export | Actual existing STEP surface/guide checks; no new geometry |
| Source/visual fidelity | NOT RUN new adapter | No adapter solid yet; prior replacement comparisons remain historical |
| Interfaces | PASS stated probes |120 cam/lifter witnesses,24 baseline contact poses and12 central guide probes only |
| Motion | PASS numeric; broader geometry NOT RUN |721 phase samples ×12 ×2 axial endpoints; no continuous new linkage clearance claim |
| Learning | N/A research contract | No user lesson or repair specification changed |
| Browser / installation | NOT RUN | No shared/canonical edits |
| Reproduction | PASS worker checks | Module/checker/input hashes; root review pending |

Next action: integration owner review the minimal adapter contract before authorizing the new estimated rocker/head scope. Checker finished; no background execution. Model/effort and usage unavailable.
