# Spring tessellation precision diagnostic

Issue47, root integration owner. Baseline7f1723898920a8ae87093a3e5a60456fb4b714f8 merged; current checkout contains identical pump candidate files. Scope: new pump-spring-manifold-20261003 prefix only. Frozen pump-functional outputs remain untouched.

The unchanged illustrative spring STEP is valid but the export has nonmanifold edges. Prior pipeline merges CAD-mm vertices to five decimal places before GLB float32 conversion. Hypothesis: tiny trim triangles collapse during quantization. Test exact native triangulation and tighter vertex identity precision before changing mesher density or geometry. No hole filling, manual vertex movement, shape changes or acceptance threshold relaxation.

Use same absolute0.01mm/angular0.06 mesher. Preserve float64 native arrays, compare edge/degenerate counts before welding and across rounding precisions9/8/7/6/5. Diagnose float32 meter export separately. Existing measured bounds0.025mm gate remains. Require manifold/winding and actual STEP proximity/trim bounds before accepting any export; a watertight result alone is insufficient. CAD units WORLDmm; GLB meter(X,Z,-Y), stable spring occurrence. Budget one native mesh pass, up to5minutes; inspect live handle before stopping. All original anatomy/dimensions remain illustrative.

No canonical assets or shared code changed. Root records result and exact next step; production fidelity, five neighbor clashes and browser acceptance remain open.

## Precision result and next test

Five vertex precisions9..5 produced identical native defects:88 nonmanifold edges before removing degenerate/repeated faces, then15 boundary/6 nonmanifold edges. The native float64 mesh already contains the defect; GLB conversion and rounding are not its cause. Native run completed33.53s. Preserve this rejected hypothesis.

Next single bounded test explicitly selects the alternate Delabella triangulator at unchanged0.01mm absolute and0.06rad angular parameters, with surface-deflection control retained. No CAD or tolerance changes. Compare topology and measured bounds; any successful mesh still requires source-surface distance and component checks.

## Native flap diagnosis

Delabella completes35.72s, leaving exactly two triangular flaps: each has two boundary edges and one edge shared by three faces. This is an extra-face defect rather than an ordinary missing-face hole. Next diagnostic removes only that topology-defined extraneous face class, never fills a hole or changes vertices. Require one closed consistently wound positive-volume component, unchanged bounds, sampled STEP-boundary distance<=0.025mm at deterministic broad and affected-region points, plus comparison of volume/area against the unchanged STEP. Failed original retained. This finite distance test is not a whole-surface maximum proof or production accuracy claim.

## Rejected flap-removal result

The topology-defined removal produces a watertight, consistently wound GLB, but three disconnected components, mesh volume148.626466mm³ versus CAD180.818697mm³, and affected-region samples up to0.266110mm from the STEP boundary. Result FAIL, not adopted. The sampled set includes old removed-face centroids as diagnostics, but numerous retained adjacent faces also exceed0.025mm; component/volume failures independently reject it. No native candidate or canonical file changed. This demonstrates why topology alone cannot accept an export.

All root jobs completed: precision56494, alternate61410 and flap54251; no live root process. Next action is inspect the STEP sweep/trim surface and compare a separately constructed analytic helical wire against the illustrative spring parameters. Do not keep deleting triangles or tuning tolerances. Any successor remains an explicitly illustrative seal spring, not identified production geometry. Generated native arrays reproduce from the two diagnostic scripts using the unchanged STEP in published PR122 artifacts; they are intermediate cache, not required distributed inputs.
