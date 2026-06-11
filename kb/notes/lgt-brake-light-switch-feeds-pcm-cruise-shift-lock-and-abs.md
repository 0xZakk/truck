---
title: "The brake light switch feeds the PCM, cruise control, shift lock and ABS, not just the stop lamps"
kind: how-it-works
source: "[[sources/lgt-brake-light-switch|Brake (Stop) Light Switch — Description and Service (FSM)]]"
related:
  - "[[notes/lgt-a-failed-brake-light-switch-can-disable-cruise-and-torque-converter-unlock|A failed brake light switch shows up as cruise or torque-converter symptoms, not just dark stop lamps]]"
tags:
  - brake-light-switch
  - stop-lamp
  - speed-control
  - lighting
---

The pedal-mounted brake on/off switch on the 1994 F-150 is a hub for several systems. Beyond
lighting the stop lamps, it sends a brake-applied signal to the Powertrain Control Module
(PCM) to disengage the torque converter clutch when you brake — though the PCM may ignore
that signal if the throttle position is above closed throttle. The same switch supplies a
brakes-applied signal to the speed control (cruise) system for deactivation, to the shift
lock actuator, and to the anti-lock brake module.

Understanding this fan-out matters for diagnosis: one switch failure can ripple into the
transmission, cruise control, and the column shift interlock all at once. This is part of
the truck's `electrical-body` system.

> "It also provides a brakes-applied signal to the speed control system (for deactivation),
> the shift lock actuator, and the anti-lock brake module."

## Related Concepts

- [[notes/lgt-a-failed-brake-light-switch-can-disable-cruise-and-torque-converter-unlock|A failed brake light switch shows up as cruise or torque-converter symptoms, not just dark stop lamps]]
- [[notes/crz-cruise-has-multiple-independent-deactivation-paths|Cruise control has several independent deactivation paths so braking always disengages it]]
- [[notes/crz-clutch-switch-deactivates-cruise-when-pedal-depressed|On manual trucks the clutch switch deactivates cruise the moment the pedal is depressed]]
- [[notes/crz-brake-pressure-switch-opens-at-5-to-10-pounds|The brake pressure switch is a redundant deactivator that opens at 5-10 lbs of pedal pressure]]

## Source

- [[sources/lgt-brake-light-switch|Brake (Stop) Light Switch — Description and Service (FSM)]]
