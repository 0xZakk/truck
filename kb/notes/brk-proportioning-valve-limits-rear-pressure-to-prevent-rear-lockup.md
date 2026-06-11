---
title: "The integral proportioning valve limits rear-circuit pressure to prevent rear-wheel lockup"
kind: how-it-works
source: "[[sources/brk-master-cylinder|Brake Master Cylinder and Reservoir (FSM)]]"
related:
  - "[[notes/brk-dual-split-hydraulic-system-keeps-half-the-brakes-after-a-leak|The dual split hydraulic system keeps half the brakes working after a single-circuit leak]]"
  - "[[notes/brk-rabs-modulates-only-the-rear-wheels-above-5-mph|RABS prevents only rear-wheel lockup, modulating rear pressure above ~5 mph]]"
tags: [brakes, proportioning-valve, master-cylinder, rear-brakes]
---

A proportioning valve is built into the master cylinder of the 1994 F-150 and regulates hydraulic pressure to the rear brake system. Below the valve's "split point," full pedal pressure passes straight through to the rear brakes. Above the split point, the valve begins reducing the pressure delivered to the rear, so the rear brakes get proportionally less than the fronts during hard braking.

The purpose is balance: a light-bodied pickup's rear axle unloads under hard braking, so feeding it full pressure would lock the rear wheels first. Holding rear pressure back creates a balanced front/rear braking condition that minimizes rear lock-up. The valve also has a bypass feature — if the front brake circuit fails, it allows full pressure to reach the rear system so the remaining circuit isn't crippled. This valve is the mechanical (always-on) counterpart to the electronic RABS modulation in the `brakes` system.

> "Above its split point, the brake pressure control valve begins to reduce the hydraulic pressure to the rear brakes, creating a balanced braking condition... to minimize rear wheel lock-up during hard braking."

## Related Concepts

- [[notes/brk-dual-split-hydraulic-system-keeps-half-the-brakes-after-a-leak|The dual split hydraulic system keeps half the brakes working after a single-circuit leak]]
- [[notes/brk-rabs-modulates-only-the-rear-wheels-above-5-mph|RABS prevents only rear-wheel lockup, modulating rear pressure above ~5 mph]]
- [[notes/brk-low-fluid-grounds-the-warning-switch-disabling-abs-and-lighting-the-indicator|Low master-cylinder fluid grounds the warning switch, disabling ABS and lighting the indicator]]

## Source

- [[sources/brk-master-cylinder|Brake Master Cylinder and Reservoir (FSM)]]
