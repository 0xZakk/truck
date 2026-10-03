# Illustrative spring export successor

Root-owned issue47 work, baseline PR12315983ad869324745c304ca84ba5cafc42ecbd5d5. Contract and failed construction trials: `pump-spring-sweep-20261003-contract.md`. No shared assembly, original STEP or frozen pump candidate changed.

## Selected result

The analytic mesh reproduces the existing declared circular helix (pitch1.4mm, radius15.5mm, wire radius0.4mm) clipped at WORLDX406.93/411.43. Axis is WORLDX throughY−32/Z170. The original CAD STEP remains `cad/engine/generated/pump-functional-20261003/water-pump-seal-spring.step`, SHA256f5a387b4d3f2532235c33258e66d706f0dc53eda7fbb22354ce11d3fac7f9a99. The replacement export candidate is `cad/engine/generated/pump-spring-sweep-20261003/spring-analytic.glb`, mapping mmXYZ to meter(X,Z,−Y). It is not installed.

Instead of repairing a broken native triangle mesh, the script derives the circular normal/binormal tube and solves the two clipping-plane curves analytically. Ear clipping triangulates each explicitly generated planar end loop; no arbitrary hole is filled, no native vertex is sculpted, and no part dimension or gate is relaxed. Stable target occurrence remains `water-pump-seal-spring`.

Actual GLB is one connected, watertight, consistently wound positive-volume mesh.500 deterministic surface/trim samples have maximum distance0.005690mm to the original STEP boundary; bounds error0.0000569mm, under the unchanged0.025mm gate. A wrong0.6mm wire-radius point is0.200007mm from that boundary and rejected. This is finite CAD comparison, not a whole-surface STEP maximum proof.

Separately, an analytic derivative bound gives maximum side interpolation error0.010427mm and planar trim-boundary chord error0.006149mm against the intended analytic surface. A128×32 coarse-grid bound0.667298mm fails the same gate. This argument does not establish the original CAD's global approximation error or any production dimension. All coil dimensions and pump seal architecture remain illustrative.

The mesh volume156.859991mm³ is0.323% below adaptive CAD157.367943mm³, recorded as tessellation difference, not hidden with a default mass approximation. Adaptive integration qualifies the earlier erroneous17.8% deficit report: default CAD mass180.818697mm³ is inaccurate on the trimmed spline. The rejected three-component mesh remains about5.56% below adaptive volume and has independently failing local surface distances. It stays rejected.

## Reproduction

Restore original STEP from published PR122 functional pump release and its prerequisite chain. Existing `.venv-cad` supplies build123d/OCP/trimesh/NumPy; systemPython provides plotting. No environment upgrade.

1. `.venv-cad/bin/python scripts/pump-spring-sweep-20261003-analytic.py`
2. `.venv-cad/bin/python scripts/pump-spring-sweep-20261003-analytic-check.py`
3. `python3 scripts/pump-spring-sweep-20261003-bound.py`
4. `MPLCONFIGDIR=/tmp/truck-spring-mpl python3 scripts/pump-spring-sweep-20261003-render.py`

The temporary directory is a disposable font cache only. Actual exported three-view image was inspected: a continuous squat coil and trimmed axial ends are visible. Rendering uses depth-sorted actual triangles; raster aliasing is not an additional geometric feature. Intermediate native arrays and rejected spline trials reproduce from their own scripts and are not required to build the selected analytic export. Model/effort/usage unavailable.

## Gate scope and next action

Application: illustrative construction only. Units/declared parameters: PASS. Selected export topology/bounds/finite source-surface checks: PASS. Analytic interpolation bound: PASS stated scope. Source identity/factory internal dimensions: unknown. Actual render: reviewed. Installed assembly, motion, spring preload/contact, browser and production fidelity: NOT RUN or unresolved; no installed acceptance.

Original STEP interfaces remain unchanged; a future pump integration may bind this export after independent review. It must retain the existing five pump-neighbor clashes and all other acceptance gaps rather than letting a mesh-only correction imply complete pump acceptance. Native full-sweep, Frenet and segmented failures are preserved. No root process remains running.
