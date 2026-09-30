# Ignition coil and internals

Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: [#52](https://github.com/0xZakk/truck/issues/52).

**In review** — Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.

Baseline manifest: `91950c89dc12c17d1169ec77eed16efa71919c6832061346582ee02b81599ad6`. Quantities below count current modeled instances, not verified production quantities.

## Existing modeled parts

- [x] Provisional geometry is present in the integrated engine manifest.

Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.

- [ ] **Coil E-core · lamination stack** — `ignition-coil-core-e`; modeled quantity **1**; provisional.
  - Instances: `ignition-coil-core-e`
  - Source IDs: system-f015ea2ab18c, system-f1571449160a, system-4fe310c18acd, ford-dg470. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: DG470/F7PZ12029AA matches the archived service part, but the installed coil identity has not been read.
  - Open: All dimensions, mounting datum, winding order, wire turns, core lamination count and internal connections are unverified. Winding packs are aggregate teaching volumes, not individual wires.
  - Open: Bracket, fasteners, potting, interference capacitor and installed harness remain unfinished. This is not a service-disassembly sequence.
- [ ] **Coil core closing stack** — `ignition-coil-core-i`; modeled quantity **1**; provisional.
  - Instances: `ignition-coil-core-i`
  - Source IDs: system-f015ea2ab18c, system-f1571449160a, system-4fe310c18acd, ford-dg470. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: DG470/F7PZ12029AA matches the archived service part, but the installed coil identity has not been read.
  - Open: All dimensions, mounting datum, winding order, wire turns, core lamination count and internal connections are unverified. Winding packs are aggregate teaching volumes, not individual wires.
  - Open: Bracket, fasteners, potting, interference capacitor and installed harness remain unfinished. This is not a service-disassembly sequence.
- [ ] **Coil bobbin · illustrative** — `ignition-coil-bobbin`; modeled quantity **1**; provisional.
  - Instances: `ignition-coil-bobbin`
  - Source IDs: system-f015ea2ab18c, system-f1571449160a, system-4fe310c18acd, ford-dg470. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: DG470/F7PZ12029AA matches the archived service part, but the installed coil identity has not been read.
  - Open: All dimensions, mounting datum, winding order, wire turns, core lamination count and internal connections are unverified. Winding packs are aggregate teaching volumes, not individual wires.
  - Open: Bracket, fasteners, potting, interference capacitor and installed harness remain unfinished. This is not a service-disassembly sequence.
- [ ] **Coil primary winding pack** — `ignition-coil-primary`; modeled quantity **1**; provisional.
  - Instances: `ignition-coil-primary`
  - Source IDs: system-f015ea2ab18c, system-f1571449160a, system-4fe310c18acd, ford-dg470. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: DG470/F7PZ12029AA matches the archived service part, but the installed coil identity has not been read.
  - Open: All dimensions, mounting datum, winding order, wire turns, core lamination count and internal connections are unverified. Winding packs are aggregate teaching volumes, not individual wires.
  - Open: Bracket, fasteners, potting, interference capacitor and installed harness remain unfinished. This is not a service-disassembly sequence.
- [ ] **Coil interwinding insulation · illustrative** — `ignition-coil-insulation`; modeled quantity **1**; provisional.
  - Instances: `ignition-coil-insulation`
  - Source IDs: system-f015ea2ab18c, system-f1571449160a, system-4fe310c18acd, ford-dg470. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: DG470/F7PZ12029AA matches the archived service part, but the installed coil identity has not been read.
  - Open: All dimensions, mounting datum, winding order, wire turns, core lamination count and internal connections are unverified. Winding packs are aggregate teaching volumes, not individual wires.
  - Open: Bracket, fasteners, potting, interference capacitor and installed harness remain unfinished. This is not a service-disassembly sequence.
- [ ] **Coil secondary winding pack** — `ignition-coil-secondary`; modeled quantity **1**; provisional.
  - Instances: `ignition-coil-secondary`
  - Source IDs: system-f015ea2ab18c, system-f1571449160a, system-4fe310c18acd, ford-dg470. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: DG470/F7PZ12029AA matches the archived service part, but the installed coil identity has not been read.
  - Open: All dimensions, mounting datum, winding order, wire turns, core lamination count and internal connections are unverified. Winding packs are aggregate teaching volumes, not individual wires.
  - Open: Bracket, fasteners, potting, interference capacitor and installed harness remain unfinished. This is not a service-disassembly sequence.
- [ ] **Coil molded insulation and connectors** — `ignition-coil-case`; modeled quantity **1**; provisional.
  - Instances: `ignition-coil-case`
  - Source IDs: system-f015ea2ab18c, system-f1571449160a, system-4fe310c18acd, ford-dg470. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: DG470/F7PZ12029AA matches the archived service part, but the installed coil identity has not been read.
  - Open: All dimensions, mounting datum, winding order, wire turns, core lamination count and internal connections are unverified. Winding packs are aggregate teaching volumes, not individual wires.
  - Open: Bracket, fasteners, potting, interference capacitor and installed harness remain unfinished. This is not a service-disassembly sequence.
- [ ] **Coil high-voltage terminal** — `ignition-coil-hv-terminal`; modeled quantity **1**; provisional.
  - Instances: `ignition-coil-hv-terminal`
  - Source IDs: system-f015ea2ab18c, system-f1571449160a, system-4fe310c18acd, ford-dg470. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: DG470/F7PZ12029AA matches the archived service part, but the installed coil identity has not been read.
  - Open: All dimensions, mounting datum, winding order, wire turns, core lamination count and internal connections are unverified. Winding packs are aggregate teaching volumes, not individual wires.
  - Open: Bracket, fasteners, potting, interference capacitor and installed harness remain unfinished. This is not a service-disassembly sequence.
- [ ] **Coil primary terminal** — `ignition-coil-primary-terminal`; modeled quantity **2**; provisional.
  - Instances: `ignition-coil-primary-terminal-1`, `ignition-coil-primary-terminal-2`
  - Source IDs: system-f015ea2ab18c, system-f1571449160a, system-4fe310c18acd, ford-dg470. Resolve in `inventory/engine/full-assembly.json` / evidence records.
  - Open: DG470/F7PZ12029AA matches the archived service part, but the installed coil identity has not been read.
  - Open: All dimensions, mounting datum, winding order, wire turns, core lamination count and internal connections are unverified. Winding packs are aggregate teaching volumes, not individual wires.
  - Open: Bracket, fasteners, potting, interference capacitor and installed harness remain unfinished. This is not a service-disassembly sequence.

## Additional known scope and reconciliation

- [ ] Primary connector, terminals and suppression capacitor: reconcile vehicle configuration
- [ ] Verify winding construction and production envelope

## Cross-system boundaries

Coordinate with [#11](https://github.com/0xZakk/truck/issues/11). Keep the current engine-mounted component here; agree ownership before adding its vehicle-side continuation.

## Acceptance and handoff

Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.

Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.
