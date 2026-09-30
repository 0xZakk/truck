# Spark plugs and internal construction

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#54](https://github.com/0xZakk/truck/issues/54).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `91950c89dc12c17d1169ec77eed16efa71919c6832061346582ee02b81599ad6`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **Spark-plug threaded metal shell** — `spark-plug-shell`; modeled quantity **6**; provisional.
  - Instances: `spark-plug-1-shell`, `spark-plug-2-shell`, `spark-plug-3-shell`, `spark-plug-4-shell`, `spark-plug-5-shell`, `spark-plug-6-shell`
  - Source IDs: ngk-2019-spark-plugs, ngk-plug-construction, ngk-uk-2017-thread-families. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: NGK lists WR4-1/4652 for 1993–94 F-150 4.9L. This does not identify the installed plug brand.
  - Open: Sourced envelope: 18 mm thread diameter, 11.684 mm reach, 20.6375 mm hex and tapered seat; .044 inch application gap. 1.5 mm pitch is inferred from NGK 18 mm families; exact thread tolerances, overall length, projection length and seat angle remain unresolved.
  - Open: Internal materials/layer dimensions are illustrative and require a WR4-1 section drawing. Head bore angle and station are photo-informed provisional datums shared with the head. Leads and production fit remain unfinished.
- [ ] **Spark-plug ceramic insulator** — `spark-plug-insulator`; modeled quantity **6**; provisional.
  - Instances: `spark-plug-1-insulator`, `spark-plug-2-insulator`, `spark-plug-3-insulator`, `spark-plug-4-insulator`, `spark-plug-5-insulator`, `spark-plug-6-insulator`
  - Source IDs: ngk-2019-spark-plugs, ngk-plug-construction, ngk-uk-2017-thread-families. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: NGK lists WR4-1/4652 for 1993–94 F-150 4.9L. This does not identify the installed plug brand.
  - Open: Sourced envelope: 18 mm thread diameter, 11.684 mm reach, 20.6375 mm hex and tapered seat; .044 inch application gap. 1.5 mm pitch is inferred from NGK 18 mm families; exact thread tolerances, overall length, projection length and seat angle remain unresolved.
  - Open: Internal materials/layer dimensions are illustrative and require a WR4-1 section drawing. Head bore angle and station are photo-informed provisional datums shared with the head. Leads and production fit remain unfinished.
- [ ] **Spark-plug center electrode** — `spark-plug-center-electrode`; modeled quantity **6**; provisional.
  - Instances: `spark-plug-1-center-electrode`, `spark-plug-2-center-electrode`, `spark-plug-3-center-electrode`, `spark-plug-4-center-electrode`, `spark-plug-5-center-electrode`, `spark-plug-6-center-electrode`
  - Source IDs: ngk-2019-spark-plugs, ngk-plug-construction, ngk-uk-2017-thread-families. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: NGK lists WR4-1/4652 for 1993–94 F-150 4.9L. This does not identify the installed plug brand.
  - Open: Sourced envelope: 18 mm thread diameter, 11.684 mm reach, 20.6375 mm hex and tapered seat; .044 inch application gap. 1.5 mm pitch is inferred from NGK 18 mm families; exact thread tolerances, overall length, projection length and seat angle remain unresolved.
  - Open: Internal materials/layer dimensions are illustrative and require a WR4-1 section drawing. Head bore angle and station are photo-informed provisional datums shared with the head. Leads and production fit remain unfinished.
- [ ] **Spark-plug electrode core · illustrative** — `spark-plug-copper-core`; modeled quantity **6**; provisional.
  - Instances: `spark-plug-1-copper-core`, `spark-plug-2-copper-core`, `spark-plug-3-copper-core`, `spark-plug-4-copper-core`, `spark-plug-5-copper-core`, `spark-plug-6-copper-core`
  - Source IDs: ngk-2019-spark-plugs, ngk-plug-construction, ngk-uk-2017-thread-families. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: NGK lists WR4-1/4652 for 1993–94 F-150 4.9L. This does not identify the installed plug brand.
  - Open: Sourced envelope: 18 mm thread diameter, 11.684 mm reach, 20.6375 mm hex and tapered seat; .044 inch application gap. 1.5 mm pitch is inferred from NGK 18 mm families; exact thread tolerances, overall length, projection length and seat angle remain unresolved.
  - Open: Internal materials/layer dimensions are illustrative and require a WR4-1 section drawing. Head bore angle and station are photo-informed provisional datums shared with the head. Leads and production fit remain unfinished.
- [ ] **Spark-plug suppressor resistor · illustrative** — `spark-plug-resistor`; modeled quantity **6**; provisional.
  - Instances: `spark-plug-1-resistor`, `spark-plug-2-resistor`, `spark-plug-3-resistor`, `spark-plug-4-resistor`, `spark-plug-5-resistor`, `spark-plug-6-resistor`
  - Source IDs: ngk-2019-spark-plugs, ngk-plug-construction, ngk-uk-2017-thread-families. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: NGK lists WR4-1/4652 for 1993–94 F-150 4.9L. This does not identify the installed plug brand.
  - Open: Sourced envelope: 18 mm thread diameter, 11.684 mm reach, 20.6375 mm hex and tapered seat; .044 inch application gap. 1.5 mm pitch is inferred from NGK 18 mm families; exact thread tolerances, overall length, projection length and seat angle remain unresolved.
  - Open: Internal materials/layer dimensions are illustrative and require a WR4-1 section drawing. Head bore angle and station are photo-informed provisional datums shared with the head. Leads and production fit remain unfinished.
