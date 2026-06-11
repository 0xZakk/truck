---
title: "Low master-cylinder fluid grounds the warning switch, disabling ABS and lighting the indicator"
kind: how-it-works
source: "[[sources/brk-master-cylinder|Brake Master Cylinder and Reservoir (FSM)]]"
related:
  - "[[notes/brk-dual-split-hydraulic-system-keeps-half-the-brakes-after-a-leak|The dual split hydraulic system keeps half the brakes working after a single-circuit leak]]"
  - "[[notes/brk-fluid-falling-as-pads-wear-is-normal-but-frequent-topups-mean-a-leak|A reservoir level that falls as pads wear is normal, but frequent top-ups mean a leak]]"
tags: [brakes, fluid-level-sensor, master-cylinder, abs, warning-light]
---

The master cylinder reservoir on the 1994 F-150 carries an integral Low Fluid Level Warning Switch made of a float-and-magnet assembly and a reed switch. It is part of the reservoir and is not separately serviceable. When fluid drops low enough, the magnet on the float closes the reed switch and provides a path to ground through the dual brake warning switch.

That ground does two things: it illuminates the anti-lock brake (REAR ABS) indicator and disables the anti-lock brake system, and the low level also lights the red BRAKE warning lamp. So in the `brakes` system a glowing ABS light can be a fluid-level symptom, not necessarily an electronic ABS fault — checking the reservoir level is a cheap first step. Correct level is between the MAX line and 4 mm (0.16 in) below it.

> "When a low fluid level condition occurs, a path to ground is provided through the dual brake warning switch to disable the Antilock brake system and illuminate the Antilock brake indicator."

## Related Concepts

- [[notes/brk-dual-split-hydraulic-system-keeps-half-the-brakes-after-a-leak|The dual split hydraulic system keeps half the brakes working after a single-circuit leak]]
- [[notes/brk-fluid-falling-as-pads-wear-is-normal-but-frequent-topups-mean-a-leak|A reservoir level that falls as pads wear is normal, but frequent top-ups mean a leak]]
- [[notes/brk-proportioning-valve-limits-rear-pressure-to-prevent-rear-lockup|The integral proportioning valve limits rear-circuit pressure to prevent rear-wheel lockup]]

## Source

- [[sources/brk-master-cylinder|Brake Master Cylinder and Reservoir (FSM)]]
