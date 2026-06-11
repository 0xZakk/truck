---
title: "The temperature, oil pressure, and fuel gauges all use the same three-coil magnetic movement with no voltage regulator"
kind: how-it-works
source: "[[sources/ipc-magnetic-gauge-movement|Magnetic Gauge Movement / Instrument Cluster — Description, Operation and Specifications (FSM)]]"
related:
  - "[[notes/ipc-fuel-sender-resistance-spans-22-5-to-145-ohms|The fuel sender resistance spans 22.5 ohms empty to 145 ohms full]]"
  - "[[notes/ipc-magnetic-gauges-need-tester-021-00055|Magnetic dash gauges are diagnosed with tester tool 021-00055 and per-symptom pinpoint tests]]"
tags:
  - gauges
  - magnetic-gauge
  - instrument-cluster
---

On the 1994 F-150 the temperature, oil pressure, and fuel gauges are not three unrelated
designs — they share one "magnetic" movement. It has three primary coils, one wound at a
90-degree angle to the other two. The coils create a magnetic field whose direction changes
with the resistance of the sender connected between two of them, and a magnet on the
pointer shaft simply rotates to line up with that field. Whatever the sender's resistance
is, that is where the needle sits.

The important consequence is that this gauge system uses NO instrument voltage regulator
(IVR). Many older Ford clusters used a pulsing IVR to feed thermal gauges a stable average
voltage; this magnetic system does not, because pointer position depends on field direction
(a ratio of currents) rather than on absolute supply voltage. The gauges also need no
adjustment, calibration, or maintenance. Recognizing the shared movement means a fault that
affects all gauges together points to common power/ground, while a single dead gauge points
to that gauge's sender or wiring.

This ties into the truck inventory systems `electrical-body` and `interior`, since the
movement is part of the instrument cluster.

## Related Concepts

- [[notes/ipc-fuel-sender-resistance-spans-22-5-to-145-ohms|The fuel sender resistance spans 22.5 ohms empty to 145 ohms full]]
- [[notes/ipc-magnetic-gauges-need-tester-021-00055|Magnetic dash gauges are diagnosed with tester tool 021-00055 and per-symptom pinpoint tests]]

## Source

- [[sources/ipc-magnetic-gauge-movement|Magnetic Gauge Movement / Instrument Cluster — Description, Operation and Specifications (FSM)]]
