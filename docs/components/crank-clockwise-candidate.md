# Clockwise crankshaft candidate

## Contract

Root integration owner, issue #32 motion dependency; branch `engine/timing-motion-integration`, baseline `dafb8175e4e7b328d2a16bdc47914307f044b0c8`. Own only `cad/engine/crank_clockwise_candidate.py`, its dedicated checker, this handoff and generated/report files. No shared builder, pose helper or canonical definition edits.

The source-supported clockwise motion correction needs throw rest phases `[0,120,240,240,120,0]`. Rebuild the existing crank construction with that phase list only; keep existing journal dimensions, cylinder stations, main journals and front/rear interface adapters. Preserve event phases and stable `crankshaft` identity. Do not reflect the whole solid or change flywheel/key geometry.

First reproduce the original formula with original phases and compare it against the actual canonical STEP. A mismatch blocks adopting the regenerated candidate until its cause is identified. Then check candidate validity, protected end material and main-journal regions, changed cylinder-journal centers, native exports and bounded actual rod closure through the separate corrected-pose helper. Source evidence and assumptions are inherited from the rotation convention ledger and existing crank definition: journal widths, counterweights, fillets and oil drillings remain provisional. This task fixes a physical phase inconsistency; it does not establish production crankshaft fidelity.

Command: `XDG_CACHE_HOME=/tmp/truck-cache .venv-cad/bin/python scripts/check-crank-clockwise-candidate.py`. No installed or browser acceptance. CAD environment unchanged. Usage unavailable.

## Delivery and review

The original generator replay exactly matches the canonical crank (zero missing or added material). The new generator changes only the four nonzero-phase throw bands. Front/rear end regions and seven main-journal regions have zero changed material. Exported STEP roundtrip difference is zero; direct GLB is watertight, consistently wound, 10,140 triangles, with 0.003255 mm maximum bounds error.

Actual exported crank-journal, rod-bearing and piston-pin cylindrical axes close over 721 poses for each of six cylinders: maximum error 8.30e-12 mm. Wrong rotation produces 101.092 mm separation and is detected. This establishes the local kinematic pairing, not full engine collision clearance. Broader block/pan sampled checks are separate in `scripts/check-crank-clockwise-neighbors.py`; inspect its report status before relying on it.

Root inspected the actual old/new shaded mesh comparison. The middle throw orientations change and the end interfaces remain visibly consistent. This is a before/after phase review, not a new factory contour comparison. No production counterweight/fillet/oil-drilling fidelity is claimed. Reports: `inventory/engine/crank-clockwise-candidate-validation.json` and `crank-clockwise-render-review.json`. Assets: `cad/engine/generated/crank-clockwise-candidate/`.

Render uses the existing split environments (CAD environment has trimesh; system environment has matplotlib):

```sh
.venv-cad/bin/python scripts/render-crank-clockwise-candidate.py --extract
MPLCONFIGDIR=/tmp/truck-gear-mpl python3 scripts/render-crank-clockwise-candidate.py
```

An initial checker assumed Boolean differences always returned a Shape and encountered a ShapeList. Normalizing its solids into a Compound fixed the checker; it did not change candidate geometry or thresholds. Renderer now uses explicit orthographic projection of actual exported triangles so the complete shaft stays visible. No new packages were installed.

Root verdict: usable candidate for coordinated corrected-motion integration, pending neighboring motion, matching cam, signed drive ratios and installed/browser checks. Source application is the recorded rotation inference; other crank geometry retains the original explicit estimates. No stable ID, canonical asset, manifest or viewer change was made.

Assembly manifest remains SHA-256 `91950c89dc12c17d1169ec77eed16efa71919c6832061346582ee02b81599ad6`. All 48 sampled block/pan comparisons now pass with zero overlap; a 100 mm upward-shift fault produces interference. Sampling is every 15 degrees over one revolution, not continuous clearance or an all-neighbor audit.

| Gate | Result and evidence | Remaining limit |
|---|---|---|
| Application/coverage | PASS scoped rotation correction, `engine-rotation-convention-review.json` | Exact truck crank identity/production contours unresolved |
| Dimensions/coordinates | PASS unchanged source parameters and measured exported axes | Other source estimates retained |
| CAD/export | PASS exact baseline/roundtrip, single solid, watertight mesh | No manufacturing claim |
| Source/visual | PASS bounded old/new actual render and qualified rotation sources | No new production casting comparison |
| Installed interfaces | PASS protected ends/main-journal regions and sampled candidate block/pan | Remaining installed neighbors NOT RUN |
| Motion/disassembly | PASS local axis closure and sampled block/pan | Full coupled engine motion/explosion NOT RUN |
| Learning/diagnostics | NOT RUN revised user-facing crank lesson | Existing lesson must explain physical direction and event time |
| Browser integration | NOT RUN | Coordinated manifest/viewer update required |
| Reproduction/review | PASS local commands, hashed reports and root render review | Asset release and integration checkpoint pending |

Exact next action: compose the corrected crank with the separately rephased cam and signed pose helper, check affected neighboring motion, and then stage shared viewer changes. Engine issue remains In progress; no Done claim. No root crank build or sweep process remains running.
