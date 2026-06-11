---
title: "Ignition system"
kind: map
system_id: ignition
tags:
  - ignition
---

Distributor, coil, plugs, wires, EEC control.

This map is the entry point for the **ignition system** system of the truck. As notes are added
(via `kb-process`), link the load-bearing ones below.

## Key Notes

- [[notes/sen-narrow-1-shutter-gives-cylinder-identification|A narrower number-1 shutter creates a signature PIP pulse that tells the PCM which cylinder is which]]
- [[notes/eec-clear-kam-and-drive-10-miles-after-replacing-an-eec-part|After replacing an EEC component, clear Keep Alive Memory and drive ~10 miles to relearn]]  ·  _procedure_
- [[notes/eec-base-timing-is-10-btdc-set-with-spout-disconnected|Base ignition timing is 10 deg BTDC, set with the SPOUT connector disconnected]]  ·  _procedure_
- [[notes/eec-compression-is-acceptable-if-lowest-cylinder-is-within-25-percent|Compression is acceptable if the lowest cylinder reads within 25% of the highest]]  ·  _procedure_
- [[notes/dtc-111-is-system-pass-not-a-fault|DTC 111 means System Pass — the self-test found no faults]]
- [[notes/dtc-codes-may-be-shared-between-modules-so-confirm-the-source|DTC numbers may be shared between modules, so confirm which module a code came from before chasing it]]
- [[notes/eec-firing-order-is-1-5-3-6-2-4|The 4.9L I6 firing order is 1-5-3-6-2-4]]  ·  _spec_
- [[notes/dtc-self-test-runs-in-koeo-and-koer-modes|The EEC self-test runs in two modes — Key On Engine Off and Key On Engine Running — and each finds different faults]]
- [[notes/ford-300-firing-order-is-1-5-3-6-2-4|The Ford 300 inline-six firing order is 1-5-3-6-2-4]]  ·  _spec_
- [[notes/eec-map-sensor-outputs-a-frequency-and-doubles-as-a-baro-sensor|The MAP sensor outputs a frequency proportional to load and doubles as a barometric sensor]]
- [[notes/eec-pcm-learns-an-adaptive-strategy-stored-in-kam|The PCM learns an adaptive strategy in Keep Alive Memory to compensate for component wear]]
- [[notes/sen-pip-is-a-hall-switch-driven-by-a-6-vane-shutter|The PIP signal is a 0–12 V square wave a distributor Hall switch makes as a 6-vane shutter passes through it]]
- [[notes/sen-cmp-is-camshaft-driven-and-serviceable-in-the-distributor|The camshaft position / cylinder ID sensor lives inside the distributor and is camshaft-driven, so it can be serviced separately]]  ·  _spec_
- [[notes/eec-cmp-in-distributor-produces-the-pip-signal-for-spark-and-injection|The distributor-mounted CMP sensor produces the PIP signal that times both spark and injection]]
- [[notes/sen-knock-sensor-is-self-generating-and-tuned-to-5-6khz|The knock sensor generates its own voltage by resonating at engine-knock frequency, so it needs only a ground]]
- [[notes/eec-knock-sensor-is-self-generating-and-tuned-to-knock-frequency|The knock sensor is a self-generating piezo element tuned to the 5-6 kHz knock frequency]]

## Common Issues

- [[notes/dtc-hard-codes-vs-memory-codes-mean-present-vs-stored|A hard code is a fault present during the test, while a memory code was stored from earlier driving]]  ·  _troubleshooting_
- [[notes/dtc-coil-primary-failure-codes-defer-to-the-ignition-system-section|Coil-primary-failure DTCs are detected by the PCM but defer to the Ignition System section to diagnose]]  ·  _troubleshooting_
- [[notes/dtc-225-confirms-the-knock-sensor-during-the-koer-dynamic-test|DTC 225 means knock was not sensed during the KOER dynamic response test, a knock-sensor check]]  ·  _troubleshooting_
- [[notes/dtc-211-and-226-point-to-the-pip-and-idm-crank-signals|DTCs 211 and 226 point at the PIP and IDM crank-timing signals the PCM needs to fire the ignition]]  ·  _troubleshooting_
- [[notes/dtc-511-and-513-call-for-pcm-replacement|DTCs 511 and 513 are internal PCM failures that the chart resolves by replacing the PCM]]  ·  _troubleshooting_
- [[notes/sen-koer-self-test-provokes-knock-to-check-the-ks|The KOER self-test deliberately advances timing to provoke knock and confirm the knock sensor responds]]  ·  _troubleshooting_

## Sources

- [[sources/dtc-idle-speed-input-codes|EEC DTCs 411-539 — Idle Speed, Vehicle Speed, and Switch Input Codes (FSM)]]
- [[sources/dtc-ignition-codes|EEC DTCs 211-244 — Ignition and Spark Codes (FSM)]]
- [[sources/dtc-self-test-overview|EEC Diagnostic Trouble Codes — Self-Test Overview and Code Conventions (FSM)]]
- [[sources/eec-camshaft-position-sensor|Camshaft Position (CMP) Sensor and PIP Signal — Operation and Specs (FSM)]]
- [[sources/eec-engine-control-module|Engine Control Module (PCM / EEC-IV) — Description, Operation, and Reset (FSM)]]
- [[sources/eec-knock-sensor|Knock Sensor (KS) — Operation, DTC, and Specs (FSM)]]
- [[sources/eec-map-sensor|Manifold Absolute Pressure (MAP) Sensor — Operation, DTCs, and Range (FSM)]]
- [[sources/eec-tune-up-and-engine-checks|Tune-up and Engine Performance Checks — Timing, Firing Order, Compression, Valve Clearance, Spark Plugs (FSM)]]
- [[sources/ford-300-inline-six-bulletproof-engine|Ford 300 Inline Six — What You Need to Know About Ford's Bulletproof Engine (4.9L)]]
- [[sources/sen-distributor-hall-effect-pip-cmp-sensor|Distributor Hall-Effect Sensor — PIP, Camshaft Position, and Cylinder Identification (FSM)]]
- [[sources/sen-knock-sensor|Knock Sensor (KS) — Description, Operation, and DTC (FSM)]]
