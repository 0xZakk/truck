---
title: "The brake bleed sequence is RR, LR, ABS valve, RF, LF, and only an HCU replacement needs the bleeder box"
kind: procedure
source: "[[sources/brk-bleeding|Brake Bleeding (FSM)]]"
related:
  - "[[notes/brk-dual-split-hydraulic-system-keeps-half-the-brakes-after-a-leak|The dual split hydraulic system keeps half the brakes working after a single-circuit leak]]"
  - "[[notes/brk-rabs-uses-one-rear-axle-speed-sensor-with-isolation-and-dump-valves|RABS uses one rear-axle speed sensor and isolation/dump valves to modulate pressure]]"
tags: [brakes, bleeding, abs, procedure]
---

The FSM bleed order for the 1994 F-150 is RR, LR, ABS valve, RF, LF — rears first, then the RABS valve, then fronts. The primary and secondary systems are bled separately, longest line first on each, the reservoir is never allowed to run dry, and drained fluid is never reused. The master cylinder is bled first (loosen its line nuts, slow pedal strokes to push air out at the fittings, tighten with the pedal held down). Each wheel: pump, hold the pedal firmly, open the bleeder until the pedal fades, close it, and repeat until fluid flows continuously with no air.

Afterward, fill the reservoir to 1/4 inch from the top and centralize the pressure differential valve (ignition ACC/ON, press the pedal so the piston centers and the warning light goes out, ignition OFF), then road test for a firm pedal. The ABS-specific bleed using the Antilock Brake Adapter bleeder box (T90P-50-ALA) and jumper cable (T93T-50-ALA) is required only if the Hydraulic Control Unit has been replaced; for ordinary work the conventional sequence is enough. This keeps `brakes`-system bleeding simple unless the HCU itself was opened.

> "Bleed brakes as follows: RR, LR, ABS valve, RF, LF"

## Related Concepts

- [[notes/brk-dual-split-hydraulic-system-keeps-half-the-brakes-after-a-leak|The dual split hydraulic system keeps half the brakes working after a single-circuit leak]]
- [[notes/brk-rabs-uses-one-rear-axle-speed-sensor-with-isolation-and-dump-valves|RABS uses one rear-axle speed sensor and isolation/dump valves to modulate pressure]]
- [[notes/drv-bleeding-the-concentric-clutch-slave-cylinder|Bleeding the concentric clutch slave requires the disconnect coupling, not just pedal pumping]]

## Source

- [[sources/brk-bleeding|Brake Bleeding (FSM)]]
