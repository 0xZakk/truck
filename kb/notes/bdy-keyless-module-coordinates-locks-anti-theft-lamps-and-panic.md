---
title: "The keyless entry module coordinates door locks, anti-theft arming, interior lamps, and the panic alarm"
kind: how-it-works
source: "[[sources/bdy-keyless-entry-system|Keyless Entry System (Module + Transmitter) — Description, Operation and Programming (FSM)]]"
related:
  - "[[notes/bdy-keyless-transmitters-are-programmed-by-shorting-the-j2-connector|Up to four keyless transmitters are programmed by shorting the J2 connector with the ignition on]]"
tags:
  - keyless-entry
  - anti-theft
  - door-locks
  - how-it-works
---

On the 1994 F-150, the optional remote keyless entry is not a set of independent gadgets but a
single electronic door lock control (keyless entry module) that listens to two inputs — the
remote transmitter and the power door lock switch — and drives several outputs from them.
A LOCK command both locks the doors and arms the anti-theft system; an UNLOCK command unlocks
and disarms.

The module also owns convenience and alarm behaviors. Pressing UNLOCK or PANIC lights the
interior lamps for about 25 seconds, and pressing LOCK or turning the ignition to RUN kills
them immediately. PANIC tells the anti-theft module to flash the exterior lights and sound the
horn for about four minutes, and a second PANIC press cancels it. Understanding that one module
mediates all of this matters for diagnosis: a fault that affects locks, dome lamp timing, and
the panic alarm together points at the module or its power/ground, not at three separate
circuits. This is part of the truck inventory `body-cab` system (locks and interior lamps) with
`exterior-trim` outputs (exterior lights and horn).

## Related Concepts

- [[notes/bdy-keyless-transmitters-are-programmed-by-shorting-the-j2-connector|Up to four keyless transmitters are programmed by shorting the J2 connector with the ignition on]]
- [[notes/acc-anti-theft-module-monitors-switches-and-flashes-lamps-at-80-cpm|The anti-theft controller module monitors vehicle switches and, when triggered, sounds the horn and flashes the lamps at 80 cycles per minute]]
- [[notes/acc-door-disarm-switch-grounds-the-controller-when-the-door-is-key-unlocked|A door disarm switch grounds the controller when its door is unlocked with the key, disabling the anti-theft system]]
- [[notes/rly-alarm-module-disables-starting-and-flashes-lamps-at-80-cycles-per-minute|The alarm module disables the starting system and flashes the lamps at 80 cycles per minute when triggered]]
- [[notes/acc-anti-theft-disables-the-starting-system-until-disarmed|The anti-theft system disables the starting system until it is disarmed]]

## Source

- [[sources/bdy-keyless-entry-system|Keyless Entry System (Module + Transmitter) — Description, Operation and Programming (FSM)]]
