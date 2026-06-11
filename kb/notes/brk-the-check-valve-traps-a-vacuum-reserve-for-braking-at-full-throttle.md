---
title: "The booster check valve traps a vacuum reserve for braking at full throttle"
kind: how-it-works
source: "[[sources/brk-power-brake-booster|Vacuum Power Brake Booster and Check Valve (FSM)]]"
related:
  - "[[notes/brk-vacuum-booster-multiplies-pedal-effort-and-brakes-still-work-manually-if-vacuum-fails|The vacuum booster multiplies pedal effort, and the brakes still work manually if vacuum fails]]"
  - "[[notes/brk-test-the-booster-by-watching-the-pedal-sink-when-the-engine-starts|Test the power brake booster by watching the pedal sink when the engine starts]]"
tags: [brakes, check-valve, power-brake-booster, vacuum]
---

The power brake booster check valve on the 1994 F-150 is a one-way valve between the intake manifold and the booster. It lets manifold vacuum flow into the booster, then prevents that vacuum from escaping if manifold vacuum is lost — which happens during sustained full-throttle operation, when the throttle is wide open and manifold vacuum collapses toward zero.

By trapping the stored vacuum, the check valve preserves a reserve of brake assist for the moments you most need it: braking hard right after a full-throttle acceleration. It is one of the only three serviceable booster parts, and the FSM's diagnostic logic uses it directly — a hard, no-assist pedal on the reserve test calls for replacing the check valve. In the `brakes` system, a leaking check valve quietly bleeds away assist between engine vacuum pulses.

> "The function of the power brake booster check valve is to allow manifold vacuum to enter the power brake booster and prevent the escape of vacuum in case manifold vacuum is lost during sustained full throttle operation."

## Related Concepts

- [[notes/brk-vacuum-booster-multiplies-pedal-effort-and-brakes-still-work-manually-if-vacuum-fails|The vacuum booster multiplies pedal effort, and the brakes still work manually if vacuum fails]]
- [[notes/brk-test-the-booster-by-watching-the-pedal-sink-when-the-engine-starts|Test the power brake booster by watching the pedal sink when the engine starts]]

## Source

- [[sources/brk-power-brake-booster|Vacuum Power Brake Booster and Check Valve (FSM)]]
