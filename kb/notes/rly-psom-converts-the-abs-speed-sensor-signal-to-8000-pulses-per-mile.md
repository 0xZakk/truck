---
title: "The PSOM converts the ABS differential speed sensor input to a standard 8000 pulses-per-mile signal"
kind: how-it-works
source: "[[sources/rly-body-control-modules|Body Control Modules — Warning Chime, Alarm, Keyless Entry, Wiper, PSOM, Starter Relay (FSM)]]"
related:
  - "[[notes/rly-warning-chime-module-sounds-for-key-in-lights-on-and-unbuckled-belt|The warning chime module sounds for key-in-ignition, lights-on-with-door-open, and unbuckled belt]]"
tags:
  - psom
  - speedometer
  - vehicle-speed
  - instrument-panel
---

The Programmable Speedometer/Odometer Module (PSOM) houses the electric analog speedometer, the
LCD odometer, and the trip odometer under a single programmable microprocessor. It takes a speed
input from the Differential Speed Sensor (the anti-lock brake sensor) and uses a programmed
conversion constant to produce a standard 8000-pulses-per-mile speed output.

That output is not just for the dash — the speedometer also supplies the vehicle-speed signal the
EEC module and speed control rely on. Because the conversion constant is internal, the FSM stresses
that it MUST be changed if tire size changes, both to keep the speedometer accurate and to keep the
EEC's speed signal correct. The PSOM is serviceable only as a unit. This module is the speed-signal
hub of the `electrical-body` instrument-panel network.

## Related Concepts

- [[notes/rly-warning-chime-module-sounds-for-key-in-lights-on-and-unbuckled-belt|The warning chime module sounds for key-in-ignition, lights-on-with-door-open, and unbuckled belt]]
- [[notes/ipc-speedometer-is-electronic-psom-fed-by-the-abs-sensor|The 1994 F-150 speedometer is an electronic PSOM fed by the ABS/differential speed sensor, not a cable]]
- [[notes/sen-vehicle-speed-flows-through-the-psom|Vehicle speed reaches the PCM through the PSOM, which converts the axle sensor signal to 8000 pulses per mile]]
- [[notes/ipc-reprogram-the-psom-conversion-constant-when-tire-size-changes|Reprogram the PSOM conversion constant whenever tire size changes]]

## Source

- [[sources/rly-body-control-modules|Body Control Modules — Warning Chime, Alarm, Keyless Entry, Wiper, PSOM, Starter Relay (FSM)]]
