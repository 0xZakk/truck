---
title: "Test the power brake booster by watching the pedal sink when the engine starts"
kind: procedure
source: "[[sources/brk-power-brake-booster|Vacuum Power Brake Booster and Check Valve (FSM)]]"
related:
  - "[[notes/brk-vacuum-booster-multiplies-pedal-effort-and-brakes-still-work-manually-if-vacuum-fails|The vacuum booster multiplies pedal effort, and the brakes still work manually if vacuum fails]]"
  - "[[notes/brk-the-check-valve-traps-a-vacuum-reserve-for-braking-at-full-throttle|The booster check valve traps a vacuum reserve for braking at full throttle]]"
tags: [brakes, power-brake-booster, diagnosis, procedure]
---

The FSM's basic booster test on the 1994 F-150: with the transmission in NEUTRAL, stop the engine and set the parking brake, then pump the brake pedal several times to exhaust all stored vacuum. Hold the pedal down and start the engine — if the booster is working, the pedal will sink downward under constant foot pressure as vacuum returns. If the pedal does not move, the booster system is not functioning.

A reserve/functional test follows: run the engine ~10 seconds at fast idle, stop it, let the vehicle sit 10 minutes, then apply the pedal with about 89 N (20 lb). Pedal feel should match the engine-running feel. A hard pedal (no power assist) means replace the check valve and retest; a spongy pedal means air in the hydraulics — bleed the system. The functional check also confirms manifold vacuum is actually present at the check valve end of the booster hose at idle. This sequence separates booster, check-valve, and air-in-lines causes in the `brakes` system.

> "Apply brake pedal and hold it in the applied position. Start engine. If vacuum system is operating, brake pedal will tend to move downward under constant foot pressure. If no motion is felt, replace the vacuum booster."

## Related Concepts

- [[notes/brk-vacuum-booster-multiplies-pedal-effort-and-brakes-still-work-manually-if-vacuum-fails|The vacuum booster multiplies pedal effort, and the brakes still work manually if vacuum fails]]
- [[notes/brk-the-check-valve-traps-a-vacuum-reserve-for-braking-at-full-throttle|The booster check valve traps a vacuum reserve for braking at full throttle]]

## Source

- [[sources/brk-power-brake-booster|Vacuum Power Brake Booster and Check Valve (FSM)]]
