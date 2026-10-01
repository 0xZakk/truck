# Engine exterior fidelity audit

Engine #32; root integration owner. Qualitative exterior review only, no shared CAD/runtime edits. Owned engine-exterior-fidelity-audit script, reports, this handoff and generated render folder. Exact manifest/mesh/source hashes are bound in the reports. Canonical1349 occurrences and privatev3 1361 occurrences were rendered separately at static event0 using their respective pose helpers; newer uninstalled water-pump/carrier trials were not substituted.

**The largest visible mismatch is missing exterior systems and context, followed by simplified contours—not something v3's internal timing corrections address.** Canonical andv3 have nearly the same top/front silhouette. That is consistent with the owner's concern despite detailed internal work.

Actual authorized driver/passenger engine-bay photographs were independently viewed, along with exact-year air-intake drawing190226466. Stored photo orientation was interpreted using radiator/firewall landmarks. Photos and source diagrams remain excluded from Git and outputs. The authored render shows the actual full meshes, including occlusion, in two orthographic views; camera angles are approximate source-view comparisons, not calibrated overlays. No pixel measurement becomes a dimension.

![Actual canonical and private v3 whole-engine meshes](../../cad/engine/generated/engine-exterior-fidelity-audit/whole-engine-review.png)

## Ranked differences and next steps

1. **Airbox and paired intake ducts are missing from both assembled scenes.** The owner's rectangular driver-side box and two ribbed ducts are visually dominant. Exact-year drawing190226466 confirms box, paired outlet tubes, clamps, bracket and body references. The isolated air-cleaner candidate is not an installed air system. Next: establish airbox/body anchors and duct endpoint frames, then finish connected ducts/bracket/clamps. Do not place the box by eye beside the engine.
2. **Large hoses and harness runs are missing.** The owner's radiator/heater hoses, loom and cables obscure and connect substantial parts of the engine. Existing short metal takeoffs/individual leads leave the render unnaturally bare. Next: source-supported engine-side connections and vehicle-side boundary frames, clips and hose diameters; obtain views only where existing photos hide depth. This is partly a scope gap, not proof castings are misplaced.
3. **Accessory carriers and belt context need attention.** The model's clean exposed cylindrical accessories and regular plate/brace supports contrast with the photographed cast support mass; no continuous belt spans the pulley grooves. Next: finish the matched carrier and belt system from applicable front/rear references. The pictures do not justify an exact compressor/alternator shift or a clearance-driven relocation.
4. **Intake/cover shapes remain visibly simplified.** Repeated runner sweeps, regular plenum walls and valve-cover shoulders look more geometric than the owner's partly obscured cast forms. This is a qualitative contour concern, not a verified width/height error. Next: identified specimen plan/side views with scales and bolt/port datums before changing those interfaces. The current22mm cover lean remains an inherited fit-study assumption, not a photo-derived correction.
5. **An isolated engine does not resemble a complete engine bay.** Fan shroud/radiator, battery, reservoirs, booster and firewall frame and hide the real engine. Their absence makes fan, accessories and lower block unusually prominent. Later body-context work should use actual vehicle reference frames. A cosmetic context shell would not establish physical fit.
6. **Teaching colors and pristine surfaces amplify differences.** The owner photos show subdued, weathered metal/rubber rather than high-contrast clean components. A separate appearance mode can help recognition after the major geometry/topology gaps; texture must not hide wrong geometry.

No quantitative misplaced-accessory finding is supported by these photographs alone. The audit deliberately avoids re-listing internal rod/gear/contact failures. V3's visible similarity does not invalidate its mechanical improvements; it shows those changes address a different requirement. Owner testimony of no known modifications does not establish every installed part's originality. The existing VECI-missing record stands; no repeated label search is requested.

## Delivery and reproduction

- `inventory/engine/engine-exterior-fidelity-audit.json`: source hashes, ranked observations, certainty and required evidence.
- `inventory/engine/engine-exterior-fidelity-audit-render.json`: all input mesh/manifest hashes, triangle counts, camera settings and output hash.
- `scripts/engine-exterior-fidelity-audit-render.py`: actualGLB depth-buffer rendering using existing raster helper and assembly poses.
- `cad/engine/generated/engine-exterior-fidelity-audit/whole-engine-review.png`: authored meshes only; source photographs viewed separately.

Run `MPLCONFIGDIR=/tmp/truck-mpl XDG_CACHE_HOME=/tmp/truck-cache python3 scripts/engine-exterior-fidelity-audit-render.py` from repository root. Script loads system NumPy2.4.4 before appending CAD-venv libraries, because local numba rejects CAD NumPy2.5; no dependency pins were changed. Uses existing local `.venv-cad/lib/python3.13/site-packages` for CAD/trimesh. Portable execution requires equivalent compatible dependencies; this is documented rather than claiming universal clean-clone rendering. About6.61million canonical and8.98million v3 actual triangles were rasterized; no simplification or source-photo tracing.

Actual output visually inspected. Source/mesh comparison PASS as a qualitative audit; calibrated exterior fidelity, new collision acceptance and browser NOT RUN. No geometry edits, concepts or source-photo copies. Root review pending. Next practical integration priority is airbox/duct and large-hose context with measured endpoints; source-limited contour work follows. No running process; usage unavailable.
