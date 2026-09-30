# Isolated coordinated timing core

## Contract

Issue32 under engine1. Root authorized this isolated candidate after reviewing the numeric dependency study; root remains sole integration owner and the cover worker owns its registration work. Baseline commit124aa7c345af352459a800343ffc50f1e931367c, branch engine/exhaust-timing-joints. Owned module/checker/render script: `timing_core_migration_candidate.py`, `check-timing-core-migration-candidate.py`, `render-timing-core-migration-candidate.py`; owned report `inventory/engine/timing-core-migration-candidate-validation.json` and generated directory of the same name. No canonical/shared writes.

Scope: retain stable occurrence/definition IDs and existing axial stations for camshaft, four bearings, rear plug, refined58/29 gear pair and front plate/spacer/key/two bolts/two washers. Translate cam-side parts by worldYZ(+5.109820990,+4.087856792), giving the estimated same-ray121.8-mm axis. Crank gear stays at its original axial position/crank center. Unchanged block, cover and crankshaft are explicit context witnesses, not candidate members. Crankshaft and cam local geometry otherwise remain unchanged; cam's integral distributor-drive gear moves with it but the distributor/pump branch is not yet adapted.

Evidence: tooth counts/diameters remain replacement comparisons and gear profile/helix/121.8-mm axis remain estimates. The4.804-inch forum lead is not selected. Retention comparison dimensions and unresolved radial fits retain their original source classifications; this task does not convert inherited parts into factory-verified geometry.

`source_parts(manifest)` imports bound STEP files and composes static parent/occurrence transforms. It returns world-frame candidate shapes, occurrence records and source paths. Exports deliberately use **world CAD coordinates per occurrence**, not drop-in local definition files. Repeated bearing/bolt/washer IDs are preserved separately. Root's concurrent rear-exhaust application is unrelated; full-manifest hash records the snapshot while actual timing inputs and transforms are checked independently.

## Interfaces and planned gates

Exact static comparisons: shaft to four bearings, bore/gear/spacer/plate/key, rear plug; gear to spacer/key/bolt heads; washer/plate/bolt stack; crankshaft to crank gear. Report positive gaps separately from contact and interference; no arbitrary overlap exemptions. Critical thresholds: inherited0.1-mm³ static audit convention for classification only, mesh bounds0.15 mm, STEP volume error0.001 mm³. Preserve contact gaps/endplay; these are not manufacturing acceptance tolerances. No factory fit/press-fit claim.

Each exported occurrence must be a valid single solid; STEP reload, final-mesh bounds, watertightness and duplicate/degenerate-face checks required. Actual mesh oblique/front/rear views are inspected. Refined gear report hashes bind unchanged pair geometry; prior sampled tooth proof does not validate translated shaft/context motion. Unmigrated block/cover overlaps are expected installation failures, measured separately, never hidden by moving or filling context.

## Shared block patch datums required

A future block proposal must rebuild the cam tunnel atY95.109820990/Z76.087856792, four bearing support interfaces atX-334,-110,110,360.5, rear plug boss/seat aroundX-373 and stationary front retention socket pattern aroundX373/new axis. Retain axial station uncertainty and sourced radial ranges. Start from a documented pre-cut or feature-level source so removal of the old tunnel does not require ad hoc filling across oil routes, lifter bores or casting walls. Do not translate the whole block, manufacture old-bore plugs, or perform an unbounded boolean patch to make this candidate pass.

Head/lifter/drive adaptation remains separate per `timing-axis-migration-plan.md`. Common rocker/pivot is the physical numerical hypothesis: exact rod closure passes, nominal exhaust peak and lift-curve differences remain unresolved. The rejected separate-pivot comparison is archived, not a physical proposal. Cover worker has received the same-ray axis and retained axial/gear envelopes; crank seal stays fixed.

## Reproduction

From repo root with the pinned CAD environment (build123d0.10.0, Python3.13); rendering uses system Python3 with NumPy/Matplotlib:

```sh
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-timing-core-migration-candidate.py
MPLCONFIGDIR=/tmp/truck-gear-mpl python3 scripts/render-timing-core-migration-candidate.py
```

Local input STEP files are required; restore canonical checkpoint and frozen gear studies using repository artifact policy. Source hashes and per-occurrence export hashes are recorded in the report. No purchased references or third-party source images are redistributed. `timing-core-migration-check.log` retains execution progress. Root review and browser acceptance remain pending; no installation or issue closure authorized by this document.

## Delivery and measured review

Main report `inventory/engine/timing-core-migration-candidate-validation.json` binds manifest snapshot `ab99fff2f63ad5dfc21fde8d12a32fc2a3d65832e6c8664baefd99d94403f7bf` after root's rear-only apply. Relevant18 core/context occurrences retained identities, parents, local positions/rotations, and all bound STEP/module hashes matched at handoff. The whole-manifest hash also still matched when checked; no unrelated refresh was run.

Fifteen occurrences export as valid single solids and watertight GLBs with no duplicate/degenerate triangles. Maximum bounds error0.012470 mm; maximum STEP roundtrip volume difference0.000019120 mm³. All nineteen named internal pairs have zero solid overlap. These are the listed interfaces, not an exhaustive motion proof. Cam nose/gear, cam key/shaft and key/gear gaps are0.025 mm; four journal/bearing gaps0.0254 mm; retained rear plug/shaft gap8.7878 mm; bolt head/gear clearance0.8 mm. Crank gear/bore gap0.025 mm; a matching crankshaft key/slot remains absent and is not credited as complete.

