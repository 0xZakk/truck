# ACT/IAT sensor identity — bounded research handoff

## Contract

Root-assigned next step under engine-control coverage: resolve the missing 1994 F-150 4.9L ACT/IAT service identity and source-sized interface. Research only; no CAD, shared manifests, electrical maps or frozen sensor/pump reports changed. Owned files: this handoff and `inventory/engine/act-sensor-identity-evidence.json`. Root remains integration owner. Baseline and exact local source hashes are in the evidence JSON; shared branch `engine/timing-drive-fit`. Canonical baseline SHA remains `91950c89dc12c17d1169ec77eed16efa71919c6832061346582ee02b81599ad6`.

## Evidence and result

The local exact-year **Parts and Labor → Sensors and Switches → Powertrain Management → Computers and Control Systems → Air Temperature Sensor (Ambient/Intake) → Parts Information** entry identifies manufacturer FOR, service part **F2DZ12A697A**, and instructs **“Order By Tag Number.”** This resolves the service listing, not the unseen original sensor's engineering stamp. The hashed page is a locally retained manual/parts-data reproduction, not a newly obtained Ford engineering drawing. It is not redistributed.

[MTE-THOMSON 5041](https://cate.mte-thomson.com.br/pt/br/produto/detalhes/5041/plug-eletronico--ar) explicitly includes **F2DZ12A697A** in its Ford OE interchange. Manufacturer attributes specify **3/8-18 NPTF**, **25 mm hex**, **two pins**, white connector body. This is the missing applicability bridge from the earlier coverage report: those dimensions now support an identified replacement comparison. They still do not prove original Ford production dimensions or a complete installed sensor. Its 6 × 3.3 × 3.3 cm field is packaging, never a geometry envelope.

[Tomco's manufacturer IAT catalog](https://tomco-inc.com/Catalog/iat%20sensors.pdf), printed page176, corroborates F150 1987–1995 4.9L(Y) →12100 with E4AF-12A697AA/BA, F1AF-BA, F2DF-AA and F2DZ-A references. The indexed manufacturer table was inspected; direct full-PDF retrieval timed out. These references are a compatible family, not permission to select a particular unseen engineering stamp. A separate 1995 F4TZ-12A697A row uses12125 and must stay distinct. Later F57Z-12A697A is not this resolved service identity.

[Walker manufacturer's OEM interchange](https://www.walkerproducts.com/wp-content/uploads/2021/06/Commercial-Vehicle-Products-Buyers-Guide.pdf) independently maps F2DZ12A697A to210-1002. It supplies another identifiable replacement to measure, not a dimensioned drawing.

[Parker's thread terminology](https://www.parker.com/literature/Literature%20Files/tfd/cat/pdffiles/T-Assembly%20Installation.pdf) establishes that NPTF denotes a tapered dryseal pipe-thread family. This supports a thread-sealing architecture, rather than inventing a straight metric thread with a shoulder washer. It does **not** establish this sensor's coating, need for supplemental compound, female port class, thread length or installed depth. The exact-year service page specifies16–24 N·m, but that torque alone cannot locate the sensor axially or determine thread engagement. Do not assume its hex bottoms on the manifold.

## Unresolved dimensional contract

| Required feature | Current evidence | Next acceptable evidence |
|---|---|---|
| Thread designation | Applicable replacement3/8-18 NPTF | Gauge/specification for selected replacement and actual host port; preserve class and reference plane |
| Sealing architecture | Tapered thread family | Sensor-specific instruction/coating or measured original; no invented washer |
| Probe reach | UNKNOWN | Tip-to-thread-gauge-plane or other explicit datum on drawing/specimen |
| Overall length and hex thickness | UNKNOWN; hex across flats25mm for5041 only | Dimensioned drawing or specimen measurements |
| Connector envelope | Two pins/white body only | Length, diameter, keyed latch, terminal spacing/diameter/recess, matching harness cavity |
| Installed depth and orientation | UNKNOWN | Host port gauge plane, engagement, internal airflow/wall bounds and harness approach |
| Exact engineering stamp | UNKNOWN | Owner part tag or specifically applicable Ford engineering-number record |

A finite search covered existing exact-year parts/service pages, exact service-number manufacturer interchanges, Tomco application catalog, Walker catalog and MTE manufacturer specifications. Focused manufacturer drawing searches did not produce probe or connector dimensions. No geometry has been inferred from package sizes, generic OD or catalog photos. Earlier retail AX3/TS4052 thread contradictions remain in the frozen coverage report; the new primary replacement bridge provides a stronger3/8-18 NPTF comparison without silently rewriting those failures.

## Delivery, validation and restart

Readiness: **research; not build-ready**. Deliverables: this handoff and hash-bound evidence JSON. CAD/export/source-versus-render: N/A because no candidate was made. Application identity: PASS for the qualified exact-year service listing. Replacement thread/hex bridge: PASS. Probe/connector/installed dimensional completeness: **NOT VERIFIED**. Installed contact, airflow, tool, motion, browser gates: **NOT RUN**. No part/occurrence count or completion claim changes.

Best next bounded action: acquire an F2DZ-12A697-A-tagged sensor or identified5041/12100/210-1002 specimen/drawing. Record all measurements against an explicit threaded datum, then inspect `efi-lower-intake` for the corresponding port and airflow exposure before proposing CAD. One assembly must represent ACT/IAT, with metal shell/probe, thermistor, insulating connector and two contacts; don't create two sensors from alternate terminology. C164 harness mating connector remains separate ownership.

Reproduce local evidence: locate the exact source path in JSON, verify SHA-256, then read its part number and tag qualification. Recheck public manufacturer interchanges before using revised catalogs. Command: `python3 -m json.tool inventory/engine/act-sensor-identity-evidence.json >/dev/null`. macOS/Python3, no CAD runtime used. Sources remain private or externally cited; no originals committed. Root review pending; no active process. Model/effort/usage unavailable.
