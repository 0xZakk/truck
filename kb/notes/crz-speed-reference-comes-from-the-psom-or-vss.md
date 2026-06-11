---
title: "Cruise control regulates against the speed signal from the PSOM or VSS"
kind: how-it-works
source: "[[sources/crz-speed-control-system-overview|Cruise Control (Speed Control) System — Description, Operation, Service Precautions (FSM)]]"
related:
  - "[[notes/crz-speed-control-holds-throttle-with-an-electronic-servo-and-cable|Cruise control holds speed with an electronic servo that pulls the throttle through an actuator cable]]"
  - "[[notes/sen-vehicle-speed-flows-through-the-psom|Vehicle speed reaches the PCM through the PSOM, which converts the axle sensor signal to 8000 pulses per mile]]"
tags:
  - cruise-control
  - psom
  - vehicle-speed-sensor
  - how-it-works
---

The speed control servo/amplifier does not measure speed itself — it regulates against the
vehicle speed signal supplied by the Programmable Speedometer/Odometer Module (PSOM) or the
Vehicle Speed Sensor (VSS), which is mounted on the transaxle. The servo increases or
decreases throttle to drive that measured speed toward the set speed.

This shared dependency is important for diagnosis on the `electrical-body` system: because the
PSOM/VSS speed signal also feeds the speedometer and the powertrain, a speed-signal fault can
present simultaneously as a dead or erratic speedometer and as cruise control that surges,
won't hold, or won't engage. Confirm the speed signal is good before condemning the servo.

> "The speed signal is generated either by the Programmable Speedometer/Odometer Module (PSOM)
> or the Vehicle Speed Sensor (VSS)."

## Related Concepts

- [[notes/crz-speed-control-holds-throttle-with-an-electronic-servo-and-cable|Cruise control holds speed with an electronic servo that pulls the throttle through an actuator cable]]
- [[notes/sen-vehicle-speed-flows-through-the-psom|Vehicle speed reaches the PCM through the PSOM, which converts the axle sensor signal to 8000 pulses per mile]]
- [[notes/crz-control-switch-sends-set-coast-accel-resume-to-amplifier|The steering-wheel speed control switch tells the amplifier to set, hold, coast, or accelerate]]
- [[notes/crz-cruise-engages-only-above-about-30-mph|Cruise control will only engage above about 30 mph]]
- [[notes/ipc-speedometer-is-electronic-psom-fed-by-the-abs-sensor|The 1994 F-150 speedometer is an electronic PSOM fed by the ABS/differential speed sensor, not a cable]]

## Source

- [[sources/crz-speed-control-system-overview|Cruise Control (Speed Control) System — Description, Operation, Service Precautions (FSM)]]
