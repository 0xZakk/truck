---
title: "DTCs 211 and 226 point at the PIP and IDM crank-timing signals the PCM needs to fire the ignition"
kind: troubleshooting
source: "[[sources/dtc-ignition-codes|EEC DTCs 211-244 — Ignition and Spark Codes (FSM)]]"
related:
  - "[[notes/dtc-coil-primary-failure-codes-defer-to-the-ignition-system-section|Coil-primary-failure DTCs are detected by the PCM but defer to the Ignition System section to diagnose]]"
  - "[[notes/dtc-225-confirms-the-knock-sensor-during-the-koer-dynamic-test|DTC 225 means knock was not sensed during the KOER dynamic response test, a knock-sensor check]]"
tags:
  - dtc
  - ignition
  - profile-ignition-pickup
  - ignition-diagnostic-monitor
  - troubleshooting
---

The EEC needs to know crankshaft position and timing to schedule spark, and two signals carry
that information: the **Profile Ignition Pickup (PIP)**, which reports crank position, and the
**Ignition Diagnostic Monitor (IDM)**, which feeds the PCM back the actual firing events. DTC
211 is a PIP circuit failure, routing to NA1 (Erratic Ignition). DTC 226 means the IDM signal
was not received at all (NA/NC2), and DTC 212 means the PCM lost its IDM input or the spark
output (SPOUT) circuit is grounded (NA2).

These are among the most serious ignition codes because the PIP is the master timing
reference — lose it and the engine will not run, or runs erratically. DTC 213 (spark output
circuit open) and 219 (spark timing defaulted to 10 degrees with the spark output open) show
what the PCM does when it cannot command timing: it falls back to a fixed 10-degree default.
Cylinder identification faults (214, 244) round out the timing-signal codes, since the PCM
also needs to know which cylinder is which for sequential operation.

On this truck these codes are the `ignition` system's first-look diagnostics; a PIP or IDM
fault explains no-start and stumble complaints the temperature and fuel codes cannot.

## Related Concepts

- [[notes/dtc-coil-primary-failure-codes-defer-to-the-ignition-system-section|Coil-primary-failure DTCs are detected by the PCM but defer to the Ignition System section to diagnose]]
- [[notes/dtc-225-confirms-the-knock-sensor-during-the-koer-dynamic-test|DTC 225 means knock was not sensed during the KOER dynamic response test, a knock-sensor check]]
- [[notes/sen-narrow-1-shutter-gives-cylinder-identification|A narrower number-1 shutter creates a signature PIP pulse that tells the PCM which cylinder is which]]
- [[notes/sen-pip-is-a-hall-switch-driven-by-a-6-vane-shutter|The PIP signal is a 0–12 V square wave a distributor Hall switch makes as a 6-vane shutter passes through it]]

## Source

- [[sources/dtc-ignition-codes|EEC DTCs 211-244 — Ignition and Spark Codes (FSM)]]
