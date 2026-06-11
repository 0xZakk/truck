---
title: "The knock sensor is a self-generating piezo element tuned to the 5-6 kHz knock frequency"
kind: how-it-works
source: "[[sources/eec-knock-sensor|Knock Sensor (KS) — Operation, DTC, and Specs (FSM)]]"
related: []
tags:
  - knock-sensor
  - detonation
  - piezoelectric
  - ignition
---

The Knock Sensor (KS) is a piezoelectric device: a thin piezoelectric ceramic disc bonded to a
metal diaphragm that produces a voltage when mechanically stressed. It is deliberately tuned to
resonate at about the same frequency as engine knock (5-6 kHz), the frequency band of engine
detonation. When detonation occurs, the vibration drives the disc into resonance and it outputs a
voltage of equal frequency, which it sends directly to the PCM. The sensor is self-generating — it
needs no power supply, so the PCM only provides its ground through SIG RTN, and the device has a
simple two-pin connector.

The PCM uses the KS input to optimize (retard) ignition timing until knock stops, reducing spark
detonation and minimizing NOx while still allowing as much advance as the fuel and conditions
permit. This protects the `ignition` and `engine` systems from detonation damage. The single
related code is DTC 25/225, set when the PCM senses no KS signal during the dynamic-response
(snap-throttle) part of the KOER self-test — during which the PCM deliberately advances timing to
provoke knock and confirm the sensor responds.

A practical implication: torque matters. A knock sensor that is loose or not torqued to the block
can't couple vibration into the disc, so it under-reports knock. Mounting integrity is as much a
part of "is it working" as the electrical circuit.

## Related Concepts
- [[notes/sen-koer-self-test-provokes-knock-to-check-the-ks|The KOER self-test deliberately advances timing to provoke knock and confirm the knock sensor responds]]
- [[notes/dtc-225-confirms-the-knock-sensor-during-the-koer-dynamic-test|DTC 225 means knock was not sensed during the KOER dynamic response test, a knock-sensor check]]

## Source

- [[sources/eec-knock-sensor|Knock Sensor (KS) — Operation, DTC, and Specs (FSM)]]
- [[sources/sen-knock-sensor|Knock Sensor (KS) — Description, Operation, and DTC (FSM)]]
