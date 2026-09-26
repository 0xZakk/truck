# Clutch pilot bearing and internals

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#63](https://github.com/0xZakk/truck/issues/63).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `4f98bbdad7fb1996487d17c4a651de588cef39254efe24e96384375dbdce0c07`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **Pilot bearing outer case** — `pilot-bearing-case`; modeled quantity **1**; provisional.
  - Instances: `pilot-bearing-case`
  - Source IDs: timken-pilot-application, timken-pilot-dimensions. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Timken application catalog specifies FC65662 for 1990–2002 six-cylinder truck applications including 300/4.9L. Installed identity is not inspected.
  - Open: Needle-bearing table gives 1.4400 inch OD, 0.6721 inch shaft diameter and 0.6700 inch width. The same guide pilot table gives 1.450/0.671/0.669 inch; this discrepancy is preserved, not treated as manufacturing tolerance.
  - Open: Sixteen needles, needle size, cage, race section, seal and axial seating depth are illustrative. SPCL catalog type lacks a production section drawing. No rolling/contact/friction simulation or production interference fit.
- [ ] **Pilot bearing cage** — `pilot-bearing-cage`; modeled quantity **1**; provisional.
  - Instances: `pilot-bearing-cage`
  - Source IDs: timken-pilot-application, timken-pilot-dimensions. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Timken application catalog specifies FC65662 for 1990–2002 six-cylinder truck applications including 300/4.9L. Installed identity is not inspected.
  - Open: Needle-bearing table gives 1.4400 inch OD, 0.6721 inch shaft diameter and 0.6700 inch width. The same guide pilot table gives 1.450/0.671/0.669 inch; this discrepancy is preserved, not treated as manufacturing tolerance.
  - Open: Sixteen needles, needle size, cage, race section, seal and axial seating depth are illustrative. SPCL catalog type lacks a production section drawing. No rolling/contact/friction simulation or production interference fit.
- [ ] **Pilot bearing needle** — `pilot-bearing-needle`; modeled quantity **16**; provisional.
  - Instances: `pilot-bearing-needle-1`, `pilot-bearing-needle-2`, `pilot-bearing-needle-3`, `pilot-bearing-needle-4`, `pilot-bearing-needle-5`, `pilot-bearing-needle-6`, `pilot-bearing-needle-7`, `pilot-bearing-needle-8`, `pilot-bearing-needle-9`, `pilot-bearing-needle-10`, `pilot-bearing-needle-11`, `pilot-bearing-needle-12`, `pilot-bearing-needle-13`, `pilot-bearing-needle-14`, `pilot-bearing-needle-15`, `pilot-bearing-needle-16`
  - Source IDs: timken-pilot-application, timken-pilot-dimensions. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Timken application catalog specifies FC65662 for 1990–2002 six-cylinder truck applications including 300/4.9L. Installed identity is not inspected.
  - Open: Needle-bearing table gives 1.4400 inch OD, 0.6721 inch shaft diameter and 0.6700 inch width. The same guide pilot table gives 1.450/0.671/0.669 inch; this discrepancy is preserved, not treated as manufacturing tolerance.
  - Open: Sixteen needles, needle size, cage, race section, seal and axial seating depth are illustrative. SPCL catalog type lacks a production section drawing. No rolling/contact/friction simulation or production interference fit.
- [ ] **Pilot bearing seal** — `pilot-bearing-seal`; modeled quantity **1**; provisional.
  - Instances: `pilot-bearing-seal`
  - Source IDs: timken-pilot-application, timken-pilot-dimensions. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Timken application catalog specifies FC65662 for 1990–2002 six-cylinder truck applications including 300/4.9L. Installed identity is not inspected.
  - Open: Needle-bearing table gives 1.4400 inch OD, 0.6721 inch shaft diameter and 0.6700 inch width. The same guide pilot table gives 1.450/0.671/0.669 inch; this discrepancy is preserved, not treated as manufacturing tolerance.
  - Open: Sixteen needles, needle size, cage, race section, seal and axial seating depth are illustrative. SPCL catalog type lacks a production section drawing. No rolling/contact/friction simulation or production interference fit.

## Additional known scope and reconciliation

- [ ] Resolve conflicting catalog dimensions, crank bore fit and internal geometry

## Cross-system boundaries

Coordinate with [#2](https://github.com/0xZakk/truck/issues/2). Keep the current engine-mounted component here; agree ownership before adding its vehicle-side continuation.

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
