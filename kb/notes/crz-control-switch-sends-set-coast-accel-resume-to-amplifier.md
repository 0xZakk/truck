---
title: "The steering-wheel speed control switch tells the amplifier to set, hold, coast, or accelerate"
kind: how-it-works
source: "[[sources/crz-control-switch-and-clutch-switch|Speed Control Switch and Clutch Switch — Description and Operation (FSM)]]"
related:
  - "[[notes/crz-speed-control-holds-throttle-with-an-electronic-servo-and-cable|Cruise control holds speed with an electronic servo that pulls the throttle through an actuator cable]]"
  - "[[notes/crz-disarm-the-air-bag-before-working-on-the-cruise-switches|Disarm the air bag before servicing the steering-wheel cruise switches]]"
tags:
  - cruise-control
  - speed-control-switch
  - how-it-works
---

The driver's only direct interface to the cruise system is the speed control switch mounted in
the steering wheel. It signals the speed control amplifier to activate or deactivate the
system, to set and hold the current vehicle speed, to accelerate, or to coast. The amplifier
then commands the servo accordingly; the switch carries no actuation power itself, only the
driver's intent.

Because each function (On/Off, Set-Acc, Coast, Resume) is a separate signal to the amplifier,
the FSM's pinpoint tests are likewise split by function — there are individual tests for the
"On" switch, accel/tap-up, coast/tap-down, and resume. On the `electrical-body` system that
means a complaint like "resume doesn't work but set does" points at one switch contact or its
wire, not the whole servo.

> "Signals the speed control amplifier to activate or deactivate the speed control system, to
> set and hold vehicle speed, to accelerate, or to coast."

## Related Concepts

- [[notes/crz-speed-control-holds-throttle-with-an-electronic-servo-and-cable|Cruise control holds speed with an electronic servo that pulls the throttle through an actuator cable]]
- [[notes/crz-disarm-the-air-bag-before-working-on-the-cruise-switches|Disarm the air bag before servicing the steering-wheel cruise switches]]
- [[notes/crz-speed-reference-comes-from-the-psom-or-vss|Cruise control regulates against the speed signal from the PSOM or VSS]]
- [[notes/crz-cruise-pinpoint-tests-are-organized-by-symptom-letter|Cruise control pinpoint tests are organized by lettered symptom from A through K]]
- [[notes/crz-cruise-has-multiple-independent-deactivation-paths|Cruise control has several independent deactivation paths so braking always disengages it]]
- [[notes/crz-cruise-engages-only-above-about-30-mph|Cruise control will only engage above about 30 mph]]

## Source

- [[sources/crz-control-switch-and-clutch-switch|Speed Control Switch and Clutch Switch — Description and Operation (FSM)]]
