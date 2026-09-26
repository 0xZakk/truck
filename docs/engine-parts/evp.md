# EGR valve-position sensor and internals

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#57](https://github.com/0xZakk/truck/issues/57).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `4f98bbdad7fb1996487d17c4a651de588cef39254efe24e96384375dbdce0c07`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **EVP sensor housing** — `evp-body`; modeled quantity **1**; provisional.
  - Instances: `evp-body`
  - Source IDs: truck-egr-evtm, standard-egv258, system-d015c4a19a04. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Three-wire potentiometer topology follows Ford EVTM23-4. All internal dimensions, contact layout, spring rate and physical part decomposition are illustrative rather than teardown-verified.
  - Open: The external three-fastener mounting and circular seal follow replacement photographs. Installed sensor identity, cavity assignment, electrical leads, resistance and calibration remain unresolved.
- [ ] **EVP sensor lid** — `evp-lid`; modeled quantity **1**; provisional.
  - Instances: `evp-lid`
  - Source IDs: truck-egr-evtm, standard-egv258, system-d015c4a19a04. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Three-wire potentiometer topology follows Ford EVTM23-4. All internal dimensions, contact layout, spring rate and physical part decomposition are illustrative rather than teardown-verified.
  - Open: The external three-fastener mounting and circular seal follow replacement photographs. Installed sensor identity, cavity assignment, electrical leads, resistance and calibration remain unresolved.
- [ ] **EVP flange seal** — `evp-flange-seal`; modeled quantity **1**; provisional.
  - Instances: `evp-flange-seal`
  - Source IDs: truck-egr-evtm, standard-egv258, system-d015c4a19a04. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Three-wire potentiometer topology follows Ford EVTM23-4. All internal dimensions, contact layout, spring rate and physical part decomposition are illustrative rather than teardown-verified.
  - Open: The external three-fastener mounting and circular seal follow replacement photographs. Installed sensor identity, cavity assignment, electrical leads, resistance and calibration remain unresolved.
- [ ] **EVP spring-loaded follower** — `evp-follower`; modeled quantity **1**; provisional.
  - Instances: `evp-follower`
  - Source IDs: truck-egr-evtm, standard-egv258, system-d015c4a19a04. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Three-wire potentiometer topology follows Ford EVTM23-4. All internal dimensions, contact layout, spring rate and physical part decomposition are illustrative rather than teardown-verified.
  - Open: The external three-fastener mounting and circular seal follow replacement photographs. Installed sensor identity, cavity assignment, electrical leads, resistance and calibration remain unresolved.
- [ ] **EVP follower spring** — `evp-follower-spring`; modeled quantity **1**; provisional.
  - Instances: `evp-follower-spring`
  - Source IDs: truck-egr-evtm, standard-egv258, system-d015c4a19a04. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Three-wire potentiometer topology follows Ford EVTM23-4. All internal dimensions, contact layout, spring rate and physical part decomposition are illustrative rather than teardown-verified.
  - Open: The external three-fastener mounting and circular seal follow replacement photographs. Installed sensor identity, cavity assignment, electrical leads, resistance and calibration remain unresolved.
- [ ] **EVP spring stop** — `evp-spring-stop`; modeled quantity **1**; provisional.
  - Instances: `evp-spring-stop`
  - Source IDs: truck-egr-evtm, standard-egv258, system-d015c4a19a04. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Three-wire potentiometer topology follows Ford EVTM23-4. All internal dimensions, contact layout, spring rate and physical part decomposition are illustrative rather than teardown-verified.
  - Open: The external three-fastener mounting and circular seal follow replacement photographs. Installed sensor identity, cavity assignment, electrical leads, resistance and calibration remain unresolved.
- [ ] **EVP resistive-element carrier** — `evp-resistor-carrier`; modeled quantity **1**; provisional.
  - Instances: `evp-resistor-carrier`
  - Source IDs: truck-egr-evtm, standard-egv258, system-d015c4a19a04. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Three-wire potentiometer topology follows Ford EVTM23-4. All internal dimensions, contact layout, spring rate and physical part decomposition are illustrative rather than teardown-verified.
  - Open: The external three-fastener mounting and circular seal follow replacement photographs. Installed sensor identity, cavity assignment, electrical leads, resistance and calibration remain unresolved.
- [ ] **EVP resistance track** — `evp-resistance-track`; modeled quantity **1**; provisional.
  - Instances: `evp-resistance-track`
  - Source IDs: truck-egr-evtm, standard-egv258, system-d015c4a19a04. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Three-wire potentiometer topology follows Ford EVTM23-4. All internal dimensions, contact layout, spring rate and physical part decomposition are illustrative rather than teardown-verified.
  - Open: The external three-fastener mounting and circular seal follow replacement photographs. Installed sensor identity, cavity assignment, electrical leads, resistance and calibration remain unresolved.
