---
title: "The anti-theft system disables the starting system until it is disarmed"
kind: troubleshooting
source: "[[sources/acc-anti-theft-alarm-system|Anti-Theft / Alarm System — Alarm Module and Arm/Disarm Switch (FSM)]]"
related:
  - "[[notes/acc-anti-theft-module-monitors-switches-and-flashes-lamps-at-80-cpm|The anti-theft controller module monitors vehicle switches and, when triggered, sounds the horn and flashes the lamps at 80 cycles per minute]]"
  - "[[notes/acc-door-disarm-switch-grounds-the-controller-when-the-door-is-key-unlocked|A door disarm switch grounds the controller when its door is unlocked with the key, disabling the anti-theft system]]"
tags:
  - anti-theft
  - alarm
  - no-start
  - troubleshooting
---

Beyond the audible/visual alarm, the anti-theft controller module on the 1994 F-150 also
disables the starting system, and it keeps the starter disabled until the anti-theft system is
disarmed. This is a starter-inhibit feature, distinct from the horn-and-lamp alarm.

For a no-crank diagnosis this is an important branch to rule out on trucks equipped with the
option. If the engine will not crank on a vehicle with factory anti-theft, confirm the system
is actually disarmed — unlock a door with the key, which grounds the controller through the
door disarm switch and disables the system — before chasing the usual starter, relay, or
clutch/neutral interlock causes. On the truck inventory `electrical-body` system, a fault or
miscommunication that leaves the anti-theft module thinking it is still armed presents exactly
as a dead starter with otherwise normal electrics.

## Related Concepts

- [[notes/acc-anti-theft-module-monitors-switches-and-flashes-lamps-at-80-cpm|The anti-theft controller module monitors vehicle switches and, when triggered, sounds the horn and flashes the lamps at 80 cycles per minute]]
- [[notes/acc-door-disarm-switch-grounds-the-controller-when-the-door-is-key-unlocked|A door disarm switch grounds the controller when its door is unlocked with the key, disabling the anti-theft system]]
- [[notes/rly-alarm-module-disables-starting-and-flashes-lamps-at-80-cycles-per-minute|The alarm module disables the starting system and flashes the lamps at 80 cycles per minute when triggered]]
- [[notes/bdy-keyless-module-coordinates-locks-anti-theft-lamps-and-panic|The keyless entry module coordinates door locks, anti-theft arming, interior lamps, and the panic alarm]]

## Source

- [[sources/acc-anti-theft-alarm-system|Anti-Theft / Alarm System — Alarm Module and Arm/Disarm Switch (FSM)]]
