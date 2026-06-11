---
title: "The fuel sender resistance spans 22.5 ohms empty to 145 ohms full"
kind: spec
source: "[[sources/ipc-fuel-gauge-and-sender|Fuel Gauge and Fuel Gauge Sender — Description, Operation and Testing (FSM)]]"
related:
  - "[[notes/ipc-dash-gauges-share-a-three-coil-magnetic-movement|The temperature, oil pressure, and fuel gauges all use the same three-coil magnetic movement with no voltage regulator]]"
  - "[[notes/ipc-magnetic-gauges-need-tester-021-00055|Magnetic dash gauges are diagnosed with tester tool 021-00055 and per-symptom pinpoint tests]]"
tags:
  - fuel-gauge-sender
  - fuel-gauge
  - spec
---

The 1994 F-150 fuel sender is a float-driven variable resistor with two FSM-specified
endpoints: 22.5 ohms when the tank is LOW (empty) and 145 ohms when the tank is HIGH (full).
The instrument-panel fuel gauge is a magnetic indicator that operates on battery voltage and
sets pointer position from this resistance.

These two numbers are the practical anchors for diagnosing fuel-level complaints. Measuring
the sender (or substituting a known resistance) and watching the gauge tells you which half
is at fault: a sender stuck outside the 22.5-145 ohm window points to the sender or its
float, while a sender that ohms correctly but a gauge that does not track points to the gauge
or wiring. Note the direction — low resistance reads empty, high resistance reads full — so
an open circuit (effectively infinite resistance) and a short behave very differently on the
needle.

This belongs to the `interior` instrument-cluster and `electrical-body` wiring domains.

## Related Concepts

- [[notes/ipc-dash-gauges-share-a-three-coil-magnetic-movement|The temperature, oil pressure, and fuel gauges all use the same three-coil magnetic movement with no voltage regulator]]
- [[notes/ipc-magnetic-gauges-need-tester-021-00055|Magnetic dash gauges are diagnosed with tester tool 021-00055 and per-symptom pinpoint tests]]

## Source

- [[sources/ipc-fuel-gauge-and-sender|Fuel Gauge and Fuel Gauge Sender — Description, Operation and Testing (FSM)]]