The initial whole-shaft/detailed-gear distance query was stopped for excessive computation; `stopped-global-distance.log` is retained. Distances now use the neighboring axial slab and cam-gear inner50-mm radius; those are explicitly **local interface distances**, not global minima. The slab contains the neighbor's possible intersection region; the inner gear region contains all checked counterpart radial envelopes (shaft, plate, key, spacer, bolt heads). The first slab was too narrow to include the rear shaft across its real positive gap; that failed attempt is retained as `failed-empty-rear-slab.log`, then widened for the rear-plug witness without changing geometry or tolerances.

Supplement `scripts/check-timing-core-contact-witnesses.py` produces `inventory/engine/timing-core-contact-witnesses.json`, binding its input STEP hashes before/after. Planar axial witnesses:

| Faces | Contact area mm² |
|---|---:|
| Shaft shoulder / spacer |348.361392|
| Shaft shoulder / thrust plate |724.430182|
| Gear / spacer |340.456505|
| Each washer / plate |116.332026|
| Each bolt / washer |81.004899|

**Inherited thrust-control gap remains unresolved.** There is no current gear/plate contact. Local closest distance is1.490858 mm, but that diagonal/radial distance is not endplay. Projecting opposing axial faces gives an8.1-mm gap over1538.254409 mm²: `machine_gear_back` removes the annular gear material that would oppose the plate at the nominal0.1-mm spacer-minus-plate thickness. Do not label0.1 mm as demonstrated axial retention, or8.1 mm as complete effective endplay without checking all potential stops. This inherited relief must be reconciled with a source-supported thrust-face and bolt-head-clearance design before installation. No ad hoc fill or repair was introduced.

The shifted-bearing negative control moves bearing2 laterally1 mm: correct overlap0, bad overlap1083.227500 mm³. It detects lost coaxial support, while the numerical study separately detects omitted bearing/drive migration and wrong rod closure.

Unmigrated-context failures are measured: moved camshaft versus block18,775.065723 mm³, larger cam gear versus current cover520.175534 mm³. They keep installation blocked; no collision waiver or block-patch workaround was applied.

`cad/engine/generated/timing-core-migration-candidate/timing-core-render.png` was directly inspected from actual exported GLBs. It shows the entire core, front gears and a labeled retention-only detail with gears/shaft hidden. It is a mechanism-context render; the prior refined gear source comparison remains separate. Root review pending.

| Gate | Result | Scope/limit |
|---|---|---|
| Application/coverage | PARTIAL | Estimated migration, replacement gears; missing crank key interface |
| Dimensions/coordinates | PASS model-frame preservation | Same-ray axis and production axial positions unverified |
| CAD/export | PASS | Fifteen individual world-frame exports |
| Visual | PASS worker actual-mesh inspection; root pending | No new factory identity claim |
| Internal interfaces | PASS listed overlap/clearance/contact measurements; thrust-control FAIL/UNRESOLVED | Opposing plate/gear face not at nominal endplay |
| Installed interfaces | FAIL expected | Block and cover remain unmigrated |
| Motion/disassembly | NOT RUN for migrated core | Original gear-only sampled proof does not cover full shaft/context |
| Learning/diagnostics | N/A developer candidate | Not a production service specification |
| Browser | NOT RUN | Uninstalled study; prior security restriction remains |
| Reproduction/review | PASS local checks; root pending | Existing artifact restoration requirements apply |

Additional command:

```sh
XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-timing-core-contact-witnesses.py
```

No processes remain running at handoff; syntax checks passed. Next action: root review of this concrete core and the inherited opposing-thrust-face gap, followed by a bounded retention design/source decision before block/valvetrain/drive geometry work. Scope stays candidate, issue32 open. Model/effort/usage unavailable.

## Proposed bounded thrust-land revision — not built

After reviewing the inherited gap, root requested a minimal rear hub/land proposal. Proposed addition to **cam gear only**: an annulus with estimated radii20.65–26 mm, local axialX-7..+1.02. The extra0.02 mm joins the existing relief floor; the new rear thrust face stays at existing gear backX378.259375,0.1 mm ahead of plate frontX378.159375. It does not change the15.9-mm gear bore, key region,19.05-mm spacer outside radius, plate location or tooth surfaces. Outer radius26 is below tooth root77.7 and leaves the outer bolt-head relief open. The identified replacement image supports hub/shoulder topology generally, **not these rear dimensions or a factory thrust-face identity**.

Proposed check contract: retain stationary plate/bolts/washers; move shaft+gear+spacer+key axially as one rotating unit through[-0.1,0] mm. Confirm exact positive-area gear-land/plate contact at-0.1 and shaft-shoulder/plate contact at0, zero unintended overlap at endpoints/interior, and deliberate-0.11/+0.11-mm poses producing stop penetration. Record these as travel outside the provisional interval, not source service tolerances. Use exact swept extrusion/contact witnesses where tractable rather than only scalar minimum distance. Reuse gear tooth proof only after exact material-change containment below root and unchanged relative gear pose. Full shaft/block installation stays excluded. Proposal sent to root; no rear-land geometry has been built at this checkpoint.
