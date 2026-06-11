---
title: "On manual trucks the clutch switch deactivates cruise the moment the pedal is depressed"
kind: how-it-works
source: "[[sources/crz-control-switch-and-clutch-switch|Speed Control Switch and Clutch Switch — Description and Operation (FSM)]]"
related:
  - "[[notes/crz-cruise-has-multiple-independent-deactivation-paths|Cruise control has several independent deactivation paths so braking always disengages it]]"
  - "[[notes/chg-clutch-switch-is-an-in-series-interlock-to-the-starter-relay|The starting interlock switch sits in series between the start signal and the starter relay]]"
tags:
  - cruise-control
  - clutch-switch
  - how-it-works
---

On manual-transmission F-150s the clutch switch deactivates the speed control system when the
clutch pedal is depressed. This prevents cruise from continuing to command throttle while the
clutch is disengaged, which would otherwise let the engine race or the truck lurch when the
clutch re-engages.

This is a cruise-specific function distinct from the clutch switch's better-known role as the
manual-transmission start interlock. On the `electrical-body` system, when chasing a cruise
fault that mimics "won't stay engaged," include the clutch switch and its circuit alongside
the brake inputs as a possible cause — a clutch switch stuck in the depressed (open) state
keeps cruise from ever holding.

> "Deactivates the speed control system when the clutch pedal is depressed."

## Related Concepts

- [[notes/crz-cruise-has-multiple-independent-deactivation-paths|Cruise control has several independent deactivation paths so braking always disengages it]]
- [[notes/chg-clutch-switch-is-an-in-series-interlock-to-the-starter-relay|The starting interlock switch sits in series between the start signal and the starter relay]]
- [[notes/lgt-brake-light-switch-feeds-pcm-cruise-shift-lock-and-abs|The brake light switch feeds the PCM, cruise control, shift lock and ABS, not just the stop lamps]]
- [[notes/crz-control-switch-sends-set-coast-accel-resume-to-amplifier|The steering-wheel speed control switch tells the amplifier to set, hold, coast, or accelerate]]
- [[notes/lgt-a-failed-brake-light-switch-can-disable-cruise-and-torque-converter-unlock|A failed brake light switch shows up as cruise or torque-converter symptoms, not just dark stop lamps]]

## Source

- [[sources/crz-control-switch-and-clutch-switch|Speed Control Switch and Clutch Switch — Description and Operation (FSM)]]