- [ ] **EVP signal collector** — `evp-collector-track`; modeled quantity **1**; provisional.
  - Instances: `evp-collector-track`
  - Source IDs: truck-egr-evtm, standard-egv258, system-d015c4a19a04. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Three-wire potentiometer topology follows Ford EVTM23-4. All internal dimensions, contact layout, spring rate and physical part decomposition are illustrative rather than teardown-verified.
  - Open: The external three-fastener mounting and circular seal follow replacement photographs. Installed sensor identity, cavity assignment, electrical leads, resistance and calibration remain unresolved.
- [ ] **EVP wiper contact** — `evp-wiper`; modeled quantity **1**; provisional.
  - Instances: `evp-wiper`
  - Source IDs: truck-egr-evtm, standard-egv258, system-d015c4a19a04. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Three-wire potentiometer topology follows Ford EVTM23-4. All internal dimensions, contact layout, spring rate and physical part decomposition are illustrative rather than teardown-verified.
  - Open: The external three-fastener mounting and circular seal follow replacement photographs. Installed sensor identity, cavity assignment, electrical leads, resistance and calibration remain unresolved.
- [ ] **EVP terminal 1** — `evp-terminal-1`; modeled quantity **1**; provisional.
  - Instances: `evp-terminal-1`
  - Source IDs: truck-egr-evtm, standard-egv258, system-d015c4a19a04. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Three-wire potentiometer topology follows Ford EVTM23-4. All internal dimensions, contact layout, spring rate and physical part decomposition are illustrative rather than teardown-verified.
  - Open: The external three-fastener mounting and circular seal follow replacement photographs. Installed sensor identity, cavity assignment, electrical leads, resistance and calibration remain unresolved.
- [ ] **EVP terminal 2** — `evp-terminal-2`; modeled quantity **1**; provisional.
  - Instances: `evp-terminal-2`
  - Source IDs: truck-egr-evtm, standard-egv258, system-d015c4a19a04. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Three-wire potentiometer topology follows Ford EVTM23-4. All internal dimensions, contact layout, spring rate and physical part decomposition are illustrative rather than teardown-verified.
  - Open: The external three-fastener mounting and circular seal follow replacement photographs. Installed sensor identity, cavity assignment, electrical leads, resistance and calibration remain unresolved.
- [ ] **EVP terminal 3** — `evp-terminal-3`; modeled quantity **1**; provisional.
  - Instances: `evp-terminal-3`
  - Source IDs: truck-egr-evtm, standard-egv258, system-d015c4a19a04. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Three-wire potentiometer topology follows Ford EVTM23-4. All internal dimensions, contact layout, spring rate and physical part decomposition are illustrative rather than teardown-verified.
  - Open: The external three-fastener mounting and circular seal follow replacement photographs. Installed sensor identity, cavity assignment, electrical leads, resistance and calibration remain unresolved.
- [ ] **EVP retaining screw 1** — `evp-screw-1`; modeled quantity **1**; provisional.
  - Instances: `evp-screw-1`
  - Source IDs: truck-egr-evtm, standard-egv258, system-d015c4a19a04. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Three-wire potentiometer topology follows Ford EVTM23-4. All internal dimensions, contact layout, spring rate and physical part decomposition are illustrative rather than teardown-verified.
  - Open: The external three-fastener mounting and circular seal follow replacement photographs. Installed sensor identity, cavity assignment, electrical leads, resistance and calibration remain unresolved.
- [ ] **EVP retaining screw 2** — `evp-screw-2`; modeled quantity **1**; provisional.
  - Instances: `evp-screw-2`
  - Source IDs: truck-egr-evtm, standard-egv258, system-d015c4a19a04. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Three-wire potentiometer topology follows Ford EVTM23-4. All internal dimensions, contact layout, spring rate and physical part decomposition are illustrative rather than teardown-verified.
  - Open: The external three-fastener mounting and circular seal follow replacement photographs. Installed sensor identity, cavity assignment, electrical leads, resistance and calibration remain unresolved.
- [ ] **EVP retaining screw 3** — `evp-screw-3`; modeled quantity **1**; provisional.
  - Instances: `evp-screw-3`
  - Source IDs: truck-egr-evtm, standard-egv258, system-d015c4a19a04. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: Three-wire potentiometer topology follows Ford EVTM23-4. All internal dimensions, contact layout, spring rate and physical part decomposition are illustrative rather than teardown-verified.
  - Open: The external three-fastener mounting and circular seal follow replacement photographs. Installed sensor identity, cavity assignment, electrical leads, resistance and calibration remain unresolved.

## Additional known scope and reconciliation

- [ ] Verify follower/contact construction, calibration and connector

## Cross-system boundaries

Coordinate with [#7](https://github.com/0xZakk/truck/issues/7). Keep the current engine-mounted component here; agree ownership before adding its vehicle-side continuation.

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
