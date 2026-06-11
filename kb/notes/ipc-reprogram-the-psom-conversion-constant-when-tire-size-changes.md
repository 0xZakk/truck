---
title: "Reprogram the PSOM conversion constant whenever tire size changes"
kind: procedure
source: "[[sources/ipc-speedometer-psom|Speedometer / Programmable Speedometer-Odometer Module (PSOM) — Description and Operation (FSM)]]"
related:
  - "[[notes/ipc-speedometer-is-electronic-psom-fed-by-the-abs-sensor|The 1994 F-150 speedometer is an electronic PSOM fed by the ABS/differential speed sensor, not a cable]]"
tags:
  - speedometer
  - psom
  - procedure
  - instrument-cluster
---

Because the PSOM converts the raw speed-sensor pulses into a calibrated speed using a
programmed conversion constant, that constant is tied to the truck's tire size. The FSM
flags it as VERY IMPORTANT: change the speedometer's internal conversion constant whenever
the tire size on the vehicle is changed.

There are two reasons this matters beyond a wrong needle. First, accuracy — setting the
proper value keeps the speedometer and odometer at their original factory-set accuracy after
a tire change. Second, downstream systems — the PSOM's 8000-pulses-per-mile output also
feeds the EEC engine control module and the speed control, so an unadjusted constant after a
tire swap can degrade those systems, not just the displayed speed. Practically: any time you
move to a non-stock tire diameter on this 2WD F-150, plan to reprogram the PSOM constant.
This work touches the `interior` cluster and `electrical-body` systems.

## Related Concepts

- [[notes/ipc-speedometer-is-electronic-psom-fed-by-the-abs-sensor|The 1994 F-150 speedometer is an electronic PSOM fed by the ABS/differential speed sensor, not a cable]]
- [[notes/rly-psom-converts-the-abs-speed-sensor-signal-to-8000-pulses-per-mile|The PSOM converts the ABS differential speed sensor input to a standard 8000 pulses-per-mile signal]]
- [[notes/sen-vehicle-speed-flows-through-the-psom|Vehicle speed reaches the PCM through the PSOM, which converts the axle sensor signal to 8000 pulses per mile]]

## Source

- [[sources/ipc-speedometer-psom|Speedometer / Programmable Speedometer-Odometer Module (PSOM) — Description and Operation (FSM)]]
