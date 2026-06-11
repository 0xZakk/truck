---
title: "The seat belt reminder lamp runs for 4 to 8 seconds at key-on regardless of belt state"
kind: how-it-works
source: "[[sources/ipc-seat-belt-and-audible-warning|Seat Belt Reminder and Audible Warning (Chime) Module — Description and Operation (FSM)]]"
related:
  - "[[notes/rly-warning-chime-module-sounds-for-key-in-lights-on-and-unbuckled-belt|The warning chime module sounds for key-in-ignition, lights-on-with-door-open, and unbuckled belt]]"
tags:
  - seat-belt-reminder
  - warning-indicators
  - warning-chime
---

The seat belt reminder on the 1994 F-150 is a continuous-loop system with a warning
indicator switch, a warning lamp, and a chime. Its timing is fixed and worth memorizing for
diagnosis. When the key is turned to ON, the "fasten belts" lamp is driven for 4 to 8 seconds
no matter whether the belt is buckled — so a brief lamp at key-on is normal, not a fault.

The chime, by contrast, is conditional on belt state. If the belt is unbuckled at key-ON,
both the lamp and chime run for the 4-8 second window; buckling during that window shuts both
off. If the belt is already buckled before the key reaches ON, the lamp shows for 4-8 seconds
with no chime at all. Knowing this lets you tell "working as designed" from a real fault: a
lamp that never lights, never extinguishes, or a chime that ignores belt state indicates a
problem in the switch, lamp, or chime module within the `electrical-body` / `interior`
systems.

## Related Concepts

- [[notes/rly-warning-chime-module-sounds-for-key-in-lights-on-and-unbuckled-belt|The warning chime module sounds for key-in-ignition, lights-on-with-door-open, and unbuckled belt]]

## Source

- [[sources/ipc-seat-belt-and-audible-warning|Seat Belt Reminder and Audible Warning (Chime) Module — Description and Operation (FSM)]]
