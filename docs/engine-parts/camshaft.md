# Camshaft and cam bearings

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#31](https://github.com/0xZakk/truck/issues/31).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `4f98bbdad7fb1996487d17c4a651de588cef39254efe24e96384375dbdce0c07`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **Camshaft bearing** — `cam-bearing`; modeled quantity **4**; provisional.
  - Instances: `cam-bearing-1`, `cam-bearing-2`, `cam-bearing-3`, `cam-bearing-4`
  - Source IDs: fsm-2e5473b2bf99. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Exact production contours, dimensions and tolerances need applicable drawings or measurements.
- [ ] **Camshaft** — `camshaft`; modeled quantity **1**; provisional.
  - Instances: `camshaft`
  - Source IDs: fsm-33bfe47109d5, fsm-2e5473b2bf99, ford-industrial-csg649, fsm-a3698a10af15, melling-intermediate-shaft-dimensions, melling-camshaft-specifications, melling-stock-valve-specifications, melling-pushrod-specifications. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Journal diameter uses the midpoint of the factory range. Front journal, nose and key seat now meet the retention study; axial stations and key dimensions remain assumed. Lobe profiles, timing events and distributor drive remain unresolved.
  - Open: 20 degree lean, X227.584 station, gear-axis spacing, distributor lower extension, mounting bosses and pickup bends are constrained fit-study assumptions, not surveyed Ford geometry.
  - Open: Melling IS-74 length 114.808 mm and hex across flats 7.9248 mm remain unchanged. Ten mm upper and nine mm lower engagement are assumed.
  - Open: Cam-to-distributor crossed-helical tooth geometry, working backlash and angular phase remain unverified; this is a connected spatial study, not validated power transmission.
  - Open: Oil galleries and pump mounting architecture require a production reference. Proposed block cuts and supports must not be used as machining instructions.
  - Open: Coordinated motion is a teaching construction. The smooth lobe law fits selected Melling SYB-38 scalars; the installed cam, full lift law, advertised checking height and production timing remain unverified.
  - Open: Rigid linkage and constant-wire spring deformation explain motion; hydraulic lash adjustment, spring dynamics, lubrication, fatigue and running-engine performance are not simulated.
  - Open: Rear cam journal and bearing move from assumedX-330to-334mm to clear the complete cylinder6 intake follower. Journal width23mm, bearing width22mm and axial coordinates remain unverified; source radial dimensions are preserved.
  - Open: The existing continuous cam bore supports the revised bearing location; actual bearing retention, oil-feed indexing and axial production layout remain unresolved.
  - Open: The head gasket pushrod openings retain their old clearance and gain a6mm-radius cut at the revisedY90axis. Hole contours and sealing lands remain provisional; positive passage checks do not establish a production gasket.

## Additional known scope and reconciliation

- [ ] Verify actual cam identity, lobe law, journals, oil feeds and phase

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
