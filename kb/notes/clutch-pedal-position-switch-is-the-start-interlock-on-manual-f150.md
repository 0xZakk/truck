---
title: "The clutch pedal position switch is the start interlock on a manual F-150"
kind: how-it-works
source: "[[sources/starter-motor-description-and-operation-fsm|Starter Motor — Description and Operation (FSM)]]"
related:
  - "[[notes/f150-uses-permanent-magnet-gear-reduction-starter|The 1994 F-150 uses a permanent-magnet gear-reduction starter]]"
tags:
  - starting-system
  - clutch-switch
  - interlock
  - m5od-r2
---

On automatic-transmission trucks, the starter circuit runs through a **park/neutral position
switch** so the engine only cranks in P or N. This 1994 F-150 has the **M5OD-R2 5-speed
manual**, so that role is filled instead by the **clutch pedal position switch**: you must
press the clutch to the floor to complete the start circuit.

This matters for diagnosis. A manual truck that won't crank — but has a good battery,
relay, and starter — often has a failed, misadjusted, or unplugged clutch switch. It's a
cheap part that's easy to overlook precisely because it isn't on the engine. When chasing a
no-crank on this truck, test the clutch switch rather than the neutral-safety switch an
automatic would use.

This relates to truck inventory system `electrical-starting` and the `driveline` clutch.

## Related Concepts

- [[notes/f150-uses-permanent-magnet-gear-reduction-starter|The 1994 F-150 uses a permanent-magnet gear-reduction starter]]

## Source

- [[sources/starter-motor-description-and-operation-fsm|Starter Motor — Description and Operation (FSM)]]
