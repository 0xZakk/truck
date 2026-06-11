---
title: "The anti-theft controller module monitors vehicle switches and, when triggered, sounds the horn and flashes the lamps at 80 cycles per minute"
kind: how-it-works
source: "[[sources/acc-anti-theft-alarm-system|Anti-Theft / Alarm System — Alarm Module and Arm/Disarm Switch (FSM)]]"
related:
  - "[[notes/acc-anti-theft-disables-the-starting-system-until-disarmed|The anti-theft system disables the starting system until it is disarmed]]"
  - "[[notes/acc-door-disarm-switch-grounds-the-controller-when-the-door-is-key-unlocked|A door disarm switch grounds the controller when its door is unlocked with the key, disabling the anti-theft system]]"
  - "[[notes/bdy-keyless-module-coordinates-locks-anti-theft-lamps-and-panic|The keyless entry module coordinates door locks, anti-theft arming, interior lamps, and the panic alarm]]"
tags:
  - anti-theft
  - alarm
  - alarm-module
  - how-it-works
---

The optional anti-theft system on the 1994 F-150 is centered on an anti-theft controller
module (the alarm module). Its job is to monitor a set of switches located throughout the
vehicle — door, hood, and similar trigger points — while the system is armed. If any monitored
switch is triggered while armed, the module fires the alarm: it sounds the horn and flashes the
headlamps and parking lamps together at an intermittent rate of 80 cycles per minute.

This makes the module a pure output/decision stage. Arming and disarming come from elsewhere
(the keyless entry module's LOCK command arms it; a key-unlocked door disarms it), but the
flash-and-honk response itself is the alarm module's behavior. For diagnosis on the truck
inventory `electrical-body` system, a horn that honks and lamps that flash in unison at that
steady ~80 cpm cadence is the signature of the anti-theft module doing its job, not a wiring
short — the question becomes why it was triggered or why it failed to disarm.

## Related Concepts

- [[notes/acc-anti-theft-disables-the-starting-system-until-disarmed|The anti-theft system disables the starting system until it is disarmed]]
- [[notes/acc-door-disarm-switch-grounds-the-controller-when-the-door-is-key-unlocked|A door disarm switch grounds the controller when its door is unlocked with the key, disabling the anti-theft system]]
- [[notes/bdy-keyless-module-coordinates-locks-anti-theft-lamps-and-panic|The keyless entry module coordinates door locks, anti-theft arming, interior lamps, and the panic alarm]]
- [[notes/rly-alarm-module-disables-starting-and-flashes-lamps-at-80-cycles-per-minute|The alarm module disables the starting system and flashes the lamps at 80 cycles per minute when triggered]]

## Source

- [[sources/acc-anti-theft-alarm-system|Anti-Theft / Alarm System — Alarm Module and Arm/Disarm Switch (FSM)]]
