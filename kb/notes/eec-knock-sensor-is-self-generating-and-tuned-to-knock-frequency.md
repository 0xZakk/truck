---
title: "The knock sensor is a self-generating piezo element tuned to the 5-6 kHz knock frequency"
kind: how-it-works
source: "[[sources/eec-knock-sensor|Knock Sensor (KS) — Operation, DTC, and Specs (FSM)]]"
related:
  - "[[notes/eec-base-timing-is-10-btdc-set-with-spout-disconnected|Base ignition timing is 10 deg BTDC, set with the SPOUT connector disconnected]]"
tags:
  - knock-sensor
  - detonation
  - piezoelectric
  - ignition
---

The Knock Sensor (KS) is a thin piezoelectric ceramic disc bonded to a metal diaphragm,
deliberately tuned to resonate at about the same frequency as engine knock (5-6 kHz). When
detonation occurs, the disc resonates and converts that vibration into a voltage of equal
frequency, which it sends directly to the PCM. The sensor is self-generating — it needs no power
supply, and the PCM only provides its ground through SIG RTN.

The PCM uses the KS input to optimize (retard) ignition timing, reducing spark detonation and
minimizing NOx. The single related code is DTC 25/225, set when the PCM senses no KS signal
during the dynamic-response (snap-throttle) part of the KOER self-test — during which the PCM
deliberately advances timing to provoke knock and confirm the sensor responds. This protects the
`ignition` and `engine` systems from detonation damage.

## Related Concepts

- [[notes/eec-base-timing-is-10-btdc-set-with-spout-disconnected|Base ignition timing is 10 deg BTDC, set with the SPOUT connector disconnected]]
- [[notes/sen-knock-sensor-is-self-generating-and-tuned-to-5-6khz|The knock sensor generates its own voltage by resonating at engine-knock frequency, so it needs only a ground]]
- [[notes/sen-koer-self-test-provokes-knock-to-check-the-ks|The KOER self-test deliberately advances timing to provoke knock and confirm the knock sensor responds]]
- [[notes/dtc-225-confirms-the-knock-sensor-during-the-koer-dynamic-test|DTC 225 means knock was not sensed during the KOER dynamic response test, a knock-sensor check]]

## Source

- [[sources/eec-knock-sensor|Knock Sensor (KS) — Operation, DTC, and Specs (FSM)]]
