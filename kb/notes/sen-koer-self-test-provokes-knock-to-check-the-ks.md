---
title: "The KOER self-test deliberately advances timing to provoke knock and confirm the knock sensor responds"
kind: troubleshooting
source: "[[sources/sen-knock-sensor|Knock Sensor (KS) — Description, Operation, and DTC (FSM)]]"
related:
  - "[[notes/sen-knock-sensor-is-self-generating-and-tuned-to-5-6khz|The knock sensor generates its own voltage by resonating at engine-knock frequency, so it needs only a ground]]"
tags:
  - knock-sensor
  - ignition
  - troubleshooting
  - self-test
---

A passive, self-generating sensor like the knock sensor is hard to test at idle because it only
produces a signal when there's actually knock to detect. Ford's EEC-IV solves this during the
Key On Engine Running (KOER) self-test: in the dynamic-response (snap-throttle) portion the PCM
deliberately advances ignition timing to induce a small amount of detonation, then watches for a
corresponding output from the KS.

If no KS signal arrives during that provoked-knock window, the PCM sets DTC **25/225**. So this
code is really saying "I made the engine knock and the sensor stayed silent" — which can mean a
dead sensor, a loose sensor that isn't coupling vibration, or an open in the signal/SIG RTN
circuit.

For the `ignition` system, the takeaway is that 25/225 should be read in context: confirm the
KOER test actually completed the snap-throttle step, then check the sensor's mounting torque and
wiring before condemning the sensor itself.

## Related Concepts

- [[notes/sen-knock-sensor-is-self-generating-and-tuned-to-5-6khz|The knock sensor generates its own voltage by resonating at engine-knock frequency, so it needs only a ground]]
- [[notes/dtc-225-confirms-the-knock-sensor-during-the-koer-dynamic-test|DTC 225 means knock was not sensed during the KOER dynamic response test, a knock-sensor check]]
- [[notes/eec-knock-sensor-is-self-generating-and-tuned-to-knock-frequency|The knock sensor is a self-generating piezo element tuned to the 5-6 kHz knock frequency]]
- [[notes/dtc-self-test-runs-in-koeo-and-koer-modes|The EEC self-test runs in two modes — Key On Engine Off and Key On Engine Running — and each finds different faults]]

## Source

- [[sources/sen-knock-sensor|Knock Sensor (KS) — Description, Operation, and DTC (FSM)]]
