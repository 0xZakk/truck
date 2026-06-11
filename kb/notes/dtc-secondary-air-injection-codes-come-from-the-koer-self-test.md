---
title: "Secondary air injection DTCs are produced by the KOER self-test as the PCM commands and watches the thermactor system"
kind: troubleshooting
source: "[[sources/dtc-emissions-egr-codes|EEC DTCs 311-341, 558-572 — EGR and Emissions Codes (FSM)]]"
related:
  - "[[notes/dtc-egr-codes-split-by-pressure-sensor-vs-position-sensor|EGR DTCs split into two families depending on whether the truck uses a pressure (PFE) or position (EVP) feedback sensor]]"
  - "[[notes/dtc-self-test-runs-in-koeo-and-koer-modes|The EEC self-test runs in two modes — Key On Engine Off and Key On Engine Running — and each finds different faults]]"
tags:
  - dtc
  - secondary-air-injection
  - thermactor
  - emissions
  - koer
---

The secondary air injection (thermactor) system pumps air into the exhaust to help oxidize
unburned fuel, and the EEC verifies it works during the KOER self-test by commanding the air
in different directions and watching the oxygen sensors react. The four KOER codes describe
exactly which behavior failed: DTC 311 (system inoperative, bank #1), 312 (air misdirected),
313 (not bypassed), and 314 (inoperative, bank #2) — all routing to pinpoint test KC1.

Separately, the KOEO self-test checks the thermactor control circuits electrically without
the engine running: DTC 552 (secondary air injection bypass circuit failure) and 553
(diverter circuit failure) route to KC9. The split mirrors the general pattern — KOER catches
a system that is wired correctly but not flowing air where commanded, while KOEO catches an
open or shorted solenoid drive circuit.

For the truck's `engine`, a 311-314 code means the air pump, check valves, or routing
hardware are the suspects, whereas 552/553 point at the bypass/diverter solenoid wiring.

## Related Concepts

- [[notes/dtc-egr-codes-split-by-pressure-sensor-vs-position-sensor|EGR DTCs split into two families depending on whether the truck uses a pressure (PFE) or position (EVP) feedback sensor]]
- [[notes/dtc-self-test-runs-in-koeo-and-koer-modes|The EEC self-test runs in two modes — Key On Engine Off and Key On Engine Running — and each finds different faults]]

## Source

- [[sources/dtc-emissions-egr-codes|EEC DTCs 311-341, 558-572 — EGR and Emissions Codes (FSM)]]
