# Engine wiring harness, connectors and grounds

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#82](https://github.com/0xZakk/truck/issues/82).

**Backlog** — Known scope not delivered as a complete modeled/installed package; applicability and quantity may need research.

Baseline manifest: `91950c89dc12c17d1169ec77eed16efa71919c6832061346582ee02b81599ad6`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- No accepted installed definitions are mapped to this package; candidate artifacts may exist as noted below.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.


## Additional known scope and reconciliation

- [ ] Injector connectors, terminals, seals and retaining clips
- [ ] ECT/TPS/IAC/EVP/EVR/distributor/coil/switch mating connectors
- [ ] Engine harness branches, loom, splices, clips, grounds and bonding straps
- [ ] Intake-air sensor and separate gauge-temperature sender: verify exact location/applicability
- [ ] PCM and body-side wiring remain Electrical scope
- [ ] MAP C1011, ACT/IAT C164 and HO2S C1025 physical sensors are absent;14 connector interfaces are source-mapped, not14 modeled harness assemblies
- [ ] ACT serviceF2DZ12A697A is tag-qualified;3/8-18NPTF/25mmhex are applicable replacement dimensions, probe reach/connector envelope/installed depth unknown
- [ ] HO2S F4UZ-9F472-C service identity from exact-year Ford bulletin; exhaust pipe/bung host and sensor geometry remain missing

## Cross-system boundaries

Coordinate with [#11](https://github.com/0xZakk/truck/issues/11). Keep the current engine-mounted component here; agree ownership before adding its vehicle-side continuation.

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
