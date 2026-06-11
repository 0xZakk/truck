---
title: "RABS uses one rear-axle speed sensor and isolation/dump valves to modulate pressure"
kind: how-it-works
source: "[[sources/brk-rabs-antilock|Rear Anti-Lock Brake System (RABS) (FSM)]]"
related:
  - "[[notes/brk-rabs-modulates-only-the-rear-wheels-above-5-mph|RABS prevents only rear-wheel lockup, modulating rear pressure above ~5 mph]]"
  - "[[notes/brk-low-fluid-grounds-the-warning-switch-disabling-abs-and-lighting-the-indicator|Low master-cylinder fluid grounds the warning switch, disabling ABS and lighting the indicator]]"
tags: [brakes, rabs, wheel-speed-sensor, electronic-brake-control-module, abs]
---

RABS reads rear wheel speed from a single sensor in the rear axle housing: a toothed sensor ring mounted on the ring gear sweeps past the sensor pole piece, inducing an AC voltage whose frequency and amplitude are proportional to average rear wheel speed. The electronic control module watches this signal for an impending lockup.

When deceleration is too rapid, the module energizes the RABS valve (a dual-solenoid electro-hydraulic valve on the left frame rail behind the No. 1 crossmember). First the isolation valve closes, cutting the rear wheel cylinders off from the master cylinder so rear pressure can't rise. If still locking, the dump solenoid is pulsed to bleed rear-cylinder fluid into an accumulator built into the RABS valve, dropping rear pressure so the wheels spin back up. The two solenoids are pulsed together to keep the wheels rotating at high deceleration; on pedal release the isolation valve opens and accumulator fluid returns to the master cylinder. RABS II in the `brakes` system also includes a yellow REAR ABS light, a diagnostic connector, a diode/resistor element under the power distribution box, and a self-test-capable module — and a low fluid level disables it.

> "First the isolation valve closes... With the isolation valve closed, the rear wheel cylinders are isolated from the brake master cylinder and the rear brake pressure cannot increase... the antilock electronic control module will energize the dump solenoid... to bleed off rear wheel cylinder fluid into an accumulator."

## Related Concepts

- [[notes/brk-rabs-modulates-only-the-rear-wheels-above-5-mph|RABS prevents only rear-wheel lockup, modulating rear pressure above ~5 mph]]
- [[notes/brk-low-fluid-grounds-the-warning-switch-disabling-abs-and-lighting-the-indicator|Low master-cylinder fluid grounds the warning switch, disabling ABS and lighting the indicator]]

## Source

- [[sources/brk-rabs-antilock|Rear Anti-Lock Brake System (RABS) (FSM)]]
