# Engine sensor coverage — research contract and handoff

## Contract

Assigned by engine integration owner under the engine reconstruction/electrical coverage work. Contributor: pump_foot_resume; integration owner: root. Baseline `6b1608257e8c2eaa12512ac0c256d882854f3996`, branch `engine/timing-drive-fit`. Canonical manifest SHA-256 `91950c89dc12c17d1169ec77eed16efa71919c6832061346582ee02b81599ad6`.

Research-only scope: missing MAP, ACT/IAT and heated oxygen sensor identities, dimensions, mounting ownership and physical breakdown. Own only `engine-sensor-coverage*` files. No CAD, manifest/map edits, engine pose changes or revision of frozen pump candidates. Millimeters for future CAD; sensor local frames and transforms are **unknown**. No guessed threaded standard from outside diameter. Exact calibration remains unknown.

Inputs: existing exact-year 1994 F-150 2WD 4.9L service-manual pages, Ford TSB 94-16-9 and reviewed electrical map. `inventory/engine/engine-sensor-coverage-evidence.json` hashes each selected local source. Manual originals remain excluded from distribution. Manufacturer sources are qualified replacement comparisons, not original Ford production drawings.

## Findings and evidence ledger

| Sensor | Applicable identity / topology | Dimensions supported and gaps | Installation ownership |
|---|---|---|---|
| MAP | Manual illustration callout 9S428; three-contact C1011 in EVTM map. Remote vacuum hose and bracket, rather than a screw-in manifold sensor. Complete service number unresolved. | No authoritative body dimensions, bolt pitch, nipple OD/ID, connector cavity/terminal sizes or bracket thickness found. Three contacts is electrical coverage, not dimensional evidence. | Service procedure locates sensor/bracket below cowl drip rail. Cowl/body datum is absent from current engine manifest. Hose endpoint on manifold and routing remain open. Do not bolt a generic MAP onto engine to hide the missing host. |
| ACT / IAT | One physical sensor, manual callout 12A697; C164 has two contacts. NTC thermistor projects into intake airflow. Figure 147826554 places it on lower intake casting. Full target service number unresolved. | Exact manual torque 16–24 N·m. No target thread, engagement length, probe reach, body length or connector dimensions verified. MTE-THOMSON 5041 comparison specifies 3/8-18 NPTF and 25 mm hex, two pins; target application transfer unverified. | Existing `efi-lower-intake` is candidate host, but this audit does not prove a modeled matching port. Axis, seat, insertion depth and connector rotation require a fresh source-bound host review. |
| Heated O2 | Ford TSB 94-16-9, dated 1994-08-10, Figure 2: 1994 F-Series 4.9L engineering F4UF-9F472-CA, service F4UZ-9F472-C. C1025 has four contacts. | Exact manual torque 36–46 N·m. Bosch cross-reference supports 15718; catalog length 18.9 in / 481 mm is a replacement envelope datum with unspecified endpoints, not a body length. Target thread pitch, hex, insertion depth, sealing seat, connector dimensions and exact lead route remain unverified. | Applicable service text and figure 150757959 place it in exhaust pipe. Current manifest has front/rear exhaust manifolds but no identified front exhaust-pipe/bung host. Generic description says manifold: preserve this conflict; do not drill current manifold from that generic sentence. |

The TSB differentiates Econoline 4.9L (F4UZ-9F472-A) from F-Series 4.9L (C). This is useful applicability evidence. It is not evidence that the owner's installed sensor remains original.

