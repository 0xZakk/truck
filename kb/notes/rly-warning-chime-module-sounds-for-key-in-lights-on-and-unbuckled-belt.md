---
title: "The warning chime module sounds for key-in-ignition, lights-on-with-door-open, and unbuckled belt"
kind: how-it-works
source: "[[sources/rly-body-control-modules|Body Control Modules — Warning Chime, Alarm, Keyless Entry, Wiper, PSOM, Starter Relay (FSM)]]"
related:
  - "[[notes/rly-alarm-module-disables-starting-and-flashes-lamps-at-80-cycles-per-minute|The alarm module disables the starting system and flashes the lamps at 80 cycles per minute when triggered]]"
  - "[[notes/ipc-speedometer-is-electronic-psom-fed-by-the-abs-sensor|The 1994 F-150 speedometer is an electronic PSOM fed by the ABS/differential speed sensor, not a cable]]"
tags:
  - warning-chime
  - audible-warning-device
  - audible-warning-module
  - warning-indicators
  - instrument-panel
  - relays-and-modules
---

A single Audible Warning Device Control Module (warning buzzer/chime module) produces all the
truck's reminder chimes, switching between behaviors based on which distinct input is active —
useful when diagnosing a chime that sounds at the wrong time:

- Key-In-Ignition input: a ground signal tells the module the keys are still in the ignition,
  triggering the key-reminder chime.
- Lamps-On input: with the main light switch in PARK or HEAD, voltage reaches this input and the
  chime sounds when the driver's door is opened, continuing until the door is closed or the lamps
  are shut off (the headlights-left-on reminder).
- Seat-Belt-Unbuckled input: with the belt unbuckled and power applied, a ground signal starts an
  electronic timer that sounds the chime for six seconds.
- Seat-Belt-Lamp output: in START or RUN the module lights the "fasten belts" indicator for four to
  eight seconds regardless of whether the belts are buckled.

Understanding that one module multiplexes these reminders explains why a single failed chime module
can knock out several unrelated-seeming warnings at once, and knowing each trigger lets you map a
misbehaving chime to the specific input (key switch, lamp circuit, door switch, or belt switch). The
module sits in the `electrical-body` / `interior` instrument-panel warning electronics.

## Related Concepts

- [[notes/rly-alarm-module-disables-starting-and-flashes-lamps-at-80-cycles-per-minute|The alarm module disables the starting system and flashes the lamps at 80 cycles per minute when triggered]]
- [[notes/ipc-seat-belt-reminder-runs-4-to-8-seconds-at-key-on|The seat belt reminder lamp runs for 4 to 8 seconds at key-on regardless of belt state]]

## Source

- [[sources/rly-body-control-modules|Body Control Modules — Warning Chime, Alarm, Keyless Entry, Wiper, PSOM, Starter Relay (FSM)]]
- [[sources/ipc-seat-belt-and-audible-warning|Seat Belt Reminder and Audible Warning (Chime) Module — Description and Operation (FSM)]]
