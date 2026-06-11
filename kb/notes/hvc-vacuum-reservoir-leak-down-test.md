---
title: "Leak-test the HVAC vacuum reservoir: under 0.5 in Hg loss in 60 seconds"
kind: procedure
source: "[[sources/hvc-vacuum-control-system|HVAC Vacuum Control System — Reservoir and Harness (FSM)]]"
related:
  - "[[notes/hvc-vacuum-reservoir-holds-air-door-position-under-load|The vacuum reservoir keeps the air doors in position when manifold vacuum drops]]"
tags: [hvac, vacuum-reservoir, test, spec]
---

To check the HVAC vacuum reservoir on the 1994 F-150 (inventory id `hvac`), apply an initial
vacuum of 15 to 20 in Hg to it. Watch the gauge: the vacuum loss must not exceed 0.5 in Hg in
60 seconds. If the reservoir bleeds down faster than that, replace it.

This simple bench test isolates the reservoir itself from the rest of the vacuum control
plumbing — useful when mode doors drift toward defrost under load and you need to know whether
the reservoir is holding its stored charge.

## Related Concepts

- [[notes/hvc-vacuum-reservoir-holds-air-door-position-under-load|The vacuum reservoir keeps the air doors in position when manifold vacuum drops]]
- [[notes/hvc-evacuate-to-28-29-in-hg-adjusting-for-altitude|Evacuate the A/C system to 28–29.5 in Hg at sea level, minus 1 in Hg per 1000 ft of altitude]]

## Source

- [[sources/hvc-vacuum-control-system|HVAC Vacuum Control System — Reservoir and Harness (FSM)]]
