---
title: "DTC 225 means knock was not sensed during the KOER dynamic response test, a knock-sensor check"
kind: troubleshooting
source: "[[sources/dtc-ignition-codes|EEC DTCs 211-244 — Ignition and Spark Codes (FSM)]]"
related:
  - "[[notes/sen-koer-self-test-provokes-knock-to-check-the-ks|The KOER self-test deliberately advances timing to provoke knock and confirm the knock sensor responds]]"
  - "[[notes/dtc-self-test-runs-in-koeo-and-koer-modes|The EEC self-test runs in two modes — Key On Engine Off and Key On Engine Running — and each finds different faults]]"
tags:
  - dtc
  - knock-sensor
  - ignition
  - koer
  - troubleshooting
---

DTC 225 is set when "knock not sensed during dynamic response test KOER" — during the running
self-test the PCM deliberately advances spark to induce detonation and listens for the knock
sensor to report it. If the PCM advances timing and hears nothing, it concludes the knock
sensor or its circuit is not responding and sets 225, routing to pinpoint test DG1.

This is a clear example of why the KOER mode exists: a knock sensor fault is invisible with
the engine off because there is nothing to knock. Only a running, loaded engine can produce
the vibration the sensor is tuned to detect, so the test has to provoke the condition rather
than just measure a resting voltage. A 225 does not necessarily mean the engine is detonating
in normal driving — it means the diagnostic stimulus did not produce a sensor response.

On the truck's `ignition` system, 225 sits alongside the knock-sensor description: the sensor
is self-generating and tuned to engine-knock frequency, so it needs only a good ground and a
clean signal path to pass this test.

## Related Concepts

- [[notes/sen-koer-self-test-provokes-knock-to-check-the-ks|The KOER self-test deliberately advances timing to provoke knock and confirm the knock sensor responds]]
- [[notes/dtc-self-test-runs-in-koeo-and-koer-modes|The EEC self-test runs in two modes — Key On Engine Off and Key On Engine Running — and each finds different faults]]
- [[notes/eec-knock-sensor-is-self-generating-and-tuned-to-knock-frequency|The knock sensor is a self-generating piezo element tuned to the 5-6 kHz knock frequency]]
- [[notes/sen-knock-sensor-is-self-generating-and-tuned-to-5-6khz|The knock sensor generates its own voltage by resonating at engine-knock frequency, so it needs only a ground]]

## Source

- [[sources/dtc-ignition-codes|EEC DTCs 211-244 — Ignition and Spark Codes (FSM)]]
