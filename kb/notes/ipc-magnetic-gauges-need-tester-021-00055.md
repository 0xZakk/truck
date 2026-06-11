---
title: "Magnetic dash gauges are diagnosed with tester tool 021-00055 and per-symptom pinpoint tests"
kind: procedure
source: "[[sources/ipc-oil-pressure-gauge|Oil Pressure Gauge — Description, Operation and Testing (FSM)]]"
related:
  - "[[notes/ipc-dash-gauges-share-a-three-coil-magnetic-movement|The temperature, oil pressure, and fuel gauges all use the same three-coil magnetic movement with no voltage regulator]]"
  - "[[notes/ipc-fuel-sender-resistance-spans-22-5-to-145-ohms|The fuel sender resistance spans 22.5 ohms empty to 145 ohms full]]"
tags:
  - gauges
  - troubleshooting
  - temperature-gauge
  - oil-pressure-gauge
---

The FSM's general diagnostic instruction for the magnetic gauges (temperature and oil
pressure) is the same: use gauge tester tool No. 021-00055 (or equivalent) and then follow
the pinpoint test that matches the symptom. The tester substitutes a known resistance for
the sender so you can tell whether a wrong or dead reading is the gauge or the sender/wiring.

Each gauge's symptoms split into two branches — "Inaccurate" and "Inoperative" — each with
its own pinpoint test chart. "Inoperative" means no reading at all (think open circuit, dead
gauge, or lost power/ground); "Inaccurate" means the needle moves but reads wrong (think
sender out of spec, resistance/ground issue, or a marginal gauge). Picking the right branch
first keeps the diagnosis focused. The fuel gauge follows the same pattern with a "No fuel
level indication" chart plus combined Fuel Gauge & Sender symptom charts.

This procedure lives in the `interior` / `electrical-body` instrument-cluster domain.

## Related Concepts

- [[notes/ipc-dash-gauges-share-a-three-coil-magnetic-movement|The temperature, oil pressure, and fuel gauges all use the same three-coil magnetic movement with no voltage regulator]]
- [[notes/ipc-fuel-sender-resistance-spans-22-5-to-145-ohms|The fuel sender resistance spans 22.5 ohms empty to 145 ohms full]]

## Source

- [[sources/ipc-oil-pressure-gauge|Oil Pressure Gauge — Description, Operation and Testing (FSM)]]
