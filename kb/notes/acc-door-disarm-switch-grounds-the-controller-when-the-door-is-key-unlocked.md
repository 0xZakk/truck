---
title: "A door disarm switch grounds the controller when its door is unlocked with the key, disabling the anti-theft system"
kind: how-it-works
source: "[[sources/acc-anti-theft-alarm-system|Anti-Theft / Alarm System — Alarm Module and Arm/Disarm Switch (FSM)]]"
related:
  - "[[notes/acc-anti-theft-module-monitors-switches-and-flashes-lamps-at-80-cpm|The anti-theft controller module monitors vehicle switches and, when triggered, sounds the horn and flashes the lamps at 80 cycles per minute]]"
  - "[[notes/acc-anti-theft-disables-the-starting-system-until-disarmed|The anti-theft system disables the starting system until it is disarmed]]"
tags:
  - anti-theft
  - arm-disarm-switch
  - door-locks
  - how-it-works
---

The 1994 F-150's anti-theft system is disarmed through door disarm switches. Each switch is
closed when its door is unlocked with the key, and in the closed state it provides a ground
input to the anti-theft controller module. That ground is the signal the controller reads as
"a legitimate key-holder is entering," and it disables the anti-theft system.

This is the mechanical-key counterpart to the keyless entry module's electronic UNLOCK
command. It also explains a real-world quirk: unlocking with the physical key is what releases
the system, so a faulty or disconnected door disarm switch can leave the controller unable to
disarm — keeping the alarm armed and the starter inhibited even after the owner unlocks the
door. On the truck inventory `interior` and `electrical-body` systems, this switch is therefore
a prime suspect when the alarm refuses to clear via the key.

## Related Concepts

- [[notes/acc-anti-theft-module-monitors-switches-and-flashes-lamps-at-80-cpm|The anti-theft controller module monitors vehicle switches and, when triggered, sounds the horn and flashes the lamps at 80 cycles per minute]]
- [[notes/acc-anti-theft-disables-the-starting-system-until-disarmed|The anti-theft system disables the starting system until it is disarmed]]
- [[notes/bdy-keyless-module-coordinates-locks-anti-theft-lamps-and-panic|The keyless entry module coordinates door locks, anti-theft arming, interior lamps, and the panic alarm]]
- [[notes/rly-alarm-module-disables-starting-and-flashes-lamps-at-80-cycles-per-minute|The alarm module disables the starting system and flashes the lamps at 80 cycles per minute when triggered]]
- [[notes/bdy-keyless-transmitters-are-programmed-by-shorting-the-j2-connector|Up to four keyless transmitters are programmed by shorting the J2 connector with the ignition on]]

## Source

- [[sources/acc-anti-theft-alarm-system|Anti-Theft / Alarm System — Alarm Module and Arm/Disarm Switch (FSM)]]
