---
title: "The brake pressure switch is a redundant deactivator that opens at 5-10 lbs of pedal pressure"
kind: spec
source: "[[sources/crz-brake-deactivation-switches|Cruise Control Brake Switches — Brake On/Off Switch and Brake Pressure (Deactivator) Switch (FSM)]]"
related:
  - "[[notes/crz-cruise-has-multiple-independent-deactivation-paths|Cruise control has several independent deactivation paths so braking always disengages it]]"
tags:
  - cruise-control
  - brake-pressure-switch
  - spec
  - deactivation
---

The brake pressure switch is the redundant safety deactivator for cruise control. Under
increased brake pedal pressure of 5-10 lbs it opens and removes power from the servo clutch,
dropping the system independently of the electrical brake on/off (stop-lamp) signal.

The 5-10 lb threshold is the spec to keep in mind: it is light brake-pedal effort, so cruise
should release with the first deliberate brake application, not only under hard braking. On
the `electrical-body` system, a brake pressure switch that fails to open (or one wired/plumbed
incorrectly) is exactly what the FSM's pinpoint test J — "Speed Control Does Not Disengage
When Brakes Applied" — exists to catch.

> "Under increased brake pedal pressure (5-10 lbs), the switch will open and remove power from
> the servo clutch."

## Related Concepts

- [[notes/crz-cruise-has-multiple-independent-deactivation-paths|Cruise control has several independent deactivation paths so braking always disengages it]]
- [[notes/lgt-brake-light-switch-feeds-pcm-cruise-shift-lock-and-abs|The brake light switch feeds the PCM, cruise control, shift lock and ABS, not just the stop lamps]]

## Source

- [[sources/crz-brake-deactivation-switches|Cruise Control Brake Switches — Brake On/Off Switch and Brake Pressure (Deactivator) Switch (FSM)]]
