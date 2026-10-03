# Component research handoff: Bosch 15718 heated oxygen sensor

## Contract

- Issue #82 under engine #1; contributor `airbox_screw_finish`, integration owner root. Assigned primary-source research only, no CAD yet.
- Baseline read `6b14e88527295d56ef234113ccc3065c57db4e3b`, branch `engine/source-host-interfaces-20261002`. No assembly manifest consumed or changed; manifest hash N/A.
- Scope: identified Bosch 15718 /0258005718 replacement exterior, dimensions, connector and internal evidence. Prior qualified Ford TSB 94-16-9 identity F4UF-9F472-CA /service F4UZ-9F472-C remains in `engine-sensor-coverage.md`; this task does not requalify the owner's calibration or originality.
- Owned: `ho2s-online-20261003*` under `kb/sources`, `kb/notes`, `docs/components`, `reference/engine`. No shared KB index, CAD, manifest, viewer, issue or git writes.
- Intended detail: distinguish manufacturer numbers, observed topology, family architecture and unresolved dimensions. No sensor posed in a manifold; applicable front exhaust-pipe/bung host is absent.
- Units: mm/in as printed, with explicit endpoint labels. Origin, axis, parent transform and explode scheme N/A (no geometry). Future local datum should be the sealing/bearing plane, with a named thread axis and connector clocking frame, but no values selected here.
- Neighbor/interfaces: exhaust-pipe/bung seat and thread; hot-gas access to protection tube; four electrical circuits via C1025; flexible lead/harness joint. Current circuit separation from prior coverage: heater298/57, sensing74/89. Contact-to-cavity mapping and connector clocking remain unknown.
- Inputs verified: prior sensor-coverage handoff/evidence; public Bosch product HTML and three linked full-size photos; catalog and family brochure. Originals excluded. Capture SHA/URLs/locators are in `reference/engine/ho2s-online-20261003-evidence.json`.
- Checks planned/completed: verify identity chain and actual photo marking; inspect actual source pixels; preserve endpoint and family/target distinctions; validate JSON and prefixed KB links; no CAD acceptance checks applicable.

## Evidence ledger

| Claim | Value / datum | Evidence class and locator | Limit |
|---|---|---|---|
| Bosch identity | 0258005718→15718 | Manufacturer catalog PDF 27; actual pixels | Cross-reference, not owner's original sensor proof |
| Part-photo identity | 0258005718 marked shell, linked from15718 product | Manufacturer product HTML `productResponse.images`, three actual photos | Current replacement specimen appearance |
| Hex | 22 mm | Manufacturer product data `attrb.baseAttributes` | Hex size; no body diameter or axial dimensions follow |
| Sensor operation | Heated narrow-band, four terminals | Manufacturer product data; catalog PDF 18 lists heated/four wires | Not exact internal ceramic format |
| Connector | Four male round-ended contacts, round shroud, latch, colored annular seal | Product attributes + front/rear/right photos | No cavity numbers, mating connector, pin dimensions or circuit map |
| US length | 18.9 in, sealing surface to connector end | Manufacturer `otherAttributes` | 480.06 mm decimal conversion; rounded catalog481 mm retained separately |
| Catalog length | 18.9 in/481 mm | Catalog PDF 3 | No dimensioned endpoint picture; longer-harness substitutes are not same installed route |
| Regional length | 511 mm overall; four wires; round contacts; heated switching | Manufacturer regional page, search-indexed fields only | Direct page returned 502; endpoint/version compatibility not resolved |
| Exterior | Cylindrical/stepped shell, hex, annular ring at thread base, external threads, rounded slotted protective tip, four wire exits | Three identified manufacturer photos | Ring's precise sealing construction/material and hidden attachments unmeasured |
| Internal operation | Zirconia Nernst-cell switching | Bosch switching-family FAQ | Functional support, no 15718 section/BOM dimensions |
| Thimble-family internals | Protection tube, ceramic thimble, heater, electrodes/filter layers and rear connections | Trade brochure PDF 3 actual cutaway | Family reference only; perforated nose differs from target slots |
| Thread/pilot/engagement | Unknown from reviewed primary target sources | Gap | Retail M18×1.5 is a lead, not acceptance |
| Probe/body/connector dimensions | Unknown | Gap | Do not infer30 mm probe reach from511 − 481 |

The catalog currently linked by Bosch's US page and Mexico attachment9509184 have identical bytes/hash. A new URL is not a new edition. The indexed regional record is not treated as equal to an inspected dimensioned drawing. The qualifier matters because511 mm is sometimes described as cable length by retailers while Bosch labels it overall length.

## Physical breakdown and bounded next model

The available photographs support separating: (1) main metal shell/hex/threaded region; (2) annular seat-ring feature; (3) slotted protective gas-side tube; (4) stepped rear closure/wire-exit insulation; (5) four individual lead conductors/insulation and outer covering; (6) connector shroud/latch/insert/seal; and (7) four visible metal contacts. This is an exterior feature decomposition, not a verified service-disassembly BOM or proof every region is a separate manufactured part. The black wrap around the displayed folded harness is not evidence of installed vehicle retention.