- [ ] **Spark-plug lower conductive seal · illustrative** — `spark-plug-lower-seal`; modeled quantity **6**; provisional.
  - Instances: `spark-plug-1-lower-seal`, `spark-plug-2-lower-seal`, `spark-plug-3-lower-seal`, `spark-plug-4-lower-seal`, `spark-plug-5-lower-seal`, `spark-plug-6-lower-seal`
  - Source IDs: ngk-2019-spark-plugs, ngk-plug-construction, ngk-uk-2017-thread-families. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: NGK lists WR4-1/4652 for 1993–94 F-150 4.9L. This does not identify the installed plug brand.
  - Open: Sourced envelope: 18 mm thread diameter, 11.684 mm reach, 20.6375 mm hex and tapered seat; .044 inch application gap. 1.5 mm pitch is inferred from NGK 18 mm families; exact thread tolerances, overall length, projection length and seat angle remain unresolved.
  - Open: Internal materials/layer dimensions are illustrative and require a WR4-1 section drawing. Head bore angle and station are photo-informed provisional datums shared with the head. Leads and production fit remain unfinished.
- [ ] **Spark-plug upper conductive seal · illustrative** — `spark-plug-upper-seal`; modeled quantity **6**; provisional.
  - Instances: `spark-plug-1-upper-seal`, `spark-plug-2-upper-seal`, `spark-plug-3-upper-seal`, `spark-plug-4-upper-seal`, `spark-plug-5-upper-seal`, `spark-plug-6-upper-seal`
  - Source IDs: ngk-2019-spark-plugs, ngk-plug-construction, ngk-uk-2017-thread-families. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: NGK lists WR4-1/4652 for 1993–94 F-150 4.9L. This does not identify the installed plug brand.
  - Open: Sourced envelope: 18 mm thread diameter, 11.684 mm reach, 20.6375 mm hex and tapered seat; .044 inch application gap. 1.5 mm pitch is inferred from NGK 18 mm families; exact thread tolerances, overall length, projection length and seat angle remain unresolved.
  - Open: Internal materials/layer dimensions are illustrative and require a WR4-1 section drawing. Head bore angle and station are photo-informed provisional datums shared with the head. Leads and production fit remain unfinished.
- [ ] **Spark-plug terminal and stem** — `spark-plug-terminal`; modeled quantity **6**; provisional.
  - Instances: `spark-plug-1-terminal`, `spark-plug-2-terminal`, `spark-plug-3-terminal`, `spark-plug-4-terminal`, `spark-plug-5-terminal`, `spark-plug-6-terminal`
  - Source IDs: ngk-2019-spark-plugs, ngk-plug-construction, ngk-uk-2017-thread-families. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: NGK lists WR4-1/4652 for 1993–94 F-150 4.9L. This does not identify the installed plug brand.
  - Open: Sourced envelope: 18 mm thread diameter, 11.684 mm reach, 20.6375 mm hex and tapered seat; .044 inch application gap. 1.5 mm pitch is inferred from NGK 18 mm families; exact thread tolerances, overall length, projection length and seat angle remain unresolved.
  - Open: Internal materials/layer dimensions are illustrative and require a WR4-1 section drawing. Head bore angle and station are photo-informed provisional datums shared with the head. Leads and production fit remain unfinished.
- [ ] **Spark-plug ground electrode** — `spark-plug-ground-electrode`; modeled quantity **6**; provisional.
  - Instances: `spark-plug-1-ground-electrode`, `spark-plug-2-ground-electrode`, `spark-plug-3-ground-electrode`, `spark-plug-4-ground-electrode`, `spark-plug-5-ground-electrode`, `spark-plug-6-ground-electrode`
  - Source IDs: ngk-2019-spark-plugs, ngk-plug-construction, ngk-uk-2017-thread-families. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: NGK lists WR4-1/4652 for 1993–94 F-150 4.9L. This does not identify the installed plug brand.
  - Open: Sourced envelope: 18 mm thread diameter, 11.684 mm reach, 20.6375 mm hex and tapered seat; .044 inch application gap. 1.5 mm pitch is inferred from NGK 18 mm families; exact thread tolerances, overall length, projection length and seat angle remain unresolved.
  - Open: Internal materials/layer dimensions are illustrative and require a WR4-1 section drawing. Head bore angle and station are photo-informed provisional datums shared with the head. Leads and production fit remain unfinished.

## Additional known scope and reconciliation

- [ ] Verify installed plug specification, gap and source-supported internal construction

## Cross-system boundaries

Coordinate with [#11](https://github.com/0xZakk/truck/issues/11). Keep the current engine-mounted component here; agree ownership before adding its vehicle-side continuation.

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
