---
title: "The warning chime module sounds for key-in-ignition, lights-on-with-door-open, and unbuckled belt"
kind: how-it-works
source: "[[sources/rly-body-control-modules|Body Control Modules — Warning Chime, Alarm, Keyless Entry, Wiper, PSOM, Starter Relay (FSM)]]"
related:
  - "[[notes/rly-alarm-module-disables-starting-and-flashes-lamps-at-80-cycles-per-minute|The alarm module disables the starting system and flashes the lamps at 80 cycles per minute when triggered]]"
  - "[[notes/rly-psom-converts-the-abs-speed-sensor-signal-to-8000-pulses-per-mile|The PSOM converts the ABS differential speed sensor input to a standard 8000 pulses-per-mile signal]]"
tags:
  - warning-chime
  - audible-warning-module
  - instrument-panel
  - relays-and-modules
---

The Audible Warning Device Control Module (warning buzzer/chime module) drives the chime from
several distinct inputs, which is useful when diagnosing a chime that sounds at the wrong time. A
key-in-ignition ground signal warns the keys are still in the ignition. A lamps-on input (main
switch in PARK or HEAD) sounds the chime when the driver's door is opened, continuing until the
door closes or the lights go off.

A seat-belt-unbuckled input grounds an electronic timer to sound the chime for six seconds, and a
seat-belt lamp output lights the "fasten belts" indicator for four to eight seconds at START or RUN
regardless of whether the belts are buckled. Knowing each trigger lets you map a misbehaving chime
to the specific input (key switch, lamp circuit, door switch, or belt switch) in the
`electrical-body` instrument-panel wiring.

## Related Concepts

- [[notes/rly-alarm-module-disables-starting-and-flashes-lamps-at-80-cycles-per-minute|The alarm module disables the starting system and flashes the lamps at 80 cycles per minute when triggered]]
- [[notes/rly-psom-converts-the-abs-speed-sensor-signal-to-8000-pulses-per-mile|The PSOM converts the ABS differential speed sensor input to a standard 8000 pulses-per-mile signal]]
- [[notes/ipc-chime-module-handles-key-in-ignition-lamps-on-and-belt-reminders|The chime module drives key-in-ignition, lamps-on, and seat-belt reminders from separate inputs]]
- [[notes/ipc-seat-belt-reminder-runs-4-to-8-seconds-at-key-on|The seat belt reminder lamp runs for 4 to 8 seconds at key-on regardless of belt state]]

## Source

- [[sources/rly-body-control-modules|Body Control Modules — Warning Chime, Alarm, Keyless Entry, Wiper, PSOM, Starter Relay (FSM)]]
