---
title: "RABS prevents only rear-wheel lockup, modulating rear pressure above ~5 mph"
kind: how-it-works
source: "[[sources/brk-rabs-antilock|Rear Anti-Lock Brake System (RABS) (FSM)]]"
related:
  - "[[notes/brk-rabs-uses-one-rear-axle-speed-sensor-with-isolation-and-dump-valves|RABS uses one rear-axle speed sensor and isolation/dump valves to modulate pressure]]"
  - "[[notes/brk-proportioning-valve-limits-rear-pressure-to-prevent-rear-lockup|The integral proportioning valve limits rear-circuit pressure to prevent rear-wheel lockup]]"
tags: [brakes, abs, rabs, rear-brakes, how-it-works]
---

The 1994 F-150 uses Rear Anti-Lock Brake System II (RABS II), which controls only the rear wheels — there is no front-wheel ABS on this truck. Its job is to prevent rear-wheel lockup during braking, which on a light-tailed pickup would cause loss of directional stability (the rear stepping out). The system becomes active only at vehicle speeds above approximately 5 mph; below that it does nothing.

RABS exists because a 2WD pickup's rear axle is lightly loaded and locks easily, especially when the bed is empty. The mechanical proportioning valve already biases pressure away from the rear, and RABS adds active electronic modulation on top of that. In the `brakes` system, then, rear-lockup prevention is handled in two layers: the always-on proportioning valve and the electronically modulated RABS valve.

> "The Rear Antilock Brake System (RABS) is used to release brake hydraulic pressure to the rear wheels to prevent rear wheel lock-up."

## Related Concepts

- [[notes/brk-rabs-uses-one-rear-axle-speed-sensor-with-isolation-and-dump-valves|RABS uses one rear-axle speed sensor and isolation/dump valves to modulate pressure]]
- [[notes/brk-proportioning-valve-limits-rear-pressure-to-prevent-rear-lockup|The integral proportioning valve limits rear-circuit pressure to prevent rear-wheel lockup]]
- [[notes/brk-dual-split-hydraulic-system-keeps-half-the-brakes-after-a-leak|The dual split hydraulic system keeps half the brakes working after a single-circuit leak]]

## Source

- [[sources/brk-rabs-antilock|Rear Anti-Lock Brake System (RABS) (FSM)]]
