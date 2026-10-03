# Illustrative spring sweep reconstruction test

Issue47; root owns pump-spring-sweep-20261003 prefix only. Baseline merged PR12315983ad869324745c304ca84ba5cafc42ecbd5d5. No shared/installed geometry changes. Old failures remain under pump-spring-manifold-20261003.

Scope: reproduce the existing illustrative seal spring's declared centerline (pitch1.4mm, height5.6mm, radius15.5mm), circular wire radius0.4mm and local clipping planes15.5/20mm with an explicitly Frenet-oriented circular sweep. A circular section is rotationally symmetric about its tangent, so transport choice should not alter intended tube anatomy; actual BRep differences must be measured rather than assumed away. All dimensions remain illustrative, not factory evidence.

Frames: original local coil translated14.95 alongX after90degreeYrotation. Final WORLD translation391.43,-32,170 derived from440+98.43−147. Preserve clipped WORLDX406.93..411.43 and axis. GLB mapping remains meter(X,Z,−Y).

Before adoption: valid one solid, tube/centerline and envelope checks, roundtrip, watertight one-component consistent-winding export, unchanged0.025mm bounds gate, actual source-boundary sampling and volume comparison, actual render and unchanged functional/neighbor interfaces. Exclude geometry from canonical until review. Preserve failed tests. This bounded first command builds STEP and records metrics, not acceptance. No source download or owner photo required for this illustrative construction.

## Adaptive mass finding

The default CAD mass evaluator is inaccurate for this trimmed B-spline sweep: old default180.818697mm³ becomes157.367943mm³ with adaptive Gauss-Kronrod span integration; new default154.457043 becomes157.365987mm³. Requested relative error1e−8, reported estimates1.13e−7/4.13e−8 are retained rather than claimed as requested accuracy. Old/new adaptive volumes differ0.001956mm³. This qualifies the prior17.8% discrepancy: it was versus default mass, while the failed mesh is about5.56% below adaptive mass and still has3components/large local surface errors. It remains rejected. Do not use default mass as exact proof on this sweep.

## Frenet result and segmented representation

The full-length Frenet sweep remains valid but native tessellation still fails (41boundary/5nonmanifold edges after degenerate cleanup). No adoption. Next bounded representation uses16 contiguous quarter-turn helical sweeps with identical pitch/radius/wire and clipping planes, fused before export. This changes BRep face partition, not intended centerline or declared spring anatomy. Verify joins, adaptive volume and actual surface/export quality; do not accept merely because segmentation exports.

## Segmented result and next action

Sixteen fused quarter-turn sweeps produce one valid STEP, but native triangulation still fails after cleanup (66boundary/4nonmanifold edges). Completed job82976; no accepted export. Exact declared helix parameters remain suitable for a directly parameterized tube surface with clipping-plane cap loops. Next diagnostic should derive that surface analytically, triangulate its planar end loops without filling arbitrary native holes, and compare deterministic surface samples against the unchanged declared construction/STEP. No geometry or accuracy gate is relaxed.
