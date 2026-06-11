---
title: "The knock sensor generates its own voltage by resonating at engine-knock frequency, so it needs only a ground"
kind: how-it-works
source: "[[sources/sen-knock-sensor|Knock Sensor (KS) — Description, Operation, and DTC (FSM)]]"
related:
  - "[[notes/sen-koer-self-test-provokes-knock-to-check-the-ks|The KOER self-test deliberately advances timing to provoke knock and confirm the knock sensor responds]]"
tags:
  - knock-sensor
  - ignition
  - detonation
---

The knock sensor is a piezoelectric device: a thin ceramic disc bonded to a metal diaphragm
that produces a voltage when mechanically stressed. It is deliberately tuned to resonate at
about 5–6 kHz, the frequency band of engine detonation. When the engine pings, the vibration
drives the disc into resonance and it outputs a voltage at the same frequency, which goes
straight to the PCM.

Because it makes its own signal, the sensor needs no power supply — the PCM supplies only the
SIG RTN ground, and the device has a simple two-pin connector. The PCM reacts to KS activity by
retarding ignition timing until the knock stops, which protects the `ignition` system's tune
from detonation damage while still allowing as much advance as the fuel and conditions permit.

A practical implication: torque matters. A knock sensor that is loose or not torqued to the
block can't couple vibration into the disc, so it under-reports knock. Mounting integrity is as
much a part of "is it working" as the electrical circuit.

## Related Concepts

- [[notes/sen-koer-self-test-provokes-knock-to-check-the-ks|The KOER self-test deliberately advances timing to provoke knock and confirm the knock sensor responds]]
- [[notes/eec-knock-sensor-is-self-generating-and-tuned-to-knock-frequency|The knock sensor is a self-generating piezo element tuned to the 5-6 kHz knock frequency]]
- [[notes/dtc-225-confirms-the-knock-sensor-during-the-koer-dynamic-test|DTC 225 means knock was not sensed during the KOER dynamic response test, a knock-sensor check]]

## Source

- [[sources/sen-knock-sensor|Knock Sensor (KS) — Description, Operation, and DTC (FSM)]]
