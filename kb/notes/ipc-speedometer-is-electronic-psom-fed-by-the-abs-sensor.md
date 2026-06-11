---
title: "The 1994 F-150 speedometer is an electronic PSOM fed by the ABS/differential speed sensor, not a cable"
kind: how-it-works
source: "[[sources/ipc-speedometer-psom|Speedometer / Programmable Speedometer-Odometer Module (PSOM) — Description and Operation (FSM)]]"
related:
  - "[[notes/ipc-reprogram-the-psom-conversion-constant-when-tire-size-changes|Reprogram the PSOM conversion constant whenever tire size changes]]"
tags:
  - speedometer
  - psom
  - abs
  - instrument-cluster
  - vehicle-speed
---

Despite the "Speedometer Cable" folder in the manual, the 1994 F-150's speedometer is
electronic. The Programmable Speedometer/Odometer Module (PSOM) bundles the electric analog
speedometer, the LCD total odometer, and the trip odometer under one programmable
microprocessor. Its speed input comes from the Differential Speed Sensor (DSS), described as
the anti-lock brake sensor, not from a rotating cable. The microprocessor applies a programmed
conversion constant to that input and outputs a standard 8000-pulses-per-mile speed signal.

Two practical points follow. First, the PSOM is serviceable only as a unit — you replace the
whole module, not internal parts. Second, the same speed signal also feeds the EEC engine
control module and speed control, so the speedometer is not an isolated gauge; a speed-sensor
or PSOM fault can ripple into engine and cruise behavior. Because the conversion constant is
internal, the FSM stresses that it MUST be changed if tire size changes, both to keep the
speedometer accurate and to keep the EEC's speed signal correct. The trip odometer is operated
with SELECT (upper right) to display and RESET (upper left) to zero. This module is the
speed-signal hub spanning the `interior` cluster, `electrical-body` instrument-panel wiring,
and the ABS sensing system.

## Related Concepts

- [[notes/ipc-reprogram-the-psom-conversion-constant-when-tire-size-changes|Reprogram the PSOM conversion constant whenever tire size changes]]
- [[notes/sen-vehicle-speed-flows-through-the-psom|Vehicle speed reaches the PCM through the PSOM, which converts the axle sensor signal to 8000 pulses per mile]]
- [[notes/crz-speed-reference-comes-from-the-psom-or-vss|Cruise control regulates against the speed signal from the PSOM or VSS]]

## Source

- [[sources/ipc-speedometer-psom|Speedometer / Programmable Speedometer-Odometer Module (PSOM) — Description and Operation (FSM)]]
- [[sources/rly-body-control-modules|Body Control Modules — Warning Chime, Alarm, Keyless Entry, Wiper, PSOM, Starter Relay (FSM)]]