Heater, sensing ceramic, electrical joints and insulating/sealing supports must be represented separately in any later educational cutaway, but their target-specific shape/stack remains unknown. Bosch's thimble brochure is a clearly labeled family comparison, not permission to copy its perforated cap or layer dimensions into15718. Current target data states heated switching; no reviewed source conclusively selects the current 15718 ceramic geometry as thimble versus planar. LSM11 motorsport drawings are excluded as unrelated dimensional proof.

This evidence supports a future **isolated exterior visual specimen**, after a modeling contract explicitly declares unresolved axial/connector/thread quantities as estimates or omissions. A dimensioned target drawing or identified donor survey should close thread pitch/class, seat diameter, engagement length, hex height, below-seat probe reach, shell diameters/lengths and connector dimensions. Multi-view photography with22 mm hex as an anchor could support a camera-fit estimate, but perspective and hex rotation must be solved and uncertainty retained; no such scale fit was performed here.

No installed geometry is authorized. Before installation, obtain the pipe/bung geometry and seat normal, insertion/protrusion relation to the gas passage, tool removal envelope, thermal clearance, lead slack/bend/retention route and mating connector frame. Do not fill the missing pipe ownership with a generic manifold placement.

## Learning and diagnostics

The heated sensing element compares exhaust oxygen with its reference and supplies switching feedback for fuel control; its heater helps it operate before exhaust heat alone suffices. Gas must reach the protective tip while insulation and seals preserve separate heater and sensing circuits. A metal placeholder with four wires does not explain those functions.

Contamination, damaged wiring/connector contacts, loss of heater function or a slow sensing response can compromise feedback. An exterior mesh cannot diagnose these faults or establish calibration, acceptable response time, heater resistance, torque or replacement interval. Use the applicable service procedure and preserve signal-ground versus heater-ground separation; no new repair specification is authored here.

## Delivery and reproduction

Readiness: **research**, not integration-ready. Parametric API, STEP, GLB, CAD renders, assembly integration call and generated-asset archive: N/A, no geometry. Source originals are neither committed nor archived. Six authored KB files plus this contract, observations and evidence ledger are frozen by `reference/engine/ho2s-online-20261003-delivery.json`. Root owns review/merge/issue tracking; no worker commit/PR.

Capture workflow: public page/PDF requests, extract only bounded relevant metadata/observations, inspect three full-size images and catalog/brochure pages, then `python3 tools/ingest.py reference/engine/ho2s-online-20261003-observations.txt --type local --title 'HO2S online 20261003 manufacturer observations'`; source pages then atomic notes. Raw capture is ignored. Semantic index/backlinker not run because root owns shared changes. All new KB links resolve.

Reproduction uses URLs and exact locators in the ledger; retrieve originals independently if visual re-review is needed. Public originals can change or become unavailable, so compare their hashes. The HTML embeds `var productResponse = JSON.stringify({...})`; parse the object as JSON rather than executing page code. Read `product.partId`, selected `attrb` fields and `images`. PDFs can be rasterized with `pdftoppm -f PAGE -singlefile -png INPUT OUTPUT`; no proprietary manual or original local temporary file is a dependency.

Environment: macOS, systemPython3/Poppler/curl. Basic sandbox network calls failed DNS resolution; authorized read-only public fetches succeeded with network-enabled execution. Regional page direct fetch returned 502; web PDF screenshot failed cache lookup, recovered by local rendering of public download. No access controls bypassed. Model/effort, tokens and billing unavailable.

## Validation and review

| Gate | Status | Evidence / remaining limit |
|---|---|---|
| Application/coverage | PASS scoped research | Qualified prior Ford→Bosch link; fresh Bosch ten-digit mapping and photo identity |
| Dimensions/coordinates | PASS research distinctions; metric installation unresolved |22 mm hex/new length endpoint; thread/probe/pose gaps explicit |
| CAD/export | N/A | No CAD |
| Source/visual | PASS observations | Actual full-size front/rear/right photos; catalog PDF 3/27 and brochure PDF 3 inspected; PDF 18 row checked |
| Installed interfaces | NOT RUN | No pipe/bung, host pose or lead route |
| Motion/disassembly | NOT RUN | No engine/body flex or service tool neighborhood |
| Learning/diagnostics | PASS bounded content | Functional architecture and limits, no unsourced service thresholds |
| Browser integration | NOT RUN | No runtime assets |
| Reproduction/review | PASS authored evidence; root review pending | URLs/hashes, exact HTML fields, PDF pages, observations→source→notes and frozen authored files |

Negative controls: reject511 − 481 as measured probe reach; reject thimble-family hole pattern as target slotted cap; reject retailblade-contact descriptor against actual round-ended contacts; reject display harness bundle as installed route; reject generic manifold host and LSM11 dimensions. These are explicit source-review controls, not automated geometry tests.

Verdict: reviewable research preservation, no installed acceptance. #82 remains open. Next action: root reviews the source ledger and scope, then decides an explicitly estimated isolated exterior study or further target-drawing research. No running process or implied background research at handoff; no shared geometry/checks invalidated.
