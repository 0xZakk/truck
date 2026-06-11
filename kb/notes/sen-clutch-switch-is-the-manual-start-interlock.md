---
title: "On the manual F-150 the clutch pedal switch is the start interlock and feeds the starter relay only when the pedal is down"
kind: troubleshooting
source: "[[sources/sen-clutch-pedal-position-switch|Clutch Pedal Position Switch (Manual Transmission Start Interlock) — Description and Operation (FSM)]]"
related:
  - "[[notes/sen-tripped-inertia-switch-causes-crank-no-start|A tripped inertia switch is a common crank-no-start cause and must be manually reset]]"
tags:
  - clutch-switch
  - start-interlock
  - electrical-body
  - no-crank
---

Because this truck has the M5OD-R2 5-speed manual, its start interlock is a clutch pedal
position switch rather than a neutral safety switch. The switch sits in series with the starter
relay control circuit: pressing the clutch pedal closes it and lets voltage reach the starter
relay; with the pedal up the circuit is open and the relay never pulls in, so the starter
doesn't crank.

For the `electrical-body` and starting circuits, this makes the clutch switch a prime suspect
in no-crank complaints — especially the telltale pattern where the truck only cranks if you
"stand on" the clutch, or won't crank at all after the switch drifts out of adjustment, wears,
or unplugs. The battery, relay, and starter can all test fine while a 10-cent switch blocks the
trigger signal.

A quick check is to verify continuity through the switch with the pedal fully depressed and an
open with it released; no continuity when pressed points at the switch or its adjustment. This
is the manual-transmission analog of diagnosing an automatic's neutral safety switch.

## Related Concepts

- [[notes/sen-tripped-inertia-switch-causes-crank-no-start|A tripped inertia switch is a common crank-no-start cause and must be manually reset]]
- [[notes/chg-clutch-switch-is-an-in-series-interlock-to-the-starter-relay|The starting interlock switch sits in series between the start signal and the starter relay]]
- [[notes/clutch-pedal-position-switch-is-the-start-interlock-on-manual-f150|The clutch pedal position switch is the start interlock on a manual F-150]]
- [[notes/chg-park-neutral-switch-both-closes-the-relay-and-lights-backup-lamps|On automatics, the park/neutral switch both closes the starter relay and lights the backup lamps]]
- [[notes/crz-clutch-switch-deactivates-cruise-when-pedal-depressed|On manual trucks the clutch switch deactivates cruise the moment the pedal is depressed]]

## Source

- [[sources/sen-clutch-pedal-position-switch|Clutch Pedal Position Switch (Manual Transmission Start Interlock) — Description and Operation (FSM)]]
