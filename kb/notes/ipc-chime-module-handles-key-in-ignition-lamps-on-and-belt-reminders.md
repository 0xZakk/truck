---
title: "The chime module drives key-in-ignition, lamps-on, and seat-belt reminders from separate inputs"
kind: how-it-works
source: "[[sources/ipc-seat-belt-and-audible-warning|Seat Belt Reminder and Audible Warning (Chime) Module — Description and Operation (FSM)]]"
related:
  - "[[notes/ipc-seat-belt-reminder-runs-4-to-8-seconds-at-key-on|The seat belt reminder lamp runs for 4 to 8 seconds at key-on regardless of belt state]]"
tags:
  - audible-warning-device
  - warning-chime
  - warning-indicators
---

A single audible warning device (buzzer/chime) control module produces all the truck's
reminder chimes, switching between behaviors based on which input is active:

- Key-In-Ignition input: a ground signal tells the module the keys are still in the ignition,
  triggering the key-reminder chime.
- Lamps-On input: with the main light switch in PARK or HEAD, voltage reaches this input; the
  chime sounds when the driver's door is opened, until the door is closed or the lamps are
  shut off (the headlights-left-on reminder).
- Seat-Belt-Buckled input: with the belt unbuckled and power applied, a ground signal starts
  an electronic timer that sounds the chime for six seconds.
- Seat-Belt-Lamp output: in START or RUN the module turns on the fasten-belts indicator for
  four to eight seconds regardless of belt state.

Understanding that one module multiplexes these reminders explains why a single failed chime
module can knock out several unrelated-seeming warnings at once. The module sits in the
`electrical-body` / `interior` warning electronics.

## Related Concepts

- [[notes/ipc-seat-belt-reminder-runs-4-to-8-seconds-at-key-on|The seat belt reminder lamp runs for 4 to 8 seconds at key-on regardless of belt state]]
- [[notes/rly-warning-chime-module-sounds-for-key-in-lights-on-and-unbuckled-belt|The warning chime module sounds for key-in-ignition, lights-on-with-door-open, and unbuckled belt]]

## Source

- [[sources/ipc-seat-belt-and-audible-warning|Seat Belt Reminder and Audible Warning (Chime) Module — Description and Operation (FSM)]]
