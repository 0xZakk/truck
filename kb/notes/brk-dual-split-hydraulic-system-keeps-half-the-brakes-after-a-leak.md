---
title: "The dual split hydraulic system keeps half the brakes working after a single-circuit leak"
kind: how-it-works
source: "[[sources/brk-master-cylinder|Brake Master Cylinder and Reservoir (FSM)]]"
related:
  - "[[notes/brk-proportioning-valve-limits-rear-pressure-to-prevent-rear-lockup|The integral proportioning valve limits rear-circuit pressure to prevent rear-wheel lockup]]"
  - "[[notes/brk-low-fluid-grounds-the-warning-switch-disabling-abs-and-lighting-the-indicator|Low master-cylinder fluid grounds the warning switch, disabling ABS and lighting the indicator]]"
tags: [brakes, master-cylinder, hydraulic-system, dual-circuit]
---

The 1994 F-150's brakes are a dual (split) hydraulic system driven by a tandem master cylinder (2140) with two pistons in one bore. The primary piston feeds the front circuit through the primary outlet port (nearest the dash panel); the secondary piston feeds the rear circuit through the secondary outlet port. In normal braking both pistons move together and pressurize both circuits at once.

The point of the split is fault tolerance. Because the two circuits are hydraulically independent, a leak or failure in one circuit still leaves the other able to generate stopping force — you keep either the fronts or the rears. This is also why the FSM insists on bleeding the primary and secondary systems separately. The truck inventory system `brakes` therefore has two distinct hydraulic legs rather than one shared line.

> "Rear wheel brakes - are connected to the secondary outlet port... Front wheel brakes - are connected to the primary outlet port (nearest the dash panel)."

## Related Concepts

- [[notes/brk-proportioning-valve-limits-rear-pressure-to-prevent-rear-lockup|The integral proportioning valve limits rear-circuit pressure to prevent rear-wheel lockup]]
- [[notes/brk-low-fluid-grounds-the-warning-switch-disabling-abs-and-lighting-the-indicator|Low master-cylinder fluid grounds the warning switch, disabling ABS and lighting the indicator]]
- [[notes/brk-front-caliper-is-a-pin-sliding-single-piston-design-that-reacts-torque-into-the-spindle|The front caliper is a pin-sliding single-piston design that reacts brake torque into the spindle]]
- [[notes/brk-rabs-modulates-only-the-rear-wheels-above-5-mph|RABS prevents only rear-wheel lockup, modulating rear pressure above ~5 mph]]

## Source

- [[sources/brk-master-cylinder|Brake Master Cylinder and Reservoir (FSM)]]