[Bosch manufacturer catalog](https://www.boschautopartes.mx/o/commerce-media/accounts/-1/attachments/9650200?download=true), PDF pages 3 and 46, maps F4UZ-9F472-C to 15718 and lists 481 mm. The substitution section discusses differing harness lengths; no dimensional endpoint drawing was found. Do not turn 481 mm into a straight installed lead or use a different lead variant without a routing contract.

[MTE-THOMSON 5041 manufacturer page](https://cate.mte-thomson.com.br/pt/br/produto/detalhes/5041/plug-eletronico--ar) lists historical Ford 12A697 references and other Ford applications, but no reviewed 1994 F-150 4.9 entry. Its explicit thread/hex values support a comparison only. Its 6 × 3.3 × 3.3 cm dimensions describe packaging and are excluded from geometry.

## Conflicts and rejected shortcuts

Retail AX3 data reports M18×1.50; a TS4052 listing reports both M16×1.5 and 3/8-18 Dryseal. These are unresolved catalog conflicts, not alternative tolerances. Retail 18 mm oxygen-sensor diameter does not establish M18×1.5. No such target thread is selected by this task. Cross-engine temperature sensors and a GM Delphi MAP result were excluded. An older three-wire oxygen-sensor application lead cannot override the exact-year four-contact EVTM and Ford TSB identity. NTK's large catalog was searchable but could not be fully fetched by the available web tool; its 22503 lead remains unverified here.

Full manufacturer external/connector drawings were not obtained for any of the three. This is a bounded search result, not a claim that no drawings exist. No photo dimensions were silently promoted.

## Physical breakdown and buildability

- **MAP:** sensor enclosure/cover, three electrical contacts and connector shroud, pressure element/circuit module, vacuum nipple; separately bracket, attachment hardware and vacuum hose. Exact enclosure seam, internal element dimensions and fastener count/specification need evidence. Educational internals would require explicitly illustrative geometry. Complete installed CAD is blocked by body/cowl coordinates and source-sized interfaces.
- **ACT:** metal threaded shell/hex and probe protection, thermistor element, insulating connector body and two contacts; harness mating shell/contacts belong to harness. Do not model ACT and IAT as two sensors. The existing intake host makes this the best next bounded measurement task, but no threaded candidate is authorized by this research.
- **HO2S:** threaded metal shell/hex and protective tip, zirconia sensing element, internal heater, insulating/sealing stack, four leads with strain relief and four-contact connector; harness mating connector and exhaust bung/pipe remain separate owners. The manual supports functional architecture, not a dimensioned internal BOM. It is not four generic wires terminating inside a solid rod. Source-sized external candidate needs a matched replacement drawing or physical specimen; installation also needs pipe/bung and harness routing.

For future mating checks retain circuit separation: MAP reference351, return359 and signal358; ACT return359 and signal743; O2 heater supply298, heater ground57, signal74 and oxygen ground89. Signal ground89 is not heater ground57 or sensor return359. Component cavity indices are unknown in the accepted map; don't infer pin order from wire count.

## Delivery and validation

Readiness **research**, not build-ready or accepted installed. Delivered this handoff plus hash-bound evidence JSON. No STEP/GLB/render produced; no geometry changed. Exact-year illustrations were visually reviewed locally; source originals are not copied into the delivery. Commands: `python3 -m json.tool inventory/engine/engine-sensor-coverage-evidence.json >/dev/null`; independently rehash source paths from the JSON before reuse. Environment macOS/Python3; CAD dependencies N/A. Model/effort and usage unavailable.

| Quality gate | Status / basis |
|---|---|
| Application/coverage | PASS bounded service/electrical identities, with MAP/ACT full part numbers unresolved |
| Dimensions/coordinates | NOT VERIFIED; table identifies every usable comparison and unresolved datum |
| CAD/export | N/A: research-only task, no candidate |
| Source/visual comparison | PASS for reading service figures; CAD comparison N/A |
| Installed interfaces | NOT RUN; hosts, threads and poses are unresolved |
| Motion/disassembly | NOT RUN; future hose/lead strain, hot-neighbor clearance and tool access required |
| Learning/diagnostics | Bounded physical/function coverage above; diagnostic thresholds not authored |
| Browser integration | NOT RUN; no assets or navigation changes |
| Reproduction/review | Local inputs hashed; public URLs and PDF pages recorded; root review pending |

Next actions: prioritize an applicable ACT specimen/drawing and inspect the lower-intake port; obtain dimensioned MAP/bracket and cowl registration; obtain Bosch15718 or confirmed Ford sensor dimensional drawing plus front-pipe source. These are concrete evidence dependencies, not permission to estimate threads or install placeholder geometry. No running process. All frozen pump reports and failures remain unchanged.
